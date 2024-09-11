from typing import Optional

from apps.users.models import User


class UserService:
    @classmethod
    def create(cls, email: str = None, phone_number: int = None) -> User:
        if email is None and phone_number is None:
            raise ValueError('Either email or phone_number must be provided.')

        if email is not None and phone_number is None:
            username = email
        elif phone_number is not None and email is None:
            username = str(phone_number)
        else:
            raise ValueError('Either email and phone_number must not be provided together.')

        user_obj = User.objects.create(
            username=username,
            password='None',
            email=email,
            phone_number=phone_number,
        )
        user_obj.password = None
        user_obj.save()

        return user_obj

    @classmethod
    def detail(cls, email: str = None, phone_number: int = None) -> Optional[User]:
        user_objs = User.objects.filter(
            email=email,
            phone_number=phone_number,
        )

        if user_objs.exists():
            return user_objs.first()

        return None
