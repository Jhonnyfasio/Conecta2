from unicodedata import category
from django.http.response import JsonResponse
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import CardPost, Category, User, Like, Save
import json

# Create your views here.


class CardPostView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id_user):
        user = User.objects.get(id=id_user)
        cards = list(CardPost.objects.annotate(isLike=Count(
            'like_card', filter=Q(like_card__status=True, like_card__user_id=user))).annotate(isSave=Count(
                'save_card', filter=Q(save_card__status=True, save_card__user_id=user))).annotate(countLike=Count(
                    'like_card', filter=Q(like_card__status=True))).values('id', 'user_id__name', 'content', 'category_id', 'user_id', 'isLike', 'isSave', 'countLike'))

        if len(cards) > 0:
            data = {'cards': cards}
        else:
            data = {'message': 'Cards not found...'}
        return JsonResponse(data)

    def post(self, request):
        card = json.loads(request.body)
        user = User.objects.get(id=card['id_user'])
        category = Category.objects.get(id=card['id_category'])
        CardPost.objects.create(
            content=card['content'], user=user, category=category)
        data = {'message': "Success"}

        return JsonResponse(data)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class UserView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        users = list(User.objects.values())
        if len(users) > 0:
            data = {'message': 'Success', 'users': users}
        else:
            data = {'message': 'users not found...'}
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
    @method_decorator(csrf_exempt)
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

        if len(like) == 1:
            newLike = Like.objects.get(id=like[0])
            newLike.status = dataLike['status']
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
    @method_decorator(csrf_exempt)
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

    def put(self, request):
        pass

    def delete(self, request):
        pass


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
