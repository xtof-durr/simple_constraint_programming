#!/usr/bin/env pypy
# -*- coding: utf-8 -*-
# c.durr - ecole centrale paris - 2015-2019 - eternity

# Wang tiling
# https://en.wikipedia.org/wiki/Eternity_II_puzzle

from constraint_programming import ConstraintProgram
import sys

# ----------------- encoding of the tiles

# numbering of the tile border
TOP    = 0
LEFT   = 1
BOTTOM = 2
RIGHT  = 3

# for every tile, for every border, its color 
# the color 0 has to be on the grid border
color = \
    [[5, 2, 2, 5],[5, 2, 5, 2],[5, 2, 5, 4],[5, 2, 2, 4],
     [5, 2, 5, 4],[5, 5, 2, 4],[2, 3, 0, 1],[5, 2, 2, 5],
     [2, 5, 5, 5],[6, 2, 6, 0],[6, 5, 1, 0],[0, 3, 2, 6],
     [6, 0, 7, 5],[3, 7, 0, 0],[0, 1, 2, 7],[5, 6, 0, 1],
     [7, 0, 7, 5],[6, 2, 1, 0],[2, 5, 2, 5],[0, 6, 2, 7],
     [2, 6, 0, 1],[1, 5, 3, 0],[2, 1, 0, 7],[2, 2, 5, 5],
     [3, 2, 1, 0],[0, 3, 3, 0],[2, 5, 5, 5],[0, 7, 2, 3],
     [4, 4, 5, 5],[2, 2, 4, 2],[7, 0, 6, 5],[2, 2, 2, 5],
     [2, 2, 4, 5],[0, 7, 1, 0],[2, 5, 2, 2],[0, 0, 3, 3]]

# ------------------ encoding of the problem

# grid consist of n times n cells

n = 6
assert len(color) == n * n

# variables
CELLS = {(i, j) for i in range(n) for j in range(n)}

# domain for variables
TILEROT = {(t, r) for t in range(n * n) for r in range(4)}

# ---------------- Create the variables.


# var(i,j) indicates the tile and its rotation
var = {(i, j): TILEROT for i, j in CELLS}

prob = ConstraintProgram(var, "f.dot")


# ---------------- Create the constraints.

# check adjacent tiles
def border_color(tr, side):
    t, r = tr
    return color[t][(r + side) % 4]


# restrict grid border color
for k in range(n):
    prob.add_unary_constraint((0,   k), lambda tr: border_color(tr, TOP) == 0)
    prob.add_unary_constraint((n-1, k), lambda tr: border_color(tr, BOTTOM) == 0)
    prob.add_unary_constraint((k,   0), lambda tr: border_color(tr, LEFT) == 0)
    prob.add_unary_constraint((0, n-1), lambda tr: border_color(tr, RIGHT) == 0)


# every tile is used exactly once
for ij1 in CELLS:
    for ij2 in CELLS:
        if ij1 < ij2:
            prob.add_constraint(ij1, ij2, lambda (t1, r1), (t2, r2): t1 != t2)



def match_vert(above, below):
    return border_color(above, BOTTOM) == border_color(below, TOP)


def match_horiz(left, right):
    return border_color(left, RIGHT) == border_color(right, LEFT)

for i in range(n-1):
    for j in range(n):
        prob.add_constraint((i, j), (i + 1, j), match_vert)

for i in range(n):
    for j in range(n-1):
        prob.add_constraint((i, j), (i, j + 1), match_horiz)


sol = prob.solve()

for row in range(n):
    for k in range(4):
        for col in range(n):
            tr = sol[row, col]
            if k==0:
                print " %i |" % border_color(tr, TOP),
            elif k==1:
                print "%i %i|" % (border_color(tr, LEFT), border_color(tr, RIGHT)),
            elif k==2:
                print " %i |" % border_color(tr, BOTTOM),
            else:
                print "---+",
        print
