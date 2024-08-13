from board import Board
from piece import *
from potato import *

__all__ = ["move", "move_generation", "move_filter"]
__author__ = 'potato 232'


def move(piece_: Piece, board: Board) -> tuple:
    # - get move piece - #

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
                if p.color != c:
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
                if king_(piece_, board, get_location((l1 + v1, l2 + v2))):
                    output.append(get_location((l1 + v1, l2 + v2)))
                continue
            if p.color != c:
                if king_(piece_, board, get_location((l1 + v1, l2 + v2))):
                    output.append(get_location((l1 + v1, l2 + v2)))

    return tuple(output)


def move_generation(board: Board, info: tuple) -> tuple:
    pieces_w, pieces_b = info
    ow, ob = [], []

    for i in pieces_w:
        ow.append((i.location, move(i, board)))

    for i in pieces_b:
        ob.append((i.location, move(i, board)))

    return tuple(ow), tuple(ob)


def move_filter(info: tuple) -> tuple:
    # - filter move_generation - #
    # move_filter(move_generation(board, board_info(board))))

    out_w, out_b = [list(), list()], [list(), list()]
    [out_w[0].append(i) if (len(i[1]) > 0) else (out_w[1].append(i)) for i in info[0]]
    [out_b[0].append(i) if (len(i[1]) > 0) else (out_b[1].append(i)) for i in info[1]]
    return tuple(out_w), tuple(out_b)


def __test__():
    from board import board_info
    from datetime import datetime
    from sys import stdout

    start = datetime.now()
    board_test = Board()
    board_test.clean()
    info1 = board_info(board_test)

    # - test function - #
    info2 = move_generation(board_test, info1)
    print(" - info 2 - \n", info2, '\n')

    info3 = move_filter(info2)
    print(" - info 3 - \n", info3, '\n')

    # - #
    stdout.write(str(datetime.now()-start))


if __name__ == "__main__":
    __test__()
