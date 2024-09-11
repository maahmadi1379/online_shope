from django.urls import path

from apps.shopping.views import (
    ListOrderAPIView,
    DetailAddUpdateDeleteOrderAPIView,
    BuyOrderAPIView,
)

urlpatterns = [
    path('order/', ListOrderAPIView.as_view(), name="create-list-order"),
    path('order/<int:order_id>/', DetailAddUpdateDeleteOrderAPIView.as_view(), name="detail-add-update-delete-order"),
    path('order/<int:order_id>/buy/', BuyOrderAPIView.as_view(), name="buy-order"),
]
