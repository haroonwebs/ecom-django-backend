from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from project.renderers import DataRenderer
from rest_framework.permissions import IsAdminUser

# get all products view
class ProductListView(APIView):
    renderer_classes=[DataRenderer]
    def get(self, request, format=None):
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('per_page', 10))

        start = (page - 1) * limit
        end = start + limit
        products=Product.objects.all().order_by('-created_at')[start:end]

        serializer= ProductSerializer(products, many=True)

        total_products = Product.objects.count()
        total_pages = (total_products + limit - 1) // limit  
        return Response({
            'message':'Products Fetched',
            'data': serializer.data,
            "total_pages": total_pages,
            "current_page": page
        }, status=status.HTTP_200_OK)


# create new project view        
class CreateProductView(APIView):
    permission_classes=[IsAdminUser]
    renderer_classes=[DataRenderer]
    def post(self, request, format=None):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'message':'Product created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# update product view    
class UpdateProductView(APIView):
    def patch(self, request, pk ,format=None):
        try:
            product=Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer=ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'message':'Product updated Successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# get single product view    
class GetSingleProductView(APIView):
    renderer_classes=[DataRenderer]
    def get(self, request, pk ,format=None):
        product=''
        try:
            product=Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer=ProductSerializer(product)
        return Response({
            'message':'Product fetched Successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)   
    

# delete product
class DeleteProductView(APIView):
    renderer_classes=[DataRenderer]
    def delete(self, request, pk ,format=None):
        try:
            product=Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer=ProductSerializer(product)
        product.delete()
        return Response({
            'message':'Product deleted Successfully',
        }, status=status.HTTP_200_OK)   