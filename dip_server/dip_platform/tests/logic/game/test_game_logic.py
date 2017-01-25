import pytest

from dip_platform.logic.game import game_logic


def test__get_turn_data__negative_is_error():
    with pytest.raises(AssertionError):
        game_logic.get_turn_data(-1)


@pytest.mark.parametrize(
    [ 'turn_number', 'expected_year', 'expected_season', 'expected_phase' ],
    [
        (  0, None, None,                     game_logic.PHASE_REGISTRATION),
        (  1, 1901, game_logic.SEASON_SPRING, game_logic.PHASE_MOVEMENT),
        (  2, 1901, game_logic.SEASON_SPRING, game_logic.PHASE_RETREAT),
        (  3, 1901, game_logic.SEASON_FALL,   game_logic.PHASE_MOVEMENT),
        (  4, 1901, game_logic.SEASON_FALL,   game_logic.PHASE_RETREAT),
        (  5, 1901, game_logic.SEASON_FALL,   game_logic.PHASE_ADJUSTMENT),
        (  6, 1902, game_logic.SEASON_SPRING, game_logic.PHASE_MOVEMENT),
        (  7, 1902, game_logic.SEASON_SPRING, game_logic.PHASE_RETREAT),
        (  8, 1902, game_logic.SEASON_FALL,   game_logic.PHASE_MOVEMENT),
        (  9, 1902, game_logic.SEASON_FALL,   game_logic.PHASE_RETREAT),
        ( 10, 1902, game_logic.SEASON_FALL,   game_logic.PHASE_ADJUSTMENT),
        (100, 1920, game_logic.SEASON_FALL,   game_logic.PHASE_ADJUSTMENT),
        (156, 1932, game_logic.SEASON_SPRING, game_logic.PHASE_MOVEMENT),
        (257, 1952, game_logic.SEASON_SPRING, game_logic.PHASE_RETREAT),
        (445, 1989, game_logic.SEASON_FALL,   game_logic.PHASE_ADJUSTMENT),
    ],
)
def test__get_turn_data__valid_turns(turn_number, expected_year, expected_season, expected_phase):
    assert game_logic.get_turn_data(turn_number) == {
        'year'   : expected_year,
        'season' : expected_season,
        'phase'  : expected_phase,
    }
