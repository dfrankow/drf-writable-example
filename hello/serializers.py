from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from drf_writable_nested.mixins import RelatedSaveMixin, \
    GetOrCreateNestedSerializerMixin

from .models import Avatar, Site, AccessKey, Profile, User


class AvatarSerializer(serializers.ModelSerializer):
    image = serializers.CharField()

    class Meta:
        model = Avatar
        fields = ('pk', 'image',)


class SiteSerializer(serializers.ModelSerializer,
                     GetOrCreateNestedSerializerMixin):
    url = serializers.CharField()
    DEFAULT_MATCH_ON = ['url']

    class Meta:
        model = Site
        fields = ('pk', 'url',)


class AccessKeySerializer(serializers.ModelSerializer,
                          GetOrCreateNestedSerializerMixin):
    DEFAULT_MATCH_ON = ['key']

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
