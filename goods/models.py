from django.db import models
from tinymce.models import HTMLField
# Create your models here.


class Type(models.Model):
    """商品分类"""
    title = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Goods(models.Model):
    """商品"""
    goods_title = models.CharField(max_length=20)
    # 图片位置 服务器部署记得看看
    goods_picture = models.ImageField(upload_to='df_goods')
    goods_price = models.DecimalField(max_digits=5, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    # 单位
    goods_unit = models.CharField(max_length=20, default='500g')
    # 点击量 用于排序
    goods_click = models.IntegerField()
    # 简介
    goods_introduction = models.CharField(max_length=200)
    # 库存
    goods_inventory = models.IntegerField()
    # 详细介绍
    goods_content = HTMLField()
    # 外键
    goods_type = models.ForeignKey(Type)

    def __str__(self):
        return self.goods_title
