from game_logic import GameLogicBase
from game_state import GameState
from drop_state import DropState
from game_token import GameToken
import requests

class GameLogicClient(GameLogicBase):
    """
    A client for interacting with the game logic server over a REST API.

    This class enables the player coordinator to retrieve game state, game board, 
    and execute moves in a distributed game setup.

    Attributes:
    -----------
    _url (str): The base URL of the game logic server.

    Methods:
    -----------
    get_board(): Retrieves the current game board from the game logic server.
    get_state(): Retrieves the current game state from the game logic server.
    drop_token(player, column): Drops a token in the specified column on the game board.
    """

    def __init__(self, host):
        """
        Initialize the GameLogicClient with the given server host address.

        The constructor sets up the client by constructing the base URL for API requests.
        This URL is used to communicate with the game logic server.

        Parameters:
        -----------
        host (str): The IP address or hostname of the server hosting the game logic API.
        """
        
        super().__init__()
        print( f"GameLogicClient initialized with host {host}" )
        self._url = f'http://{host}:5000/api'

    def get_board(self) -> list:
        """
        Retrieve the current game board from the game logic server.

        The game board is represented as a 2D list, where each element indicates
        the state of a cell (empty, red, or yellow).

        Returns:
        -------
        list: The current state of the game board, represented as a list of lists.
        """
        
        # call remote API
        response = requests.get( f"{self._url}/board")
        # return result to locall caller
        return response.json().get("board")

    def get_state(self) -> GameState:
        """
        Retrieve the current game state from the game logic server.

        The game state indicates whether it is a player's turn, or if the game 
        has ended in a win or draw.

        Returns:
        -------
        GameState: The current state of the game, represented as a GameState enum value. Returns None
        if an error occurs.
        """

        try:
            # call remote API
            response = requests.get( f"{self._url}/state")
            # return result to local caller
            return response.json().get("game_state")
        except requests.exceptions.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            return None
        except Exception as e:
            print(f"Error in get_state: {e}")
            return None

    def drop_token(self, player, column) -> DropState:

        """
        Drop a token in the specified column on the game board.

        This method sends a request to the server to place a token in the given column 
        and returns the result of the operation.

        Parameters:
        -----------
        player (GameToken): The token to drop, either 'X' or 'Y'.
        column (int): The column in which to drop the token, zero-indexed.

        Returns:
        -------
        DropState: The result of the drop operation, represented as a DropState enum value. 
        Returns None if an error occurs.
        """

        post_drop = { "player_id": player.value, "column": column}

        try:        
            response = requests.post( f"{self._url}/drop", json=post_drop)
            return response.json().get("drop_state")
        except requests.exceptions.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            return None
        except Exception as e:
            print(f"Error in get_state: {e}")
            return None
        


if __name__ == '__main__':
    """
    Test programm to manually check if GameLogicClient is working.
    Limitations:
    - Implements both players at once--no distributed gameplay possible
    - Does not handle errors
    - Does not handle end of game gracefully
    """
    # local function
    def draw_board( board: list, state: GameState) -> None:
        print("0|1|2|3|4|5|6")
        for row in board:
            print('|'.join(row))
        print( f"GameState: {state}" )

    client = GameLogicClient("127.0.0.1")
    
    while( True ):
        game_state = client.get_state()
        board = client.get_board()

        draw_board(board, game_state)

        if game_state == GameState.TURN_RED.value or  game_state == GameState.TURN_YELLOW.value:
            player = GameToken.RED if game_state == 0 else GameToken.YELLOW
            print( f"It is {player}'s turn" )  
            column = int(input("Which colum to drop? "))    
            drop_state = client.drop_token( player, column )
            print( "drop_state:", drop_state )
        else: break # bail out if its neither RED's nor YELLOW's turn, i.e. WON or DRAW
    
    print("Game Over")
