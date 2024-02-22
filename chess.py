from move import *

__all__ = ['Chess', 'Potato', 'white', 'black', 'char', 'power',
           'KING', 'QUEEN', 'ROOK', 'BISHOP', 'KNIGHT', 'PAWN', 'NOTING']

# - ♚ ♛ ♝ ♞ ♜ ♟- #
# - ♔ ♕ ♖ ♘ ♗ ♙ - #

KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN, NOTING = ('King', 'Queen', 'Rook', 'Bishop', 'Knight', 'Pawn', '')
char = {'A': 0, 'B': 1, 'C': 2, 'D': 3,
        'E': 4, 'F': 5, 'G': 6, 'H': 7}

power = {QUEEN: 8, ROOK: 5, BISHOP: 4, KNIGHT: 3, PAWN: 1, KING: 0}

white = ('♚', '♛', '♜', '♞ ', '♝', '♟')
black = ('♔', '♕', '♖', '♘ ', '♗ ', '♙')


def __def__(location, chess, color):
    _chess_: Chess = chess
    x, y = location

    info = chess.info()[0]
    _a = {'white': (info[0], info[2]),
          'black': (info[0], info[1]), }[color]
    a1, a2 = tuple(_a[0]), tuple(_a[1])

    for row in move_rook_:
        for c in row:
            c = __potato__((c[0] + x, c[1] + y))
            if c != '':
                if c in a1:
                    continue
                elif c in a2:
                    p: Potato = chess.get(c)
                    if p.type == ROOK or p.type == QUEEN:
                        return False
                    break
                break

    for row in move_bishop:
        for c in row:
            c = __potato__((c[0] + x, c[1] + y))
            if c != '':
                if c in a1:
                    continue
                elif c in a2:
                    p: Potato = chess.get(c)
                    if p.type == BISHOP or p.type == QUEEN:
                        return False
                    break
                break

    for row in move_knight:
        for c in row:
            c = __potato__((c[0] + x, c[1] + y))
            if c != '':
                if c in a1:
                    continue
                elif c in a2:
                    p: Potato = chess.get(c)
                    if p.type == KNIGHT:
                        return False
                    break
                break

    move = {'white': ((-1+x, -1+y), (1+x, -1+y)),
            'black': ((1+x, 1+y), (-1+x, 1 + y))}[color]
    for i in __potato__(move[0]), __potato__(move[1]):
        if i != '':
            if i in a1:
                continue
            elif i in a2:
                p: Potato = chess.get(i)
                if p.type == PAWN:
                    return False
                break
            break
    return True


def __potato__(link):
    out = str()
    c = {0: 'A', 1: 'B', 2: 'C', 3: 'D',
         4: 'E', 5: 'F', 6: 'G', 7: 'H'}
    y = int(link[1])+1
    x = link[0]

    if x in tuple(c.keys()):
        if int(y) < 9 and y > 0:
            out = (c[x])+str(y)
    return out


def __move__(location, move, chess, color, type_):
    _chess_: Chess = chess
    x, y = location

    out = (list(), move, color, type_)

    info = chess.info()[0]

    arr1 = {KING: move_king_, QUEEN: move_queen, ROOK: move_rook_,
            BISHOP: move_bishop, KNIGHT: move_knight, PAWN: move_pawn_, }.get(type_)

    _a = {'white': (info[0], info[2]),
          'black': (info[0], info[1]), }[color]
    a1, a2 = tuple(_a[0]), tuple(_a[1])

    if type_ != PAWN:
        for row in arr1:
            for c in row:
                c = __potato__((c[0]+x, c[1]+y))
                if c != '':
                    if c in a1:
                        out[0].append(c)
                        continue
                    elif c in a2:
                        out[0].append(c)
                        break
                    break
    else:
        move1 = (0, 1), (0, 2), (1, 1), (-1, 1)
        move2 = (0, -1), (0, -2), (-1, -1), (1, -1)
        move_ = {'white': move1, 'black': move2}[color]
        move_ = tuple(__potato__((i[0]+x, i[1]+y)) for i in move_)

        if move_[0] in a1:
            out[0].append(move_[0])
        if move_[1] in a1 and move:
            out[0].append(move_[1])
        if move_[2] in a2:
            out[0].append(move_[2])
        if move_[3] in a2:
            out[0].append(move_[3])

    # m1 = __potato__((move_[1][0]+x, move_[1][1]+y))
    # m2 = __potato__((move_[2][0]+x, move_[2][1]+y))
    # print(m1, m2)
    return out


