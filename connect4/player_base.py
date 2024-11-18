from display_base import *
from game_state import GameState


class PlayerBase:
    """
    Base class for representing a player in the game.

    This class provides an interface for player actions, including
    making a move and drawing the game board. Subclasses must implement
    the required methods to provide specific player behavior.
    """

    def __init__(self, player: GameToken):
        """
        Initialize the player with a specific game token.

        Parameters:
        - player: The token representing the player (e.g., RED or YELLOW).
        """
        self._player = player

    def play_turn(self) -> int:
        """
        Asks the player to play their turn.

        Returns:
            int: The column index where the player drops their token.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("You need to subclass Player to use play_turn().")

    def draw_board(self, board) -> None:
        """
        Draw the game board for the player.

        Parameters:
        - board: The current state of the game board.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("You need to subclass Player to use draw_board().")

    @property
    def player_id(self) -> GameToken:
        """
        Get the player's token.

        Returns:
            GameToken: The token representing the player.
        """
        return self._player
