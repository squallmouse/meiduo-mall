# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/6 08:35   -- yh 
# @文件名:      main.py

# celery 启动文件
import os
import sys

# 获取项目的根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from celery import Celery

# 创建celery实例, 生产者
celery_app = Celery('meiduo')
# 加载celery配置
celery_app.config_from_object("celery_tasks.config")
#自动注册celery任务
celery_app.autodiscover_tasks(["celery_tasks.sms", "celery_tasks.email"])