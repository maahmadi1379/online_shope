from rest_framework import serializers

from apps.users.models import OTP, User
from apps.utils.validators import validate_phone_number


class EmailRequestSerializers(serializers.Serializer):
    email = serializers.EmailField(required=True)


class EmailVerifySerializers(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)


class PhoneNumberRequestSerializers(serializers.Serializer):
    phone_number = serializers.IntegerField(required=True, validators=[validate_phone_number])


class PhoneNumberVerifySerializers(serializers.Serializer):
    phone_number = serializers.IntegerField(required=True, validators=[validate_phone_number])
    code = serializers.CharField(required=True)
