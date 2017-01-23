import pytest

from dip_platform.logic.game import game_logic


def test__get_readable_turn__negative_is_error():
    with pytest.raises(AssertionError):
        game_logic.get_readable_turn(-1)


@pytest.mark.parametrize(
    [ 'turn_number', 'expected' ],
    [
        (  0, 'Registration'),
        (  1, 'Spring 1901'),
        (  2, 'Spring 1901 (Retreat)'),
        (  3, 'Fall 1901'),
        (  4, 'Fall 1901 (Retreat)'),
        (  5, 'Fall 1901 (Adjustment)'),
        (  6, 'Spring 1902'),
        (  7, 'Spring 1902 (Retreat)'),
        (  8, 'Fall 1902'),
        (  9, 'Fall 1902 (Retreat)'),
        ( 10, 'Fall 1902 (Adjustment)'),
        (100, 'Fall 1920 (Adjustment)'),
        (156, 'Spring 1932'),
        (257, 'Spring 1952 (Retreat)'),
        (445, 'Fall 1989 (Adjustment)'),
    ],
)
def test__get_readable_turn__valid_turns(turn_number, expected):
    assert game_logic.get_readable_turn(turn_number) == expected
