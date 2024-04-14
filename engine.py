from board import *
from math_ import *
from move import *
import datetime
import sys

CleanBoard = ([NOTING] * 8, [NOTING] * 8, [NOTING] * 8, [NOTING] * 8,
              [NOTING] * 8, [NOTING] * 8, [NOTING] * 8, [NOTING] * 8,)

power = {QUEEN: 8, ROOK: 5, BISHOP: 4, KNIGHT: 3, PAWN: 1, KING: 0}
piece = {KING: 0, QUEEN: 1, ROOK: 2, KNIGHT: 3, BISHOP: 4, PAWN: 5}

white_pieces = ('♚', '♛', '♜', '♞ ', '♝', '♟')
black_pieces = ('♔', '♕', '♖', '♘ ', '♗ ', '♙')

char = {'A': 0, 'B': 1, 'C': 2, 'D': 3,
        'E': 4, 'F': 5, 'G': 6, 'H': 7}


def __move__(obj: tuple, chess: Board, info: tuple) -> tuple:
    if obj[0] == KING:
        return __king__(obj, chess, info)[0]

    p1, p2 = {WHITE: (info[0], info[1]), BLACK: (info[1], info[0])}[obj[1]]
    l1, l2 = tuple(i[-1] for i in p1), tuple(i[-1] for i in p2)
    if obj[0] == QUEEN:
        out = list()

        for row in queen:
            for v1, v2 in row:
                v1, v2 = v1+obj[-1][0], v2+obj[-1][1]
                if not ((v1 > -1) and (v1 < 8) and (v2 > -1) and (v2 < 8)):
                    continue
                if (v1, v2) in l1:
                    break
                if (v1, v2) in l2:
                    out.append(location_2((v1, v2 + 1)))
                    break
                out.append(location_2((v1, v2+1)))

        return tuple(out)

    if obj[0] == ROOK:
        out = list()
        for row in rook:
            for v1, v2 in row:
                v1, v2 = v1 + obj[-1][0], v2 + obj[-1][1]
                if not ((v1 > -1) and (v1 < 8) and (v2 > -1) and (v2 < 8)):
                    continue
                if (v1, v2) in l1:
                    break
                if (v1, v2) in l2:
                    out.append(location_2((v1, v2 + 1)))
                    break
                out.append(location_2((v1, v2 + 1)))
        return tuple(out)

    if obj[0] == BISHOP:
        out = list()
        for row in bishop:
            for v1, v2 in row:
                v1, v2 = v1 + obj[-1][0], v2 + obj[-1][1]
                if not ((v1 > -1) and (v1 < 8) and (v2 > -1) and (v2 < 8)):
                    continue
                if (v1, v2) in l1:
                    break
                if (v1, v2) in l2:
                    out.append(location_2((v1, v2 + 1)))
                    break
                out.append(location_2((v1, v2 + 1)))
        return tuple(out)

    if obj[0] == KNIGHT:
        out = list()
        for row in knight:
            for v1, v2 in row:
                v1, v2 = v1 + obj[-1][0], v2 + obj[-1][1]
                if not ((v1 > -1) and (v1 < 8) and (v2 > -1) and (v2 < 8)):
                    continue
                if (v1, v2) in l1:
                    break
                if (v1, v2) in l2:
                    out.append(location_2((v1, v2 + 1)))
                    break
                out.append(location_2((v1, v2 + 1)))
        return tuple(out)

    if obj[0] == PAWN:
        out = list()

        move, attack = pawn_b, pawn_attack_b
        if obj[1] == WHITE:
            move, attack = pawn_w, pawn_attack_w

        for v1, v2 in attack:
            v1, v2 = v1 + obj[-1][0], v2 + obj[-1][1]
            if not ((v1 > -1) and (v1 < 8) and (v2 > -1) and (v2 < 8)):
                continue
            if (v1, v2) in l2:
                out.append(location_2((v1, v2)))

        r = 0
        for v1, v2 in move:
            if r == 1:
                if obj[2]:
                    break
            v1, v2 = v1+obj[-1][0], v2+obj[-1][1]

            if not ((v1 > -1) and (v1 < 8) and (v2 > -1) and (v2 < 8)):
                break
            if (v1, v2) in l1:
                break
            if (v1, v2) in l2:
                break

            out.append(location_2((v1, v2+1)))
            r += 1

        return tuple(out)


