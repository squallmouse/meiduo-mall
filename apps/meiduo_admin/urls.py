# -*- coding: UTF-8 -*-
# @创建时间: 2025/3/6 14:37   -- yh 
# @文件名:      urls.py
from django.urls import re_path, path
# from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import statistical

app_name = "myadmin"

urlpatterns = [
    #     登录
    path("authorizations/", statistical.CustomTokenObtainPairView.as_view()),

    re_path("^statistical/total_count/$", statistical.UserTotalCountView.as_view()),

]
