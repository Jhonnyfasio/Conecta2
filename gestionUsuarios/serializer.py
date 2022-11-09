from rest_framework import serializers
from api.models import CardPost as Card, Category, User, Like, Save

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'