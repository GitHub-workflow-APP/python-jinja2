from django.urls import path, include, re_path

from . import views
from django.views.generic.base import TemplateView, RedirectView

#from simple_class_based_view.views import TaintedData

app_name = 'simple_class_based_view'

view_class_pattern = [# django.views.generic.base.View

	path('',views.TaintedData.as_view(),name='tainted_data'),
	re_path(r'^index/$', views.IndexView.as_view(), name='index'),
	path('http_404/',views.TaintedDataHttp404.as_view()),
	path('path_converter/<str:tag_slug>/',views.TaintedDataPathConverter.as_view(),name='tainted_data_path_converter'),
	# tainted_arg, tainted_arg_1 are tainted, but tag_id is not tainted
	path('fp_path_converter/<str:tainted_arg>/<tainted_arg_1>/<int:tag_id>/',views.FPTaintedDataPathConverter.as_view(),name='tainted_data_path_converter'),
]

template_class_pattern = [# django.views.geenric.base.TemplateView

	path('render_response/<tainted_args>/', views.RenderResponseTemplate.as_view() ),
	path('about/', TemplateView.as_view(template_name="about.html")),
	path('<tainted_arg>/', views.TaintSourceArg.as_view(),{'tainted_data':{'%(tainted_arg)s'}}), ## One more way to pass tainted data to views.
	path('extra_context/<tainted_args>/', views.TemplateView.as_view(
		template_name="extra_context.html",
	))

]

redirect_class_pattern = [# django.views.generic.base.RedirectView
	path('tainted_redirect_url/<tainted_args>/',views.TaintedArgRedirectView.as_view()),
	# Attack.Payload curl --include 'http://localhost:8000/class_based_view/redirect_class_tainted_data/taint_source_args/cnn.com/'
	path('taint_source_args/<tainted_args>/', RedirectView.as_view(
		url='http://%(tainted_args)s') # CWEID 601
		 ),
	path('tainted_url_param/<tainted_args>/', views.TaintedUrlParam.as_view()),
]

urlpatterns = [

	path('view_class_tainted_data/', include(view_class_pattern)),
	path('template_class_tainted_data/', include(template_class_pattern)),
	path('redirect_class_tainted_data/', include(redirect_class_pattern)),
]


