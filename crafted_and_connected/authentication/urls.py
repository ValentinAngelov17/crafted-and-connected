from django.urls import path
from crafted_and_connected.authentication.views import CustomUserRegistrationView, CustomLoginView, profile, \
    logout_view, update_profile_picture
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', CustomUserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('update_profile_picture/', update_profile_picture, name='update_profile_picture'),
]

