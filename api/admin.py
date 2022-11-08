from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CardPost, EnglishLevel, User, Category, Like, Save, StatusFriendRequest, FriendRequest


# Register your models here.

admin.site.register(CardPost)
admin.site.register(User, UserAdmin)
admin.site.register(EnglishLevel)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Save)
admin.site.register(StatusFriendRequest)
admin.site.register(FriendRequest)
