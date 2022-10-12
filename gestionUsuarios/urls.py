from django.urls import path
from .views import SuggestionView, Pearson, Recommendation, PearsonRecommendation


urlpatterns = [
    path('suggestion/<int:id_user>', SuggestionView.as_view(), name='get_suggestion'),
    path('suggestion/makePearson', Pearson.as_view(), name='make_all_pearson'),
    path('suggestion/makeRecommendation', Recommendation.as_view(), name='make_all_recommendation'),
    path('suggestion/getRecommendation/<int:idUser>', PearsonRecommendation.as_view(), name='get_pearson_recommendation'),
    #path('cards/', CardPostView.as_view(), name='post_cards'),
    #path('likes/<int:id_user>', LikeView.as_view(), name='get_likes'),
    #path('likes/', LikeView.as_view(), name='post_likes'),
    #path('saves/<int:id_user>', SaveView.as_view(), name='get_saves'),
    #path('saves/', SaveView.as_view(), name='post_saves'),

]
