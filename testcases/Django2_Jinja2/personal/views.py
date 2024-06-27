from django.shortcuts import render

# Attack Payload: curl 'http://localhost:8000/' -d "tainted_name=<script>alert(1)</script>"
def index(request):
    return render(request, 'personal/home.html',{'tainted_name':request.POST['tainted_name']})
