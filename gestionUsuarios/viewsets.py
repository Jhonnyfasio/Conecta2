from rest_framework import viewsets
from .serializer import userSerializers
from api.models import CardPost as Card, Category, User, Like, Save

class userviewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializers