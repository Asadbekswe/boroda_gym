from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices
from django.db.models.fields import CharField, EmailField

from apps.managers import CustomUserManager, validate_phone_number


class User(AbstractUser):
    class Gender(TextChoices):
        MALE = 'MALE', 'male'
        FEMALE = 'FEMALE', 'female'

    middle_name = CharField(max_length=60, blank=True, null=True)
    username = None
    email = EmailField(max_length=255, unique=True)
    phone_number = CharField(max_length=13, unique=True, validators=[validate_phone_number], blank=True)
    gender = CharField(max_length=6, choices=Gender.choices, db_default=Gender.MALE)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['phone_number']
    objects = CustomUserManager()
