from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.views import PaymentsViewSet
from django.urls import path


app_name = "users"

router = DefaultRouter()
router.register("payments", PaymentsViewSet)

urlpatterns = router.urls


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]