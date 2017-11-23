#!/usr/bin/env python3

LEFT = 0
RIGHT = 1
TOP = 2
BOTTOM = 3

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

    ret = [0, 0, 0, 0] # create a new array and copy old values into it
    for i in range(0, 4):
        if array[i] < 0: array[i] = 0
        ret[mapping[i]] += array[i]
    if ret[-1] == 0:
        ret[-1] = -1 # mark this as possible insertion point of new 1/2 block 
    return ret
       
assert shift4([6, 6, 0, 2]) == [12, 0, 2, -1]
assert shift4([12, 0, 2, -1]) == [12, 2, 0, -1]
assert shift4([6, 0, 0, 6]) == [6, 0, 6,  -1]
assert shift4([1, 2, 2, 1]) == [3, 3, 0,  -1]
assert shift4([1, 0, 0, 2]) == [1, 0, 2,  -1]
assert shift4([1, 1, 1, 1]) == [1, 1, 1, 1]


class GameGrid:

    rotationToLeftMatrix = {
        RIGHT: [
            [(0, 3), (0, 2), (0, 1), (0, 0)],
            [(1, 3), (1, 2), (1, 1), (1, 0)],
            [(2, 3), (2, 2), (2, 1), (2, 0)],
            [(3, 3), (3, 2), (3, 1), (3, 0)],
        ],
        TOP: [
            [(0, 3), (1, 3), (2, 3), (3, 3)],
            [(0, 2), (1, 2), (2, 2), (3, 2)],
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(0, 0), (1, 0), (2, 0), (3, 0)],
        ],
        BOTTOM: [
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(0, 2), (1, 2), (2, 2), (3, 2)],
            [(0, 3), (1, 3), (2, 3), (3, 3)],
        ],
    }

    possibleNewBlockPositions = {
        LEFT:   [(0, 3), (1, 3), (2, 3), (3, 3)],
        RIGHT:  [(0, 0), (1, 0), (2, 0), (3, 0)],
        TOP:    [(3, 0), (3, 1), (3, 2), (3, 3)],
        BOTTOM: [(0, 0), (0, 1), (0, 2), (0, 3)],
    }

    def __getRotationNormalizedMatrix(self, src, direction):
        """Based on the user action on moving in `direction`, transform
        `self.state` and its movement into a always-shifting-to-left direction,
        so that we can reuse the shifting code."""
        assert direction in [LEFT, RIGHT, TOP, BOTTOM]
        if direction == LEFT: 
            return src 
        else:
            convMatrix = self.rotationToLeftMatrix[direction]
            newMatrix = [
                [ src[row][col] for row, col in rowConv ]
                for rowConv in convMatrix
            ]
            return newMatrix

    def __reverseRotationNormalizedMatrix(self, src, direction):
        """Resume the rotation of matrix."""
        assert direction in [LEFT, RIGHT, TOP, BOTTOM]
        if direction == LEFT: 
            return src 
        else:
            convMatrix = self.rotationToLeftMatrix[direction]
            newMatrix = [ [0] * 4 ] * 4
            for row in range(0, 4):
                for col in range(0, 4):
                    oldRow, oldCol = convMatrix[row][col]
                    newMatrix[oldRow][oldCol] = src[row][col]
            return newMatrix
                

    def __init__(self, state):
        self.state = state # initial state as given by 3+3
        self.__next = 1    # we know the first block appears will always be 1

    def enumerateUserMove(self, direction):
        """Fictional analyse of user movement, returns a series of possible
        matrixes."""
        pass

    def newState(self, state):
        """Updates the new state as given by 3+3 and user/AI choice."""
        self.state = state
        if self.__next == 1:
            self.__next == 2
        else:
            self.__next == 1
