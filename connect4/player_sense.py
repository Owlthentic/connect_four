from input_sense import InputSense
from display_sense import DisplaySense
from player_base import PlayerBase
from game_state import GameState
from game_token import GameToken
from input_base import Keys
from sense_hat import SenseHat

class PlayerSense(PlayerBase):
    """
    Class representing the player's interaction and logical decisions in the game.

    Methods:
    - __init__(self, player: GameToken): Initializes the PlayerSense object with the specified player (Red or Yellow).
    - draw_board(self, board: list, gamestate: GameState): Draws the game board based on the current state of the game.
    - play_turn(self) -> int: Handles the sequence of playing a turn.
    - select_column(self): Handles the column selection logic for the player.
    """
    def __init__(self, player: GameToken):  # Red or Yellow player
        """
        Initializes a new instance of the Class.

        Args:
            player: a GameToken (enum) representing the player color, either RED or YELLOW

        Returns:
            None
        """
        super().__init__(player)
        self.display_sense = DisplaySense()
        self._input = InputSense()
        
        self._base_color = 0
        if player == GameToken.RED:
            self._player_color = 1
        elif player == GameToken.YELLOW:
            self._player_color = 3
        else:
            self._player_color = 2


    def draw_board(self, board:list, gamestate:GameState):
        """
        Draws the game board based on the current state of the game.

        Args:
            board: list, the 2D list representing the game board
            gamestate: GameState, the current state of the game

        Returns:
            None
        """
        self.display_sense.draw_grid()
        
        for y_pos, row in enumerate(board):
            for x_pos, cell in enumerate(row):
                self.display_sense.draw_token(x_pos, y_pos, cell)
        
        YELLOW = (255, 255, 0)
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        sense = SenseHat()

        if gamestate == GameState.TURN_RED.value:
            pass
        elif gamestate == GameState.TURN_YELLOW.value:
            pass
        elif gamestate == GameState.WON_RED.value: # winning screen for player red
            sense.clear(RED)
            sense.show_message("RED WINS", 0.1, BLACK, RED)
        elif gamestate == GameState.WON_YELLOW.value: # winning screen for player yellow:
            sense.clear(YELLOW)
            sense.show_message("YELLOW WINS", 0.1, BLACK, YELLOW)
        else: # draw screen
            sense.clear(BLACK)
            sense.show_message("DRAW", 0.1, BLACK, WHITE)
       

    def play_turn(self) -> int:
        """
        This method is used to play a turn in a game.
        It selects a column to place a game piece and returns the position of the selected column.

        Args:
            None

        Returns:
            int: The position of the selected column
        """
        pos = self.select_column()

        return pos

    def select_column(self):
        """
        Get user to select a column on the display.

        Args:
            None

        Returns:
            int: The position of the selected column.
        """
        pos = 3
        key_pressed = Keys.UNKNOWN
        while True:
            self.display_sense.draw_input(pos, self._player)
            key_pressed = self._input.read_key()

            if key_pressed == Keys.RIGHT and pos < 6:
                pos += 1

            elif key_pressed == Keys.LEFT and pos > 0:
                pos -= 1
            
            elif key_pressed == Keys.ENTER or key_pressed == Keys.DOWN:
                self.display_sense.clear_input()
                return pos


if __name__ == '__main__':
    board = [[' ' for _ in range(7)] for _ in range(6)]
    board[5][0] = GameToken.RED  # [Y][X]
    board[4][3] = GameToken.YELLOW
    p = PlayerSense(GameToken.YELLOW)

    p.draw_board(board, GameState.TURN_YELLOW)
    pos = p.play_turn()
    print(pos)