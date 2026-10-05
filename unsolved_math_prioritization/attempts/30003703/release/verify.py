#!/usr/bin/env python3
"""Exact controls for PROOF.md. Python standard library only; no network/files read.

The general proof is in PROOF.md. This finite symbolic calculation is a
reproducibility and transcription control, not a substitute for that proof.
"""
from collections import defaultdict
import json


def add(a, b, sign=1):
    out = defaultdict(int, a)
    for monomial, coefficient in b.items():
        out[monomial] += sign * coefficient
    return {m: c for m, c in out.items() if c}


def mul(a, b, bound=99, commutative=False):
    out = defaultdict(int)
    for m, c in a.items():
        for n, d in b.items():
            if len(m) + len(n) <= bound:
                word = m + n
                if commutative:
                    word = tuple(sorted(word))
                out[word] += c * d
    return {m: c for m, c in out.items() if c}


def bracket(a, b):
    return add(mul(a, b), mul(b, a), -1)


def mmul(a, b):
    n = len(a)
    return [[sum_poly(mul(a[i][k], b[k][j], commutative=True)
                      for k in range(n)) for j in range(n)] for i in range(n)]


def sum_poly(polynomials):
    out = {}
    for p in polynomials:
        out = add(out, p)
    return out


def mbr(a, b):
    ab, ba = mmul(a, b), mmul(b, a)
    return [[add(x, y, -1) for x, y in zip(row, other)]
            for row, other in zip(ab, ba)]


def is_zero_matrix(a):
    return all(not p for row in a for p in row)


def variable(i):
    return {(i,): 1}


def traceless(offset):
    a, b, c = (variable(offset + i) for i in range(3))
    return [[a, b], [c, {m: -v for m, v in a.items()}]]


def numeric_matrix(rows):
    return [[{(): v} if v else {} for v in row] for row in rows]


def inverse_word(word):
    return tuple(-i for i in reversed(word))


def reduce_word(word):
    out = []
    for i in word:
        if out and out[-1] == -i:
            out.pop()
        else:
            out.append(i)
    return tuple(out)


def group_bracket(a, b):
    return reduce_word(a + b + inverse_word(a) + inverse_word(b))


def magnus(word, bound):
    out = {(): 1}
    for letter in word:
        if letter > 0:
            factor = {(): 1, (letter,): 1}
        else:
            factor = {(abs(letter),) * i: (-1) ** i for i in range(bound + 1)}
        out = mul(out, factor, bound=bound)
    return out


def substitute(word, images):
    out = ()
    for i in word:
        image = images[abs(i)]
        out += image if i > 0 else inverse_word(image)
    return reduce_word(out)


def check_inverse(word, moving, rank):
    phi = {i: (i,) for i in range(1, rank + 1)}
    psi = dict(phi)
    phi[moving] += word
    psi[moving] += inverse_word(word)
    assert all(abs(i) != moving for i in word)
    for i in range(1, rank + 1):
        assert substitute(phi[i], psi) == (i,)
        assert substitute(psi[i], phi) == (i,)


def serialized(poly):
    return [{"word": list(m), "coefficient": c} for m, c in sorted(poly.items())]


def run():
    x, y, z = (variable(i) for i in (1, 2, 3))
    p = bracket(bracket(bracket(x, y), bracket(x, z)), x)
    q = bracket(bracket(bracket(x, y), bracket(x, bracket(x, y))), x)
    assert len(p) == 12 and p[(1, 1, 2, 1, 3)] == -1
    assert len(q) == 10 and q[(1, 1, 1, 2, 1, 2)] == 1
    gx, gy, gz = (1,), (2,), (3,)
    w = group_bracket(group_bracket(group_bracket(gx, gy), group_bracket(gx, gz)), gx)
    v = group_bracket(group_bracket(group_bracket(gx, gy),
                                   group_bracket(gx, group_bracket(gx, gy))), gx)
    assert magnus(w, 5) == add({(): 1}, p)
    assert magnus(v, 6) == add({(): 1}, q)
    assert magnus(w, 4) == {(): 1}
    assert magnus(v, 5) == {(): 1}
    check_inverse(w, moving=4, rank=4)
    check_inverse(v, moving=3, rank=3)

    X, Y, Z = traceless(0), traceless(3), traceless(6)
    assert is_zero_matrix(mbr(mbr(mbr(X, Y), mbr(X, Z)), X))
    assert is_zero_matrix(mbr(mbr(mbr(X, Y), mbr(X, mbr(X, Y))), X))

    # Negative control 1: changing the outer repeated variable breaks the identity.
    H = numeric_matrix([[1, 0], [0, -1]])
    E = numeric_matrix([[0, 1], [0, 0]])
    F = numeric_matrix([[0, 0], [1, 0]])
    wrong = mbr(mbr(mbr(H, E), mbr(H, F)), E)
    assert wrong == numeric_matrix([[0, -8], [0, 0]])

    # Negative control 2: one cannot silently replace SL2 by SL3.
    H3 = numeric_matrix([[1, 0, 0], [0, -1, 0], [0, 0, 0]])
    E12 = numeric_matrix([[0, 1, 0], [0, 0, 0], [0, 0, 0]])
    E23 = numeric_matrix([[0, 0, 0], [0, 0, 1], [0, 0, 0]])
    p3 = mbr(mbr(mbr(H3, E12), mbr(H3, E23)), H3)
    assert p3 == numeric_matrix([[0, 0, 2], [0, 0, 0], [0, 0, 0]])

    # Negative control 3: deleting the outer commutator loses vanishing in degree 4.
    inner = mbr(mbr(H, E), mbr(H, F))
    assert inner == numeric_matrix([[-4, 0], [0, 4]])

    # Negative control 4: Magnus multiplication must retain noncommuting letters.
    comm = group_bracket(gx, gy)
    assert magnus(comm, 2) == {(): 1, (1, 2): 1, (2, 1): -1}

    # Negative control 5: a deliberately false coefficient is detected.
    assert p[(1, 1, 2, 1, 3)] != 1

    return {
        "result": "PASS",
        "arithmetic": "exact integers; sparse formal polynomials",
        "p5_free_associative_terms": serialized(p),
        "q6_free_associative_terms": serialized(q),
        "w5_reduced_word": list(w),
        "v6_reduced_word": list(v),
        "magnus_w5_through_degree5": "1 + P exactly",
        "magnus_v6_through_degree6": "1 + Q exactly",
        "generic_traceless_2x2_P": "zero polynomial matrix",
        "generic_traceless_2x2_Q": "zero polynomial matrix",
        "automorphism_inverse_checks": ["rank 4, moving x4", "rank 3, moving x3"],
        "negative_controls": {
            "wrong_outer_letter": [[0, -8], [0, 0]],
            "size3_counterexample": [[0, 0, 2], [0, 0, 0], [0, 0, 0]],
            "outer_bracket_removed": [[-4, 0], [0, 4]],
            "ordinary_group_commutator": "1 + XY - YX through degree 2",
            "wrong_coefficient": "rejected"
        },
        "proof_role": "Independent exact control of formulas; general deduction is in PROOF.md"
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
