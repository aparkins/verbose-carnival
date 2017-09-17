from pydip.map.predefined import vanilla_dip
from pydip.turn import resolve

from dip_platform.constants.enums import TurnPhase
from dip_platform.logic.game.resolution import transform_logic


def resolve_turn(state):
    phase = TurnPhase(state['turn']['phase'])

    if phase == TurnPhase.MOVEMENT:
        resolve_move(state['players'])

    if phase == TurnPhase.RETREAT:
        resolve_retreat(state['players'], state['turn'])

    if phase == TurnPhase.ADJUSTMENT:
        resolve_adjustment(state['players'], state['turn'])

    raise ValueError


def resolve_move(player_state):
    game_map = vanilla_dip.generate_map()
    commands = transform_logic.build_pydip_commands(game_map, player_state)

    retreats = resolve.resolve_turn(game_map, commands)
    return transform_logic.destructure_pydip_retreats(retreats)


def resolve_retreat(player_state, turn):
    pass


def resolve_adjustment(player_state, turn):
    pass
