from rest_framework import serializers

from apps.shopping.models import Order, OrderItem
from apps.shopping.services.order import OrderItemService
from apps.shopping.services.product import ProductService


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
            'address',
            'bought',
            'reminded',
            'created',
        )


class DetailMenuSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'address',
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
