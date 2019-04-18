from django.urls import include
from django.conf.urls import url

from rest_framework import urls as rest_framework_urls

from .rest import router

urlpatterns = [
    # Wire up rest
    # See https://www.django-rest-framework.org/
    url(r'^api/auth/', include(rest_framework_urls,
                               namespace='rest_framework')),
    url(r'^api/', include(router.urls))
]
