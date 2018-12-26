from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^info/$', views.info, name='info'),
    url(r'^register_exist/$', views.register_exist, name='register_exist'),
    url(r'^site/$', views.site, name='site'),
    url(r'^user_center_order&(\d+)/$', views.user_center_order),
    url(r'^logout/$', views.logout, name='logout'),
]
