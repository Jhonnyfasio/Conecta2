from django.urls import path
from .views import CardPostView, LikeView


urlpatterns = [
    path('cards/<int:id_user>', CardPostView.as_view(), name='get_cards'),
    path('cards/', CardPostView.as_view(), name='post_cards'),
    path('likes/', LikeView.as_view(), name='post_likes'),

]
