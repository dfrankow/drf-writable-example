from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Avatar, Site, AccessKey, Profile, User, Thing, ThingVersion


class AvatarSerializer(serializers.ModelSerializer):
    image = serializers.CharField()

    class Meta:
        model = Avatar
        fields = ('pk', 'image',)


class SiteSerializer(serializers.ModelSerializer):
    url = serializers.CharField()

    class Meta:
        model = Site
        fields = ('pk', 'url',)


class AccessKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessKey
        fields = ('pk', 'key',)


class ProfileSerializer(WritableNestedModelSerializer):
    # Direct ManyToMany relation
    sites = SiteSerializer(many=True)

    # Reverse FK relation
    avatars = AvatarSerializer(many=True)

    # Direct FK relation
    access_key = AccessKeySerializer(allow_null=True)

    class Meta:
        model = Profile
        fields = ('pk', 'sites', 'avatars', 'access_key',)


class UserSerializer(WritableNestedModelSerializer):
    # Reverse OneToOne relation
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('pk', 'profile', 'username',)


class ThingSerializer(WritableNestedModelSerializer):
    DEFAULT_MATCH_ON = ['name']

    class Meta:
        model = Thing
        fields = ('name',)


class ThingVersionSerializer(WritableNestedModelSerializer):
    DEFAULT_MATCH_ON = ['thing', 'version']

    class Meta:
        model = ThingVersion
        fields = ('thing', 'version')

        # Direct FK relation
        thing = ThingSerializer(allow_null=True)
