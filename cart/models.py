from django.db import models

# Create your models here.


class Cart(models.Model):
    """购物车"""
    cart_user = models.ForeignKey('user.User')
    cart_goods = models.ForeignKey('goods.Goods')
    count = models.IntegerField(default=0)
