#!/usr/bin/env python3

LEFT = 0
RIGHT = 1
TOP = 2
BOTTOM = 3

def shift4(array):
    """Returns a 4-elements array that's shifted to the left. Mark the right
    most cell if it may be inserted with a new block with -1, and returns
    whether the array is in fact shifted(e.g. a [3, 2, 2, 0] is not
    left-shiftable, although it will be returned as [3, 2, 2, -1], meaning that
    if another row is shifted, this array may be still appended with a value at
    position 3, whereas if all 4 rows in the matrix are not shiftable, a
    movement to the left is defacto impossible.
    """
    shifted = False
    
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
           shifted = True
        else:
            cur += 1
    
    shiftbegin = -1
    for cur in range(0, lenarray):
        if array[cur] == 0:
            shiftbegin = cur
            break
    if shiftbegin >= 0: # if not, this is unshiftable
        for cur in range(shiftbegin, lenarray-1):
            if not shifted and (array[cur] > 0 or array[cur+1] > 0):
                shifted = True
            t = array[cur]
            array[cur] = array[cur+1]
            array[cur+1] = t
    if array[-1] == 0:
        # the insertion point of new block can be anywhere opposite the moving
        # direction, even though this row itself was not moved
        array[-1] = -1 # mark this as possible insertion point of new 1/2 block 
    return array, shifted
        
       
#print(shift4([0, 0, 0, 1]))
#print(shift4([0, 0, 1, 0]))
#exit()

def test(i, oseries, oshifted):
    a, b = shift4(i)
    assert a == oseries and b == oshifted

test([6, 6, 0, 2], [12, 0, 2, -1], True)
test([12, 0, 2, -1], [12, 2, 0, -1], True)
test([6, 0, 0, 6], [6, 0, 6,  -1], True)
test([1, 2, 2, 1], [3, 3, 0,  -1], True)
test([1, 0, 0, 2], [1, 0, 2,  -1], True)
test([1, 1, 1, 1], [1, 1, 1, 1], False)
test([0, 0, 0, 0], [0, 0, 0, -1], False)


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
        newMatrix = [ [0, 0, 0, 0 ], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0] ]
        if direction == LEFT: 
            for row in range(0,4):
                for col in range(0,4):
                    newMatrix[row][col] = src[row][col]
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
        self.__next = ((movementCount + 1) % 2) + 1 

    def enumerateUserMoveResults(self, direction):
        """Fictional analyse of user movement, returns a series of possible
        matrixes."""

        matrix = self.__getRotationNormalizedMatrix(self.state, direction)
#        print("before shift\n", matrix)
        shiftable = False
        for each in matrix:
            _, shifted = shift4(each)
            shiftable = shiftable or shifted

        if not shiftable:
#            print("not shiftable")
            yield from ()
            return

#        print("after shift\n", matrix)

        for i in range(0, 4):
            if matrix[i][-1] < 0:
                # if the right most col is marked as appendable
                matrix[i][-1] = self.__next
                yield self.__reverseRotationNormalizedMatrix(matrix, direction)
                matrix[i][-1] = 0
#                print(matrix)


if __name__ == "__main__":

    test = "3,6,192,3,24,48,12,24,3,768,48,3,1,384,6,3"
    nxt = 2

    grid = [int(i) for i in test.split(",")]
    grid = [grid[0:4], grid[4:8], grid[8:12], grid[12:16]]
    
    s = GameGrid(grid, nxt)

    for each in s.enumerateUserMoveResults(TOP):
        for line in each:
            print(" ".join(["%4d" % (i > 0 and i or 0) for i in line]))
        print("----")
