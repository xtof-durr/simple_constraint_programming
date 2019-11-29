#!/usr/bin/env pypy3
# Christoph Dürr - 2019 - Ecole Centrale Supelec

from constraint_programming import ConstraintProgram
import sys

n = int(sys.argv[1])

N = set(range(n))

reines = {i:N for i in N}

C = ConstraintProgram(reines)

for j in N:
    for i in range(j):
        C.add_constraint(i, j, lambda u, v: u - v not in {i - j, 0, j - i})

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

pretty_print()
