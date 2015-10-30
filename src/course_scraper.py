#!/usr/bin/python
# NOTE: populate_class needs to account for course semester/year as well
#       as name since multiple course objects may have the same name
#imports
import sys
import fileinput   
import subprocess  
import urllib2     #wget
import re          #regex

# ###########################################################
# S1: USES LIST OF SUBJECT PREFIXES TO FIND EVERY COURSE CODE
# ###########################################################

#find list of prefixes from URL
subjectURL = "http://www.timetable.unsw.edu.au/current/subjectSearch.html"
response = urllib2.urlopen(subjectURL)
courseHTML = response.read()

#filter the html
prefix_list = []
for line in courseHTML.splitlines():
#    break
    line = line.strip()
    prefixFind = re.search(r'[A-Z]{4}KENS\.html\"\>([A-Z]{4})\<',line)
    if (prefixFind is not None):
        prefix = prefixFind.group(1)
        prefix_list.append(prefix)

#loop over every prefix site to find list of courses
course_list = []
for prefix in prefix_list:
#    break
    prefix = "{0}KENS".format(prefix) #must appent KENS so each UNSW course prefix
    prefixURL = "http://www.timetable.unsw.edu.au/current/{0}.html".format(prefix)
    response = urllib2.urlopen(prefixURL)
    prefixHTML = response.read()
    for line in prefixHTML.splitlines():
        line = line.strip()
        if (re.search('[A-Z]{4}[0-9]{4}',line) is not None):
            line = re.sub('[^A-Za-z0-9]+','\>',line)
            line = re.sub('^\>','',line)
            line = re.sub('\>$','',line)
            line_list = line.split('\>')
            for course in line_list:
                if (re.match('[A-Z]{4}[0-9]{4}',course) is not None):
                    if course not in course_list: #add the course to course_list if
                        course_list.append(course)#it doesn't already exist there

# ######################################################
# S2: USING EACH COURSE CODE, RETRIEVES TIMETABLING DATA
# ######################################################

#get the current teaching period
semest1 = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Dec']
currDate = subprocess.check_output(["date"])
dateList = currDate.split(" ")
currMonth = dateList[1].strip()
currYear = dateList[5].strip()

currSem = "2" #default value
if currMonth in semest1:
    currSem = "1"

#manually set year and semester
currSem = "2"
currYear = "2015"

#loop over each course
#replace with: for subject in sys.stdin.readlines(): 
#to test with STDIN instead of every course available
for subject in course_list: 
#for subject in sys.stdin.readlines():
    sys.stdout.write("course = Course(name=\"{0}\", semester={1}, year={2})\n".format(subject, currSem, currYear));
