from django.urls import path
from .views import CardPostView, LikeView, SaveView


urlpatterns = [
    path('cards/<int:id_user>', CardPostView.as_view(), name='get_cards'),
    path('cards/', CardPostView.as_view(), name='post_cards'),
    path('likes/<int:id_user>', LikeView.as_view(), name='get_likes'),
    path('likes/', LikeView.as_view(), name='post_likes'),
    path('saves/<int:id_user>', SaveView.as_view(), name='get_saves'),
    path('saves/<int:id_user>/<int:id_category>',
         SaveView.as_view(), name='get_saves_category'),
    path('saves/', SaveView.as_view(), name='post_saves'),

]
