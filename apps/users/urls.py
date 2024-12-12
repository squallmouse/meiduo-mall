# -*- coding: UTF-8 -*-
# @创建时间: 2024/12/12 15:22   -- yh 
# @文件名:      urls.py


# 存放path路径
from django.urls import path, re_path
from . import views

# 命名空间
app_name = 'users'
urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),

]
