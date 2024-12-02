from display_base import DisplayBase
from input_console import InputConsole
from player_base import PlayerBase
from game_state import GameState
from game_token import GameToken
from ansi import Ansi
from connect4.input_sense import Keys
import os
from sense_hat import SenseHat
from time import sleep

# Farben definieren
RED = [255, 0, 0]       # Rot für roten Spieler
YELLOW = [255, 255, 0]  # Gelb für gelben Spieler
WHITE = [100, 100, 100] # Weiß für leere Felder
BLACK = [0, 0, 0]       # Schwarz für Hintergrund

class DisplaySense(DisplayBase):
    def __init__(self):
        self._sense = SenseHat()  # SenseHat-Instanz erstellen
        self._display = []
        self._grid = self.gen_grid()

    def _update_screen(self):
        # Display an Sense HAT senden
        flat_display = sum(self.display, [])  # 2D-Array in 1D-Array umwandeln
        self._sense.set_pixels(flat_display)

    def gen_grid(self):
        # clear screen
        grid = [[BLACK for _ in range(8)] for _ in range(8)]

        # create play-area
        for y in range(2, 6+2):
            for x in range(7):
                grid[y][x] = WHITE

        return grid

    def draw_grid(self):
        # clear screen
        self.display = self._grid
        self._update_screen()

    def draw_token(self, x_pos, y_pos, token):
        if token == GameToken.RED:
            color = RED
        elif token == GameToken.YELLOW:
            color = YELLOW
        else:
            color = WHITE
        
        self.display[y_pos + 2][x_pos] = color
        self._update_screen()

    def draw_input(self, token):
        pass


if __name__ == "__main__":
    fc = DisplaySense()
    fc.draw_grid()
    fc.draw_token(0, 0, GameToken.RED)
    fc.draw_token(5, 2, GameToken.YELLOW)
