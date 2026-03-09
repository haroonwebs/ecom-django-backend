from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from cart.models import Cart, CartItem
from .models import Order, OrderItem
from project.renderers import DataRenderer


class CreateOrderView(APIView):
    renderer_classes = [DataRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user
        shipping_address = request.data.get("shipping_address")

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response(
                {"error": "Cart has no items"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_price = 0

        # calculate total
        for item in cart_items:
            total_price += item.product.price * item.quantity

        with transaction.atomic():

            # create order
            order = Order.objects.create(
                user=user,
                total_price=total_price,
                shipping_address=shipping_address
            )

            # create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # clear cart
            cart_items.delete()

        return Response(
            {
                "message": "Order placed successfully",
                "order_id": order.id,
                "total_price": total_price
            },
            status=status.HTTP_201_CREATED
        )