from api.models import Domain, Record, Zone, User
from api.serializers import DomainSerializer, RecordSerializer
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated


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
    lookup_field = "name"

    def get_queryset(self):
        '''Only return domains which the user is allowed to manage.

        '''
        owner = User.objects.get(username=self.request.user.username)
        allowed_zones = [zone.id for zone in Zone.objects.filter(owner=owner.id)]

        return Domain.objects.filter(pk__in=allowed_zones)



class RecordList(generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticated,)

class RecordDetail(generics.RetrieveUpdateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticated,)
