from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView

from apps.models import User
from apps.serializers import UserCreateSerializer


@extend_schema(tags=['Users'])
class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
