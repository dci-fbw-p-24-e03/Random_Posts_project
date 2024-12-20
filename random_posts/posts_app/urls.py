from django.urls import path
from .views import UsersListView,HomePageView,PostsListView,UserDetailView,PostDetailView,UserPostsView,UserRagisterView,PostCreateView,UserLoginView,UserLogoutView,UserUpdateView,UpdatePostView,PostDeleteView,CustomUserDeleteView,ErrorPage
urlpatterns = [
    path("",HomePageView.as_view(),name="home"),
    path('users/',UsersListView.as_view(),name="users-list"), 
    path("posts/",PostsListView.as_view(),name="posts-list"),
    path("users/<slug:username>/",UserDetailView.as_view(),name="user-details"),
    path("posts/<int:pk>/",PostDetailView.as_view(),name="post-details"),
    path("users/<slug:username>/posts/",UserPostsView.as_view(),name="user-posts"),
    path('register/',UserRagisterView.as_view(),name='register'),
    path('posts/new/',PostCreateView.as_view(),name='new-post'),
    path("login/",UserLoginView.as_view(),name="login"),
    path("logout/",UserLogoutView.as_view(),name="logout"),
    path("users/<slug:username>/update/",UserUpdateView.as_view(),name="user-update"),
    path('users/<slug:username>/delete/', CustomUserDeleteView.as_view(), name='delete-account'),
    path("posts/<int:pk>/update/",UpdatePostView.as_view(),name="post-update"),
    path('posts/<int:pk>/delete/',PostDeleteView.as_view(),name="post-delete"),
    path("error/",ErrorPage.as_view(),name="error_page")
]