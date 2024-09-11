from typing import Optional, Dict

from django.db.models import QuerySet

from apps.shopping.models import Category, ProductCategories


class CategoryService:
    @classmethod
    def create(cls, name: str) -> Category:
        category_obj = Category.objects.create(
            name=name,
        )

        return category_obj

    @classmethod
    def detail(cls, category_id: int) -> Optional[Category]:
        try:
            category_obj = Category.objects.get(id=category_id)

            return category_obj
        except Category.DoesNotExist as exe:
            return None

    @classmethod
    def list(cls, parameters: Dict = None) -> QuerySet[Category]:
        if parameters is None:
            parameters = {}

        categories_objs = Category.objects.filter(**parameters).order_by('-created')

        return categories_objs

    @classmethod
    def update(cls, *, category_obj: Category, name: str = None) -> Category:
        update_fields = []

        if name is not None:
            category_obj.name = name
            update_fields.append('name')

        category_obj.save(update_fields=update_fields)

        return category_obj

    @classmethod
    def delete(cls, category_obj: Category) -> None:
        category_obj.delete()


class ProductCategoriesService:
    @classmethod
    def list(cls, parameters: Dict = None) -> QuerySet[ProductCategories]:
        if parameters is None:
            parameters = {}

        product_categories_objs = ProductCategories.objects.filter(**parameters)

        return product_categories_objs
