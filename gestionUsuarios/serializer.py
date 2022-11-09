from rest_framework import serializers
from api.models import CardPost as Card, Category, User, Like, Save

class userSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fiels = '__all__'