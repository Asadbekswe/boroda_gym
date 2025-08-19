from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.core.exceptions import ValidationError


class CustomUserManager(UserManager):

    def _create_user_object(self, email, phone_number, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, email, phone_number, password, **extra_fields):
        """
        Create and save a user with the given phone_number,email, and password.
        """
        user = self._create_user_object(email, phone_number, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, phone_number, password, **extra_fields)

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, phone_number, password, **extra_fields)


def validate_phone_number(value: str) -> None:
    if not value.startswith('+998'):
        raise ValidationError("This field accepts only Phone number +998901001010 !!!")
