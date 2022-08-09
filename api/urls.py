from django.urls import path
from .views import CardPostView
urlpatterns = [
    path('cards/', CardPostView.as_view(), name='cards_list')
]