def __def__(link: tuple, chess: Board, info: tuple, color: str) -> bool:
    p1, p2, l1, l2 = info
    x, y = link

    pawn_attack = {WHITE: ((-1, -1), (+1, -1),),
                   BLACK: ((+1, +1), (-1, +1),)}[color]

    for row in rook:
        for v in row:
            v = v[0]+x, v[1]+y
            if not ((v[0] > -1) and (v[0] < 9) and (v[1] > -1) and (v[1] < 9)):
                break
            if (v[0], v[1]) in l1:
                break
            if (v[0], v[1]) in l2:
                p = __info__(chess.get(location_2((v[0], v[1]+1))))
                if p[0] == QUEEN:
                    return True
                if p[0] == ROOK:
                    return True
                break

    for row in bishop:
        for v in row:
            v = v[0] + x, v[1] + y
            if not ((v[0] > -1) and (v[0] < 9) and (v[1] > -1) and (v[1] < 9)):
                break
            if (v[0], v[1]) in l1:
                break
            if (v[0], v[1]) in l2:
                p = __info__(chess.get(location_2((v[0], v[1] + 1))))
                if p[0] == QUEEN:
                    return True
                if p[0] == BISHOP:
                    return True
                break

    for row in knight:
        for v in row:
            v = v[0] + x, v[1] + y
            if not ((v[0] > -1) and (v[0] < 9) and (v[1] > -1) and (v[1] < 9)):
                break
            if (v[0], v[1]) in l1:
                break
            if (v[0], v[1]) in l2:
                p = __info__(chess.get(location_2((v[0], v[1] + 1))))
                if p[0] == KNIGHT:
                    return True
                break

    for row in king:
        for v in row:
            v = v[0] + x, v[1] + y
            if not ((v[0] > -1) and (v[0] < 9) and (v[1] > -1) and (v[1] < 9)):
                break
            if (v[0], v[1]) in l1:
                break
            if (v[0], v[1]) in l2:
                p = __info__(chess.get(location_2((v[0], v[1] + 1))))
                if p[0] == KING:
                    return True
                break

    for v in pawn_attack:
        v = v[0] + x, v[1] + y
        if not ((v[0] > -1) and (v[0] < 9) and (v[1] > -1) and (v[1] < 9)):
            break
        if (v[0], v[1]) in l1:
            break
        if (v[0], v[1]) in l2:
            p = __info__(chess.get(location_2((v[0], v[1] + 1))))
            if p[0] == PAWN:
                return True
            break

    return False


def __king__(obj: tuple, chess: Board, info: tuple) -> tuple:
    # obj = type0, color1, is_move?2, link3(-1) #

    p1, p2 = info[1], info[0]
    if obj == WHITE:
        p1, p2 = (info[0], info[1])

    l1 = tuple(i[-1] for i in p1)
    l2 = tuple(i[-1] for i in p2)

    out = list()
    for i in king:
        x, y = i[0][0]+obj[-1][0], i[0][1]+obj[-1][1]

        if not ((x > -1) and (x < 8) and (y > -1) and (y < 8)):
            continue

        if (x, y) in l1:
            continue

        if (x, y) in l2:
            if not __def__((x, y), chess, (p1, p2, l1, l2), obj[1]):
                link = location_2((x, y + 1))
                out.append(link) if link != '' else ...
            continue

        if not __def__((x, y), chess, (p1, p2, l1, l2), obj[1]):
            link = location_2((x, y + 1))
            out.append(link) if link != '' else ...

    # - output - #
    if __def__(obj[-1], chess, (p1, p2, l1, l2), obj[1]):
        return tuple(out), True
    return tuple(out), False


def __info__(item: Piece):
    return item.type, item.color, item.move, item.link


class Engine:
    def __init__(self, chess, color=WHITE):
        self.chess: Board = chess
        self.color = color
        self.nothing = -1

    def analyst(self):
        return self.move_generation()

    def board_info(self) -> tuple:
        white, black = [], []
        k1, k2 = tuple(), tuple()
        for row in self.chess.board:
            if row == [NOTING]*8:
                continue

            for item in row:
                if item == NOTING:
                    continue
                p = __info__(item)
                if p[0] == KING:
                    if p[1] == 'white':
                        k1 = p
                        continue
                    k2 = p
                    continue
                white.append(p) if p[1] == 'white' else black.append(p)
        return tuple(white), tuple(black), k1, k2

    def move_generation(self) -> tuple:
        white, black, king_w, king_b = self.board_info()

        king_mov_w = __king__(king_w, self.chess, (black+(king_b, ), white))
        king_mov_b = __king__(king_b, self.chess, (white+(king_w, ), black))

        white_mov = (list(), list())
        black_mov = (list(), list())

        for row in self.chess.board:
            if row == [NOTING]*8:
                continue

            for item in row:
                if item == NOTING:
                    continue

                _piece_ = __info__(item)
                _data_ = __move__(_piece_, self.chess, (white+(king_w, ), black+(king_b, )))

                if _piece_[1] == WHITE:
                    if len(_data_) > 0:
                        white_mov[0].append((_piece_, _data_))
                        continue
                    white_mov[1].append((_piece_, _data_))
                else:
                    if len(_data_) > 0:
                        black_mov[0].append((_piece_, _data_))
                        continue
                    black_mov[1].append((_piece_, _data_))
        return king_mov_w, king_mov_b, white_mov, black_mov


# - test - #
def main():
    board = Board()

    board.clr()

    board.prt()

    data = Engine(board).analyst()
    for i in data[2:]:
        for hi in i:
            for k in hi:
                print(k)
        print()
    print(data[0])
    print(data[1])


if __name__ == '__main__':
    start = datetime.datetime.now()

    main()

    _end_ = datetime.datetime.now()
    print(_end_-start)
