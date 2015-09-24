#!/usr/bin/env python

#imports
import sys
import fileinput   
import subprocess  
import urllib2     #wget
import re          #regex

print

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
    line = line.strip()
    prefixFind = re.search(r'[A-Z]{4}KENS\.html\"\>([A-Z]{4})\<',line)
    if (prefixFind is not None):
        prefix = prefixFind.group(1)
        prefix_list.append(prefix)

#loop over every prefix site to find list of courses
course_list = []
for prefix in prefix_list:
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

#loop over each course
#replace with: for subject in sys.stdin.readlines(): 
#to test with STDIN instead of every course available
for subject in course_list: 
    currSub = subject.strip('\r\n') #remove newline, whitespace, etc

    #make subject headers
    sys.stdout.write("\n    //    ")
    sys.stdout.write(currSub)
    sys.stdout.write(" Semester ")
    sys.stdout.write(currSem)
    sys.stdout.write(" ")
    sys.stdout.write(currYear)
    print "    //\n"

    #open html with respect to current year/subject
    currURL = "http://www.timetable.unsw.edu.au/{0}/{1}.html".format(currYear, currSub)
    response = urllib2.urlopen(currURL)
    HTML = response.read()

    #flags/counters
    lineNum = 0
    detailFlag = 0
    notesFlag = 1
    nextLineCapture = 0
    captureCapacity = 0
    weeksFlag = 0
   
    #iterate over the html
    for line in HTML.splitlines():
        line = line.strip()

        #check the capacity of the class
        if (captureCapacity == 1):
            line = re.sub('\<.+?\>','',line)
            line = re.sub('\ +','',line)
            sys.stdout.write("    Capacity: {0}\n".format(line))
            captureCapacity = 0
        if ("Enrols/Capacity" in line and detailFlag == 1):
            captureCapacity = 1
        
        #flag for reaching the 'details' section 
        if ("- Detail" in line):
            detailFlag = 1

        #detect the current activity e.g LECTURE/TUTORIAL
        if (nextLineCapture == 1):
            currLine = line
            currLine = re.sub('\<.+?\>','',currLine)
            currLine = re.sub('^\ +','',currLine)
            currLine = re.sub('\ $','',currLine)
            sys.stdout.write("    {0}\n".format(currLine))
            nextLineCapture = 0
        if ('label\">Activity' in line):
            nextLineCapture = 1

        #account for 'TUTORIAL 1 OF 2' problem, e.g Calc/Alg for MATH1141
        tutFind = re.search(r'Tutorial ([0-9]) of ([0-9])', line)
        if (tutFind is not None and detailFlag == 1): 
            tutCurr = tutFind.group(1)
            tutNeed = tutFind.group(2)
            sys.stdout.write("    {0} of {1}\n".format(tutCurr, tutNeed))

        #next activity
        if ("Class Notes" in line):
            sys.stdout.write("-----------------------\n")
            notesFlag = 1
        
        #clean current line of irrelevant tags
        line = re.sub('^\ +','',line)
        line = re.sub('\<(.+?)\>','',line)
        
        #blank line regex
        if (re.match('^\ *$',line) is not None):
            continue

        #weeks regex
        if (re.match('[0-9]+\-[0-9]\,',line) is not None):
            weeksFlag = 1
            lineNum = lineNum + 1
            continue

        #skip professor/lecturer, etc
        if ("Instructor" in line and detailFlag == 1):
            notesFlag = 0
            continue
 
        #print the clean line
        if (notesFlag == 0 and detailFlag == 1):
            sys.stdout.write("    {0}\n".format(line))
            lineNum = lineNum + 1
            continue
        
        lineNum = lineNum + 1
