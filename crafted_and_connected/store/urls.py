from django.urls import path

from crafted_and_connected.store import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/latest-posts/', views.latest_posts, name='latest_posts'),
    path('register/', views.register, name='register')

]
