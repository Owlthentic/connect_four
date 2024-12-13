from input_console import InputConsole
from display_console import DisplayConsole
from player_base import PlayerBase
from game_state import GameState
from game_token import GameToken
from ansi import Ansi
from input_base import Keys


class PlayerConsole(PlayerBase):
    """
    This class is responsible for displaying the game board on the console, tracking the player's moves,
    and showing the result of the game (winner or draw).

    It uses the `DisplayConsole` to manage the board's visual representation and the `InputConsole` to handle 
    player input. It also includes logic to determine and display the current player and the game result.
    
    
    Attributes:
    -----------
    display_console (DisplayConsole): Handles the drawing and updating of the game board on the console. 
    _input (InputConsole): Handles the key inputs for the console.
    _basecolor (int): basecolor for console text
    _player_color (int): The player's token (color: Red or Yellow), used for marking the player's moves.

    Methods:
    --------
    __init__(self, player: GameToken): Initializes the player with a specific token and sets up the console for display and input.
    draw_board(self, board: list, gamestate: GameState): Displays the game board and updates the player and game state information on the console.
    play_turn(self) -> int: Handles the player's turn, allowing them to select a column to drop their token.
    select_column(self) -> int: Tracks the player's cursor movements and returns the selected column index.

    """
    def __init__(self, player: GameToken): 
        """
        Initializes the player with a specific token and sets up console input and display.

        Parameters:
        -----------
        player (GameToken): The token representing the player (e.g., RED or YELLOW).

        This method configures the console display and input handler for the player. 
        It assigns a specific color to the player token for display purposes 
        (Red = 1, Yellow = 3, Neutral = 2) and sets a default base color for the console text.
        """

        super().__init__(player)
        self.display_console = DisplayConsole() # initialize display
        self._input = InputConsole() # initialize key input
        
        self._base_color = 0 #color for?
        if player == GameToken.RED: # initialize player color red
            self._player_color = 1 
        elif player == GameToken.YELLOW: # initialize player color yellow
            self._player_color = 3
        else:
            self._player_color = 2 # define a neutral player color


    def draw_board(self, board:list, gamestate:GameState):
        """
        Draws the current state of the game board on the console.

        This method displays the board grid and places the appropriate tokens (RED or YELLOW)
        on the grid based on the `board` parameter. It also provides feedback on the console
        regarding the current game state, indicating whose turn it is or announcing the winner
        if the game has concluded.

        Parameters:
        -----------
        
        - board (list): A 2D list representing the game board, with each cell containing a
        GameToken indicating the presence of a RED or YELLOW token, or an empty space.
        - gamestate (GameState): The current state of the game, which determines whose turn
        it is or if a player has won or if the game is a draw.

        The method uses ANSI escape codes to set foreground colors for the console output,
        ensuring that the game board and status messages are displayed in color.
        """
        self.display_console.draw_grid() # draw the grid of the board

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
        
        if gamestate == 0: # turn red
            Ansi.set_foreground(self._base_color, False)
            print("Es ist der Zug von ", end="")
            Ansi.set_foreground(1, False)
            print("Rot")
        elif gamestate == 1: # turn yellow
            Ansi.set_foreground(self._base_color, False)
            print("Es ist der Zug von ", end="")
            Ansi.set_foreground(3, False)
            print("Gelb")
        elif gamestate == 2: # won red
            Ansi.set_foreground(1, False)
            print("Rot hat gewonnen!!")
            Ansi.set_foreground(self._base_color, False)
        elif gamestate == 3: # won yellow
            Ansi.set_foreground(3, False)
            print("Gelb hat gewonnen!!")
            Ansi.set_foreground(self._base_color, False)   
        elif gamestate == 4: # draw
            Ansi.set_foreground(self._base_color, False)
            print("Unentschieden...")
            Ansi.set_foreground(self._base_color, False)

        Ansi.set_foreground(self._base_color, False) # reset color

    def play_turn(self) -> int:
        """
        Executes the player's turn by allowing them to select a column.

        Returns:
        --------
        int: The column index chosen by the player to drop their token.

        This method:
        - Displays the player's cursor on the board.
        - Waits for the player to select a column using keyboard input.
        - Resets the console color to the default after input.
        """

        Ansi.set_foreground( self._player_color, False)
        pos = self.select_column()

        Ansi.set_foreground(self._base_color, False)
        return pos

    def select_column(self):

        """
        Tracks the player's cursor movements and returns the selected column index.

        This method displays a cursor on the game board, allowing the player to move 
        it using the keyboard. The following keys are supported:
        
        - LEFT: Move the cursor one position to the left (if possible).
        - RIGHT: Move the cursor one position to the right (if possible).
        - ENTER or DOWN: Confirms the selected column index and returns it.
        - ESC: Aborts the input (for debugging purposes).

        Returns:
        --------
        int: The column index where the player wants to drop their token.
        """

        pos = 3
        key_pressed = Keys.UNKNOWN
        while key_pressed != Keys.ESC:
            self.display_console.draw_input(pos) # draw current position of the player
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



