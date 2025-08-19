from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import User


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'email', 'password',


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'phone_number', 'email',


class EmailModelSerializer(Serializer):
    email = EmailField(max_length=255, help_text='Enter email')


class VerifyModelSerializer(Serializer):
    email = EmailField(max_length=255, help_text='Enter email')
    code = CharField(max_length=6, help_text='Enter confirmation code')

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        cache_code = str(cache.get(email))
        if code != cache_code:
            raise ValidationError('Code not found or timed out')

        return attrs
