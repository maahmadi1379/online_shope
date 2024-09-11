from typing import Tuple

from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


class TokenService:
    @classmethod
    def generate(cls, user_obj: User) -> Tuple[str, str]:
        refresh = RefreshToken.for_user(user_obj)

        access = str(refresh.access_token)
        refresh = str(refresh)

        return access, refresh
