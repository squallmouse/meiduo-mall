# -*- coding: UTF-8 -*-
# @创建时间: 2024/12/11 23:08   -- yh 
# @文件名:      jinja2_env.py

from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


def jinja2_environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url, # 静态文件路径
        'url': reverse, # 模板中反向解析url
    })
    return env


"""
确保可以使用模板引擎中的{{ url('') }} {{ static('') }}这类语句 
"""
