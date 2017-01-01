#author: moghya
import json as j
import requests as r
import urllib.request as u
from bs4 import BeautifulSoup as b


def getCourseData(courseId):
    course = {
        "courseId" : str(courseId),
        "name": "",
        "isFree" : 0,
        "modules":[],
        "lectureDownloads":[],
        "lecturesLinks":[],
        "syllabus":"http://nptel.ac.in/syllabus/syllabus_pdf/"+courseId+".pdf",
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
                    modules = soup.find('div',{'id':'div_lm'}).findAll('a',{'class':'header','href':'#'})
                else:
                    return 2,None
                if soup.find('div',{'id':'div_lm'}) and soup.find('div',{'id':'div_lm'}).findAll('ul'):
                    uls = soup.find('div',{'id':'div_lm'}).findAll('ul')
                else:
                    return 2,None
                i=1
                for m in modules:
                    course['modules'].append({
                        'name':str(m.text),
                        'lectures':[]
                    })
                    i = i + 1
                l=1
                for i in range(1,len(uls)):
                    ul=uls[i]
                    mod = ""+str(i)
                    if(i<10):
                        mod = "0"+ mod
                    mod = "mod" + mod
                    for li in ul.findAll('li'):
                        lec = ""+str(l)
                        if l < 10:
                            lec = "0"+lec
                        srt = "http://nptel.ac.in/srt/"+courseId+"/Lec-"+lec+".srt"
                        lec = "lec"+lec
                        downlink = "http://npteldownloads.iitm.ac.in/downloads_mp4/"+courseId+"/"+mod + lec + ".mp4"
                        pdf = "http://textofvideo.nptel.iitm.ac.in/"+courseId+"/lec"+str(l)+".pdf"
                        name = str(li.text)
                        download = mod + lec + '___' + name
                        lecture = [name,downlink,download,pdf,srt]
                        course['modules'][i-1]['lectures'].append(lecture)
                        down = {
                            'download': download ,
                            'href' : downlink,
                            'pdf'  : pdf,
                            'srt'  : srt
                        }
                        course['lectureDownloads'].append(down)
                        l = l + 1
            page = s.get('http://nptel.ac.in/downloads/'+courseId+'/')
            if page.status_code==200:
                soup = b(page.text,'html.parser')
                if soup.find('div',{'id':'tab1'}):
                    trs = soup.find('div',{'id':'tab1'}).find('tbody').findAll('tr')
                    for tr in trs:
                        pdf = 'http://nptel.ac.in/' + tr.findAll('td')[1].find('a')['href']
                        filename = 'lecturenotes__'+pdf.split('/')[-1]
                        lectureNote = {
                            'pdf':pdf,
                            'filename':filename
                        }
                        course['lecture_notes'].append(lectureNote)
                if soup.find('div',{'id':'tab3'}):
                    trs = soup.find('div',{'id':'tab3'}).find('tbody').findAll('tr')
                    for tr in trs:
                        pdf = 'http://nptel.ac.in/' + tr.findAll('td')[1].find('a')['href']
                        filename = 'assignments__'+pdf.split('/')[-1]
                        assignment = {
                            'pdf':pdf,
                            'filename':filename
                        }
                        course['assignments'].append(assignment)
                if soup.find('div',{'id':'tab4'}):
                    trs = soup.find('div',{'id':'tab4'}).find('tbody').findAll('tr')
                    for tr in trs:
                        pdf = 'http://nptel.ac.in/' + tr.findAll('td')[1].find('a')['href']
                        filename = 'self_evaluation__'+pdf.split('/')[-1]
                        assignment = {
                            'pdf':pdf,
                            'filename':filename
                        }
                        course['self_evaluation'].append(assignment)
            return 0,course


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
        local_filename = video.split('/')[-1].split('.')[0] + '___' + soup.find('li',{'class':'here'}).text  +'.' + video.split('/')[-1].split('.')[1]
        lecture = {
            'download':local_filename,
            'href':video
        }
        return lecture

#getCourseData('106108051')