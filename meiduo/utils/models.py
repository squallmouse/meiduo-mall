# -*- coding: UTF-8 -*-
# @创建时间: 2025/1/9 10:30   -- yh 
# @文件名:      models.py

from django.db import models

class BaseModel(models.Model):
    """为模型类补充字段"""
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True,verbose_name="更新时间")

    class Meta:
        # 说明是抽象模型类, 用于继承使用, 数据库迁移时不会创建 BaseModel 的表
        abstract = True
