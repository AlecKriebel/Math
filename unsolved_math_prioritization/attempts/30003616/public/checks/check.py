#!/usr/bin/env python3
"""Exact supplementary checks for Problem 30003616.

Requires Python 3 and SymPy. No network, random search, or spectral numerics.
The infinite-energy and Hausdorff-dimension claims are proved in RESULT.md;
these finite algebraic checks do not certify the original open problem.
"""

import json
from fractions import Fraction
from pathlib import Path
import sympy as sp


def check_fricke_identity():
    a, b, c, d, e, f, g, h = sp.symbols("a b c d e f g h")
    A = sp.Matrix([[a, b], [c, d]])
    B = sp.Matrix([[e, f], [g, h]])
    x, y, z = sp.trace(A) / 2, sp.trace(B) / 2, sp.trace(A * B) / 2
    invariant = x*x + y*y + z*z - 2*x*y*z - 1
    polynomial = sp.expand(4 * invariant + (A*B - B*A).det())
    ideal = sp.groebner(
        [a*d-b*c-1, e*h-f*g-1], a, d, e, h, b, c, f, g,
        domain=sp.QQ,
    )
    remainder = ideal.reduce(polynomial)[1]
    assert remainder == 0
    return {"identity": "4 I + det(AB-BA) = 0", "remainder": str(remainder)}


def check_trace_invariance():
    x, y, z = sp.symbols("x y z")
    G = lambda x, y, z: x*x + y*y + z*z - 2*x*y*z - 1
    remainder = sp.expand(G(2*x*y-z, x, y) - G(x, y, z))
    assert remainder == 0
    return {"identity": "G(T(x,y,z)) = G(x,y,z)", "remainder": str(remainder)}


def check_constant_tile_invariant():
    c0, s0, c1, s1, k0, k1 = sp.symbols("c0 s0 c1 s1 k0 k1")
    z = c0*c1 - (k0/k1 + k1/k0)*s0*s1/2
    I = c0*c0 + c1*c1 + z*z - 2*c0*c1*z - 1
    expected = (k0/k1-k1/k0)**2*s0*s0*s1*s1/4
    numerator = sp.expand(4*k0*k0*k1*k1*(I-expected))
    ideal = sp.groebner(
        [c0*c0+s0*s0-1, c1*c1+s1*s1-1],
        c0, c1, s0, s1, k0, k1, domain=sp.QQ,
    )
    remainder = ideal.reduce(numerator)[1]
    assert remainder == 0
    return {"identity": "I = (k0/k1-k1/k0)^2 s0^2 s1^2 / 4",
            "remainder": str(remainder)}


def check_overlap_coefficients():
    n, P, a1, b1, a2, b2 = sp.symbols("n P a1 b1 a2 b2")
    D1 = (n*P+b1)**2-(n*P+a1)**2
    gapB = ((n+1)*P+a2)**2-(n*P+b2)**2
    D2next = ((n+1)*P+b2)**2-((n+1)*P+a2)**2
    gapA = ((n+1)*P+a1)**2-(n*P+b1)**2
    expected = 2*P*((b1-a1)+(b2-a2)-P)
    c_first = sp.expand(D1-gapB).coeff(n, 1)
    c_second = sp.expand(D2next-gapA).coeff(n, 1)
    assert sp.expand(c_first-expected) == 0
    assert sp.expand(c_second-expected) == 0
    assert sp.Poly(sp.expand(D1-gapB), n).degree() == 1
    assert sp.Poly(sp.expand(D2next-gapA), n).degree() == 1
    return {"first_margin_leading_coefficient": str(c_first),
            "second_margin_leading_coefficient": str(c_second)}


def check_residues():
    A = {0, 1, 2, 4, 5, 9}
    B = {0, 3, 7, 8, 10, 11}
    assert B == {(-a) % 12 for a in A}
    sumA = {(a+b) % 12 for a in A for b in A}
    sumB = {(a+b) % 12 for a in B for b in B}
    mixed = {(a+b) % 12 for a in A for b in B}
    assert sumA == sumB == set(range(12))
    assert set(range(12)) - mixed == {6}
    assert set(range(12)).issubset({a+b for a in A for b in A})
    witnesses_A = {
        str(r): list(next((a,b) for a in sorted(A) for b in sorted(A) if a+b == r))
        for r in range(12)
    }
    witnesses_B = {
        str(r): list(next((a,b) for a in sorted(B) for b in sorted(B) if (a+b) % 12 == r))
        for r in range(12)
    }
    return {"A": sorted(A), "B": sorted(B), "mixed_missing_residues": [6],
            "A_integer_witnesses": witnesses_A, "B_modular_witnesses": witnesses_B}


def check_cover_formulas():
    Q = N = D = 1
    previous = Fraction(1, 1)
    samples = []
    for n in range(1, 33):
        Q *= 2*(n+1)
        N *= n+1
        D *= 2*n+1
        assert Q == (2**n)*N
        ratio = Fraction(D, Q)
        assert ratio == previous * Fraction(2*n+1, 2*n+2)
        assert ratio < previous
        previous = ratio
        if n in [1, 2, 4, 8, 16, 32]:
            samples.append({"n": n, "K_total_cover_bound": str(Fraction(N, 2*Q)),
                            "K_plus_K_total_cover_bound": str(ratio)})
    p, q = sp.symbols("p q")
    assert sp.expand((p-1)+(q-1)+(p-1)*(q-1)-(p*q-1)) == 0
    return samples


def main():
    results = {
        "status": "all_exact_supplementary_checks_passed",
        "sympy_version": sp.__version__,
        "fricke_commutator": check_fricke_identity(),
        "trace_map": check_trace_invariance(),
        "constant_tile_control": check_constant_tile_invariant(),
        "mixed_block_overlaps": check_overlap_coefficients(),
        "sumset_residues": check_residues(),
        "mixed_radix_cover_samples": check_cover_formulas(),
        "original_problem_status": "unsolved 5/5",
        "limits": "Finite checks do not prove any infinite spectral-ray assertion."
    }
    destination = Path(__file__).with_name("results.json")
    destination.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
