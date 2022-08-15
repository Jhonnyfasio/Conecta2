from django.urls import path
from .views import CardPostView, UserView


urlpatterns = [
    path('cards/', CardPostView.as_view(), name='cards_list'),
    path('users/', UserView.as_view(), name='users_list'),
    path('likes/', UserView.as_view(), name='users_list'),


]
