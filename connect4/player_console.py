from display_base import DisplayBase
from input_console import InputConsole
from player_base import PlayerBase
from game_state import GameState
from game_token import GameToken
from ansi import Ansi
from input_base import Keys
import os

# going to work in this
class PlayerConsole(PlayerBase):
    def __init__(self, player: GameToken):  # Red or Yellow player
        super().__init__(player)
        # self._display = DisplayConsole()
        self._input = InputConsole()

    def play_turn(self) -> int:
        # TODO: return desired column from user input (0..6)
        drop_pos = 3
        input = InputConsole()
        while True:
            if input.key_pressed():
                key = input.read_key()  # Lese die gedrückte Taste
                if key == Keys.DOWN:
                    return drop_pos
                elif key == Keys.LEFT:
                    if drop_pos > 0:
                        drop_pos -= 1
                    else:
                        pass
                elif key == Keys.RIGHT:
                    if drop_pos < 6:
                        drop_pos += 1
                    else:
                        pass
    def _clear_console(self):
        os.system('clear')
        os.system('cls')    

                
    def draw_board(self, board: list, state: GameState):
        self._clear_console()

        # TODO: draw grid with tokens
        print("┌───┬───┬───┬───┬───┬───┬───┐")
        row_count = 0
        for row in board:
            print("|", end="")
            for cell in row:
                if cell == GameToken.RED:
                    print(" \033[31m●\033[0m ", end="|")
                elif cell == GameToken.YELLOW:
                    print(" \033[33m●\033[0m ", end="|")
                else:
                    print("   ", end="|")
            print()
            if row_count <=4:
                print("├───┼───┼───┼───┼───┼───┼───┤")
                row_count += 1
            elif row_count == 5:
                print("└───┴───┴───┴───┴───┴───┴───┘")

        if state == GameState.TURN_YELLOW:
            print("Es ist der Zug von Gelb")
        elif state == GameState.TURN_RED:
            print("Es ist der Zug von Rot.")


if __name__ == '__main__':
    board = [[' ' for _ in range(7)] for _ in range(6)]
    board[5][0] = GameToken.RED  # [Y][X]
    p = PlayerConsole(GameToken.YELLOW)

    Ansi.clear_screen()
    Ansi.reset()
    p.draw_board(board, GameState.TURN_YELLOW)
    pos = p.play_turn()
    Ansi.reset()
    Ansi.gotoXY(1, 20)
    print(f"Position: {pos}")
