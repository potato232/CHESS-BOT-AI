from datetime import datetime
from sys import stdout
from potato import *

__all__ = ["Board", "Piece"]
__author__ = 'potato 232'


class Piece:
    def __init__(self, _type_, _color_, location) -> None:
        piece = {KING: 0, QUEEN: 1, ROOK: 2, KNIGHT: 3, BISHOP: 4, PAWN: 5}
        self.skin = white_pieces[piece[_type_]] if (_color_ == WHITE) else black_pieces[piece[_type_]]

        self.type, self.color = _type_, _color_
        self.location = location
        self.is_move = False

        self.last_move = ''

    def move(self, location: str) -> None:
        self.last_move = self.location
        self.location = location
        self.is_move = True

    def info(self) -> tuple:
        output = (self.type, self.color, self.location, self.is_move)
        return output

    def __repr__(self) -> str:
        return f"{self.skin}"


def __pw__(_l_: str) -> Piece:
    return Piece(PAWN, WHITE, _l_)


def __pb__(_l_: str) -> Piece:
    return Piece(PAWN, BLACK, _l_)


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


# - test Board & Piece - #
def __test__() -> None:
    start = datetime.now()

    # - test Piece - #
    _test_1 = Piece(PAWN, WHITE, "A2")
    _test_1.move('A4')
    _test_1.info()

    # - test Board - #
    _test_2 = Board()
    _test_2.clean()
    _test_2.delete("A1")
    _test_2.add(Piece(PAWN, WHITE, "E5"))
    _test_2.mov("D2", "D3")

    _test_2.display()

    # - #
    print(datetime.now()-start)


if __name__ == '__main__':
    __test__()
