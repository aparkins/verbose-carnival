from dip_platform.api.generic_view import GenericView
from dip_platform.logic.game import game_logic
from dip_platform.management.game import game_management
from dip_platform.management.game import player_management


class GameView(GenericView):
    def handle_get(self, request, game_id):
        game = game_management.get_game_by_id(game_id)
        game_players = player_management.get_players_for_game(game_id)
        player_units = {
            player['id']: player_management.get_units_for_player(player['id'])
            for player in game_players
        }
        player_territories = {
            player['id']: player_management.get_territories_for_player(player['id'])
            for player in game_players
        }

        status = 200
        payload = {
            'id': game['id'],
            'currentTurn': game_logic.get_readable_turn(game['current_turn']),
            'players': [{
                'id':   player['id'],
                'name': player['name'],

                'units': [{
                    'id':            unit['id'],
                    'type':          unit['type'],
                    'territoryName': unit['territory_name'],
                } for unit in player_units[player['id']] ],

                'ownedTerritories': [{
                    'id':            owned_territory['id'],
                    'territoryName': owned_territory['territory_name']
                } for owned_territory in player_territories[player['id']] ]

            } for player in game_players ]
        }
        headers = dict()
        return status, payload, headers
