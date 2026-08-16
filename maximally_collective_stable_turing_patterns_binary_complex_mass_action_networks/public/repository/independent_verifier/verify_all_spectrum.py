#!/usr/bin/env python3
"""Verify the topology-wide all-spectrum principal-subsystem theorem."""
from __future__ import annotations
import argparse
import itertools
import sympy as sp
from stable_core import A_matrix, hurwitz_determinants


def tarjan_scc(adj: dict[int, set[int]], vertices: tuple[int, ...]) -> list[tuple[int, ...]]:
    index = 0
    stack: list[int] = []
    onstack: set[int] = set()
    indices: dict[int, int] = {}
    low: dict[int, int] = {}
    out: list[tuple[int, ...]] = []

    def visit(v: int) -> None:
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v); onstack.add(v)
        for w in adj.get(v, set()):
            if w not in vertices:
                continue
            if w not in indices:
                visit(w); low[v] = min(low[v], low[w])
            elif w in onstack:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            comp = []
            while True:
                w = stack.pop(); onstack.remove(w); comp.append(w)
                if w == v:
                    break
            out.append(tuple(sorted(comp)))

    for v in vertices:
        if v not in indices:
            visit(v)
    return out


def interaction_adjacency(A: sp.Matrix) -> dict[int, set[int]]:
    # edge j -> i when A_ij is nonzero
    n = A.rows
    return {j: {i for i in range(n) if i != j and A[i, j] != 0} for j in range(n)}


def classify_component(m: int, comp: tuple[int, ...]) -> str:
    S = set(comp)
    if len(S) == 1:
        return "negative-singleton"
    boundary = {0, m - 1, m}
    if S <= boundary:
        return "boundary-triad-principal"
    if S == set(range(0, m - 1)):
        return "long-cycle-X1-to-Xm-1"
    if S == set(range(1, m)):
        return "long-cycle-X2-to-Xm"
    raise AssertionError(f"unclassified SCC for m={m}: {sorted(i+1 for i in S)}")


def exact_hurwitz(M: sp.Matrix) -> bool:
    lam = sp.symbols("lambda")
    p = M.charpoly(lam).as_poly()
    coeffs = p.all_coeffs()
    if coeffs[0] != 1:
        coeffs = [sp.factor(x / coeffs[0]) for x in coeffs]
    return all(sp.factor(d) > 0 for d in hurwitz_determinants(coeffs))


def symbolic_boundary_certificate() -> None:
    a, b, h1, hm, hz, lam = sp.symbols("a b h1 hm hz lambda", positive=True)
    T = sp.Matrix([
        [-(a+b)*h1, -b*hm, 2*b*hz],
        [(2*a-b)*h1, -(4*a+b)*hm, 2*b*hz],
        [2*b*h1, 2*b*hm, -4*b*hz],
    ])
    coeffs = T.charpoly(lam).all_coeffs()
    c1 = a*h1 + 4*a*hm + b*h1 + b*hm + 4*b*hz
    c2 = a*(4*a*h1*hm + 7*b*h1*hm + 4*b*h1*hz + 16*b*hm*hz)
    c3 = 16*a*a*b*h1*hm*hz
    assert [sp.expand(x) for x in coeffs] == [1, sp.expand(c1), sp.expand(c2), sp.expand(c3)]
    gap = sp.Poly(sp.expand(c1*c2-c3), a,b,h1,hm,hz)
    assert gap.terms() and all(coef > 0 for _, coef in gap.terms())
    # Every two-vertex principal boundary block has negative trace and positive determinant.
    for I in itertools.combinations(range(3), 2):
        M = T.extract(I, I)
        assert sp.Poly(-sp.trace(M), a,b,h1,hm,hz).terms()
        assert all(c > 0 for _,c in sp.Poly(sp.expand(M.det()), a,b,h1,hm,hz).terms())
    print(f"BOUNDARY_SYMBOLIC_PASS positive_gap_terms={len(gap.terms())}")


def verify_finite(m: int) -> None:
    # Two exact positive realizations, including the cancellation b=2a.
    parameter_sets = [
        (sp.Rational(3,2), sp.Rational(5,3), [sp.Rational(i+2, i+1) for i in range(m+1)]),
        (sp.Integer(1), sp.Integer(2), [sp.Integer(i+1) for i in range(m+1)]),
    ]
    for a,b,hs in parameter_sets:
        A = A_matrix(m,a,b) * sp.diag(*hs)
        adj = interaction_adjacency(A)
        category_counts: dict[str,int] = {}
        for q in range(1,m):
            for subset in itertools.combinations(range(m+1),q):
                comps = tarjan_scc(adj, subset)
                for comp in comps:
                    typ = classify_component(m,comp)
                    category_counts[typ] = category_counts.get(typ,0)+1
                    block=A.extract(comp,comp)
                    assert exact_hurwitz(block), (m,a,b,subset,comp,block.charpoly().as_expr())
        C=tuple(range(m))
        signed=sp.factor((-1)**m*A.extract(C,C).det())
        expected=sp.factor(-2*a**(m-1)*b*sp.prod(hs[:m]))
        assert signed==expected and signed<0
        print(f"ALL_SPECTRUM_FINITE_PASS m={m} a={a} b={b} categories={category_counts}")


def symbolic_core_determinant_regression() -> None:
    a,b=sp.symbols('a b', positive=True)
    for m in range(3,9):
        A=A_matrix(m,a,b)
        got=sp.factor((-1)**m*A[:m,:m].det(method='domain-ge'))
        assert got == -2*a**(m-1)*b
    print('CORE_DETERMINANT_RECURRENCE_REGRESSION_PASS m=3..8')


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument('m',nargs='*',type=int,default=[3,4,5,6,8])
    args=p.parse_args()
    symbolic_boundary_certificate()
    symbolic_core_determinant_regression()
    for m in args.m:
        verify_finite(m)


if __name__=='__main__':
    main()
