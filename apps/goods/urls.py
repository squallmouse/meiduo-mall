# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/15 12:17   -- yh 
# @文件名:      urls.py
from django.urls import re_path
from . import views

app_name = "goods"

urlpatterns = [
    re_path("^list/(?P<category_id>\\d+)/(?P<page_num>\\d+)/$", views.ListView.as_view(),
            name="list"),
]
