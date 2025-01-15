# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/15 12:34   -- yh 
# @文件名:      utils.py

from apps.goods.models import GoodsCategory

def get_breadcrumb(category:GoodsCategory):
    """
    获取面包屑导航
    :param category: 商品类别
    :return:
    """
    breadcrumb = {
        'cat1': '',
        'cat2': '',
        'cat3': ''
    }
    if category.parent is None:
#         一级
        breadcrumb['cat1']=category
    elif category.parent.parent is None:
#         二级
        breadcrumb['cat2'] = category
        breadcrumb['cat1'] = category.parent
    else:
#         三级
        breadcrumb['cat3'] = category
        breadcrumb['cat2'] = category.parent
        breadcrumb['cat1'] = category.parent.parent
    return breadcrumb
