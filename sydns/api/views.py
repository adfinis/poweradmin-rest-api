from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import ParseError
from sydns.api.models import Domain, Record, User
from sydns.api.permissions import IsRecordOwner
from sydns.api.serializers import (DomainSerializer, RecordSerializer)
from sydns.api.filters import RecordFilter


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'domains': reverse('domain-list', request=request, format=format),
        'records': reverse('record-list', request=request, format=format),
    })


class DomainViewSet(viewsets.ModelViewSet):
    """
    This viewset provides actions around `domains`.
    """
    serializer_class = DomainSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'name'
    lookup_value_regex = '.*'

    def get_queryset(self):
        """
        Only return domains which the user is allowed to manage.
        """

        # django_auth_ldap converts the username to lowercase when
        # creating a new user
        owner = User.objects.get(username__iexact=self.request.user.username)

        return Domain.objects.filter(zones__owner=owner.id)


class RequiredFilterViewSetMixin(object):
    """
    Define filters that have to be present
    Use when you don't want to return everything when no filter
    is specified.
    """
    required_filters = ()
    required_filter_actions = ('list',)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if not self.has_required_filters:
            raise ParseError()

    @property
    def has_required_filters(self):
        if self.action not in self.required_filter_actions:
            return True

        return all(
            self.request.query_params.get(f)
            for f
            in self.required_filters
        )


class RecordViewSet(RequiredFilterViewSetMixin, viewsets.ModelViewSet):
    """
    This viewset provides actions around `records`.
    """
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticated, IsRecordOwner)
    filter_class = RecordFilter
    required_filters = ('domain',)

    def get_queryset(self):
        """
        Only return records which the user is allowed to manage.
        """

        # django_auth_ldap converts the username to lowercase when
        # creating a new user
        owner = User.objects.get(username__iexact=self.request.user.username)
        return Record.objects.filter(
            domain__zones__owner=owner.id
        )
