from django.db import models
from swampdragon.models import SelfPublishModel
from timetable.serializers import TimetableSerializer, ClassSerializer

class Timetable(SelfPublishModel, models.Model):
    serializer_class = TimetableSerializer
    name = models.CharField(max_length=100)
    

class Class(SelfPublishModel, models.Model):
    serializer_class = ClassSerializer
    timetable = models.ForeignKey(Timetable)
    name = models.CharField(max_length=10) 
    timeFrom = models.IntegerField()
    timeTo = models.IntegerField()
    
