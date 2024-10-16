from move import white_move, black_move
from evaluation import evaluate_board
from potato import *
from board import *
import datetime

Opening, MiddleGame, EndGame = (
    "opening", "middle game", "end game"
)


def mfmp(board: Board, path) -> Board:
    new_board = board.copy_board()
    for move in path:
        try:
            move.control(new_board)
        except:
            break
    return new_board


def minimax(board: Board, depth: int, maximizing_player: bool, move_path: tuple):
    if depth == 0:
        try:
            return evaluate_board(mfmp(board, move_path))
        except:
            try:
                return evaluate_board(board)
            except:
                if maximizing_player:
                    return -99999
                else:
                    return +99999

    if maximizing_player:
        value = -9999

        new_board = board.copy_board()
        for move in move_path:
            try:
                move.control(new_board)
            except:
                try:
                    return evaluate_board(new_board)
                except:
                    return value
        # - #
        for moves in white_move(board):
            if len(moves) > 0:
                for move in moves:
                    try:
                        value = max(value, minimax(board, depth-1, False, move_path+(move, )))
                    except:
                        continue

    else:
        value = +9999

        new_board = board.copy_board()
        for move in move_path:
            try:
                move.control(new_board)
            except:
                try:
                    return evaluate_board(new_board)
                except:
                    return value

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
