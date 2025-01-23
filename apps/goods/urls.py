# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/15 12:17   -- yh 
# @文件名:      urls.py
from django.urls import re_path
from . import views

app_name = "goods"

urlpatterns = [
    re_path("^list/(?P<category_id>\\d+)/(?P<page_num>\\d+)/$", views.ListView.as_view(),
            name="list"),
    re_path("^hot/(?P<category_id>\\d+)/$",views.HotGoodsView.as_view()),
    re_path("^detail/(?P<sku_id>\\d+)/$",views.DetailView.as_view(),name="detail"),
    re_path("^detail/visit/(?P<category_id>\\d+)/$",views.DetailVisitView.as_view()),
# re_path("^detail/$",views.DetailView.as_view(),name="detail"),
]
