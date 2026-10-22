#!/usr/bin/env python3
"""Independent exact controls; Python standard library only."""
from itertools import product
import json
from pathlib import Path

I = (1, 0, 0, 1)
Z = (0, 0)


def madd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mneg(a):
    return tuple(-x for x in a)


def mmul(a, b):
    p, q, r, s = a
    u, v, w, z = b
    return (p*u + q*w, p*v + q*z, r*u + s*w, r*v + s*z)


def det(a):
    p, q, r, s = a
    return p*s - q*r


def minv(a):
    p, q, r, s = a
    d = det(a)
    assert d in (-1, 1)
    return (s*d, -q*d, -r*d, p*d)


def mpow(a, n):
    if n < 0:
        return mpow(minv(a), -n)
    ans = I
    while n:
        if n & 1:
            ans = mmul(ans, a)
        a = mmul(a, a)
        n //= 2
    return ans


def mv(a, v):
    p, q, r, s = a
    x, y = v
    return (p*x + q*y, r*x + s*y)


def vadd(a, b):
    return tuple(x+y for x, y in zip(a, b))


def vneg(a):
    return tuple(-x for x in a)


def mul(a, g, h):
    v, n = g
    w, m = h
    return (vadd(v, mv(mpow(a, n), w)), n+m)


def inv(a, g):
    v, n = g
    return (vneg(mv(mpow(a, -n), v)), -n)


def comm(a, g, h):
    return mul(a, mul(a, mul(a, g, h), inv(a, g)), inv(a, h))


def invword(w):
    return tuple(-s for s in reversed(w))


def reduce_word(w):
    out = []
    for s in w:
        if out and out[-1] == -s:
            out.pop()
        else:
            out.append(s)
    return tuple(out)


def wordcomm(u, v):
    return u + v + invword(u) + invword(v)


def evaluate(a, w, x, y):
    table = {1: x, 2: y, -1: inv(a, x), -2: inv(a, y)}
    out = (Z, 0)
    for s in w:
        out = mul(a, out, table[s])
    return out


def laurent_sum(a, n):
    # A^n - I = (A-I) S_n for positive, zero, and negative n.
    total = (0, 0, 0, 0)
    if n >= 0:
        for k in range(n):
            total = madd(total, mpow(a, k))
    else:
        for k in range(1, -n+1):
            total = madd(total, mneg(mpow(a, -k)))
    return total


def run():
    # x -> 1, y -> 2; negative integers are inverse letters.
    c = (1, 2, -1, -2)
    d = (1,) + c + (-1,)
    raw = wordcomm(c, d)
    witness = reduce_word(raw)
    expected = (1, 2, -1, -2, 1, 1, 2, -1, -2, -1, 2, 1, 1, -2, -1, -1)
    assert witness == expected
    assert witness and reduce_word(witness) == witness
    assert all(witness[i] != -witness[i+1] for i in range(len(witness)-1))
    assert sum(s for s in witness if abs(s) == 1) == 0
    assert sum(s//2 for s in witness if abs(s) == 2) == 0

    matrices = {
        "identity": (1, 0, 0, 1),
        "minus_identity_order_2": (-1, 0, 0, -1),
        "rotation_order_4": (0, -1, 1, 0),
        "rotation_order_6": (0, -1, 1, 1),
        "reflection_order_2": (1, 0, 0, -1),
        "swap_order_2": (0, 1, 1, 0),
        "unipotent": (1, 1, 0, 1),
        "negative_unipotent": (-1, 1, 0, -1),
        "hyperbolic": (2, 1, 1, 1),
        "orientation_reversing_hyperbolic": (2, 1, 1, 0),
    }
    vectors = [Z, (1, 0), (0, 1), (2, -3), (-2, 5)]
    elements = list(product(vectors, range(-4, 5)))
    counts = {k: 0 for k in ("matrix_inverse", "laurent_factorization", "group_inverse",
                            "associativity", "commutator_formula", "witness_identity")}
    rows = []
    for name, a in matrices.items():
        assert mmul(a, minv(a)) == mmul(minv(a), a) == I
        counts["matrix_inverse"] += 1
        for n in range(-8, 9):
            assert madd(mpow(a, n), mneg(I)) == mmul(madd(a, mneg(I)), laurent_sum(a, n))
            counts["laurent_factorization"] += 1
        for g in elements:
            assert mul(a, g, inv(a, g)) == mul(a, inv(a, g), g) == (Z, 0)
            counts["group_inverse"] += 1
        for g, h in product(elements, repeat=2):
            v, n = g
            w, m = h
            expected_comm = (vadd(mv(madd(I, mneg(mpow(a, m))), v),
                                  mv(madd(mpow(a, n), mneg(I)), w)), 0)
            assert comm(a, g, h) == expected_comm
            counts["commutator_formula"] += 1
            assert evaluate(a, witness, g, h) == (Z, 0)
            counts["witness_identity"] += 1
        # Deterministic 405 triples per matrix, including mixed negative heights.
        for j in range(len(elements)):
            for k in range(9):
                g, h, z = elements[j], elements[(7*j+k) % len(elements)], elements[(13*j+5*k) % len(elements)]
                assert mul(a, mul(a, g, h), z) == mul(a, g, mul(a, h, z))
                counts["associativity"] += 1
        rows.append({"name": name, "matrix": list(a), "determinant": det(a)})
    result = {
        "status": "PASS",
        "scope": "Independent exact integer controls; finite checks supplement the universal proof.",
        "witness_convention": "[u,v]=u v u^-1 v^-1; 1=x, 2=y, negative=letter inverse",
        "witness_raw_length": len(raw),
        "witness_reduced_length": len(witness),
        "witness_reduced": list(witness),
        "matrices": rows,
        "elements_per_matrix": len(elements),
        "counts": counts,
    }
    Path(__file__).with_name("controls_result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "counts": counts, "witness_reduced_length": len(witness)}, sort_keys=True))


if __name__ == "__main__":
    run()
