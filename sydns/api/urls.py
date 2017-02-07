from django.conf.urls import url, include
from api import views


urlpatterns = [
    url(r'^domains/(?P<name>.*)/$', views.DomainDetail.as_view(), name='domain-detail'),
    url(r'^domains/$', views.DomainList.as_view(), name='domain-list'),
    url(r'^records/(?P<pk>[0-9]+)/$', views.RecordDetail.as_view(), name='record-detail'),
    url(r'^records/$', views.RecordList.as_view(), name='record-list'),
    url(r'^api-auth/', include('rest_framework.urls',)),
    url(r'^', views.api_root),
]
