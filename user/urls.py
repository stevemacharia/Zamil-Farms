from django.urls import path, include
from . import views

urlpatterns = [
    path("register", views.register_request, name="user_register"),
    path("login", views.login_request, name="user_login"),
    path("reset", views.password_reset, name="reset"),
    path("logout", views.logout_request, name="logouts"),
    path('login_prompt/', views.login_prompt, name='login_prompt'),
    path('profile/', views.profile, name='profile'),
]
