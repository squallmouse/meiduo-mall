# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/6 08:46   -- yh 
# @文件名:      tasks.py
import logging

from celery_tasks.main import celery_app
from apps.verifications.libs.yuntongxun.ccp_sms import CCP



# bind：保证task对象会作为第一个参数自动传入
# name：异步任务别名
# retry_backoff：异常自动重试的时间间隔 第n次(retry_backoff×2^(n-1))s
# max_retries：异常自动重试次数的上限
@celery_app.task(name='celery_send_sms_code', bind=True, max_retries=3, retry_backoff=3)
def celery_send_sms_code(self,template_tag,mobile,sms_code):
    """
    发送短信异步任务
    :param self:
    :param mobile: 手机号
    :param sms_code: 短信验证码
    :return: 成功0 | 失败-1
    """
    try:
        send_result_code = CCP().send_message(template_tag, mobile, sms_code)
    except Exception as e:
        logging.getLogger('django').error(e)
#     有异常自动重试三次
        raise self.retry(exc=e, max_retries=3)

    if send_result_code != 0:
        #     有异常自动重试三次
        raise self.retry(exc=Exception('发送短信验证码失败'), max_retries=3)

    return send_result_code