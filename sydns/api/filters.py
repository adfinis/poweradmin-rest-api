from django_filters.rest_framework import FilterSet
from sydns.api.models import Record


class RecordFilter(FilterSet):
    class Meta:
        model = Record
        fields = ['domain']
