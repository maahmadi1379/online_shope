from django.urls import path

from apps.shopping.views import (
    ListOrderAPIView,
    DetailAddUpdateDeleteOrderAPIView,
    BuyOrderAPIView,

    CreateListAddressAPIView,
    UpdateDeleteAddressAPIView,

    CreateListCityAPIView,
    UpdateDeleteCityAPIView,

    CreateListCategoryAPIView,
    UpdateDeleteCategoryAPIView,

    AddListReviewAPIView,
)

urlpatterns = [
    path('order/', ListOrderAPIView.as_view(), name="list-order"),
    path('order/<int:order_id>/', DetailAddUpdateDeleteOrderAPIView.as_view(), name="detail-add-update-delete-order"),
    path('order/<int:order_id>/buy/', BuyOrderAPIView.as_view(), name="buy-order"),

    path('address/', CreateListAddressAPIView.as_view(), name="create-list-address"),
    path('address/<int:address_id>/', UpdateDeleteAddressAPIView.as_view(), name="detail-update-delete-address"),

    path('city/', CreateListCityAPIView.as_view(), name="create-list-city"),
    path('city/<int:city_id>/', UpdateDeleteCityAPIView.as_view(), name="update-delete-city"),

    path('category/', CreateListCategoryAPIView.as_view(), name="create-list-category"),
    path('category/<int:category_id>/', UpdateDeleteCategoryAPIView.as_view(), name="update-delete-category"),

    path('review/', AddListReviewAPIView.as_view(), name="create-list-review"),
]
