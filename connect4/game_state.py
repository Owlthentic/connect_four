from enum import Enum


class GameState(Enum):
    """
    Enum class representing different states of the game.

    This class defines the possible states that the game can be in,
    including the current turn and the outcome of the game.
    """
    TURN_RED = 0          # It's Red's turn to play
    TURN_YELLOW = 1       # It's Yellow's turn to play
    WON_RED = 2           # Red has won the game
    WON_YELLOW = 3        # Yellow has won the game
    DRAW = 4              # The game ends in a draw


if __name__ == '__main__':
    s = GameState.TURN_RED
    print(f"GameState {s}, Type: {type(s)}, Value: {s.value}")
