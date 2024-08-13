from potato import *

__all__ = ["Piece", "king_"]
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


def __rook__(board, location: str) -> tuple:
    output = list()

    location = get_location(location)
    output.append(board.out_()[location[1]][0:])
    output = output[0]

    for i in (0, 1, 2, 3, 4, 5, 6, 7):
        output.append(board.out_()[i][location[0]])
    return tuple(output)


def __bishop__(board, location: str) -> tuple:
    output = list()
    l1, l2 = get_location(location)
    b = board.out_()

    for i in (0, 1, 2, 3, 4, 5, 6, 7):
        output.append(b[+i+l1][+i+l2]) if (8 > +i+l1 > -1) and (8 > +i+l2 > -1) else...
        output.append(b[-i+l1][-i+l2]) if (8 > -i+l1 > -1) and (8 > -i+l2 > -1) else...
        output.append(b[-i+l1][+i+l2]) if (8 > -i+l1 > -1) and (8 > +i+l2 > -1) else...
        output.append(b[+i+l1][-i+l2]) if (8 > +i+l1 > -1) and (8 > -i+l2 > -1) else...
    return tuple(output)


def king_(piece_: Piece, board, link: str) -> bool:
    t, c, l, m = piece_.info()
    l1, l2 = get_location(link)

    # - rook & queen - #
    r = __rook__(board, link)
    if (ROOK in r) or (QUEEN in r):
        for a in rookMove:
            for v1, v2 in a:
                if not (8 > l1+v1 > -1) or not (8 > l2+v2 > -1):
                    break

                p = board.get(get_location((l1+v1, l2+v2)))
                if p == NOTING:
                    continue
                if p.color == c:
                    break
                if p.type not in (ROOK, QUEEN):
                    break
                return False

    # - bishop & queen - #
    r = __bishop__(board, link)
    if (BISHOP in r) or (QUEEN in r):
        for a in bishopMove:
            for v1, v2 in a:
                if not (8 > l1+v1 > -1) or not (8 > l2+v2 > -1):
                    break

                p = board.get(get_location((l1+v1, l2+v2)))
                if p == NOTING:
                    continue
                if p.color == c:
                    break
                if p.type not in (BISHOP, QUEEN):
                    break
                return False

    # - knight - #
    for v1, v2 in knightMove:
        if not (8 > l1 + v1 > -1) or not (8 > l2 + v2 > -1):
            continue

        p = board.get(get_location((l1 + v1, l2 + v2)))
        if p == NOTING:
            continue
        if p.color == c:
            continue
        if p.type != KNIGHT:
            continue
        return False

    for v1, v2 in kingMove:
        if not (8 > l1 + v1 > -1) or not (8 > l2 + v2 > -1):
            continue
        p = board.get(get_location((l1 + v1, l2 + v2)))
        if p == NOTING:
            continue
        if p.color == c:
            continue
        if p.type != KING:
            continue
        return False

    pawn_attack = pawnAttackW if c != WHITE else pawnAttackB
    for v1, v2 in pawn_attack:
        if not (8 > l1 + v1 > -1) or not (8 > l2 + v2 > -1):
            continue
        p = board.get(get_location((l1 + v1, l2 + v2)))
        if p == NOTING:
            continue
        if p.color == c:
            continue
        if p.type != PAWN:
            continue
        return False
    return True
