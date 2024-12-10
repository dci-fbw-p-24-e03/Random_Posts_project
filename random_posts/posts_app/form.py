from django import forms
from .models import CustomUser,Post
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.forms import AuthenticationForm


SEX_CHOICES = [
        ("M","Male"),
        ("F","Female")
    ]

class CustomUserCreationForm(UserCreationForm):
    sex = forms.ChoiceField(choices=SEX_CHOICES,widget=forms.RadioSelect())
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False 
    class Meta:
        model = CustomUser
        fields = ("username","first_name","last_name","email","password1","password2","bio","sex","phone_number","age")
        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "Enter your username", "class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Enter your email", "class": "form-control"}
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "placeholder": "Enter your phone number",
                    "class": "form-control",
                }
            ),
            "age": forms.NumberInput(
                attrs={"placeholder": "Enter your age", "class": "form-control"}
            ),
            "password1": forms.PasswordInput(
                attrs={"placeholder": "Enter your password", "class": "form-control"}
            ),
            "password2": forms.PasswordInput(
                attrs={"placeholder": "Confirm your password", "class": "form-control"}
            ),
        }
        help_texts = {
            'username': '',  # Remove the help text for username
            'password1':None,
            'password2':None
        }


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('visibility','categories','content','image')

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  

class UserUpdateForm(UserChangeForm):
    
    sex = forms.ChoiceField(choices=SEX_CHOICES,widget=forms.RadioSelect())
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name","email","age","sex","phone_number","bio"]


class SearchForm(forms.Form):
    category = forms.CharField()
    user = forms.CharField()