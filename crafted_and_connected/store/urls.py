from django.urls import path

from crafted_and_connected.store import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/latest-posts/', views.latest_posts, name='latest_posts'),
    path('register/', views.register, name='register'),
    path('category/<str:category>/', views.category_view, name='category_view'),
    path('category/<str:category>/<str:subcategory>/', views.category_view, name='subcategory_view'),
    path('search/', views.search, name='search'),
]
