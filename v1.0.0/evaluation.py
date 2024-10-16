import datetime

from potato import *
from board import *
from piece import *

from move import king_security
from move import move

__all__ = ["evaluate_board", "checkmate"]

evalFuncW = (lambda t, x, y: ({
                KING: kingEvalWhite,
                QUEEN: evalQueen,
                ROOK: rookEvalWhite,
                KNIGHT: knightEval,
                BISHOP: bishopEvalWhite,
                PAWN: pawnEvalWhite,
    }[t])[x][y])

evalFuncB = (lambda t, x, y: ({
                KING: kingEvalBlack,
                QUEEN: evalQueen,
                ROOK: rookEvalBlack,
                KNIGHT: knightEval,
                BISHOP: bishopEvalBlack,
                PAWN: pawnEvalBlack,
    }[t])[x][y])


def evaluate_board(board: Board) -> float:
    total_evaluation: float = 0.0

    pieces_w = board.white_pieces()
    pieces_b = board.black_pieces()

    pawns_w = list()
    pawns_b = list()

    [pawns_w.append(i) if i.type == PAWN else ... for i in pieces_w]
    [pawns_b.append(i) if i.type == PAWN else ... for i in pieces_b]

    # - king safety - #
    for i in pieces_w:
        if i.type == KING:
            total_evaluation += king_safety(i, board)
            break
    for i in pieces_b:
        if i.type == KING:
            total_evaluation += king_safety(i, board)
            break

    # - eval - #
    total_evaluation += sum([material(i) for i in pieces_w])
    total_evaluation += sum([material(i) for i in pieces_b])

    total_evaluation += sum([mobility(board, piece=i) for i in pieces_w])
    total_evaluation += sum([mobility(board, piece=i) for i in pieces_b])

    total_evaluation += pawn_structure(tuple(pawns_w), WHITE)
    total_evaluation += pawn_structure(tuple(pawns_b), BLACK)

    total_evaluation += piece_coordination(pieces_w)
    total_evaluation += piece_coordination(pieces_b)

    return total_evaluation


def checkmate(king_w: Piece, king_b: Piece, board: Board) -> str:
    # - checkmate - #

    if not king_safety(king_w, board):
        if len(move(king_w, board)) == 0:
            return "W"

    if not king_safety(king_b, board):
        if len(move(king_b, board)) == 0:
            return "B"

    return "N"


def material(piece: Piece) -> float:
    # - the number and value of pieces on the board - #
    num: float = 0.0

    num += pieceValue[piece.type]*(+1 if piece.color == WHITE else -1)
    if piece.location in center1:
        num += 13.0*(+1 if piece.color == WHITE else -1)
    elif piece.location in center2:
        num += 8.5*(+1 if piece.color == WHITE else -1)

    num += (
        +(evalFuncW(piece.type, piece.location[0]-1, piece.location[1]-1))
        if piece.color == WHITE else -(evalFuncB(piece.type, piece.location[0]-1, piece.location[1]-1))
    )

    return num


def mobility(board: Board, piece=None, moves=None) -> float:
    # - the ability of pieces to move around the board and control space - #

    if moves is not None:
        if type(moves) != tuple:
            raise quit(f"Error: moveType is {type(moves)}")
    elif piece is not None:
        if type(piece) != Piece:
            raise quit(f"Error: pieceType is {type(piece)}")
        moves = move(piece, board)
    else:
        raise quit("Error: (piece is None) & (moves is None)")

    num: float = 0.0

    if piece.color == WHITE:
        # - white - #
        num += len(moves)
        for i in moves:
            num += evalFuncW(piece.type, i.code[2][0]-1, i.code[2][1]-1)/2

            if (i.code[2][0], i.code[2][1]) in center1:
                num += 2.5  # num += (2.5) if piece can move to center1
            elif (i.code[2][0], i.code[2][1]) in center2:
                num += 1.0  # num += (1.0) if piece can move to center2
        return num

    # - black - #
    num -= len(moves)
    for i in moves:
        num -= evalFuncB(piece.type, i.code[2][0]-1, i.code[2][1]-1)/2

        if (i.code[2][0], i.code[2][1]) in center1:
            num -= 2.5  # num -= (2.5) if piece can move to center1
        elif (i.code[2][0], i.code[2][1]) in center2:
            num -= 1.0  # num -= (1.0) if piece can move to center2
    return num


