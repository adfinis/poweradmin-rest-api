from django.conf.urls import url
from rest_framework import routers
from powerdns.api.views import DomainViewSet, RecordViewSet
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


router = routers.SimpleRouter()
router.register(r'domains', DomainViewSet, base_name='domain')
router.register(r'records', RecordViewSet, base_name='record')

urlpatterns = router.urls

urlpatterns += [
    url(r'^token-auth/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
]
