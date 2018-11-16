from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

from .filters import RecordFilter
from .models import Domain, Record
from .serializers import DomainSerializer, RecordSerializer


class DomainViewSet(viewsets.ModelViewSet):
    """
    This viewset provides actions around `domains`.
    """
    serializer_class = DomainSerializer
    lookup_field = 'name'
    lookup_value_regex = '.*'

    def get_queryset(self):
        """
        Only return domains which the user is allowed to manage.
        """
        return Domain.objects.filter(zones__owner=self.request.user.id)


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
    filterset_class = RecordFilter
    required_filters = ('domain',)

    def get_queryset(self):
        """
        Only return records which the user is allowed to manage.
        """
        return Record.objects.filter(
            domain__zones__owner=self.request.user.id
        )


class SwaggerSchemaView(APIView):  # pragma: no cover
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator(title='PowerAdmin API')
        schema = generator.get_schema(request=request)

        return Response(schema)
