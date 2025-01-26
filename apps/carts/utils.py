# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/23 10:50   -- yh 
# @文件名:      utils.py

import pickle
import base64

from django_redis import get_redis_connection


def cart_py2b64str(dict):
    """
    将字典转为base64字符串
    :param dict: python 字典
    :return: base64字符串
    """
    ret = pickle.dumps(dict)
    b = base64.b64encode(ret)
    # 二进制转字符串 解码
    res = b.decode()
    return res

def cart_64str2py(b64str):
    """
    将base64字符串转为字典
    :param b64str: base64字符串
    :return: 字典
    """
    # base64转二进制 编码
    b = b64str.encode()
    ret = base64.b64decode(b)
    res = pickle.loads(ret)
    return res

def merge_cart_cookie_to_redis(request, user, response):
    """
    登录后合并cookie购物车数据到Redis
    :param request: 本次请求对象，获取cookie中的数据
    :param response: 本次响应对象，清除cookie中的数据
    :param user: 登录用户信息，获取user_id
    :return: response
    """
    # 获取cookie中的购物车数据
    cookie_cart_str = request.COOKIES.get('carts')
    # cookie中没有数据就响应结果
    if not cookie_cart_str:
        return response
    cookie_cart_dict = cart_64str2py(cookie_cart_str)

    new_cart_dict = {}
    new_cart_selected_add = []
    new_cart_selected_remove = []
    # 同步cookie中购物车数据
    for sku_id, cookie_dict in cookie_cart_dict.items():
        new_cart_dict[sku_id] = cookie_dict['count']

        if cookie_dict['selected']:
            new_cart_selected_add.append(sku_id)
        else:
            new_cart_selected_remove.append(sku_id)

    # 将new_cart_dict写入到Redis数据库
    redis_conn = get_redis_connection('carts')
    pl = redis_conn.pipeline()
    pl.hmset('carts_%s' % user.id, new_cart_dict)
    # 将勾选状态同步到Redis数据库
    if new_cart_selected_add:
        pl.sadd('selected_%s' % user.id, *new_cart_selected_add)
    if new_cart_selected_remove:
        pl.srem('selected_%s' % user.id, *new_cart_selected_remove)
    pl.execute()

    # 清除cookie
    response.delete_cookie('carts')

    return response


if __name__ == '__main__':
    dict = {
        '1': {'count'   : 10,
              'selected': True
              },
        '2': {'count'   : 20,
              'selected': False
              }
    }

    res = cart_py2b64str(dict)
    print(res)
    r = cart_64str2py(res)
    print(r)

    te = "gASVIAAAAAAAAAB9lEsDfZQojAVjb3VudJRLAYwIc2VsZWN0ZWSUiHVzLg=="
    r = cart_64str2py(te)

    print("finish")