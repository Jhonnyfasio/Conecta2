from django.db import models
from django.contrib.auth.models import User as UserD
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.utils.timezone import now


# Create your models here.


class EnglishLevel(models.Model):
    tag = models.CharField(max_length=10)


class StatusFriendRequest(models.Model):
    name = models.CharField(max_length=10)


class User(AbstractUser):
    
    name = models.CharField(max_length=1000)
    email = models.EmailField(default='pedromorales2@gmail.com', unique=True)
    username = models.CharField(max_length=100)
    english_level = models.ForeignKey(EnglishLevel, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='user_english_level')
    password = models.SlugField(max_length=170, default="aaa")
    id_firebase = models.CharField(max_length=1000, default="aaa")
    image = models.CharField(max_length=5000, default="aaaa")
    image_up = models.ImageField(null=True, blank=True ,upload_to='images/')
    last_login = models.DateTimeField(auto_now_add=True)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    objects = UserManager()

class FriendRequest(models.Model):
    status = models.ForeignKey(StatusFriendRequest, blank=True, null=True, on_delete=models.CASCADE,
                               related_name='friend_request_status')
    user_s = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                               related_name='user_sends')
    user_r = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                               related_name='user_receives')


class Category(models.Model):
    name = models.CharField(max_length=1000)


class CardPost(models.Model):
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='card_user')
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE,
                                 related_name='card_category')


class Like(models.Model):
    status = models.BooleanField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='like_user')
    card = models.ForeignKey(CardPost, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='like_card')


class Save(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='save_user')
    card = models.ForeignKey(CardPost, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='save_card')