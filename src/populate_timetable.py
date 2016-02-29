#usr/bin/python

#sys path
import re
import sys
sys.path.insert(0, '/dropjangles/')

#env variabls
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dropjangles.settings')

#mdels
from timetable.models import Course, Class

#django functions
import django
django.setup()

def populate():
    #populate courses
    courseFile = open("2016s1_django_course_list.txt")
    i = 0
    for course in courseFile.readlines():
        course = course.strip()
        print course
        exec(course)
        course.save()
        i = i + 1

    #populate classes
    #classFile = open("classLIST.txt")
    #for clss in classFile.readlines():
        #get current class
    #    currCrs = clss
    #    crsFind = re.search(r'([A-Z]{4}[0-9]{4})',currCrs)        
    #    if (crsFind is not None):
    #       currCrs = crsFind.group(1)

    #    relatedCourse = Course.objects.get(name=currCrs)
    #    exec(clss)
    #    c.course_id = relatedCourse.id
    #    c.save()

#start population
if __name__ == '__main__':
    print "Starting course population from scraper"
    populate()

# ADD COURSE
# CHAR NAME, INT YEAR, INT SEMESTER

# ADD CLASS
# CHAR NAME, INT timeFrom, INT timeTo, INT classtype, INT day, INT course_id
