from rest_framework.views import APIView
from .models import Product
from .serializers import ProductListSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class ProductListView(APIView):
    def get(self, request, format=None):
        prodcuts=Product.objects.all()
        serializer= ProductListSerializer(prodcuts, many=True)
        return Response({
            'message':'Products Fetched',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
 