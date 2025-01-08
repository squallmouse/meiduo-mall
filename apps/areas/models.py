from django.db import models

# Create your models here.


class Area(models.Model):
    """地区 省 市 区"""
    name = models.CharField(max_length=20, verbose_name='名称')
    """
    ForeignKey("self")：     外键指向自身，表示该字段可以引用同一个模型中的其他实例。
    on_delete=models.SET_NULL：  当父级区域被删除时，将此字段设置为 NULL。
    related_name="subs"：    反向查询时使用 subs 作为相关名称，例如可以通过某个区域对象获取其所有子区域。
    null=True, blank=True：  允许该字段为空。
    verbose_name='上级区域'：    在管理界面中显示为“上级区域”
    """
    parent = models.ForeignKey("self",on_delete=models.SET_NULL,related_name="subs",null=True,blank=True,verbose_name='上级区域')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name