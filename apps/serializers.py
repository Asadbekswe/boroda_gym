from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import User
from apps.tasks import send_code_to_email
from apps.utils import sms_code


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


class ForgetPasswordSerializer(Serializer):
    email = CharField(max_length=255, required=True, write_only=True)
    new_password = CharField(max_length=50, required=True, write_only=True)
    confirm_password = CharField(max_length=50, required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] and attrs['new_password'] != attrs['confirm_password']:
            raise ValidationError('Password did not match !')

        email = attrs['email']
        code = sms_code()
        if not User.objects.filter(email=email):
            raise ValidationError('Bunday user mavjud emas')

        send_code_to_email(f"{email}", code)
        data = {
            'code': code,
            'new_password': attrs['new_password']
        }

        cache.set(email, data, 60)
        return attrs
