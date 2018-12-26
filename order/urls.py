from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.order, name='order'),
    url(r'^addorder/$', views.order_handle, name='order_handle'),
    url(r'^pay&(\d+)/$', views.pay, name='pay'),
]
