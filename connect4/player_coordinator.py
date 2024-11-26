from player_console import PlayerConsole
from game_token import GameToken
from game_state import GameState
from drop_state import DropState
from game_logic_client import GameLogicClient
from ansi import Ansi


class PlayerCoordinator:
    def __init__(self):
        # initialize players
        self._player_red = PlayerConsole(GameToken.RED)  # X
        self._player_yellow = PlayerConsole(GameToken.YELLOW)  # 0

        # initialize game
        self._game_logic = GameLogicClient("127.0.0.1")
        self._board = self._game_logic.get_board() #get board
        
    """def _end_game(self):
        gamestate = self._game_logic.get_state()
        if gamestate == GameState.WON_RED:
            self._player_red.draw_board(self._board, gamestate)
            print("\033[31mRot hat das Spiel gewonnen!!")
            Ansi.reset()
        if gamestate == GameState.WON_YELLOW:
            self._player_yellow.draw_board(self._board, gamestate)
            print("\033[33mGelb hat das Spiel gewonnen!!")
            Ansi.reset()
        if gamestate == GameState.DRAW:
            self._player_yellow.draw_board(self._board, gamestate) 
            print("Unentschieden!!")"""

    def run(self):
        # play game until won or draw
        while (True):

            """gamestate = self._game_logic.get_state()
            print(f"gamestate = {gamestate}")
            if gamestate == GameState.WON_RED or gamestate == GameState.WON_YELLOW or gamestate == GameState.DRAW:
                #self._end_game()
                break"""

           
            self._player_red.draw_board(self._game_logic.get_board(), self._game_logic.get_state())
            while(True):
                column_to_drop = self._player_red.play_turn()  # get the move of the player
                drop_state = self._game_logic.drop_token(GameToken.RED, column_to_drop)
                if drop_state == DropState.DROP_OK.value:
                    break
                else:
                    print("Das hat nicht geklappt, versuch's noch einmal")
            
            """gamestate = self._game_logic.get_state()
            print(f"gamestate = {gamestate}")
            if gamestate == GameState.WON_RED or gamestate == GameState.WON_YELLOW or gamestate == GameState.DRAW:
                print(f"gamestate = {gamestate}")
                #self._end_game()
                break"""
           
            self._player_yellow.draw_board(self._game_logic.get_board(), self._game_logic.get_state())
            while(True):
                column_to_drop = self._player_yellow.play_turn()  # get the move of the player
                drop_state = self._game_logic.drop_token(GameToken.YELLOW, column_to_drop)
                if drop_state == DropState.DROP_OK.value:
                    break
                else:
                    print("Das hat nicht geklappt, versuch's noch einmal")


# start a local game
if __name__ == '__main__':
    coordinator = PlayerCoordinator()
    coordinator.run()
