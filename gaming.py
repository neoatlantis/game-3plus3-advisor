#!/usr/bin/env python3

TO_LEFT = 0
TO_RIGHT = 1
TO_TOP = 2
TO_BOTTOM = 3

def shift4(array):
    assert len(array) == 4
    mapping = [0, 1, 2, 3]
    def shift(pos):
        for i in range(pos, 4):\
            mapping[i] -= 1
    cur = 0
    while cur < 3:
        if (array[cur] == 1 and array[cur+1] == 2) or \
           (array[cur] == 2 and array[cur+1] == 1) or \
           (array[cur] == array[cur+1] and array[cur] > 2) or \
           (array[cur] > 0 and array[cur+1] == 0):
            shift(cur+1)
            cur += 2
            continue
        if array[cur] > 0 and array[cur+1] == 0:
            shift(cur+1)
            cur += 1
            continue
        cur += 1
    ret = [0, 0, 0, 0]
    for i in range(0, 4):
        ret[mapping[i]] += array[i]
    return ret
       
assert shift4([6, 6, 0, 2]) == [12, 0, 2, 0]
assert shift4([6, 0, 0, 6]) == [6, 0, 6, 0]
assert shift4([1, 2, 2, 1]) == [3, 3, 0, 0]
assert shift4([1, 0, 0, 2]) == [1, 0, 2, 0]
print(shift4([1, 1, 1, 1]))


class GameGrid:

    def __init__(self):
        self.state = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

    def userMove(self, direction):
        assert direction in [TO_LEFT, TO_RIGHT, TO_TOP, TO_BOTTOM]

        if direction == TO_LEFT:
            grid = self.state
        
