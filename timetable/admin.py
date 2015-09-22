from django.contrib import admin
from timetable.models import Timetable, Class, Course, CourseInstance, ClassInstance

admin.site.register(Timetable)
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(CourseInstance)
admin.site.register(ClassInstance)
