# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Make sure each model has one field with primary_key=True
from __future__ import unicode_literals

from django.db import models


class Domain(models.Model):
    name = models.CharField(unique=True, max_length=255)
    master = models.CharField(max_length=20, blank=True, null=True)
    last_check = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=6)
    notified_serial = models.IntegerField(blank=True, null=True)
    account = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domains'


class Record(models.Model):
    domain = models.ForeignKey(
        Domain, models.CASCADE, blank=True, null=True
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    ttl = models.IntegerField(blank=True, null=True)
    prio = models.IntegerField(blank=True, null=True)
    change_date = models.IntegerField(blank=True, null=True)
    ordername = models.CharField(max_length=255, blank=True, null=True)
    auth = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'records'


class Zone(models.Model):
    domain = models.ForeignKey(Domain, models.CASCADE, related_name='zones')
    owner = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    zone_templ_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zones'


class User(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    fullname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    description = models.TextField()
    level = models.IntegerField()
    active = models.IntegerField()
    perm_templ = models.IntegerField()
    use_ldap = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users'


# following models are currently not in use but here for full representation
# of powerdns db schema

class Cryptokeys(models.Model):
    domain_id = models.IntegerField()
    flags = models.IntegerField()
    active = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cryptokeys'


class Domainmetadata(models.Model):
    domain_id = models.IntegerField()
    kind = models.CharField(max_length=16, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domainmetadata'


class Migrations(models.Model):
    version = models.CharField(max_length=255)
    apply_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class PermItems(models.Model):
    name = models.CharField(max_length=64)
    descr = models.TextField()

    class Meta:
        managed = False
        db_table = 'perm_items'


class PermTempl(models.Model):
    name = models.CharField(max_length=128)
    descr = models.TextField()

    class Meta:
        managed = False
        db_table = 'perm_templ'


class PermTemplItems(models.Model):
    templ_id = models.IntegerField()
    perm_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'perm_templ_items'


class RecordsZoneTempl(models.Model):
    domain_id = models.IntegerField()
    record_id = models.IntegerField()
    zone_templ_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'records_zone_templ'


class Supermasters(models.Model):
    ip = models.CharField(max_length=25)
    nameserver = models.CharField(max_length=255)
    account = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supermasters'


class Tsigkeys(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    algorithm = models.CharField(max_length=50, blank=True, null=True)
    secret = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tsigkeys'
        unique_together = (('name', 'algorithm'),)


class ZoneTempl(models.Model):
    name = models.TextField()
    descr = models.TextField()
    owner = models.IntegerField()
    global_field = models.IntegerField(db_column='global')

    class Meta:
        managed = False
        db_table = 'zone_templ'


class ZoneTemplRecords(models.Model):
    zone_templ_id = models.IntegerField()
    name = models.TextField()
    type = models.TextField()
    content = models.TextField()
    ttl = models.IntegerField()
    prio = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zone_templ_records'
