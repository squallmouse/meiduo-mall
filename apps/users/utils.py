# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/7 08:26   -- yh 
# @文件名:      utils.py
import re
from django.contrib.auth.backends import ModelBackend


from .models import User

def get_user_by_account(account):
    """
    根据account查询用户
    :param account: 用户名或者手机号
    :return: 查询到了 user ; 没查询到 None;
    """
    try:
        if re.match(r"^1[3-9]\d{9}$",account):
            # 手机号登录
            user = User.objects.get(mobile=account)
        else:
            # 用户名登录
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user

class UsernameMobileAuthBackend(ModelBackend):
    """自定义用户认证后端"""
    def authenticate(self,request,username=None,password=None,**kwargs):
        """
        继承自django的ModelBackend类,重写认证方法,实现多账号登录
        loginView 的登录方法中,
        > # 认证登录用户
        > user = authenticate(request,username=username,password=password)
        会到上面的 authenticate 方法中
        :param request: 请求对象
        :param username: 用户名或手机号
        :param password: 密码
        :param kwargs: 其它参数
        :return: user
        """
        user = get_user_by_account(username)
        if user is not None:
            if user.check_password(password):
                return user