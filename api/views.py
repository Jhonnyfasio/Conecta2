from unicodedata import category
from django.http.response import JsonResponse
from django.db.models import Count, Q, F
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User as UserD
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from api.serializer import UserSerializers, LikeSerializer, SaveSerializer
from .models import CardPost, Category, FriendRequest, StatusFriendRequest, User, Like, Save
import json

# Create your views here.

#///

#@api_view(['GET'])
@api_view(['POST'])
def login(request):
    print("ni")
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        #user = UserD.objects.get(username="pedrome")
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response("Usuario inválido")
    
    pwd_valid = check_password(password,user.password)
    if(not pwd_valid):
        return Response("Contraseña inválida")

    token, create = Token.objects.get_or_create(user=user)
    print(token.key)
    return Response(token.key)
#///

class CardPostViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializers
    queryset = UserSerializers.Meta.model.objects.all()

    def create(self, request):
        try:
            card = json.loads(request.body)

            user = User.objects.get(id=card['id_user'])

            category = Category.objects.get(id=card['id_category'])

            CardPost.objects.create(
                content=card['content'], user=user, category=category)
            data = {'message': "Success"}
            return JsonResponse(data)
        except KeyError:
            print(KeyError)

class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = LikeSerializer.Meta.model.objects.all()

    def create(self, request):
        dataLike = json.loads(request.body)
        user = User.objects.get(id=dataLike['id_user'])
        card = CardPost.objects.get(id=dataLike['id_card'])
        like = Like.objects.filter(
            card_id=card, user_id=user).values_list('id', flat=True)
        data = {'message': 'Sin datos'}
        print(len(like))
        if len(like) == 1:
            newLike = Like.objects.get(id=like[0])
            #print(like[0])
            newLike.status = dataLike['status']
            print(newLike)
            newLike.save()
            data = {'message': 'Success Update'}
        else:
            Like.objects.create(
                status=dataLike['status'], card=card, user=user)
            data = {'message': "Success Create"}
        return JsonResponse(data)

class SaveViewSet(viewsets.ModelViewSet):
    serializer_class = SaveSerializer
    queryset = SaveSerializer.Meta.model.objects.all()

    def create(self, request):
        dataLike = json.loads(request.body)
        user = User.objects.get(id=dataLike['id_user'])
        card = CardPost.objects.get(id=dataLike['id_card'])
        save = Save.objects.filter(
            card_id=card, user_id=user).values_list('id', flat=True)
        data = {'message': 'Sin datos'}
        if len(save) == 1:
            newSave = Save.objects.get(id=save[0])
            newSave.status = dataLike['status']
            newSave.save()
            print(newSave)
            data = {'message': 'Success Update'}
        else:
            Save.objects.create(
                status=dataLike['status'], card=card, user=user)
            data = {'message': "Success Create"}

        return JsonResponse(data)

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id' : user.pk,
            'token': token.key,
        })

