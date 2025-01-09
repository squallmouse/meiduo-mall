# -*- coding: UTF-8 -*-
# @创建时间: 2024/12/12 15:22   -- yh 
# @文件名:      urls.py


# 存放path路径
from django.urls import path, re_path
from . import views

# 命名空间
app_name = 'users'
urlpatterns = [
    re_path('^register/$', views.Register.as_view(), name='register'),
    re_path('^usernames/(?P<username>[A-Za-z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    re_path('^mobiles/(?P<mobile>1[3-9]\\d{9})/count/$', views.MobileCountView.as_view()),
    re_path('^login/$', views.LoginView.as_view(), name="login"),
    re_path('^logout/$', views.LogoutView.as_view(), name="logout"),
    re_path('^info/$', views.UserInfoView.as_view(), name="info"),
    re_path('^emails/$', views.EmailView.as_view()),
    re_path('^address/$', views.AddressView.as_view(), name="address"),
    re_path("^addresses/create/$", views.CreateAddressView.as_view()),
    re_path("^addresses/(?P<address_id>\d+)/$", views.UpdateDestroyAddressView.as_view()),
    re_path("^addresses/(?P<address_id>\d+)/default/$", views.DefaultAddressView.as_view()),
]
