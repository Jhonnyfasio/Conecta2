from django.http.response import JsonResponse

from django.views import View

from .models import CardPost, User, Like
from rest_framework import status
from rest_framework.response import Response
import json

# Create your views here.


class CardPostView(View):

    def get(self, request):
        cards = list(CardPost.objects.values())
        if len(cards) > 0:
            data = {'message': 'Successw', 'cards': cards}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'message': 'Cards not found...'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id_category):
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
