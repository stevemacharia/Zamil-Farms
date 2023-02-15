from django.urls import path
from . import views
from .views import PaymentView
urlpatterns = [
    path('pesapal/', PaymentView.as_view(), name="payment"),
    path('payment_option/', views.payment_option, name='payment_option'),
    path('payment_confirmation/', views.payment_confirmation, name='payment_confirmation'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
]