from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.validators import validate_video_link



from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.CharField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True)

    def get_lesson_count(self, obj):
        return LessonSerializer.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = "__all__"
