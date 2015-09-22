from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter
from timetable.models import Timetable, Class, Course, ClassInstance, CourseInstance
from timetable.serializers import TimetableSerializer, ClassSerializer, CourseSerializer, ClassInstanceSerializer, CourseInstanceSerializer

class TimetableRouter(ModelRouter):
    route_name = 'timetable'
    serializer_class = TimetableSerializer
    model = Timetable

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()

class ClassRouter(ModelRouter):
    route_name = 'class'
    serializer_class = ClassSerializer
    model = Class

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])
    def get_query_set(self, **kwargs):
        return self.model.objects.filter(class__id=kwargs['list_id'])

class CourseRouter(ModelRouter):
    route_name = 'course'
    serializer_class = CourseSerializer
    model = Course

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])
    def get_query_set(self, **kwargs):
        return self.model.objects.all()

class CourseInstanceRouter(ModelRouter):
    route_name = 'courseInstance'
    serializer_class = CourseInstanceSerializer
    model = CourseInstance

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])
    def get_query_set(self, **kwargs):
        return self.model.objects.filter(class__id=kwargs['timetable_id'])    

class ClassInstanceRouter(ModelRouter):
    route_name = 'classInstance'
    serializer_class = ClassInstanceSerializer
    model = ClassInstance

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])
    def get_query_set(self, **kwargs):
        return self.model.objects.filter(class__id=kwargs['timetable_id'])

route_handler.register(TimetableRouter)
route_handler.register(ClassRouter)
route_handler.register(CourseRouter)
route_handler.register(CourseInstanceRouter)
route_handler.register(ClassInstanceRouter)
