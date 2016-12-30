from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from downloader.nptel import *
import json

def index(request):
    context = {
        'haha' : request,
    }
    return render(request,'downloader/index.html',context)

def details(request):
    if  request.method == "POST":
        try:
            courseId = request.POST['courseId']
            courseDetails = getCourseData(courseId)
            context = {
                'courseDetails' : courseDetails
            }
            return render(request,'downloader/details.html',context)
        except:
            return HttpResponse('Sorry we\'re down now :(')
            pass
    else:
        return HttpResponse("you know i need course code for giving you details :)")

def getLecture(request):
    if request.method == "POST":
        link = request.POST['lectureLink']
        lecture = getLectureDownloadLink(link)
        return HttpResponse(json.dumps(lecture), content_type="application/json")
    else:
        return HttpResponse("Sorry buddy nothing is here :)")
