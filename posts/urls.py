from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.comment_create_and_list_view, name='all_posts'),
    path('create_post/', views.post_create, name='post_create'),
    path('liked/', views.like_unlike_post, name='like-post-view'),
    # delete page doesnt show
    path('<pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('<pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('<pk>/detail/', views.PostDetail.as_view(), name='single'),
    path('friends_posts/', views.friends_posts, name='friends_posts'),
]