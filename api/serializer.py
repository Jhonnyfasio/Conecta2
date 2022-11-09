from rest_framework import serializers
from api.models import CardPost as Card, Category, User, Like, Save

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'

class SaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Save
        fields = '__all__'