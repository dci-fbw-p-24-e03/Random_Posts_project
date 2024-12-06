from django import forms
from .models import CustomUser,Post
from django.contrib.auth.forms import UserCreationForm

SEX_CHOICES = [
        ("M","Male"),
        ("F","Female")
    ]

class CustomUserCreationForm(UserCreationForm):
    sex = forms.ChoiceField(choices=SEX_CHOICES,widget=forms.RadioSelect())
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


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('user','visibility','categories','content','image')