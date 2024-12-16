# -*- coding: UTF-8 -*-
# @创建时间: 2024/12/16 09:54   -- yh 
# @文件名:      urls.py

from django.urls import path, re_path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
