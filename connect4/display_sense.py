om display_base import DisplayBase
from game_token import GameToken
from sense_hat import SenseHat

# Farben definieren
RED = [255, 0, 0]       # Rot für roten Spieler
YELLOW = [255, 255, 0]  # Gelb für gelben Spieler
WHITE = [100, 100, 100] # Weiß für leere Felder
BLACK = [0, 0, 0]       # Schwarz für Hintergrund

class DisplaySense(DisplayBase):
    """
    This class serves as a display controller for the Sense HAT module, providing methods to draw grids, tokens, and manage input.

    Methods:
    - __init__(self): Initializes the DisplaySense class with necessary attributes.
    - _update_screen(self): Sends the display to the Sense HAT hardware.
    - gen_grid(self): Generates a grid for the play area.
    - draw_grid(self): Draws the grid on the display.
    - draw_token(self, x_pos, y_pos, token): Draws a token of specified color at the given position.
    - clear_input(self): Clears the input token on the display.
    - draw_input(self, column, token): Draws the input token at the specified column position.
    """
    def __init__(self):
        """
        Initializes a new instance of the Class.

        Args:
            self: Instance of the Class.

        Returns:
            None.
        """
        self._sense = SenseHat()  # SenseHat-Instanz erstellen
        self._display = []
        self._grid = self.gen_grid()
        self._prev_column = 3

    def _update_screen(self):
        """
        Send Display to Sense HAT.
        Convert 2D-Array to 1D-Array and set pixels on Sense HAT screen.

        Args:
            None

        Returns:
            None
        """
        # Display an Sense HAT senden
        flat_display = sum(self.display, [])  # 2D-Array in 1D-Array umwandeln
        self._sense.set_pixels(flat_display)

    def gen_grid(self):
        """
        Generates and returns a new grid for the game.

        Args:
            None

        Returns:
            gir: A 2D list representing the game grid.
        """
        # clear screen
        grid = [[BLACK for _ in range(8)] for _ in range(8)]

        # create play-area
        for y in range(2, 6+2):
            for x in range(7):
                grid[y][x] = WHITE

        return grid

    def draw_grid(self):
        """
        Draws the grid on the screen.

        Args:
            None

        Returns:
            None
        """
        # clear screen
        self.display = self._grid
        self._update_screen()

    def draw_token(self, x_pos, y_pos, token):
        """
        Draws a token of specified color at the given position.

        Args:
            x_pos: x-coordinate of the position where the token will be drawn
            y_pos: y-coordinate of the position where the token will be drawn
            token: the type of token to be drawn, either GameToken.RED or GameToken.YELLOW

        Returns:
            None
        """
        if token == GameToken.RED:
            color = RED
        elif token == GameToken.YELLOW:
            color = YELLOW
        else:
            color = WHITE
        
        self.display[y_pos + 2][x_pos] = color
        self._update_screen()

    def clear_input(self):
        """
        This method clears the input area on the screen.

        Args:
            None

        Returns:
            None
        """
        self.display[1][self._prev_column] = BLACK

    def draw_input(self, column, token):
        """
        Draw the input indicator for a specific column.

        Args:
            column: the column number where the token will be drawn
            token: the token to be drawn in the specified column

        Returns:
            None
        """
        self.clear_input()
        self.draw_token(column, -1, token)
        self._prev_column = column


if __name__ == "__main__":
    fc = DisplaySense()
    fc.draw_grid()
    fc.draw_token(0, 0, GameToken.RED)
    fc.draw_token(5, 2, GameToken.YELLOW)
