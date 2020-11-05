from django.urls import path, re_path, include

from teacher import views

urlpatterns = [
    re_path(r'^listTeacher$', views.listTeacher),
    re_path(r'^listDept$', views.listDept),
    re_path(r'^listProfession$', views.listProfession),
    re_path(r'^deleteAndInsertProfession$', views.deleteAndInsertProfession)
]