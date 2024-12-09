from player_console import PlayerConsole
from game_token import GameToken
from game_state import GameState
from drop_state import DropState
from game_logic_client import GameLogicClient
from ansi import Ansi
import time


class PlayerCoordinator:
    def __init__(self):
        # initialize players
        self._player_red = PlayerConsole(GameToken.RED)  # X
        self._player_yellow = PlayerConsole(GameToken.YELLOW)  # 0
        self._current_player = self._player_red

        # initialize game
        self._game_logic = GameLogicClient("127.0.0.1")
        self._board = self._game_logic.get_board() #get board
        

    def run(self):
        # play game until won or draw
        while (True):   

            gamestate = self._game_logic.get_state()
            self._current_player.draw_board(self._game_logic.get_board(), self._game_logic.get_state())

            if gamestate == GameState.WON_RED or gamestate == GameState.WON_YELLOW or gamestate == GameState.DRAW:
                print("Noch eine Runde? j/n")
                response = input()
                if response.lower() == "j":
                    self._game_logic.reset()
                    self._current_player = self._player_red
                else:
                    print("Spiel wird beendet.")
                    break
            
            
            if self._current_player == self._player_red:
                column_to_drop = self._player_red.play_turn()  # get the move of the player
                drop_state = self._game_logic.drop_token(GameToken.RED, column_to_drop)
                if drop_state == DropState.DROP_OK.value:
                    self._current_player = self._player_yellow
                else:
                    print("Das hat nicht geklappt, versuch's noch einmal")
                    continue
            
            else:
                time.sleep(1)



# start a local game
if __name__ == '__main__':
    coordinator = PlayerCoordinator()
    coordinator.run()
