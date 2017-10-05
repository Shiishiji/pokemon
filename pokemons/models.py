from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
import random

# Create your models here.


class Trainer(AbstractUser):
    level = models.IntegerField(default=1)
    cash = models.BigIntegerField(default=5)

    def __str__(self):
        return "lvl: {lvl} u:{u}".format(lvl=self.level, u=self.username)

    def change_cash(self, cash_amount):
        self.cash += cash_amount
        self.save()

    class Meta:
        verbose_name = _('trainer')
        verbose_name_plural = _('trainers')


class Item(models.Model):
    pass


class Type(models.Model):
    name = models.CharField(max_length=25)

    # FOR LATER WHEN DOING FIGHTING SYSTEM
    # effective = 2  # super efektywnosc
    # resistant = 0.5  # odpornosc
    # not_effective = 0.5  # mala efektywnosc
    # vulnerability = 2  # podatnosc
    # immune = 0  # nietykalnosc
    # no_effect = 0  # brak efektu

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

    def change_owner(self, new_owner):
        self.owner = new_owner
        self.save()


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
    def_increases = {
        'attack': 1,
        'defense': 1,
        'special_attack': 1,
        'special_defense': 1,
        'agility': 1,
        'health': 5,
    }

    def up_all(self, increases=def_increases):
        counter = 0
        for x, y in increases:
            for i in range(y):
                if counter == 0:
                    self.up_attack()
                elif counter == 1:
                    self.up_defense()
                elif counter == 2:
                    self.up_special_attack()
                elif counter == 3:
                    self.up_special_defense()
                elif counter == 4:
                    self.up_agility()
                elif counter == 5:
                    self.up_health()


class Trainings(Statistics):

    # TRAIN x NUMBER OF TIMES
    def train_attack(self, times=1):
        for i in range(times):
            self.up_attack()

    def train_defense(self, times=1):
        for i in range(times):
            self.up_defense()

    def train_special_attack(self, times=1):
        for i in range(times):
            self.up_special_attack()

    def train_special_defense(self, times=1):
        for i in range(times):
            self.up_special_defense()

    def train_agility(self, times=1):
        for i in range(times):
            self.up_agility()

    def train_health(self, times=1):
        for i in range(times):
            self.up_health()
