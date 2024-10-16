from potato import *
from piece import Piece
from sys import stdout

__all__ = ["Board"]


CleanBoard = (lambda: (
    [EMPTY]*8, [EMPTY]*8, [EMPTY]*8, [EMPTY]*8,
    [EMPTY]*8, [EMPTY]*8, [EMPTY]*8, [EMPTY]*8,
))

EmptyRow = ([EMPTY]*8)


class Board:
    def __init__(self):
        self.board = CleanBoard()
        self.lastMove = ("", "")

    def copy_board(self):
        new_board = Board()
        new_board.board = tuple([copyList(i) for i in self.board])
        new_board.lastMove = self.lastMove
        return new_board

    def clear(self) -> None:
        self.board = CleanBoard()

    def push(self, piece, link) -> None:
        self.board[link[0]-1][link[1]-1] = piece

    def pop(self, link) -> None:
        self.board[link[0]-1][link[1]-1] = EMPTY

    def get(self, link):
        return self.board[link[0]-1][link[1]-1]

    def out(self) -> tuple:
        return self.board

    def move(self, l1, l2) -> None:
        piece: Piece = self.board[l1[0] - 1][l1[1] - 1]    # get piece
        if piece == EMPTY:
            raise Exception(f"Error: u can't move in {l1, l2}")

        piece.move(l2)
        self.board[l2[0] - 1][l2[1] - 1] = piece    # add piece to new link
        self.board[l1[0] - 1][l1[1] - 1] = EMPTY    # del piece in old link
        self.lastMove = (l1, l2)

    def display(self) -> None:
        stdout.write('    ')
        for w in ["A", "B", "C", "D", "E", "F", "G", "H"]:
            stdout.write(f'{w}, ')
        stdout.write('\n')

        for i in range(8):
            stdout.write(str(i+1)+' [ ')
            [stdout.write(f'{w}, ') for w in self.board[i]]
            stdout.write(']\n')

    def add_pieces(self) -> None:
        self.clear()

        for color, link, i in ((WHITE, 2, -1), (BLACK, 7, 1)):
            for hi in range(1, 9):
                self.push(Piece(color, PAWN, (link, hi)), (link, hi))

            self.push(Piece(color, ROOK, (link + i, 8)), (link + i, 8))
            self.push(Piece(color, ROOK, (link + i, 1)), (link + i, 1))

            self.push(Piece(color, KNIGHT, (link + i, 7)), (link + i, 7))
            self.push(Piece(color, KNIGHT, (link + i, 2)), (link + i, 2))

            self.push(Piece(color, BISHOP, (link + i, 6)), (link + i, 6))
            self.push(Piece(color, BISHOP, (link + i, 3)), (link + i, 3))

            self.push(Piece(color, QUEEN, (link + i, 4)), (link + i, 4))
            self.push(Piece(color, KING, (link + i, 5)), (link + i, 5))

    def get_pieces(self) -> tuple:
        # - get all pieces - #
        output = list()
        for row in self.board:
            if row == EmptyRow:
                continue

            for i in row:
                output.append(i) if i != EMPTY else ...
        return tuple(output)

    def white_pieces(self):
        # - get white pieces - #
        output = list()

        for row in self.board:
            if row == EmptyRow:
                continue

            for i in row:
                if i == EMPTY:
                    continue

                if i.color == WHITE:
                    output.append(i)

        return tuple(output)

    def black_pieces(self):
        # - get black pieces - #
        output = list()
        for row in self.board:
            if row == EmptyRow:
                continue

            for i in row:
                if i == EMPTY:
                    continue
                output.append(i) if i.color == BLACK else ...
        return tuple(output)


def __test__():
    test_board = Board()

    p1, p2, p3 = (
        Piece(WHITE, PAWN, (2, 2)),
        Piece(WHITE, PAWN, (5, 2)),
        Piece(WHITE, PAWN, (3, 2))
    )

    # - - - #

    test_board.push(p1, (2, 2))
    test_board.push(p2, (5, 2))
    test_board.push(p3, (3, 2))

    test_board.pop((5, 2))

    test_board.move((3, 2), (4, 2))

    test_board.add_pieces()
    test_board.display()

    # piece_list = test_board.get_pieces()
    # print(piece_list)


if __name__ == '__main__':
    __test__()
