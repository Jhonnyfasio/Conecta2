from django.urls import path
from .views import CardPostView, FriendView, LikeView, SaveView, CardsUserView, AllCardsUserView, UserView, FriendRequests
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
     path('cards/<int:id_user>', CardPostView.as_view(), name='get_cards'),
     path('cards/', CardPostView.as_view(), name='post_cards'),
     path('users/<int:id_user>/<int:id_user_stalker>',
         UserView.as_view(), name='get_cards'),
     path('friends/', FriendView.as_view(), name='friends'),
     path('likes/<int:id_user>/<int:id_category>',
         LikeView.as_view(), name='get_likes'),
     path('likes/', LikeView.as_view(), name='post_likes'),
     path('saves/<int:id_user>/<int:id_category>',
         SaveView.as_view(), name='get_saves_category'),
     path('saves/', SaveView.as_view(), name='post_saves'),
     path('create_card/<int:id_user>/<int:id_category>',
         CardsUserView.as_view(), name='get_cards_create_category'),
     path('all_create_card/<int:id_user>',
         AllCardsUserView.as_view(), name='get_all_cards_create'),
     path('friend_requests/<int:id_user>',
         FriendRequests.as_view(), name='get_friend_requests'),
     path('friend_requests/',
         FriendRequests.as_view(), name='post_friend_requests'),
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += path('login',views.login),