from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.shopping.serializers import (
    ListOrderSerializer,
    DetailOrderSerializer,
    AddUpdateOrderSerializer,
    DeleteOrderSerializer,

    CreateAddressSerializer,
    DetailAddressSerializer,
    ListAddressSerializer,
    UpdateAddressSerializer,

    CreateCitySerializer,
    DetailCitySerializer,
    ListCitySerializer,
    UpdateCitySerializer,

    CreateCategorySerializer,
    DetailCategorySerializer,
    ListCategorySerializer,
    UpdateCategorySerializer,

    AddReviewSerializer,
    ListReviewSerializer,

    CreateProductSerializer,
    DetailProductSerializer,
    ListProductSerializer,
    QueryParamsListProductSerializer,
)
from apps.shopping.services.city import CityService
from apps.shopping.services.order import OrderService
from apps.shopping.services.review import ReviewService
from apps.shopping.services.product import ProductService
from apps.shopping.services.address import AddressService
from apps.shopping.services.category import CategoryService
from apps.utils.pagination import CustomPageNumberPagination


class ListOrderAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
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

        serializer = DetailOrderSerializer(instance=order_obj)

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


class CreateListAddressAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateAddressSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        address_obj = AddressService.create(
            user_obj=request.user,
            city_obj=serializer.validated_data.get('city_obj'),
            text=serializer.validated_data.get('text'),
        )

        serializer = DetailAddressSerializer(instance=address_obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        parameters = {'user': request.user}

        addresses_objs = AddressService.list(parameters=parameters)

        paginator = CustomPageNumberPagination()
        paginated_addresses_objs = paginator.paginate_queryset(addresses_objs, request)

        serializer = ListAddressSerializer(paginated_addresses_objs, many=True)

        return paginator.get_paginated_response(serializer.data)


class UpdateDeleteAddressAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, address_id):
        address_obj = AddressService.detail(address_id=address_id)

        if not address_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateAddressSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        address_obj = AddressService.update(
            address_obj=address_obj,
            text=serializer.validated_data.get('text'),
            city_obj=serializer.validated_data.get('city_obj'),
            is_current=serializer.validated_data.get('is_current'),
        )

        serializer = DetailAddressSerializer(instance=address_obj)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, address_id):
        address_obj = AddressService.detail(address_id=address_id)

        if not address_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        AddressService.delete(address_obj=address_obj)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CreateListCityAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permission() for permission in self.permission_classes]
        return []  # No permissions required for GET method

    def post(self, request):
        serializer = CreateCitySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        city_obj = CityService.create(
            name=serializer.validated_data.get('name'),
        )

        serializer = DetailCitySerializer(instance=city_obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        cities_objs = CityService.list()

        paginator = CustomPageNumberPagination()
        paginated_cities_objs = paginator.paginate_queryset(cities_objs, request)

        serializer = ListCitySerializer(paginated_cities_objs, many=True)

        return paginator.get_paginated_response(serializer.data)


class UpdateDeleteCityAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, city_id):
        city_obj = CityService.detail(city_id=city_id)

        if not city_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateCitySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        city_obj = CityService.update(
            city_obj=city_obj,
            name=serializer.validated_data.get('name'),
        )

        serializer = DetailCitySerializer(instance=city_obj)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, city_id):
        city_obj = CityService.detail(city_id=city_id)

        if not city_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        CityService.delete(city_obj=city_obj)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CreateListCategoryAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permission() for permission in self.permission_classes]
        return []  # No permissions required for GET method

    def post(self, request):
        serializer = CreateCategorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        category_obj = CategoryService.create(
            name=serializer.validated_data.get('name'),
        )

        serializer = DetailCategorySerializer(instance=category_obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        categories_objs = CategoryService.list()

        paginator = CustomPageNumberPagination()
        paginated_categories_objs = paginator.paginate_queryset(categories_objs, request)

        serializer = ListCategorySerializer(paginated_categories_objs, many=True)

        return paginator.get_paginated_response(serializer.data)


class UpdateDeleteCategoryAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, category_id):
        category_obj = CategoryService.detail(category_id=category_id)

        if not category_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateCategorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        category_obj = CategoryService.update(
            category_obj=category_obj,
            name=serializer.validated_data.get('name'),
        )

        serializer = DetailCategorySerializer(instance=category_obj)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, category_id):
        category_obj = CategoryService.detail(category_id=category_id)

        if not category_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        CategoryService.delete(category_obj=category_obj)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class AddListReviewAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permission() for permission in self.permission_classes]
        return []  # No permissions required for GET method

    def post(self, request):
        serializer = AddReviewSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        review_obj = ReviewService.add(
            user_obj=request.user,
            product_obj=serializer.validated_data.get('product_obj'),
            rating=serializer.validated_data.get('rating', 0),
            description=serializer.validated_data.get('description', ''),
        )

        return Response({}, status=status.HTTP_201_CREATED)

    def get(self, request):
        reviews_objs = ReviewService.list()

        paginator = CustomPageNumberPagination()
        paginated_reviews_objs = paginator.paginate_queryset(reviews_objs, request)

        serializer = ListReviewSerializer(paginated_reviews_objs, many=True)

        return paginator.get_paginated_response(serializer.data)


class CreateListProductAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permission() for permission in self.permission_classes]
        return []  # No permissions required for GET method

    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_obj = ProductService.create(
            price=serializer.validated_data.get('price'),
            title=serializer.validated_data.get('title'),
            description=serializer.validated_data.get('description'),
            cities_objs=serializer.validated_data.get('cities_objs', []),
            categories_objs=serializer.validated_data.get('categories_objs', []),
        )

        serializer = DetailProductSerializer(instance=product_obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        serializer = QueryParamsListProductSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        parameters = {}

        search = serializer.validated_data.get('search', None)
        if search is not None:
            parameters['title__icontains'] = search

        city_obj = serializer.validated_data.get('city_obj', None)
        if city_obj is not None:
            parameters['productcities__city'] = city_obj

        category_obj = serializer.validated_data.get('category_obj', None)
        if category_obj is not None:
            parameters['productcategories__category'] = category_obj

        products_objs = ProductService.list(parameters=parameters)

        paginator = CustomPageNumberPagination()
        paginated_products_objs = paginator.paginate_queryset(products_objs, request)

        serializer = ListProductSerializer(paginated_products_objs, many=True)

        return paginator.get_paginated_response(serializer.data)


class DetailUpdateDeleteProductAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [permission() for permission in self.permission_classes]
        return []  # No permissions required for GET method

    def get(self, request, product_id):
        product_obj = ProductService.detail(product_id=product_id)

        if not product_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DetailProductSerializer(instance=product_obj)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        product_obj = ProductService.detail(product_id=product_id)

        if not product_obj:
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        ProductService.delete(product_obj=product_obj)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
