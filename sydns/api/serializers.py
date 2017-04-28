from rest_framework import serializers
from sydns.api.models import Domain, Record, Zone


class DomainSerializer(serializers.ModelSerializer):

    class Meta:
        lookup_field = 'name'
        model = Domain
        fields = ('name', 'type',)
        read_only_fields = ('type',)


class RecordSerializer(serializers.ModelSerializer):
    domain = serializers.SlugRelatedField(
        queryset=Domain.objects.all(), slug_field='name'
    )

    class Meta:
        model = Record
        fields = ('name', 'type', 'content', 'ttl', 'prio', 'domain')


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('domain', 'owner')
