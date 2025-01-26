from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from apps.goods.models import SKU
from apps.users.models import Address


# Create your views here.


class OrderSettlementView(LoginRequiredMixin,View):
    """结算订单"""
    @staticmethod
    def get(request):
        # 获取登录用户
        user = request.user
        # 查询地址
        try:
            addresses = Address.objects.filter(user=user,is_delete=False)
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

        return render(request, "place_order.html",context)