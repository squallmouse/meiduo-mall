# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/8 10:00   -- yh 
# @文件名:      contants.py
import jwt
import datetime
import urllib.parse

from django.conf import settings

# 密钥，用于签名JWT
SECRET_KEY = settings.SECRET_KEY


def _generate_verification_token(user_id, email):
    # 设置token的有效期，例如1小时
    payload = {
        'user_id': user_id,
        "email"  : email,
        'exp'    : datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    }
    # 生成JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def _generate_verification_link(token, base_url):
    """

    :param token:
    :param base_url: 邮件验证url
    :return:  完整的邮件验证链接
    """
    # 对token进行URL编码，确保链接中的参数是安全的
    encoded_token = urllib.parse.quote(token)
    # 拼接完整的验证链接
    verification_link = f"{base_url}?token={encoded_token}"
    return verification_link


def generate_verify_email_url(userid, email):
    """
    生成邮箱验证链接
    :param email: 用户验证的邮箱
    :param userid: 用户id
    :return: verify_url 邮箱验证链接
    """
    token = _generate_verification_token(userid, email)
    verify_url = _generate_verification_link(token, base_url=settings.EMAIL_VERIFY_URL)

    return verify_url


def verify_email_token(token):
    """
    验证token是否有效

    1 * 如果token已经过期，jwt.decode 会抛出 jwt.ExpiredSignatureError 异常，并返回 "Token has expired"。

    2 * 如果token无效（例如签名不匹配），jwt.decode 会抛出 jwt.InvalidTokenError 异常，并返回 "Invalid token"。

    3  * 如果token有效且未过期，jwt.decode 会返回 payload['user_id']。
    :param token: 待验证的token
    :return: 用户ID或错误信息

    """
    try:
        # 解码JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id'], payload['email']
    except jwt.ExpiredSignatureError:
        return "Token has expired", None
    except jwt.InvalidTokenError:
        return "Invalid token", None


if __name__ == '__main__':
    # SECRET_KEY = "123321123fdksajhdfkashdfkashf"
    # 示例使用
    user_id = 123321123
    user_email = 'user@example.com'

    token = _generate_verification_token(user_id, user_email)
    verification_link = _generate_verification_link(token, 'http://127.0.0.1:8000/emails/verification/')
    print("Verification Link:", verification_link)

    # 验证token
    decoded_user_id, decoded_email = verify_email_token(token)
    print("Decoded User ID:", decoded_user_id)
    print("Decoded Email:", decoded_email)
