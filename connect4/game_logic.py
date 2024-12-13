from game_token import GameToken
from drop_state import DropState
from game_logic_base import GameLogicBase
from game_state import GameState


class GameLogic(GameLogicBase):
    """ 
    The GameLogic class represents the game logic for Connect Four. It is responsible for managing the game board, 
    checking for wins, draws, and updating the game state.

    Attributes:
    -----------
    _board (list): A 2D list representing the current state of the game board.
    _game_state (GameState): An enum value representing the current state of the game (e.g., WON_RED, WON_YELLOW, TURN_RED, TURN_YELLOW, DRAW).

    Methods:
    --------
    drop_token(player, column): Drops a token in the specified column on the game board.
    get_board(): Retrieves the current game board.
    get_state(): Retrieves the current game state.
    """

    def __init__(self):
        """
        Initializes the game logic with an empty board and sets the game state to the first player's turn.

        The constructor initializes the game board with all empty positions and sets the initial game state to
        GameState.TURN_RED to indicate that the player with the red token is the first player to make a move.
        
        Attributes:
        -----------
        _board (list): A 2D list representing the current state of the game board.
        _game_state (GameState): An enum value representing the current state of the game (e.g., WON_RED, WON_YELLOW, TURN_RED, TURN_YELLOW, DRAW).
        """
        super().__init__()
        self._game_state = GameState.TURN_RED #initial gamestate
        self._board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)] #initial board

    def drop_token(self, player: GameToken, column: int) -> DropState:
        """
        Drops a token in the specified column on the game board.

        Parameters:
        -----------
        player (GameToken): The token to drop, either RED or YELLOW.
        column (int): The column in which to drop the token, zero-indexed.

        Returns:
        -------
        DropState: The result of the drop operation, represented as a DropState enum value. 
        Returns None if an error occurs.
        """
        # check if the column is valid (0..6) => return the appropriate DropState
        if column not in range(0, 7): # invalid dropstate, if column out of range
            return DropState.COLUMN_INVALID

        # check if the column is full => return the appropriate DropState   
        if self._board[0][column] != GameToken.EMPTY: # column_full dropstate, if column is full
            return DropState.COLUMN_FULL

        # insert token into board (column = column_to_drop) => return the appropriate DropState
        for i in range(5,-1,-1):
            if self._board[i][column] == GameToken.EMPTY: # look for empty cell in chosen column     
                self._board[i][column] = player # insert token
                self._game_state = self._calculate_state() # update gamestate
                return DropState.DROP_OK # successful drop
        
    def get_state(self):
        """
        Retrieves the current game state.

        Returns:
        -------
        GameState: The current state of the game, represented as a GameState enum value.
        """
        return self._game_state
    
    def get_board(self):
        """
        Retrieves the current game board.

        Returns:
        -------
        list: The current state of the game board, represented as a 2D list of lists.
        """
        return self._board
    
    def _calculate_state(self):
        # check for a win horizontally, vertically or diagonally
        """
        Determines and updates the current state of the game based on the board configuration.

        This method evaluates the board to check if there is a winning condition (four consecutive tokens) 
        horizontally, vertically, or diagonally for either player. If such a condition is found, it updates 
        the game state to WON_RED or WON_YELLOW accordingly. If the board is full with no winner, it sets 
        the game state to DRAW. If neither condition is met, it switches the turn to the other player.

        Returns:
        -------
        GameState: The updated state of the game, indicating if a player has won, the game is a draw, or 
        whose turn it is next.
        """
        for row in range(6):
            for col in range(7):
                # skip empty cells
                if self._board[row][col] == GameToken.EMPTY:
                    continue
                directions = [(0,1), (-1,0), (-1,-1),  (-1,1)] #right, up, diagonal left, diagonal right
                current_token = self._board[row][col] #content of the current cell
                for di, dj in directions:
                    count = 1 # count the current token
                    for i in range(1,4): #check the next 3 tokens in each direction
                        if col + dj*i < 7:
                            if self._board[row+di*i][col+dj*i] == current_token: 
                                count +=1
                            else:
                                break
                    if count == 4: #set gamestate to won_red or won_yellow, if there are 4 consecutives tokens with the same colour
                        if current_token == GameToken.RED: 
                            return GameState.WON_RED
                        elif current_token == GameToken.YELLOW: 
                            return GameState.WON_YELLOW

        # if there is no empty cell in the board left and no one has won, the game is a draw
        if self._board[0].count(GameToken.EMPTY) == 0:
            return GameState.DRAW
        
        #return which players turn it is
        if self._game_state == GameState.TURN_RED:
            return GameState.TURN_YELLOW
        elif self._game_state == GameState.TURN_YELLOW:
            return GameState.TURN_RED