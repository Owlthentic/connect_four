from game_state import GameState
from game_token import GameToken
from drop_state import DropState


class GameLogicBase:
    """
        GameLogicBase provides basic methods for interacting with the game's logic.
    """

    def __init__(self):
        pass

    def get_board(self) -> list:
        """
        Returns the board as a list of lists. The board positions are displayed as a string. They can contain one of 3 values:
        - 'X' or '0': the game position is occupied by player 'X' or '0', respectively
        - ' ': the game position is still unoccupied
        """
        return self._board

    def get_state(self) -> GameState:
        raise NotImplementedError("")

    def drop_token(self, player: GameToken, column: int) -> DropState:
        """
        The current player (identified by either 'X' or 'Y') makes their move by dropping their token into the specified column. 
        Parameters:
        - player: The token representing the player (i.e., RED or YELLOW).
        - column: The column (0..6) into which to drop the token.
        Returns:
        DropState: The state of the drop (e.g., okay, invalid position, column full).

        """
        raise NotImplementedError("You need to subclass GameLogicBase to use move().")
