from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from downloader.nptel import *

def index(request):
    filters = getSearchFeature()
    context = {
        'filters' : filters
    }
    if  request.method == "POST":
        dispid = request.POST['dispid']
        ins = request.POST['ins']
        courses = searchCourses(dispid,ins)
        context['courses'] = courses
    return render(request,'npteldl/index.html',context)