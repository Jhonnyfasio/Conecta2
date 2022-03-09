from django.db import models

# Create your models here.

class User(models.Model):
    idUser = models.IntegerField()
    name = models.CharField(max_length=50)
    firstLastName = models.CharField(max_length=50)
    secondLastName = models.CharField(max_length=50)
    email = models.EmailField()
    english_level = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class Message(models.Model):
    idMessage = models.IntegerField()
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField()

class Like(models.Model):
    idLike = models.IntegerField()
    score = models.SmallIntegerField()
    created_at = models.DateTimeField()

class Card(models.Model):
    idCard = models.IntegerField()
    content = models.CharField(max_length=1000)
    translation = models.CharField(max_length=1000)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

