
from cmu_112_graphics import *
import math
import numpy as np
import copy

#from 112 course page
#https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
def repr2dList(L):
    if (L == []): return '[]'
    output = [ ]
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [['']*cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append('[\n')
    for row in range(rows):
        output.append(' [ ')
        for col in range(cols):
            if (col > 0):
                output.append(', ' if col < len(L[row]) else '  ')
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((' ],' if row < rows-1 else ' ]') + '\n')
    output.append(']')
    return ''.join(output)

def print2dList(L):
    print(repr2dList(L))

#https://thispointer.com/python-numpy-create-a-ndarray-from-list-tuple-or-list-of-lists-using-numpy-array/
def convertToGrid(map):
    conversion = copy.deepcopy(map)
    rowLen = len(conversion)
    colLen = len(conversion[0])

    # for r in range(rowLen):
    #     for c in range(colLen):
    #         val = map[r][c]
    #         newMatrix=[[val]*2 for r in range(2)]
    #         conversion[r][c] = newMatrix

    newMap = [ (['.']*3*colLen) for r in range(3*rowLen)]
    
    print(rowLen, colLen)
    print(len(newMap), len(newMap[0]))

    for r in range(rowLen):
        for c in range(colLen):
            number = map[r][c]
            newRow = 3*r
            newCol = 3*c
            for i in range(3):
                for j in range(3):
                    newMap[newRow + i][newCol+j] = number


    newMap[15][27] = 'P'
    newMap[27][51] = 'A'
    
    # print2dList(newMap)
    return newMap


            
        