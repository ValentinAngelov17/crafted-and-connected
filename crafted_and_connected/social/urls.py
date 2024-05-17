#social urls
from django.urls import path
from .views import add_post, load_subcategories

urlpatterns = [
    path('add_post/', add_post, name='add_post'),
    path('ajax/load_subcategories/', load_subcategories, name='load_subcategories'),
]
