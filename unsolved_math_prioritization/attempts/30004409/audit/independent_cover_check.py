#!/usr/bin/env python3
"""Independent exact presentation, cover, and endpoint checks.

This uses normal forms a^r b^t, not the submitted checker's quaternion model.
It does not prove the imported smooth-embedding theorem or the real-matrix
nonembedding theorem. Arithmetic in Q(sqrt(2)) is exact throughout.
"""
import itertools
import json
import os
import sys
from fractions import Fraction as F


def need(ok, label):
    if not ok:
        raise RuntimeError(label)


def mul(x, y, mutant="none"):
    r, t = x
    u, v = y
    square = 0 if mutant == "split_extension" else 2
    sign = 1 if mutant == "commuting_generators" else (-1)**t
    return ((r + sign*u + square*t*v) % 4, (t+v) % 2)


def power(x, n, product):
    z = (0, 0)
    for _ in range(n):
        z = product(z, x)
    return z


def matmul(x, y):
    return tuple(tuple(sum(x[i][k]*y[k][j] for k in range(len(y)))
                       for j in range(len(y[0]))) for i in range(len(x)))


def neg(x):
    return tuple(tuple(-v for v in row) for row in x)


def mpow(x, n):
    result = ((1, 0), (0, 1))
    for _ in range(n):
        result = matmul(result, x)
    return result


# A real number in Q(sqrt(2)) is (rational part, sqrt(2) coefficient).
ZERO = (F(0), F(0))
ONE = (F(1), F(0))
HALFROOT = (F(0), F(1, 2))


def add(x, y):
    return (x[0]+y[0], x[1]+y[1])


def minus(x):
    return (-x[0], -x[1])


def times(x, y):
    return (x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0])


def qtimes(x, y):
    # Scalar/vector form with an explicit cross product, independent of input code.
    scalar = times(x[0], y[0])
    for k in range(1, 4):
        scalar = add(scalar, minus(times(x[k], y[k])))
    vector = []
    for i, j, k in ((1, 2, 3), (2, 3, 1), (3, 1, 2)):
        vector.append(add(add(times(x[0], y[i]), times(y[0], x[i])),
                          add(times(x[j], y[k]), minus(times(x[k], y[j])))))
    return (scalar, *vector)


QONE = (ONE, ZERO, ZERO, ZERO)


def qpower(x, n):
    value = QONE
    for _ in range(n):
        value = qtimes(value, x)
    return value


def conjugation_matrix(q):
    conjugate = (q[0], *(minus(v) for v in q[1:]))
    columns = []
    for k in range(3):
        v = (ZERO, *(ONE if j == k else ZERO for j in range(3)))
        result = qtimes(qtimes(q, v), conjugate)
        need(result[0] == ZERO, "quaternion conjugation remains imaginary")
        need(all(v[1] == 0 for v in result[1:]), "rotation entries rational")
        columns.append(tuple(v[0] for v in result[1:]))
    return tuple(zip(*columns))


