import datetime
import engine
import board

chess = board.Board()


def add(t_, c_, l_: str):
    return chess.add(board.Piece(t_, c_, l_.upper()))


def mov(l1: str, l2: str):
    return chess.mov(l1.upper(), l2.upper())


def get(link: str):
    return chess.get(link.upper())


def show():
    return chess.prt()


def clean():
    return chess.clr()


def _help_():
    print("""- - - - - - - - - - -
# - board commands - #
    add (type, color, Link)  : add_ piece
    mov (Link1, Link2)       : move piece
    get (Link)               : get_ piece

    show ()                  : show chess
    clean ()                 : clean chess

# - engine commands - #          
    coming soon ...          : 

# - bot commands - #
    coming soon ...          : 

- - - - - - - - - - -""")
    return 'fock you'


def potato(_input_: str):
    if _input_.upper() == 'HELP':
        return _help_()
    if _input_[-1] != ')':
        _input_ += '()'
    return str(eval(_input_))


def main():
    while 1:
        _input_ = input('>>> ')

        start = datetime.datetime.now()
        potato(_input_)
        end = datetime.datetime.now()
        print(end-start)


if __name__ == '__main__':
    main()
