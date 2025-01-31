import json
import logging
from decimal import Decimal

from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django.utils import timezone

from apps.goods.models import SKU
from apps.orders.models import OrderInfo, OrderGoods
from apps.users.models import Address
from meiduo.utils.response_code import RETCODE
from meiduo.utils.views import LoginRequiredJSONMixin
from django.db import transaction


# Create your views here.

class OrderCommitView(LoginRequiredJSONMixin, View):
    """提交订单"""

    @staticmethod
    def post(request):
        # 接收参数
        dict = json.loads(request.body.decode())
        pay_method = dict.get("pay_method")
        address_id = dict.get("address_id")
        # 校验参数
        if not all([address_id, pay_method]):
            return http.HttpResponseForbidden("缺少必传参数")

        # 判断address_id是否合法
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return http.HttpResponseForbidden("参数address_id错误")

        # 判断pay_method是否合法
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM["CASH"],
                              OrderInfo.PAY_METHODS_ENUM["ALIPAY"]]:
            return http.HttpResponseForbidden("参数pay_method错误")

        # 获取登录用户
        user = request.user
        # 生成订单编号
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)

        # 保存订单基本信息 OrderInfo(一  : 可对应多个OrderGoods商品)
        with transaction.atomic():
            save_id = transaction.savepoint()
            # 暴力回滚
            try:
                orderInfo = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal('0'),
                    freight=Decimal('10.00'),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM["UNPAID"] if pay_method ==
                                                                    OrderInfo.PAY_METHODS_ENUM[
                                                                        "ALIPAY"] else
                    OrderInfo.ORDER_STATUS_ENUM["UNSEND"],
                )

                # 2. 从redis中获取购物车中被勾选的商品信息
                redis_conn = get_redis_connection("carts")
                selected = redis_conn.smembers('selected_%s' % user.id)
                goods = redis_conn.hgetall('carts_%s' % user.id)
                # 2.1 遍历获取商品信息
                carts = {}
                for sku_id in selected:
                    count = int(goods[sku_id])
                    carts[int(sku_id)] = count
                sku_ids = carts.keys()
                # 2.2 遍历购物车中被勾选的商品信息
                for sku_id in sku_ids:
                    sku = SKU.objects.get(id=sku_id)
                    #     判断sku的库存
                    count = carts[sku_id]
                    if sku.stock < carts[sku_id]:
                        return http.JsonResponse({"code": 400, "errmsg": "商品库存不足"})
                    #     库存减少,销量增加
                    sku.stock -= count
                    sku.sales += count
                    sku.save()
                    #     修改SPU的销量
                    sku.spu.sales += count
                    sku.spu.save()

                    #     保存订单信息
                    OrderGoods.objects.create(
                        order=orderInfo,
                        sku=sku,
                        count=count,
                        price=sku.price,
                    )
                    #     保存商品订单中总价和总数量
                    orderInfo.total_count += count
                    orderInfo.total_amount = sku.price * count

                # 最后添加邮费和保存订单信息
                orderInfo.total_amount += orderInfo.freight
                orderInfo.save()


            except Exception as e:
                logging.getLogger("django").error(f"暴力回滚 --> {e}")
                transaction.savepoint_rollback(save_id)
                return http.JsonResponse({"code": RETCODE.DBERR, "errmsg": "下单失败"})

            transaction.savepoint_commit(save_id)

            # 清除购物车中已结算的商品
            pl = redis_conn.pipeline()
            pl.hdel('carts_%s' % user.id, *selected)
            pl.srem('selected_%s' % user.id, *selected)
            pl.execute()

        # 响应提交订单结果
        return http.JsonResponse(
            {"code": RETCODE.OK, "errmsg": "ok", "order_id": orderInfo.order_id})


class OrderSettlementView(LoginRequiredMixin, View):
    """结算订单"""

    @staticmethod
    def get(request):
        # 获取登录用户
        user = request.user
        # 查询地址
        try:
            addresses = Address.objects.filter(user=user, is_delete=False)
        except Address.DoesNotExist:
            addresses = None

        # 从购物车记录获取用户勾选要结算的商品信息
        redis_conn = get_redis_connection("carts")
        # pl = redis_conn.pipeline()
        selected = redis_conn.smembers('selected_%s' % user.id)
        carts = redis_conn.hgetall('carts_%s' % user.id)
        # pl.execute()
        cart = {}

        for sku_id in selected:
            temp = int(carts[sku_id])
            cart[int(sku_id)] = int(carts[sku_id])

        skus = SKU.objects.filter(id__in=cart.keys())

        total_count = 0
        total_amount = Decimal(0.00)

        for sku in skus:
            sku.count = cart[sku.id]
            sku.amount = sku.price * sku.count

            total_count += sku.count
            total_amount += sku.amount

        freight = Decimal("10.00")
        # 渲染界面
        context = {
            'addresses'     : addresses,
            'skus'          : skus,
            'total_count'   : total_count,
            'total_amount'  : total_amount,
            'freight'       : freight,
            'payment_amount': total_amount + freight,
        }

        return render(request, "place_order.html", context)
