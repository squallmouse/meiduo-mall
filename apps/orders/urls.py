# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/26 09:02   -- yh 
# @文件名:      urls.py

from django.urls import path, re_path
from . import views

app_name = "orders"

urlpatterns = [
    re_path("^orders/settlement/$", views.OrderSettlementView.as_view(), name="settlement"),
    re_path("^orders/commit/$",views.OrderCommitView.as_view()),
    re_path("^orders/success/$",views.OrderSuccessView.as_view(),name="success"),
    re_path("^orders/info/(?P<page_num>\\d+)/$",views.UserOrderInfoView.as_view(),name="info"),
]
