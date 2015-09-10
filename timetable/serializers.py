from swampdragon.serializers.model_serializer import ModelSerializer

class TimetableSerializer(ModelSerializer):
    class Meta:
        model = 'timetable.Timetable'
        publish_fields = ('name', 'description')

class ClassSerializer(ModelSerializer):
    class Meta:
        model = 'timetable.Class'
        publish_fields = ('name', 'timeFrom', 'timeTo')
