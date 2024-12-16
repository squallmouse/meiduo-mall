import re

from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, HttpResponse
from django.views import View
from apps.users.models import User


# Create your views here.


class Register(View):
    """用户注册"""

    def get(self, request):
        """返回渲染后的注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        """实现用户注册"""
        dict = request.POST
        userName = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        allow = dict.get('allow')

        # 判断参数是否齐全
        if not all([userName, password, password2, mobile, allow]):
            return HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9-_]{5,20}$', userName):
            return HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个
        if not re.match(r'^[a-zA-Z0-A_-]{8,20}', password):
            return HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return HttpResponseForbidden('两次密码输入不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseForbidden('请输入正确的手机号')
        # 判断是否勾选用户协议
        if allow == False:
            return HttpResponseForbidden('请勾选用户协议')

        return JsonResponse({'code': 0})

        # User.objects.create_user(username=userName, password=password, mobile=mobile)
