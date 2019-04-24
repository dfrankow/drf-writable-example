from django.test import TestCase

from .serializers import SiteSerializer, UserSerializer

from rest_framework.exceptions import ValidationError


class SerializerTest(TestCase):
    USER_DATA = {
            'username': 'test',
            'profile': {
                'access_key': {
                    'key': 'key',
                },
                'sites': [
                    {
                        'url': 'http://google.com',
                    },
                    {
                        'url': 'http://yahoo.com',
                    },
                ],
                'avatars': [
                    {
                        'image': 'image-1.png',
                    },
                    {
                        'image': 'image-2.png',
                    },
                ],
            },
        }

    def test_serialize_site(self):
        url = 'google.com'
        serializer = SiteSerializer(data={'url': url})
        serializer.is_valid(raise_exception=True)
        site = serializer.save()

        # Test the object has been created properly
        self.assertEqual(url, site.url)

    def test_profile(self):
        serializer = UserSerializer(data=self.USER_DATA)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Test the object has been created properly
        self.assertEqual('test', user.username)
        self.assertEqual('key', user.profile.access_key.key)
        # id was assigned
        self.assertEqual(1, user.profile.access_key.id)

        self.assertEqual(2, user.profile.sites.count())
        site1 = user.profile.sites.get(id=1)
        self.assertEqual(1, site1.id)
        self.assertEqual('http://google.com', site1.url)

    def test_save_twice(self):
        serializer = UserSerializer(data=self.USER_DATA)
        serializer.is_valid(raise_exception=True)
        user1 = serializer.save()

        serializer = UserSerializer(data=self.USER_DATA)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
