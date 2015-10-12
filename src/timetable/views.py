from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Course, Timetable, Class
# Create your views here.

@csrf_exempt
def timetable(request):
    # direct user to login if they arn't
    if not request.user.is_authenticated():
        return login(request)

    course_list = Course.objects.order_by('name')
    class_list = Class.objects.all()
    for obj in Timetable.objects.all(): #for all timetables
        timetableCourses = obj.courses.all()
        context = {
            'course_list': course_list,
            'timetableCourses': timetableCourses,
            'class_list': class_list,
        }
        # we only want the first timetable
        break
    # find the course instance and add the course to the timetable
    if request.POST.get("course_code"):
        # print request.POST.get("course_code")
        timetable = Timetable.objects.all()[0]
        for course in Course.objects.order_by('name'):
            # print course
            if course.name == request.POST.get("course_code"):
                timetable.courses.add(course)
                break
    if request.POST.get("rm_course"):
        #print "removing '%s'" %(request.POST.get("rm_course_code"))
        timetable = Timetable.objects.all()[0]
        for course in Course.objects.order_by('name'):
            if course.name == request.POST.get("rm_course_code"):
                timetable.courses.remove(course)
                break
    # print "start render"
    return render(request, 'main.html' ,context)


@csrf_exempt
def login(request):
    if request.user.is_authenticated():
        return timetable(request)
    return render(request, 'custom_login.html', {})
