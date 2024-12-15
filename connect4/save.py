from player_console import PlayerConsole

from game_token import GameToken
from game_state import GameState
from drop_state import DropState
from game_logic_client import GameLogicClient
from ansi import Ansi
import time
from util import Util


class PlayerCoordinator:
    def __init__(self):
        """
        Initializes the game, sets up the player and game state. The player is going to be initialized 
        within the setup-function according to the OS and depending on the chosen player-color.
        
        Additionally prompts the user to input the IP address of the server where the game logic
        is hosted. Initializes the game logic client and retrieves the current game board.
        """
        self._current_player = None  # tracks current player in the game
        self._player = None
        self._myturn = None
        self._mytoken = None

        # initialize game
        raspi_name = input("Gib die IP deines Servers an: ")
        self._game_logic = GameLogicClient(raspi_name)
        self._board = self._game_logic.get_board() #get board
    
    def __setup__(self):
        """
        Method to set up the game environment including choosing player color and display mode.

        Args:
            None

        Returns:
            None
        """
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
        
        #Choose display mode if playing on Raspberry
        if Util.isRaspberry():
            from player_sense import PlayerSense
            self._display = input("Wo spielst du? Auf Konsole (c) oder dem SenseHat (s)? ")
            
            if self._display == "c":
                self._player = PlayerConsole(self._mytoken) # initialize Player on Console
            
            elif self._display == "s":
                self._player = PlayerSense(self._mytoken) # initialize Player on SenseHat
            
            else:
                print("Falsche Eingabe")
        else:
            self._player = PlayerConsole(self._mytoken)
        
        if self._mytoken == GameToken.RED: # make sure player red starts first
                self._current_player = self._player

        
            

    def run(self):
        """
        Play game until either won or draw.

        Args:
            None

        Returns:
            None
        """
        # play game until won or draw
        self.__setup__()
        if Util.isRaspberry():
            from player_sense import PlayerSense
    
    
        while (True):   

            gamestate = self._game_logic.get_state()
            self._player.draw_board(self._game_logic.get_board(), self._game_logic.get_state())


            if gamestate == GameState.WON_RED.value or gamestate == GameState.WON_YELLOW.value or gamestate == GameState.DRAW.value:
                print("Spiel wird beendet.")
                """if Util.isRaspberry():
                    #TODO: Win-Animation je nach Spieler"""
                self._game_logic.reset_board()
                break
            
            
            elif gamestate == self._myturn:
                self._current_player = self._player 
                column_to_drop = self._player.play_turn()  # get the move of the player
                drop_state = self._game_logic.drop_token(self._mytoken, column_to_drop)
                if drop_state == DropState.DROP_OK.value:
                    gamestate = self._game_logic.get_state()
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
