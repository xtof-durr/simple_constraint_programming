#!/usr/bin/env pypy3

import dump_tree

class constraint_programming:
    def __init__(self, var):
        self.var = var
        self.conflict = {x:[] for x in var}
        self.assign = {x:None for x in var}
        self.context = []

    def add_constraint(self, x, y, rel):
        self.conflict[x].append((y, rel))
        inv = {(v,u) for (u,v) in  rel}
        self.conflict[y].append((x, inv))

    def select_var(self):
        x = None
        for y in self.var:
            if (self.assign[y] is None and
                (x is None or
                 len(self.var[y]) < len(self.var[x]))):
                x = y
        return x

    # def backward_check(self, x, u):
    #     for y, rel in self.conflict[x]:
    #         v = self.assign[y] 
    #         if v is not None and (u,v) not in rel:
    #             return False
    #     return True


    def forward_check(self, x, u):
        for y, rel in self.conflict[x]:
            if self.assign[y] is None:
                restreint = {v for v in self.var[y]
                        if (u, v) in rel}
                self.var[y] = restreint


    def save_context(self):
        copy = {x:set(self.var[x]) for x in self.var}
        self.context.append(copy)

    def restore_context(self):
        self.var = self.context.pop()


    def solve(self):
        x = self.select_var()
        if x is None:
            dump_tree.close()
            return self.assign
        for u in self.var[x]:
            self.save_context()
            self.assign[x] = u
            self.forward_check(x, u)
            dump_tree.enter("{}:={}".format(x, u))
            sol = self.solve()
            dump_tree.leave()
            if sol:
                return sol
            self.restore_context()
            self.assign[x] = None
        return None


