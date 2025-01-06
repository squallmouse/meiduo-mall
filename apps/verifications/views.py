from logging import Logger

from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
import random, logging

from apps.verifications.libs.captcha.captcha import captcha
from meiduo.utils.response_code import RETCODE
from apps.verifications.libs.yuntongxun.ccp_sms import CCP, expiration_time
from celery_tasks.sms.tasks import celery_send_sms_code


# Create your views here.

class ImageCodeView(View):
    """ 图形验证码"""

    @staticmethod
    def get(request, uuid):
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
        # img_uuid 为key : text 为图片的验证码 为value
        redis_conn.setex('img_%s' % uuid, 300, text)

        return http.HttpResponse(image, content_type='image/jpg')


class SMSCodeView(View):
    """短信验证码"""

    @staticmethod
    def get(request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        # 接收get请求中的参数
        response = request.GET
        image_code_client = response.get("image_code").lower()
        uuid = response.get("uuid")
        # 验证图片验证码和redis中的是否一致
        # 拼接key
        key = "img_%s" % uuid
        # 创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')
        image_code_server = redis_conn.get(key).decode().lower()
        # 验证图片验证码是否一致
        if image_code_server is None:
            return http.JsonResponse({"code": RETCODE.IMAGECODEERR, "errmsg": "图片验证码过期"})

        # 对比收到的验证码和redis中的验证码是否一致
        if image_code_server != image_code_client:
            return http.JsonResponse({"code": RETCODE.IMAGECODEERR, "errmsg": "图片验证码错误"})

        # 删除图形验证码，避免恶意测试图形验证码
        try:
            redis_conn.delete(key)
        except Exception as e:
            logging.getLogger("django").error(e)


        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:
            return http.JsonResponse({"code": RETCODE.THROTTLINGERR, "errmsg": "发送短信过于频繁"})

        # 图片验证码正确
        # 生成短信验证码：生成6位数验证码
        sms_code = '%04d' % random.randint(0, 9999)

        # code = CCP().send_message("1", mobile, sms_code)
        celery_send_sms_code.delay('1', mobile,sms_code)

        # if code != 0:
        #     return http.JsonResponse({"code": RETCODE.OK, "errmsg": "发送短信失败"})
        # 短信发送成功
        # 自己生成的验证码,自己存起来
        pl = redis_conn.pipeline()
        pl.setex("send_flag_%s" % mobile, 60, 1)
        pl.setex('sms_%s' % mobile, expiration_time, sms_code)
        pl.execute()
        return http.JsonResponse({"code": RETCODE.OK, "errmsg": "发送短信成功"})
