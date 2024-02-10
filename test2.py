
# - ♚ ♛ ♝ ♞ ♜ ♟- #
# - ♔ ♕ ♖ ♘ ♗ ♙ - #

KING, QUEEN, ROOK, AL_FIL, HORSE, PAWN, NOTING = ('King', 'Queen', 'Rook', 'AlFil', 'Horse', 'Pawn', '')
char = {'A': 0, 'B': 1, 'C': 2, 'D': 3,
        'E': 4, 'F': 5, 'G': 6, 'H': 7}

black = ('♚', '♛', '♜', '♞ ', '♜', '♟')
white = ('♔', '♕', '♖', '♘ ', '♗ ', '♙')


class Chess:
    def __init__(self):
        self.board = (['']*8, ['']*8, ['']*8, ['']*8,
                      ['']*8, ['']*8, ['']*8, ['']*8,)

    def potato(self):
        for d in (('white', 1, 1), ('black', 8, -1)):
            color, n1, n2 = d[0], d[1], d[2]
            for i in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',):
                i += str(n1+n2)
                pawn = Potato(PAWN, color, i)
                self.add(i, pawn)

            self.add(f'A{n1}', Potato(ROOK, color, f'A{n1}'))
            self.add(f'H{n1}', Potato(ROOK, color, f'H{n1}'))

            self.add(f'B{n1}', Potato(AL_FIL, color, f'B{n1}'))
            self.add(f'G{n1}', Potato(AL_FIL, color, f'G{n1}'))

            self.add(f'C{n1}', Potato(HORSE, color, f'C{n1}'))
            self.add(f'F{n1}', Potato(HORSE, color, f'F{n1}'))

            self.add(f'D{n1}', Potato(QUEEN, color, f'D{n1}'))
            self.add(f'E{n1}', Potato(KING, color, f'E{n1}'))

    def show(self):
        for i in self.board:
            print(i)

    def info(self):
        le = ('A', 'B', 'C', 'D',
              'E', 'F', 'G', 'H',)
        out = ([], [], []), tuple()
        re1 = 0
        for i in self.board:
            re2 = 0
            for potato in i:
                if potato == NOTING:
                    out[0][0].append(le[re2]+f'{re1+1}')
                else:
                    if self.get(le[re2]+f'{re1+1}').color == 'white':
                        out[0][1].append(le[re2]+f'{re1+1}')
                    elif self.get(le[re2]+f'{re1+1}').color == 'black':
                        out[0][2].append(le[re2]+f'{re1+1}')
                re2 += 1
            re1 += 1
        return out

    def get(self, link: str):
        x, y = link[0], link[1]
        x, y = char.get(x), int(y)-1
        return self.board[y][x]

    def mov(self, old_link: str, new_link: str):
        x1, y1 = old_link[0], old_link[1]
        x2, y2 = new_link[0], new_link[1]
        x1, y1 = char.get(x1), int(y1)-1
        x2, y2 = char.get(x2), int(y2)-1

        obj = self.board[y1][x1]
        self.board[y1][x1] = NOTING
        self.board[y2][x2] = obj

    def add(self, link, potato):
        x, y = link[0], link[1]
        x, y = char.get(x), int(y)-1
        self.board[y][x] = potato


class Potato:
    def __init__(self, type_, color, location):
        self.type = type_
        self.color = color
        self.potato = ''

        x, y = location
        x, y = char.get(x), int(y)-1
        self.location = (x, y)

        potato = {KING: 0, QUEEN: 1, ROOK: 2,
                  AL_FIL: 3, HORSE: 4, PAWN: 5}

        if self.color == 'white':
            self.skin = white[potato[self.type]]
        elif self.color == NOTING:
            self.skin = NOTING
        else:
            self.skin = black[potato[self.type]]

    def move(self, location):
        x, y = location
        x, y = char.get(x), int(y) - 1
        self.location = (x, y)

    def info(self, board: Chess):
        out = tuple()
        info = board.info()
        return out

    def __repr__(self):
        return self.skin


def main():
    chess = Chess()
    chess.potato()
    chess.show()


if __name__ == '__main__':
    main()
