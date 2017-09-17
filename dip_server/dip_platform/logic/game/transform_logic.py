from pydip.player.player import Player
from pydip.player.unit import UnitTypes
from pydip.player.command.command import *


def transform_player(player_name, game_map, player_units):
    """
    game_map -- Map (from PyDip) for the current game
    player_name -- String name of the player we are constructing
    player_units -- [{
        type : TROOP | FLEET
        territory : String
    }]
    """
    starting_configuration = [
        { 'territory_name' : unit['territory'], 'unit_type' : UnitTypes(unit['type']) }
        for unit in player_units
    ]
    return Player(player_name, game_map, starting_configuration)

def transform_command(player, unit_map, command_data):
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
        return HoldCommand(player, commanded_unit)
    if command_data['type'] == "Move":
        return MoveCommand(player, commanded_unit, command_data['destination'])
    if command_data['type'] == "Support":
        supported_unit = unit_map[command_data['supportedTerritory']]
        return SupportCommand(player, commanded_unit, supported_unit, command_data['destination'])
    if command_data['type'] == "ConvoyTransport":
        convoyed_unit = unit_map[command_data['convoyedTerritory']]
        return ConvoyTransportCommand(player, commanded_unit, convoyed_unit, command_data['destination'])
    if command_data['type'] == "ConvoyMove":
        return ConvoyMoveCommand(player, commanded_unit, command_data['destination'])

    raise

