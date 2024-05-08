from django.urls import path
from crafted_and_connected.authentication.views import CustomUserRegistrationView, CustomLoginView, profile, logout_view

urlpatterns = [
    path('register/', CustomUserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
]
