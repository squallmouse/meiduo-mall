# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/8 08:37   -- yh 
# @文件名:      tasks.py
import logging

from django.conf import settings
from django.core.mail import send_mail

from celery_tasks.main import celery_app


@celery_app.task(name='Celery_send_verify_email', bind=True, max_retries=3, retry_backoff=3)
def celery_send_verify_email(self, to_email, verify_url):
    """
    发送邮箱验证邮件
    :param self:
    :param to_email: 收件人邮箱
    :param verify_url: 验证链接
    :return: None
    """
    html_message = '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s</a></p>' % (to_email, verify_url, verify_url)
    try:
        send_mail(subject="美多商城验证邮件",
                  message="一小时有效期",
                  from_email=settings.EMAIL_FROM,
                  recipient_list=[to_email],
                  html_message=html_message)
    except Exception as e:
        # 有异常自动重试三次
        self.retry(exc=e, max_retries=3)
        print("邮件发送失败")
        print(f"邮件发送失败==> %s" % e)
        logging.getLogger("django").error(f"邮件发送失败==> %s" % e)
