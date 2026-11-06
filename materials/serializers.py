from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_video_link


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.CharField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = "__all__"
