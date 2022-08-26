from unittest.util import _MAX_LENGTH
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

    def __str__(self):
        return "%s" %(self.name)

class Category(models.Model):
    idCategory = models.IntegerField()
    name = models.CharField(max_length=15)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return "%s" %(self.name)

class Message(models.Model):
    idMessage = models.IntegerField()
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField()

    def __str__(self):
        return "%s" %(self.message)

class Card(models.Model):
    idCard = models.IntegerField()
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    idCategory = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=1000)
    translation = models.CharField(max_length=1000)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return "%s" %(self.idCard)

class Like(models.Model):
    idLike = models.IntegerField()
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    idCard = models.ForeignKey(Card, on_delete=models.CASCADE, null=True)
    #score = models.SmallIntegerField()
    score = models.FloatField()
    created_at = models.DateTimeField()

    def __str__(self):
        return "%s" %(self.score)