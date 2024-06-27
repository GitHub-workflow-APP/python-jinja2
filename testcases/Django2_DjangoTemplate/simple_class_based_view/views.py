from django.http import HttpResponse
from django.views import View
from django.http import Http404
from django.http import HttpResponseNotAllowed
import logging
from django.views.generic.base import TemplateView, RedirectView
from django.http.request import QueryDict



# Testcase for all Entry Points of View class. Also, tried to include most of the HttpRequest objects TAINTED SOURCED. Specially the onces not in Django 1.x research testcases
class TaintedData(View):

    logger = logging.getLogger(__name__)

    # Attach.Payload curl -X POST "http://localhost:8000/class_based_view/view_class_tainted_data/" -d "{'name':'<script>alert(1)</script>'}"
    def dispatch(self, request, *args, **kwargs):
        self.logger.info("TaintedData:dispatch " + request.body.decode('utf-8')) # CWEID 117
        return super(TaintedData,self).dispatch(request)

    # Trace is the only http method which is not implemented.
    # Exercising HttpResponseNotAllowed as a SINK
    # Attack.Payload curl -X TRACE 'http://localhost:8000/class_based_view/view_class_tainted_data/' --cookie "tainted_cookie=<scriptalert(1)</script>"
    def http_method_not_allowed(self, req, *args, **kwargs):
        self.logger.info("TaintedData:http_method_not_allowed " + req.COOKIES.get('tainted_cookie')) # CWEID 117
        return HttpResponseNotAllowed(self._allowed_methods() , req.COOKIES.get('tainted_cookie')) # CWEID 80

    # Attach.Payload:  curl -X GET "http://localhost:8000/class_based_view/view_class_tainted_data/?name=<script>alert(21)</script>"
    def get(self, request):
        self.logger.debug("Tainted:get path_info " , request.path_info) # CWEID 117
        self.logger.debug("TaintedData:get " , request.GET) # CWEID 117
        return HttpResponse("TaintedData:get ", request.GET)  # CWEID 80

    # Tainted SOURCE request object, could be named anything and not just 'request'
    # Attack.Payload curl -X POST "http://localhost:8000/class_based_view/view_class_tainted_data/" -d "{'name':'<script>alert(1)</script>'}"
    def post(self, req):
        self.logger.info("TaintedData:post " + req.body.decode('utf-8')) # CWEID 117
        return HttpResponse("TaintedData:post " + str(req.POST.get('name')))  # CWEID 80

    # Attack.Payload curl -X PUT 'http://localhost:8000/class_based_view/view_class_tainted_data/' --cookie "tainted_cookie=<scriptalert(1)</script>>"
    def put(self, req):
        self.logger.info("TaintedData:put --------------------" + req.COOKIES.get('tainted_cookie')) # CWEID 117
        return HttpResponse("TaintedData:put " + req.body.decode('utf-8'))  # CWEID 80

    # Attach.Payload curl -X PATCH 'http://localhost:8000/class_based_view/view_class_tainted_data/' --cookie "tainted_cookie=<scriptalert(1)</script>>"
    def patch(self, req):
        self.logger.info("TaintedData:patch " + req.COOKIES.get('tainted_cookie')) # CWEID 117
        return HttpResponse("TaintedData:patch " + req.body.decode('utf-8'))  # CWEID 80

    # Attach.Payload curl -X DELETE  'http://localhost:8000/class_based_view/view_class_tainted_data/' --cookie "tainted_cookie=<scriptalert(1)</script>>"
    def delete(self, req):
        self.logger.info("TaintedData:delete " + req.COOKIES.get('tainted_cookie')) # CWEID 117
        return HttpResponse("TaintedData:delete " + req.body.decode('utf-8'))  # CWEID 80

    # Attack.Payload curl -X HEAD -I 'http://localhost:8000/class_based_view/view_class_tainted_data/' --cookie "tainted_cookie=<scriptalert(1)</script>>"
    def head(self, req):
        self.logger.info("TaintedData:head " + req.COOKIES.get('tainted_cookie')) # CWEID 117
        return HttpResponse("TaintedData:head " + req.body.decode('utf-8'))  # CWEID 80

    # Attach.Payload curl -X OPTIONS 'http://localhost:8000/class_based_view/view_class_tainted_data/' --cookie "tainted_cookie=<scriptalert(1)</script>>"
    def options(self, req):
        self.logger.info("TaintedData:options " + req.COOKIES.get('tainted_cookie')) # CWEID 117
        return HttpResponse("TaintedData:options " + req.body.decode('utf-8'))  # CWEID 80

    #def trace(self, req):
    #    self.logger.info("TaintedData:trace " + req.body.decode('utf-8')) # CWEID 117
    #    return HttpResponse("TaintedData:trace " + req.body.decode('utf-8'))  # CWEID 80

