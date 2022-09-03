from django.urls import path
from .views import SuggestionView


urlpatterns = [
    path('suggestion/<int:id_user>', SuggestionView.as_view(), name='get_suggestion'),
    #path('cards/', CardPostView.as_view(), name='post_cards'),
    #path('likes/<int:id_user>', LikeView.as_view(), name='get_likes'),
    #path('likes/', LikeView.as_view(), name='post_likes'),
    #path('saves/<int:id_user>', SaveView.as_view(), name='get_saves'),
    #path('saves/', SaveView.as_view(), name='post_saves'),

]