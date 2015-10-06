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
        (0, '8:00'),
        (1, '8:30'),
        (2, '9:00'),
        (3, '9:30'),
        (4, '10:00'),
        (5, '10:30'),
        (6, '11:00'),
        (7, '11:30'),
        (8, '12:00'),
        (9, '12:30'),
        (10, '13:00'),
        (11, '13:30'),
        (12, '14:00'),
        (13, '14:30'),
        (14, '15:00'),
        (15, '15:30'),
        (16, '16:00'),
        (17, '16:30'),
        (18, '17:00'),
        (19, '17:30'),
        (20, '18:00'),
        (21, '18:30'),
        (22, '19:00'),
        (23, '19:30'),
        (24, '20:00'),
        (25, '20:30'),
        (26, '21:00'),
        (27, '21:30'),
    )    
    course = models.ForeignKey(Course, null=True)
    name = models.CharField(max_length=20) 
    classtype = models.IntegerField(default=0, choices=TYPES)
    timeFrom = models.IntegerField(default=2, choices=HOURS)
    timeTo = models.IntegerField(default=4, choices=HOURS)
    day = models.IntegerField(default=0, choices=DAYS)
    students = models.ManyToManyField("Timetable", blank=True)
    def __str__(self):
        return self.name

