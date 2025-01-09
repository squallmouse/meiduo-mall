# -*- coding: UTF-8 -*-
import json
import logging
import re

from django import http
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db import DatabaseError
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django_redis import get_redis_connection

from apps.users.contants import generate_verify_email_url
from apps.users.models import User, Address
from celery_tasks.email.tasks import celery_send_verify_email
from meiduo.utils.response_code import RETCODE
from meiduo.utils.views import LoginRequiredJSONMixin


# Create your views here.

class EmailView(View):
    """添加邮箱"""

    @staticmethod
    def put(request):
        """实现添加邮箱逻辑"""

        user = request.user
        if not request.user.is_authenticated:
            return http.JsonResponse({"code": RETCODE.SESSIONERR, "errmsg": "用户未登录"})

        json_dict = json.loads(request.body.decode())
        email = json_dict.get("email")

        if not email:
            return HttpResponseForbidden("缺少必传参数")
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return HttpResponseForbidden("邮箱格式错误")

        try:
            user.email = email
            user.save()
        except DatabaseError:
            logging.getLogger("django").error("邮件验证失败~~~")
            return http.JsonResponse({"code": RETCODE.DBERR, "errmsg": "添加邮箱失败"})

        verify_url = generate_verify_email_url(user.id, email)
        celery_send_verify_email(to_email=email, verify_url=verify_url)
        # try:
        #     send_mail(subject="美多商城验证邮件",
        #               message="一小时有效期",
        #               from_email=settings.EMAIL_FROM,
        #               recipient_list=[email],
        #               html_message="<p>verify_url</p>"
        #               )
        # except Exception as e:
        #     print("邮件发送失败")
        #     print(f"==> %s" % e)
        #     logging.getLogger("django").error(e)

        return http.JsonResponse({"code": RETCODE.OK, "errmsg": "添加邮件成功"})


class Register(View):
    """用户注册"""

    @staticmethod
    def get(request):
        """返回渲染后的注册页面"""
        return render(request, 'register.html')

    @staticmethod
    def post(request):
        """实现用户注册"""
        dict = request.POST
        userName = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        allow = dict.get('allow')
        msg_code_client = dict.get('sms_code')

        # 判断参数是否齐全
        if not all([userName, password, password2, mobile, allow, msg_code_client]):
            return HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9-_]{5,20}$', userName):
            return HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个
        if not re.match(r'^[a-zA-Z0-9_-]{8,20}$', password):
            return HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return HttpResponseForbidden('两次密码输入不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseForbidden('请输入正确的手机号')
        # 判断是否勾选用户协议
        if allow != 'on':
            return HttpResponseForbidden('请勾选用户协议')
        # 判断短信验证码
        redis_conn = get_redis_connection("verify_code")
        sms_code_server = redis_conn.get('sms_%s' % mobile).decode()
        if msg_code_client != sms_code_server:
            return render(request, 'register.html', {'register_errmsg': '短信验证码错误'})
        try:
            redis_conn.delete('sms_%s' % mobile)
        except Exception as e:
            logging.getLogger("django").error(e)

        # 保存注册数据
        try:
            user = User.objects.create_user(username=userName, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        print('注册成功 --> 跳转首页')

        # 实现状态保持
        #   将通过认证的用户的唯一标识信息（比如：用户ID）写入到当前浏览器的 cookie 和服务端的 session 中。
        login(request, user)

        return redirect(reverse('contents:index'))


class UsernameCountView(View):
    """判断用户名是否重复 """

    @staticmethod
    def get(request, username):
        """查找用户名的数量"""
        count = User.objects.filter(username=username).count()

        print(f"用户名的个数 --> {count}")

        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'count': count})


class MobileCountView(View):
    """手机号是否重复"""

    @staticmethod
    def get(request, mobile):
        """查找手机号的数量"""
        count = User.objects.filter(mobile=mobile).count()

        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'count': count})


