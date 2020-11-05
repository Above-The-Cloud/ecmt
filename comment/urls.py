from django.urls import path, re_path, include

from comment import views

urlpatterns = [
    re_path(r'^more_comment$', views.more_comment),
    re_path(r'^submit_comment', views.submit_comment),
    re_path(r'^favor_comment', views.favor_comment),
    re_path(r'^hot_comment', views.hot_comment),
    re_path(r'^my_comment', views.my_comment),
    re_path(r'^my_approval', views.my_approval),
    re_path(r'^my_news', views.my_news),
	re_path(r'^search_read$', views.search_read)
]