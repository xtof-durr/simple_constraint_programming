#!/usr/bin/env pypy3
# Christoph Dürr - 2019 - Ecole Centrale Supelec
"""The Zebra puzzle by Lewis Caroll
"""

import sys
from constraint_programming import ConstraintProgram

DOM = {1, 2, 3, 4, 5}
# chaque attribut est une variable
varnames = [
    ["norvégien", "anglais",  "espagnol",  "ukrainien", "japonais"],
    ["bleue",     "rouge",    "verte",     "jaune",     "blanche"],
    ["lait",      "café",     "thé",       "vin",       "eau"],
    ["kools",     "cravens",  "old golds", "gitanes",   "chesterfields"],
    ["chien",     "escargot", "renard",    "cheval",    "zèbre"]
]

# les maisons sont numérotés de 1 à 5



var = {}
for categorie in varnames:
    for name in categorie:
        var[name] = DOM

# norvégien = 1
var["norvégien"] = {1}

# lait = 3
var["lait"] = {3}

P = ConstraintProgram(var)

# tout différent
for categorie in varnames:
    for a in categorie:
        for b in categorie:
            if a < b:
                P.add_constraint(a, b, int.__ne__)

EQUAL = int.__eq__
SUCC = lambda u, v: v - u == 1
PREC = lambda u, v: v - u == -1
NEXT = lambda u, v: v - u in [-1, 1]


# bleue = norvégien + 1
P.add_constraint("bleue", "norvégien", PREC)

# anglais = rouge
P.add_constraint("anglais", "rouge", EQUAL)

# verte = café
P.add_constraint("verte", "café", EQUAL)

# jaune = kools
P.add_constraint("jaune", "kools", EQUAL)

# blanche = verte + 1
P.add_constraint("blanche", "verte", PREC)

# espagnol = chien
P.add_constraint("espagnol", "chien", EQUAL)

# ukrainien = thé
P.add_constraint("ukrainien", "thé", EQUAL)

# japonais = cravens
P.add_constraint("japonais", "cravens", EQUAL)

# old golds = escargot
P.add_constraint("old golds", "escargot", EQUAL)

# gitanes = vin
P.add_constraint("gitanes", "vin", EQUAL)

# (chesterfields = renard + 1) ou (chesterfields = renard - 1)
P.add_constraint("chesterfields", "renard", NEXT)

# (kools = cheval + 1) ou (kools = cheval - 1)
P.add_constraint("kools", "cheval", NEXT)


sol = P.solve_w_forward_check()
for maison in DOM:
    print("%-15i" % maison, end="")
print()

for categorie in varnames:
    for maison in DOM:
        for name in categorie:
            if sol[name] == maison:
                print("%-15s" % name, end="")
    print()