class CardPostView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    
    def get(self, request, id_user):
        user = User.objects.get(id=id_user)
        cards = list(CardPost.objects.exclude(user_id=user).annotate(isLike=Count(
            'like_card', filter=Q(like_card__status=True, like_card__user_id=user), distinct=True)).annotate(isSave=Count(
                'save_card', filter=Q(save_card__status=True, save_card__user_id=user), distinct=True)).annotate(countLike=Count(
                    'like_card', filter=Q(like_card__status=True), distinct=True)).order_by('?').values('id', 'user_id__name', 'user_id__image', 'content', 'category_id', 'user_id', 'isLike', 'isSave', 'countLike'))
        if len(cards) > 0:
            data = {'cards': cards}
        else:
            data = {'message': 'Cards not found...'}
        return JsonResponse(data)

    def post(self, request):
        try:
            card = json.loads(request.body)

            user = User.objects.get(id=card['id_user'])

            category = Category.objects.get(id=card['id_category'])

            CardPost.objects.create(
                content=card['content'], user=user, category=category)
            data = {'message': "Success"}
            return JsonResponse(data)
        except KeyError:
            print(KeyError)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class UserView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id_user, id_user_stalker):
        cards = list()
        newUser = list()
        friends_result = list()

        user = User.objects.get(id=id_user)

        userStalker = User.objects.get(id=id_user_stalker)
        statusRequest = list(FriendRequest.objects.filter((Q(user_s_id=userStalker) & Q(
            user_r_id=user)) | (Q(user_s_id=user) & Q(user_r_id=userStalker))).values('status'))
        accepted = StatusFriendRequest.objects.get(id=2)

        friends_one = list(FriendRequest.objects.filter(
            user_s_id=user).filter(status_id=accepted).annotate(idUser=F('user_r__id'), name=F('user_r__name'), username=F('user_r__username'), email=F('user_r__email'), english_level_id=F('user_r__english_level_id'), id_firebase=F('user_r__id_firebase'), image=F('user_r__image')).values('idUser', 'id', 'name', 'username', 'email', 'english_level_id', 'id_firebase', 'image'))

        friends_two = list(FriendRequest.objects.filter(
            user_r_id=user).filter(status_id=accepted).annotate(idUser=F('user_s__id'), name=F('user_s__name'), username=F('user_s__username'), email=F('user_s__email'), english_level_id=F('user_s__english_level_id'), id_firebase=F('user_s__id_firebase'), image=F('user_s__image')).values('idUser', 'id', 'name', 'username', 'email', 'english_level_id', 'id_firebase', 'image'))
        friends_result = friends_one + friends_two
        cards = list(CardPost.objects.filter(
            user_id=user).values('id', 'content', 'category_id'))
        newUser = list(User.objects.filter(pk=id_user).annotate(idUser=F('id')).values(
            'idUser', 'id', 'name', 'username', 'email', 'english_level_id', 'id_firebase', 'image'))
        if len(statusRequest) == 0:
            statusRequest = 0
        else:
            statusRequest = statusRequest[0]['status']
        data = {'user': newUser[0], 'status': statusRequest,
                'cards': cards, 'friends': friends_result}
        return JsonResponse(data)

    def post(self, request):
        user = json.loads(request.body)

        User.objects.create(
            name=user['name'], english_level_id=user['id_english_level'])
        data = {'message': "Success"}

        return JsonResponse(data)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class LikeView(View):
    @ method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id_user, id_category):
        user = User.objects.get(id=id_user)
        category = Category.objects.get(id=id_category)
        cards = list(CardPost.objects.exclude(user_id=user).filter(category_id=category).annotate(isLike=Count(
            'like_card', filter=Q(like_card__status=True, like_card__user_id=user))).filter(isLike=1).values('id', 'user_id__name', 'content', 'category_id', 'user_id', 'isLike'))

        if len(cards) > 0:
            data = {'message': 'SUCCESS', 'cards': cards}
        else:
            data = {'message': 'NO FOUND'}
        return JsonResponse(data)

    def post(self, request):
        dataLike = json.loads(request.body)
        user = User.objects.get(id=dataLike['id_user'])
        card = CardPost.objects.get(id=dataLike['id_card'])
        like = Like.objects.filter(
            card_id=card, user_id=user).values_list('id', flat=True)
        data = {'message': 'Sin datos'}
        print(len(like))
        if len(like) == 1:
            newLike = Like.objects.get(id=like[0])
            #print(like[0])
            newLike.status = dataLike['status']
            print(newLike)
            newLike.save()
            data = {'message': 'Success Update'}
        else:
            Like.objects.create(
                status=dataLike['status'], card=card, user=user)
            data = {'message': "Success Create"}
        return JsonResponse(data)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class SaveView(View):
    @ method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id_user, id_category):
        user = User.objects.get(id=id_user)
        category = Category.objects.get(id=id_category)
        cards = list(CardPost.objects.exclude(user_id=user).filter(category_id=category).annotate(isSave=Count(
            'save_card', filter=Q(save_card__status=True, save_card__user_id=user))).filter(isSave=1).values('id', 'user_id__name', 'content', 'category_id', 'user_id', 'isSave'))
        if len(cards) > 0:
            data = {'message': 'SUCCESS', 'cards': cards}
        else:
            data = {'message': 'NO FOUND'}
        return JsonResponse(data)

    def post(self, request):
        dataLike = json.loads(request.body)
        user = User.objects.get(id=dataLike['id_user'])
        card = CardPost.objects.get(id=dataLike['id_card'])
        save = Save.objects.filter(
            card_id=card, user_id=user).values_list('id', flat=True)
        data = {'message': 'Sin datos'}
        if len(save) == 1:
            newSave = Save.objects.get(id=save[0])
            newSave.status = dataLike['status']
            newSave.save()
            print(newSave)
            data = {'message': 'Success Update'}
        else:
            Save.objects.create(
                status=dataLike['status'], card=card, user=user)
            data = {'message': "Success Create"}

        return JsonResponse(data)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class FriendView(View):
    @ method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id_user):
        user = User.objects.get(id=id_user)
        cards = list(User.objects.exclude(user_id=user).filter(category_id=category).annotate(isSave=Count(
            'save_card', filter=Q(save_card__status=True, save_card__user_id=user))).filter(isSave=1).values('id', 'user_id__name', 'content', 'category_id', 'user_id', 'isSave'))

        if len(cards) > 0:
            data = {'message': 'SUCCESS', 'cards': cards}
        else:
            data = {'message': 'NO FOUND'}
        return JsonResponse(data)

    def post(self, request):
        dataLike = json.loads(request.body)
        user = User.objects.get(id=dataLike['id_user'])
        card = CardPost.objects.get(id=dataLike['id_card'])
        save = Save.objects.filter(
            card_id=card, user_id=user).values_list('id', flat=True)
        data = {'message': 'Sin datos'}
        if len(save) == 1:
            newSave = Save.objects.get(id=save[0])
            newSave.status = dataLike['status']
            newSave.save()
            data = {'message': 'Success Update'}
        else:
            Save.objects.create(
                status=dataLike['status'], card=card, user=user)
            data = {'message': "Success Create"}

        return JsonResponse(data)


