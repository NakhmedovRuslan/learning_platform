from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.views import (CourseViewSet, LessonsCreateAPIView,
                             LessonsDestroyAPIView, LessonsListAPIView,
                             LessonsRetrieveAPIView, LessonsUpdateAPIView, SubscriptionAPIView)

app_name = "materials"

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonsListAPIView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonsRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonsCreateAPIView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/update/", LessonsUpdateAPIView.as_view(), name="lessons_update"
    ),
    path(
        "lessons/<int:pk>/destroy/",
        LessonsDestroyAPIView.as_view(),
        name="lessons_destroy",
    ),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions_list"),
]

urlpatterns += router.urls
