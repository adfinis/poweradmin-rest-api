from rest_framework import routers

from powerdns.api.views import DomainViewSet, RecordViewSet

router = routers.SimpleRouter()
router.register(r'domains', DomainViewSet, base_name='domain')
router.register(r'records', RecordViewSet, base_name='record')

urlpatterns = router.urls
