from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.contrib import messages
import logging

class IndexView(View):
	def get(self,request):
		return HttpResponse('Index')

logger = logging.getLogger(__name__)

def my_custom_error_view(request):
	messages.add_message(request, messages.DEBUG, 'Something Not Wrong')
	logger.debug("my_custom_error_view " + request.COOKIES.get('tainted_cookie')) # CWEID 117
	return render(request, '500.html', status=500)

# Attack.Payload curl 'http://localhost:8000/abc/' --cookie "tainted_cookie=<script>alert(1)</script>"
def my_custom_page_not_found_view(request):
	logger.debug("my_custom_page_not_found_view " + request.COOKIES.get('tainted_cookie')) # CWEID 117
	return render(request, '404.html', status=404)

def my_custom_permission_denied_view(request):
	logger.debug("my_custom_permission_denied_view " + request.COOKIES.get('tainted_cookie')) # CWEID 117
	return render(request,'403.html', status=403)

def my_custom_bad_request_view(request):
	logger.debug("my_custom_bad_request_view " + request.COOKIES.get('tainted_cookie')) # CWEID 117
	return render(request,'400.html',status=400)
