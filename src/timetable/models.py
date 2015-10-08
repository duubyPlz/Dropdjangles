from django.db import models
from django.forms import ModelForm
from swampdragon.models import SelfPublishModel
from timetable.serializers import TimetableSerializer, ClassSerializer, CourseSerializer

class Timetable(SelfPublishModel, models.Model):
    serializer_class = TimetableSerializer
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField("Course", blank=True)
    classes = models.ManyToManyField("Class", blank=True)
    def __str__(self):
        return self.name
    
class Course(SelfPublishModel, models.Model):
    serializer_class = CourseSerializer
    SEMESTERS = (
        (0, 'One'),
        (1, 'Two'),
    )
    name = models.CharField(max_length=20)
    year = models.IntegerField(default=2015)
    semester = models.IntegerField(default=0, choices=SEMESTERS)
    students = models.ManyToManyField("Timetable")
    def __str__(self):
        return self.name

# https://docs.djangoproject.com/en/1.8/ref/models/fields/
class Class(SelfPublishModel, models.Model):
    serializer_class = ClassSerializer
    DAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    course = models.ForeignKey(Course, null=True)
    name = models.CharField(max_length=20,default='Not specified')
    timeFrom = models.CharField(max_length=10,default='0')
    timeTo = models.CharField(max_length=10, default='0')
    day = models.IntegerField(default=0, choices=DAYS)
    classtype = models.CharField(max_length=40, default='Not specified')
    enrols = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    room = models.CharField(max_length=60, default='Not specified')
    students = models.ManyToManyField("Timetable")
    def __str__(self):
        return self.name
