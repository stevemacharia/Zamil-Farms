from django.urls import path, include
from . import views

urlpatterns = [
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login1"),
    path("logout", views.logout_request, name="logout"),
    path('login_prompt/', views.login_prompt, name='login_prompt'),
    path('profile/', views.profile, name='profile'),
]
