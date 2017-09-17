from enum import Enum

from pydip.player.unit import UnitTypes


class UnitType(Enum):
    TROOP = 'troop'
    FLEET = 'fleet'

    def to_pydip(self):
        if self == UnitType.TROOP:
            return UnitTypes.TROOP
        if self == UnitType.FLEET:
            return UnitTypes.FLEET
        raise ValueError

    @staticmethod
    def from_pydip(pydip_type):
        if pydip_type == UnitTypes.TROOP:
            return UnitType.TROOP
        if pydip_type == UnitTypes.FLEET:
            return UnitType.FLEET
        raise ValueError


class TurnPhase(Enum):
    MOVEMENT   = 'move'
    RETREAT    = 'retreat'
    ADJUSTMENT = 'adjustment'
