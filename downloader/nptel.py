#author: moghya
import json as j
import requests as r
import urllib.request as u
from bs4 import BeautifulSoup as b


def getCourseData(courseId):
    course = {
        "courseId" : str(courseId),
        "name": "",
        "isFree" : False,
        "lecturesLinks":[],
    }
    s = r.session()
    page=s.get('http://nptel.ac.in/courses/'+courseId+'/')
    if page.status_code!=200:
        return None
    else:
        soup = b(page.text,'lxml')
        js = soup.find('script',type="application/ld+json").text
        jsobj = j.loads(js)
        if jsobj['isAccessibleForFree'] == "True":
            course['isFree'] = True
            course['name'] = jsobj['name']
            course['lecturesLinks'] = jsobj['partOfEducationalTrack']
    return course

def exportCourseData(courseData):
    courseId = courseData['courseId']
    f = open(courseId+'.js','w')
    f.write(j.dumps(courseData,indent=4))
    f.close()
    return

def getLectureDownloadLink(link):
    page=r.get(link)
    if page.status_code!=200:
        return None
    else:
        soup = b(page.text,'lxml')
        video = soup.find('div',{'id':'download'}).findAll('p')[0].findAll('a')[0].attrs['href']
        local_filename = video.split('/')[-1].split('.')[0] + '_' + soup.find('li',{'class':'here'}).text  +'.' + video.split('/')[-1].split('.')[1]
        lecture = {
            'download':local_filename,
            'href':video
        }
        return lecture