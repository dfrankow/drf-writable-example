from django.test import TestCase

from .serializers import SiteSerializer


class SerializerTest(TestCase):
    def test_serialize_site(self):
        url = 'google.com'
        serializer = SiteSerializer(data={'url': url})
        serializer.is_valid(raise_exception=True)
        site = serializer.save()

        # Test the object has been created properly
        self.assertEqual(url, site.url)
