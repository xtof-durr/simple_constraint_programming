#!/usr/bin/env pypy3

from constraint_programming import constraint_programming
import sys

n = int(sys.argv[1])

N = list(range(n))

reines = {i:N for i in N}

C = constraint_programming(reines)

for j in N:
    for i in range(j):
        rel = {(u, v) for u in reines[i]
                      for v in reines[j]
                      if u-v not in {i-j, 0, j-i}}
        C.add_constraint(i, j, rel)

sol = C.solve()

for i in N:
    for j in N:
        if sol[i] == j:
            print("* ", end='')
        else:
            print(". ", end='')
    print()

