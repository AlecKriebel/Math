#!/usr/bin/env python3
"""Exact auxiliary group checks; no source files, network, or writes required."""
import itertools
import json
import os
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def matrix_mul(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n))
                       for j in range(n)) for i in range(n))


def identity(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def neg(a):
    return tuple(tuple(-x for x in row) for row in a)


def qmul(a, b):
    w, x, y, z = a
    v, r, s, t = b
    return (w*v-x*r-y*s-z*t, w*r+x*v+y*t-z*s,
            w*s-x*t+y*v+z*r, w*t+x*s-y*r+z*v)


def order(a, unit, mul, bound=16):
    value = unit
    for k in range(1, bound + 1):
        value = mul(value, a)
        if value == unit:
            return k
    raise RuntimeError("Element order exceeded exact expected bound")


def determinant3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def mv(a, v):
    return tuple(sum(a[i][k] * v[k] for k in range(len(v)))
                 for i in range(len(v)))


def transpose(a):
    return tuple(zip(*a))


def main():
    one = (1, 0, 0, 0)
    minus_one = (-1, 0, 0, 0)
    q8 = {tuple(s*int(i == j) for i in range(4))
          for j in range(4) for s in (-1, 1)}
    require(len(q8) == 8, "Q8 cardinality")
    require(all(qmul(a, b) in q8 for a in q8 for b in q8), "Q8 closure")
    require(all(qmul(qmul(a, b), c) == qmul(a, qmul(b, c))
                for a in q8 for b in q8 for c in q8), "Q8 associativity")
    require(all(qmul(one, a) == a == qmul(a, one) for a in q8), "Q8 identity")
    require(all(any(qmul(a, b) == one == qmul(b, a) for b in q8)
                for a in q8), "Q8 inverses")
    qorders = {a: order(a, one, qmul) for a in q8}
    require(sorted(qorders.values()) == [1, 2, 4, 4, 4, 4, 4, 4], "Q8 orders")
    centre = {a for a in q8 if all(qmul(a, b) == qmul(b, a) for b in q8)}
    require(centre == {one, minus_one}, "Q8 centre")
    require(any(qmul(a, b) != qmul(b, a) for a in q8 for b in q8), "Q8 nonabelian")

    i2 = identity(2)
    p = ((0, 1), (1, 0))
    d8 = set()
    for permutation in itertools.permutations(range(2)):
        for signs in itertools.product((-1, 1), repeat=2):
            d8.add(tuple(tuple(signs[j]*int(i == permutation[j])
                               for j in range(2)) for i in range(2)))
    require(len(d8) == 8, "signed symmetric group cardinality")
    require(all(matrix_mul(a, b) in d8 for a in d8 for b in d8), "signed closure")
    dorders = sorted(order(a, i2, matrix_mul) for a in d8)
    require(dorders == [1, 2, 2, 2, 2, 2, 4, 4], "signed group orders")
    require(any(matrix_mul(a, b) != matrix_mul(b, a) for a in d8 for b in d8),
            "signed group is nonabelian")

    v4 = {i2, neg(i2), p, neg(p)}
    preserving_link = {a for a in d8
                       if sum(a[0][j] for j in range(2))
                       * sum(a[1][j] for j in range(2)) == 1}
    require(preserving_link == v4, "linking-preserving signed subgroup")
    require(sorted(order(a, i2, matrix_mul) for a in v4) == [1, 2, 2, 2],
            "Dahm image is Klein four")
    basis_images = [i2, neg(i2), p, neg(p)]
    dahm = {a: basis_images[next(i for i, value in enumerate(a) if value)] for a in q8}
    require(all(dahm[qmul(a, b)] == matrix_mul(dahm[a], dahm[b])
                for a in q8 for b in q8), "64 Dahm homomorphism identities")
    require(set(dahm.values()) == v4, "Dahm surjectivity")
    kernel = {a for a in q8 if dahm[a] == i2}
    require(kernel == centre, "Dahm kernel equals central C2")
    require(all(qorders[a] == 4 for a in q8 if a not in centre),
            "each nontrivial image element has only order-four lifts")
    # A splitting would send a nonidentity order-two element to an order-two lift.
    require(not any(qorders[a] == 2 and dahm[a] != i2 for a in q8), "nonsplitting")

    i3 = identity(3)
    a3 = ((1, 0, 0), (0, -1, 0), (0, 0, -1))
    b3 = ((-1, 0, 0), (0, 0, 1), (0, 1, 0))
    k = {i3, a3, b3, matrix_mul(a3, b3)}
    require(len(k) == 4, "rotation stabilizer cardinality")
    require(all(determinant3(a) == 1 and matrix_mul(transpose(a), a) == i3
                for a in k), "rotation matrices belong to SO3")
    require(all(matrix_mul(a, b) in k for a in k for b in k), "rotation closure")
    require(sorted(order(a, i3, matrix_mul) for a in k) == [1, 2, 2, 2],
            "rotation stabilizer Klein four")
    # Centres are doubled to stay in integer arithmetic; oriented normals are exact.
    c1, c2 = (-1, 0, 0), (1, 0, 0)
    n1, n2 = (0, 0, 1), (0, 1, 0)
    require(mv(a3, c1) == c1 and mv(a3, c2) == c2, "orientation reversal fixes centres")
    require(mv(a3, n1) == tuple(-v for v in n1)
            and mv(a3, n2) == tuple(-v for v in n2), "both normal orientations reversed")
    require(mv(b3, c1) == c2 and mv(b3, c2) == c1, "exchange swaps centres")
    require(mv(b3, n1) == n2 and mv(b3, n2) == n1, "exchange preserves normal orientations")

    print(json.dumps({
        "status": "PASS", "uid": os.getuid(), "optimization": sys.flags.optimize,
        "q8_order_distribution": {str(n): list(qorders.values()).count(n) for n in (1,2,4)},
        "signed_order_distribution": {str(n): dorders.count(n) for n in (1,2,4)},
        "dahm_image_order": len(v4), "dahm_kernel_order": len(kernel),
        "q8_associativity_cases": 512, "dahm_homomorphism_cases": 64,
        "scope": "Auxiliary finite checks only; smooth topology is a credited theorem input."
    }, sort_keys=True))


if __name__ == "__main__":
    main()
