from django.urls import path, include
from .views import ProductListView
from . import views

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    # path('', views.index, name='index'),
    path('AboutUs/', views.AboutUs, name='AboutUs'),
    path('visitormessage/', views.VisitorMessages, name='VisitorMessage'),
]
