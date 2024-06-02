from django.urls import path

from crafted_and_connected.store import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/latest-posts/', views.latest_posts, name='latest_posts'),
    path('register/', views.register, name='register'),
    path('category/<str:category>/', views.category_view, name='category_view'),
    path('category/<str:category>/<str:subcategory>/', views.category_view, name='subcategory_view'),
    path('search/', views.search, name='search'),
    path('add_to_cart/<int:post_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
]
