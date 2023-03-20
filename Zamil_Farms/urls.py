"""Zamil_Farms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from product import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('user/', include('user.urls')),
    path('product/', include('product.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('payments/', include('django_pesapal.urls')),
    path('blog/', include('blog.urls')),
    path('account/', include('password_reset.urls')),
    path('verification/', include('verify_email.urls')),

    path('tinymce/', include('tinymce.urls')),
    #start of cart
    path('cart/add/<str:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<str:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<str:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<str:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
    # end of cart
    path('', include('admin_volt.urls')),

    # start of user accounts
    # path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    # path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'),
    #      name='password_reset'),
    # path('password-reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),
    #      name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
    #      name='password_reset_confirm'),
    # path('password-reset-complete/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
    #      name='password_reset_complete'),
    # end of user accounts
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
