from .piece import Piece
from .board import Board
from .potato import *


__all__ = ["Move", "move", "king_security",
           "all_move", "white_move", "black_move"]


class Move:
    def __init__(self, *code):
        self.code = code

    def control(self, board: Board):
        n = 0
        while n < len(self.code):
            c = self.code[n]
            if c == MOVE_KEY:
                board.move(self.code[n+1], self.code[n+2])
                n += 2
            if c == PUSH_KEY:
                board.push(Piece(self.code[n+1], self.code[n+2], self.code[n+3]), self.code[n+3])
                n += 3
            if c == DEL_KEY:
                board.pop((self.code[n+1], self.code[n+2]))
                n += 2
            if c == END_KEY:
                print("End game")
                break
            n += 1

    def __repr__(self):
        return f'{self.code[1]} to {self.code[2]}'


def ordered_legal_moves(board: Board) -> bool:
    moves = all_move(board)

    for i in moves:
        print(i)

    return True


def white_move(board: Board) -> tuple:
    output = list()

    pieces = board.white_pieces()
    for i in pieces:
        output.append(move(i, board))
    return tuple(output)


def black_move(board: Board) -> tuple:
    output = list()

    pieces = board.black_pieces()
    for i in pieces:
        output.append(move(i, board))
    return tuple(output)


def all_move(board: Board) -> tuple:
    return white_move(board)+black_move(board)


def move(piece: Piece, board: Board) -> tuple:
    if piece.type == PAWN:
        return pawn_move(piece, board)

    if piece.type == BISHOP:
        return bishop_move(piece, board)

    if piece.type == KNIGHT:
        return knight_move(piece, board)

    if piece.type == ROOK:
        return rook_move(piece, board)

    if piece.type == QUEEN:
        return rook_move(piece, board)+bishop_move(piece, board)

    if piece.type == KING:
        return king_move(piece, board)


def king_security(piece: Piece, board: Board, location) -> bool:
    l1, l2 = location

    # rook or queen
    for n in ReverseArray(range(l1-1)):
        p = board.get((n+1, l2))
        if p == EMPTY:
            continue
        if p.color != piece.color:
            if p.type in (ROOK, QUEEN):
                return False
        break

    for n in range(l1, 8):
        p = board.get((n + 1, l2))
        if p == EMPTY:
            continue
        if p.color != piece.color:
            if p.type in (ROOK, QUEEN):
                return False
        break

    for n in ReverseArray(range(l2-1)):
        p = board.get((l1, n + 1))
        if p == EMPTY:
            continue
        if p.color != piece.color:
            if p.type in (ROOK, QUEEN):
                return False
        break

    for n in range(l2, 8):
        p = board.get((l1, n + 1))
        if p == EMPTY:
            continue
        if p.color != piece.color:
            if p.type in (ROOK, QUEEN):
                return False
        break

    # bishop or queen
    r = 0
    for _ in range(l1, 8):
        r += 1
        if 1 > l1+r or l1+r > 8:
            break
        if 1 > l2+r or l2+r > 8:
            break
        p = board.get((l1+r, l2+r))
        if p == EMPTY:
            continue
        if p.color != piece.color:
            if p.type in (BISHOP, QUEEN):
                return False
        break

    r = 0
    for _ in range(l1, 8):
        r += 1
        if 1 > l1+r or l1+r > 8:
            break
        if 1 > l2-r or l2-r > 8:
            break
        p = board.get((l1+r, l2-r))
        if p == EMPTY:
            continue
        if p.color != piece.color:
            if p.type in (BISHOP, QUEEN):
                return False
        break

    r = 0
    for _ in range(l2, 8):
        r += 1
        if 1 > l1-r or l1-r > 8:
            break
        if 1 > l2+r or l2+r > 8:
            break
        p = board.get((l1-r, l2+r))
        if p == EMPTY:
            continue
        if p.color != piece.color:
            if p.type in (BISHOP, QUEEN):
                return False
        break

    r = 0
    for _ in range(l2, 8):
        r += 1
        if 1 > l1-r or l1-r > 8:
            break
        if 1 > l2-r or l2-r > 8:
            break
        p = board.get((l1-r, l2-r))
        if p == EMPTY:
            continue
        if p.color != piece.color:
            if p.type in (BISHOP, QUEEN):
                return False
        break
    del r

    # knight
    for v1, v2 in (
        (1, 2), (-1, 2), (1, -2), (-1, -2),
        (2, 1), (2, -1), (-2, 1), (-2, -1),
    ):
        if not (9 > l1 + v1 > 0) or not (9 > l2 + v2 > 0):
            continue
        p: Piece = board.get((l1 + v1, l2 + v2))
        if p == EMPTY:
            continue
        if p.color != piece.color and p.type == KNIGHT:
            return False

    # pawn
    try:
        p1 = board.get((l1+1, l2+1)) if piece.color == WHITE else board.get((l1-1, l2+1))
        if p1 != EMPTY:
            if p1.color != piece.color and p1.type == PAWN:
                return False
        del p1
    except IndexError:
        pass
    try:
        p2 = board.get((l1+1, l2-1)) if piece.color == WHITE else board.get((l1-1, l2-1))
        if p2 != EMPTY:
            if p2.color != piece.color and p2.type == PAWN:
                return False
        del p2
    except IndexError:
        pass

    # king
    for v1, v2 in (
        (+1, +1), (+0, +1), (+1, +0), (-1, +1),
        (-1, -1), (+0, -1), (-1, +0), (+1, -1),
    ):
        if not (9 > l1 + v1 > 0) or not (9 > l2 + v2 > 0):
            continue
        p: Piece = board.get((l1 + v1, l2 + v2))
        if p == EMPTY:
            continue
        if p.color != piece.color and p.type == KING:
            return False

    return True


