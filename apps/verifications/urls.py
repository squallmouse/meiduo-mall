# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/3 10:01   -- yh 
# @文件名:      urls.py

from django.urls import path, re_path
from . import views

app_name = 'verifications'
urlpatterns = [
    re_path('^image_codes/(?P<uuid>[\\w-]+)/$',views.ImageCodeView.as_view()),
]
