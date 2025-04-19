from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    TransactionListView,
    TransactionCreateView, ProductListView,
    ProductDetailView,product_restock,
    stock_api  # Make sure to import the new view


    

)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('new/', ProductCreateView.as_view(), name='product-create'),
    path('products/', ProductListView.as_view(), name='product-list'),
   
   # Update all other product URLs to include products/ prefix
   path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
   path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
   path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
   path('products/new/', ProductCreateView.as_view(), name='product-create'),
    # Transaction URLs
    path('transaction/', TransactionListView.as_view(), name='transaction-list'),
    path('transaction/new/', TransactionCreateView.as_view(), name='transaction-create'),
    path('products/<int:pk>/restock/', product_restock, name='product-restock'),

    path('api/stock/<int:product_id>/', stock_api, name='stock-api'),  # API endpoint
]