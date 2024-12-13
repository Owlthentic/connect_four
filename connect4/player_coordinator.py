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
        Initializes the game, sets up the player and game state. 
        prompts the user to input the IP address of the server where the game logic
        is hosted. Initializes the game logic client and retrieves the current game board.
        -----------------------------------------------------------------------------------
        _current_player (None): Placeholder for the player who will start the game.
        This value is set later during the game setup.
        
        _player (None): Placeholder for the player's identifier. The player is going to be initialized 
        within the setup-function according to the OS and depending on the chosen player-color.

        _myturn (None): Placeholder to track if it's this player's turn. This will be set to indicate whether it is this player's turn to make a move.
        
        _mytoken (None): Placeholder to track the player's color. This will be set to indicate in which color
        the dropped token needs to be drawn
        """
        self._current_player = None # used to initialize the first player
        self._player = None # used to initialize the player on this console or sensehat
        self._myturn = None # used to track if it's this player's turn
        self._mytoken = None # used to track the player's color

        """
        raspi_name (str): Prompts the user to enter the IP address of the server hosting
        the game logic. This value is used to establish a connection to the game server.
        
        _game_logic (GameLogicClient): Initializes the game logic client with the provided IP address.
        
        _board (list): Retrieves the current state of the game board from the game logic client.
        """
        raspi_name = input("Gib die IP deines Servers an: ")
        self._game_logic = GameLogicClient(raspi_name)
        self._board = self._game_logic.get_board() #get board
    
    def __setup__(self):
        """Sets up the game by prompting the user to choose their player color and mode of displaying the game 
        (console or sensehat). Setting the red player as first player.
        ---------------------------------------------------------------------------------------------------
        _color (str): Placeholder to track the player's color. Let's the player choose their color.
        
        _myturn (enum): Placeholder to track if it's this player's turn. Set according to the values defined by 
        the game_state class. 
        
        _mytoken (enum): Placeholder to track the player's color. Set according to the values defined by the game_token class .
        """
        self._color = input("Was ist deine Spielerfarbe? Rot (r) oder Gelb (g)? ")
        if self._color.lower() == "r":
            self._myturn = GameState.TURN_RED.value
            self._mytoken = GameToken.RED
            print("Du bist Rot")
        
        elif self._color.lower() == "g":
            self._myturn = 1
            self._mytoken = GameToken.YELLOW
            print("Du bist Gelb")
        
        else:
            print("Falsche Eingabe")
            self.__setup__()
        
        """
        Setting up the appropriate game display depending on the hardware in use.
        -----------------------------------------------------------------------------------------------
        _display (str): In case the player is playing on a raspberry, the player is asked to choose playing
        either  on the console or on the SenseHat. If not, the game will be played on the console. 
        """
        if Util.isRaspberry():
            from player_sense import PlayerSense
            self._display = input("Wo spielst du? Auf Konsole (c) oder dem SenseHat (s)? ")
            
            if self._display == "c":
                self._player = PlayerConsole(self._mytoken) # initialize Player on Console
            
            elif self._display == "s":
                self._player = PlayerSense(self._mytoken) # initialize Player on SenseHat
            
            else:
                print("Falsche Eingabe")
                self.__setup__()
        else:
            self._player = PlayerConsole(self._mytoken)
        
        """
        If this player chose the red colour, this player will be set as the first player.
        """
        if self._mytoken == GameToken.RED: # make sure player red starts first
                self._current_player = self._player



    def run(self):
        """
        Running the game loop. Continuously asks the current player to make a move or waits for the other
        player to make a move. Exits the loop game when the game is won or drawn.
        """
        self.__setup__()
        if Util.isRaspberry(): # checking, if the game is played on the Raspberry
            from player_sense import PlayerSense # Import the PlayerSense class from the player_sense module
    
        while (True):  
            """
            gamestate (enum): Placeholder to track the current game state. Gets the gamestate from the game_logic_client via REST Api.
            
            _player.draw_board(board, gamestate): Draws the current game board.
            
            """ 
            gamestate = self._game_logic.get_state()
            self._player.draw_board(self._game_logic.get_board(), self._game_logic.get_state())


            """
            1. Check for a win or a draw and ends the game when the game is won or drawn
            2. Ask the player to make a move, when it is his turn 
            3. Waits for the other player's move.
            """ 
            if gamestate == GameState.WON_RED.value or gamestate == GameState.WON_YELLOW.value or gamestate == GameState.DRAW.value:
                print("Spiel wird beendet.")
                """if Util.isRaspberry(): # if the game was beeing played on the Raspberry, it will show the following winning screens
                    YELLOW = (255, 255, 0)
                    RED = (255, 0, 0)
                    BLACK = (0, 0, 0)
                    WHITE = (255, 255, 255)
                    if gamestate == GameState.WON_RED.value: # winning screen for player red
                        SenseHat.clear(RED)
                        SenseHat.show_message("RED WINS", 0.1, BLACK, RED)
                    elif gamestate == GameState.WON_YELLOW.value: # winning screen for player yellow:
                        SenseHat.clear(YELLOW)
                        SenseHat.show_message("YELLOW WINS", 0.1, BLACK, YELLOW)
                    else: # draw screen
                        SenseHat.clear(BLACK)
                        SenseHat.show_message("DRAW", 0.1, BLACK, WHITE)"""
                break # exit the game loop
            
               
            elif gamestate == self._myturn: # check if it is this player's turn
                column_to_drop = self._player.play_turn()  # get the move of the player
                drop_state = self._game_logic.drop_token(self._mytoken, column_to_drop) # get the drop_state which states if move is valid
                if drop_state == DropState.DROP_OK.value: # if the drop_state is okay, calculate the gamestate
                    gamestate = self._game_logic.get_state()
                else:
                    print("Das hat nicht geklappt, versuch's noch einmal") # message if the move is not valid
                    continue # continue the game loop
            
            else: # wait for the other player to make a move if it is not this player's turn
                print("Warte auf deinen Mitspieler")
                time.sleep(1)



# start a local game
if __name__ == '__main__':
    coordinator = PlayerCoordinator()
    coordinator.run()
