from rest_framework.routers import DefaultRouter
from users.views import PaymentsViewSet

app_name = "users"

router = DefaultRouter()
router.register("payments", PaymentsViewSet)

urlpatterns = router.urls