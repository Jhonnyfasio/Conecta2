from django.urls import path, include
from .views import SuggestionView, Pearson, Recommendation, PearsonRecommendation, SuggestionViewSet
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'suggestionset', SuggestionViewSet, basename="suggestionset")

urlpatterns = [
    path('suggestion/<int:id_user>', SuggestionView.as_view(), name='get_suggestion'),
    path('suggestion/makePearson', Pearson.as_view(), name='make_all_pearson'),
    path('suggestion/makeRecommendation', Recommendation.as_view(), name='make_all_recommendation'),
    path('suggestion/getRecommendation/<int:idUser>', PearsonRecommendation.as_view(), name='get_pearson_recommendation'),
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls))
    #path('cards/', CardPostView.as_view(), name='post_cards'),
    #path('likes/<int:id_user>', LikeView.as_view(), name='get_likes'),
    #path('likes/', LikeView.as_view(), name='post_likes'),
    #path('saves/<int:id_user>', SaveView.as_view(), name='get_saves'),
    #path('saves/', SaveView.as_view(), name='post_saves'),

]
