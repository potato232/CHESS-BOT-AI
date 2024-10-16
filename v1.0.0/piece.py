from potato import *

__all__ = ["Piece"]

# white_pieces = ('♚', '♛', '♜', '♞', '♝', '♟')
# black_pieces = ('♔', '♕', '♖', '♘', '♗', '♙')

white_pieces = ('K', 'Q', 'R', 'H', 'B', 'P')
black_pieces = ('k', 'q', 'r', 'h', 'b', 'p')

skin = {
    KING: 0, QUEEN: 1, ROOK: 2, KNIGHT: 3, BISHOP: 4, PAWN: 5
}


class Piece:
    def __init__(self, color: str, type_: str, link: tuple):
        self.skin = white_pieces[skin[type_]] if color == WHITE else black_pieces[skin[type_]]

        self.color = color
        self.type = type_
        self.location = link
        self.isMove = False

    def move(self, link: tuple):
        self.location = link
        self.isMove = True

    def info(self):
        return (
            self.type,
            self.color,
            self.location,
            self.isMove,
        )

    def __repr__(self):
        return self.skin
