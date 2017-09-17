from dip_platform.api.generic_view import GenericView
from dip_platform.logic.game.transform_logic import transform_player, transform_command
from pydip.map.predefined import vanilla_dip
from pydip.turn.resolve import resolve_turn


class AdjudicateView(GenericView):
    def handle_put(self, request, data):
        """
        data:
        {
            players: [
                {
                    name: Russia
                    commands: [{convoy, move, etc}]
                    territories: [Munich]
                    units: [{type: Army, territory: Munich}]
                }
            ]
            turn: {
                year: 1907
                phase: move
                season: Fall
            }
        }

        """

        game_map = vanilla_dip.generate_map()
        player_map = {
            player['name'] :
            transform_player(player['name'], game_map, player['units'])
            for player in data['players']
        }
        unit_map = {
            unit.position : unit
            for player in player_map.values()
            for unit in player.units
        }
        commands = [
            transform_command(player_map[player['name']], unit_map, command)
            for player in data['players']
            for command in player['commands']
        ]

        retreats = resolve_turn(game_map, commands)
        payload = {
            player : {
                unit.position : {
                    "type"     : unit.unit_type.value,
                    "retreats" : list(retreat) if retreat is not None else None
                }
                for unit, retreat in unit_retreats.items()
            }
            for player, unit_retreats in retreats.items()
        }


        status = 200
        headers = dict()
        return status, payload, headers
