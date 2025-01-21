import logging

from django import http
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View
from redis import DataError

from apps.content.utils import get_categories
from apps.goods.models import GoodsCategory, SKU, SPUSpecification
from apps.goods.utils import get_breadcrumb
from meiduo.utils.response_code import RETCODE


# Create your views here.

class DetailView(View):
    """详情页"""

    @staticmethod
    def get(request, sku_id):
        print(sku_id)
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return render(request, "404.html")

        # 商品分类
        categories = get_categories()
        # 面包屑导航
        breadcrumb = get_breadcrumb(sku.category)

        # 构建商品规格
        sku_specs = sku.specs.order_by("spec_id")
        # 当前sku商品的规格 比如: 颜色; 内存
        sku_key = []
        for spec in sku_specs:
            sku_key.append(spec.option.id)  # option中存放的是每个sku规格具体的名称(spec_option)的id , 可通过id查找option的名称
        # 获取当前商品的所有SKU
        skus = sku.spu.sku_set.all()  # sku 所属的全部spu里找到所有的sku(各种不同种类的商品) 比如苹果手机(SPU),土豪金,深空灰,银色(3种) * 64G 256G(2种) = 6种SKU ,
        # 构建不同规格参数（选项）的sku字典
        spec_sku_map = {}
        for s in skus:
            # 获取sku的规格参数 ; 每个sku商品的规格参数
            s_specs = s.specs.order_by('spec_id')
            # 用于形成规格参数-sku字典的键
            key = []
            for spec in s_specs:
                # 把每个sku商品所对应的option对应名称的id存入key列表中
                key.append(spec.option.id)
            # 向规格参数-sku字典添加记录 key为option对应的id : value为sku商品的id
            spec_sku_map[tuple(key)] = s.id
        # 获取当前商品的规格信息
        goods_specs = sku.spu.specs.order_by('id')  # spu的spec信息;手机就是: 颜色 内存 两种
        # 若当前sku的规格信息不完整，则不再继续
        if len(sku_key) < len(goods_specs):
            return
        for index, spu_spec in enumerate(goods_specs):
            # 复制当前sku的规格键
            key = sku_key[:] # option 的 id
            # 该规格的选项
            spec_options = spu_spec.options.all()  # 从option表中找到所有的具体1.颜色(金色,深空灰,银色 ) 和 2. 第二次虚幻拿到所有的 - 内存(64,256)
            for option in spec_options:
                # 在规格参数sku字典中查找符合当前规格的sku
                key[index] = option.id
                option.sku_id = spec_sku_map.get(tuple(key)) # 根据key找到sku的id
            spu_spec.spec_options = spec_options

        context = {
            "sku"       : sku,
            "categories": categories,
            "breadcrumb": breadcrumb,
            "specs"     : goods_specs,
        }
        return render(request, "detail.html", context=context)


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
            'categories' : categories,  # 频道分类
            'breadcrumb' : breadcrumb,  # 面包屑导航
            'sort'       : sort,  # 排序字段
            'category'   : cat3,  # 第三级分类
            'page_skus'  : page_skus,  # 分页后数据
            'total_page' : total_page,  # 总页数
            'page_num'   : page_num,  # 当前页码
            "category_id": category_id,
        }

        return render(request, 'list.html', context=context)
