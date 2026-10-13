#!/usr/bin/env python3
"""Independent exact convex/duality audit; Python standard library only.

This code imports no candidate code. Small box least-squares problems are solved
by enumerating faces whose free columns are independent, with rational normal
equations. Every selected projection is certified against every binary vertex.
"""
from fractions import Fraction as Q
from itertools import product, combinations
import json
from pathlib import Path


def mat(rows):
    return [[Q(x) for x in row] for row in rows]


def vec(xs):
    return [Q(x) for x in xs]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def mv(a, x):
    return [dot(row, x) for row in a]


def tr(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[dot(row, col) for col in tr(b)] for row in a]


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def submat(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def addmat(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def rref(a):
    b = [row[:] for row in a]
    pivots = []
    r = 0
    for j in range(len(b[0]) if b else 0):
        k = next((k for k in range(r, len(b)) if b[k][j]), None)
        if k is None:
            continue
        b[r], b[k] = b[k], b[r]
        div = b[r][j]
        b[r] = [x / div for x in b[r]]
        for k in range(len(b)):
            if k != r:
                mul = b[k][j]
                b[k] = [x - mul * y for x, y in zip(b[k], b[r])]
        pivots.append(j)
        r += 1
        if r == len(b):
            break
    return b, pivots


def inv(a):
    n = len(a)
    b, pivots = rref([row[:] + erow for row, erow in zip(a, eye(n))])
    assert pivots[:n] == list(range(n))
    assert [row[:n] for row in b] == eye(n)
    return [row[n:] for row in b]


def projection_range(a):
    """Orthogonal projector onto the column space, exactly."""
    _, pivots = rref(a)
    m = len(a)
    if not pivots:
        return [[Q(0)] * m for _ in range(m)]
    b = [[row[j] for j in pivots] for row in a]
    return mm(mm(b, inv(mm(tr(b), b))), tr(b))


def binary_images(n):
    return [vec(x) for x in product((-1, 1), repeat=n)]


def box_projection(a, y):
    """Enumerate face minima; certify the result by the projection inequality."""
    n = len(a[0])
    best = None
    for status in product((-1, 0, 1), repeat=n):
        free = [j for j, v in enumerate(status) if v == 0]
        x = vec(status)
        rhs = [v - u for v, u in zip(y, mv(a, x))]
        if free:
            b = [[row[j] for j in free] for row in a]
            if len(rref(b)[1]) != len(free):
                continue
            z = mv(inv(mm(tr(b), b)), mv(tr(b), rhs))
            if any(abs(v) > 1 for v in z):
                continue
            for j, v in zip(free, z):
                x[j] = v
        p = mv(a, x)
        residual = [v - u for v, u in zip(y, p)]
        value = dot(residual, residual) / 2
        if best is None or value < best[0]:
            best = value, x, p, residual
    value, x, p, residual = best
    # This finite certificate proves p is the projection on the entire zonotope.
    for t in binary_images(n):
        assert dot(residual, [v - u for v, u in zip(mv(a, t), p)]) <= 0
    q = mv(tr(a), residual)
    assert dot(q, x) == sum(abs(v) for v in q)
    return best


def f(a, y, mu):
    r = [v - u for v, u in zip(mu, y)]
    return dot(r, r) / 2 + sum(abs(v) for v in mv(tr(a), mu))


def g(a, y, mu, p):
    r = mv(p, [v - u for v, u in zip(mu, y)])
    return dot(r, r) / 2 + sum(abs(v) for v in mv(tr(a), mu))


def show(xs):
    return [str(x) for x in xs]


def run():
    counts = dict(exact_box_projection_certificates=0, exact_dual_checks=0,
                  exact_perturbation_checks=0, exact_noiseless_identities=0,
                  exact_projected_identities=0, tomography_binary_images=0)
    examples = []
    cases = [
        ('scalar', [[1]], [[-2], [-1], [Q(-1, 2)], [0], [Q(1, 2)], [1], [2]]),
        ('weighted-row', [[1, 2]], [[-4], [-3], [-1], [0], [1], [3], [4]]),
        ('rank-deficient', [[1, 2], [2, 4]], [[1, 0], [1, 2], [4, 8], [-2, 1], [0, 0]]),
        ('zero-matrix', [[0, 0], [0, 0]], [[0, 0], [1, -2]]),
        ('invertible', [[1, 1], [0, 1]], [[0, 0], [1, 1], [Q(1, 2), -2], [3, 2]]),
        ('signed-matrix', [[1, -2, 0], [0, 1, 1]], [[0, 0], [1, 0], [Q(1, 2), Q(3, 2)], [4, -3]]),
    ]
    for name, rows, ys in cases:
        a = mat(rows)
        n, m = len(a[0]), len(a)
        p = projection_range(a)
        normal = submat(eye(m), p)
        at = tr(a)
        gram = mm(at, a)
        rowp = projection_range(at)
        # For symmetric Gram matrix, this independently constructs its MP inverse.
        normaln = submat(eye(n), rowp)
        pinv = submat(inv(addmat(gram, normaln)), normaln)
        assert mm(mm(gram, pinv), gram) == gram
        assert mm(mm(pinv, gram), pinv) == pinv
        assert tr(mm(gram, pinv)) == mm(gram, pinv)
        assert tr(mm(pinv, gram)) == mm(pinv, gram)
        assert mm(mm(a, pinv), at) == p
        for yy in ys:
            y = vec(yy)
            dval, x, image, mu = box_projection(a, y)
            counts['exact_box_projection_certificates'] += 1
            mu_projected = mv(p, mu)
            assert f(a, y, mu) == dot(y, y) / 2 - dval
            assert mv(at, mu) == mv(at, mu_projected)
            nu = mv(at, mu)
            rhs = [v - u for v, u in zip(mv(at, y), nu)]
            dual = dot(y, y) / 2 - dot(rhs, mv(pinv, rhs)) / 2 - sum(abs(v) for v in nu)
            assert dual == dval
            assert dual == dot(y, y) / 2 - g(a, y, mu_projected, p)
            counts['exact_dual_checks'] += 1
            pval = min(dot([v - u for v, u in zip(mv(a, t), y)],
                           [v - u for v, u in zip(mv(a, t), y)]) / 2
                       for t in binary_images(n))
            assert pval >= dval
            for perturbation in product((-1, 0, 1), repeat=m):
                w = [v + Q(u, 3) for v, u in zip(mu, perturbation)]
                delta = [v - u for v, u in zip(w, mu)]
                assert f(a, y, w) - f(a, y, mu) >= dot(delta, delta) / 2
                counts['exact_perturbation_checks'] += 1
            for j in range(m):
                z = [row[j] for row in normal]
                w = [v + 2 * u for v, u in zip(mu_projected, z)]
                assert mv(at, w) == nu
                assert g(a, y, w, p) == g(a, y, mu_projected, p)
            examples.append(dict(name=name, y=show(y), box_primal=str(dval),
                                 binary_primal=str(pval), binary_duality_gap=str(pval-dval),
                                 mu_unprojected=show(mu), mu_projected=show(mu_projected),
                                 box_solution=show(x)))
        for s in product((Q(-1), Q(-1, 2), Q(0), Q(1, 2), Q(1)), repeat=n):
            y = mv(a, s)
            for values in product((-1, 0, 1), repeat=m):
                mu = vec(values)
                q = mv(at, mu)
                correction = sum(abs(v) - u*v for u, v in zip(s, q))
                assert correction >= 0
                assert f(a, y, mu) - f(a, y, vec([0]*m)) == dot(mu, mu)/2 + correction
                counts['exact_noiseless_identities'] += 1
                pmu = mv(p, mu)
                assert g(a, y, mu, p)-g(a, y, vec([0]*m), p) == dot(pmu, pmu)/2 + correction
                counts['exact_projected_identities'] += 1
    # Independently construct all six 3x3 horizontal/vertical measurements.
    full = mat([[int(j//3 == i) for j in range(9)] for i in range(3)] +
               [[int(j%3 == i) for j in range(9)] for i in range(3)])
    reduced = full[:5]
    assert len(rref(reduced)[1]) == 5
    assert len(rref(full)[1]) == 5
    fiber = []
    fibers = {}
    for t in binary_images(9):
        y = tuple(mv(reduced, t))
        fibers.setdefault(y, []).append(t)
        assert mv(full, t)[5] == sum(y[:3]) - sum(y[3:])
        if y == tuple(vec([3, 1, 1, 3, 1])):
            fiber.append(t)
        counts['tomography_binary_images'] += 1
    assert len(fiber) == 2
    common = [ts[0] if all(v == ts[0] for v in ts) else Q(0) for ts in zip(*fiber)]
    assert common == vec([1,1,1,1,0,0,1,0,0])
    assert mv(reduced, common) == vec([3,1,1,3,1])
    unique = [t for t in binary_images(9) if mv(reduced,t) == vec([3,3,3,3,3])]
    assert len(unique) == 1 and unique[0] == vec([1]*9)
    # Both epsilon signs approach the exact scalar optimum; their signs disagree.
    for e in (Q(1,2), Q(1,10), Q(1,100), Q(1,10000)):
        assert f(mat([[1]]),vec([1]),vec([e]))-Q(1,2) == e*e/2
        assert f(mat([[1]]),vec([1]),vec([-e]))-Q(1,2) == 2*e+e*e/2
    # Binary uniqueness does not force a unique auxiliary box variable.
    a, y = mat([[1,2]]), vec([1])
    solutions = [t for t in binary_images(2) if mv(a,t) == y]
    assert solutions == [vec([-1,1])]
    assert mv(a,vec([1,0])) == y
    assert mv(a,vec([Q(1,5),Q(2,5)])) == y
    return dict(status='PASS', arithmetic='exact fractions; no candidate imports',
                counts=counts, tomography=dict(fibers=len(fibers),
                   singleton_fibers=sum(len(v)==1 for v in fibers.values()),
                   target_solutions=[show(t) for t in fiber],common=show(common)),
                examples=examples)


if __name__ == '__main__':
    result = run()
    output = Path(__file__).with_name('verification_results.json')
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],counts=result['counts'],
                         tomography=result['tomography']), indent=2))
