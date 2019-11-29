#!/usr/bin/env pypy3
# Christoph Dürr - 2019 - Ecole Centrale Supelec
"""Sudoku solver
"""

from constraint_programming import ConstraintProgram
import sys
from pprint import PrettyPrinter

def block(i, j):
    """returns the block index to which 
    a given cell belongs
    """
    return (i // 3) * 3 + j // 3

    
P = PrettyPrinter()

grid = [
[0, 2, 6, 0, 0, 0, 8, 1, 0],
[3, 0, 0, 7, 0, 8, 0, 0, 6],
[4, 0, 0, 0, 5, 0, 0, 0, 7],
[0, 5, 0, 1, 0, 7, 0, 9, 0],
[0, 0, 3, 9, 0, 5, 1, 0, 0],
[0, 4, 0, 3, 0, 2, 0, 5, 0],
[1, 0, 0, 0, 3, 0, 0, 0, 2],
[5, 0, 0, 2, 0, 4, 0, 0, 9],
[0, 3, 8, 0, 0, 0, 4, 6, 0]]

P.pprint(grid)

N = range(9)
var = {}

for i in N:
    for j in N:
        if grid[i][j]:
            var[i, j] = {grid[i][j]}  # fixed inital value
        else:
            var[i, j] = set(range(1,10))

C = ConstraintProgram(var)

for i1 in N:
    for i2 in N:
        for j1 in N:
            for j2 in N:
                if ((i1, j1) != (i2, j2) and 
                    (i1 == i2 or j1 == j2 or
                        block(i1, j1) == block(i2, j2))):
                    C.add_constraint((i1, j1), (i2, j2), int.__ne__)

sol = C.solve()

for i, j in sol:
    grid[i][j] = sol[i, j]

P.pprint(grid)