from rest_framework.routers import DefaultRouter

from .views import RecordViewSet

router = DefaultRouter()
router.register(r'records', RecordViewSet, basename='user')
urlpatterns = router.urls