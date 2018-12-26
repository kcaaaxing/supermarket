from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(\d+)/$', views.detail, name='detail'),
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.goods_list, name='goodsList'),
]
