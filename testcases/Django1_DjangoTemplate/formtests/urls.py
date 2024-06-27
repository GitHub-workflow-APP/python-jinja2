from django.conf.urls import url, patterns

urlpatterns = patterns('formtests.views',
    url(r'^name/$', view='get_name'),
    url(r'^cycle/$', view='docycle'),
)

