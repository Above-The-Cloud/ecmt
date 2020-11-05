from django.urls import path, re_path, include

from feedback import views

urlpatterns = [
    re_path(r'^submitErr$', views.submitErr),
]