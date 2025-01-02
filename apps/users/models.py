from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    """自定义用户模型类 , 扩展额外的字段(mobile)"""
    # 因为继承自 AbstractUser 类,所以本身含有两个必填字段: username, password
    # 新定义了一个字段, 手机号
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")

    class Meta:
        """
        类似例子
        verbose_name = "书"
        verbose_name_plural = "书籍"
        """
        db_table = "tb_users"  # 自定义表名
        verbose_name = "用户"  # 站点显示的用户
        verbose_name_plural = verbose_name  # 模型的复数可读名称 它覆盖了 Django 默认为模型生成的复数形式。

    def __str__(self):
        return self.username
