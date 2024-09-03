from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.otp import OTPService
from utils.validators import validate_phone_number


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
    email = LowercaseEmailField(unique=True, null=True, blank=True)
    phone_number = models.IntegerField(unique=True, null=True, blank=True, validators=[validate_phone_number])

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
    code = models.CharField(default=OTPService.generate, max_length=10, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
