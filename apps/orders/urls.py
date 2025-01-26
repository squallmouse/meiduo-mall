# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/26 09:02   -- yh 
# @文件名:      urls.py

from django.urls import path, re_path
from . import views

app_name = "orders"

urlpatterns = [
    re_path("^orders/settlement/$", views.OrderSettlementView.as_view(), name="settlement"),
]
