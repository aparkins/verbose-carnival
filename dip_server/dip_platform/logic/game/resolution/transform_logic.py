from pydip.player.player import Player
from pydip.player.command.command import HoldCommand, MoveCommand, SupportCommand, ConvoyTransportCommand, ConvoyMoveCommand

from dip_platform.constants.enums import UnitType


def build_pydip_commands(game_map, player_state):
    player_map = __build_player_map(game_map, player_state)
    unit_map = __build_unit_map(player_map)
    return [
        build_pydip_command(player_map[player['name']], unit_map, command)
        for player in player_state['players']
        for command in player['commands']
        ]


def __build_player_map(game_map, player_state):
    return {
        player['name']: build_pydip_player(player['name'], game_map, player['units'])
        for player in player_state['players']
    }


def __build_unit_map(player_map):
    return {
        unit.position: unit
        for player in player_map.values()
        for unit in player.units
    }


def build_pydip_player(player_name, game_map, player_units):
    """
    game_map -- Map (from PyDip) for the current game
    player_name -- String name of the player we are constructing
    player_units -- [{
        type : TROOP | FLEET
        territory : String
    }]
    """
    starting_configuration = [
        {
            'territory_name' : unit['territory'],
            'unit_type'      : UnitType(unit['type']).to_pydip(),
        }
        for unit in player_units
    ]
    return Player(player_name, game_map, starting_configuration)


def build_pydip_movement_command(player, unit_map, command_data):
    """
    player -- PyDip Player issuing the command
    unit_map -- Territory Name to PyDip Unit object in that territory
    command_data -- {
        type -- Type of command being issued (dictates other parameters)
        territory -- Name of territory being issued command
        [destination] -- (Non-Hold command only) Name of territory the command targets
        [supportedTerritory] -- (Support command only) Name of territory being supported
        [convoyedTerritory] -- (Convoy Transport command only) Name of territory being convoyed
    }
    """
    commanded_unit = unit_map[command_data['territory']]

    if command_data['type'] == "Hold":
        return HoldCommand(
            player,
            commanded_unit,
        )

    if command_data['type'] == "Move":
        return MoveCommand(
            player,
            commanded_unit,
            command_data['destination'],
        )

    if command_data['type'] == "Support":
        supported_unit = unit_map[command_data['supportedTerritory']]
        return SupportCommand(
            player,
            commanded_unit,
            supported_unit,
            command_data['destination'],
        )

    if command_data['type'] == "ConvoyTransport":
        convoyed_unit = unit_map[command_data['convoyedTerritory']]
        return ConvoyTransportCommand(
            player,
            commanded_unit,
            convoyed_unit,
            command_data['destination'],
        )

    if command_data['type'] == "ConvoyMove":
        return ConvoyMoveCommand(
            player,
            commanded_unit,
            command_data['destination'],
        )

    raise ValueError


def destructure_pydip_retreats(retreats):
    result = dict()
    for player, unit_retreats in retreats.items():
        result[player] = dict()

        for unit, retreat in unit_retreats.items():
            if retreat is not None:
                retreat = list(retreat)

            result[player][unit.position] = {
                'type' : UnitType.from_pydip(unit.unit_type),
                'retreats' : retreat,
            }

    return result
