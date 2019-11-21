#!/usr/bin/env pypy

# dot tmp.dot -T png -o tmp.png


nodes = 0
f = None
p = [0]


def enter(label):
    global f, p, nodes
    if f is None:
        f = open("tmp.dot", "w")
        print("digraph G {\n node [shape=dot]", file=f)
    nodes += 1
    p.append(nodes)
    print(p[-2], "->", p[-1], 
        '[label="{}"]'.format(label), file=f)

def leave():
    global f, p, nodes
    p.pop()

def close():
    global f, p, nodes
    print("}", file=f)
