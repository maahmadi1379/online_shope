from rest_framework import serializers

from apps.shopping.models import (
    Order,
    OrderItem,
    Address,
    City,
    Category,
    Review,
    Product,
)
from apps.shopping.services.order import OrderItemService
from apps.shopping.services.product import ProductService
from apps.shopping.services.city import CityService, ProductCitiesService
from apps.shopping.services.category import CategoryService, ProductCategoriesService


class AddUpdateOrderSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(required=False, min_value=1, max_value=10)
    product_id = serializers.IntegerField(required=False)

    def validate(self, data):
        valid_data = {}

        quantity = data.get('quantity', None)
        if quantity is None:
            raise serializers.ValidationError(f'"quantity" is Required')
        valid_data['quantity'] = quantity

        product_id = data.get('product_id', None)
        if product_id is None:
            raise serializers.ValidationError(f'"product_id" is Required')
        product_obj = ProductService.detail(product_id=product_id)
        if not product_obj:
            raise serializers.ValidationError(f'"product_id" Not Found')
        valid_data['product_obj'] = product_obj

        return valid_data


class DeleteOrderSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=False)

    def validate(self, data):
        valid_data = {}

        product_id = data.get('product_id', None)
        if product_id is None:
            raise serializers.ValidationError(f'"product_id" is Required')
        product_obj = ProductService.detail(product_id=product_id)
        if not product_obj:
            raise serializers.ValidationError(f'"product_id" Not Found')
        valid_data['product_obj'] = product_obj

        return valid_data


class ListOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'bought',
            'reminded',
            'created',
        )


class DetailOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'bought',
            'reminded',
            'created',
            'order_items',
        )

    def get_order_items(self, instance):
        order_items_objs = OrderItemService.list({'order': instance}).order_by('-created')
        order_items = ListOrderItemSerializer(order_items_objs, many=True).data
        return order_items


class ListOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'id',
            'user',
            'order',
            'product',
            'quantity',
            'price',
            'created',
        )


class CreateAddressSerializer(serializers.Serializer):
    text = serializers.IntegerField(required=True)
    city_id = serializers.IntegerField(required=False)

    def validate(self, data):
        valid_data = {
            'text': data['text'],
        }

        city_id = data.get('city_id', None)
        if city_id is None:
            raise serializers.ValidationError(f'"city_id" is Required')
        city_obj = CityService.detail(city_id=city_id)
        if not city_obj:
            raise serializers.ValidationError(f'"city_id" Not Found')
        valid_data['city_obj'] = city_obj

        return valid_data


class UpdateAddressSerializer(serializers.Serializer):
    text = serializers.IntegerField(required=False)
    city_id = serializers.IntegerField(required=False)
    is_current = serializers.BooleanField(required=False)

    def validate(self, data):
        valid_data = {
            'text': data['text'],
            'is_current': data['is_current'],
        }

        city_id = data.get('city_id', None)
        if city_id is None:
            raise serializers.ValidationError(f'"city_id" is Required')
        city_obj = CityService.detail(city_id=city_id)
        if not city_obj:
            raise serializers.ValidationError(f'"city_id" Not Found')
        valid_data['city_obj'] = city_obj

        return valid_data


class ListAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'id',
            'user',
            'city',
            'text',
            'is_current',
            'created',
        )


class DetailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'id',
            'user',
            'city',
            'text',
            'is_current',
            'created',
        )


class CreateCitySerializer(serializers.Serializer):
    name = serializers.IntegerField(required=True)


class UpdateCitySerializer(serializers.Serializer):
    name = serializers.IntegerField(required=False)


class ListCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id',
            'name',
            'created',
        )


class DetailCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id',
            'name',
            'created',
        )


class CreateCategorySerializer(serializers.Serializer):
    name = serializers.IntegerField(required=True)


class UpdateCategorySerializer(serializers.Serializer):
    name = serializers.IntegerField(required=False)


class ListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'created',
        )


class DetailCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'created',
        )


class AddReviewSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(required=False, min_value=1, max_value=5)

    def validate(self, data):
        valid_data = {}

        rating = data.get('rating', None)
        description = data.get('description', None)

        if description is None and rating is None:
            raise serializers.ValidationError(f'"rating" or "description" is required')

        if rating is not None:
            valid_data['rating'] = rating

        if description is not None:
            valid_data['description'] = description

        product_id = data.get('product_id', None)
        if product_id is None:
            raise serializers.ValidationError(f'"product_id" is Required')
        product_obj = ProductService.detail(product_id=product_id)
        if not product_obj:
            raise serializers.ValidationError(f'"product_id" Not Found')
        valid_data['product_obj'] = product_obj

        return valid_data


class ListReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'user',
            'product',
            'rating',
            'description',
            'created',
        )


class CreateProductSerializer(serializers.Serializer):
    price = serializers.IntegerField(required=True, min_value=0)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    cities = serializers.ListField(
        required=False,
        child=serializers.IntegerField(),
    )
    categories = serializers.ListField(
        required=False,
        child=serializers.IntegerField(),
    )

    def validate(self, data):
        valid_data = {
            'price': data['price'],
            'title': data['title'],
        }

        description = data.get('description', None)
        if description is not None:
            valid_data['description'] = description

        cities = list(set(data.get('cities', [])))
        cities_objs = CityService.list({'id__in': cities})

        if len(cities) != cities_objs.count():
            raise serializers.ValidationError('cities Invalid')

        valid_data['cities_objs'] = cities_objs

        categories = list(set(data.get('categories', [])))
        categories_objs = CategoryService.list({'id__in': categories})

        if len(categories) != categories_objs.count():
            raise serializers.ValidationError('categories Invalid')

        valid_data['categories_objs'] = categories_objs

        return valid_data


class QueryParamsListProductSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    city_id = serializers.IntegerField(required=False)
    category = serializers.IntegerField(required=False)

    def validate(self, data):
        valid_data = {}

        search = data.get('search', None)
        if search is not None:
            valid_data['search'] = search

        city_id = data.get('city_id', None)
        if city_id is not None:
            city_obj = CityService.detail(city_id=city_id)
            if not city_obj:
                raise serializers.ValidationError(f'"city_id" Not Found')
            valid_data['city_obj'] = city_obj

        category_id = data.get('category_id', None)
        if category_id is not None:
            category_obj = CategoryService.detail(category_id=category_id)
            if not category_obj:
                raise serializers.ValidationError(f'"category_id" Not Found')
            valid_data['category_obj'] = category_obj

        return valid_data


class ListProductSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'price',
            'title',
            'description',
            'cities',
            'categories',
            'created',
        )

    def get_cities(self, instance):
        cities = []

        product_cities_objs = ProductCitiesService.list({'product': instance})

        for product_city_obj in product_cities_objs:
            cities.append(DetailCitySerializer(instance=product_city_obj.city).data)

        return cities

    def get_categories(self, instance):
        categories = []

        product_categories_objs = ProductCategoriesService.list({'product': instance})

        for product_category_obj in product_categories_objs:
            categories.append(DetailCategorySerializer(instance=product_category_obj.category).data)

        return categories


class DetailProductSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'price',
            'title',
            'description',
            'cities',
            'categories',
            'created',
        )

    def get_cities(self, instance):
        cities = []

        product_cities_objs = ProductCitiesService.list({'product': instance})

        for product_city_obj in product_cities_objs:
            cities.append(DetailCitySerializer(instance=product_city_obj.city).data)

        return cities

    def get_categories(self, instance):
        categories = []

        product_categories_objs = ProductCategoriesService.list({'product': instance})

        for product_category_obj in product_categories_objs:
            categories.append(DetailCategorySerializer(instance=product_category_obj.category).data)

        return categories
