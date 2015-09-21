from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse

from .models import Course
# Create your views here.

def index(request):
    course_list = Course.objects.order_by('name')
    template = loader.get_template('../templates/index.html')
    
    return HttpResponse(template.render())
