# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/3 10:01   -- yh 
# @文件名:      urls.py

from django.urls import path, re_path
from . import views

app_name = 'verifications'
urlpatterns = [
    # 用于获取图片验证码
    re_path('^image_codes/(?P<uuid>[\\w-]+)/$',views.ImageCodeView.as_view()),
    # 用于发送短信
    re_path('^sms_codes/(?P<mobile>1[3-9]\\d{9})/$',views.SMSCodeView.as_view()),
# (?P<mobile>1[3-9]\d{9})/
]
