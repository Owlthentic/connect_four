import random
from player_base import PlayerBase
from game_token import GameToken
from game_state import GameState
from drop_state import DropState

class BotPlayer(PlayerBase):
    def __init__(self, player: GameToken):
        super().__init__(player)

    def play_turn(self, board: list) -> int:
        """
        Wählt eine zufällige Spalte aus, die nicht voll ist.
        """
        valid_columns = [col for col in range(7) if board[0][col] == GameToken.EMPTY]
        if not valid_columns:
            raise Exception("Keine gültigen Spalten verfügbar!")
        return random.choice(valid_columns)

# Integration in den PlayerCoordinator
if __name__ == "__main__":
    from player_console import PlayerConsole
    from player_coordinator import PlayerCoordinator

    class PlayerCoordinatorWithBot(PlayerCoordinator):
        def __init__(self):
            super().__init__()
            self._player_yellow = BotPlayer(GameToken.YELLOW)  # Gelber Spieler wird zum Bot

        def run(self):
            while True:
                self._player_red.draw_board(self._board, self._state)
                column_to_drop = self._player_red.play_turn()  # Spieler rot wählt Spalte
                drop_state = self.drop_token(GameToken.RED, column_to_drop)
                if drop_state != DropState.DROP_OK:
                    print("Ungültiger Zug, bitte erneut versuchen.")
                    continue

                self._player_yellow.draw_board(self._board, self._state)
                column_to_drop = self._player_yellow.play_turn(self._board)  # Bot wählt Spalte
                drop_state = self.drop_token(GameToken.YELLOW, column_to_drop)
                if drop_state != DropState.DROP_OK:
                    print("Bot hat eine ungültige Spalte gewählt. Dies sollte nicht passieren.")
                    continue

    coordinator = PlayerCoordinatorWithBot()
    coordinator.run()
