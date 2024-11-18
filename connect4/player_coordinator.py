from player_console import PlayerConsole
from game_token import GameToken
from game_state import GameState
from drop_state import DropState


class PlayerCoordinator:
    def __init__(self):
        # initialize players
        self._player_red = PlayerConsole(GameToken.RED)  # X
        self._player_yellow = PlayerConsole(GameToken.YELLOW)  # 0
        self._game_state = GameState.TURN_RED #initial gamestate
        self._board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]
        
    def drop_token(self, player: GameToken, column: int) -> DropState:
        # überprüfen ob es der richtige player ist

        # TODO check if the column is valid (0..6) => return the appropriate DropState
        if column not in range(0, 7):
            return DropState.COLUMN_INVALID

        # TODO check if the column is full => return the appropriate DropState   
        if self._board[0][column] != GameToken.EMPTY:
            return DropState.COLUMN_FULL

        # TODO insert token into board (column = column_to_drop)
        for i in range(5,-1,-1):
            if self._board[i][column] == GameToken.EMPTY:
                  
                self._board[i][column] = player
                self._game_state = self._calculate_state()
                
                return DropState.DROP_OK

    def get_state(self):
        return self._game_state
    
    def _end_game(self):
        gamestate = self.get_state()
        if gamestate == GameState.WON_RED:
            self._player_red.draw_board(self._board, gamestate)
            print("Rot hat das Spiel gewonnen!!")
        if gamestate == GameState.WON_YELLOW:
            self._player_yellow.draw_board(self._board, gamestate)
            print("Gelb hat das Spiel gewonnen!!")
        if gamestate == GameState.DRAW:
            self._player_yellow.draw_board(self._board, gamestate) 
            print("Unentschieden!!")

    def _calculate_state(self):
        # TODO check for a win horizontally, vertically or diagonally
        for row in range(6):
            for col in range(7):
                # skip empty cells
                if self._board[row][col] == GameToken.EMPTY:
                    continue
                directions = [(0,1), (-1,0), (-1,-1),  (-1,1)] #right, up, diagonal left, diagonal right
                current_token = self._board[row][col] #content of the current cell
                for di, dj in directions:
                    count = 1 # count the current token
                    #check the next 3 tokens in each direction
                    for i in range(1,4):
                        if self._board[row+di*i][col+dj*i] == current_token: 
                            count +=1
                        else:
                            break
                    if count == 4:
                        #set gamestate to won, if there are 4 consecutives tokens with the same colour
                        if current_token == GameToken.RED: 
                            return GameState.WON_RED
                        elif current_token == GameToken.YELLOW: 
                            return GameState.WON_YELLOW

        # TODO check if there is a draw
        if self._board[0].count(GameToken.EMPTY) == 0:
            return GameState.DRAW
        
        #TODO oder Spieler, der an der Reihe ist, zurückgeben
        if self._game_state == GameState.TURN_RED:
            return GameState.TURN_YELLOW
        elif self._game_state == GameState.TURN_YELLOW:
            return GameState.TURN_RED
        

    def run(self):
        # play game until won or draw
        while (True):

            self._player_red.draw_board(self._board, self._game_state)
            while(True):
                column_to_drop = self._player_red.play_turn()  # get the move of the player
                drop_state = self.drop_token(GameToken.RED, column_to_drop)
                if drop_state == DropState.DROP_OK:
                    if self._game_state == GameState.WON_RED or self._game_state == GameState.WON_YELLOW or self._game_state == GameState.DRAW:
                        self._end_game()
                        return
                    break
            
            self._player_yellow.draw_board(self._board, self._game_state)
            while(True):
                column_to_drop = self._player_yellow.play_turn()  # get the move of the player
                drop_state = self.drop_token(GameToken.YELLOW, column_to_drop)
                if drop_state == DropState.DROP_OK:
                    if drop_state == DropState.DROP_OK:
                        if self._game_state == GameState.WON_RED or self._game_state == GameState.WON_YELLOW or self._game_state == GameState.DRAW:  
                            self._end_game()
                            return 
                    break


# start a local game
if __name__ == '__main__':
    coordinator = PlayerCoordinator()
    coordinator.run()
