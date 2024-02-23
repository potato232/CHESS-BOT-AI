from datetime import datetime
from move import *
import sys

__all__ = ['Chess', 'Potato', 'white', 'black', 'char', 'power', 'datetime',
           'KING', 'QUEEN', 'ROOK', 'BISHOP', 'KNIGHT', 'PAWN', 'NOTING', ]

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

    move = {'white': (((-1, -1), (+1, -1),),),
            'black': (((+1, +1), (-1, +1),),)}[color]
    move = potato_ + (move, )

    re = 0
    for p1 in move:
        _break_ = False
        for p2 in p1:
            for p3 in p2:
                p3 = p3[0]+x, p3[1]+y
                step = __potato__(p3)
                if step != '':
                    if step in a1:
                        continue
                    elif step in a2:
                        p: Potato = chess.get(step)
                        if re == 0:
                            if p.type == ROOK or p.type == QUEEN:
                                return False
                        elif re == 1:
                            if p.type == BISHOP or p.type == QUEEN:
                                return False
                        elif re == 2:
                            if p.type == KNIGHT:
                                return False
                        elif re == 3:
                            if p.type == PAWN:
                                return False

                        _break_ = True
                        break
                    else:
                        _break_ = True
                        break
            if _break_:
                break
        re += 1
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

    out = list()
    info = chess.info()[0]

    arr1 = {KING: move_king_, QUEEN: move_queen, ROOK: move_rook_,
            BISHOP: move_bishop, KNIGHT: move_knight, PAWN: move_pawn_, }[type_]

    _a = {'white': (info[0], info[2]),
          'black': (info[0], info[1]), }[color]
    a1, a2 = tuple(_a[0]), tuple(_a[1])

    if type_ != PAWN:
        for row in arr1:
            for c in row:
                c = __potato__((c[0]+x, c[1]+y))
                if c != '':
                    if c in a1:
                        out.append(c)
                        continue
                    elif c in a2:
                        out.append(c)
                        break
                    break
        return tuple(out)
    else:
        move1 = (0, 1), (0, 2), (1, 1), (-1, 1)
        move2 = (0, -1), (0, -2), (-1, -1), (1, -1)
        move_ = {'white': move1, 'black': move2}[color]
        move_ = tuple(__potato__((i[0]+x, i[1]+y)) for i in move_)

        if move_[0] in a1:
            out.append(move_[0])
        if move_[1] in a1 and move:
            out.append(move_[1])
        if move_[2] in a2:
            out.append(move_[2])
        if move_[3] in a2:
            out.append(move_[3])
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

    def info2(self):
        out, re = (list(), list(), self.info()), 0
        for row in self.info()[0][1:]:
            for i in row:
                d0 = (char.get(i[0]), int(i[1])-1)
                d1 = (self.get(i)).info(self)
                d2 = __def__(d0, self, d1[2])
                out[re].append(d1+(d0, d2))
            re += 1
        return out

    def show_info(self):
        data = (self.info2())
        for i in data:
            for j in i:
                sys.stdout.write(str(j)+'\n')
            sys.stdout.write('\n')

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
        return (__move__(self.location, self.potato, _board_, self.color, self.type),
                self.potato, self.color, self.type)

    def __repr__(self):
        return self.skin


def main():
    chess: Chess = Chess()
    chess.potato()
    chess.show_info()
    chess.show()


if __name__ == '__main__':
    start = datetime.now()

    main()

    end = datetime.now()
    print((end - start))
