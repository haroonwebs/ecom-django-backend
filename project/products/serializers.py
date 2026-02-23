from rest_framework import serializers
from .models import Product
from categories.models import Category




class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',   
        queryset=Category.objects.all()
    )
    class Meta:
        model=Product
        fields='__all__'
