#!/usr/bin/env pypy3
# Christoph Dürr - 2019 - Ecole Centrale Supelec

from constraint_programming import ConstraintProgram
import sys

n = int(sys.argv[1])

N = set(range(n))

reines = {i:N for i in N}

C = ConstraintProgram(reines)

def rel(i, j):
	return lambda u, v: u - v not in {i - j, 0, j - i}
# 
for j in N:
    for i in range(j):
        C.add_constraint(i, j, rel(i,j))
        # the following does not work since the lambda function is not a 
        # closure. It means that the when the function is called, i and j
        # do not have the same value as they had when the function was called
        # https://www.geeksforgeeks.org/python-closures/
        # in summary: it is ok to use lambda functions when adding a constraint
        # as long as they don't refer to variables other than the parameters 
        # and global constants.
        # C.add_constraint(i, j, lambda u, v: u - v not in {i - j, 0, j - i})

sol = C.solve()

# sol = C.solve_lex_smallest()
# for i in N:
#     print("{:02}".format(sol[i]), end='')
# print()


def pretty_print():
    for i in N:
        for j in N:
            if sol[i] == j:
                print("* ", end='')
            else:
                print(". ", end='')
        print()


if not sol:
	print("no solution")
else:
	pretty_print()

