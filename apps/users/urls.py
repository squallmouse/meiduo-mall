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
    re_path('^usernames/(?P<username>[A-Za-z0-9_-]{5,20})/count/$',views.UsernameCountView.as_view()),
    re_path('^mobiles/(?P<mobile>1[3-9]\d{9})/count/$',views.MobileCountView.as_view()),

]
