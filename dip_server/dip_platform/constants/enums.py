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


class MovementCommandType(Enum):
    HOLD = 'hold'
    MOVE = 'move'
    SUPPORT = 'support'
    CONVOY_TRANSPORT = 'convoyTransport'
    CONVOY_MOVE = 'convoyMove'


class RetreatCommandType(Enum):
    RETREAT = 'retreat'
    DISBAND = 'disband'


class TurnSeason(Enum):
    SPRING = 'spring'
    FALL   = 'fall'
    WINTER = 'winter'


class TurnPhase(Enum):
    MOVEMENT   = 'movement'
    RETREAT    = 'retreat'
    ADJUSTMENT = 'adjustment'
