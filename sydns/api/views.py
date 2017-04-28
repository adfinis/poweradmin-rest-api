from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import ParseError
from sydns.api.models import Domain, Record, User, Zone
from sydns.api.serializers import (DomainSerializer, RecordSerializer,
                                   ZoneSerializer)


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
        allowed_zones = [zone.id for zone in
                         Zone.objects.filter(owner=owner.id)]

        return Domain.objects.filter(pk__in=allowed_zones)

    def create(self, request):
        """
        Link user to the created domain through a record in the in the
        intermediate "zones" table.
        """
        owner = User.objects.get(username=request.user.username)

        domain_serializer = DomainSerializer(data=request.data)
        domain_serializer.is_valid()
        domain = domain_serializer.save()

        zone = ZoneSerializer(data={'domain_id': domain.id, 'owner': owner.id})
        zone.is_valid()
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

        return all([
            self.request.query_params.get(f)
            for f
            in self.required_filters
        ])


class RecordViewSet(RequiredFilterViewSetMixin, viewsets.ModelViewSet):
    """
    This viewset provides actions around `records`.
    """
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticated,)
    required_filters = ('domain',)

    def get_queryset(self):
        """
        Only return records which the user is allowed to manage.
        """

        # django_auth_ldap converts the username to lowercase when
        # creating a new user
        owner = User.objects.get(username__iexact=self.request.user.username)

        domain_name = self.request.query_params.get('domain')
        domain = Domain.objects.get(name=domain_name)

        # Check wheter the requested domain belongs to the user
        if domain.id in [zone.id for zone
                         in Zone.objects.filter(owner=owner.id)]:
            return Record.objects.filter(domain_id=domain.id)
        else:
            return None

    # def create(self, request):

    #     owner = User.objects.get(username__iexact=self.request.user.username)

    #     data = request.data
    #     record_serializer = RecordSerializer(data=data)
    #     print(record_serializer)
    #     record_serializer.is_valid()
    #         record_serializer.save()

    #         return Response(record_serializer.data,
    #                         status=status.HTTP_201_CREATED)

    #     else:
    #         return Response(record_serializer.data,
    #                         status=status.HTTP_403_FORBIDDEN)
