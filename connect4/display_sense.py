from display_base import DisplayBase
from input_console import InputConsole
from player_base import PlayerBase
from game_state import GameState
from game_token import GameToken
from ansi import Ansi
from input_base import Keys
import os
from sense_hat import SenseHat
from time import sleep

class SenseHatConsole(PlayerBase):
    def __init__(self, player: GameToken):  # Red or Yellow player
        super().__init__(player)
        self._sense = SenseHat()  # SenseHat-Instanz erstellen
        self._input = InputConsole()

    def draw_board(self, board: list, state: GameState):
        # Farben definieren
        RED = [255, 0, 0]       # Rot für roten Spieler
        YELLOW = [255, 255, 0]  # Gelb für gelben Spieler
        WHITE = [255, 255, 255] # Weiß für leere Felder
        BLACK = [0, 0, 0]       # Schwarz für Hintergrund

        # Sense-HAT-Display vorbereiten
        display = [[BLACK for _ in range(8)] for _ in range(8)]

        # 4-Gewinnt-Spielfeld unten links (6x7)
        for y in range(6):  # Zeilen des Spielfelds
            for x in range(7):  # Spalten des Spielfelds
                if board[y][x] == GameToken.RED:
                    display[7 - y][x] = RED  # Token des roten Spielers
                elif board[y][x] == GameToken.YELLOW:
                    display[7 - y][x] = YELLOW  # Token des gelben Spielers
                else:
                    display[7 - y][x] = WHITE  # Leeres Feld

        # Display an Sense HAT senden
        flat_display = sum(display, [])  # 2D-Array in 1D-Array umwandeln
        self._sense.set_pixels(flat_display)

        # Statusanzeige in der Konsole
        if state == GameState.TURN_YELLOW:
            print("Es ist der Zug von Gelb")
        elif state == GameState.TURN_RED:
            print("Es ist der Zug von Rot.")

#----------------------------------------------------

"""class PlayerCoordinator:
    def __init__(self):
        # initialize players
        self._player_red = SenseHatConsole(GameToken.RED)  # X
        self._player_yellow = SenseHatConsole(GameToken.YELLOW)  # 0
        self._board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
        self._state = GameState.TURN_RED

    def drop_token(self, player: GameToken, column: int) -> DropState:
        # TODO check if the column is valid (0..6) => return the appropriate DropState
        if column < 0 or column > 6:
            return DropState.COLUMN_INVALID
        
        # TODO check if the column is full => return the appropriate DropState
        elif self._board[0][column]  != GameToken.EMPTY:
            return DropState.COLUMN_FULL

        # TODO insert token into board (column = column_to_drop)      
        else:
            for row in range(5, -1, -1):
                if self._board[row][column] == GameToken.EMPTY:
                    self._board[row][column] = player  
                    return DropState.DROP_OK """

#ToDo Methode: Joystick input --> Inputs are the same as the arrow keys