from pydip.map.map import OwnershipMap
from pydip.map.predefined import vanilla_dip
from pydip.turn import adjustment, resolve, retreat

from dip_platform.constants.enums import TurnPhase, TurnSeason
from dip_platform.logic.game.resolution import transform_logic


def resolve_turn(state):
    phase = TurnPhase(state['turn']['phase'])

    if phase == TurnPhase.MOVEMENT:
        return resolve_move(state['players'])

    if phase == TurnPhase.RETREAT:
        return resolve_retreat(state['players'], state['turn'])

    if phase == TurnPhase.ADJUSTMENT:
        return resolve_adjustment(state['players'], state['turn'])

    raise ValueError


def resolve_move(player_state):
    game_map = vanilla_dip.generate_map()
    commands = transform_logic.build_pydip_movement_commands(game_map, player_state)

    retreats = resolve.resolve_turn(game_map, commands)
    return transform_logic.destructure_pydip_movement_results(retreats)


def resolve_retreat(player_state, turn):
    owned_territories = transform_logic.build_owned_territories(player_state)
    ownership_map = OwnershipMap(
        vanilla_dip.generate_supply_center_map(),
        owned_territories,
        vanilla_dip.generate_home_territories(),
    )
    game_map = ownership_map.supply_map.game_map

    retreat_map = transform_logic.build_pydip_retreat_map(game_map, player_state)
    commands = transform_logic.build_pydip_retreat_commands(game_map, retreat_map, player_state)

    player_units = retreat.resolve_retreats(retreat_map, commands)
    adjustment_counts = None
    if TurnSeason(turn['season']) == TurnSeason.FALL:
        ownership_map, adjustment_counts = adjustment.calculate_adjustments(ownership_map, player_units)

    return transform_logic.destructure_pydip_retreat_results(player_units, ownership_map, adjustment_counts)


def resolve_adjustment(player_state, turn):
    owned_territories = transform_logic.build_owned_territories(player_state)
    ownership_map = OwnershipMap(
        vanilla_dip.generate_supply_center_map(),
        owned_territories,
        vanilla_dip.generate_home_territories(),
    )

    player_units = transform_logic.build_pydip_player_units(player_state)
    _, adjustment_counts = adjustment.calculate_adjustments(ownership_map, player_units)
    commands = transform_logic.build_pydip_adjustment_commands(ownership_map, player_state)

    new_player_units = adjustment.resolve_adjustment__validated(
        ownership_map,
        adjustment_counts,
        player_units,
        commands,
    )

    return transform_logic.destructure_pydip_adjustment_results(new_player_units)
