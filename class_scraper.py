#!/usr/bin/python
# NOTE: run using 'python class_scraper.py', pipe output to text file, which goes into populate_classes.py
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
    currSub = subject.strip('\r\n') #remove newline, whitespace, etc
    #print currSub
    #open html with respect to current year/subject
    currURL = "http://www.timetable.unsw.edu.au/{0}/{1}.html".format(currYear, currSub)
    #print currURL
    try:
        response = urllib2.urlopen(currURL)
        HTML = response.read()
    except urllib2.HTTPError, error:
        continue

    #flags/counters
    lineNum = 0
    daysFlag = 0
    dayNum = 0
    detailFlag = 0
    notesFlag = 1
    nextLineCapture = 0
    captureCapacity = 0
    weeksFlag = 0
    streamCounter = 0
   
    #iterate over the html
    for line in HTML.splitlines():
        line = line.strip()

        #check the capacity of the class
        if (captureCapacity == 1):
            line = re.sub('\<.+?\>','',line)
            line = re.sub('\ +','',line)
            line = re.sub('\*','',line)
            capacityFind = re.search(r'([0-9]+)\/([0-9]+)',line) #convert capacity to two variable ints
            if (capacityFind is not None):
                capCur = capacityFind.group(1)
                capMax = capacityFind.group(2)
            captureCapacity = 0
        if ("Enrols/Capacity" in line and detailFlag == 1):
            captureCapacity = 1
        
        #for some classes that offer in both semesters, the details flag is not enough
        if ('1' in currSem):
            if ("SEMESTER ONE CLASSES - Detail" in line):
                detailFlag = 1
            if ("SEMESTER TWO CLASSES - Detail" in line):
                detailFlag = 0
        elif ('2' in currSem):
            if ("SEMESTER ONE CLASSES - Detail" in line):
                detailFlag = 0
            if ("SEMESTER TWO CLASSES - Detail" in line):
                detailFlag = 1

        #detect the current activity e.g LECTURE/TUTORIAL
        if (nextLineCapture == 1):
            currLine = line
            currLine = re.sub('\<.+?\>','',currLine)
            currLine = re.sub('^\ +','',currLine)
            currLine = re.sub('\ $','',currLine)
            currActivity = currLine
            nextLineCapture = 0
        if ('label\">Activity' in line):
            nextLineCapture = 1

        #account for 'TUTORIAL 1 OF 2' problem, e.g Calc/Alg for MATH1141
        tutFind = re.search(r'Tutorial ([0-9]) of ([0-9])', line)
        if (tutFind is not None and detailFlag == 1): 
            tutCurr = tutFind.group(1)
            tutNeed = tutFind.group(2)

        #convert data into database format
        if (("Class Notes" in line) and detailFlag == 1):
            # CLASS FORMAT:
            # CLASS(CHAR name, INT timeFrom, INT timeTo, INT classType, INT day, INT course_id)
            # NOTES: DAYS --> 0 = MON, 1 = TUE, etc
            #        TYPE --> 0 = LEC, 1 = TUT, 2 = LAB
            # USE STDOUT TO SEND DJANGO COMMANDS
            sys.stdout.write("next-stream\n")
            #sys.stdout.write("c = Class(name=\"{0}\", timeFrom=\"{1}{2}\", timeTo=\"{3}{4}\", day={5}, classtype=\"{6}\", enrols={7}, capacity={8}, room=\"{9}\")\n".format(currSub, startHour, startMins, endHour, endMins, dayNum, currActivity, capCur, capMax, room))
            notesFlag = 1
        
        #clean current line of irrelevant tags
        line = re.sub('^\ +','',line)
        line = re.sub('\<(.+?)\>','',line)
        
        #blank line regex
        if (re.match('^\ *$',line) is not None):
            continue

        #here we want to detect whether or not classes/lectures/etc are in the same stream, e.g lecture on monday and wednesday
        #basic idea: start a counter before the classes e.g 'instruction mode' and end it at 'class notes', will give a count
        #            of how many classes to keep track of
        if ('Instruction Mode' in line and detailFlag == 1):
            #here we reset the stream counter which gets incremented on every 'dayFind' below
            streamCounter = 0

        #weeks regex
        #16th Oct update: in theory, when weeks are reached, then all relevant info is found, so we can print the class here, and not at the 'Class Notes'
        if ((re.match('[0-9]+\-[0-9]\,',line) is not None) and detailFlag == 1):
            weeksFlag = 1
            lineNum = lineNum + 1
            sys.stdout.write("c{0} = Class(name=\"{1}\", time_from=\"{2}{3}\", time_to=\"{4}{5}\", day={6}, classtype=\"{7}\", enrols={8}, capacity={9}, room=\"{10}\")\n".format(streamCounter, currSub, startHour, startMins, endHour, endMins, dayNum, currActivity, capCur, capMax, room))
            continue

        #capture time
        timeFind = re.search(r'([0-9]{2})\:([0-9]{2}) \- ([0-9]{2})\:([0-9]{2})', line) 
        if (timeFind is not None and detailFlag == 1):
            startHour = timeFind.group(1)
            startMins = timeFind.group(2)
            endHour = timeFind.group(3)
            endMins = timeFind.group(4)
            continue

        #capture day
        dayFind = re.search(r'(Mon|Tue|Wed|Thu|Fri|Sat|Sun)',line)
        if (dayFind is not None and detailFlag == 1):
            streamCounter = streamCounter + 1
            currDay = dayFind.group(1)
            currDay = currDay.strip()
            if ("Mon" in currDay):
                dayNum = 0
            elif ("Tue" in currDay):
                dayNum = 1
            elif ("Wed" in currDay):
                dayNum = 2
            elif ("Thu" in currDay):
                dayNum = 3
            elif ("Fri" in currDay):
                dayNum = 4
            elif ("Sat" in currDay):
                dayNum = 5
            elif ("Sun" in currDay):
                dayNum = 6
            daysFlag = 1
            continue

        #capture room
        if (daysFlag == 1 and detailFlag == 1):
            room = line
            room = re.sub(r"\s+\(.+?\)","",room)
            #print ("room: x{0}x".format(room))
            daysFlag = 0 
            continue

        #skip professor/lecturer, etc
        if ("Instructor" in line and detailFlag == 1):
            notesFlag = 0
            continue

        #print the clean line
        if (notesFlag == 0 and detailFlag == 1):
            #sys.stdout.write("    {0}\n".format(line))
            lineNum = lineNum + 1
            continue
        
        lineNum = lineNum + 1
