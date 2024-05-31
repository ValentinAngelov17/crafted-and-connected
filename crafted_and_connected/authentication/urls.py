from django.urls import path
from crafted_and_connected.authentication.views import CustomUserRegistrationView, CustomLoginView, profile, \
    logout_view, update_profile_picture, user_profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', CustomUserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/<int:user_id>/', user_profile, name='user_profile'),  # For viewing other user profiles
    path('profile/', profile, name='profile'),  # For viewing the logged-in user's profile
    path('logout/', logout_view, name='logout'),
    path('update_profile_picture/', update_profile_picture, name='update_profile_picture'),
]

