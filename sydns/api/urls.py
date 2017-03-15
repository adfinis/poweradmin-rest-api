from django.conf.urls import url, include
from sydns.api import views
from sydns.api.views import DomainViewSet, RecordViewSet

domain_list = DomainViewSet.as_view({
    'get': 'list',
    'put': 'update',
    'post': 'create',
    'delete': 'destroy'
})

domain_detail = DomainViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'post': 'create',
    'delete': 'destroy'
})

record_list = RecordViewSet.as_view({
    'get': 'list',
    'put': 'update',
    'post': 'create',
    'delete': 'destroy'
})

record_detail = RecordViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'post': 'create',
    'delete': 'destroy'
})


urlpatterns = [
    url(r'^domains/(?P<name>.*)/$', domain_detail, name='domain-detail'),
    url(r'^domains/$', domain_list, name='domain-list'),
    url(r'^records/(?P<pk>[0-9]+)/$', record_detail, name='record-detail'),
    url(r'^records/$', record_list, name='record-list'),
    url(r'^api-auth/', include('rest_framework.urls',)),
    url(r'^', views.api_root),
]
