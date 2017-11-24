#!/usr/bin/env python3

from gaming import *

def evaluateMovement(state, direction, movementCount=1, maxcount=3):
    retMax = max([max(l) for l in state]) 
    retFreedomGrade = 1 # how many moves can be done after this move

    if movementCount <= maxcount:
        grid = GameGrid(state, movementCount)
        
        totalNextFreedomGrades = 0
        
        for possibility in grid.enumerateUserMoveResults(direction):
            for nextMove in [LEFT, RIGHT, TOP, BOTTOM]:
                results = evaluateMovement(
                    possibility,
                    nextMove,
                    movementCount+1,
                    maxcount
                )

                retMax = max(retMax, results[0])
                totalNextFreedomGrades += results[1] 

        retFreedomGrade *= totalNextFreedomGrades

    return (retMax, retFreedomGrade)

##############################################################################

from bottle import route, run, request, response
import re

@route('/<grid>/<food>/')
def index(grid, food):
    response.set_header("Access-Control-Allow-Origin", "*")

    grid = [int(i) for i in grid.split(",")]
    grid = [grid[0:4], grid[4:8], grid[8:12], grid[12:16]]
    food = int(food)


    maxcount = 5
    movementCount = food

    caller = lambda d: evaluateMovement(\
        grid, d, movementCount=movementCount, maxcount=maxcount)
    
    result = ""
    for line in grid:
        result += " ".join(["%4d" % (i > 0 and i or 0) for i in line]) + "\n"
    result += "LEFT  -> %s\n" % str(caller(LEFT))
    result += "RIGHT -> %s\n" % str(caller(RIGHT))
    result += "TOP   -> %s\n" % str(caller(TOP))
    result += "BOTTOM -> %s\n" % str(caller(BOTTOM))
    
    return result


run(host='localhost', port=13333)

"""
state = [
    [0, 2, 0, 3],
    [0, 2, 0, 1],
    [1, 0, 0, 3],
    [6, 24, 12, 2],
]
nxt = 1
maxcount = 5

if nxt == 1:
    movementCount = 1
else:
    movementCount = 2

print("LEFT", evaluateMovement(state, LEFT, maxcount=maxcount))
print("RIGHT", evaluateMovement(state, RIGHT, maxcount=maxcount))
print("TOP", evaluateMovement(state, TOP, maxcount=maxcount))
print("BOTTOM", evaluateMovement(state, BOTTOM, maxcount=maxcount))
"""
