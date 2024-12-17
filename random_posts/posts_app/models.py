from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .validators import validate_email,validate_username,validate_no_bad_words,validate_age,validate_post_length
from PIL import Image
import logging

logger= logging.getLogger("posts_app")
class CustomUser(AbstractUser):
    SEX_CHOICES = [
        ("M","Male"),
        ("F","Female")
    ]
    phone_number = models.CharField(max_length=40,blank=True,null=True)
    age = models.PositiveBigIntegerField(blank=True,null=True,validators=[validate_age])
    bio = models.TextField(blank=True,validators=[validate_no_bad_words])
    email=models.EmailField(unique=True,validators=[validate_email])
    sex = models.CharField(choices=SEX_CHOICES,max_length=10)

    def __str__(self) -> str:
        return self.username
    
    def save(self,*args,**kwargs) :
        if self.password and not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        if self.first_name:
            self.first_name = self.first_name.capitalize()
        if self.last_name:
            self.last_name = self.last_name.capitalize()

        logger.info(f"Saving {self.username} with {self.password}")
        super().save(*args,**kwargs)
    

    def clean(self) -> None:
        super().clean()
        validate_username(self.username)

    class Meta:
        ordering = ['username','age']
        db_table = 'random_posts_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Post(models.Model):
    VISIBILITY_CHOICES =[
        ('public','Public'),
        ('private','Private')
    ]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_posts")
    content= models.TextField(validators=[validate_no_bad_words,validate_post_length])
    categories = models.CharField(max_length=100,validators=[validate_no_bad_words])
    visibility = models.CharField(max_length=20,choices=VISIBILITY_CHOICES,default='public')
    created_at=models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="post_image/",blank=True,null=True)
    

    def __str__(self) -> str:
        return f'Post by {self.user.username} on {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
    
    def save(self,*args,**kwargs ) :
        super().save(*args,**kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                img = img.resize((300,300))
                img.save(self.image.path)

    class Meta:
        ordering = ['-created_at']#- for descending order
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        db_table = 'posts'
