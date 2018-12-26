# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-09-07 15:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_title', models.CharField(max_length=20)),
                ('goods_picture', models.ImageField(upload_to='images')),
                ('goods_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('isDelete', models.BooleanField(default=False)),
                ('goods_unit', models.CharField(default='500g', max_length=20)),
                ('goods_click', models.IntegerField()),
                ('goods_introduction', models.CharField(max_length=200)),
                ('goods_inventory', models.IntegerField()),
                ('goods_content', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='goods_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Type'),
        ),
    ]
