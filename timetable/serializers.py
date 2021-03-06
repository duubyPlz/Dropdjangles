from swampdragon.serializers.model_serializer import ModelSerializer

class TimetableSerializer(ModelSerializer):
    class Meta:
        model = 'timetable.Timetable'
        publish_fields = ('name', 'description')

class ClassSerializer(ModelSerializer):
    class Meta:
        model = 'timetable.Class'
        publish_fields = ('name', 'timeFrom', 'timeTo')

class CourseSerializer(ModelSerializer):
    class Meta:
        model = 'timetable.Course'
        publish_fields = ('name', 'year', 'semester')

class CourseInstanceSerializer(ModelSerializer):
    class Meta:
        model = 'timetable.CourseInstance'
        publish_fields = ('base', 'user')

class ClassInstanceSerializer(ModelSerializer):
    class Meta:
        model = 'timetable.ClassInstance'
        publish_fields = ('base', 'user')
