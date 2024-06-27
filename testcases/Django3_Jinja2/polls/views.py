from django.shortcuts import render
  
# Attack Payload: curl 'http://localhost:8000/polls/' -d "tainted_name=<script>alert(1)</script>"
def index(request):
    return render(request, 'polls/index.html',{'tainted_name':request.POST['tainted_name']})
