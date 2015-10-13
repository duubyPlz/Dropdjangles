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
    # class_list = Class.objects.all()

    # Get the timetable from the user if there is one
    # Create one if it doesn't exist
    usr_profile = request.user.profile
    timetable = usr_profile.timetable
    if timetable is None:
        timetable = Timetable.objects.create(name=current_user.username+"'s 15s2")
        usr_profile.timetable = timetable
        usr_profile.save()


    # find the course instance and add the course to the timetable
    if request.POST.get("course_code"):
        course = Course.objects.raw("SELECT * FROM timetable_course WHERE name=%s",[request.POST.get("course_code")])[0]
        timetable.courses.add(course)
        timetable.save()

    if request.POST.get("rm_course"):
        course = Course.objects.raw("SELECT * FROM timetable_course WHERE name=%s",[request.POST.get("rm_course_code")])[0]
        timetable.courses.remove(course)
        timetable.save()
    
    # Get all the courses from the user's timetable
    timetableCourses = timetable.courses.all()
    # Get all the class from the courses
    class_list = []
    for course in timetableCourses:
        for c in Class.objects.raw("SELECT * FROM timetable_class WHERE name=%s",[course.name]):
                class_list.append(c)

    context = {
        'course_list': course_list,
        'timetableCourses': timetableCourses,
        'class_list': class_list,
    }
    return render(request, 'main.html' ,context)

@csrf_exempt
def login(request):
    if request.user.is_authenticated():
        return timetable(request)
    return render(request, 'custom_login.html', {})
