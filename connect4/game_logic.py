from game_token import GameToken
from drop_state import DropState
from game_logic_base import GameLogicBase
from game_state import GameState


class GameLogic(GameLogicBase):

    def __init__(self):
        super().__init__()
        self._game_state = GameState.TURN_RED #initial gamestate
        self._board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)] #initial board

    def drop_token(self, player: GameToken, column: int) -> DropState:
        # TODO überprüfen ob es der richtige player ist

        # check if the column is valid (0..6) => return the appropriate DropState
        if column not in range(0, 7):
            return DropState.COLUMN_INVALID

        # check if the column is full => return the appropriate DropState   
        if self._board[0][column] != GameToken.EMPTY:
            return DropState.COLUMN_FULL

        # insert token into board (column = column_to_drop) => return the appropriate DropState
        for i in range(5,-1,-1):
            if self._board[i][column] == GameToken.EMPTY:     
                self._board[i][column] = player
                self._game_state = self._calculate_state()
                return DropState.DROP_OK
        
    def get_state(self):
        print(f"gamelogic get gamestate {self._game_state}")
        return self._game_state
    
    def get_board(self):
        return self._board
    
    def _calculate_state(self):
        # check for a win horizontally, vertically or diagonally
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
        print("gamelogic calculate_self {self._game_state}")
        if self._game_state == GameState.TURN_RED:
            return GameState.TURN_YELLOW
        elif self._game_state == GameState.TURN_YELLOW:
            return GameState.TURN_RED