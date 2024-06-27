from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.safestring import mark_safe

from .forms import NameForm

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponse('/thanks/' + form.data['your_name'])     # CWEID 80
    else:
        form = NameForm(request.GET)
    if 'hi' in request.GET:
        bah = mark_safe(request.GET['hi'])
    else:
        bah = "bah"

    return render(request, 'name.html', {'form': form, 'bah': bah})

def docycle(request):
    return render(request, 'docycle.html', { 'foo': 'foo', 'bar': request.GET['foo'], 'baz': request.GET.values(), 'quux': mark_safe('<b>hi</b>')})