def king_move(piece: Piece, board: Board) -> tuple:
    l1, l2 = piece.location
    output = list()

    for v1, v2 in (
            (+1, +1), (-1, +1), (+1, -1), (-1, -1),
            (+1, +0), (-1, +0), (+0, +1), (+0, -1),
    ):
        if not (9 > l1 + v1 > 0) or not (9 > l2 + v2 > 0):
            continue
        link = (l1+v1, l2+v2)
        p = board.get(link)

        if p == EMPTY:
            if king_security(piece, board, link):
                output.append(Move(MOVE_KEY, (l1, l2), link))
            continue

        if p.color == piece.color:
            continue

        if king_security(piece, board, link):
            output.append(Move(MOVE_KEY, (l1, l2), link))

    if not piece.isMove:
        if piece.color == WHITE:
            if piece.location == (1, 5):
                r1_, r2_ = board.get((1, 1)), board.get((1, 8))

                p1, p2, p3 = (
                    board.get((1, 2)),
                    board.get((1, 3)),
                    board.get((1, 4)),
                )
                p4, p5 = (
                    board.get((1, 6)),
                    board.get((1, 7))
                )

                if r1_ != EMPTY and (
                    p1 == EMPTY and p2 == EMPTY and p3 == EMPTY
                ):
                    if r1_.type == ROOK and r1_.color == piece.color and not r1_.isMove:
                        output.append(Move(
                            MOVE_KEY, (1, 5), (1, 3),
                            MOVE_KEY, (1, 1), (1, 4),
                           ))
                if r2_ != EMPTY and (
                    p4 == EMPTY and p5 == EMPTY
                ):
                    if r2_.type == ROOK and r2_.color == piece.color and not r2_.isMove:
                        output.append(Move(
                            MOVE_KEY, (1, 5), (1, 7),
                            MOVE_KEY, (1, 8), (1, 6),
                        ))
        else:
            if piece.location == (8, 5):
                r1_, r2_ = board.get((8, 1)), board.get((8, 8))

                p1, p2, p3 = (
                    board.get((8, 2)),
                    board.get((8, 3)),
                    board.get((8, 4)),
                )
                p4, p5 = (
                    board.get((8, 6)),
                    board.get((8, 7))
                )

                if r1_ != EMPTY and (
                    p1 == EMPTY and p2 == EMPTY and p3 == EMPTY
                ):
                    if r1_.type == ROOK and r1_.color == piece.color and not r1_.isMove:
                        output.append(Move(
                            MOVE_KEY, (8, 5), (8, 3),
                            MOVE_KEY, (8, 1), (8, 4),
                           ))
                if r2_ != EMPTY and (
                    p4 == EMPTY and p5 == EMPTY
                ):
                    if r2_.type == ROOK and r2_.color == piece.color and not r2_.isMove:
                        output.append(Move(
                            MOVE_KEY, (8, 5), (8, 7),
                            MOVE_KEY, (8, 8), (8, 6),
                        ))

    return tuple(output)


