from rest_framework import serializers
from api.models import Domain, Record, Zone


class DomainSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        lookup_field = 'name'
        model = Domain
        fields = ('name', 'type',)
        read_only_fields = ('type',)


class RecordSerializer(serializers.HyperlinkedModelSerializer):

    domain_id = serializers.HyperlinkedRelatedField(read_only=True, view_name='domain-detail')

    class Meta:
        model = Record
        fields = ('id', 'domain_id', 'name', 'type', 'content', 'ttl', 'prio',)


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('domain_id', 'owner',)
