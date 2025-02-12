from enum import Enum, auto

class PrepaymentDecision(Enum):
    SAVE = auto()
    BREAK_EVEN = auto()
    LOSE = auto()