from django.db import models


class Game(models.Model):
    # SETTINGS! :D
    pass

class User(models.Model):
    username = models.CharField(max_length=32)
    email = models.CharField(max_length=32)

class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32)

class Unit(models.Model):
    UNIT_TYPE_CHOICES = (
        ('T', 'TROOP'),
        ('F', 'FLEET'),
    )

    owner = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=1, choices=UNIT_TYPE_CHOICES)
    territory_name = models.CharField(max_length=32)

class TerritoryOwnership(models.Model):
    owner = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    territory_name = models.CharField(max_length=32)
