from django.urls import path, include, re_path

from . import views
from django.views.generic import ListView
from .models import Document
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload/', views.UploadFileView.as_view(), name='upload'),
    path('', ListView.as_view(
        template_name='file_upload/document_detail.html',
        model = Document,
        context_object_name='documents'
    ), name='file-render'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)