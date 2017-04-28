from django_filters.rest_framework import FilterSet
from django_filters import NumberFilter
from models import Domain


class DomainFilter(FilterSet):
    test_type = NumberFilter(name='domain')

    class Meta:
        model = Domain
        fields = ['domain']
