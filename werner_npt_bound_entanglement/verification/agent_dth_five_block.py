#!/usr/bin/env python3
"""Exact local-block audit for the five-replica DTH lift.

This script uses only the Python standard library.  It realizes the local
S_5 modules [4,1], [4,1], [3,2] inside the point, point, and two-subset
permutation modules.  Sparse vectors have rational coefficients throughout.

The first checkpoint reconstructs the cloud obstruction xi and verifies its
source symmetries, first Pluecker-kernel condition, norm, and both the strong
and minimal-DTH lifted-witness expectations.
"""

from fractions import Fraction as F
from itertools import combinations, permutations


LABELS = tuple(range(5))
EDGES = tuple(combinations(LABELS, 2))


def add(*vs):
    out = {}
    for v in vs:
        for k, x in v.items():
            out[k] = out.get(k, F(0)) + x
            if not out[k]:
                del out[k]
    return out


def scale(c, v):
    c = F(c)
    return {k: c * x for k, x in v.items() if c * x}


def inner(v, w):
    # All vectors constructed here are real and rational.
    if len(v) > len(w):
        v, w = w, v
    return sum((x * w.get(k, F(0)) for k, x in v.items()), F(0))


# Arithmetic in Q(sqrt(231)), represented by pairs a+b sqrt(231).
def qadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def qneg(x):
    return (-x[0], -x[1])


