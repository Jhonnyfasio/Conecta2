from django.urls import path
from .views import CardPostView, LikeView


urlpatterns = [
    path('cards/', CardPostView.as_view(), name='get_cards'),
    path('cards/<int:id_user>', CardPostView.as_view(),
         name='get_cards_for_category'),
    path('cards/', LikeView.as_view(), name='get_cards_likes'),

]
