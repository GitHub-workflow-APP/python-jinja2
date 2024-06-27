from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[^\/]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[^\/]+)/getacc/$', views.getaccess, name='getaccess'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<question_id>[^\/]+)/pd$', views.poll_detail, name='poll_detail'),
]