def rook_move(piece: Piece, board: Board) -> tuple:
    l1, l2 = piece.location
    output = list()

    for n in ReverseArray(range(l1-1)):
        p = board.get((n+1, l2))
        if p == EMPTY:
            output.append(Move(MOVE_KEY, (l1, l2), (n+1, l2)))
            continue
        if p.color != piece.color:
            output.append(Move(MOVE_KEY, (l1, l2), (n+1, l2)))
        break
    for n in range(l1, 8):
        p = board.get((n + 1, l2))
        if p == EMPTY:
            output.append(Move(MOVE_KEY, (l1, l2), (n+1, l2)))
            continue
        if p.color != piece.color:
            output.append(Move(MOVE_KEY, (l1, l2), (n+1, l2)))
        break
    for n in ReverseArray(range(l2-1)):
        p = board.get((l1, n + 1))
        if p == EMPTY:
            output.append(Move(MOVE_KEY, (l1, l2), (l1, n+1)))
            continue
        if p.color != piece.color:
            output.append(Move(MOVE_KEY, (l1, l2), (l1, n+1)))
        break
    for n in range(l2, 8):
        p = board.get((l1, n + 1))
        if p == EMPTY:
            output.append(Move(MOVE_KEY, (l1, l2), (l1, n+1)))
            continue
        if p.color != piece.color:
            output.append(Move(MOVE_KEY, (l1, l2), (l1, n+1)))
        break

    """
    for i in output:
        print(i)
    """

    return tuple(output)


def bishop_move(piece: Piece, board: Board) -> tuple:
    l1, l2 = piece.location
    output = list()

    r = 0
    for _ in range(l1, 8):
        r += 1
        if 1 > l1+r or l1+r > 8:
            break
        if 1 > l2+r or l2+r > 8:
            break
        p = board.get((l1+r, l2+r))
        if p == EMPTY:
            output.append(Move(MOVE_KEY, (l1, l2), (l1+r, l2+r)))
            continue
        if p.color != piece.color:
            output.append(Move(MOVE_KEY, (l1, l2), (l1+r, l2+r)))
        break

    r = 0
    for _ in range(l1, 8):
        r += 1
        if 1 > l1+r or l1+r > 9:
            break
        if 1 > l2-r or l2-r > 9:
            break
        p = board.get((l1+r, l2-r))
        if p == EMPTY:
            output.append(Move(MOVE_KEY, (l1, l2), (l1+r, l2-r)))
            continue
        if p.color != piece.color:
            output.append(Move(MOVE_KEY, (l1, l2), (l1+r, l2-r)))
        break

    r = 0
    for _ in range(l2, 8):
        r += 1
        if 1 > l1-r or l1-r > 9:
            break
        if 1 > l2+r or l2+r > 9:
            break
        p = board.get((l1-r, l2+r))
        if p == EMPTY:
            output.append(Move(MOVE_KEY, (l1, l2), (l1-r, l2+r)))
            continue
        if p.color != piece.color:
            output.append(Move(MOVE_KEY, (l1, l2), (l1-r, l2+r)))
        break

    r = 0
    for _ in range(l2, 8):
        r += 1
        if 1 > l1-r or l1-r > 9:
            break
        if 1 > l2-r or l2-r > 9:
            break
        p = board.get((l1-r, l2-r))
        if p == EMPTY:
            output.append(Move(MOVE_KEY, (l1, l2), (l1-r, l2-r)))
            continue
        if p.color != piece.color:
            output.append(Move(MOVE_KEY, (l1, l2), (l1-r, l2-r)))
        break

    """
    for i in output:
        print(i)
    """

    return tuple(output)


