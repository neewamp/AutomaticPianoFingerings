from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Greeting
from django.views.generic import TemplateView

# class StaticView(TemplateView):
#    template_name = "WeakOne.html"

def index(request):
    return HttpResponse('Hello from Python!')
    # return render(request, 'index.html')

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

