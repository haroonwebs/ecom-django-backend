from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from products.models import Product

# Create your views here.

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id)
        except product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # get or create cart
        cart, created = Cart.objects.get_or_create(user=user)

        # check if item already exists
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return Response(
            {"message": "Item added to cart"},
            status=status.HTTP_200_OK
        ) 



# remove items from the cart       

class RemoveItemFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        product_id = request.data.get("product_id")

        try:
            cart = Cart.objects.get(user=user)
            cart_item = CartItem.objects.get(
                cart=cart,
                product_id=product_id
            )
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not in cart"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        cart_item.delete()

        return Response(
            {"message": "Item removed from cart"},
            status=status.HTTP_200_OK
        )




