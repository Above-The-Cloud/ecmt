from django.urls import path, re_path, include

from user import views

urlpatterns = [
    re_path(r'^create$', views.create),
    re_path(r'^get$', views.get),
    re_path(r'^update$', views.update),
    re_path(r'^login$', views.login),
    re_path(r'^auth$', views.auth),
    re_path(r'^getOpenid$', views.getOpenid),
]