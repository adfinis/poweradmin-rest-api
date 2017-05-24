from django.db import transaction
from rest_framework import exceptions, serializers

from powerdns.api.models import Domain, Record, User, Zone


class DomainSerializer(serializers.ModelSerializer):

    @transaction.atomic
    def create(self, validated_data):
        """
        Link user to the created domain through a record in the in the
        intermediate "zones" table.
        """
        domain = super().create(validated_data)

        owner = User.objects.get(username__iexact=self.context['request'].user)
        Zone.objects.create(domain=domain, owner=owner.id)

        return domain

    class Meta:
        lookup_field = 'name'
        model = Domain
        fields = ('name', 'type',)
        read_only_fields = ('type',)


class RecordSerializer(serializers.ModelSerializer):
    domain = serializers.SlugRelatedField(
        queryset=Domain.objects.all(), slug_field='name'
    )

    def validate_domain(self, domain):
        """
        Check whether is allowed to update records on this domain
        """
        request = self.context['request']
        owner = User.objects.get(username__iexact=request.user.username)
        if not domain.zones.filter(owner=owner.id).exists():
            raise exceptions.PermissionDenied()

        return domain

    class Meta:
        model = Record
        fields = ('id', 'name', 'type', 'content', 'ttl', 'prio', 'domain')


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('domain', 'owner')
