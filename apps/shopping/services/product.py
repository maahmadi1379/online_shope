from typing import Optional

from apps.shopping.models import Product


class ProductService:
    @classmethod
    def detail(cls, product_id: int) -> Optional[Product]:
        try:
            product_obj = Product.objects.get(id=product_id)

            return product_obj
        except Product.DoesNotExist as exe:
            return None
