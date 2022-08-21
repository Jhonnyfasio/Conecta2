from django.urls import path
from .views import CardPostView, LikeView


urlpatterns = [
    path('cards/<int:id_user>', CardPostView.as_view(), name='get_cards'),
    path('likes/<int:id_user>', LikeView.as_view(), name='get_cards_likes'),

]
