from django.db import models


# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    isCurrentUser = models.BooleanField()
    score = models.IntegerField()
    def __str__(self):
        return self.name

class Words(models.Model):
    word = models.CharField(max_length=200)
    wasprocessed = models.BooleanField()
    userid = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    def __str__(self):
        return self.word

class WordsGuessed(models.Model):
    wordid = models.IntegerField(default=0)
    letter = models.CharField(max_length=1)
    guessed = models.BooleanField()
    def __str__(self):
        return self.wordid