from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def redirect(request):
    return HttpResponseRedirect('/admin/')