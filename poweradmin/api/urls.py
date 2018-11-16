from rest_framework import routers

from .views import DomainViewSet, RecordViewSet

router = routers.SimpleRouter()
router.register(r'domains', DomainViewSet, basename='domain')
router.register(r'records', RecordViewSet, basename='record')

urlpatterns = router.urls
