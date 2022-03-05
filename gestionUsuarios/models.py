from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField()
    name = models.CharField(max_length=50)
    firstLastName = models.CharField(max_length=50)
    secondLastName = models.CharField(max_length=50)
    email = models.EmailField()
    english_level = models.IntegerField()
    created_at = models.TimeField()
    updated_at = models.TimeField()

class Message(models.Model):
    id = models.AutoField()
    message = models.CharField(max_length=1000)
    created_at = models.TimeField()