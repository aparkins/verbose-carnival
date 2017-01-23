

def get_readable_turn(turn_number):
    assert turn_number >= 0
    if turn_number == 0:
        return 'Registration'

    turn_number -= 1
    season_phase_map = {
        0: ('Spring', None),
        1: ('Spring', 'Retreat'),
        2: ('Fall', None),
        3: ('Fall', 'Retreat'),
        4: ('Fall', 'Adjustment'),
    }

    year = 1901 + (turn_number // 5)
    season, phase = season_phase_map[turn_number % 5]

    readable_turn = '{} {}'.format(season, year)
    if phase is not None:
        readable_turn += ' ({})'.format(phase)

    return readable_turn
