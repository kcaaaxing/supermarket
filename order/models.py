from django.db import models

# Create your models here.


class Order(models.Model):
    """订单"""
    order_id = models.CharField(max_length=20, primary_key=True)
    order_user = models.ForeignKey('user.User')
    order_date = models.DateTimeField(auto_now=True)
    order_IsPay = models.IntegerField(default=0)
    order_total = models.DecimalField(max_digits=6, decimal_places=2)
    order_address = models.CharField(max_length=150, default='')
    order_Pay = models.IntegerField(default=0)


class OrderDetail(models.Model):
    order_goods = models.ForeignKey('goods.Goods')
    order = models.ForeignKey(Order)
    order_price = models.DecimalField(max_digits=5, decimal_places=2)
    order_count = models.IntegerField()
