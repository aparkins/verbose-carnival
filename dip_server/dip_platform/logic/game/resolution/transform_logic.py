from pydip.player.command.retreat_command import RetreatMoveCommand, RetreatDisbandCommand
from pydip.player.player import Player
from pydip.player.command.command import HoldCommand, MoveCommand, SupportCommand, ConvoyTransportCommand, ConvoyMoveCommand

from dip_platform.constants.enums import UnitType, MovementCommandType, RetreatCommandType


def build_pydip_movement_commands(game_map, player_state):
    player_map = __build_player_map(game_map, player_state)
    unit_map = __build_unit_map(player_map)
    return [
        build_pydip_movement_command(player_map[player['name']], unit_map, command)
        for player in player_state
        for command in player['commands']
    ]


def build_owned_territories(player_state):
    return {
        player['name'] : set(player['territories'])
        for player in player_state
    }


def build_pydip_retreat_map(game_map, player_state):
    player_map = __build_player_map(game_map, player_state)
    unit_map = __build_unit_map(player_map)

    results = dict()
    for player in player_state:
        player_name = player['name']
        results[player_name] = dict()

        for unit_data in player['units']:
            unit = unit_map[unit_data['territory']]
            results[player_name][unit] = unit_data['retreats']

    return results

def build_pydip_retreat_commands(game_map, retreat_map, player_state):
    player_map = __build_player_map(game_map, player_state)
    unit_map = __build_unit_map(player_map)
    return [
        build_pydip_retreat_command(retreat_map, player_map[player['name']], unit_map, command)
        for player in player_state
        for command in player['commands']
    ]


def __build_player_map(game_map, player_state):
    return {
        player['name']: build_pydip_player(player['name'], game_map, player['units'])
        for player in player_state
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
    command_type = MovementCommandType(command_data['type'])

    if command_type == MovementCommandType.HOLD:
        return HoldCommand(
            player,
            commanded_unit,
        )

    if command_type == MovementCommandType.MOVE:
        return MoveCommand(
            player,
            commanded_unit,
            command_data['destination'],
        )

    if command_type == MovementCommandType.SUPPORT:
        supported_unit = unit_map[command_data['supportedTerritory']]
        return SupportCommand(
            player,
            commanded_unit,
            supported_unit,
            command_data['destination'],
        )

    if command_type == MovementCommandType.CONVOY_TRANSPORT:
        convoyed_unit = unit_map[command_data['convoyedTerritory']]
        return ConvoyTransportCommand(
            player,
            commanded_unit,
            convoyed_unit,
            command_data['destination'],
        )

    if command_type == MovementCommandType.CONVOY_MOVE:
        return ConvoyMoveCommand(
            player,
            commanded_unit,
            command_data['destination'],
        )

    raise ValueError


def build_pydip_retreat_command(retreat_map, player, unit_map, command_data):
    """
    retreat_map -- PyDip retreat map (result from movement adjudication)
    player -- PyDip Player issuing the command
    unit_map -- Territory Name to PyDip Unit object in that territory
    command_data -- {
        type -- Type of command being issued (dictates other parameters)
        territory -- Name of territory being issued command
        [destination] -- (Retreat command only) Name of territory retreating to
    }
    """
    commanded_unit = unit_map[command_data['territory']]
    command_type = RetreatCommandType(command_data['type'])

    if command_type == RetreatCommandType.DISBAND:
        return RetreatDisbandCommand(
            retreat_map,
            player,
            commanded_unit,
        )

    if command_type == RetreatCommandType.RETREAT:
        return RetreatMoveCommand(
            retreat_map,
            player,
            commanded_unit,
            command_data['destination'],
        )

    raise ValueError


def destructure_pydip_movement_results(retreats):
    result = dict()
    for player, unit_retreats in retreats.items():
        result[player] = dict()

        result[player]['units'] = dict()
        for unit, retreat in unit_retreats.items():
            if retreat is not None:
                retreat = list(retreat)

            result[player]['units'][unit.position] = {
                'type' : UnitType.from_pydip(unit.unit_type).value,
                'retreats' : retreat,
            }

    return result


def destructure_pydip_retreat_results(player_units, ownership_map, adjustment_counts):
    players = (
        player_units.keys()
      | ownership_map.owned_territories.keys()
      | adjustment_counts.keys()
    )

    result = dict()
    for player in players:
        result[player] = dict()

        result[player]['units'] = dict()
        for unit in player_units.get(player, []):
            result[player]['units'][unit.position] = {
                'type' : UnitType.from_pydip(unit.unit_type).value,
            }

        result[player]['territories'] = list(ownership_map.owned_territories.get(player, set()))

        result[player]['adjustments'] = adjustment_counts.get(player, 0)

    return result
