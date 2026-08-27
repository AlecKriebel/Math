#!/usr/bin/env python3
"""Fresh exact checks of the article's elementary K3P and 3-leaf formulas.

This script is intentionally self-contained.  It starts from equations
(inverse-Fourier), (sunlet-map), and (H14) in the article and does not import
any package producer/verifier.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
import json
import random

import sympy as sp


LETTERS = "0CGT"
CHAR = {x: i for i, x in enumerate(LETTERS)}
ORDER3 = (
    "000", "0CC", "0GG", "0TT", "C0C", "CC0", "CGT", "CTG",
    "G0G", "GCT", "GG0", "GTC", "T0T", "TCG", "TGC", "TT0",
)


def principal_margins(y):
    c, g, t = y
    return (
        c, g, t, 1 - c, 1 - g, 1 - t,
        1 + c - g - t, 1 - c + g - t, 1 - c - g + t,
    )


def ct_margins(y):
    c, g, t = y
    return principal_margins(y) + (c - g * t, g - c * t, t - c * g)


def inverse_fourier(y):
    c, g, t = y
    return (
        (1 + c + g + t) / 4,
        (1 + c - g - t) / 4,
        (1 - c + g - t) / 4,
        (1 - c - g + t) / 4,
    )


def make_sunlet_map():
    lam = sp.symbols("lam")
    arrays = {}
    for name in "abcdef":
        vals = [sp.Integer(1)] + list(sp.symbols(f"{name}C {name}G {name}T"))
        arrays[name] = vals

    def q(word):
        x, y, z = map(CHAR.__getitem__, word)
        assert x ^ y ^ z == 0
        a, b, c, d, e, f = (arrays[n] for n in "abcdef")
        return a[x] * b[y] * c[z] * (lam * f[y] * d[z] + (1 - lam) * f[x] * e[z])

    return q, arrays, lam


def circuit_pullbacks(q):
    pairs = (
        (("000", "CGT", "GTC"), ("0TT", "C0C", "GG0")),
        (("000", "CTG", "TGC"), ("0GG", "C0C", "TT0")),
        (("000", "GCT", "TGC"), ("0CC", "GG0", "T0T")),
        (("000", "GTC", "TCG"), ("0CC", "G0G", "TT0")),
        (("000", "CTG", "GCT"), ("0TT", "CC0", "G0G")),
        (("000", "CGT", "TCG"), ("0GG", "CC0", "T0T")),
    )
    return [sp.factor(sp.prod(q(w) for w in left) - sp.prod(q(w) for w in right))
            for left, right in pairs]


def h14(q):
    return sp.expand(
        q("000") * q("CGT") * q("GTC") * q("TCG")
        - q("000") * q("CTG") * q("GCT") * q("TGC")
        - q("0CC") * q("CGT") * q("G0G") * q("TT0")
        + q("0CC") * q("CTG") * q("GG0") * q("T0T")
        + q("0GG") * q("C0C") * q("GCT") * q("TT0")
        - q("0GG") * q("CC0") * q("GTC") * q("T0T")
        - q("0TT") * q("C0C") * q("GG0") * q("TCG")
        + q("0TT") * q("CC0") * q("G0G") * q("TGC")
    )


def permuted_map(base_q, perm):
    """Relabel base leaf positions: base position i receives observed perm[i]."""
    inv = [perm.index(i) for i in range(3)]

    def q(word):
        return base_q("".join(word[inv[i]] for i in range(3)))

    return q


def independent_square_minor(matrix):
    """Find a full-rank square minor without using any stored row/column list."""
    rank = matrix.rank()
    col_pivots = matrix.rref()[1]
    cols = list(col_pivots[:rank])
    narrowed = matrix[:, cols]
    row_pivots = narrowed.T.rref()[1]
    rows = list(row_pivots[:rank])
    det = sp.factor(matrix.extract(rows, cols).det())
    assert det != 0
    return rank, rows, cols, det


def numeric_separator_search(factors, symbols, trials=5000):
    rng = random.Random(830917)
    funcs = [sp.lambdify(symbols, x, "math") for x in factors]
    best = None
    accepted = 0
    while accepted < trials:
        vals = [rng.uniform(0.015, 0.985) for _ in symbols]
        # Every edge triple occurs consecutively except lambda.  Reject edge
        # triples outside the strict principal tetrahedron.
        okay = True
        for i in range(0, len(symbols) - 1, 3):
            if min(principal_margins(vals[i:i + 3])) <= 0:
                okay = False
                break
        if not okay:
            continue
        vals[-1] = rng.uniform(0.015, 0.985)
        accepted += 1
        score = sum(float(fun(*vals)) ** 2 for fun in funcs)
        if best is None or score < best[0]:
            best = (score, vals)
    return accepted, best[0]


def main():
    report = {}

    # Inverse Fourier: exact inverse and CT implication.
    c, g, t = sp.symbols("c g t", positive=True)
    probs = inverse_fourier((c, g, t))
    reconstructed = (
        sp.expand(probs[0] + probs[1] - probs[2] - probs[3]),
        sp.expand(probs[0] - probs[1] + probs[2] - probs[3]),
        sp.expand(probs[0] - probs[1] - probs[2] + probs[3]),
    )
    assert reconstructed == (c, g, t)
    # c > gt implies the corresponding principal margin is even larger than
    # (1-g)(1-t), and cyclically.
    identities = (
        sp.expand((1 + c - g - t) - (1 - g) * (1 - t)),
        sp.expand((1 - c + g - t) - (1 - c) * (1 - t)),
        sp.expand((1 - c - g + t) - (1 - c) * (1 - g)),
    )
    assert identities == (c - g * t, g - c * t, t - c * g)
    principal_not_ct = (Fraction(2, 5), Fraction(2, 5), Fraction(1, 10))
    assert min(principal_margins(principal_not_ct)) > 0
    assert min(ct_margins(principal_not_ct)) < 0
    report["domains"] = {
        "fourier_round_trip": [str(x) for x in reconstructed],
        "ct_to_principal_margin_identities": [str(x) for x in identities],
        "strict_principal_not_ct_example": [str(x) for x in principal_not_ct],
        "example_ct_margin_min": str(min(ct_margins(principal_not_ct))),
    }

    base_q, arrays, lam = make_sunlet_map()
    factors = circuit_pullbacks(base_q)
    # These assertions compare only after direct expansion/factorization.
    a, b, cc, d, e, f = (arrays[n] for n in "abcdef")
    mu = lam * (1 - lam)
    expected = (
        mu*a[1]*a[2]*b[2]*b[3]*cc[1]*cc[3]*(f[1]*f[3]-f[2])*(d[1]*e[3]-d[3]*e[1]*f[2]),
        mu*a[1]*a[3]*b[2]*b[3]*cc[1]*cc[2]*(f[1]*f[2]-f[3])*(d[1]*e[2]-d[2]*e[1]*f[3]),
        -mu*a[2]*a[3]*b[1]*b[2]*cc[1]*cc[3]*(f[1]*f[3]-f[2])*(d[1]*e[3]*f[2]-d[3]*e[1]),
        -mu*a[2]*a[3]*b[1]*b[3]*cc[1]*cc[2]*(f[1]*f[2]-f[3])*(d[1]*e[2]*f[3]-d[2]*e[1]),
        -mu*a[1]*a[2]*b[1]*b[3]*cc[2]*cc[3]*(f[1]-f[2]*f[3])*(d[2]*e[3]-d[3]*e[2]*f[1]),
        mu*a[1]*a[3]*b[1]*b[2]*cc[2]*cc[3]*(f[1]-f[2]*f[3])*(d[2]*e[3]*f[1]-d[3]*e[2]),
    )
    assert all(sp.expand(x - y) == 0 for x, y in zip(factors, expected))
    params = [x for n in "abcdef" for x in arrays[n][1:]] + [lam]
    trials, smallest = numeric_separator_search(factors, params)
    # Two exact boundary failures show why both nonidentity and inheritance
    # strictness matter.
    identity_f = {f[i]: 1 for i in (1, 2, 3)}
    lambda_zero = {lam: 0}
    assert all(sp.expand(x.subs(identity_f)) == 0 for x in factors)
    assert all(sp.expand(x.subs(lambda_zero)) == 0 for x in factors)
    report["tree_sunlet"] = {
        "factored_pullbacks": [str(x) for x in factors],
        "random_strict_principal_trials": trials,
        "smallest_S_seen": smallest,
        "boundary_counterexamples": ["f=(1,1,1)", "lambda=0"],
    }

    # H14 symbolic annihilation under each possible leaf relabeling.  The three
    # cyclic relabelings are the triangle orientations used below; checking all
    # six is a stronger symmetry sanity check.
    annihilation = {}
    for perm in permutations(range(3)):
        value = sp.factor(h14(permuted_map(base_q, perm)))
        annihilation["".join(map(str, perm))] = (value == 0)
    assert all(annihilation.values())

    qvars = {w: sp.Integer(1) if w == "000" else sp.symbols("q_" + w) for w in ORDER3}
    F = h14(qvars.__getitem__)
    assert sp.factor(F) == F  # SymPy finds no factorization over QQ.
    A = sp.diff(F, qvars["0CC"])
    B = sp.expand(F.subs(qvars["0CC"], 0))
    assert sp.gcd(A, B) == 1

    iso = {}
    for name in "abcde":
        iso.update({arrays[name][i]: sp.Rational(1, 2) for i in (1, 2, 3)})
    iso.update({arrays["f"][i]: sp.Rational(1, 3) for i in (1, 2, 3)})
    iso[lam] = sp.Rational(1, 2)
    expected_q0 = (
        sp.Integer(1), sp.Rational(1, 12), sp.Rational(1, 12), sp.Rational(1, 12),
        sp.Rational(1, 12), sp.Rational(1, 12), sp.Rational(1, 48), sp.Rational(1, 48),
        sp.Rational(1, 12), sp.Rational(1, 48), sp.Rational(1, 12), sp.Rational(1, 48),
        sp.Rational(1, 12), sp.Rational(1, 48), sp.Rational(1, 48), sp.Rational(1, 12),
    )
    orientation_results = {}
    for perm in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        qmap = permuted_map(base_q, perm)
        out = [qmap(w) for w in ORDER3[1:]]
        image = tuple([sp.Integer(1)] + [sp.factor(x.subs(iso)) for x in out])
        assert image == expected_q0
        J = sp.Matrix(out).jacobian(params).subs(iso)
        rank, rows, cols, det = independent_square_minor(J)
        assert rank == 14
        orientation_results["".join(map(str, perm))] = {
            "rank": rank,
            "minor_rows_zero_based_normalized": rows,
            "minor_columns_zero_based": cols,
            "minor_determinant": str(det),
        }

    q0_sub = {qvars[w]: expected_q0[i] for i, w in enumerate(ORDER3) if w != "000"}
    grad = [sp.factor(sp.diff(F, qvars[w]).subs(q0_sub)) for w in ORDER3[1:]]
    nonzero_grad = [x for x in grad if x]
    assert len(nonzero_grad) == 6 and {abs(x) for x in nonzero_grad} == {sp.Rational(1, 6912)}
    report["H14"] = {
        "annihilation_all_six_leaf_permutations": annihilation,
        "primitive_linear_coeff_gcd_remainder": str(sp.gcd(A, B)),
        "orientation_rank_witnesses": orientation_results,
        "gradient_nonzero_count": len(nonzero_grad),
        "gradient_nonzero_absolute_values": [str(x) for x in sorted({abs(x) for x in nonzero_grad})],
    }

    # Cherry inverse and physical point.
    uC, vC, uG, vG, uT, vT = sp.symbols("uC vC uG vG uT vT", positive=True)
    cherry_in = (uC, vC, uG, vG, uT, vT)
    cherry_out = (uC/vC, uC*vC, uG/vG, uG*vG, uT/vT, uT*vT)
    cherry_det = sp.factor(sp.Matrix(cherry_out).jacobian(cherry_in).det())
    asserted_det = 8*uC*uG*uT/(vC*vG*vT)
    assert sp.simplify(cherry_det - asserted_det) == 0
    u = (Fraction(2, 5), Fraction(4, 9), Fraction(3, 7))
    v = (Fraction(3, 7), Fraction(5, 11), Fraction(4, 9))
    det_point = Fraction(8) * u[0]*u[1]*u[2] / (v[0]*v[1]*v[2])
    assert det_point == Fraction(176, 25)
    report["cherry"] = {
        "jacobian_determinant": str(cherry_det),
        "point_determinant": str(det_point),
        "u_min_ct_margin": str(min(ct_margins(u))),
        "v_min_ct_margin": str(min(ct_margins(v))),
        "inverse": ["u_h=sqrt(R_h P_h)", "v_h=sqrt(P_h/R_h)"],
    }

    with open("three_leaf_and_domains_results.json", "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
