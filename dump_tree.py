#!/usr/bin/env pypy
# Christoph Dürr - 2019 - Ecole Centrale Supelec

""" command line to convert the produced dot file into an image: 
            dot tmp.dot -T png -o tmp.png
    Or better: use graphviz

    call enter before entering a recursive call
    and leave when finishing it.
    call close when the recursion is done.
"""


class DumpTree:
    def __init__(self, dumpfile):
        self.nodes = 0  # node counter
        self.p = [0]    # stack of recursive calls
        if dumpfile is not None:
            self.f = open(dumpfile, "w")
            self.f.write('digraph G {\n node [shape=point]\n')
        else:
            self.f = None


    def enter(self, label):
        if self.f is None: 
            return
        self.nodes += 1
        self.p.append(self.nodes)
        self.f.write('{} -> {} [label="{}"]'.format(self.p[-2], self.p[-1], label))


    def leave(self):
        if self.f is None: 
            return
        self.p.pop()


    def close(self):
        if self.f is None: 
            return
        self.f.write("}")
        self.f.close()
        self.f = None   # print only a single tree
