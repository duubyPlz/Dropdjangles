from swampdragon import route_handler
from swampdragon.route_handler import ModelRouter
from timetable.models import Timetable, Class, Course
from timetable.serializers import TimetableSerializer, ClassSerializer, CourseSerializer

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
        return self.model.objects.filter(course__id=kwargs['list_id'])

route_handler.register(TimetableRouter)
route_handler.register(ClassRouter)
route_handler.register(CourseRouter)
