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


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('user','visibility','categories','content','image')