def king_safety(king: Piece, board: Board) -> float:
    # - how vulnerable the kings are - #

    if king.type != KING:
        raise quit(f"Error: piece type is not king")

    num: float = 0.0

    n = +1 if king.color == WHITE else -1    # n=(1) if king is white else n=(-1)

    num += n if king_security(king, board, king.location) else (-100)*n

    m = len(move(king, board))
    if 2 < m > 5 and m != 3:
        num += +2 * n
    elif m == 3:
        num += +1 * n
    else:
        num += -2 * n

    # - #

    if king.location in center1:
        num += 25*(-n)
    elif king.location in center2:
        num += 18*(-n)

    return num


def pawn_structure(pawns: tuple, color) -> float:
    # - the configuration of pawns on the board - #

    n = +1 if color == WHITE else -1
    t = tuple([p.location for p in pawns])

    num: float = 0.0
    for x, y in t:
        if (x+1, y+1) in t:
            num += n
        if (x+1, y-1) in t:
            num += n
        if (x-1, y+1) in t:
            num += n
        if (x-1, y-1) in t:
            num += n

    return (num/2)+len(t)*n


def piece_coordination(pieces: tuple) -> float:
    # - how well the pieces work together - #

    p = {
        KING: 0,
        QUEEN: 0,
        ROOK: 0,
        KNIGHT: 0,
        BISHOP: 0,
        PAWN: 0,
    }
    for i in pieces:
        p[i.type] += 1

    n = 1 if pieces[0].color == WHITE else -1
    num: float = 0.0

    if p[KNIGHT] >= 1 and p[BISHOP] >= 1:
        num += n*2
    if p[KNIGHT] > 1 or p[BISHOP] > 1:
        num += n
    else:
        num -= n

    num += n*1 if p[ROOK] > 1 else 0
    num += n*2 if p[QUEEN] > 1 else 0

    return num


center1 = (4, 4), (4, 5), (5, 4), (5, 5)

center2 = (
    (3, 3), (3, 4), (3, 5),
    (3, 6), (6, 3), (6, 4),
    (6, 5), (6, 6), (5, 6),
    (5, 3), (4, 6), (4, 3),
)


pieceValue = {
    KING: +90.00, QUEEN: +9.00, ROOK: +5.0,
    KNIGHT: +3.0, BISHOP: +3.5, PAWN: +1.0,
}

pawnStructure = (
    (+1, +1), (-1, +1),
    (+1, -1), (-1, -1),
)

pawnEvalWhite = (
        (0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0),
        (5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0),
        (1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0),
        (0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5),
        (0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0),
        (0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5),
        (0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5),
        (0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0),
)

pawnEvalBlack = ReverseArray(pawnEvalWhite)

knightEval = (
        (-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0),
        (-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0),
        (-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0),
        (-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0),
        (-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0),
        (-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0),
        (-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0),
        (-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0),
)

bishopEvalWhite = (
        (-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0),
        (-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0),
        (-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0),
        (-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0),
        (-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0),
        (-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0),
        (-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0),
        (-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0),
)

bishopEvalBlack = ReverseArray(bishopEvalWhite)

rookEvalWhite = (
        (+0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, +0.0),
        (+0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, +0.5),
        (-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5),
        (-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5),
        (-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5),
        (-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5),
        (-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5),
        (+0.0,  0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  +0.0),
)

rookEvalBlack = ReverseArray(rookEvalWhite)

evalQueen = (
        (-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0),
        (-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0),
        (-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0),
        (-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5),
        (+0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5),
        (-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0),
        (-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0),
        (-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0),
)

kingEvalWhite = (
        (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0),
        (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0),
        (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0),
        (-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0),
        (-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0),
        (-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0),
        (+2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0),
        (+2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0),
)

kingEvalBlack = ReverseArray(kingEvalWhite)


def __test__():
    start = datetime.datetime.now()

    # - board - #
    chess = Board()
    chess.add_pieces()

    chess.move((2, 5), (4, 5))

    # - test - #
    print(evaluate_board(chess))

    # - end test - #
    chess.display()
    print(datetime.datetime.now()-start)


if __name__ == '__main__':
    __test__()
