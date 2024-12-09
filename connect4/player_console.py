from input_console import InputConsole
from display_console import DisplayConsole
from player_base import PlayerBase
from game_state import GameState
from game_token import GameToken
from ansi import Ansi
from input_base import Keys


class PlayerConsole(PlayerBase):
    def __init__(self, player: GameToken):  # Red or Yellow player
        super().__init__(player)
        self.display_console = DisplayConsole()
        self._input = InputConsole()
        
        self._base_color = 0
        if player == GameToken.RED:
            self._player_color = 1
        elif player == GameToken.YELLOW:
            self._player_color = 3
        else:
            self._player_color = 2


    def draw_board(self, board:list, gamestate:GameState):

        self.display_console.draw_grid()

        for y_pos, row in enumerate(board):
            for x_pos, cell in enumerate(row):
                if cell == GameToken.RED:
                    Ansi.set_foreground(1, False)
                    self.display_console.draw_token(x_pos, y_pos)
                if cell == GameToken.YELLOW:
                    Ansi.set_foreground(3, False)
                    self.display_console.draw_token(x_pos, y_pos)
                else:
                    pass
        
        if gamestate == 0:
            Ansi.set_foreground(self._base_color, False)
            print("Es ist der Zug von ", end="")
            Ansi.set_foreground(1, False)
            print("Rot")
        elif gamestate == 1:
            Ansi.set_foreground(self._base_color, False)
            print("Es ist der Zug von ", end="")
            Ansi.set_foreground(3, False)
            print("Gelb")
        elif gamestate == 2:
            Ansi.set_foreground(1, False)
            print("Rot hat gewonnen!!")
            Ansi.set_foreground(self._base_color, False)
            
        elif gamestate == 3:
            Ansi.set_foreground(3, False)
            print("Gelb hat gewonnen!!")
            Ansi.set_foreground(self._base_color, False)
           
        elif gamestate == 4:
            Ansi.set_foreground(self._base_color, False)
            print("Unentschieden...")
            Ansi.set_foreground(self._base_color, False)

        Ansi.set_foreground(self._base_color, False)

    def play_turn(self) -> int:
        Ansi.set_foreground( self._player_color, False)
        pos = self.select_column()

        Ansi.set_foreground(self._base_color, False)
        return pos

    def select_column(self):
        pos = 3
        key_pressed = Keys.UNKNOWN
        while key_pressed != Keys.ESC:
            self.display_console.draw_input(pos)
            key_pressed = self._input.read_key()

            if key_pressed == Keys.RIGHT and pos < 6:
                pos += 1

            elif key_pressed == Keys.LEFT and pos > 0:
                pos -= 1
            
            elif key_pressed == Keys.ENTER or key_pressed == Keys.DOWN:
                return pos
            
        print("pressed Escape")  

if __name__ == '__main__':
    board = [[' ' for _ in range(7)] for _ in range(6)]
    board[5][0] = GameToken.RED  # [Y][X]
    board[4][3] = GameToken.YELLOW
    p = PlayerConsole(GameToken.YELLOW)

    p.draw_board(board, GameState.TURN_YELLOW)
    pos = p.play_turn()
    print(pos)



