# social urls
from django.urls import path
from .views import add_post, load_subcategories, post_detail, like_post, add_comment

urlpatterns = [
    path('add_post/', add_post, name='add_post'),
    path('ajax/load_subcategories/', load_subcategories, name='load_subcategories'),
    path('<int:post_id>/', post_detail, name='post_detail'),
    path('<int:post_id>/like/', like_post, name='like_post'),
    path('<int:post_id>/comment/', add_comment, name='add_comment'),
]
