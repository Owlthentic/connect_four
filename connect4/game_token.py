from enum import StrEnum


class GameToken(StrEnum):
    """
    Enum class representing the two different game tokens.
    """
    EMPTY = ' '     # An empty token (placeholder)
    RED = 'X'       # Token for the red player
    YELLOW = '0'    # Token for the yellow player


if __name__ == '__main__':
    t = GameToken.RED
    st = str(t)
    print(f"GameToken {t}, Type: {type(t)}, Value: {t.value}, Type of Value: {type(t.value)}")
    print(f"GameToken {st}, Type: {type(st)}")
