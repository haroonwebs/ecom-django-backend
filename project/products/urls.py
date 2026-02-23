from django.urls import path
from .views import ProductListView, CreateProductView, UpdateProductView


urlpatterns=[
    path('products/', ProductListView.as_view(), name='produts'),
    path('create-product/', CreateProductView.as_view(), name='create-product'),
    path('<int:pk>/update/', UpdateProductView.as_view(), name='update-product')
]