from piece import *
from potato import *
from move import *
from board import *

__all__ = ["game_over_w", "game_over_b", "material", "mobility",
           "king_safety", "pawn_structure", "control_space",
           "piece_coordination", "potato_func_analysis"]


def get_king(info: tuple) -> tuple:
    kw, kb = None, None

    for i in info[0]:
        if i.type != KING:
            kw = i
            break

    for i in info[1]:
        if i.type == KING:
            kb = i
            break

    return kw, kb


def game_over_w(chess: Board, n1=None, n2=None, n3=None) -> bool:
    # - game over white - #
    # - input: move_filter -> output: bool - #

    # n1 = board_info
    # n2 = move_generation
    # n3 = move_filter

    info1 = board_info(chess) if n1 is None else n1
    info2 = move_generation(chess, info1) if n2 is None else n2
    info3 = move_filter(info2)[0][0] if n3 is None else n3[0][0]

    if len(info3) == 0:
        return True

    for i in info3:
        board = copy_board(chess)
        for j in i[1]:
            board.mov(i[0], j)
            my_info = board_info(board)
            my_king: Piece = get_king(my_info)[0]
            if not king_(my_king, chess, my_king.location):
                continue
            return False

    return True


def game_over_b(chess: Board, n1=None, n2=None, n3=None) -> bool:
    # - game over black - #
    # - input: move_filter -> output: bool - #

    # n1 = board_info
    # n2 = move_generation
    # n3 = move_filter

    info1 = board_info(chess) if n1 is None else n1
    info2 = move_generation(chess, info1) if n2 is None else n2
    info3 = move_filter(info2)[1][0] if n3 is None else n3[1][0]

    if len(info3) == 0:
        return True

    for i in info3:
        board = copy_board(chess)
        for j in i[1]:
            board.mov(i[0], j)
            my_info = board_info(board)
            my_king: Piece = get_king(my_info)[1]
            if not king_(my_king, chess, my_king.location):
                continue
            return False

    return True


def material(data: tuple, out: float = 0.0) -> float:
    # - the number and value of pieces on the board - #
    # - input: board_info() -> output - #

    for i in data[0]:
        out += (strengthWhite[i.type])
    for i in data[1]:
        out += (strengthBlack[i.type])
    return out


def mobility(data: tuple, out: float = 0.0) -> float:
    # - the ability of pieces to move around the board - #
    # - input: move_filter() -> output - #

    out += (+len(data[0][0])) + (+len(data[1][1]))
    out += (-len(data[0][1])) + (-len(data[1][0]))
    return out


def king_safety(data: tuple, chess: Board, out: float = 0.0) -> float:
    # - how vulnerable the kings are - #
    # - input: board_info -> output - #

    kw, kb = get_king(data)
    if kw is not None:
        king_m = move(kw, chess)
        if not king_(kw, chess, kw.location):
            out += -500
        out += + 15 if (len(king_m) > 1) and (len(king_m) < 4) else -15
        out += +(len(king_m)/2) if len(king_m) != 0 else -3
    else:
        out += -100

    if kb is not None:
        king_m = move(kb, chess)
        if not king_(kb, chess, kb.location):
            out += +500
        out += -15 if (len(king_m) > 1) and (len(king_m) < 4) else +15
        out += -(len(king_m)/2) if len(king_m) != 0 else +3
    else:
        out += +100
    return out


def pawn_structure(data: tuple, out: float = 0.0) -> float:
    # - the configuration of pawns on the board - #
    return out


def control_space(data: tuple, out: float = 0.0) -> float:
    # - which side controls more of the board - #
    return out


def piece_coordination(data: tuple, out: float = 0.0) -> float:
    # - how well the pieces work together - #
    return out


def potato_func_analysis(data: tuple, out: float = 0.0) -> float:
    # potato_func_analysis(board_info(board)) -> number

    # - white pieces - #
    for p in data[0]:
        i = get_location(p.info()[2])

        match p.type:
            case "Pawn":
                out += pawnEvalWhite[i[1]][i[0]]
            case "Knight":
                out += kingEvalWhite[i[1]][i[0]]
            case "Bishop":
                out += bishopEvalWhite[i[1]][i[0]]
            case "Queen":
                out += evalQueen[i[1]][i[0]]
            case "Rook":
                out += rookEvalWhite[i[1]][i[0]]

    # - black pieces - #
    for p in data[1]:
        i = get_location(p.info()[2])

        match p.type:
            case "Pawn":
                out += pawnEvalBlack[i[1]][i[0]]*(-1)
            case "Knight":
                out += kingEvalBlack[i[1]][i[0]]*(-1)
            case "Bishop":
                out += bishopEvalBlack[i[1]][i[0]]*(-1)
            case "Queen":
                out += evalQueen[i[1]][i[0]]*(-1)
            case "Rook":
                out += rookEvalBlack[i[1]][i[0]]*(-1)
    return out


def __test__():
    # - board - #
    chess = Board()
    chess.clean()
    chess.mov("E2", "E4")
    # chess.delete("E2")

    info1 = board_info(chess)
    info2 = move_generation(chess, info1)
    info3 = move_filter(info2)

    # - test - #
    # print(material(info1))
    # print(game_over_w(chess))

    num = material(info1)
    num += (mobility(info3))
    num += (king_safety(info1, chess))
    num += (potato_func_analysis(info1))
    print(num)


if __name__ == '__main__':
    __test__()