def knight_move(piece: Piece, board: Board) -> tuple:
    l1, l2 = piece.location
    output = list()

    for v1, v2 in (
        (1, 2), (-1, 2), (1, -2), (-1, -2),
        (2, 1), (2, -1), (-2, 1), (-2, -1),
    ):
        if not (9 > l1 + v1 > 0) or not (9 > l2 + v2 > 0):
            continue
        p: Piece = board.get((l1 + v1, l2 + v2))
        if p == EMPTY:
            output.append(Move(MOVE_KEY, (l1, l2), (l1 + v1, l2 + v2)))
            continue
        if p.color != piece.color:
            output.append(Move(MOVE_KEY, (l1, l2), (l1 + v1, l2 + v2)))
    return tuple(output)


def pawn_move(piece: Piece, board: Board) -> tuple:
    if piece.color == WHITE:
        return pawn_white(piece, board)
    return pawn_black(piece, board)


def pawn_white(piece: Piece, board: Board) -> tuple:
    l1, l2 = piece.location
    output = list()

    u = (
        lambda i1, i2, t: Move(
            MOVE_KEY, (l1, l2), (i1, i2),
            PUSH_KEY, WHITE, t, i2,)
    )

    if board.get((l1+1, l2)) == EMPTY:
        if l1 == 7:
            output.append(u(l1+1, l2, QUEEN))
            output.append(u(l1+1, l2, KNIGHT))
            output.append(u(l1+1, l2, ROOK))
            output.append(u(l1+1, l2, BISHOP))
        else:
            output.append(Move(MOVE_KEY, (l1, l2), (l1+1, l2)))

        if l1 == 2:
            if board.get((l1+2, l2)) == EMPTY:
                output.append(Move(MOVE_KEY, (l1, l2), (l1+2, l2)))

    if l2 != 8:
        if board.get((l1+1, l2+1)) != EMPTY:
            if board.get((l1+1, l2+1)).color == BLACK:
                if l1 == 7:
                    output.append(u(l1+1, l2+1, QUEEN))
                    output.append(u(l1+1, l2+1, KNIGHT))
                    output.append(u(l1+1, l2+1, ROOK))
                    output.append(u(l1+1, l2+1, BISHOP))
                else:
                    output.append(Move(MOVE_KEY, (l1, l2), (l1+1, l2+1)))
        elif l1 == 5:
            if l2+1 != EMPTY:
                p: Piece = board.get((l1, l2 + 1))
                if p.color != WHITE and p.type == PAWN and board.lastMove[0] == (l1-2, l2+1):
                    output.append(Move(
                        MOVE_KEY, (l1, l2), (l1+1, l2+1),
                        DEL_KEY, l1, l2+1
                    ))

    if l2 != 1:
        if board.get((l1+1, l2-1)) != EMPTY:
            if board.get((l1+1, l2-1)).color == BLACK:
                if l1 == 7:
                    output.append(u(l1+1, l2-1, QUEEN))
                    output.append(u(l1+1, l2-1, KNIGHT))
                    output.append(u(l1+1, l2-1, ROOK))
                    output.append(u(l1+1, l2-1, BISHOP))
                else:
                    output.append(Move(MOVE_KEY, (l1, l2), (l1+1, l2-1)))
        elif l1 == 5:
            if l2-1 != EMPTY:
                p: Piece = board.get((l1, l2-1))
                if p.color != WHITE and p.type == PAWN and board.lastMove[0] == (l1-2, l2-1):
                    output.append(Move(
                        MOVE_KEY, (l1, l2), (l1+1, l2-1),
                        DEL_KEY, l1, l2-1
                    ))

    return tuple(output)


