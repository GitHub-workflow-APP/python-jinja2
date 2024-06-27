from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^rolls/', include('rolls.urls', namespace='rolls')),
    url(r'^formtests/', include('formtests.urls', namespace='formtests')),
    url(r'^admin/', include(admin.site.urls)),
]
