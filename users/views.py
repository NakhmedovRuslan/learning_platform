from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import CustomUser, Payments
from users.permissions import IsModerator
from users.serializers import CustomUsersSerializer, PaymentsSerializer
from users.services import (
    create_stripe_price,
    create_stripe_product,
    create_stripe_session,
)


class PaymentsViewSet(ModelViewSet):
    """контроллер информации о платеже"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]


class PaymentsCreateAPIView(CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]
        payment = serializer.save(user=self.request.user, payment_amount=course.price)
        product = create_stripe_product(payment.course.name)
        price = create_stripe_price(payment.payment_amount, product)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


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
