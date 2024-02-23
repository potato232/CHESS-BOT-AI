from math import *


def func1(array):
    array = list(array)
    array.sort()
    o, i = [], 0
    while i < len(array):
        o.append(array.count(array[i]))
        i += 1
    o = [k for (k, v) in dict(zip(array, o)).items() if v == max(o)]
    if o != array:
        return o


def func2(array):
    array = list(array)
    array.sort()
    if len(array) % 2 == 0:
        return (array[len(array) // 2] + array[len(array) // 2]) / 2
    else:
        return array[len(array) // 2]


def func3(array):
    array = list(array)
    return sum(array) / len(array)


def func4(array):
    array = list(array)
    out, re = [0, 0, 0, ], 0
    for i in (25, 50, 75):
        i = (len(array) / 100) * i
        i = int(str(i).rstrip('.')[0])
        out[re] = array[i]
        re += 1
    return out


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


def potato_(array):
    """
    out = (mean, median), (q1, q2, q3), mode, (len, max, min)
    """

    # - test - #
    out = ((func1(array), func2(array)),
           func3(array), func4(array),
           (len(array), max(array),  min(array)))

    return out


if __name__ == '__main__':
    sqrt(9)
