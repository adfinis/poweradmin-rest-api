from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import ParseError
from sydns.api.models import Domain, Record, User, Zone
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

    def create(self, request):
        """
        Link user to the created domain through a record in the in the
        intermediate "zones" table.

        TODO: this should happen on the serializer
        example: http://www.drf.org/api-guide/validators/#currentuserdefault
        """
        owner = User.objects.get(username__iexact=self.request.user.username)

        domain_serializer = DomainSerializer(data=request.data)
        domain_serializer.is_valid()
        domain = domain_serializer.save()

        zone = Zone(domain=domain, owner=owner.id)
        zone.save()

        return Response(domain_serializer.data, status=status.HTTP_201_CREATED)


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
