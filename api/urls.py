from django.urls import path
from .views import CardPostView


urlpatterns = [
    path('cards/', CardPostView.as_view(), name='get_cards'),
    path('cards/<int:id_user>', CardPostView.as_view(),
         name='get_cards_for_category'),


]
