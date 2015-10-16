from django.db import models
from django.forms import ModelForm
from swampdragon.models import SelfPublishModel
from timetable.serializers import TimetableSerializer, ClassSerializer, CourseSerializer

from django.contrib.auth.models import User

class Timetable(SelfPublishModel, models.Model):
    serializer_class = TimetableSerializer
    name = models.CharField(max_length=100,default="15s2")
    courses = models.ManyToManyField("Course", blank=True)
    classes = models.ManyToManyField("Class", blank=True, related_name="timetable")

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
    classtype = models.CharField(max_length=70, default='Not specified')
    enrols = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    room = models.CharField(max_length=170, default='Not specified')
    # students = models.ManyToManyField("Timetable",blank=True)

    # Here, we'll return the dictionary as part of the model
    def as_dict(self):
        return dict(
            # course = self.course,
            name = self.name,
            timeFrom = self.timeFrom,
            timeTo = self.timeTo,
            day = self.day,
            classtype = self.classtype,
            enrols = self.enrols,
            capacity = self.capacity,
            room = self.room,
            # students = self.students
        )
    

    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    timetable = models.OneToOneField(Timetable, primary_key=False,unique=True, null=True, blank=True)
    friends = models.ManyToManyField('UserProfile',blank=True)
    pending_friends = models.ManyToManyField('UserProfile',related_name='pendingFriends',blank=True)

    # we can access the user profile by user.profile
    User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

    def __str__(self):
        return self.user.username



