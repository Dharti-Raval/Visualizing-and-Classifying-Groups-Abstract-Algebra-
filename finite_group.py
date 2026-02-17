class FiniteGroup:
    def __init__(self, name, elements, op, identity):
        self.name = name
        self.elements = list(elements)
        self.op = op
        self.e = identity
        self.order = len(self.elements)
        self.index = {x:i for i,x in enumerate(self.elements)}
        # compute inverses
        self._inv = {}
        for a in self.elements:
            for b in self.elements:
                if op(a,b) == identity and op(b,a) == identity:
                    self._inv[a] = b
                    break

    def multiply(self, a, b):
        return self.op(a,b)

    def inverse(self, a):
        return self._inv.get(a)

    def cayley_table(self):
        n = self.order
        mat = [[self.op(self.elements[i], self.elements[j]) for j in range(n)] for i in range(n)]
        return mat

    def is_abelian(self):
        for a in self.elements:
            for b in self.elements:
                if self.op(a,b) != self.op(b,a):
                    return False
        return True

    def center(self):
        return [a for a in self.elements if all(self.op(a,b)==self.op(b,a) for b in self.elements)]

    def conjugacy_classes(self):
        seen = set()
        classes = []
        for a in self.elements:
            if a in seen:
                continue
            cls = set(self.op(g, self.op(a, self.inverse(g))) for g in self.elements)
            classes.append(sorted(cls, key=lambda x: str(x)))
            seen |= cls
        return classes

    def element_order(self, a):
        cur = self.e
        for n in range(1, self.order+1):
            cur = self.op(cur, a)
            if cur == self.e:
                return n
        return None

    def element_orders(self):
        return {a: self.element_order(a) for a in self.elements}

    def powers_of(self, a):
        cur = self.e
        seen = {cur}
        while True:
            cur = self.op(cur, a)
            if cur in seen:
                break
            seen.add(cur)
        return sorted(seen, key=lambda x: str(x))

    def is_cyclic(self):
        for a in self.elements:
            if len(self.powers_of(a)) == self.order:
                return True
        return False

    def all_subgroups(self, limit=16):
        if self.order > limit:
            return None
        subs = set()
        for r in range(1, len(self.elements)+1):
            for gens in itertools.combinations(self.elements, r):
                S = {self.e}
                changed = True
                while changed:
                    changed = False
                    for x in list(S):
                        for g in gens:
                            a = self.op(x,g)
                            b = self.op(g,x)
                            if a not in S:
                                S.add(a); changed = True
                            if b not in S:
                                S.add(b); changed = True
                subs.add(tuple(sorted(S, key=lambda x: str(x))))
        return [list(s) for s in subs]

    def normal_subgroups(self):
        subs = self.all_subgroups()
        if subs is None:
            return None
        normals = []
        for H in subs:
            Hset = set(H)
            ok = True
            for g in self.elements:
                for h in H:
                    conj = self.op(g, self.op(h, self.inverse(g)))
                    if conj not in Hset:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                normals.append(H)
        return normals

    def commutator(self, a, b):
        ainv = self.inverse(a); binv = self.inverse(b)
        return self.op(self.op(ainv, binv), self.op(a, b))

    def commutator_subgroup(self):
        gens = set(self.commutator(a,b) for a in self.elements for b in self.elements)
        S = {self.e}
        changed = True
        while changed:
            changed = False
            for x in list(S):
                for g in gens:
                    a = self.op(x,g); b = self.op(g,x)
                    if a not in S:
                        S.add(a); changed = True
                    if b not in S:
                        S.add(b); changed = True
        return sorted(S, key=lambda x: str(x))

    def derived_series(self, max_iter=10):
        series = [sorted(self.elements, key=lambda x: str(x))]
        current_set = set(self.elements)
        for _ in range(max_iter):
            comm = set(self.commutator_subgroup())
            series.append(sorted(comm, key=lambda x: str(x)))
            if comm == {self.e} or comm == current_set:
                break
            current_set = comm
        return series

    def is_solvable(self):
        series = self.derived_series()
        return series and set(series[-1]) == {self.e}

    def cayley_graph(self, generators):
        G = nx.Graph()
        for v in self.elements:
            G.add_node(v)
        for a in self.elements:
            for g in generators:
                b = self.op(a,g)
                G.add_edge(a,b)
        return G
