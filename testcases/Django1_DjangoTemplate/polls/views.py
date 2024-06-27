from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.db.models.expressions import RawSQL
from django.db import connection

import polls
from models import Question, Choice

from django.http import HttpResponse, Http404

def index(request):
    if 'foo' in request.GET:
        return HttpResponse("abcdefg<b>hijklmnop</b>qrstuvwxyz" + request.GET['foo'])   # CWEID 80
    if 'bar' in request.GET:
        bar = request.GET['bar']
    if 'baz' in request.GET:
        raise Http404('unknown: ' + request.GET['baz'])
    else:
        bar = "safe"
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'var1': "hello",
        'var2': bar,
    })
    return HttpResponse(template.render(context))


def detail(request, question_id):
    r = HttpResponse("hey detail: " + question_id)      # CWEID 80
    r.write("whasdoif")
    r.write("whasdoif" + question_id)   # CWEID 80
    r['foo'] = 'bar' + question_id  # CWEID 113
    r['fox' + question_id] = 'bar' # CWEID 113
    return r

def results(request, question_id):
    return HttpResponse("yo results")

def getaccess(request, question_id):
    if 'sql' in request.GET:
        rv = RawSQL(request.GET['sql'], ())         # CWEID 89
        print "rv: " + str(rv)
        cursor = connection.cursor()
        cursor.execute(request.GET['sql'])          # CWEID 89
        rv2 = str(cursor.fetchone())
        print "rv2: " + str(rv2)
        cursor2 = connection.cursor()
        cursor2.execute(request.GET['sql'])         # CWEID 89
        rv3 = str(cursor2.fetchmany())
        print "rv3: " + str(rv3)
    else:
        rv = ""
        rv2 = ""
        rv3 = ""
    context = { 'getvars': request.GET, 'rv': rv, 'rv2': rv2, 'rv3': rv3 }
    return render(request, 'getacc.html', context)

def vote(request, question_id):
    return HttpResponse("yo vote: " + str(request.POST['choice']))   # CWEID 80

def poll_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll_detail.html', { 'question': question})
    
