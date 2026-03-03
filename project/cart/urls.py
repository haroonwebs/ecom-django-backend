from django.urls import path
from .views import AddToCartView, RemoveItemFromCart, ListCartItems


urlpatterns = [
    path('add', AddToCartView.as_view(), name='addtocart'),
    path('remove', RemoveItemFromCart.as_view(), name='remove-from-cart'),
    path('', ListCartItems.as_view(), name='cart list')
]