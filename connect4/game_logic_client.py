from game_logic import GameLogicBase
from game_state import GameState
from drop_state import DropState
from game_token import GameToken
import requests

class GameLogicClient(GameLogicBase):

    def __init__(self, host):
        super().__init__()
        print( f"GameLogicClient initialized with host {host}" )
        self._url = f'http://{host}:5000/api'

    def get_board(self) -> list:
        # call remote API
        response = requests.get( f"{self._url}/board")
        # return result to locall caller
        return response.json().get("board")

    def get_state(self) -> GameState:
        # IMPLEMENT METHOD HERE!
        return GameState.TURN_RED

    def drop_token(self, player, column) -> DropState:
        # IMPLEMENT METHOD HERE
        return DropState.DROP_OK


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

        draw_board( board, game_state )

        if game_state == GameState.TURN_RED or  game_state == GameState.TURN_YELLOW:
            player = GameToken.RED if game_state == GameState.TURN_RED else GameToken.YELLOW  
            column = int(input("Which colum to drop? "))    
            drop_state = client.drop_token( player, column )
            print( "drop_state:", drop_state )
        else: break # bail out if its neither RED's nor YELLOW's turn, i.e. WON or DRAW
    
    print("Game Over")
