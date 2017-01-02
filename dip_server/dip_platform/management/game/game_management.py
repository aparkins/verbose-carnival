from dip_platform import models
from dip_platform.management.exceptions import NotFoundError


def get_game_by_id(game_id):
    try:
        orm_game = models.Game.objects.get(id=game_id)
        return orm_game.to_dict()
    except models.Game.DoesNotExist:
        raise NotFoundError('No Game found with id={}'.format(game_id))
