from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializer import CartItemSerializer

from project.renderers import DataRenderer
from .models import Cart, CartItem
from products.models import Product

# Create your views here.

class AddToCartView(APIView):
    renderer_classes=[DataRenderer]
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

        if quantity > product.stock:
            return Response(
                {"error": "Not enough stock available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if cart_item.quantity + quantity > product.stock:
            return Response(
                {"error": "Stock limit exceeded"},
                status=status.HTTP_400_BAD_REQUEST
            )    

        cart_item.save()

        return Response(
            {"message": "Item added to cart"},
            status=status.HTTP_200_OK
        ) 



# remove items from the cart       

class RemoveItemFromCart(APIView):
    renderer_classes=[DataRenderer]
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


class ListCartItems(APIView):
    renderer_classes=[DataRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart is Empty"},
                status=status.HTTP_404_NOT_FOUND
            )
         
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)

        return Response({
                'message':'Product updated Successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)