from typing import Optional, Dict

from django.db.models import QuerySet

from apps.shopping.models import City, ProductCities


class CityService:
    @classmethod
    def create(cls, name: str) -> City:
        city_obj = City.objects.create(
            name=name,
        )

        return city_obj

    @classmethod
    def detail(cls, city_id: int) -> Optional[City]:
        try:
            city_obj = City.objects.get(id=city_id)

            return city_obj
        except City.DoesNotExist as exe:
            return None

    @classmethod
    def list(cls, parameters: Dict = None) -> QuerySet[City]:
        if parameters is None:
            parameters = {}

        cities_objs = City.objects.filter(**parameters).order_by('-created')

        return cities_objs

    @classmethod
    def update(cls, *, city_obj: City, name: str = None) -> City:
        update_fields = []

        if name is not None:
            city_obj.name = name
            update_fields.append('name')

        city_obj.save(update_fields=update_fields)

        return city_obj

    @classmethod
    def delete(cls, city_obj: City) -> None:
        city_obj.delete()


class ProductCitiesService:
    @classmethod
    def list(cls, parameters: Dict = None) -> QuerySet[ProductCities]:
        if parameters is None:
            parameters = {}

        product_cities_objs = ProductCities.objects.filter(**parameters)

        return product_cities_objs
