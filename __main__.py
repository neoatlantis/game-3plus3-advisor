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
import json

@route('/<grid>/<food>/')
def index(grid, food):
    response.set_header("Access-Control-Allow-Origin", "*")
    
    orighash = grid
    grid = [int(i) for i in grid.split(",")]

    zeros = 0
    for i in grid:
        if i == 0: 
            zeros+=1

    grid = [grid[0:4], grid[4:8], grid[8:12], grid[12:16]]
    food = int(food)

#    print(grid)
#    print("next: %d" % food)
    
    if zeros >= 6:
        maxcount = 4
    elif zeros >= 4:
        maxcount = 5
    else:
        maxcount = 6

    movementCount = food

    caller = lambda d: evaluateMovement(\
        grid, d, movementCount=movementCount, maxcount=maxcount)

    ret = {
        "result": "",
        "hash": orighash,
        "data": {
            "left": caller(LEFT),
            "right": caller(RIGHT),
            "top": caller(TOP),
            "bottom": caller(BOTTOM),
        }
    }

    # discard moves with no freedom grade and build a list
    sort = [each for each in ret["data"].items() if each[1][1] > 0]
    print(ret)
    def criteria(item):
        value = item[1]
        return value[0] + value[1] / 16777216.0
    sort = sorted(sort, key=criteria, reverse=True)
    print(sort)
    if not sort:
        ret["choice"] = ""
    else:
        ret["choice"] = sort[0][0]

    result = ""
    for line in grid:
        result += " ".join(["%4d" % (i > 0 and i or 0) for i in line]) + "\n"
    arrow = lambda x: x == ret["choice"] and "<-" or ""
    result += "LEFT   -> %s %s\n" % (str(ret["data"]["left"]), arrow("left"))
    result += "RIGHT  -> %s %s\n" % (str(ret["data"]["right"]), arrow("right"))
    result += "TOP    -> %s %s\n" % (str(ret["data"]["top"]), arrow("top"))
    result += "BOTTOM -> %s %s\n" % (str(ret["data"]["bottom"]), arrow("bottom"))
    ret["result"] = result
    
    return json.dumps(ret)


run(host='localhost', port=13333)
