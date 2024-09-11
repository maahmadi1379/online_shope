from typing import Optional, Dict, List

from django.db.models import QuerySet

from apps.shopping.models import Product, City, Category
from apps.shopping.services.order import OrderItemService


class ProductService:
    @classmethod
    def create(cls, price: int, title: str, description: str, cities_objs: List[City], categories_objs: List[Category]):
        product_obj = Product(
            price=price,
            title=title,
            description=description,
            cities=cities_objs,
            categories=categories_objs,
        )

        product_obj.save()
        return product_obj

    @classmethod
    def detail(cls, product_id: int) -> Optional[Product]:
        try:
            product_obj = Product.objects.get(id=product_id, deleted=False)

            return product_obj
        except Product.DoesNotExist as exe:
            return None

    @classmethod
    def list(cls, parameters: Dict) -> QuerySet[Product]:
        if parameters is None:
            parameters = {}

        product_objs = Product.objects.filter(**parameters, deleted=False).order_by('-created')

        return product_objs

    @classmethod
    def delete(cls, product_obj: Product) -> None:
        OrderItemService.delete_with_product(product_obj=product_obj)

        product_obj.deleted = True
        product_obj.save(update_fields=['deleted'])
