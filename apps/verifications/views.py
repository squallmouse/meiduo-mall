from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from apps.verifications.libs.captcha.captcha import captcha


# Create your views here.

class ImageCodeView(View):
    """ 图形验证码"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpg
        """
        # 生成图片验证码

        text, image = captcha.generate_captcha()
        # 保存图片验证码
        # 连接到 verify_code 的 redis库
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, 300, text)

        return http.HttpResponse(image, content_type='image/jpg')
