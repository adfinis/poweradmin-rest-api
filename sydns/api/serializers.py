from rest_framework import serializers
from sydns.api.models import Domain, Record, Zone


class DomainSerializer(serializers.ModelSerializer):

    class Meta:
        lookup_field = 'name'
        model = Domain
        fields = ('name', 'type',)
        read_only_fields = ('type',)


class RecordSerializer(serializers.ModelSerializer):
    domain_name = serializers.StringRelatedField(many=False)

    class Meta:
        model = Record
        fields = ('id', 'domain_name', 'name',
                  'type', 'content', 'ttl', 'prio',)
        read_only_fields = ('id',)


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('domain_id', 'owner',)
