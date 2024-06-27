# Introduction:

[Django](https://www.djangoproject.com) and [Flask](https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/) are 2 popular python web frameworks we currently support. Django has its own templating language called [DTL](https://docs.djangoproject.com/en/3.0/ref/templates/language/#) (Django Templating language) and Flask uses [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templates. Django applications can also be configured to use Jinja templates. Interesting thing is Jinja2 templating language is based off DTL. Tags/filters which are relevant for us to normalize for further analysis is exactly the same in both these templating languages. Good news is we already support relevant part of DTL as part of our [Django 1.x template support](https://wiki.veracode.local/display/RES/Django+1.x+Normalizer+Additions) which can be utilized in Jinja2 as well.

Going forward, in normalizer component we remove distinction between various python web templating languages and frameworks its used in. This will enable us to support both frameworks with both templating languages for past and future framework supports.

From our current support, this specification adds upgrades for:

1. Flask 1.x using Jinja2 templates
2. Django 2.x using Jinja2 templates
3. Django 2.x using DjangoTemplates

In near future we would be updating our Django and Flask support to latest versions. Again same templating support discussed above can be extended to future versions of both these frameworks, which this specification provisions for. Testcases are provided, which can be used to test normalized outputs. Python Scanner might need additional intelligence around these future versions:

1. Django 3.x using Django Templates
2. Django 3.x using Jinja2 Templates
3. Flask 1.1.0 using Jinja2 Templates

Jinja2 templates are also used in bottle framework which we currently don't support. This specification, would normalize templates of bottle applications as well. Ofcourse, we wont find anything since python scanner doesn't have any intelligence about it.

# Normalizer:

## Detection:

[Django DTL Detection Spec](https://wiki.veracode.local/pages/viewpage.action?spaceKey=RES&title=Django+1.x+Normalizer+Additions#Django1.xNormalizerAdditions-Detection) specifies identifying Django projects based on presence of urls.py and settings.py files. With this specification, we are dealing with all python web templating languages similarly, thus removing the need to distinguish between django and flask apps. Thus, we would remove logic to look for urls.py/settings.py files and apply DTL rules to all html-like files [.html, .htm, .xhtml, .jinja, .jinja2]. Thus pseudo code would be something like:

```
if a submissions contains .py files: 
	for all html-like files:
		if html-like file contains DTL specific comment/tag/variable:
			apply DTL rules to convert it into corresponding .py file
		
```

## Extra specifications for supporting Jinja2 templates:

Everything from [DTL](https://wiki.veracode.local/display/RES/Django+1.x+Normalizer+Additions) also applied to Jinja2 templates. In addition we need to support below Jinja2 specific variables and tags:

**Variables:**

In addition to [DTL's Variables](https://wiki.veracode.local/display/RES/Django+1.x+Normalizer+Additions#Django1.xNormalizerAdditions-Variables), variables could be access as maps as under:

```
{{ foo['bar'] | safe }} {# CWEID 80 #}
```

**Tags:**

In addition to [DTL's url Tag](https://wiki.veracode.local/display/RES/Django+1.x+Normalizer+Additions#Django1.xNormalizerAdditions-The{%urlEXPRARG1ARG2...ARGn%}tag), add `url_for` for urls as well:

```
<a href="{{ url_for('auth.register') }}">Register</a>
```


# Testcases:



* [Django1 Using Django Templates](https://maven.laputa.veracode.io/api/object/snapshots/com/veracode/research/python-jinja2/Django1_DjangoTemplate.zip) - [Normalized version](https://maven.laputa.veracode.io/api/object/snapshots/com/veracode/research/python-jinja2/Django1_DjangoTemplate.zip_htmlpythoncode.veracodegen.htmla.pya)
* [Django2 using Django Template](https://maven.laputa.veracode.io/api/object/snapshots/com/veracode/research/python-jinja2/Django2_DjangoTemplate.zip) - [Normalized Version](https://maven.laputa.veracode.io/api/object/snapshots/com/veracode/research/python-jinja2/Django2_DjangoTemplate.zip_htmlpythoncode.veracodegen.htmla.pya)
* [Django 2 Using Jinja2 Templates](https://maven.laputa.veracode.io/api/object/snapshots/com/veracode/research/python-jinja2/Django2_Jinja2.zip) - [Normalized Version](https://maven.laputa.veracode.io/api/object/snapshots/com/veracode/research/python-jinja2/Django2_Jinja2.zip_htmlpythoncode.veracodegen.htmla.pya)

**Future versions** Testcases provided to test normalizer output.

* [Django3 Using Django Templates](https://maven.laputa.veracode.io/api/object/snapshots/com/veracode/research/python-jinja2/Django3_DjangoTemplate.zip) - [Normalized Version](https://maven.laputa.veracode.io/api/object/snapshots/com/veracode/research/python-jinja2/Django3_DjangoTemplate.zip_htmlpythoncode.veracodegen.htmla.pya)
* [Flask 1.1.0 Using Jinja2 Templates](https://maven.laputa.veracode.io/api/object/snapshots/com/veracode/research/python-jinja2/Flask1.1_Jinja2.zip) - [Normalized Version](https://maven.laputa.veracode.io/api/object/snapshots/com/veracode/research/python-jinja2/Flask1.1_Jinja2.zip_htmlpythoncode.veracodegen.htmla.pya): Please not, normalizer code was hacked to produce this normalized version of flask application. Attached normalized version is for reference purposes only.
* [Django3 Using Jinja2 Templates](https://maven.laputa.veracode.io/api/object/snapshots/com/veracode/research/python-jinja2/Django3_Jinja2.zip) - [Normalized Version](https://maven.laputa.veracode.io/api/object/snapshots/com/veracode/research/python-jinja2/Django3_Jinja2.zip_htmlpythoncode.veracodegen.htmla.pya)



# References:
* [Flask Specification](https://wiki.veracode.local/display/RES/Python+Research+Details)
* [Python Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
* [Jinja Documentation](https://jinja.palletsprojects.com/en/2.11.x/templates/)
* [Django2 Documentation](https://docs.djangoproject.com/en/2.2/)
* [Django3 Documentation](https://docs.djangoproject.com/en/3.0/)
* [Django1 Normalizer](https://wiki.veracode.local/display/RES/Django+1.x+Normalizer+Additions)
* Default Directory of templates in Django: https://docs.djangoproject.com/en/1.8/_modules/django/template/backends/django/
* Flask template rendering logic: https://flask.palletsprojects.com/en/1.1.x/quickstart/#rendering-templates