import json

from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from apps.carts.utils import cart_64str2py, cart_py2b64str
from apps.goods.models import SKU


# from meiduo.utils.views import LoginRequiredJSONMixin


class CartView(View):
    """购物车相关"""
    """
        {
           "sku_id1":{
               "count":"1",
               "selected":"True"
           },
           "sku_id3":{
               "count":"3",
               "selected":"True"
           },
        }
    """

    @staticmethod
    def post(request):
        """添加购物车"""

        dict = json.loads(request.body.decode())

        count = dict["count"]
        sku_id = dict["sku_id"]
        selected = dict.get("selected", True)

        # 判断是否齐全
        if not all([sku_id, count]):
            return http.HttpResponseForbidden("缺少必传参数")
        # 判断sku_id 是否存在
        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden("商品不存在")

        try:
            count = int(count)
        except Exception:
            return http.HttpResponseForbidden("参数count错误")

        user = request.user
        # 如果没有登录,返回的是一个匿名用户对象 （AnonymousUser）
        if user.is_authenticated:
            # 是登录用户
            redis_conn = get_redis_connection("carts")
            pl = redis_conn.pipeline()
            pl.hincrby("carts_%s" % user.id, sku_id, count)
            #
            if selected:
                pl.sadd("selected_%s" % user.id, sku_id)
            pl.execute()
            return http.JsonResponse({"code": 0, "errmsg": "ok"})
        else:
            # 未登录用户
            # 获取cookie中的购物车数据
            cart_str = request.COOKIES.get("cart")
            if cart_str:
                # 已经有购物车cookie数据
                cart_dict = cart_64str2py(cart_str)
            else:
                # 没有购物车cookie数据
                cart_dict = {}
                #     处理购物车数据
                if sku_id in cart_dict:
                    origin_count = cart_dict[sku_id]["count"]
                    count += origin_count
                cart_dict[sku_id] = {
                    "count"   : count,
                    "selected": selected
                }
                cookie_str = cart_py2b64str(cart_dict)
                #         字典转base64
                response = http.JsonResponse({"code": 0, "errmsg": "ok"})
                response.set_cookie("cart", cookie_str)
                return response

    @staticmethod
    def get(request):
        user = request.user
        if user.is_authenticated:
            #     登录用户
            redis_conn = get_redis_connection("carts")
            redis_cart = redis_conn.hgetall("carts_%s" % user.id)
            cart_selected = redis_conn.smembers("selected_%s" % user.id)
            # 将redis中的数据构成跟cookie中的格式一样
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    "count"   : int(count),
                    "selected": sku_id in cart_selected
                }
        else:
            #     未登录用户
            cookie_carts_str = request.COOKIES.get("carts")
            """
            {
                "sku_id1":{
                    "count":"1",
                    "selected":"True"
                },
                "sku_id3":{
                    "count":"3",
                    "selected":"True"
                },
            }
            """
            if cookie_carts_str:
                cart_dict = cart_64str2py(cookie_carts_str)
            else:
                cart_dict = {}

        # 上面已经 获取到了cookie样式的购物车数据
        sku_ids = cart_dict.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        cart_skus = []

        for sku in skus:
            cart_skus.append({
                "id":sku.id,
                "name":sku.name,
                "count":cart_dict.get(sku.id).get("count"),
                "selected":str(cart_dict.get(sku.id).get("selected")),
                "default_image_url":sku.default_image.url,
                "price":str(sku.price),
                "amount":str(sku.price * cart_dict.get(sku.id).get("count"))
            })

        context = {
            "cart_skus": cart_skus
        }

        return render(request, "cart.html", context)

    @staticmethod
    def put(request):
        """  修改购物车 """
        pass
