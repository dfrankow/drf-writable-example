"""From https://github.com/beda-software/drf-writable-nested"""

from django.db import models


class Site(models.Model):
    url = models.CharField(max_length=100)


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)


class AccessKey(models.Model):
    key = models.CharField(max_length=100)


class Profile(models.Model):
    sites = models.ManyToManyField(Site)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    access_key = models.ForeignKey(AccessKey, null=True,
                                   on_delete=models.DO_NOTHING)


class Avatar(models.Model):
    image = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, related_name='avatars',
                                on_delete=models.DO_NOTHING)


class Thing(models.Model):
    name = models.CharField(unique=True, blank=True, null=True, max_length=191)


class ThingVersion(models.Model):
    thing = models.ForeignKey(Thing, models.DO_NOTHING, blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('thing',),)


