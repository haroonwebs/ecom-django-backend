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
        prodcuts=Product.objects.all()
        serializer= ProductSerializer(prodcuts, many=True)
        return Response({
            'message':'Products Fetched',
            'data': serializer.data
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
        product=Product.objects.get(pk=pk)
        if product is not None:
            serializer=ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    'message':'Product updated Successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'message':'Product Not Found'
        }, status=status.HTTP_404_NOT_FOUND)