import logging

from django import http
from django.shortcuts import render
from django.views import View
from redis import DataError

from apps.content.utils import get_categories
from apps.goods.models import GoodsCategory
from apps.goods.utils import get_breadcrumb


# Create your views here.

class ListView(View):
    """商品列表页"""

    @staticmethod
    def get(request, category_id, page_num):
        print(category_id, page_num)
        try:
            cat3 = GoodsCategory.objects.get(id=category_id)
        except DataError:
            return http.HttpResponseForbidden('商品类别不存在')
        except Exception as e:
            logging.getLogger('django').error(e)

        categories = get_categories()
        breadcrumb = get_breadcrumb(cat3)

        context= {
            'categories': categories,
            'breadcrumb': breadcrumb
        }

        return render(request, 'list.html',context=context)
