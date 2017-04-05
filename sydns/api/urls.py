from django.conf.urls import include, url
from rest_framework import routers
from sydns.api import views
from sydns.api.views import DomainViewSet, RecordViewSet


router = routers.SimpleRouter()
router.register(r'domains', DomainViewSet, base_name='domain')
router.register(r'records', RecordViewSet, base_name='record')

urlpatterns = router.urls

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',)),
    url(r'^', views.api_root),
]
