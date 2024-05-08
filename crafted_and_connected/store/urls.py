from django.urls import path

from crafted_and_connected.store import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register')

]