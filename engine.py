from chess.move import white_move, black_move
from chess.potato import *
from chess.board import *

from evaluation import evaluate_board
from evaluation import checkmate
import datetime

Opening, MiddleGame, EndGame = (
    "1", "2", "3"
)


def get_king(pieces: tuple):
    for i in pieces:
        if i.type == KING:
            return i


def minimax(board: Board, depth: int, maximizing_player: bool, move_path: tuple):
    if depth == 0:
        # if depth == 0 and ordered legal moves - #
        try:
            new_board = board.copy_board()
            for move in move_path:
                try:
                    move.control(new_board)
                except:
                    break
            return new_board
        except:
            try:
                return evaluate_board(board)
            except:
                if maximizing_player:
                    return -99999
                else:
                    return +99999
    # - ordered legal moves - #
    new_board = board.copy_board()
    for move in move_path:
        try:
            move.control(new_board)
        except:
            try:
                return evaluate_board(new_board)
            except:
                if maximizing_player:
                    return -9999
                else:
                    return +9999

    # - check mate - #
    kw, kb = (
        get_king(new_board.white_pieces()), get_king(new_board.black_pieces())
    )

    if kw is None:
        return -9999
    if kb is None:
        return +9999

    _checkmate_ = checkmate(kw, kb, new_board)
    if _checkmate_ == WHITE:
        return -9999
    if _checkmate_ == BLACK:
        return +9999

    # - minimax algorithm - #
    if maximizing_player:
        value = -9999
        for moves in white_move(board):
            if len(moves) > 0:
                for move in moves:
                    try:
                        value = max(value, minimax(board, depth-1, False, move_path+(move, )))
                    except:
                        continue
    else:
        value = +9999
        for moves in black_move(board):
            if len(moves) > 0:
                for move in moves:
                    try:
                        value = min(value, minimax(board, depth-1, True, move_path+(move, )))
                    except:
                        continue

    return value


def analysis(board: Board, color: str, depth: int) -> tuple:
    output = list()

    # - white - #
    if color == WHITE:
        for moves in white_move(board):
            if len(moves) > 0:
                for move in moves:
                    print(move, minimax(board, depth, True, (move, )))

        return tuple(output)

    # - black - #
    for moves in black_move(board):
        if len(moves) > 0:
            for move in moves:
                print(move, minimax(board, depth, False, (move, )))

    return tuple(output)


def __test__():
    # - start - #
    start = datetime.datetime.now()

    board = Board()
    board.add_pieces()

    # - - - - #

    analysis(board, WHITE, 5)

    # - end - #
    board.display()

    end = datetime.datetime.now()
    print(end-start)


if __name__ == '__main__':
    __test__()
