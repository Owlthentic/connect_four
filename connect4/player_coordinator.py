from player_console import PlayerConsole
from player_sense import PlayerSense
from game_token import GameToken
from game_state import GameState
from drop_state import DropState
from game_logic_client import GameLogicClient
from ansi import Ansi
import time


class PlayerCoordinator:
    def __init__(self):
        # initialize players
        self._current_player = None  # player to start the game
    
        self._player = None
        self._myturn = None
        self._mytoken = None

        # initialize game
        self._game_logic = GameLogicClient("127.0.0.1")
        self._board = self._game_logic.get_board() #get board
    
    def __setup__(self):
        #Choose player color
        self._color = input("Was ist deine Spielerfarbe? Rot (r) oder Gelb (g)? ")
        if self._color.lower() == "r":
            self._myturn = 0
            self._mytoken = GameToken.RED
            print("Du bist Rot")
        
        elif self._color.lower() == "g":
            self._myturn = 1
            self._mytoken = GameToken.YELLOW
            print("Du bist Gelb")
        
        else:
            print("Falsche Eingabe")
            self.__setup__()
        
        #Choose display mode
        self._display = input("Wo spielst du? Auf Konsole (c) oder dem SenseHat (s)? ")
        
        if self._display == "c":
            self._player = PlayerConsole(self._mytoken) # initialize Player on Console
        
        elif self._display == "s":
            self._player = PlayerSense(self._mytoken) # initialize Player on SenseHat
        
        else:
            print("Falsche Eingabe")
        
        if self._mytoken == GameToken.RED: # make sure player red starts first
                self._current_player = self._player

        
            

    def run(self):
        # play game until won or draw
        self.__setup__()
    
        while (True):   

            gamestate = self._game_logic.get_state()
            self._current_player.draw_board(self._game_logic.get_board(), self._game_logic.get_state())


            if gamestate == GameState.WON_RED or gamestate == GameState.WON_YELLOW or gamestate == GameState.DRAW:
                print("Noch eine Runde? j/n")
                response = input()
                if response.lower() == "j":
                    self._game_logic.reset_board()
                    self._current_player = None
                else:
                    print("Spiel wird beendet.")
                    break
            
            
            elif gamestate == self._myturn:
                self._current_player = self._player 
                column_to_drop = self._player.play_turn()  # get the move of the player
                drop_state = self._game_logic.drop_token(self._mytoken, column_to_drop)
                if drop_state == DropState.DROP_OK.value:
                    if self._mytoken == GameToken.RED:
                        gamestate = GameState.TURN_YELLOW
                    else:
                        gamestate = GameState.TURN_RED
                else:
                    print("Das hat nicht geklappt, versuch's noch einmal")
                    continue
            
            else:
                print("Warte auf deinen Mitspieler")
                time.sleep(1)



# start a local game
if __name__ == '__main__':
    coordinator = PlayerCoordinator()
    coordinator.run()
