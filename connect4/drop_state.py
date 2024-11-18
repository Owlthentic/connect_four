from enum import Enum


class DropState(Enum):
    """
    Enum class representing different states after drop of a token
    """
    DROP_OK = 0          # token dropped successfully
    COLUMN_INVALID = 1   # The selected column is invalid
    COLUMN_FULL = 2      # The selected column is already full
    WRONG_PLAYER = 3     # A player made a move that is not theirs
