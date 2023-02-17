from django.urls import path, include
from .views import ProductListView, BlogDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='BlogList'),
    path('FullStory/<str:pk>/', BlogDetailView.as_view(), name='blog-detail'),
]