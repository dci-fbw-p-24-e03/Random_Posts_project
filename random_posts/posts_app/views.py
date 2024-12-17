from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import CustomUser,Post
from django.views.generic import ListView,TemplateView,DetailView,CreateView,FormView,RedirectView,UpdateView,DeleteView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from .form import CustomUserCreationForm,PostCreationForm,CustomAuthenticationForm,UserUpdateForm,PasswordConfirmationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden,HttpResponseNotFound

class HomePageView(TemplateView):
    template_name = "posts_app/home.html"

class ErrorPage(TemplateView):
    template_name = "posts_app/error_page.html" 

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
    form_class = CustomAuthenticationForm
    template_name = "posts_app/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self,form):
        if form.cleaned_data.get("username") and form.cleaned_data.get("password"):
            user = form.get_user()
            if user:  # Ensure the user exists
                login(self.request, user)
        else:
            return self.form_invalid(form)  # Treat as invalid if empty data is present
        return super().form_valid(form)
    
    
class UserLogoutView(LoginRequiredMixin,RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        print(self.request.user)
        return super().get(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin,CreateView):
    form_class = PostCreationForm
    template_name="posts_app/create_post.html"

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            "user-details", kwargs={"username": self.object.user.username}
        )
    

class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = "posts_app/profile_update.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user

    
class UpdatePostView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostCreationForm
    template_name = "posts_app/update_post.html"

    def get_success_url(self):
        return reverse_lazy("user-posts",kwargs={"username":self.request.user.username})
    
    def form_valid(self, form):
        print(form.errors)
        form.instance.user=self.request.user
        return super().form_valid(form)


class CustomUserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'posts_app/user_confirm_delete.html'  # Replace with your template path
    success_url = reverse_lazy('home')  # Redirect after successful delete

    def get_object(self, queryset=None):
        # Ensure the user can only delete their own account
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'password_form' not in context:
            context['password_form'] = PasswordConfirmationForm()
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        form = PasswordConfirmationForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']

            # Check if the password matches the user's password
            if user.check_password(password):
                # If password is correct, delete the user and log them out
                user.delete()
                logout(request)
                return redirect(self.success_url)
            else:
                # If password is incorrect, return forbidden
                return HttpResponseForbidden("Password is incorrect.")
        else:
            # If form is invalid, re-render the page with errors
            return self.render_to_response(self.get_context_data(password_form=form))
        
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name ="posts_app/delete_post.html"

    def get_success_url(self):
        return reverse_lazy("user-posts",kwargs={"username":self.object.user.username})