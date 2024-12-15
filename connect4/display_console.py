from ansi import Ansi
from game_token import GameToken
from display_base import DisplayBase
import os

class DisplayConsole(DisplayBase):
    """
    DisplayConsole class provides methods to display a grid and various elements on the console for a game.

    Methods:
        - __init__(): Constructor method to initialize the DisplayConsole class, generating the grid.
        - gen_row(left:str, middle:str, right:str, spacer:str): Static method to generate a row of the grid structure.
        - gen_grid(): Method to generate the full grid structure.
        - draw_grid(): Method to draw the grid on the console.
        - draw_token(x_pos, y_pos): Method to draw a token at a specified position on the grid.
        - y_translation(y_pos): Static method to translate the y position of the board into console coordinates.
        - x_translation(x_pos): Static method to translate the x position of the board into console coordinates.
        - draw_input(column): Method to draw the input indicator for a specific column.
        - clear_input(): Static method to clear the input indicator from the console.
    """
    def __init__(self):
        self.gen_grid()
        self._grid = self.gen_grid()

    def _clear_console(self):
        """
        Clears the console by executing system commands to clear the console screen on both Unix and Windows systems.

        Args:
            self: The current instance of the class.

        Returns:
            None
        """
        os.system('clear')
        os.system('cls')    

    @ staticmethod
    def gen_row(left:str, middle:str, right:str, spacer:str):
        """
        Static method to generate a row of the grid structure.

        Args:
            left: A string representing the left boarder of the row.
            middle: A string representing the middle boarder of the row.
            right: A string representing the right boarder of the row.
            spacer: A string representing the space between the boarders of a row.

        Returns:
            A string representing a row of a connect four grid.
        """
        row = ""
        row += left + spacer
        for cell in range(7-2):
            row += middle + spacer
        row += middle + spacer + right
        return row
    
    
    def gen_grid(self):
        """
        Generate a grid with custom stylized characters.

        Args:
            None

        Returns:
            str: A string representing the generated grid.
        """
        horizontal_spacer = "───"
        void_spacer = "   "

        top_row = self.gen_row("┌", "┬", "┐", horizontal_spacer)
        middle_row = self.gen_row("├", "┼", "┤", horizontal_spacer)
        bottom_row = self.gen_row("└", "┴", "┘", horizontal_spacer)
        spacer = self.gen_row("│", "│", "│", void_spacer)

        grid = ""
        grid += top_row + "\n"
        grid += spacer + "\n"

        for row_1 in range(6-1):
            grid += middle_row + "\n"
            grid += spacer + "\n"
        grid += bottom_row

        return grid


    def draw_grid(self):
        """
        Draws the grid on the console.

        Args:
            None

        Returns:
            None
        """
        self._clear_console
        Ansi.clear_screen()
        Ansi.reset()

        Ansi.gotoXY(0, 3)
        print(self._grid)

        Ansi.gotoXY(0, 16)
        
    def draw_token(self, x_pos: int, y_pos: int):
        """
        Draw a token at a specified position on the grid.

        Args:
            x_pos: Integer representing the x position of the token on the board.
            y_pos: Integer representing the y position of the token on the board.

        Returns:
            None
        """
        Ansi.gotoXY(self.x_translation(x_pos),
                    self.y_translation(y_pos))
        print("●")
        Ansi.gotoXY(0, 16)
        
    @ staticmethod
    def y_translation(y_pos):
        """
        Static method to translate the y position of the board into console coordinates.

        Args:
            y_pos:

        Returns:
            y: Integer representing the y position of the board on the console.
        """
        y = 2 + 2 + y_pos * 2
        return y
    @ staticmethod
    def x_translation(x_pos):
        """
        Static method to translate the x position of the board into console coordinates.

        Args:
            x_pos:

        Returns:
            x: Integer representing the x position of the board on the console.
        """
        x = 3 + x_pos * 4
        return x
    
    def draw_input(self, column):
        """
        Draw the input indicator for a specific column.

        Args:
            column: The column number where the input should be displayed.

        Returns:
            None
        """
        self.clear_input()

        y = 2
        x = self.x_translation(column)

        Ansi.gotoXY(x, y)
        print("●")
        
        Ansi.gotoXY(0, 16)

    @ staticmethod
    def clear_input():
        """
        This method clears the input area on the screen.

        Args:
            None

        Returns:
            None
        """
        y = 2
        empty_line = " " * (7 * 4 + 1)

        Ansi.gotoXY(0, y)
        print(empty_line, end="")

        Ansi.gotoXY(0, 16)



if __name__ == '__main__':
    fc = DisplayConsole()
    fc.draw_grid()
    fc.draw_token(0, 0)
    fc.draw_token(5, 2)
    fc.draw_input(1)
    fc.draw_input(2)
