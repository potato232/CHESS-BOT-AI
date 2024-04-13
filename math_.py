import math

__all__ = [
    'func1', 'func2', 'func3',
    'func4', 'func5', 'ran', 'math'
]


def func1(array) -> list:
    o, i = [], 0
    array = func5(list(array))
    while i < len(array):
        o.append(array.count(array[i]))
        i += 1
    o = [k for (k, v) in dict(zip(array, o)).items() if v == max(o)]
    if o != array:
        return o


def func2(array):
    array = func5(list(array))
    if len(array) % 2 == 0:
        return (array[len(array) // 2] + array[len(array) // 2]) / 2
    else:
        return array[len(array) // 2]


def func3(array) -> float:
    array = list(array)
    return sum(array) / len(array)


def func4(array) -> list:
    array = list(array)
    out, re = [0, 0, 0, ], 0
    for i in (25, 50, 75):
        i = (len(array) / 100) * i
        i = int(str(i).rstrip('.')[0])
        out[re] = array[i]
        re += 1
    return out


def func5(array: list) -> list:
    array.sort()
    return array


def ran_arr():
    from random import randint
    return [randint(1, 100) for _ in [0]*randint(1, 5000)]


def ran(my_potato):
    from random import randint
    my_potato = list(my_potato)
    for _ in range(len(my_potato)):
        x, y = randint(0, len(my_potato))*-1, randint(0, len(my_potato))*-1
        x_, y_ = my_potato[x], my_potato[y]
        x_ = x_ + y_
        y_ = x_ - y_
        x_ = x_ - y_
        my_potato[x], my_potato[y] = x_, y_
    return tuple(my_potato)


def __test__(array):
    # - test - #
    out = ((func1(array), func2(array)),
           func3(array), func4(array),
           (len(array), max(array),  min(array)))

    return out