class LoginView(View):
    """用户登录"""

    @staticmethod
    def get(request):
        """返回登录页面"""
        return render(request, "login.html")

    @staticmethod
    def post(request):
        """实现用户登录"""
        dict = request.POST
        username = dict.get("username")
        password = dict.get("password")
        remember = dict.get("remembered")

        #  检验参数是否齐全
        if not all([username, password]):
            return HttpResponseForbidden("缺少必传参数")
        # 检验用户名是否合格 5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden("用户名错误")

        # 检验密码是否合格 8-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{8,20}$', password):
            return HttpResponseForbidden("密码错误")

        # 认证登录用户
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "login.html", {"errmsg": "用户名或密码错误"})
        # 登录成功
        login(request, user)
        if remember != "on":
            # 不记住,浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            # 默认就是两周过后
            request.session.set_expiry(None)

        next = request.GET.get('next')
        if next:
            response = redirect(next)
        else:
            indexHtmlPage = reverse('contents:index')
            response = redirect(indexHtmlPage)

        response.set_cookie('username', user.username, max_age=14 * 24 * 3600)
        return response


class LogoutView(View):
    """用户退出登录"""

    @staticmethod
    def get(request):
        """实现用户退出登录"""
        # 清理session
        logout(request)
        # 退出后反向定位到首页
        response = redirect(reverse('contents:index'))
        # 清除cookie中的username
        response.delete_cookie('username')
        return response


class UserInfoView(LoginRequiredMixin, View):
    """用户中心-信息页"""

    @staticmethod
    def get(request):
        """提供个人信息界面"""
        context = {
            "username"    : request.user.username,
            "mobile"      : request.user.mobile,
            "email"       : request.user.email,
            "email_active": request.user.email_active
        }
        response = render(request, 'user_center_info.html', context=context)
        return response


class AddressView(View):
    """用户中心地址"""

    @staticmethod
    def get(request):
        """提供地址界面"""
        user = request.user
        address_list = []
        temp = user.address.all()
        for address in temp:
            item = {
                "id"      : address.id,
                "title"   : address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city"    : address.city.name,
                "distract": address.distract.name,
                "place"   : address.place,
                "mobile"  : address.mobile,
                "tel"     : address.tel,
                "email"   : address.email,
            }
            address_list.append(item)
        context = {
            "default_address_id": user.default_address_id,
            "addresses"         : address_list
        }
        response = render(request, "user_center_site.html", context=context)
        return response


class CreateAddressView(LoginRequiredJSONMixin, View):
    """用户中心 创建地址"""

    @staticmethod
    def post(request):
        """保存用户新地址"""
        body_para = json.loads(request.body.decode())
        receiver = body_para.get("receiver")
        province_id = body_para.get("province_id")
        city_id = body_para.get("city_id")
        district_id = body_para.get("district_id")
        place = body_para.get("place")
        mobile = body_para.get("mobile")
        tel = body_para.get("tel")
        email = body_para.get("email")

        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden("缺少必传参数")

        if not re.match(r"^1[3-9]\d{9}$", mobile):
            return http.HttpResponseForbidden("参数mobile有误")

        if tel:
            if not re.match(r"^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$", tel):
                return http.HttpResponseForbidden("参数tel有误")

        if email:
            if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
                return http.HttpResponseForbidden("参数email有误")

        #       保存地址
        try:
            address = Address.objects.create(
                user=request.user,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                distract_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
            #     设置默认收货地址
            if request.user.default_address is None:
                request.user.default_address = address
                request.user.save()

        except DatabaseError as e:
            logging.getLogger('django').error(f"保存地址失败 => {e}")
            return http.HttpResponseServerError("保存地址失败")
        address_dict = {
            "id"      : address.id,
            "title"   : address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city"    : address.city.name,
            "distract": address.distract.name,
            "place"   : address.place,
            "mobile"  : address.mobile,
            "tel"     : address.tel,
            "email"   : address.email,
        }
        # 返回响应结果
        return http.JsonResponse({"code": RETCODE.OK, "errmsg": "新增地址成功", "address": address_dict})

class UpdateDestroyAddressView(LoginRequiredJSONMixin,View):
    """修改和删除收货地址"""
    @staticmethod
    def put(request,address_id):
        """修改地址"""

        pass