def pawn_black(piece: Piece, board: Board) -> tuple:
    l1, l2 = piece.location
    output = list()

    u = (
        lambda i1, i2, t: Move(
            MOVE_KEY, (l1, l2), (i1, i2),
            PUSH_KEY, BLACK, t, i2
        )
    )

    if board.get((l1-1, l2)) == EMPTY:
        if l1 == 2:
            output.append(u(l1-1, l2, QUEEN))
            output.append(u(l1-1, l2, KNIGHT))
            output.append(u(l1-1, l2, ROOK))
            output.append(u(l1-1, l2, BISHOP))
        else:
            output.append(Move(MOVE_KEY, (l1, l2), (l1-1, l2)))

        if l1 == 7:
            if board.get((l1 - 2, l2)) == EMPTY:
                output.append(Move(MOVE_KEY, (l1, l2), (l1-2, l2)))

    if l2 != 8:
        if board.get((l1-1, l2+1)) != EMPTY:
            if board.get((l1-1, l2 + 1)).color == BLACK:
                if l1 == 2:
                    output.append(u(l1-1, l2+1, QUEEN))
                    output.append(u(l1-1, l2+1, KNIGHT))
                    output.append(u(l1-1, l2+1, ROOK))
                    output.append(u(l1-1, l2+1, BISHOP))
                else:
                    output.append(Move(MOVE_KEY, (l1, l2), (l1-1, l2+1)))
        elif l1 == 4:
            if l2+1 != EMPTY:
                p: Piece = board.get((l1, l2 + 1))
                if p.color != WHITE and p.type == PAWN and board.lastMove[0] == (l1+2, l2+1):
                    output.append(Move(
                        MOVE_KEY, (l1, l2), (l1-1, l2+1),
                        DEL_KEY, l1, l2+1
                    ))

    if l2 != 1:
        if board.get((l1 - 1, l2 - 1)) != EMPTY:
            if board.get((l1 - 1, l2 - 1)).color == BLACK:
                if l1 == 2:
                    output.append(u(l1-1, l2-1, QUEEN))
                    output.append(u(l1-1, l2-1, KNIGHT))
                    output.append(u(l1-1, l2-1, ROOK))
                    output.append(u(l1-1, l2-1, BISHOP))
                else:
                    output.append(Move(MOVE_KEY, (l1, l2), (l1-1, l2-1)))
        elif l1 == 4:
            if l2 - 1 != EMPTY:
                p: Piece = board.get((l1, l2 - 1))
                if p.color != WHITE and p.type == PAWN and board.lastMove[0] == (l1+2, l2 - 1):
                    output.append(Move(
                        MOVE_KEY, (l1, l2), (l1 - 1, l2 - 1),
                        DEL_KEY, l1, l2 - 1
                    ))

    return tuple(output)


def __test__():
    board = Board()

    h = (8, 5)
    k = (7, 8)
    j = (8, 7)

    board.push(Piece(BLACK, KING, h), h)
    board.push(Piece(WHITE, PAWN, k), k)
    board.push(Piece(BLACK, ROOK, j), j)

    # rook_move(board.get((5, 3)), board)
    # print(king_security(board.get(h), board, board.get(h).location))

    for i in move(board.get(k), board):
        i.display()

    board.display()


if __name__ == '__main__':
    __test__()
