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
        try:
            # call remote API
            response = requests.get( f"{self._url}/state")
            print(f"Response Text: {response.text}, Response Status Code: {response.status_code}")  
            # return result to local caller
            return response.json().get("game_state")
        except requests.exceptions.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            return None
        except Exception as e:
            print(f"Error in get_state: {e}")
            return None

    def drop_token(self, player, column) -> DropState:
        # post to remote API
        post_drop = { "player_id": player.value, "column": column}
        print(f"Post Data {post_drop}")
        try:        
            response = requests.post( f"{self._url}/drop", json=post_drop)
            print(f"Response Text: {response.text}, Response Status Code: {response.status_code}") 
            return response.json().get("drop_state")
        except requests.exceptions.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            return None
        except Exception as e:
            print(f"Error in get_state: {e}")
            return None
        
    def reset_board(self):
        # Setzt das Spielfeld zurück, indem alle Zellen auf None gesetzt werden
        self.board = [[' ' for _ in range(7)] for _ in range(6)]  # Leere Zellen
        return True  # Gibt zurück, dass das Zurücksetzen erfolgreich war


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
