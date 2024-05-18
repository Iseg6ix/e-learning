from django.shortcuts import render, HttpResponse

def home(request):
    return HttpResponse('<hi> Big Day</h1>')


# Create your views here.
