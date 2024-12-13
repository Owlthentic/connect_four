from player_console import PlayerConsole

from game_token import GameToken
from game_state import GameState
from drop_state import DropState
from game_logic_client import GameLogicClient
from ansi import Ansi
import time
from util import Util



class PlayerCoordinator:
    """
    This class coordinates the game, setting up the player, starting the game, and managing the game state.
    
    It allows a player to connect to the game server, start the game, and manage the ongoing game. 
    It handles communication between the client (the player) and the server, tracks the current game state, 
    and ensures the game is displayed correctly based on the chosen display mode (console or SenseHat).
    
    Attributes:
    -----------
    _current_player (Player): The player currently taking their turn. This is set during setup.
    _player (Player): The player object that handles player input (either on the console or SenseHat).
    _myturn (int): The state indicating whether it is the player's turn to play (as defined by GameState).
    _mytoken (GameToken): The player's token (color: Red or Yellow), used for marking the player's moves.
    _game_logic (GameLogicClient): The client that communicates with the game server to retrieve the game state.
    _board (list): The current game board retrieved from the game server.
    _color (str): The color chosen by the player (Red or Yellow).
    _display (str): The display mode (console or SenseHat) selected by the player.
    raspi_name (str): The IP address of the Raspberry Pi (server) hosting the game logic.

    Methods:
    --------
    __init__(self): Initializes the game and the player.
    __setup__(self): Configures the game and player settings.
    run(self): Runs the game loop, managing the flow of the game.
    """
    def __init__(self):
        """
        Initializes the game and the player, establishes a connection to the server, and loads the game board.
        
        The constructor prompts the user for the IP address of the server hosting the game logic. 
        It then connects to the GameLogicClient, retrieves the current game board, and prepares the game for the player. 
        Player settings such as color and game display options are configured later during the setup phase.
        
        - Prompts the user for the IP address of the game server to establish a connection.
        - Initializes the GameLogicClient with the provided server IP and retrieves the game board.
        
        Attributes:
        -----------
        _current_player (None): Placeholder for the player who will start the game.
        _player (None): Placeholder for the player object that handles player input (on console or SenseHat).
        _myturn (None): Placeholder to track if it's the player's turn.
        _mytoken (None): Placeholder to track the player's color token (Red or Yellow).
        _game_logic (GameLogicClient): The client used to interact with the server.
        _board (list): The game board fetched from the server.

        Methods:
        --------
        __init__(self): Initializes the game and the player.
        __setup__(self): Configures the game and player settings.
        run(self): Runs the game loop, managing the flow of the game.
        """
        self._first_player = None # used to make sure the first player is red
        self._player = None # used to initialize the player on this console or sensehat
        self._myturn = None # used to track if it's this player's turn
        self._mytoken = None # used to track the player's color

        raspi_name = input("Gib die IP deines Servers an: ")
        self._game_logic = GameLogicClient(raspi_name)
        self._board = self._game_logic.get_board() #get board
    
    def __setup__(self):
        """
        Sets up the game by allowing the player to choose their color, the display mode (console or SenseHat), 
        and determines the first player (Red).
        
        This method configures the player by asking them to choose their color and display mode. 
        It ensures that the Red player is set as the first player. The player is also prompted to choose 
        whether to play on the console or the SenseHat.
        
        - Prompts the user to select their player color (Red or Yellow) and sets the player's token.
        - Determines whether the game will be played on the console or on the SenseHat.
        - Ensures the Red player is set as the first player.
        
        Attributes:
        -----------
        _color (str): The color selected by the player.
        _myturn (int): The GameState value indicating if it's the player's turn.
        _mytoken (GameToken): The token representing the player's color.
        _display (str): The display mode selected (console or SenseHat).
        _player (Player): The player object handling input on the selected display.
        """
        self._color = input("Was ist deine Spielerfarbe? Rot (r) oder Gelb (g)? ")
        if self._color.lower() == "r": # initialize player if red was chosen
            self._myturn = GameState.TURN_RED.value
            self._mytoken = GameToken.RED
            print("Du bist Rot")
        
        elif self._color.lower() == "g": # initialize player if yellow was chosen
            self._myturn = 1
            self._mytoken = GameToken.YELLOW
            print("Du bist Gelb")
        
        else:   # catch invalid input and restart setup
            print("Falsche Eingabe")
            self.__setup__()
        
        
        if Util.isRaspberry(): # check if the game is played on the Raspberry
            from player_sense import PlayerSense
            self._display = input("Wo spielst du? Auf Konsole (c) oder dem SenseHat (s)? ") # Let the player choose if the game is played on the console or on the SenseHat
            
            if self._display == "c":
                self._player = PlayerConsole(self._mytoken) # initialize Player on Console
            
            elif self._display == "s":
                self._player = PlayerSense(self._mytoken) # initialize Player on SenseHat
            
            else:
                print("Falsche Eingabe")
                self.__setup__()
        else:
            self._player = PlayerConsole(self._mytoken)
        
        if self._mytoken == GameToken.RED: # make sure player red starts first
                self._first_player = self._player



    def run(self):
        """
        Runs the main game loop, continuously checking the game state and allowing the player to make a move 
        or waiting for the opponent to play. Exits when the game is won or a draw occurs.
        
        This method contains the core game logic, executing in a loop to manage the flow of the game. It checks 
        the game state regularly, displays the current game board, and waits for the player to make a move. 
        The game ends when either a player wins or the game results in a draw.
        
        - Retrieves the current game state and updates the game board.
        - Displays the current board.
        - Ends the game if a winner is found or a draw occurs.
        - Prompts the player to make a move if it's their turn, or waits for the opponent's move if it's not.
        
        Attributes:
        -----------
        gamestate (enum): The current state of the game (won, draw, or ongoing).
        """
        self.__setup__()
        if Util.isRaspberry(): # checking, if the game is played on the Raspberry
            from player_sense import PlayerSense # Import the PlayerSense class from the player_sense module
    
        while (True):  
            gamestate = self._game_logic.get_state() # get the current game state
            self._player.draw_board(self._game_logic.get_board(), self._game_logic.get_state()) # draw the board

            """
            1. Check for a win or a draw and ends the game when the game is won or drawn
            2. Ask the player to make a move, when it is his turn 
            3. Waits for the other player's move.
            """ 
            if gamestate == GameState.WON_RED.value or gamestate == GameState.WON_YELLOW.value or gamestate == GameState.DRAW.value:
                next_turn = input("Noch eine Runde? (j/n)")
                if next_turn == "j":
                    self._game_logic.reset_board()
                    if Util.isRaspberry():
                        from sense_hat import SenseHat
                        sense = SenseHat()
                        sense.clear()
                    continue
                else:
                    print("Spiel wird beendet.")
                    self._game_logic.reset_board()
                    
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
