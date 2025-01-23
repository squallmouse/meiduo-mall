# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/23 11:38   -- yh 
# @文件名:      urls.py

from django.urls import re_path


from . import views

app_name = "carts"

urlpatterns = [
    re_path("^carts/$", views.CartView.as_view(),name="cart"),
]
