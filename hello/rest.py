from rest_framework import routers, viewsets

from .models import User


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = User
    # TODO(dan): Review for security


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserModelViewSet)
