from ansi import Ansi
from game_token import GameToken
from display_base import DisplayBase
import os

class DisplayConsole(DisplayBase):
    def __init__(self):
        self.gen_grid()

    def _clear_console(self):
        os.system('clear')
        os.system('cls')    

    @ staticmethod
    def gen_row(left:str, middle:str, right:str, spacer:str):
        row = ""
        row += left + spacer
        for cell in range(7-2):
            row += middle + spacer
        row += middle + spacer + right
        return row
    
        
    def gen_grid(self):
        horizontal_spacer = "───"
        void_spacer = "   "

        top_row = self.gen_row("┌", "┬", "┐", horizontal_spacer)
        middle_row = self.gen_row("├", "┼", "┤", horizontal_spacer)
        bottom_row = self.gen_row("└", "┴", "┘", horizontal_spacer)
        spacer = self.gen_row("│", "│", "│", void_spacer)

        self.grid = ""
        self.grid += top_row + "\n"
        self.grid += spacer + "\n"

        for row_1 in range(6-1):
            self.grid += middle_row + "\n"
            self.grid += spacer + "\n"
        self.grid += bottom_row


    def draw_grid(self):
        self._clear_console
        Ansi.clear_screen()
        Ansi.reset()

        Ansi.gotoXY(0, 3)
        print(self.grid)

        Ansi.gotoXY(0, 16)
        
    def draw_token(self, x_pos, y_pos):
        Ansi.gotoXY(self.x_translation(x_pos), 
                    self.y_translation(y_pos))
        print("●")
        Ansi.gotoXY(0, 16)
        
    @ staticmethod
    def y_translation(y_pos):
        y = 2 + 2 + y_pos * 2
        return y
    @ staticmethod
    def x_translation(x_pos):
        x = 3 + x_pos * 4
        return x
    
    def draw_input(self, column):
        self.clear_input()

        y = 2
        x = self.x_translation(column)

        Ansi.gotoXY(x, y)
        print("●")
        
        Ansi.gotoXY(0, 16)

    @ staticmethod
    def clear_input():
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
