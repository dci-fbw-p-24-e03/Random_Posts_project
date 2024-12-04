from django.urls import path
from .views import UsersListView,HomePageView,PostsListView


urlpatterns = [
    path('users/',UsersListView.as_view(),name="users-list"),
    path("",HomePageView.as_view(),name="home"),
    path("posts/",PostsListView.as_view(),name="posts-list")
]