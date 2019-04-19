from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from django.core.exceptions import ObjectDoesNotExist

from .models import Avatar, Site, AccessKey, Profile, User


class GetOrCreateModelSerializer(serializers.ModelSerializer):
    """Implement get-or-create semantics.

    Requires id_fields in the Meta information, used to check for existence.
    """

    def create(self, validated_data):
        """Implement get-or-create semantics."""
        model_class = self.Meta.model
        kwargs = {field: self.validated_data[field]
                  for field in self.Meta.id_fields}
        print("get-or-create model_class %s kwargs: %s" % (
            model_class.__name__, str(kwargs)))

        try:
            instance = model_class.objects.get(**kwargs)
            # TODO(dan): For fields not in id_fields, should we update?
        except ObjectDoesNotExist:
            instance = super().create(validated_data)
        return instance


class AvatarSerializer(GetOrCreateModelSerializer):
    image = serializers.CharField()

    class Meta:
        model = Avatar
        fields = ('pk', 'image',)
        # id_fields for get_or_create
        id_fields = ('image',)


class SiteSerializer(GetOrCreateModelSerializer):
    url = serializers.CharField()

    class Meta:
        model = Site
        fields = ('pk', 'url',)
        # id_fields for get_or_create
        id_fields = ('url',)


class AccessKeySerializer(GetOrCreateModelSerializer):

    class Meta:
        model = AccessKey
        fields = ('pk', 'key',)
        # id_fields for get_or_create
        id_fields = ('key',)


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
