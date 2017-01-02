from dip_platform import models


def get_players_for_game(game_id):
    return [
        player.to_dict()
        for player in models.Player.objects.filter(game_id=game_id).all()
    ]

def get_units_for_player(player_id):
    return [
        unit.to_dict()
        for unit in models.Unit.objects.filter(owner_id=player_id).all()
    ]

def get_territories_for_player(player_id):
    return [
        unit.to_dict()
        for unit in models.TerritoryOwnership.objects.filter(owner_id=player_id).all()
    ]