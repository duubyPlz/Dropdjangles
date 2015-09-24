from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse

from .models import Course, Timetable, Class
# Create your views here.

def index(request):
    course_list = Course.objects.order_by('name')
    timetableCourses = Timetable.objects.get(id=1).courses.all()
    class_list = Class.objects.all()
    template = loader.get_template('../templates/index.html')
    context = RequestContext(request, {
        'course_list': course_list,
        'timetableCourses': timetableCourses,
        'class_list': class_list,
    })
    return HttpResponse(template.render(context))
