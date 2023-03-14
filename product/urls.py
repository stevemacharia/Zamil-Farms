from django.urls import path
from .views import ProductDetailView
from . import views

urlpatterns = [
    path('product/<str:pk>/', ProductDetailView.as_view(), name='product-detail'),
    # path('shop/', ProductListView.as_view(), name='shop'),
    path('shop/', views.product_list, name='shop'),
]
