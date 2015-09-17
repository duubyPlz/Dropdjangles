from django.db import models
from django.forms import ModelForm
from swampdragon.models import SelfPublishModel
from timetable.serializers import TimetableSerializer, ClassSerializer

class Timetable(SelfPublishModel, models.Model):
    serializer_class = TimetableSerializer
    name = models.CharField(max_length=100)
    
class Course(SelfPublishModel, models.Model):
    serializer_class = CourseSerializer
    name = models.CharField(max_length=20)
    timetable = models.ForeignKey(Timetable)

# https://docs.djangoproject.com/en/1.8/ref/models/fields/
class ClassType(SelfPublishModel, models.Model):
    LECTURE = 0
    TUTORIAL = 1
    LAB = 2
    TYPES = (
        (LECTURE, 'Lecture'),
        (TUTORIAL, 'Tutorial'),
        (LAB, 'Lab'),
    ) 

class Class(SelfPublishModel, models.Model):
    serializer_class = ClassSerializer
    timetable = models.ForeignKey(Timetable)
    name = models.CharField(max_length=10) 
    classtype = models.IntegerField(choices=TYPES)
    timeFrom = models.IntegerField()
    timeTo = models.IntegerField()
    
class SearchForm(SelfPublishModel, models.Model):
    serializer_class = SearchSerializer
    class Meta:
        model = Course



