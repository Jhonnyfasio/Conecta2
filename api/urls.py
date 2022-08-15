from django.urls import path
from .views import CardPostView, UserView


urlpatterns = [
    path('cards/', CardPostView.as_view(), name='get_cards'),
    path('cards/<int:id_category>', CardPostView.as_view(),
         name='get_cards_for_category'),
    path('users/', UserView.as_view(), name='users_list'),
    path('likes/', UserView.as_view(), name='users_list'),


]
