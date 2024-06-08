from django.urls import path
from crafted_and_connected.authentication.views import CustomUserRegistrationView, CustomLoginView, profile, \
    logout_view, update_profile, user_profile, follow_user, unfollow_user


urlpatterns = [
    path('register/', CustomUserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/<int:user_id>/', user_profile, name='user_profile'),  # For viewing other user profiles
    path('profile/', profile, name='profile'),  # For viewing the logged-in user's profile
    path('logout/', logout_view, name='logout'),
    path('update_profile/', update_profile, name='update_profile_picture'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
]
