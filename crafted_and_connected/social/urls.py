# social urls
from django.urls import path
from .views import add_post, load_subcategories, post_detail, like_post, add_comment, notifications, \
    mark_notification_as_read, clear_notifications, follow_user, unfollow_user

urlpatterns = [
    path('add_post/', add_post, name='add_post'),
    path('ajax/load_subcategories/', load_subcategories, name='load_subcategories'),
    path('<int:post_id>/', post_detail, name='post_detail'),
    path('<int:post_id>/like/', like_post, name='like_post'),
    path('<int:post_id>/comment/', add_comment, name='add_comment'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', mark_notification_as_read,
         name='mark_notification_as_read'),
    path('clear_notifications/', clear_notifications, name='clear_notifications'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
]