def qmul(x, y):
    return (x[0] * y[0] + 231 * x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


def qinv(x):
    den = x[0] * x[0] - 231 * x[1] * x[1]
    assert den
    return (x[0] / den, -x[1] / den)


def quadratic_rank(rows):
    """Gaussian rank over Q(sqrt(231)); rows is a mutable rectangular list."""
    a = [[(F(x[0]), F(x[1])) for x in row] for row in rows]
    if not a:
        return 0
    nr, nc = len(a), len(a[0])
    rank = 0
    for col in range(nc):
        pivot = next((i for i in range(rank, nr) if a[i][col] != (0, 0)), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = qinv(a[rank][col])
        a[rank] = [qmul(inv, x) for x in a[rank]]
        for i in range(nr):
            if i == rank or a[i][col] == (0, 0):
                continue
            c = a[i][col]
            a[i] = [qadd(x, qneg(qmul(c, y))) for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == nr:
            break
    return rank


def point(i):
    return {i: F(1)}


def edge(i, j):
    return {tuple(sorted((i, j))): F(1)}


def f(i):
    return add(point(i), scale(-1, point(4)))


def r(a, b, c, d):
    # r_{ab|cd}=e_{ac}-e_{ad}-e_{bc}+e_{bd}.
    return add(edge(a, c), scale(-1, edge(a, d)),
               scale(-1, edge(b, c)), edge(b, d))


def tensor3(x, y, z):
    return {
        (i, j, k): a * b * c
        for i, a in x.items()
        for j, b in y.items()
        for k, c in z.items()
        if a * b * c
    }


def perm_sign(p):
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inv & 1 else 1


def perm5_on_subset(p4):
    """Extend a permutation of 0,1,2,3 by fixing label 4."""
    return tuple(p4) + (4,)


def transposition(a, b):
    p = list(LABELS)
    p[a], p[b] = p[b], p[a]
    return tuple(p)


def apply_local_perm(v, site, p):
    out = {}
    for key, x in v.items():
        q = list(key)
        if site < 2:
            q[site] = p[q[site]]
        else:
            i, j = q[site]
            q[site] = tuple(sorted((p[i], p[j])))
        q = tuple(q)
        out[q] = out.get(q, F(0)) + x
    return {k: x for k, x in out.items() if x}


def apply_global_perm(v, p):
    out = v
    for site in range(3):
        out = apply_local_perm(out, site, p)
    return out


def local_antisym_pair(v, site, a, b):
    return scale(F(1, 2), add(v, scale(-1, apply_local_perm(v, site, transposition(a, b)))))


def local_antisym_triple(v, site, labels):
    out = {}
    labels = tuple(labels)
    for q in permutations(labels):
        p = list(LABELS)
        for old, new in zip(labels, q):
            p[old] = new
        out = add(out, scale(perm_sign(tuple(labels.index(x) for x in q)),
                             apply_local_perm(v, site, tuple(p))))
    return scale(F(1, 6), out)


def product_pair_antisym(v, a, b):
    out = v
    for site in range(3):
        out = local_antisym_pair(out, site, a, b)
    return out


def product_triple_antisym(v, labels):
    out = v
    for site in range(3):
        out = local_antisym_triple(out, site, labels)
    return out


def global_A4(v):
    out = {}
    for p4 in permutations(range(4)):
        out = add(out, scale(perm_sign(p4), apply_global_perm(v, perm5_on_subset(p4))))
    return scale(F(1, 24), out)


def O0(v, first):
    """Minimal witness O0 on replicas (first, partner, 4).

    first=0 means O0_125 and first=2 means O0_345.  The unused partner is
    1 or 3 respectively; only the first leg swaps with z replica 4.
    """
    return add(scale(F(1, 4), v), scale(-2, product_pair_antisym(v, first, 4)))


def Ostrong(v, first):
    return add(O0(v, first), scale(F(27, 4), product_triple_antisym(v, (first, first + 1, 4))))


def lifted(v, op):
    return scale(F(1, 2), add(op(v, 0), op(v, 2)))


def J5(v):
    """Cross Jucys--Murphy operator sum_{r=1}^4 F_{r5}."""
    return add(*(apply_global_perm(v, transposition(r, 4)) for r in range(4)))


def build_xi():
    f0, f1, f2, f3 = (f(i) for i in range(4))
    r0123 = r(0, 1, 2, 3)
    r0124 = r(0, 1, 2, 4)
    r0423 = r(0, 4, 2, 3)
    return add(
        scale(-1, add(tensor3(f1, f1, r0123), tensor3(f3, f3, r0123))),
        add(tensor3(f3, f3, r0124), scale(-1, tensor3(f2, f2, r0124))),
        add(tensor3(f1, f1, r0423), scale(-1, tensor3(f0, f0, r0423))),
    )


def replica_state(key, replica):
    """The three-site 0/1 physical basis state at one replica.

    The point and edge permutation modules are embedded as the weight-one and
    weight-two binary-word permutation modules, respectively.
    """
    i, j, e = key
    return (int(replica == i), int(replica == j), int(replica in e))


def contract_replicas(v, contracted, retained):
    """Holomorphically contract two full-H replica indices with delta.

    This is the literal replica contraction on the real binary embedding.  On
    a physical monomial w12 w34 z5, contracting replicas 3 and 5 returns
    w12 tensor (W^T z)_4.  For real skew W this is the requested support
    contraction up to sign; the complex dagger-versus-transpose issue is
    discussed in the companion note.
    """
    p, q = contracted
    out = {}
    for key, x in v.items():
        if replica_state(key, p) != replica_state(key, q):
            continue
        new_key = tuple(replica_state(key, r) for r in retained)
        out[new_key] = out.get(new_key, F(0)) + x
    return {k: x for k, x in out.items() if x}


def segre_flattening_rank(xip, xim):
    """Rank of zeta'=(sqrt(231) xi_+ + 11 xi_-) across replicas 1234:5."""
    keys = set(xip) | set(xim)
    states = tuple((a, b, c) for a in range(2) for b in range(2) for c in range(2))
    col = {x: i for i, x in enumerate(states)}
    row_keys = sorted({tuple(replica_state(k, r) for r in range(4)) for k in keys})
    row = {x: i for i, x in enumerate(row_keys)}
    matrix = [[(F(0), F(0)) for _ in states] for _ in row_keys]
    for k in keys:
        st = tuple(replica_state(k, r) for r in range(5))
        # zeta' coefficient is 11*xi_- + sqrt(231)*xi_+.
        x = (11 * xim.get(k, F(0)), xip.get(k, F(0)))
        i, j = row[st[:4]], col[st[4]]
        matrix[i][j] = qadd(matrix[i][j], x)
    return quadratic_rank(matrix)


def assert_zero(v, label):
    assert not v, f"{label} is nonzero: {len(v)} sparse entries"


def main():
    xi = build_xi()
    n2 = inner(xi, xi)
    assert n2 == 64, n2

    assert_zero(add(apply_global_perm(xi, transposition(0, 1)), xi), "(12) xi + xi")
    assert_zero(add(apply_global_perm(xi, transposition(2, 3)), xi), "(34) xi + xi")
    assert_zero(add(apply_global_perm(xi, (2, 3, 0, 1, 4)), scale(-1, xi)),
                "(13)(24) xi - xi")
    assert_zero(global_A4(xi), "A4 xi")

    e0 = inner(xi, O0(xi, 0))
    e2 = inner(xi, O0(xi, 2))
    es0 = inner(xi, Ostrong(xi, 0))
    es2 = inner(xi, Ostrong(xi, 2))
    assert es0 == es2 == -16, (es0, es2)
    omega_left = product_triple_antisym(xi, (0, 1, 4))
    omega_right = product_triple_antisym(xi, (2, 3, 4))
    assert_zero(omega_left, "Omega(125) xi")
    assert_zero(omega_right, "Omega(345) xi")

    supp_right = contract_replicas(xi, (2, 4), (0, 1, 3))
    supp_left = contract_replicas(xi, (0, 4), (2, 3, 1))
    j5_exp = inner(xi, J5(xi))
    jxi = J5(xi)
    assert_zero(add(J5(jxi), scale(-4, xi)), "(J5^2-4) xi")
    xip = scale(F(1, 2), add(xi, scale(F(1, 2), jxi)))
    xim = scale(F(1, 2), add(xi, scale(F(-1, 2), jxi)))
    assert_zero(add(xip, xim, scale(-1, xi)), "xi+ + xi- - xi")
    assert inner(xip, xip) == 22
    assert inner(xim, xim) == 42
    assert inner(xip, xim) == 0
    assert inner(xip, J5(xip)) == 44
    assert inner(xim, J5(xim)) == -84
    assert_zero(global_A4(xip), "A4 xi+")
    assert_zero(global_A4(xim), "A4 xi-")
    for branch, name in ((xip, "xi+"), (xim, "xi-")):
        assert_zero(add(apply_global_perm(branch, transposition(0, 1)), branch),
                    f"F12 {name}+{name}")
        assert_zero(add(apply_global_perm(branch, transposition(2, 3)), branch),
                    f"F34 {name}+{name}")
        assert_zero(add(apply_global_perm(branch, (2, 3, 0, 1, 4)), scale(-1, branch)),
                    f"pair exchange {name}-{name}")
        assert_zero(product_triple_antisym(branch, (0, 1, 4)), f"Omega125 {name}")
        assert_zero(product_triple_antisym(branch, (2, 3, 4)), f"Omega345 {name}")
    qxip = lifted(xip, O0)
    qxim = lifted(xim, O0)
    qpp = inner(xip, qxip)
    qpm = inner(xip, qxim)
    qmm = inner(xim, qxim)
    zeta_norm2 = 21 * inner(xip, xip) + 11 * inner(xim, xim)
    zeta_j5 = 21 * inner(xip, J5(xip)) + 11 * inner(xim, J5(xim))
    zeta_q_rational = 21 * qpp + 11 * qmm
    zeta_q_sqrt231 = 2 * qpm
    assert zeta_norm2 == 924
    assert zeta_j5 == 0
    assert zeta_q_rational == 0
    assert zeta_q_sqrt231 / zeta_norm2 == F(-1, 64)
    zeta_segre_rank = segre_flattening_rank(xip, xim)
    assert zeta_segre_rank == 7

    print("exact five-replica [4,1]x[4,1]x[3,2] audit")
    print(f"||xi||^2 = {n2}")
    print("F12 xi=-xi, F34 xi=-xi, F(13)(24) xi=xi")
    print("A4 xi=0")
    print(f"<xi,Ostrong_125 xi> = {es0}")
    print(f"<xi,Ostrong_345 xi> = {es2}")
    print(f"<xi,O0_125 xi> = {e0}")
    print(f"<xi,O0_345 xi> = {e2}")
    print(f"minimal lifted quotient = {(e0 + e2) / (2 * n2)}")
    print(f"||C_supp,right^hol xi||^2 = {inner(supp_right, supp_right)}")
    print(f"||C_supp,left^hol xi||^2 = {inner(supp_left, supp_left)}")
    print(f"<xi,J5 xi> = {j5_exp}")
    print("J5 branch masses: ||xi+||^2=22, ||xi-||^2=42")
    print(f"O0~ branch Gram = [[{qpp}, {qpm}], [{qpm}, {qmm}]]")
    print("zeta=sqrt(21)xi+ + sqrt(11)xi-:")
    print(f"  ||zeta||^2={zeta_norm2}, <zeta,J5 zeta>={zeta_j5}")
    print("  O0~ quotient = -sqrt(231)/64")
    print(f"  replica 1234:5 Segre flattening rank = {zeta_segre_rank}")


if __name__ == "__main__":
    main()
