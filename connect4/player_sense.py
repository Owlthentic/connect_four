from input_sense import InputSense
from display_sense import DisplaySense
from player_base import PlayerBase
from game_state import GameState
from game_token import GameToken
from input_base import Keys
from sense_hat import SenseHat

class PlayerSense(PlayerBase):
    def __init__(self, player: GameToken):  # Red or Yellow player
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
        pos = self.select_column()

        return pos

    def select_column(self):
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