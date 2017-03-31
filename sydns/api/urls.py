from django.conf.urls import url, include
from sydns.api import views
from sydns.api.views import DomainViewSet, RecordViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'domains', DomainViewSet, base_name='domain')
router.register(r'records', RecordViewSet, base_name='record')

urlpatterns = router.urls

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',)),
    url(r'^', views.api_root),
]
