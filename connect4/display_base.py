from ansi import Ansi
from game_token import GameToken


class DisplayBase:
    """
    Base class for displaying a grid and tokens in the game.
    """

    def draw_grid(self) -> None:
        """
        Draw the grid on the display.

        This method should be implemented by subclasses to provide 
        specific grid drawing logic.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def draw_token(self, x: int, y: int, token) -> None:
        """
        Draw a token at the specified coordinates on the grid.

        Parameters:
        - x: The horizontal position (column) to place the token.
        - y: The vertical position (row) to place the token.
        - token: The token to be drawn (e.g., player token).

        This method should be implemented by subclasses to provide 
        specific token drawing logic.
        """
        raise NotImplementedError("Subclasses must implement this method.")
