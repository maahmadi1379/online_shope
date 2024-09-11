from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.users.models import OTP
from apps.users.serializers import (
    EmailRequestSerializers,
    EmailVerifySerializers,
    PhoneNumberRequestSerializers,
    PhoneNumberVerifySerializers,
)
from apps.users.services.otp import OTPService
from apps.users.services.token import TokenService
from apps.users.services.user import UserService


class EmailRegisterRequestAPIView(APIView):
    def post(self, request):
        serializer = EmailRequestSerializers(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')

        user_obj = UserService.detail(email=email)

        if user_obj is not None:
            return Response({'detail': 'Email Exists'}, status=status.HTTP_400_BAD_REQUEST)

        expire_time = OTPService.request(
            otp_type=OTP.EMAIL,
            email=email,
        )

        return Response({'expire_time': expire_time}, status=status.HTTP_200_OK)


class EmailRegisterVerifyAPIView(APIView):
    def post(self, request):
        serializer = EmailVerifySerializers(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_obj = OTPService.verify(
            register=True,
            otp_type=OTP.EMAIL,
            code=serializer.validated_data.get('code'),
            email=serializer.validated_data.get('email'),
        )

        if user_obj is None:
            return Response({'detail': 'OTP Not Exists'}, status=status.HTTP_404_NOT_FOUND)

        access, refresh = TokenService.generate(user_obj)

        return Response({'refresh': refresh, 'access': access}, status=status.HTTP_200_OK)


class PhoneNumberRegisterRequestAPIView(APIView):
    def post(self, request):
        serializer = PhoneNumberRequestSerializers(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data.get('phone_number')

        user_obj = UserService.detail(phone_number=phone_number)

        if user_obj is not None:
            return Response({'detail': 'Phone Number Exists'}, status=status.HTTP_400_BAD_REQUEST)

        expire_time = OTPService.request(
            otp_type=OTP.PHONE_NUMBER,
            phone_number=serializer.validated_data.get('phone_number'),
        )

        return Response({'expire_time': expire_time}, status=status.HTTP_200_OK)


class PhoneNumberRegisterVerifyAPIView(APIView):
    def post(self, request):
        serializer = PhoneNumberVerifySerializers(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_obj = OTPService.verify(
            register=True,
            otp_type=OTP.PHONE_NUMBER,
            code=serializer.validated_data.get('code'),
            phone_number=serializer.validated_data.get('phone_number'),
        )

        if user_obj is None:
            return Response({'detail': 'OTP Not Exists'}, status=status.HTTP_404_NOT_FOUND)

        access, refresh = TokenService.generate(user_obj)

        return Response({'refresh': refresh, 'access': access}, status=status.HTTP_200_OK)


class EmailLoginRequestAPIView(APIView):
    def post(self, request):
        serializer = EmailRequestSerializers(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')

        user_obj = UserService.detail(email=email)

        if user_obj is None:
            return Response({'detail': 'Email Not Exists'}, status=status.HTTP_404_NOT_FOUND)

        expire_time = OTPService.request(
            otp_type=OTP.EMAIL,
            email=email,
        )

        return Response({'expire_time': expire_time}, status=status.HTTP_200_OK)


class EmailLoginVerifyAPIView(APIView):
    def post(self, request):
        serializer = EmailVerifySerializers(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_obj = OTPService.verify(
            register=False,
            otp_type=OTP.EMAIL,
            code=serializer.validated_data.get('code'),
            email=serializer.validated_data.get('email'),
        )

        if user_obj is None:
            return Response({'detail': 'OTP Not Exists'}, status=status.HTTP_404_NOT_FOUND)

        access, refresh = TokenService.generate(user_obj)

        return Response({'refresh': refresh, 'access': access}, status=status.HTTP_200_OK)


class PhoneNumberLoginRequestAPIView(APIView):
    def post(self, request):
        serializer = PhoneNumberRequestSerializers(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data.get('phone_number')

        user_obj = UserService.detail(phone_number=phone_number)

        if user_obj is None:
            return Response({'detail': 'Phone Number Not Exists'}, status=status.HTTP_404_NOT_FOUND)

        expire_time = OTPService.request(
            otp_type=OTP.PHONE_NUMBER,
            phone_number=serializer.validated_data.get('phone_number'),
        )

        return Response({'expire_time': expire_time}, status=status.HTTP_200_OK)


class PhoneNumberLoginVerifyAPIView(APIView):
    def post(self, request):
        serializer = PhoneNumberVerifySerializers(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_obj = OTPService.verify(
            register=False,
            otp_type=OTP.PHONE_NUMBER,
            code=serializer.validated_data.get('code'),
            phone_number=serializer.validated_data.get('phone_number'),
        )

        if user_obj is None:
            return Response({'detail': 'OTP Not Exists'}, status=status.HTTP_404_NOT_FOUND)

        access, refresh = TokenService.generate(user_obj)

        return Response({'refresh': refresh, 'access': access}, status=status.HTTP_200_OK)

# Create your views here.
