from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.utils.validators import validate_phone_number


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """

    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


class User(AbstractUser):
    password = models.CharField(max_length=128, null=True, blank=True)
    email = LowercaseEmailField(unique=True, null=True, blank=True)
    phone_number = models.BigIntegerField(unique=True, null=True, blank=True, validators=[validate_phone_number])

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        ordering = ['-date_joined']


class OTP(models.Model):
    EMAIL = 1
    PHONE_NUMBER = 2
    OTP_TYPE_CHOICES = (
        (EMAIL, 'email type'),
        (PHONE_NUMBER, 'phone number type'),
    )

    type = models.PositiveSmallIntegerField(choices=OTP_TYPE_CHOICES)
    email = LowercaseEmailField(null=True, blank=True)
    phone_number = models.BigIntegerField(null=True, blank=True, validators=[validate_phone_number])
    code = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
