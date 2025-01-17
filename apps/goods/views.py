import logging

from django import http
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View
from redis import DataError

from apps.content.utils import get_categories
from apps.goods.models import GoodsCategory, SKU
from apps.goods.utils import get_breadcrumb
from meiduo.utils.response_code import RETCODE


# Create your views here.

class HotGoodsView(View):
    """商品排行"""

    @staticmethod
    def get(request, category_id):
        skus = SKU.objects.filter(category_id=category_id).order_by("-sales")[0:2]

        hot_skus = []

        for sku in skus:
            dic = {
                "id"               : sku.id,
                "default_image_url": sku.default_image.url,
                "name"             : sku.name,
                "price"            : sku.price
            }
            hot_skus.append(dic)

        return http.JsonResponse({
            "code"    : RETCODE.OK,
            "errmsg"  : "OK",
            "hot_skus": hot_skus,
        })

class ListView(View):
        """商品列表页"""

        @staticmethod
        def get(request, category_id, page_num):

            try:
                cat3 = GoodsCategory.objects.get(id=category_id)
            except DataError:
                return http.HttpResponseForbidden('商品类别不存在')
            except Exception as e:
                logging.getLogger('django').error(e)
            # 获取商品类别
            categories = get_categories()
            # 获取面包屑导航
            breadcrumb = get_breadcrumb(cat3)

            # 按规则查找SKU信息
            sort = request.GET.get('sort', "default")
            sort_field = "default"
            if sort == "price":
                sort_field = "price"
            elif sort == "hot":
                sort_field = "-sales"
            else:
                sort = "default"
                sort_field = "create_time"

            skus = SKU.objects.filter(category_id=category_id).order_by(sort_field)
            # 创建商品分页器
            paginator = Paginator(skus, 5)
            try:
                page_skus = paginator.page(page_num)
            except EmptyPage:
                return http.HttpResponseForbidden("页数不对")
            # 获取列表页总页数
            total_page = paginator.num_pages

            context = {
                'categories': categories,  # 频道分类
                'breadcrumb': breadcrumb,  # 面包屑导航
                'sort'      : sort,  # 排序字段
                'category'  : cat3,  # 第三级分类
                'page_skus' : page_skus,  # 分页后数据
                'total_page': total_page,  # 总页数
                'page_num'  : page_num,  # 当前页码
            }

            return render(request, 'list.html', context=context)