class Chess:
    def __init__(self):
        self.board = (['']*8, ['']*8, ['']*8, ['']*8,
                      ['']*8, ['']*8, ['']*8, ['']*8,)
        self.last_movement_white = ''
        self.last_movement_black = ''

    def potato(self):
        self.board = ([''] * 8, [''] * 8, [''] * 8, [''] * 8,
                      [''] * 8, [''] * 8, [''] * 8, [''] * 8,)

        for data in (('white', 1, 1), ('black', 8, -1)):
            color, n1, n2 = data[0], data[1], data[2]
            for i in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',):
                i = f'{i}{n1+n2}'
                self.add(i, Potato(PAWN, color, i, self))

            self.add(f'A{n1}', Potato(ROOK, color, f'A{n1}', self))
            self.add(f'H{n1}', Potato(ROOK, color, f'H{n1}', self))

            self.add(f'F{n1}', Potato(BISHOP, color, f'F{n1}', self))
            self.add(f'C{n1}', Potato(BISHOP, color, f'C{n1}', self))

            self.add(f'G{n1}', Potato(KNIGHT, color, f'G{n1}', self))
            self.add(f'B{n1}', Potato(KNIGHT, color, f'B{n1}', self))

            self.add(f'D{n1}', Potato(QUEEN, color, f'D{n1}', self))
            self.add(f'E{n1}', Potato(KING, color, f'E{n1}', self))

    def show(self):
        import sys
        for i in self.board:
            sys.stdout.write(str(i)+'\n')

    def info(self):
        le = ('A', 'B', 'C', 'D',
              'E', 'F', 'G', 'H',)
        out = ([], [], []), [], []
        power_w, power_b = 0, 0
        re1 = 0
        for i in self.board:
            re2 = 0
            for potato in i:
                if potato == NOTING:
                    out[0][0].append(le[re2]+f'{re1+1}')
                else:
                    if self.get(le[re2]+f'{re1+1}').color == 'white':
                        out[0][1].append(le[re2]+f'{re1+1}')
                        power_w += power[self.get(le[re2]+f'{re1+1}').type]
                    elif self.get(le[re2]+f'{re1+1}').color == 'black':
                        out[0][2].append(le[re2]+f'{re1+1}')
                        power_b += power[self.get(le[re2] + f'{re1 + 1}').type]
                re2 += 1
            re1 += 1
        out[2].append((power_w, power_b))
        out[1].append(self.last_movement_white)
        out[1].append(self.last_movement_black)
        return out

    def get(self, link: str):
        try:
            x, y = link[0], link[1]
            x, y = char.get(x), int(y)-1
            return self.board[y][x]
        except AttributeError:
            return NOTING

    def mov(self, old_link: str, new_link: str):
        x1, y1 = old_link[0], old_link[1]
        x2, y2 = new_link[0], new_link[1]

        x1, y1 = char.get(x1), int(y1)-1
        x2, y2 = char.get(x2), int(y2)-1

        p: Potato = self.get(old_link)
        if p.color == 'white':
            self.last_movement_white = (old_link, new_link)
        elif p.color == 'black':
            self.last_movement_black = (old_link, new_link)
        p.mov(new_link)

        obj = self.board[y1][x1]
        self.board[y1][x1] = NOTING
        self.board[y2][x2] = obj

    def add(self, link, potato):
        x, y = link[0], link[1]
        x, y = char.get(x), int(y)-1
        self.board[y][x] = potato

    def __missing__(self, key):
        try:
            x, y = key[0], key[1]
            x, y = char.get(x), int(y)-1
            return self.board[y][x]
        except AttributeError:
            return NOTING


class Potato:
    def __init__(self, type_, color, location, board):
        self.board: Chess = board
        self.potato: bool = True
        self.color: str = color
        self.type: str = type_

        x, y = location
        x, y = char.get(x), int(y)-1
        self.location = (x, y)

        potato = {KING: 0, QUEEN: 1, ROOK: 2,
                  KNIGHT: 3, BISHOP: 4, PAWN: 5}

        if self.color == 'white':
            self.skin = white[potato[self.type]]
        elif self.color == NOTING:
            self.skin = NOTING
        else:
            self.skin = black[potato[self.type]]

    def mov(self, location):
        x, y = location
        x, y = char.get(x), int(y) - 1
        self.location = (x, y)
        self.potato = False

    def info(self, _board_):
        self.board = _board_
        out = __move__(self.location, self.potato, _board_, self.color, self.type)
        return out

    def __repr__(self):
        return self.skin


def main():
    chess: Chess = Chess()

    chess.add('E5', Potato(KING, 'white', 'E5', chess))
    chess.add('D3', Potato(KNIGHT, 'black', 'E2', chess))

    x, y = 'E5'
    x, y = char.get(x), int(y) - 1

    k: Potato = chess.get('E5')
    h = __def__((x, y), chess, k.color)
    print(h)

    chess.show()


if __name__ == '__main__':
    from datetime import datetime
    start = datetime.now()

    main()

    end = datetime.now()
    print((end - start))
