from unicodedata import category
from django.http.response import JsonResponse
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import CardPost, Category, User, Like
import json

# Create your views here.


class CardPostView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id_user):
        user = User.objects.get(id=id_user)
        cards = list(CardPost.objects.annotate(isLike=Count(
            'like_card', filter=Q(like_card__status=True, like_card__user_id=user))).annotate(countLike=Count(
                'like_card', filter=Q(like_card__status=True, like_card__card_id=id))).values())

        if len(cards) > 0:
            data = {'message': 'Success', 'cards': cards}
        else:
            data = {'message': 'Cards not found...'}
        return JsonResponse(data)

    def post(self, request):
        card = json.loads(request.body)
        user = User.objects.get(id=card['id_user'])
        category = Category.objects.get(id=card['id_category'])
        CardPost.objects.create(
            content=card['content'], user_id=user, category_id=category)
        data = {'message': "Success"}

        return JsonResponse(data)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class UserView(View):
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
    def get(self, request, id_user):
        cards = list(Like.objects.filter(user_id=id_user,
                                         status=True).values())

        if len(cards) > 0:
            data = {'message': 'Success', 'cards': cards}
        else:
            data = {'message': 'Cards not found...'}
        return JsonResponse(data)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass
