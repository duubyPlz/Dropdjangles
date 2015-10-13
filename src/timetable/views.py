from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Course, Timetable, Class, UserProfile
from django.contrib.auth.models import User

@csrf_exempt
def timetable(request):
    # Require user to login inorder to continue
    if not request.user.is_authenticated():
        return login(request)

    # Load the course list and class list
    course_list = Course.objects.order_by('name')
    class_list = Class.objects.all()

    # Get the timetable from the user if there is one
    # Create one if it doesn't exist
    usr_profile = request.user.profile
    timetable = usr_profile.timetable
    if timetable is None:
        timetable = Timetable.objects.create(name=current_user.username+"'s 15s2")
        usr_profile.timetable = timetable
        usr_profile.save()

    # Get all the courses from the user's timetable
    timetableCourses = timetable.courses.all()
    context = {
        'course_list': course_list,
        'timetableCourses': timetableCourses,
        # 'class_list': class_list,
    }

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
