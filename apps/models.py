from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField

from apps.managers import CustomUserManager, validate_phone_number


class User(AbstractUser):
    username = None
    phone_number = CharField(max_length=13, unique=True, validators=[validate_phone_number])
    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
