from django.db import models
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    email = models.EmailField(max_length=100)
    addressee = models.CharField(max_length=60, default='')
    address = models.TextField(default='')
    post_code = models.CharField(max_length=40, default='')
    phone = models.CharField(max_length=20, default='')
    time = models.DateTimeField(auto_now_add=True)
    # default, blank是python层面的约束,不影响数据库表结构, 不需要迁移
