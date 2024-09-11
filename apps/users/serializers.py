from rest_framework import serializers

from apps.users.models import OTP, User
from apps.shopping.services.order import OrderService
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


class UserProfileSerializer(serializers.ModelSerializer):
    order_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'email',
            'phone_number',
            'order_id',
        )

    def get_order_id(self, instance):
        order_obj = OrderService.get_current_user_order(instance)

        if order_obj is not None:
            return order_obj.id

        return None