## Arguments can be passed to Views using either path converters, or positional arguments.
# Path Converters which are either specified as '<str:' in URLConf, or nothing which defaults to str are passed as positional arguments.
# Thus,  tainted_data/path_converter/<str:tag_slug>/ or tainted_data/path_converter/<tag_slug>/ could be access directly as kwargs or tag_slug variable name

class TaintedDataPathConverter(View):
    logger = logging.getLogger(__name__)

    # Attach.Payload curl -X GET 'http://localhost:8000/class_based_view/view_class_tainted_data/path_converter/<script>alert(1)<script>/'
    def get(self, request, *args, **kwargs):
        self.logger.debug("TaintedDataPathConverter:get with args " , args ) # FP CWEID 117
        self.logger.debug("TaintedDataPathConverter:get with kwargs" + kwargs['tag_slug'] ) # CWEID 117
        return HttpResponse("TaintedDataPathConverter:get with kwargs " + kwargs['tag_slug'])  # CWEID 80

class FPTaintedDataPathConverter(View):
    logger = logging.getLogger(__name__)

    # Attach.Payload curl -X GET 'http://localhost:8000/class_based_view/view_class_tainted_data/fp_path_converter/<script>alert(tainted_arg)/<script>alert(tainted_arg_1)/2/'
    def get(self, request, *args, **kwargs):
        query_dict = QueryDict(mutable=True)
        query_dict.update(**kwargs)
        self.logger.debug("FPTaintedDataPathConverter: post QueryDict " + query_dict['tainted_arg'] + query_dict['tainted_arg_1']) # CWEID 117
        self.logger.debug("FPTaintedDataPathConverter:get " + kwargs['tainted_arg']) # CWEID 117
        self.logger.debug("FPTaintedDataPathConverter:get " + kwargs['tainted_arg_1']) # CWEID 117
        return HttpResponse("FPTaintedDataPathConverter:get " + str(kwargs['tag_id']))  # FP CWEID 80

# Exercising Http404 as SINK
class TaintedDataHttp404(View):
    logger = logging.getLogger(__name__)

    # Attack.Payload curl 'http://localhost:8000/class_based_view/view_class_tainted_data/http_404/?name=<script>alert(1)</script>'
    def get(self, request):
        self.logger.debug("In TaintedDataHttp404 " + str(request.GET.get('name'))) # CWEID 117
        raise Http404("Http 404 " + str(request.GET.get('name'))) # CWEID 80

class IndexView(View):
    logger = logging.getLogger(__name__)

    # Attack.Payload curl 'http://localhost:8000/class_based_view/view_class_tainted_data/index/' -d "name=<script>alert(1)</script>"
    def post(self,request, *args, **kwargs):
        self.logger.debug("IndexView: get " + request.body.decode('utf-8')) # CWEID 117
        return HttpResponse("IndexView: get " + request.body.decode('utf-8')) # CWEID 80

# Attack.Payload curl --include 'http://localhost:8000/class_based_view/template_class_tainted_data/render_response/<script>/'
class RenderResponseTemplate(TemplateView):
    logger = logging.getLogger(__name__)

    def get_template_names(self):
        return 'render_response.html'

    def render_to_response(self, context, **response_kwargs):
        self.logger.debug("RenderResponseTemplate: render_to_response " + context['tainted_args']) # CWEID 117
        taint = context['tainted_args'] # Tainted data propogated
        return super(TemplateView,self).render_to_response({'taint':taint}) # Tainted data being passed to template


class TaintSourceArg(TemplateView):
    logger = logging.getLogger(__name__)
    template_name = 'kwargs_tainted_context.html'

    # Attack.Payload curl -X GET 'http://localhost:8000/class_based_view/template_class_tainted_data/<script>/'
    def get_context_data(self, **kwargs):
        self.logger.debug("TaintSourceArg:  get_context_data" + kwargs['tainted_arg'] ) # CWEID 117
        return {'tainted_data': kwargs['tainted_arg']}

class TaintedArgRedirectView(RedirectView):
    permanent = True
    logger = logging.getLogger(__name__)

    # Attack.Payload curl --include 'http://localhost:8000/class_based_view/redirect_class_tainted_data/tainted_redirect_url/cnn.com/'
    def get_redirect_url(self, *args, **kwargs):
        self.logger.debug("TaintedArgRedirectView: get_redirect_url " + kwargs['tainted_args'])
        return "https://" + kwargs['tainted_args']

# Attack.Payload curl --include 'http://localhost:8000/class_based_view/redirect_class_tainted_data/tainted_url_param/cnn.com/'
class TaintedUrlParam(RedirectView):
    url = 'https://%(tainted_args)s' # CWEID 601
