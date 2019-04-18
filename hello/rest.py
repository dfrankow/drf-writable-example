from rest_framework import routers, viewsets

from .serializers import UserSerializer
from .models import ExampleUser


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ExampleUser.objects.all()
    serializer_class = UserSerializer
    # TODO(dan): Review for security


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserModelViewSet)
