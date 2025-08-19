from rest_framework.serializers import ModelSerializer

from apps.models import User


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'phone_number', 'email', 'password',
