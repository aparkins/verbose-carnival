

SEASON_SPRING = 'spring'
SEASON_FALL   = 'fall'


PHASE_REGISTRATION = 'registration'
PHASE_MOVEMENT     = 'movement'
PHASE_RETREAT      = 'retreat'
PHASE_ADJUSTMENT   = 'adjustment'


def get_turn_data(turn_number):
    assert turn_number >= 0
    if turn_number == 0:
        return {
            'year'   : None,
            'season' : None,
            'phase'  : PHASE_REGISTRATION,
        }

    turn_number -= 1
    season_phase_map = {
        0: (SEASON_SPRING, PHASE_MOVEMENT),
        1: (SEASON_SPRING, PHASE_RETREAT),
        2: (SEASON_FALL,   PHASE_MOVEMENT),
        3: (SEASON_FALL,   PHASE_RETREAT),
        4: (SEASON_FALL,   PHASE_ADJUSTMENT),
    }

    year = 1901 + (turn_number // 5)
    season, phase = season_phase_map[turn_number % 5]

    return {
        'year'   : year,
        'season' : season,
        'phase'  : phase,
    }
