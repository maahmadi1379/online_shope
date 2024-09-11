from typing import Optional, Dict, List, Tuple

from django.db.models import QuerySet, Sum

from apps.users.models import User
from apps.shopping.models import (
    Order,
    Product,
    OrderItem,
    ProductCategories,
)
from apps.shopping.services.address import AddressService


class OrderService:
    @classmethod
    def create(cls, user_obj: User) -> Order:
        order_obj = Order.objects.create(user=user_obj)

        return order_obj

    @classmethod
    def get_current_user_order(cls, user_obj: User) -> Optional[Order]:
        order_objs = Order.objects.filter(
            user=user_obj,
            bought=False,
        ).order_by('-created')

        if order_objs.exists():
            return order_objs.first()

        return None

    @classmethod
    def detail(cls, order_id: int, bought: bool = False) -> Optional[Order]:
        try:
            order_obj = Order.objects.get(id=order_id, bought=bought)

            return order_obj
        except Order.DoesNotExist as exe:
            return None

    @classmethod
    def list(cls, include_parameters: Dict = None, exclude_parameters: Dict = None) -> QuerySet[Order]:
        if include_parameters is None:
            include_parameters = {}

        if exclude_parameters is None:
            exclude_parameters = {}

        orders_objs = Order.objects.exclude(**exclude_parameters).filter(**include_parameters).order_by('-created')

        return orders_objs

    @classmethod
    def add(cls, order_obj: Order, product_obj: Product, quantity: int) -> bool:
        order_item_obj = OrderItemService.add(order_obj=order_obj, product_obj=product_obj, quantity=quantity)

        if not order_item_obj:
            return False

        order_obj.reminded = False
        order_obj.save(update_fields=['reminded'])

        return True

    @classmethod
    def update(cls, order_obj: Order, product_obj: Product, quantity: int) -> bool:
        order_item_obj = OrderItemService.update(order_obj=order_obj, product_obj=product_obj, quantity=quantity)

        if not order_item_obj:
            return False

        order_obj.reminded = False
        order_obj.save(update_fields=['reminded'])

        return True

    @classmethod
    def delete(cls, order_obj: Order, product_obj: Product) -> bool:
        order_item_obj = OrderItemService.delete(order_obj=order_obj, product_obj=product_obj)

        if order_item_obj is None:
            return False

        order_obj.reminded = False
        order_obj.save(update_fields=['reminded'])

        return True

    @classmethod
    def buy(cls, order_obj: Order) -> Tuple[bool, str]:
        address_obj = AddressService.get_current_address(order_obj.user)
        if address_obj is None:
            return False, 'address is required, please set this.'

        quantity_sum = OrderItemService.get_count_of_other_products(order_obj=order_obj)
        if quantity_sum == 0:
            return False, 'can not buy any product'

        city_ids = OrderItemService.get_product_city_ids(order_obj=order_obj)
        if address_obj.city not in city_ids:
            return False, 'no matching city of order with products cities'

        order_obj.bought = True
        order_obj.reminded = True
        order_obj.save(update_fields=['bought', 'reminded'])

        order_obj = OrderService.create(order_obj.user)

        return True, 'successfully bought'


class OrderItemService:
    @classmethod
    def create(cls, order_obj: Order, product_obj: Product, quantity: int) -> OrderItem:
        price = int(quantity * product_obj.price)

        order_item_obj = OrderItem.objects.create(
            user=order_obj.user,
            order=order_obj,
            product=product_obj,
            quantity=quantity,
            price=price,
        )

        return order_item_obj

    @classmethod
    def get_count_of_other_products(cls, order_obj: Order, product_obj: Product = None) -> int:
        exclude_parameters = {}
        if product_obj is not None:
            exclude_parameters = {'product': product_obj}

        other_quantity_sum = OrderItem.objects.exclude(
            **exclude_parameters,
        ).filter(
            order=order_obj,
        ).aggregate(
            sum=Sum('quantity')
        )['quantity']

        other_quantity_sum = 0 if other_quantity_sum is None else other_quantity_sum

        return other_quantity_sum

    @classmethod
    def detail(cls, order_obj: Order, product_obj: Product) -> Optional[OrderItem]:
        try:
            order_item_obj = OrderItem.objects.get(order=order_obj, product=product_obj)

            return order_item_obj
        except OrderItem.DoesNotExist as exe:
            return None

    @classmethod
    def list(cls, include_parameters: Dict = None, exclude_parameters: Dict = None) -> QuerySet[OrderItem]:
        if include_parameters is None:
            include_parameters = {}

        if exclude_parameters is None:
            exclude_parameters = {}

        order_items = OrderItem.objects.exclude(**exclude_parameters).filter(**include_parameters).order_by('-created')

        return order_items

    @classmethod
    def add(cls, order_obj: Order, product_obj: Product, quantity: int) -> bool:
        order_item_obj = cls.detail(order_obj=order_obj, product_obj=product_obj)

        if order_item_obj is not None:
            return False

        other_quantity_sum = cls.get_count_of_other_products(order_obj=order_obj, product_obj=product_obj)

        if (other_quantity_sum + quantity) > 10:
            return False

        order_item_obj = cls.create(order_obj=order_obj, product_obj=product_obj, quantity=quantity)

        return True

    @classmethod
    def update(cls, order_obj: Order, product_obj: Product, quantity: int) -> bool:
        order_item_obj = cls.detail(order_obj=order_obj, product_obj=product_obj)

        if order_item_obj is None:
            return False

        other_quantity_sum = cls.get_count_of_other_products(order_obj=order_obj, product_obj=product_obj)

        if (other_quantity_sum + quantity) > 10:
            return False

        price = int(quantity * product_obj.price)

        order_item_obj.quantity = quantity
        order_item_obj.price = price
        order_item_obj.save()

        return True

    @classmethod
    def delete(cls, order_obj: Order, product_obj: Product) -> bool:
        order_item_obj = cls.detail(order_obj=order_obj, product_obj=product_obj)

        if order_item_obj is None:
            return False

        order_item_obj.delete()

        return True

    @classmethod
    def delete_with_product(cls, product_obj: Product) -> None:
        OrderItem.objects.filter(product=product_obj).delete()

    @classmethod
    def get_product_city_ids(cls, order_obj: Order) -> List[int]:
        product_ids = list(
            OrderItem.objects.filter(
                order=order_obj
            ).values_list('product_id', flat=True).distinct()
        )

        city_ids = list(
            ProductCategories.objects.filter(
                product_id__in=product_ids
            ).values_list('city_id', flat=True).distinct()
        )

        return city_ids
