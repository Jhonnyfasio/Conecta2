from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import CardPost, User, Like
from rest_framework import status
from rest_framework.response import Response
import json

# Create your views here.


class CardPostView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        cards = list(CardPost.objects.values())
        if len(cards) > 0:
            data = {'message': 'Successw', 'cards': cards}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': 'Cards not found...'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id_category):
        cards = list(CardPost.objects.filter(id_category=id_category).values())

        if len(cards) > 0:
            data = {'message': 'Success', 'cards': cards}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': 'Cards not found...'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
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
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass


class LikeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        likes = list(Like.objects.values())
        if len(likes) > 0:
            data = {'message': 'Success', 'likes': likes}
        else:
            data = {'message': 'likes not found...'}
        return JsonResponse(data)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass
