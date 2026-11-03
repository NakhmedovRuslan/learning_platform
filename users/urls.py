from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import CustomUserCreateAPIView, PaymentsViewSet, CustomUserListAPIView, CustomUserRetrieveAPIView, \
    CustomUserUpdateAPIView, CustomUserDestroyAPIView

app_name = "users"

router = DefaultRouter()
router.register("payments", PaymentsViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path("register/", CustomUserCreateAPIView.as_view(), name="register"),

    path("users/", CustomUserListAPIView.as_view(), name="user_list"),
    path("users/<int:pk>/", CustomUserRetrieveAPIView.as_view(), name="user_detail"),
    path("users/<int:pk>/update/", CustomUserUpdateAPIView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/", CustomUserDestroyAPIView.as_view(), name="user_delete"),

    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login",),
    path("token/refresh/",TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh",),
]
