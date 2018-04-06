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

import hello.Parse as Parse
from django.conf import settings
import os
import subprocess
import time

def test(request):
    s = os.getcwd() + "/hello"
    return HttpResponse(s)

def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')
 
    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    parse = 'hello/Parse.py'
    subprocess.check_output(['python3',parse,'upload/' + filename, 'upload/' + filename[:-4] + '.txt'])


def annotate(path,name):
    if not os.path.exists('annotated'):
        os.mkdir('annotated')
    subprocess.check_output(['python3', 'Converter.py', 'upload/' + name + '.xml', 'annotated/' + name + '_annotated.xml'])

def upload(request):
    # Handle file upload
    if request.method == 'POST':
        xmlfile = request.FILES['xmlfile']
        # response = HttpResponse(xmlfile.read(), content_type="application/xhtml+xml")
        # response['Content-Disposition'] = 'attachment;filename=' + request.FILES['xmlfile'].name
        handle_uploaded_file(xmlfile,str(xmlfile))
        annotate('upload/' + str(xmlfile)[:-4]+'.txt', str(xmlfile)[:-4])
        annotated = 'annotated/' + str(xmlfile)[:-4] + '_annotated.xml'
        return render(request, 'index.html', {'Files' : [str(xmlfile)[:-4] + '_annotated.xml']})

    return render(request, 'index.html')

def manual(request):
    return render(request, 'UserManual.html')

def index(request):
    # return HttpResponse('Hello from Python!')
    if not os.path.exists('annotated'):
        os.mkdir('annotated')
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

