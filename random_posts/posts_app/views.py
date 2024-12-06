from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from .models import CustomUser,Post
from django.views.generic import ListView,TemplateView,DetailView,CreateView,FormView,RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from .form import CustomUserCreationForm,PostCreationForm
from django.urls import reverse_lazy
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

class UserPostsView(ListView):
    model = Post
    template_name ="posts_app/user_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(CustomUser,username=username)
        return Post.objects.filter(user=user)
    
    def get_context_data(self, **kwargs: Any) :
        context = super().get_context_data(**kwargs)
        print(context)
        username = self.kwargs['username']
        user = get_object_or_404(CustomUser,username=username)
        context['user'] = user
        print('*'*100)
        print(context)
        return context
    

class UserRagisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "posts_app/register.html"
    success_url = reverse_lazy("home")

class UserLoginView(FormView):
    form_class = AuthenticationForm
    template_name = "posts_app/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self,form):
        user = form.get_user()
        login(self.request,user)
        print(self.request)
        return super().form_valid(form)
    
class UserLogoutView(RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        print(self.request.user)
        return super().get(request, *args, **kwargs)


class PostCreateView(CreateView):
    form_class = PostCreationForm
    template_name="posts_app/create_post.html"
    success_url = reverse_lazy("posts-list")
    




