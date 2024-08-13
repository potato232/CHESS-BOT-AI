from datetime import datetime
from evaluation import *
from board import *
from move import *


__all__ = ["Engine"]
__author__ = 'potato 232'


class Engine:
    def __init__(self, b: Board):
        self.board: Board = b

        self.i1: tuple
        self.i2: tuple
        self.i3: tuple
        self.move = {}

        self.__potato__()

    def __potato__(self):
        self.i1 = board_info(self.board)
        self.i2 = move_generation(self.board, self.i1)
        self.i3 = move_filter(self.i2)

    def analysis(self, board: Board) -> float:
        self.board = board
        self.__potato__()

        number: float = 0.0

        number += (material(self.i1))
        number += (mobility(self.i3))
        number += (king_safety(self.i1, self.board))
        number += (potato_func_analysis(self.i1))

        self.move.update({self.board: number})

        return number


"""
def analysis(chess: Board) -> float:
    i1 = board_info(chess)
    i2 = move_generation(chess, i1)
    i3 = move_filter(i2)

    number: float = 0.0

    number += (material(i1))
    number += (mobility(i3))
    number += (king_safety(i1, chess))
    number += (potato_func_analysis(i1))

    return number
"""


# - test engine - #
def __test__() -> None:
    start = datetime.now()

    # - board - #
    chess = Board()
    chess.clean()

    chess.mov("E2", "E4")
    # chess.delete("E2")

    # - test engine - #

    # - display - #
    chess.display()

    print(datetime.now()-start)


if __name__ == '__main__':
    __test__()
