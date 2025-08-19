from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError


class CustomUserManager(UserManager):

    def _create_user_object(self, phone_number, email, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, phone_number, email, password, **extra_fields):
        """
        Create and save a user with the given phone_number,email, and password.
        """
        user = self._create_user_object(phone_number, email, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)


def validate_phone_number(value: str) -> None:
    if not value.startswith('+998'):
        raise ValidationError("This field accepts only Phone number +998901001010 !!!")
