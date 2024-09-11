import random
from datetime import timedelta, datetime
from typing import Optional

from django.utils import timezone

from apps.users.models import OTP, User
from apps.utils.epoch import Epoch
from apps.users.services.user import UserService


class OTPService:

    @classmethod
    def get_delta_time(cls) -> datetime:
        expire_time = 120  # second

        delta_time = timezone.now() - timedelta(seconds=expire_time)

        return delta_time

    @classmethod
    def generate(cls) -> str:
        token = list(str(Epoch.microsecond_now())[-6:])
        random.shuffle(token)
        return ''.join(token)

    @classmethod
    def request(cls, otp_type: int, email: str = None, phone_number: int = None) -> int:
        delta_time = cls.get_delta_time()

        otp_objs = OTP.objects.filter(
            type=otp_type,
            email=email,
            phone_number=phone_number,
            created__gte=delta_time,
        ).order_by('-created')

        if otp_objs.exists():
            otp_obj = otp_objs.first()
        else:
            otp_obj = OTP.objects.create(
                type=otp_type,
                code=cls.generate(),
                email=email,
                phone_number=phone_number,
            )
            if otp_type == OTP.EMAIL:
                EmailService.send_code(code=otp_obj.code, email=email)
            elif otp_type == OTP.PHONE_NUMBER:
                SMSService.send_code(code=otp_obj.code, phone_number=phone_number)

        return int(abs(delta_time - otp_obj.created).total_seconds())

    @classmethod
    def verify(cls, register: bool, otp_type: int, code: str, email: str = None, phone_number: int = None) -> Optional[User]:
        delta_time = cls.get_delta_time()

        # Remove Extra codes
        OTP.objects.filter(
            type=otp_type,
            email=email,
            phone_number=phone_number,
            created__lt=delta_time,
        ).delete()

        otp_objs = OTP.objects.filter(
            type=otp_type,
            code=code,
            email=email,
            phone_number=phone_number,
            created__gte=delta_time,
        )

        if otp_objs.exists():
            otp_objs.delete()

            if register:
                user_obj = UserService.create(email=email, phone_number=phone_number)
            else:
                user_obj = UserService.detail(email=email, phone_number=phone_number)

            return user_obj

        return None


# TODO: add this functionality to background tasks
class EmailService:
    @classmethod
    def send_code(cls, code: str, email: str) -> None:
        print(f'code ({code}) sent to email ({email})')

    @classmethod
    def send_transaction_factor(cls, email: str) -> None:
        print(f'transaction sent to email ({email})')


# TODO: add this functionality to background tasks
class SMSService:
    @classmethod
    def send_code(cls, code: str, phone_number: int) -> None:
        print(f'code ({code}) sent to phone_number ({phone_number})')

    @classmethod
    def send_transaction_factor(cls, phone_number: int) -> None:
        print(f'transaction sent to phone_number ({phone_number})')
