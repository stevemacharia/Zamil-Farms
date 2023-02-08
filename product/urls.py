from django.urls import path
from .views import ProductDetailView
from . import views

urlpatterns = [
    path('product/<str:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
