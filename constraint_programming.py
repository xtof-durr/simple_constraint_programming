#!/usr/bin/env python3
# Christoph Dürr - 2019 - Ecole Centrale Supelec
# coding=utf-8

from dump_tree import DumpTree


class ConstraintProgram:
    """Simple constraint programming solver.
    Allows only binary constraints (involving exactly two variables).
    
    It's purpose is to illustrate the basic techniques of solving
    constraint programs, using only few lines of code, 
    but is not as efficient as other existing solvers. 
    """

    def __init__(self, var, dumpfile=None):
        """
        :param var: a dictionary mapping variable names to their domain.
            a variable name can be any hashable object.
            a domain should be a set.
        """
        self.var = var
        self.conflict = {x: [] for x in var}  # lists variables constraint with x
        self.assign = {x: None for x in var}  # partial solution
        self.context = []                     # used for saving domains
        self.dump = DumpTree(dumpfile)

    def add_constraint(self, x, y, relation):
        """Adds a binary constraint

        :param x: variable
        :param y: variable
        :param relation: either a boolean function on value pairs. 
                which returns true on (u,v) 
                if x:=u, y:=v is valid for this constraint.
                or a set of valid value pairs.
        """
        if type(relation) is set:
            R = lambda u, v: (u,v) in relation
        else:  # ok, relation is a function
            R = relation
        self.conflict[x].append((y, R))           # keep track for x
        R_inv = lambda u, v: R(v, u)
        self.conflict[y].append((x, R_inv))       # and symmetrically for y


    def add_unary_constraint(self, x, predicate):
        """Adds a unary constraint

        :param x: variable
        :param predicate: boolean function which returns True on accepted values
        """
        self.var[x] = {v for v in self.var[x] if predicate(v)}


    def select_var(self):
        """Chooses a branching variable.  
        In this implementation, the variable with the smallest domain is chosen.

        :returns: a branching variable name, or None if all variables are assigned.
        """
        x = None
        for y in self.var:
            if (self.assign[y] is None and
                (x is None or
                 len(self.var[y]) < len(self.var[x]))):
                x = y
        return x

    # -------------------------------- solving with backward check

    def backward_check(self, x, u):
        """Tests if assigning x := u would be coherent with
        all the already assigned variables
        """
        for y, rel in self.conflict[x]:
            v = self.assign[y] 
            if v is not None and not rel(u, v):
                return False   # conflict detected
        return True


    def solve_w_backward_check(self):
        """Solves the constraint program by backtracking
        using backward check to ensure consistency
        of the solution.

        :returns: a dictionary of variables to values 
        satisfying all constraints or None if none exists.
        """
        x = self.select_var()          # branching variable
        if x is None:
            self.dump.close()
            return self.assign         # we found a solution
        for u in self.var[x]:          # try all possible values for x
            if self.backward_check(x, u):
                self.assign[x] = u     # assign x := u
                self.dump.enter("{}:={}".format(x, u))
                sol = self.solve_w_backward_check()  
                self.dump.leave()
                if sol:                #recursive call succeeded ?
                    return sol
                self.assign[x] = None  # clean up
        return None                    # too bad, no solution found


    # -------------------------------- solving with forward check

    def forward_check(self, x):
        """x has been assigned to the value u.
        Restrict the domain of the related variables to
        the support of x. The support is defined as 
        the set of values in the domain of y
        which satisfy the constraint with x.

        :returns: the set of affected variables.
        """
        Q = set()
        u = self.assign[x]
        for y, rel in self.conflict[x]:
            if self.assign[y] is None:
                support = {v for v in self.var[y] if rel(u, v)}
                if len(support) < len(self.var[x]):
                    Q.add(y)
                self.var[y] = support
        return Q


    def save_context(self):
        """Save the domains for later restoration
        """
        self.context.append(self.var)
        self.var = {x: self.var[x].copy() for x in self.var}
        # we need to copy the sets so they can be modified without
        # modifying the previous ones

    def restore_context(self):
        """Restore domains as they were at the last save.
        """
        self.var = self.context.pop()

    def solve_w_forward_check(self):
        """Solves the constraint program with forward check
        """
        x = self.select_var()
        if x is None:
            self.dump.close()
            return self.assign
        for u in self.var[x]:
            self.save_context()     # save before domains are reduced
            self.assign[x] = u
            self.forward_check(x)
            self.dump.enter("{}:={}".format(x, u))
            sol = self.solve_w_forward_check()
            self.dump.leave()
            self.restore_context()  # clean up
            if sol:
                return sol
            self.assign[x] = None
        return None


    # -------------------------------- solving with arc consistency

    def has_support(self, u, y, rel_yx):
        """test if there is a value in the domain of y which
        satisfies the constraint with a variable x, 
        given x is assigned to value u.
        """
        v = self.assign[y]
        if v is not None:
            return rel_yx(v, u)
        # else
        for v in self.var[y]:
            if rel_yx(v, u):
                return True
        return False

    def revise(self, x, y, rel_yx):
        """the domain of y has just reduced.
        We want that all values in the domain of x
        have a support in y.
        Do we need to reduce the domain of x?
    
        :returns: True if the domain of x has been reduced.
        :complexity: O(t) where t is the upper bound on the domain sizes
        """
        to_remove = set()  # we cannot remove values for a set during iteration
        for u in self.var[x]:
            if not self.has_support(u, y, rel_yx):
                to_remove.add(u)
        if to_remove:
            self.var[x] -= to_remove
            # self.var[x] = self.var[x] - to_remove
            return True
        # else:
        return False

    def AC3(self, Q):
        """Maintain arc consistency after the domain of the variables in Q
        might have been reduced.

        :complexity: O(mt^3) where m is the number of constraints and t an
                upper bound on the domain size. 
        """
        while Q:
            y = Q.pop()
            for x, rel_yx in self.conflict[y]:
                if self.assign[x] is None:         # revise only free variables
                    if self.revise(x, y, rel_yx):
                        Q.add(x)


    def solve_w_arconsistency(self):
        """Solves the constraint program with arc consistency
        """
        self.save_context()
        self.AC3({x for x in self.var})  # establish arc consistency
        sol = self._solve_w_AC()
        self.restore_context() 
        return sol


    def _solve_w_AC(self):
        """Internal function, should be called only from the previous one
        """
        x = self.select_var()
        if x is None:
            self.dump.close()
            return self.assign
        dom = self.var[x]
        for u in dom:
            self.save_context()
            self.assign[x] = u
            Q = self.forward_check(x)
            self.AC3(Q)
            self.dump.enter("{}:={}".format(x, u))
            sol = self._solve_w_AC()
            self.dump.leave()
            self.restore_context() 
            if sol:
                return sol
            self.assign[x] = None
        return None

    # ---------------------------- iterate over all solutions


    def solve_iterator(self):
        """iterate over all solutions
        """
        x = self.select_var()
        if x is None:
            yield self.assign              # iterator
        else:
            for u in self.var[x]:
                self.save_context()
                self.assign[x] = u
                self.AC3({x})
                for sol in self._solve_w_AC():
                    yield sol              # iterator
                self.restore_context() 
                self.assign[x] = None

    # -------------------------- comment out your favorite method

    def solve(self):
        # return self.solve_w_backward_check()
        # return self.solve_w_forward_check()
        return self.solve_w_arconsistency()

    # -------------------------- find lexicographically smallest solution

    def solve_lex_smallest(self):
        """find lexicographically smallest solution
        by looping over all variables in natural order.
        and using binary search on the domain

        :returns: a solution opt such that for every solution sol different
                from opt there is a variable y such that opt[x] = sol[x]  for all variable x
                smaller than y and opt[y] < sol[y].
        :complexity: O(n log t) calls to solve, where n is the number of variables
                and t an upper bound on their domain size.        
        """
        if self.solve() is None:     # should feasible to start with
            return None
        var = [x for x in self.var]
        var.sort()                   # order the variables
        sol = {x: None for x in var}
        self.save_context()
        for x in var:                # loop over all variables
            dom = sorted(self.var[x])
            while len(dom) > 2:
                k = len(dom)         # divide domain
                first = dom[:k//2]
                second = dom[k//2:]
                self.var[x] = set(first)  # reduce to the earliest half with solution
                self.assign = {x: None for x in var}  # reset before each of multiple calls
                if self.solve() is None:              # to the resolution
                    dom = second
                else:
                    dom = first
                self.var[x] = set(dom)
            sol[x] = dom[0]          # domain is single value now
        self.restore_context()
        return sol
