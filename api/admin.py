from django.contrib import admin
from .models import CardPost, User, Category, Like

# Register your models here.

admin.site.register(CardPost)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Like)
