from datetime import datetime
from potato import *
from board import *


__all__ = ["board_info", "move_generation"]


def __rook__(board: Board, location: str) -> tuple:
    output = list()

    location = get_location(location)
    output.append(board.out_()[location[1]][0:])
    output = output[0]

    for i in (0, 1, 2, 3, 4, 5, 6, 7):
        output.append(board.out_()[i][location[0]])
    return tuple(output)


def __bishop__(board: Board, location: str) -> tuple:
    output = list()
    l1, l2 = get_location(location)
    b = board.out_()

    for i in (0, 1, 2, 3, 4, 5, 6, 7):
        output.append(b[+i+l1][+i+l2]) if (8 > +i+l1 > -1) and (8 > +i+l2 > -1) else...
        output.append(b[-i+l1][-i+l2]) if (8 > -i+l1 > -1) and (8 > -i+l2 > -1) else...
        output.append(b[-i+l1][+i+l2]) if (8 > -i+l1 > -1) and (8 > +i+l2 > -1) else...
        output.append(b[+i+l1][-i+l2]) if (8 > +i+l1 > -1) and (8 > -i+l2 > -1) else...
    return tuple(output)


def __king__(piece_: Piece, board: Board, link: str) -> bool:
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
    r = __bishop__(board, "B2")
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


def __move__(piece_: Piece, board: Board) -> tuple:
    # info = type 0 , color 1 , location 2, isMove 3 #
    t, c, l, m = piece_.info()
    l1, l2 = get_location(l)
    output = list()

    if t in (QUEEN, ROOK):
        for a in rookMove:
            for v1, v2 in a:
                if not (8 > l1 + v1 > -1) or not (8 > l2 + v2 > -1):
                    break

                p = board.get(get_location((l1 + v1, l2 + v2)))
                if p == NOTING:
                    output.append(get_location((l1 + v1, l2 + v2)))
                    continue
                if p.color == c:
                    break
                output.append(get_location((l1 + v1, l2 + v2)))
                break

    if t in (QUEEN, BISHOP):
        for a in bishopMove:
            for v1, v2 in a:
                if not (8 > l1 + v1 > -1) or not (8 > l2 + v2 > -1):
                    break

                p = board.get(get_location((l1 + v1, l2 + v2)))
                if p == NOTING:
                    output.append(get_location((l1 + v1, l2 + v2)))
                    continue
                if p.color == c:
                    break
                output.append(get_location((l1 + v1, l2 + v2)))
                break

    elif t == PAWN:
        pawn = (pawnMoveW, pawnAttackW) if c == WHITE else (pawnMoveB, pawnAttackB)
        p_mov, p_atk = pawn
        for v1, v2 in p_mov:
            if not (8 > l1 + v1 > -1) or not (8 > l2 + v2 > -1):
                break
            p = board.get(get_location((l1 + v1, l2 + v2)))
            if p != NOTING:
                break
            output.append(get_location((l1 + v1, l2 + v2)))
            if m:
                break

        for v1, v2 in p_atk:
            if not (8 > l1 + v1 > -1) or not (8 > l2 + v2 > -1):
                break
            p = board.get(get_location((l1 + v1, l2 + v2)))
            if p == NOTING:
                continue
            output.append(get_location((l1 + v1, l2 + v2))) if p.color != c else ...

    elif t == KNIGHT:
        for v1, v2 in knightMove:
            if not (8 > l1 + v1 > -1) or not (8 > l2 + v2 > -1):
                continue
            p = board.get(get_location((l1 + v1, l2 + v2)))
            if p == NOTING:
                output.append(get_location((l1 + v1, l2 + v2)))
                continue
            output.append(get_location((l1 + v1, l2 + v2))) if p.color != c else ...

    elif t == KING:
        for v1, v2 in kingMove:
            if not (8 > l1 + v1 > -1) or not (8 > l2 + v2 > -1):
                continue
            p = board.get(get_location((l1 + v1, l2 + v2)))
            if p == NOTING:
                if __king__(piece_, board, get_location((l1 + v1, l2 + v2))):
                    output.append(get_location((l1 + v1, l2 + v2)))
                continue
            if p.color != c:
                if __king__(piece_, board, get_location((l1 + v1, l2 + v2))):
                    output.append(get_location((l1 + v1, l2 + v2)))

    return tuple(output)


def board_info(board: Board) -> tuple:
    o1, o2 = [], []

    for row in board.out():
        if row == [NOTING]*8:
            continue

        for i in row:
            if i == NOTING:
                continue

            if i.color == WHITE:
                o1.append(i)
                continue
            o2.append(i)
    return tuple(o1), tuple(o2)


def move_generation(board: Board, info: tuple) -> tuple:
    pieces_w, pieces_b = info
    ow, ob = [], []

    for i in pieces_w:
        ow.append((i.location, __move__(i, board)))

    for i in pieces_b:
        ob.append((i.location, __move__(i, board)))

    return tuple(ow), tuple(ob)


def position_evaluation(
        board: Board, info1: tuple, info2: tuple):
    pass


def analysis():
    pass


# - test engine - #
def __test__() -> None:
    start = datetime.now()

    # - board - #
    chess = Board()
    chess.clean()

    # - test engine - #
    info = board_info(chess)
    move = move_generation(chess, info)
    printArray2D(move)

    # - display - #
    chess.display()

    print(datetime.now()-start)


if __name__ == '__main__':

    __test__()
