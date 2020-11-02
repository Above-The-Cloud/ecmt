
from django.conf.urls import url
from django.urls import include, re_path

from . import views

urlpatterns = [
    url(r'^$', views.hello),
    url(r'^upload/', include('upload.urls')),
    re_path(r'^course/', include('course.urls')),
    re_path(r'^user/', include('user.urls')),
    re_path(r'^teacher/', include('teacher.urls')),
    re_path(r'^comment/', include('comment.urls')),
    re_path(r'^feedback/', include('feedback.urls')),
]
