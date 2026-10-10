#!/usr/bin/env python3
"""Exact, finite controls for the partial results; not a continuum solver."""
from fractions import Fraction as F
import json


def radial(A, B, s, x):
    return A * (1-x/s) if x <= s else B*(x-s)/(1-s)


def gaussian(A, b):
    """Small exact Gauss-Jordan solve, with singularity detection."""
    a = [list(map(F, row)) + [F(rhs)] for row, rhs in zip(A, b)]
    n = len(a)
    for col in range(n):
        pivot = next((i for i in range(col, n) if a[i][col]), None)
        assert pivot is not None, 'singular matrix'
        a[col], a[pivot] = a[pivot], a[col]
        d = a[col][col]
        a[col] = [x/d for x in a[col]]
        for i in range(n):
            if i != col and a[i][col]:
                d = a[i][col]
                a[i] = [x-d*y for x, y in zip(a[i], a[col])]
    return [row[-1] for row in a]


def check_radial():
    count = 0
    for A in map(F, range(-4, 1)):
        for B in map(F, range(1, 5)):
            for k in range(1, 10):
                s = F(k, 10)
                h1 = A*(1-s)+B*s
                if h1 <= 0:
                    continue
                left, right = -A/s, B/(1-s)
                assert right-left == h1/(s*(1-s)) > 0
                assert radial(A, B, s, F(0)) == A
                assert radial(A, B, s, s) == 0
                assert radial(A, B, s, F(1)) == B
                for j in range(21):
                    x = F(j, 20)
                    w, h = radial(A, B, s, x), A*(1-x)+B*x
                    assert w <= h
                    if x <= s:
                        assert w <= 0
                        assert h-w == h1*x/s
                    else:
                        assert h-w == h1*(1-x)/(1-s)
                    count += 1
    # Negative control: forcing the knot to zero when h1<0 is not convex.
    A, B, s = F(-3), F(1), F(1, 2)
    assert B/(1-s)-(-A/s) < 0
    # Positive normalized example used by the finite control.
    assert radial(F(0), F(1), F(1, 2), F(1, 4)) == 0
    return {'exact_parameter_point_checks': count,
            'negative_slope_jump_control': 'passed'}


def check_graph_slit():
    """Periodic cylinder x=i/4, y=j/8, A=0, B=1; slit j=0,i<=2.

    Weighted graph Laplacian uses inverse squared mesh spacings. The result
    verifies only the stated 22-unknown finite Dirichlet problem.
    """
    nx, ny, tip = 4, 8, 2
    nodes = [(i, j) for i in range(1, nx) for j in range(ny)]
    slit = {(i, 0) for i in range(1, tip+1)}
    free = [n for n in nodes if n not in slit]
    index = {p: k for k, p in enumerate(free)}
    n = len(free)
    A, b = [[F(0) for _ in free] for _ in free], [F(0)]*n
    for p, k in index.items():
        i, j = p
        neighbors = [((i-1,j), nx*nx), ((i+1,j), nx*nx),
                     ((i,(j-1)%ny), ny*ny), ((i,(j+1)%ny), ny*ny)]
        for q, weight in neighbors:
            A[k][k] += weight
            if q in index:
                A[k][index[q]] -= weight
            elif q[0] == nx:
                b[k] += weight
            else:
                assert q in slit or q[0] == 0
    sol = gaussian(A, b)
    for row, rhs in zip(A, b):
        assert sum(a*x for a, x in zip(row, sol)) == rhs
    values = dict(zip(free, sol)) | {p:F(0) for p in slit}
    for (i,j), value in values.items():
        assert 0 <= value <= F(i,nx)
        if (i,j) not in slit:
            assert value > 0
        w = radial(F(0), F(1), F(tip,nx), F(i,nx))
        assert value >= w
    target = values[(1,4)]
    assert F(0) < target < F(1,4)
    # At grounded slit nodes the distributional graph Laplacian is positive.
    for i,j in slit:
        def value(q):
            return F(q[0]//nx) if q[0] in (0,nx) else values[q]
        lap = nx*nx*(value((i-1,j))+value((i+1,j)))
        lap += ny*ny*(value((i,(j-1)%ny))+value((i,(j+1)%ny)))
        assert lap > 0
    return {'unknowns': n, 'exact_residuals': 'zero',
            'target': '(i,j)=(1,4)', 'slit_value': str(target),
            'radial_value': '0', 'harmonic_envelope': '1/4',
            'scope': 'finite graph control only; no continuum optimality claim'}


def main():
    report = {'status': 'passed', 'arithmetic': 'Python fractions.Fraction',
              'radial': check_radial(), 'finite_slit': check_graph_slit(),
              'unverified_by_code': [
                  'continuum potential-theoretic proofs',
                  'optimal free curve or sharp extremal value',
                  'general boundary regularity', 'literature completeness']}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
