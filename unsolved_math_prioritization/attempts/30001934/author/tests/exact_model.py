"""Exact spanning-tree model. No floating-point arithmetic or assertions as guards."""
from fractions import Fraction
from itertools import combinations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def graph(n, edges):
    require(type(n) is int and n >= 1, 'positive integer vertex count required')
    es = tuple(tuple(e) for e in edges)
    require(all(len(e) == 2 and all(type(v) is int and 0 <= v < n for v in e) for e in es), 'invalid endpoint')
    return n, es


def is_tree(n, edges, indices):
    if len(indices) != n - 1 or len(set(indices)) != len(indices):
        return False
    if any(type(i) is not int or not 0 <= i < len(edges) for i in indices):
        return False
    parent = list(range(n))
    def root(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for i in indices:
        u, v = edges[i]
        a, b = root(u), root(v)
        if a == b:
            return False
        parent[a] = b
    return True


def trees(n, edges):
    graph(n, edges)
    return tuple(c for c in combinations(range(len(edges)), n-1) if is_tree(n, edges, c))


def constraints(n, edges):
    """Nonempty proper vertex sets, plus singletons, hence loops are constrained."""
    return tuple((s, s.bit_count()-1, tuple(i for i,(u,v) in enumerate(edges) if (s>>u)&1 and (s>>v)&1))
                 for s in range(1, (1<<n)-1))


def member(n, edges, z, mass):
    graph(n, edges)
    require(len(z) == len(edges), 'coordinate count')
    if mass < 0 or any(a < 0 for a in z) or sum(z) != mass*(n-1):
        return False
    if mass == 0:
        return all(a == 0 for a in z)
    if any(z[i] != 0 for i,(u,v) in enumerate(edges) if u == v):
        return False
    return all(sum(z[i] for i in ids) <= mass*r for _,r,ids in constraints(n, edges))


def maximum(n, edges, w, k, tree):
    graph(n, edges)
    require(type(k) is int and k > 0, 'positive integral k')
    require(all(type(a) is int for a in w), 'integral w required')
    require(member(n, edges, w, k), 'w not in kP')
    require(is_tree(n, edges, tree), 'not a spanning tree')
    ts = set(tree)
    bounds = [(Fraction(k), ('mass',))]
    bounds += [(Fraction(w[i]), ('edge', i)) for i in tree]
    for s, r, ids in constraints(n, edges):
        d = r - sum(i in ts for i in ids)
        if d > 0:
            bounds.append((Fraction(k*r-sum(w[i] for i in ids), d), ('subset', s)))
    return min(bounds)
