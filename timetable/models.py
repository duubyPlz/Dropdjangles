from django.db import models
from django.forms import ModelForm
from swampdragon.models import SelfPublishModel
from timetable.serializers import TimetableSerializer, ClassSerializer

class Timetable(SelfPublishModel, models.Model):
    serializer_class = TimetableSerializer
    name = models.CharField(max_length=100)
    
class Course(SelfPublishModel, models.Model):
    name = models.CharField(max_length=20)
    timetable = models.ForeignKey(Timetable)

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
    timetable = models.ForeignKey(Timetable)
    name = models.CharField(max_length=10) 
    classtype = models.IntegerField(default=0, choices=TYPES)
    timeFrom = models.IntegerField()
    timeTo = models.IntegerField()
    day = models.IntegerField(default=0, choices=DAYS)

'''  
class SearchForm(SelfPublishModel, models.Model):
    class Meta:
        model = Course
'''

