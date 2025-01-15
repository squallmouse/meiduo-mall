from collections import OrderedDict

from django.shortcuts import render
from django.views import View

from apps.content.models import ContentCategory
from apps.content.utils import get_categories
from apps.goods.models import GoodsChannel


# Create your views here.

class IndexView(View):
    def get(self, request):
        """
        首页展示, 包括 广告和商品
        :param request:
        :return:
        """
        #  获取商品分类
        categories = get_categories()
        # 广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        # 一对多 查询 ; 模型类名小写_set
        for content in content_categories:
            contents[content.key] = content.content_set.filter(status=True).order_by('sequence')

        context = {
            "categories"        : categories,
            "content_categories": contents
        }
        return render(request, 'index.html', context=context)
