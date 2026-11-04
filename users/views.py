from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import CustomUser, Payments
from users.permissions import IsModerator
from users.serializers import CustomUsersSerializer, PaymentsSerializer


class PaymentsViewSet(ModelViewSet):
    """контроллер информации о платеже"""
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]


class CustomUserCreateAPIView(CreateAPIView):
    """контроллер регистрации пользователя"""
    serializer_class = CustomUsersSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class CustomUserListAPIView(ListAPIView):
    """контроллер вывода списка пользователей"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUsersSerializer
    permission_classes = [IsModerator]

class CustomUserRetrieveAPIView(RetrieveAPIView):
    """контроллер просмотра профиля пользователя"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUsersSerializer
    permission_classes = [IsAuthenticated]

class CustomUserUpdateAPIView(UpdateAPIView):
    """контроллер обновления пользователя"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUsersSerializer
    permission_classes = [IsAuthenticated]

class CustomUserDestroyAPIView(DestroyAPIView):
    """контроллер удаления пользователя"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUsersSerializer
    permission_classes = [IsModerator]