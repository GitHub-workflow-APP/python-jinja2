"""simpleapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

handler404 = 'simpleapp.views.my_custom_page_not_found_view'
handler500 = 'simpleapp.views.my_custom_error_view'
handler403 = 'simpleapp.views.my_custom_permission_denied_view'
handler400 = 'simpleapp.views.my_custom_bad_request_view'

urlpatterns = [
	path('',views.IndexView.as_view(),name='index'),
	path('class_based_view/',include('simple_class_based_view.simple_cbv_urls')),
	path('file_upload/',include('file_upload.urls')),
]
