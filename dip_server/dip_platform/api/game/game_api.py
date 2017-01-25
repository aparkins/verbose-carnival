from dip_platform.api.generic_view import GenericView
from dip_platform.logic.game import game_logic
from dip_platform.management.game import game_management
from dip_platform.management.game import player_management


class GameView(GenericView):
    def handle_get(self, request, game_id):
        game = game_management.get_game_by_id(game_id)

        payload = {
            'id': game['id'],
        }

        if game['current_turn'] != 0:
            payload.update(_get_game_details(game['id']))

        status = 200
        headers = dict()
        return status, payload, headers


def _get_game_details(game):
    game_players = player_management.get_players_for_game(game['id'])
    player_units = {
        player['id']: player_management.get_units_for_player(player['id'])
        for player in game_players
    }
    player_territories = {
        player['id']: player_management.get_territories_for_player(player['id'])
        for player in game_players
    }

    return {
        'currentTurn': game_logic.get_turn_data(game['current_turn']),
        'players': [{
            'id': player['id'],
            'name': player['name'],

            'units': [{
                  'id': unit['id'],
                  'type': unit['type'],
                  'territoryName': unit['territory_name'],
             } for unit in player_units[player['id']]],

            'ownedTerritories': [{
                 'id': owned_territory['id'],
                 'territoryName': owned_territory['territory_name']
            } for owned_territory in player_territories[player['id']]]

        } for player in game_players]
    }
