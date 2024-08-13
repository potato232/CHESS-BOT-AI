from datetime import datetime
from sys import stdout

from potato import *
from piece import *

__all__ = ["Board", "board_info", "copy_board"]
__author__ = 'potato 232'

__pw__ = (lambda _l_: Piece(PAWN, WHITE, _l_))  # (link: str) -> White Piece in link
__pb__ = (lambda _l_: Piece(PAWN, BLACK, _l_))  # (link: str) -> Black Piece in link


class Board:
    boardType = type(clean_board())

    def __init__(self) -> None:
        self.last_move: str = ''
        self.board = clean_board()
        self.__board__ = clean_board()

    def display(self) -> None:
        for i in self.board:
            stdout.write(f"{i}\n")
        stdout.write('\n')

    def clean(self) -> None:
        self.board = clean_board()

        for h in ((WHITE, 2), (BLACK, 7)):
            n = -1 if h[1] == 2 else 1
            for le in letters:
                self.add(Piece(PAWN, h[0], le+str(h[1])))

            for i in ((0, 1, 2), (-1, -2, -3)):
                i1, i2, i3 = i
                self.add(Piece(ROOK, h[0], f'{letters[i1]}{h[1]+n}'))
                self.add(Piece(KNIGHT, h[0], f'{letters[i2]}{h[1]+n}'))
                self.add(Piece(BISHOP, h[0], f'{letters[i3]}{h[1]+n}'))

            self.add(Piece(KING, h[0], f'E{h[1]+n}'))
            self.add(Piece(QUEEN, h[0], f'D{h[1]+n}'))

    def delete(self, location: str) -> None:
        l_ = get_location(location)
        self.board[l_[1]][l_[0]] = NOTING

    def add(self, piece_: Piece) -> None:
        l_ = get_location(piece_.location)
        self.board[l_[1]][l_[0]] = piece_
        self.__board__[l_[1]][l_[0]] = piece_.type

    def get(self, location: str):
        self.last_move = location
        l_ = get_location(location)
        return self.board[l_[1]][l_[0]]

    def mov(self, l2: str, l1: str) -> None:
        self.last_move = (l2, l1)
        l1, l2 = get_location(l1), get_location(l2)
        if self.board[l2[1]][l2[0]] != NOTING:
            self.board[l2[1]][l2[0]].move(get_location(l1))
        self.board[l1[1]][l1[0]] = self.board[l2[1]][l2[0]]
        self.board[l2[1]][l2[0]] = NOTING

        self.__board__[l1[1]][l1[0]] = self.__board__[l2[1]][l2[0]]
        self.__board__[l2[1]][l2[0]] = NOTING

    def out(self) -> boardType:
        return self.board

    def out_(self) -> boardType:
        return self.__board__

    def test(self):
        print(self.__board__)

        print('\n', clean_board())


def board_info(board: Board) -> tuple:
    # - get pieces - #

    # o1 = white pieces
    # o2 = black pieces

    o1, o2 = [], []

    for row in board.out():
        if row == [NOTING] * 8:
            continue

        for i in row:
            if i == NOTING:
                continue

            if i.color == WHITE:
                o1.append(i)
                continue
            o2.append(i)
    return tuple(o1), tuple(o2)


def copy_board(chess: Board) -> Board:
    """
    I cannot copy a list simply by typing (list2 = list1)
    because list2 will only be a reference to list1
    """

    board = Board()
    board.board, board.__board__ = list(board.board), list(board.__board__)

    for i in range(len(board.board)):
        board.board[i] = copy_list(chess.board[i])
        board.__board__[i] = copy_list(chess.__board__[i])

    board.board, board.__board__ = tuple(board.board), tuple(board.__board__)
    return board


# - test - #
def __test__() -> None:
    start = datetime.now()

    # - test Piece - #
    piece_test = Piece(PAWN, WHITE, "A2")

    piece_test.move('A4')
    piece_test.info()

    # - test Board - #
    board_test = Board()

    board_test.clean()

    board_test.delete("A1")
    board_test.add(Piece(PAWN, WHITE, "E5"))
    board_test.mov("D2", "D3")

    board_test.display()

    # - test board_info - #
    info1 = board_info(board_test)
    print(" - info 1 - \n", info1, '\n')

    # - #
    stdout.write(str(datetime.now()-start))


if __name__ == '__main__':
    __test__()
