from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    """Контроллер для модели курс, сделан через вьювсет"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [~IsModerator, IsOwner]

        return super().get_permissions()



class LessonsCreateAPIView(CreateAPIView):
    """Контроллеры для модели лессон, сделаны через джинерик"""
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]


class LessonsListAPIView(ListAPIView):
    """контроллер получения списка уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonsRetrieveAPIView(RetrieveAPIView):
    """контролер детализации конкретного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonsUpdateAPIView(UpdateAPIView):
    """контроллер обновления урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonsDestroyAPIView(DestroyAPIView):
    """контроллер удаления урока"""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]


class SubscriptionAPIView(APIView):
    """контроллен подписок/отписок на обновления курса"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course")
        course_item = Course.objects.get(id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'

        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})


