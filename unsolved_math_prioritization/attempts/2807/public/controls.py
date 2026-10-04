#!/usr/bin/env python3
"""Exact, finite controls for KP-3.9; not a test of the universal conjecture.

Standard library only. No network, randomness, external programs, or packages.
"""
import itertools
import json
import math
from fractions import Fraction


def rank(matrix):
    if not matrix:
        return 0
    a = [[Fraction(x) for x in row] for row in matrix]
    rows, cols = len(a), len(a[0])
    r = 0
    for c in range(cols):
        pivot = next((j for j in range(r, rows) if a[j][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][c]
        a[r] = [x / v for x in a[r]]
        for j in range(rows):
            if j != r and a[j][c]:
                v = a[j][c]
                a[j] = [x - v*y for x, y in zip(a[j], a[r])]
        r += 1
        if r == rows:
            break
    return r


def exponents(word, d):
    out = [0]*d
    for x in word:
        out[abs(x)-1] += 1 if x > 0 else -1
    return out


def cover_profile(d, relators):
    """Cellular H1 of every connected double cover of a presentation complex."""
    base = d - rank([exponents(w, d) for w in relators])
    records = []
    for eps in itertools.product((0, 1), repeat=d):
        if not any(eps):
            continue
        if any(sum(eps[abs(x)-1] for x in w) % 2 for w in relators):
            continue
        boundaries = []
        for w in relators:
            for start in (0, 1):
                v, chain = start, [0]*(2*d)
                for x in w:
                    i = abs(x)-1
                    if x > 0:
                        chain[v*d+i] += 1
                        v ^= eps[i]
                    else:
                        v ^= eps[i]
                        chain[v*d+i] -= 1
                assert v == start
                boundaries.append(chain)
        # Connected graph with two vertices has rank(d1)=1.
        b1 = 2*d - 1 - rank(boundaries)
        records.append({"epimorphism_to_C2": eps, "b1_cover": b1})
    return {"b1_base": base, "double_covers": records,
            "dihedral_criterion": any(r["b1_cover"] > base for r in records)}


def mul(a, b, p):
    return ((a[0]*b[0]+a[1]*b[2]) % p,
            (a[0]*b[1]+a[1]*b[3]) % p,
            (a[2]*b[0]+a[3]*b[2]) % p,
            (a[2]*b[1]+a[3]*b[3]) % p)


def finite_dihedral_characters(p):
    mats = [x for x in itertools.product(range(p), repeat=4)
            if (x[0]*x[3]-x[1]*x[2]) % p == 1]
    ident = (1, 0, 0, 1)
    involutions = [a for a in mats if mul(a, a, p) == ident]
    chars = set()
    for a in involutions:
        for b in involutions:
            ab = mul(a, b, p)
            chars.add(((a[0]+a[3]) % p, (b[0]+b[3]) % p,
                       (ab[0]+ab[3]) % p))
    return {"p": p, "SL2_order": len(mats),
            "Hom_Dinfty_SL2_count": len(involutions)**2,
            "distinct_generator_trace_triples": len(chars)}


# Polynomial coefficients are in ascending degree order.
def trim(a, p):
    a = [x % p for x in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [0]


def subtract(a, b, p):
    return trim([(a[i] if i < len(a) else 0) -
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))], p)


def remainder(a, b, p):
    a, b = trim(a, p), trim(b, p)
    assert b != [0]
    while a != [0] and len(a) >= len(b):
        k = len(a)-len(b)
        c = a[-1] * pow(b[-1], -1, p) % p
        for j, bj in enumerate(b):
            a[k+j] = (a[k+j]-c*bj) % p
        a = trim(a, p)
    return a


def pgcd(a, b, p):
    a, b = trim(a, p), trim(b, p)
    while b != [0]:
        a, b = b, remainder(a, b, p)
    if a == [0]:
        return a
    return trim([x*pow(a[-1], -1, p) for x in a], p)


def product_mod(a, b, f, p):
    c = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return remainder(c, f, p)


def power_mod(a, n, f, p):
    out = [1]
    while n:
        if n % 2:
            out = product_mod(out, a, f, p)
        a = product_mod(a, a, f, p)
        n //= 2
    return out


def polynomial_controls():
    f = [8, -40, 46, -17, 2]
    p, x = 7, [0, 1]
    r49 = power_mod(x, 49, f, p)
    r2401 = power_mod(x, 2401, f, p)
    g = pgcd(f, subtract(r49, x, p), p)
    assert g == [1] and r2401 == x
    # For a degree-four polynomial, these two conditions prove irreducibility.
    q = [1, 0, -12, 0, 18, 0, -10, 0, 2]
    qprime = [i*q[i] for i in range(1, len(q))]
    repeated = pgcd(q, qprime, 43)
    assert len(repeated) > 1
    assert trim(q, 2) == [1]
    return {"f_mod7_irreducibility": {"x49_remainder": r49,
             "gcd_f_x49_minus_x": g, "x2401_remainder": r2401},
            "q_mod43_gcd_with_derivative": repeated,
            "q_mod2": trim(q, 2),
            "limit": "Polynomial facts only; no manifold representation certified."}


def crt_controls():
    output = []
    # alpha=0 modulo 2^k and alpha=1 modulo 3^k: finite shadows only.
    for k in range(1, 7):
        a, b = 2**k, 3**k
        modulus = a*b
        alpha = (a*pow(a, -1, b)) % modulus
        assert alpha % a == 0 and alpha % b == 1
        output.append({"k": k, "modulus": modulus, "alpha": alpha})
    return output


def main():
    examples = {
        "Z2": (2, [(1, 2, -1, -2)]),
        "free_rank2": (2, []),
        "Dinfty": (2, [(1, 1), (2, 2)]),
        "Klein_bottle": (2, [(1, 2, -1, 2)]),
    }
    profiles = {name: cover_profile(*data) for name, data in examples.items()}
    assert profiles["Z2"]["b1_base"] == 2
    assert [r["b1_cover"] for r in profiles["Z2"]["double_covers"]] == [2, 2, 2]
    assert profiles["free_rank2"]["dihedral_criterion"]
    assert sorted(r["b1_cover"] for r in profiles["Dinfty"]["double_covers"]) == [0, 0, 1]
    assert sorted(r["b1_cover"] for r in profiles["Klein_bottle"]["double_covers"]) == [1, 1, 2]
    finite = [finite_dihedral_characters(p) for p in (2, 3, 5)]
    assert all(r["Hom_Dinfty_SL2_count"] == 4 for r in finite if r["p"] != 2)
    # Exactly the displayed presentation in Garden–Tillmann v2, p. 43.
    rel1 = (1, 2, 2, 1, 2, 2, 1, -2, 1, 1, 1, -2)
    rel2 = (1, 1, 1, -2, -2, -2, 1, 1, 1, -2, 1, 1, 1, 1, -2)
    matrix = [exponents(rel1, 2), exponents(rel2, 2)]
    determinant = matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    gcd_entries = math.gcd(*(abs(v) for row in matrix for v in row))
    assert matrix == [[6, 2], [10, -5]] and determinant == -50 and gcd_entries == 1
    print(json.dumps({"all_checks_passed": True,
          "double_cover_profiles": profiles,
          "finite_matrix_controls": finite,
          "polynomial_controls": polynomial_controls(),
          "printed_presentation_control": {"exponent_matrix": matrix,
             "determinant": determinant, "smith_invariants": [1, 50],
             "claimed_source_H1_order": 40,
             "limit": "Checks the displayed presentation, not the census manifold."},
          "crt_shadows": crt_controls(),
          "universal_problem_resolved": False}, indent=2))


if __name__ == "__main__":
    main()
