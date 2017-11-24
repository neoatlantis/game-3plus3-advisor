#!/usr/bin/env python3

LEFT = 0
RIGHT = 1
TOP = 2
BOTTOM = 3

# 当前存在问题：新块其实可以出现在移动方向对侧的任何空块上，和当列/行是否移动过无关
# 计算自由度似乎还有很大错误。

def shift4(array):
    lenarray = len(array)
    for cur in range(0, lenarray):
        if array[cur] < 0: array[cur] = 0
    cur = 0
    while cur < lenarray - 1:
        if (array[cur] == 1 and array[cur+1] == 2) or \
           (array[cur] == 2 and array[cur+1] == 1) or \
           (array[cur] == array[cur+1] and array[cur] > 2):
           array[cur] += array[cur+1]
           array[cur+1] = 0
           cur += 2
        else:
            cur += 1
    shiftbegin = -1 
    for cur in range(0, lenarray):
        if array[cur] == 0:
            shiftbegin = cur
            break
    if shiftbegin >= 0: # if not, this is unshiftable
        for cur in range(shiftbegin, lenarray-1):
            t = array[cur]
            array[cur] = array[cur+1]
            array[cur+1] = t
        if array[-1] == 0:
            array[-1] = -1 # mark this as possible insertion point of new 1/2 block 
    return array
        
       
#print(shift4([0, 0, 0, 1]))
#print(shift4([0, 0, 1, 0]))
#exit()

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
            [(3, 0), (2, 0), (1, 0), (0, 0)],
            [(3, 1), (2, 1), (1, 1), (0, 1)],
            [(3, 2), (2, 2), (1, 2), (0, 2)],
            [(3, 3), (2, 3), (1, 3), (0, 3)],
        ],
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
        newMatrix = [ [0, 0, 0, 0 ], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0] ]
        if direction == LEFT: 
            for row in range(0,4):
                for col in range(0,4):
                    newMatrix[row][col] = src[row][col]
        else:
            convMatrix = self.rotationToLeftMatrix[direction]
            for row in range(0, 4):
                for col in range(0, 4):
                    oldRow, oldCol = convMatrix[row][col]
                    newMatrix[oldRow][oldCol] = src[row][col]
        return newMatrix
                

    def __init__(self, state, movementCount=1):
        self.state = state # initial state as given by 3+3
        self.__next = (movementCount % 2) + 1 

    def enumerateUserMoveResults(self, direction):
        """Fictional analyse of user movement, returns a series of possible
        matrixes."""

        matrix = self.__getRotationNormalizedMatrix(self.state, direction)
#        print("before shift\n", matrix)
        for each in matrix: shift4(each)
#        print("after shift\n", matrix)

        for i in range(0, 4):
            if matrix[i][-1] < 0:
                # if the right most col is marked as appendable
                matrix[i][-1] = self.__next
                yield self.__reverseRotationNormalizedMatrix(matrix, direction)
                matrix[i][-1] = 0
#                print(matrix)


    def newState(self, state):
        """Updates the new state as given by 3+3 and user/AI choice."""
        self.state = state
        if self.__next == 1:
            self.__next == 2
        else:
            self.__next == 1

"""if __name__ == "__main__":
    s = GameGrid([
        [12, 6, 3, 2],
        [6,  12, 3, 3],
        [12, 6, 3, 2],
        [6,  12, 2, 3],
    ])

    for each in s.enumerateUserMoveResults(LEFT):
        for line in each:
            print(" ".join(["%2d" % (i > 0 and i or 0) for i in line]))
        print("----")
"""
