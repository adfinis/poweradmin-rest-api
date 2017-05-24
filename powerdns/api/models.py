from __future__ import unicode_literals
from django.db import models


class Domain(models.Model):
    name = models.CharField(unique=True, max_length=255)
    master = models.CharField(max_length=20, blank=True, null=True)
    last_check = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=6, default='NATIVE')
    """
    `NATIVE` replication is the default, unless other operation is specifically
    configured. Native replication basically means that PowerDNS will not send
    out DNS update notifications, nor will react to them. PowerDNS assumes that
    the backend is taking care of replication unaided.  Other options include
    `SLAVE` and `MASTER`.
    """
    notified_serial = models.IntegerField(blank=True, null=True)
    account = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'domains'


class Record(models.Model):
    domain = models.ForeignKey(
        'Domain',
        on_delete=models.CASCADE,
        related_name='records'
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
        managed = True
        db_table = 'records'


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
        managed = True
        db_table = 'users'


class Zone(models.Model):
    domain = models.ForeignKey(
        'Domain',
        on_delete=models.CASCADE,
        related_name='zones'
    )
    owner = models.IntegerField()
    # TODO: shouldn't this be a foreignkey?
    comment = models.TextField(blank=True, null=True)
    zone_templ_id = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'zones'
