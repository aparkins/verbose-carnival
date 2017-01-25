from django.db import models


class Game(models.Model):
    # SETTINGS! :D

    current_turn = models.IntegerField(default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'current_turn': self.current_turn,
        }


class User(models.Model):
    username = models.CharField(max_length=32)
    email = models.CharField(max_length=32)

    def to_dict(self):
        return {
            'id':       self.id,
            'username': self.username,
            'email':    self.email,
        }


class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32)

    def to_dict(self):
        return {
            'id':      self.id,
            'game_id': self.game_id,
            'user_id': self.user_id,
            'name':    self.name,
        }


class Unit(models.Model):
    UNIT_TYPE_CHOICES = (
        ('T', 'TROOP'),
        ('F', 'FLEET'),
    )

    owner = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=1, choices=UNIT_TYPE_CHOICES)
    territory_name = models.CharField(max_length=32)

    def readable_type(self):
        for type, readable_type in self.UNIT_TYPE_CHOICES:
            if type == self.type:
                return readable_type
        raise ValueError('Unit with invalid type={}'.format(self.type))

    def to_dict(self):
        return {
            'id':             self.id,
            'owner_id':       self.owner_id,
            'type':           self.readable_type(),
            'territory_name': self.territory_name,
        }


class TerritoryOwnership(models.Model):
    owner = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    territory_name = models.CharField(max_length=32)

    def to_dict(self):
        return {
            'id':             self.id,
            'owner_id':       self.owner_id,
            'territory_name': self.territory_name,
        }
