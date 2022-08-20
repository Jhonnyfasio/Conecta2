from django.http.response import JsonResponse
from django.views import View
from .models import CardPost, User, Like

# Create your views here.


class CardPostView(View):
    def get(self, request):
        cards = list(CardPost.objects.values())
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


class UserView(View):
    def get(self, request):
        users = list(User.objects.values())
        if len(users) > 0:
            data = {'message': 'Success', 'users': users}
        else:
            data = {'message': 'users not found...'}
        return JsonResponse(data)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass


class LikeView(View):
    def get(self, request, id_user):
        cards = list(Like.objects.filter(id_user=id_user,
                     status=True).values('status', 'id_card__content'))

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
