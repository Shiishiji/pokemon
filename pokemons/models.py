from django.db import models
from django.contrib.auth.models import AbstractUser
import random

# Create your models here.


class Trainer(AbstractUser):
    level = models.IntegerField(default=1)

    def __str__(self):
        return "lvl: {lvl} u:{u}".format(lvl=self.level, u=self.username)


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

    number = models.CharField(max_length=4)
    owner = models.ForeignKey(Trainer, default=None)
    region = models.ForeignKey(Region)
    types = models.ManyToManyField(Type)
    catch_difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES, default=X)

    # Pokemon Attributes
    level = models.IntegerField(default=1)
    experience = models.BigIntegerField(default=0)

    class Meta:
        abstract = True

    def catch(self, trainer=1, item=1):
        difficulty = {
            'I': 10,
            'II': 8,
            'III': 6,
            'IV': 4,
            'V': 2,
            'X': 0
        }
        rate = difficulty[self.catch_difficulty] * 1 * item * trainer
        result = random.randint(1, 100)
        if result > rate:
            return True
        return False


class Statistics(models.Model):
    pokemon = models.OneToOneField(Pokemon)

    # Pokemon trainings
    attack = models.IntegerField()
    defense = models.IntegerField()
    special_attack = models.IntegerField()
    special_defense = models.IntegerField()
    agility = models.IntegerField()
    health = models.IntegerField()

    def get_all(self):
        return sum(
            self.attack,
            self.defense,
            self.special_attack,
            self.special_defense,
            self.agility,
            self.health
        )

    class Meta:
        abstract = True

    # UPGRADE ABILITIES
    def up_attack(self):
        self.attack += 1
        self.save()

    def up_defense(self):
        self.defense += 1
        self.save()

    def up_special_attack(self):
        self.special_attack += 1
        self.save()

    def up_special_defense(self):
        self.special_defense += 1
        self.save()

    def up_agility(self):
        self.agility += 1
        self.save()

    def up_health(self):
        self.health += 1
        self.save()

    # RETURN ABILITIES
    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_special_attack(self):
        return self.special_attack

    def get_special_defense(self):
        return self.special_defense

    def get_agility(self):
        return self.agility

    def get_health(self):
        return self.health * 5


class Attributes(Statistics):
    pass


class Trainings(Statistics):
    pass