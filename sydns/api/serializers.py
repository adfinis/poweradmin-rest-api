from rest_framework import serializers
from api.models import Domain, Record, Zone


class DomainSerializer(serializers.HyperlinkedModelSerializer):

    # `NATIVE` replication is the default, unless other operation is specifically configured. Native
    # replication basically means that PowerDNS will not send out DNS update notifications, nor will
    # react to them. PowerDNS assumes that the backend is taking care of replication unaided.
    # Other options include `SLAVE` and `MASTER`.
    type = serializers.CharField(default='NATIVE')

    class Meta:
        lookup_field = 'name'
        model = Domain
        fields = ('name', 'type', 'master')
        read_only_fields = ('type', 'master')


class RecordSerializer(serializers.HyperlinkedModelSerializer):

    domain_id = serializers.HyperlinkedRelatedField(read_only=True, view_name='domain-detail')

    class Meta:
        model = Record
        fields = ('id', 'domain_id', 'name', 'type', 'content', 'ttl', 'prio',)


class ZoneSerializer(serializers.ModelSerializer):

    zone_templ_id = serializers.IntegerField(default=0)
    comment = serializers.CharField(default='Created through REST API')

    class Meta:
        model = Zone
        fields = ('domain_id', 'owner', 'zone_templ_id', 'comment')
        read_only_fields = ('zone_templ_id', 'comment')
