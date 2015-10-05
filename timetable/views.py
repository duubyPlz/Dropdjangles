from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse

from .models import Course, Timetable, Class
from .forms import CourseForm
# Create your views here.

def timetable(request):
    course_list = Course.objects.order_by('name')
    # print course_list
    for obj in Timetable.objects.all(): #for all timetables
        timetableCourses = obj.courses.all()
        # print timetableCourses
        class_list = Class.objects.all()
        # print class_list
        form = CourseForm(request.POST or None)
        context = {
            'course_form': form,
            'course_list': course_list,
            'timetableCourses': timetableCourses,
            'class_list': class_list,
        }
        # we only want the first timetable
        break
    # find the course instance and add the course to the timetable
    if form.is_valid():
        timetable = Timetable.objects.all()[0]
        for course in Course.objects.order_by('name'):
            if course.name == form.cleaned_data['course_code']:
                timetable.courses.add(course)
                break
    return render(request, 'main.html' ,context)



def login(request):
    return render(request, 'login.html', {})
