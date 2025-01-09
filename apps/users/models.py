from django.db import models
from django.contrib.auth.models import AbstractUser

from meiduo.utils.models import BaseModel


# Create your models here.

class User(AbstractUser):
    """自定义用户模型类 , 扩展额外的字段(mobile)"""
    # 因为继承自 AbstractUser 类,所以本身含有两个必填字段: username, password
    # 新定义了一个字段, 手机号
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    email_active = models.BooleanField(default=False, verbose_name="邮箱验证状态")
    default_address = models.ForeignKey("Address",related_name="users",null=True,blank=True,on_delete=models.SET_NULL,verbose_name="默认地址")

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


class Address(BaseModel):
    """用户地址"""
    # on_delete=models.CASCADE：当关联的 User 对象被删除时，关联的这个对象也会被删除。
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='address',verbose_name="用户" )
    title = models.CharField(max_length=20,verbose_name="地址名称")
    receiver = models.CharField(max_length=20,verbose_name="收货人")
    # on_delete=models.PROTECT
    # 阻止删除：如果尝试删除被外键引用的对象（即 Area 对象），Django 会抛出一个 ProtectedError 异常，从而阻止删除操作。
    # 这意味着在删除 Area 对象之前，必须先删除或更新所有引用该 Area 对象的 Address 记录，否则删除操作将被阻止。
    province = models.ForeignKey("areas.Area",on_delete=models.PROTECT,related_name="province_address",verbose_name="省")
    city = models.ForeignKey('areas.Area',on_delete=models.PROTECT,related_name="city_address",verbose_name="市")
    distract = models.ForeignKey('areas.Area',on_delete=models.PROTECT,related_name="district_address",verbose_name="区")
    place = models.CharField(max_length=50,verbose_name="地址")
    mobile = models.CharField(max_length=11,verbose_name="手机号")
    # null=True：
    # 数据库层面：允许该字段在数据库中存储 NULL 值。
    # 用途：适用于那些在数据库中可以为空的字段。例如，一个用户可能没有固定电话，因此 tel 字段可以设置为 null=True。
    # blank=True：
    # 表单验证层面：允许该字段在表单中为空。
    # 用途：适用于那些在用户输入时可以留空的字段。例如，在一个用户注册表单中，固定电话字段可以留空，因此 tel 字段可以设置为 blank=True。
    tel = models.CharField(max_length=20,null=True,blank=True,default="",verbose_name="固定电话")
    email = models.CharField(max_length=30,null=True,blank=True,default="",verbose_name="邮箱")
    is_delete = models.BooleanField(default=False,verbose_name="逻辑删除")

    class Meta:
        db_table = "tb_address"
        verbose_name = "用户地址"
        verbose_name_plural = verbose_name
        # ordering 排序 根据update_time  '-'倒序排列
        ordering = ["-update_time"]

