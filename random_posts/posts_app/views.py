from django.shortcuts import render
from .models import CustomUser,Post
from django.views.generic import ListView,TemplateView,DetailView
# Create your views here.
class HomePageView(TemplateView):
    template_name = "posts_app/home.html"

class UsersListView(ListView):
    model = CustomUser
    template_name = "posts_app/users.html"
    context_object_name = "users"#the key name to the template

class PostsListView(ListView):
    model = Post
    template_name ="posts_app/posts.html"
    context_object_name = "posts"


class UserDetailView(DetailView):
    model = CustomUser
    template_name = "posts_app/profile.html"
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

class PostDetailView(DetailView):
    model = Post
    template_name= "posts_app/post_details.html"
    context_object_name = "post"

class UserPostsView(DetailView):
    pass


