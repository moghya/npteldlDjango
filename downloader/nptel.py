#author: moghya
import json as j
import requests as r
import urllib.request as u
from bs4 import BeautifulSoup as b

def getSearchFeature():
    filters = {
        "disps":[],
        "inss" : []
    }
    s = r.session()
    page=s.get('http://nptel.ac.in/course.php')
    if page.status_code!=200:
        return 1,None
    else:
        soup = b(page.text,'html.parser')
        for li in soup.find('div',{'id':'discipline'}).find('ul').findAll('li'):
            name = str(li.text).strip(' \n \n ')
            value = str(li.find('input')['value']).strip(' \n \n ')
            filters['disps'].append((name,value))
        for li in soup.find('div',{'id':'institute'}).find('ul').findAll('li'):
            name = str(li.text).strip(' \n \n ')
            value = str(li.find('input')['value']).strip(' \n \n ')
            filters['inss'].append((name,value))
        return filters

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
        soup = b(page.text,'html.parser')
        video = soup.find('div',{'id':'download'}).findAll('p')[0].findAll('a')[0].attrs['href']
        lecture = {
            'href':video
        }
        return lecture

def searchCourses(dispid,ins):
    s = r.Session()
    data = {
        'search_ctype':'video',
        'offset':1
    }
    if dispid!="-1":
        data['search_dispid']=int(dispid),
    if ins!='':
        data['search_ins']=ins
    courses = []
    page = s.post('http://nptel.ac.in/server.php',data=data)
    if page.status_code==200:
        courses = j.loads(page.text)
        if isinstance(courses,list):
            pages = courses[0]['pages']
            i = 2
            while i <= pages:
                data['offset'] = i
                page = s.post('http://nptel.ac.in/server.php',data=data)
                courses = courses + j.loads(page.text)
                i = i + 1
        print(courses)
    return courses

def getCourseData(courseId):
    course = {
        "courseId" : str(courseId),
        "name": "",
        "isFree" : 0,
        "modules":[],
        "lecturesLinks":[],
        "handouts":[],
        "assignments":[],
        "lecture_notes":[],
        "self_evaluation":[],
    }
    s = r.session()
    page=s.get('http://nptel.ac.in/courses/'+courseId+'/')
    if page.status_code!=200:
        return 1,None
    else:
        soup = b(page.text,'html.parser')
        if soup.find('div',{'id':'modError'}):
            return 2,None
        else:
            js = soup.find('script',type="application/ld+json").text
            jsobj = j.loads(js)
            if jsobj['isAccessibleForFree'] and jsobj['isAccessibleForFree'] == "True":
                course['isFree'] = 1
                course['name'] = jsobj['name']
                course['lecturesLinks'] = jsobj['partOfEducationalTrack']

                if soup.find('div',{'id':'div_lm'}) and soup.find('div',{'id':'div_lm'}).findAll('a',{'class':'header','href':'#'}):
                    mods = soup.find('div',{'id':'div_lm'}).findAll('a',{'class':'header','href':'#'})
                else:
                    return 2,None
                if soup.find('div',{'id':'div_lm'}) and soup.find('div',{'id':'div_lm'}).findAll('ul'):
                    uls = soup.find('div',{'id':'div_lm'}).findAll('ul')
                else:
                    return 2,None
                i=1
                linkCounter = 0
                modules = course['modules']
                for m in mods:
                    lis = uls[i].findAll('li')
                    modules.append({
                        'moduleName':str(m.text),
                        'totalLectures':len(lis),
                        'lectures':[]
                    })
                    print(len(lis))
                    for li in lis:
                        lec={
                            'lectureName':str(li.text),
                            'lecturelink':course['lecturesLinks'][linkCounter],
                            'downlink':''
                        }
                        print(lec)
                        modules[i-1]['lectures'].append(lec)
                        linkCounter+=1

                    i+=1
            return 0,course