from random import randint

KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN = (
    "King", "Queen", "Rook", "Bishop", "Knight", "Pawn"
)

MOVE_KEY = "M"
PUSH_KEY = "P"
DEL_KEY = "D"
NEW_KEY = "N"
END_KEY = "E"


WHITE, BLACK = ("white", "black")
EMPTY = ' '

letters = tuple([chr(i) for i in range(65, 65+8)])
numbers = ('1', '2', '3', '4', '5', '6', '7', '8')

RandomArray = (lambda r1, r2: [randint(1, r1) for _ in [0]*randint(1, r2)])
ReverseArray = (lambda array: tuple([array[-(n+1)] for n in range(len(array))]))
printArray2D = (lambda array: [[print(k) for k in i] for i in array])

copyList = (lambda mylist: [i for i in mylist])
meanFunc = (lambda array: sum(array) / len(array))


def sort_array(arr) -> tuple:
    arr = list(arr)
    arr.sort()
    return tuple(arr)
