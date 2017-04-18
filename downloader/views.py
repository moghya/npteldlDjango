from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from downloader.nptel import *
import json
import traceback


def details(request):
    if  request.method == "POST":
        courseId = request.POST['courseId']
        success,course = getCourseData(courseId)
        context = {
            'course' : course
        }
        if success==0:
            return render(request,'downloader/details.html',context)
        else:
            return HttpResponse("We\'re sorry for this but,it seems you're trying to access invalid course or our system is down due to some unknown error. Please Try again later or reach us at ")
    else:
        return HttpResponse("you know i need course code for giving you details :)")

def getLecture(request):
    if request.method == "POST":
        try:
            link = request.POST['lectureLink']
            lecture = getLectureDownloadLink(link)
            return HttpResponse(json.dumps(lecture), content_type="application/json")
        except:
            lecture = {
                'download':'',
                'href':''
            }
            return HttpResponse(json.dumps(lecture), content_type="application/json")
    else:
        return HttpResponse("Sorry buddy nothing is here :)")
