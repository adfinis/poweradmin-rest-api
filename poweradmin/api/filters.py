import django_filters
from django_filters.rest_framework import FilterSet

from .models import Record


class RecordFilter(FilterSet):
    domain = django_filters.CharFilter(name='domain__name')

    class Meta:
        model = Record
        fields = [
            'domain',
            'name',
        ]
