from chess import *


def __test__():
    # - ChessBoard - #
    chess = Chess()
    chess.potato()

    # - get info - #
    chess.info()
    chess.info2()

    chess.show_info()

    # - Add piece to ChessBoard - #
    piece = Potato(PAWN, 'black', 'E5', chess)
    chess.add('E5', piece)
    # - add black pawn in E5 - #

    # - move piece - #
    chess.mov('E2', 'E4')
    # - E2 to E4 - #

    # - show chess board - #
    chess.show()


if __name__ == '__main__':
    start = datetime.now()

    __test__()

    end = datetime.now()
    print(end - start)
