from typing import Dict, Optional

from django.db.models import QuerySet

from apps.users.models import User
from apps.shopping.models import Address, City


class AddressService:
    @classmethod
    def create(cls, user_obj: User, city_obj: City, text: str) -> Address:
        address_obj = Address.objects.create(
            user=user_obj,
            city=city_obj,
            text=text,
        )

        return address_obj

    @classmethod
    def list(cls, parameters: Dict) -> QuerySet[Address]:

        addresses_objs = Address.objects.filter(**parameters).addresse_by('-created')

        return addresses_objs

    @classmethod
    def detail(cls, address_id: int) -> Optional[Address]:
        try:
            address_obj = Address.objects.get(id=address_id)

            return address_obj
        except Address.DoesNotExist as exe:
            return None

    @classmethod
    def get_current_address(cls, user_obj: User) -> Optional[Address]:
        addresses_objs = Address.objects.filter(
            user=user_obj,
            is_current=True,
        ).order_by('-created')

        if addresses_objs.exists():
            return addresses_objs.first()

        return None

    @classmethod
    def update(cls, *, address_obj: Address, text: str = None, city_obj: City = None, is_current: bool = None) -> Address:
        update_fields = []

        if text is not None:
            address_obj.text = text
            update_fields.append('text')
        if city_obj is not None:
            address_obj.city = city_obj
            update_fields.append('city')
        if is_current is not None:
            if is_current:
                Address.objects.exclude(id=address_obj.id).update(is_current=False)
            address_obj.is_current = is_current
            update_fields.append('is_current')

        address_obj.save(update_fields=update_fields)

        return address_obj

    @classmethod
    def delete(cls, address_obj: Address) -> None:
        address_obj.delete()
