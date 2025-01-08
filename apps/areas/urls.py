# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/8 14:02   -- yh 
# @文件名:      urls.py

from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path("^areas/$",views.AreasView.as_view()),
]
