"""Independent finite checks of specific family-142 algebraic mechanisms.

These tests are not a proof of the full norm solver or prime-field algorithm.
Run with Python >=3.10; only the standard library is used.
"""
from fractions import Fraction
import json
from pathlib import Path


def mm(a, b, p):
    return [[sum(x*y for x, y in zip(row, col)) % p
             for col in zip(*b)] for row in a]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def rref(a, p):
    a = [[x % p for x in row] for row in a]
    if not a:
        return a, []
    piv = []
    r = 0
    for c in range(len(a[0])):
        k = next((k for k in range(r, len(a)) if a[k][c]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        inv = pow(a[r][c], -1, p)
        a[r] = [x*inv % p for x in a[r]]
        for k in range(len(a)):
            if k != r and a[k][c]:
                t = a[k][c]
                a[k] = [(x-t*y) % p for x, y in zip(a[k], a[r])]
        piv.append(c)
        r += 1
        if r == len(a):
            break
    return a, piv


def kernel(a, n, p):
    a, piv = rref(a, p)
    basis = []
    for c in range(n):
        if c not in piv:
            v = [int(j == c) for j in range(n)]
            for k, j in enumerate(piv):
                v[j] = -a[k][c] % p
            basis.append(v)
    return basis


def invmat(a, p):
    n = len(a)
    rr, piv = rref([row + erow for row, erow in zip(a, eye(n))], p)
    assert piv[:n] == list(range(n))
    return [row[n:] for row in rr]


def mpow(a, n, p):
    if n < 0:
        return mpow(invmat(a, p), -n, p)
    b = eye(len(a))
    while n:
        if n % 2:
            b = mm(b, a, p)
        a = mm(a, a, p)
        n //= 2
    return b


def scalar(a, s, p):
    return [[s*x % p for x in row] for row in a]


def compositions(n):
    if n == 0:
        yield ()
    else:
        for j in range(1, n+1):
            for tail in compositions(n-j):
                yield (j,) + tail


def parabolic_checks():
    cases = 0
    for p in (2, 3, 5):
        for n in range(1, 8):
            # A deterministic invertible conjugation, with both directions mixed.
            lo, up = eye(n), eye(n)
            for i in range(n):
                for j in range(i):
                    lo[i][j] = (1+i+2*j) % p
                    up[j][i] = (2+i+3*j) % p
            c = mm(lo, up, p)
            ci = invmat(c, p)
            for blocks in compositions(n):
                block = []
                for i, size in enumerate(blocks):
                    block += [i]*size
                basis = []
                for i in range(n):
                    for j in range(n):
                        if block[i] <= block[j]:
                            e = [[0]*n for _ in range(n)]
                            e[i][j] = 1
                            basis.append(mm(mm(c, e, p), ci, p))
                tr = [[sum(a[i][j]*b[j][i] for i in range(n)
                           for j in range(n)) % p for b in basis] for a in basis]
                nk = kernel(tr, len(basis), p)
                nb = [[[sum(co*b[i][j] for co, b in zip(v, basis)) % p
                        for j in range(n)] for i in range(n)] for v in nk]
                u = kernel([row for a in nb for row in a], n, p)
                assert len(u) == blocks[0]
                v = u[0]
                j = next(j for j, x in enumerate(v) if x)
                w = [0]*n
                w[j] = pow(v[j], -1, p)
                a0 = [[x*y % p for y in w] for x in v]
                assert mm(a0, a0, p) == a0
                assert len(rref(a0, p)[1]) == 1
                rows = [[x for row in b for x in row] for b in basis]
                assert len(rref(rows, p)[1]) == len(rref(rows + [[x for row in a0 for x in row]], p)[1])
                # In particular, traces may vanish on 1 when p divides n;
                # the matrix trace pairing used here remains nondegenerate.
                cases += 1
    return cases


def local_model_checks():
    cases = 0
    for q, p in ((3, 103), (5, 101), (7, 113)):
        zeta = next(z for z in range(2, p) if pow(z, q, p) == 1)
        for f in (1, 2, p-1):
            for r in (1, 3, p-2):
                y = [[0]*q for _ in range(q)]
                for j in range(q-1):
                    y[j+1][j] = 1
                y[0][-1] = f
                d = [[int(i == j)*pow(zeta, j, p)*r % p
                      for j in range(q)] for i in range(q)]
                for w in range(-4, 5):
                    v = mm(mpow(y, w, p), d, p)
                    assert mm(v, y, p) == scalar(mm(y, v, p), zeta, p)
                    g = pow(f, w, p)*pow(r, q, p) % p
                    assert mpow(v, q, p) == scalar(eye(q), g, p)
                    cases += 1
                # The unramified and infinity diagonal/weighted-shift model.
                for g in (1, 4, p-3):
                    yy = [[int(i == j)*pow(zeta, -j, p)*r % p
                           for j in range(q)] for i in range(q)]
                    vv = [[0]*q for _ in range(q)]
                    for j in range(q-1):
                        vv[j+1][j] = 1
                    vv[0][-1] = g
                    assert mm(vv, yy, p) == scalar(mm(yy, vv, p), zeta, p)
                    assert mpow(yy, q, p) == scalar(eye(q), pow(r, q, p), p)
                    assert mpow(vv, q, p) == scalar(eye(q), g, p)
                    cases += 1
    return cases


def lambda_divide(a):
    """Divide an augmentation-lattice vector by 1-sigma, if integral."""
    assert sum(a) == 0
    w = [0]
    for x in a[1:]:
        w.append(w[-1]+x)
    mean = Fraction(sum(w), len(w))
    if mean.denominator != 1:
        return None
    ans = [int(x-mean) for x in w]
    assert sum(ans) == 0
    assert [ans[j]-ans[(j-1) % len(ans)] for j in range(len(ans))] == a
    return ans


def lattice_checks():
    cases = 0
    for q in (3, 5, 7, 11):
        for r in range(1, 5):
            for a in (1, 2, q+1):
                n = q**r*a
                w = [-n, n] + [0]*(q-2)
                m = 1+(q-1)*r
                for t in range(1, m):
                    w = lambda_divide(w)
                    assert w is not None
                assert lambda_divide(w) is None
                cases += 1
    return cases


if __name__ == "__main__":
    results = {
        "parabolic_fiber_idempotent_cases": parabolic_checks(),
        "local_matrix_relation_cases": local_model_checks(),
        "infinity_lattice_obstruction_cases": lattice_checks(),
        "scope": "Finite algebraic checks; not a full proof or norm-solver implementation.",
    }
    dest = Path(__file__).with_name("geometric_checks_results.json")
    dest.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
