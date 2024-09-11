from typing import Optional

from apps.users.models import User
from apps.shopping.models import Order


class OrderService:
    @classmethod
    def create(cls, user: User) -> Order:
        order_obj = Order.objects.create(user=user)

        return order_obj

    @classmethod
    def get_current_order(cls, user_obj: User) -> Optional[Order]:
        order_objs = Order.objects.filter(
            user=user_obj,
            bought=False,
        )

        if order_objs.exists():
            return order_objs.first()

        return None
