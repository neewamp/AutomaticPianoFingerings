from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Greeting
from django.views.generic import TemplateView

from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

# from myproject.myapp.models import Document
# from myproject.myapp.forms import DocumentForm

from hello.models import Document
# from hello.forms import DocumentForm

from django.conf import settings
import os
import subprocess
import time

def test(request):
    s = os.getcwd()
    return HttpResponse(s)

def upload(request):
    # Handle file upload
    if request.method == 'POST':
        xmlfile = request.FILES['xmlfile']
        response = HttpResponse(xmlfile.read(), content_type="application/xhtml+xml")
        response['Content-Disposition'] = 'attachment;filename=' + request.FILES['xmlfile'].name
        return response

    return render(request, 'index.html')

def manual(request):
    return render(request, 'UserManual.html')

def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def weekone(request):
    return render(request, 'weekone/index.html')

def first(request):
    return render(request, 'weekone/WeekOne.html', {})

def pres(request):
    return render(request, 'presentation/index.html')


# def weekone(request):
#    return render(request, 'WeekOne.html', {})



# def index(request):
#     r = requests.get('http://httpbin.org/status/418')
#     print(r.text)
#     return HttpResponse('<pre>' + r.text + '</pre>')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

