from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import DocumentForm
import logging

class UploadFileView(FormView):

    logger = logging.getLogger(__name__)

    success_url = reverse_lazy('file-render')
    template_name = 'file_upload/document.html'

    def get(self, request):
        self.logger.debug("UploadFileView: get %s " , str(request.FILES['document'].read().decode('utf-8'))) # CWEID 117
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        self.logger.debug("UploadFileView: post %s " , str(request.FILES['document'].read().decode('utf-8'))) # CWEID 117
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

        return render(request, self.template_name, {'form': form})




