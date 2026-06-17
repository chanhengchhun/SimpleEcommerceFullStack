from django.urls import path
from .views import CartView, CartItemView, PlaceOrderView, OrderListView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('item/<int:pk>/', CartItemView.as_view(), name='cart_item_delete'),
    path('checkout/', PlaceOrderView.as_view(), name='checkout'),
    path('orders/', OrderListView.as_view(), name='order_list'),
]
