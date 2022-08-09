from django.http.response import JsonResponse
from django.views import View
from .models import CardPost

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
