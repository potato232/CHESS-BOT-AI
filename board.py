import sys

# - ♚ ♛ ♝ ♞ ♜ ♟- #
# - ♔ ♕ ♖ ♘ ♗ ♙ - #

__all__ = ['KING', 'QUEEN', 'ROOK', 'BISHOP', 'KNIGHT', 'PAWN', 'NOTING',
           'CleanBoard', 'WHITE', 'BLACK', 'Board', 'Piece',
           'location_1', 'location_2']

KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN, NOTING = ('King', 'Queen', 'Rook', 'Bishop', 'Knight', 'Pawn', '')
WHITE, BLACK = 'white', 'black'

CleanBoard = ([NOTING] * 8, [NOTING] * 8, [NOTING] * 8, [NOTING] * 8,
              [NOTING] * 8, [NOTING] * 8, [NOTING] * 8, [NOTING] * 8,)

power = {QUEEN: 8, ROOK: 5, BISHOP: 4, KNIGHT: 3, PAWN: 1, KING: 0}
piece = {KING: 0, QUEEN: 1, ROOK: 2, KNIGHT: 3, BISHOP: 4, PAWN: 5}

white_pieces = ('♚', '♛', '♜', '♞ ', '♝', '♟')
black_pieces = ('♔', '♕', '♖', '♘ ', '♗ ', '♙')

char = {'A': 0, 'B': 1, 'C': 2, 'D': 3,
        'E': 4, 'F': 5, 'G': 6, 'H': 7}


def location_1(link: str) -> tuple:
    x, y = link
    return char.get(x), int(y) - 1


def location_2(link: tuple) -> str:
    try:
        x, y = link
        return f"{'ABCDEFGH'[x]}{y}"
    except IndexError:
        pass
    return ''


class Board:
    def __init__(self):
        self.board = CleanBoard
        self.LastMovW, self.LastMovB = ('', '')

    def get(self, link):
        try:
            return self.board[int(link[1])-1][char.get(link[0])]
        except AttributeError:
            return NOTING

    def add(self, potato):
        link = potato.link
        self.board[link[1]][link[0]] = potato

    def mov(self, old_link: str, new_link: str):
        p = self.get(old_link)
        if p.color == WHITE:
            self.LastMovW = (old_link, new_link)
        else:
            self.LastMovB = (old_link, new_link)
        p.mov(new_link)

        self.board[int(new_link[1])-1][char.get(new_link[0])] = p
        self.board[int(old_link[1])-1][char.get(old_link[0])] = NOTING

    def prt(self):
        for row in self.board:
            sys.stdout.write(str(row)+'\n')
        sys.stdout.write('\n')

    def clr(self):
        self.board = CleanBoard
        for data in ((WHITE, 1, 1), (BLACK, 8, -1)):
            color, n1, n2 = data[0], data[1], data[2]
            for c in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',):
                self.add(Piece(PAWN, color, f'{c}{n1 + n2}'))
            potato = (Piece(ROOK, color, f'A{n1}'), Piece(ROOK, color, f'H{n1}'),
                      Piece(BISHOP, color, f'F{n1}'), Piece(BISHOP, color, f'C{n1}'),
                      Piece(KNIGHT, color, f'G{n1}'), Piece(KNIGHT, color, f'B{n1}'),
                      Piece(QUEEN, color, f'D{n1}'), Piece(KING, color, f'E{n1}'))
            for p in potato:
                self.add(p)

    def out(self):
        return self.board


class Piece:
    def __init__(self, type_, color, link):
        self.skin = (white_pieces if color == WHITE else black_pieces if color == BLACK else '')[piece[type_]]
        self.color, self.type, self.move = color, type_, False
        self.link = location_1(link)

    def mov(self, link):
        self.link = location_1(link)
        self.move = True

    def __repr__(self):
        return self.skin


# - test - #
if __name__ == '__main__':
    from datetime import datetime
    start = datetime.now()

    chess = Board()
    chess.clr()
    chess.mov('E2', 'E4')
    chess.prt()

    _end_ = datetime.now()
    print(_end_-start)
