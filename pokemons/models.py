from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Trainer(AbstractUser):
    pass


class Type(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Pokemon(models.Model):

    I = "I"
    II = "II"
    III = "III"
    IV = "IV"
    V = "V"
    X = "X"

    DIFFICULTY_CHOICES = (
        (I, "Very Easy"),
        (II, "Easy"),
        (III, "Difficult"),
        (IV, "Tough"),
        (V, "Hard"),
        (X, "Impossible"),
    )
    owner = models.ForeignKey(Trainer, default=None)
    region = models.ForeignKey(Region)
    types = models.ManyToManyField(Type)
    catch_difficulty = models.CharField(max_length=12, choices=DIFFICULTY_CHOICES, default=X)

    class Meta:
        abstract = True
