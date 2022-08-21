from django.contrib import admin
from .models import CardPost, EnglishLevel, User, Category, Like, Save

# Register your models here.

admin.site.register(CardPost)
admin.site.register(User)
admin.site.register(EnglishLevel)
admin.site.register(Category)
admin.site.register(Like)
admin.site.register(Save)
