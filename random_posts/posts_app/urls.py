from django.urls import path
from .views import UsersListView,HomePageView,PostsListView,UserDetailView,PostDetailView,UserPostsView,UserRagisterView,PostCreateView

urlpatterns = [
    path('users/',UsersListView.as_view(),name="users-list"),
    path("",HomePageView.as_view(),name="home"),
    path("posts/",PostsListView.as_view(),name="posts-list"),
    path("users/<slug:username>/",UserDetailView.as_view(),name="user-details"),
    path("posts/<int:pk>/",PostDetailView.as_view(),name="post-details"),
    path("users/<slug:username>/posts/",UserPostsView.as_view(),name="user-posts"),
    path('register/',UserRagisterView.as_view(),name='register'),
    path('posts/new/',PostCreateView.as_view(),name='new-post')
]