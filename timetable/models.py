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
    TYPES = (
        (0, 'Lecture'),
        (1, 'Tutorial'),
        (2, 'Lab'),
    )
    DAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    HOURS = (
        (0, '8am'),
        (1, '8:30am'),
        (2, '9am'),
        (3, '9:30am'),
        (4, '10am'),
        (5, '10:30am'),
    )    
    course = models.ForeignKey(Course, null=True)
    name = models.CharField(max_length=20) 
    classtype = models.IntegerField(default=0, choices=TYPES)
    timeFrom = models.IntegerField(default=2, choices=HOURS)
    timeTo = models.IntegerField()
    day = models.IntegerField(default=0, choices=DAYS)
    students = models.ManyToManyField("Timetable", blank=True)
    def __str__(self):
        return self.name

