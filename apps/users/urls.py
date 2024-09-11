from django.urls import path

from apps.users.views import (
    EmailRegisterRequestAPIView,
    EmailRegisterVerifyAPIView,
    PhoneNumberRegisterRequestAPIView,
    PhoneNumberRegisterVerifyAPIView,

    EmailLoginRequestAPIView,
    EmailLoginVerifyAPIView,
    PhoneNumberLoginRequestAPIView,
    PhoneNumberLoginVerifyAPIView,
)

urlpatterns = [
    path('register/email/request/', EmailRegisterRequestAPIView.as_view(), name='register-email-request'),
    path('register/email/verify/', EmailRegisterVerifyAPIView.as_view(), name='register-email-verify'),
    path('register/phone-number/request/', PhoneNumberRegisterRequestAPIView.as_view(), name='register-phone-number-request'),
    path('register/phone-number/verify/', PhoneNumberRegisterVerifyAPIView.as_view(), name='register-phone-number-verify'),

    path('login/email/request/', EmailLoginRequestAPIView.as_view(), name='login-email-request'),
    path('login/email/verify/', EmailLoginVerifyAPIView.as_view(), name='login-email-verify'),
    path('login/phone-number/request/', PhoneNumberLoginRequestAPIView.as_view(), name='login-phone-number-request'),
    path('login/phone-number/verify/', PhoneNumberLoginVerifyAPIView.as_view(), name='login-phone-number-verify'),
]
