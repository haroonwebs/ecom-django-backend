from django.urls import path
from .views import ProductListView, CreateProductView, UpdateProductView, GetSingleProductView, DeleteProductView


urlpatterns=[
    path('products/', ProductListView.as_view(), name='produts'),
    path('create-product/', CreateProductView.as_view(), name='create-product'),
    path('<int:pk>/update/', UpdateProductView.as_view(), name='update-product'),
    path('<int:pk>/', GetSingleProductView.as_view(), name='get-single-product'),
    path('<int:pk>/delete/', DeleteProductView.as_view(), name='delete-product')
]