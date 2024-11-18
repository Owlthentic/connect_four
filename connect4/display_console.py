from ansi import Ansi
from game_token import GameToken
from display_base import DisplayBase


class DisplayConsole(DisplayBase):
    pass


"""
┌
┐
└
┘
├
┤
┼
─
│
┬
┴
█ 

https://de.wikipedia.org/wiki/Unicodeblock_Rahmenzeichnung
"""


if __name__ == '__main__':
    Ansi.clear_screen()
    Ansi.reset()
    fc = DisplayConsole()
    fc.draw_grid()
    fc.draw_token(0, 0, GameToken.RED)
    fc.draw_token(5, 2, GameToken.YELLOW)
    Ansi.gotoXY(1, 20)
    print(type(GameToken.RED))
    print(GameToken.RED)
