from django.urls import path, re_path, include

from course import views

urlpatterns = [
    re_path(r'^listCourse$', views.listCourse),
    re_path(r'^course_teaching', views.course_teaching),
    re_path(r'^addCourse', views.addCourse),
    re_path(r'^addTeaching', views.addTeaching),
]