def main(mutant):
    need(os.getuid() == 1000, "audited execution UID")
    group = tuple(itertools.product(range(4), range(2)))
    product = lambda x, y: mul(x, y, mutant)
    unit, central, a, b = (0, 0), (2, 0), (1, 0), (0, 1)
    need(all(product(product(x, y), z) == product(x, product(y, z))
             for x in group for y in group for z in group), "512 associativity cases")
    need(all(product(unit, x) == x == product(x, unit) for x in group), "identity")
    need(all(any(product(x, y) == unit == product(y, x) for y in group)
             for x in group), "inverses")
    need(power(a, 2, product) == central == power(b, 2, product),
         "both half-turn lifts square to central full turn")
    need(product(b, a) == product(power(a, 3, product), b),
         "quaternion conjugation relation")
    orders = {x: next(k for k in range(1, 9) if power(x, k, product) == unit)
              for x in group}
    need(sorted(orders.values()) == [1, 2, 4, 4, 4, 4, 4, 4], "quaternion orders")
    centre = {x for x in group if all(product(x, y) == product(y, x) for y in group)}
    need(centre == {unit, central}, "quaternion centre")

    identity, swap = ((1, 0), (0, 1)), ((0, 1), (1, 0))
    reverse = ((-1, 0), (0, 1)) if mutant == "single_orientation_reversal" else neg(identity)
    image = {x: matmul(mpow(reverse, x[0]), mpow(swap, x[1])) for x in group}
    if mutant == "central_detected":
        image[central] = neg(identity)
    need(all(image[product(x, y)] == matmul(image[x], image[y])
             for x in group for y in group), "64 Dahm homomorphism cases")
    klein = {identity, neg(identity), swap, neg(swap)}
    need(set(image.values()) == klein, "Dahm image exactly Klein four")
    kernel = {x for x in group if image[x] == identity}
    need(kernel == centre, "Dahm kernel exactly central two")
    # Enumerate every set-theoretic section sending identity to identity.
    nontrivial = sorted(klein - {identity})
    sections = []
    for lifts in itertools.product(*([x for x in group if image[x] == v] for v in nontrivial)):
        section = {identity: unit, **dict(zip(nontrivial, lifts))}
        sections.append(all(section[matmul(x, y)] == product(section[x], section[y])
                            for x in klein for y in klein))
    need(len(sections) == 8 and not any(sections), "no homomorphic section")

    signed = set()
    for p in ((0, 1), (1, 0)):
        for signs in itertools.product((-1, 1), repeat=2):
            signed.add(tuple(tuple(signs[i] if j == p[i] else 0 for j in range(2))
                             for i in range(2)))
    need(len(signed) == 8, "signed permutation group order")
    need(sum(x != identity and mpow(x, 2) == identity for x in signed) == 5,
         "signed permutations have five involutions")
    link_preserving = {x for x in signed if sum(x[0])*sum(x[1]) == 1}
    need(link_preserving == klein, "linking constraint on signed permutations")

    qa = (ZERO, ONE, ZERO, ZERO)
    qb = (ZERO, ZERO, HALFROOT, HALFROOT)
    if mutant == "wrong_exchange_lift":
        qb = qa
    lifts = {x: qtimes(qpower(qa, x[0]), qpower(qb, x[1])) for x in group}
    need(len(set(lifts.values())) == 8, "eight distinct universal-cover endpoints")
    need(all(lifts[product(x, y)] == qtimes(lifts[x], lifts[y])
             for x in group for y in group), "64 exact quaternion lift identities")
    rotations = {x: conjugation_matrix(lifts[x]) for x in group}
    A = ((1, 0, 0), (0, -1, 0), (0, 0, -1))
    B = ((-1, 0, 0), (0, 0, 1), (0, 1, 0))
    if mutant == "wrong_exchange_rotation":
        B = ((-1, 0, 0), (0, 0, -1), (0, -1, 0))
    need(rotations[a] == A and rotations[b] == B, "correct exact half-turn rotations")
    need(len(set(rotations.values())) == 4, "rotation quotient order four")
    Ridentity = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    need({x for x in group if rotations[x] == Ridentity} == centre,
         "SU2-to-SO3 kernel")
    need(all(rotations[product(x, y)] == matmul(rotations[x], rotations[y])
             for x in group for y in group), "64 rotation-cover homomorphism cases")
    centres = ((F(-1, 2), 0, 0), (F(1, 2), 0, 0))
    normals = ((0, 0, 1), (0, 1, 0))
    def action(m, v):
        return tuple(sum(m[i][j]*v[j] for j in range(3)) for i in range(3))
    need(all(action(A, c) == c for c in centres), "A fixes centres")
    need(all(action(A, n) == tuple(-x for x in n) for n in normals), "A reverses normals")
    need(all(action(B, centres[k]) == centres[1-k] and action(B, normals[k]) == normals[1-k]
             for k in range(2)), "B exchanges centres and oriented normals")

    labelled = {x for x in group if x[1] == 0}
    need(len(labelled) == 4 and sorted(orders[x] for x in labelled) == [1, 2, 4, 4],
         "labelled unoriented cover has cyclic fundamental group order four")
    oriented_labelled = {x for x in group if x[0] % 2 == 0 and x[1] == 0}
    need(oriented_labelled == centre, "oriented labelled cover has central C2")
    decorations = tuple(itertools.product((-1, 1), (-1, 1), (0, 1)))
    orbits = {frozenset((e1*s, e2*s, (p+t)%2) for s in (-1, 1) for t in (0, 1))
              for e1, e2, p in decorations}
    expected_components = 1 if mutant == "connected_eightfold_cover" else 2
    need(len(orbits) == expected_components and {len(o) for o in orbits} == {4},
         "eight decorations form two connected four-sheeted components")
    need(all(len({e1*e2 for e1, e2, p in o}) == 1 for o in orbits),
         "orientation-linking sign constant on each decoration orbit")

    print(json.dumps({"status": "PASS", "uid": os.getuid(), "optimization": sys.flags.optimize,
                      "mutant": mutant, "presentation_associativity_cases": 512,
                      "dahm_homomorphism_cases": 64, "quaternion_lift_cases": 64,
                      "rotation_cover_cases": 64, "sections_rejected": len(sections),
                      "motion_group_order": len(group), "dahm_image_order": len(klein),
                      "dahm_kernel_order": len(kernel), "labelled_group_order": len(labelled),
                      "oriented_labelled_group_order": len(oriented_labelled),
                      "full_decoration_sheets": len(decorations), "cover_components": len(orbits),
                      "connected_cover_sheets": 4,
                      "limits": "Finite algebra and cover data only; smooth topology is imported."},
                     sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "none")
