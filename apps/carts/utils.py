# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/23 10:50   -- yh 
# @文件名:      utils.py

import pickle
import base64


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