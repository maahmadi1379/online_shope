from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.shopping.services.order import OrderService
from apps.shopping.serializers import (
    ListOrderSerializer,
    DetailMenuSerializer,
    AddUpdateOrderSerializer,
    DeleteOrderSerializer,
)
from apps.utils.pagination import CustomPageNumberPagination


class ListOrderAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        parameters = {}

        action = request.query_params.get('action')
        if action is not None:
            parameters['action'] = action

        orders_objs = OrderService.list()

        paginator = CustomPageNumberPagination()
        paginated_orders_objs = paginator.paginate_queryset(orders_objs, request)

        serializer = ListOrderSerializer(paginated_orders_objs, many=True)

        return paginator.get_paginated_response(serializer.data)


class DetailAddUpdateDeleteOrderAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order_obj = OrderService.detail(order_id=order_id)

        if not order_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.id != order_obj.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = DetailMenuSerializer(instance=order_obj)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, order_id):
        order_obj = OrderService.detail(order_id=order_id)

        if not order_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.id != order_obj.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = AddUpdateOrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        added = OrderService.add(
            order_obj=order_obj,
            quantity=serializer.validated_data.get('quantity'),
            product_obj=serializer.validated_data.get('product_obj'),
        )

        if not added:
            return Response({'detail': 'can not add product to order'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_201_CREATED)

    def put(self, request, order_id):
        order_obj = OrderService.detail(order_id=order_id)

        if not order_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.id != order_obj.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = AddUpdateOrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        updated = OrderService.update(
            order_obj=order_obj,
            quantity=serializer.validated_data.get('quantity'),
            product_obj=serializer.validated_data.get('product_obj'),
        )

        if not updated:
            return Response({'detail': 'can not update product to order'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, order_id):
        order_obj = OrderService.detail(order_id=order_id)

        if not order_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.id != order_obj.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = DeleteOrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        deleted = OrderService.delete(
            order_obj=order_obj,
            product_obj=serializer.validated_data.get('product_obj'),
        )

        if not deleted:
            return Response({'detail': 'can not remove product to order'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class BuyOrderAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order_obj = OrderService.detail(order_id=order_id)

        if not order_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.id != order_obj.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        bought, message = OrderService.buy(
            order_obj=order_obj,
        )

        if not bought:
            return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': message}, status=status.HTTP_201_CREATED)
