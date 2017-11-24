#!/usr/bin/env python3

from gaming import *

def evaluateMovement(state, direction, movementCount=1, maxcount=3):
    retMax = max([max(l) for l in state]) 
    retFreedomGrade = 1 # how many moves can be done after this move

#    if movementCount == 1:
#        print(state, direction)

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

#    print(grid)
#    print("next: %d" % food)

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
