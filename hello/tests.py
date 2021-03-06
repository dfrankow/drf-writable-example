from django.test import TestCase

from .serializers import SiteSerializer, UserSerializer
from .models import Site

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
        self.assertEqual('test', user1.username)

        serializer = UserSerializer(data=self.USER_DATA)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        # change username and save again
        user_data = self.USER_DATA.copy()
        user_data['username'] = 'test2'
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user2 = serializer.save()

        self.assertEqual('test2', user2.username)

        # nested object keys are equal
        self.assertEqual(user1.profile.access_key.key,
                         user2.profile.access_key.key)

        # nested object ids are not equal
        self.assertNotEqual(user1.profile.access_key.id,
                            user2.profile.access_key.id)

    def test_save_site_twice(self):
        url = 'google.com'

        serializer = SiteSerializer(data={'url': url})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        self.assertEqual(url, obj.url)
        self.assertEqual(1, Site.objects.filter(url=url).count())

        serializer = SiteSerializer(data={'url': url})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        self.assertEqual(url, obj.url)
        self.assertEqual(2, Site.objects.filter(url=url).count())