class CardsUserView(View):
    def get(self, request, id_user, id_category):
        user = User.objects.get(id=id_user)
        category = Category.objects.get(id=id_category)
        cards = list(CardPost.objects.filter(user_id=user).filter(
            category_id=category).values('id', 'content', 'category_id', 'user_id'))

        if len(cards) > 0:
            data = {'message': 'SUCCESS', 'cards': cards}
        else:
            data = {'message': 'NO FOUND'}
        return JsonResponse(data)


class AllCardsUserView(View):
    def get(self, request, id_user):
        user = User.objects.get(id=id_user)
        cards = list(CardPost.objects.filter(user_id=user).values(
            'id', 'content', 'category_id', 'user_id'))

        if len(cards) > 0:
            data = {'message': 'SUCCESS', 'cards': cards}
        else:
            data = {'message': 'NO FOUND'}
        return JsonResponse(data)


class FriendRequests(View):
    @ method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id_user):
        user = User.objects.get(id=id_user)
        sent = StatusFriendRequest.objects.get(id=1)
        friend_request = list()
        friend_request = list(FriendRequest.objects.filter(
            user_r_id=user).filter(status_id=sent).annotate(idUser=F('user_s__id'), name=F('user_s__name'), username=F('user_s__username'), email=F('user_s__email'), english_level_id=F('user_s__english_level_id'), id_firebase=F('user_s__id_firebase'), image=F('user_s__image')).values('idUser', 'id', 'name', 'username', 'email', 'english_level_id', 'id_firebase', 'image'))
        data = {'friend_request': friend_request}
        return JsonResponse(data)

    def post(self, request):
        data = json.loads(request.body)
        user_s = User.objects.get(id=data['user_s'])

        status = StatusFriendRequest.objects.get(id=data['status'])
        user_r = User.objects.get(id=data['user_r'])

        request = FriendRequest.objects.filter(
            user_s_id=user_s, user_r_id=user_r).values_list('id', flat=True)
        data = {'message': 'Sin datos'}

        if len(request) == 1:
            newRequest = FriendRequest.objects.get(id=request[0])
            newRequest.status = status
            newRequest.save()
            data = {'message': 'Success Update'}
        else:
            FriendRequest.objects.create(
                status=status, user_s=user_s, user_r=user_r)
            data = {'message': "Success Create"}

        return JsonResponse(data)
