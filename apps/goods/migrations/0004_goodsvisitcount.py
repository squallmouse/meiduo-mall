# Generated by Django 5.1.4 on 2025-01-29 05:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_rename_default_image_url_sku_default_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsVisitCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('count', models.IntegerField(default=0, verbose_name='访问量')),
                ('date', models.DateField(auto_now_add=True, verbose_name='统计日期')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodscategory', verbose_name='商品类别')),
            ],
            options={
                'verbose_name': '统计分类商品访问量',
                'verbose_name_plural': '统计分类商品访问量',
                'db_table': 'tb_goods_visit',
            },
        ),
    ]
