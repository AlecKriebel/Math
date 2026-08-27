#!/usr/bin/env python3
"""Independent exact checks of the elementary K3P and three-leaf claims.

The formulas are transcribed from the article.  This file imports no code from
the referee package and treats every failed assertion as a failed check.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import permutations
import json
from pathlib import Path
import random

import sympy as sp


if not __debug__:
    raise RuntimeError("run without -O so fail-closed assertions remain active")


LETTERS = "0CGT"
CHAR = {letter: index for index, letter in enumerate(LETTERS)}
ORDER3 = (
    "000", "0CC", "0GG", "0TT", "C0C", "CC0", "CGT", "CTG",
    "G0G", "GCT", "GG0", "GTC", "T0T", "TCG", "TGC", "TT0",
)


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


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
        arrays[name] = [sp.Integer(1)] + list(sp.symbols(f"{name}C {name}G {name}T"))

    def q(word):
        x, y, z = map(CHAR.__getitem__, word)
        assert x ^ y ^ z == 0
        a, b, c, d, e, f = (arrays[name] for name in "abcdef")
        return a[x] * b[y] * c[z] * (
            lam * f[y] * d[z] + (1 - lam) * f[x] * e[z]
        )

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
    return [
        sp.factor(sp.prod(q(word) for word in left) - sp.prod(q(word) for word in right))
        for left, right in pairs
    ]


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
    inverse = [perm.index(index) for index in range(3)]

    def q(word):
        return base_q("".join(word[inverse[index]] for index in range(3)))

    return q


def independent_square_minor(matrix):
    rank = matrix.rank()
    columns = list(matrix.rref()[1][:rank])
    narrowed = matrix[:, columns]
    rows = list(narrowed.T.rref()[1][:rank])
    determinant = sp.factor(matrix.extract(rows, columns).det())
    assert determinant != 0
    return rank, rows, columns, determinant


def numeric_separator_search(factors, symbols, trials=5000):
    rng = random.Random(2026082701)
    functions = [sp.lambdify(symbols, expression, "math") for expression in factors]
    accepted = 0
    smallest = None
    while accepted < trials:
        values = [rng.uniform(0.015, 0.985) for _ in symbols]
        if any(
            min(principal_margins(values[index:index + 3])) <= 0
            for index in range(0, len(symbols) - 1, 3)
        ):
            continue
        values[-1] = rng.uniform(0.015, 0.985)
        accepted += 1
        score = sum(float(function(*values)) ** 2 for function in functions)
        smallest = score if smallest is None else min(smallest, score)
    return accepted, smallest


def main():
    args = arguments()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = {}

    c, g, t = sp.symbols("c g t", positive=True)
    probabilities = inverse_fourier((c, g, t))
    reconstructed = (
        sp.expand(probabilities[0] + probabilities[1] - probabilities[2] - probabilities[3]),
        sp.expand(probabilities[0] - probabilities[1] + probabilities[2] - probabilities[3]),
        sp.expand(probabilities[0] - probabilities[1] - probabilities[2] + probabilities[3]),
    )
    assert reconstructed == (c, g, t)
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
        "inverse_fourier_round_trip": [str(value) for value in reconstructed],
        "ct_implies_principal_identities": [str(value) for value in identities],
        "strict_principal_not_ct_example": [str(value) for value in principal_not_ct],
        "example_min_principal_margin": str(min(principal_margins(principal_not_ct))),
        "example_min_ct_margin": str(min(ct_margins(principal_not_ct))),
    }

    base_q, arrays, lam = make_sunlet_map()
    factors = circuit_pullbacks(base_q)
    a, b, cc, d, e, f = (arrays[name] for name in "abcdef")
    mu = lam * (1 - lam)
    expected = (
        mu*a[1]*a[2]*b[2]*b[3]*cc[1]*cc[3]*(f[1]*f[3]-f[2])*(d[1]*e[3]-d[3]*e[1]*f[2]),
        mu*a[1]*a[3]*b[2]*b[3]*cc[1]*cc[2]*(f[1]*f[2]-f[3])*(d[1]*e[2]-d[2]*e[1]*f[3]),
        -mu*a[2]*a[3]*b[1]*b[2]*cc[1]*cc[3]*(f[1]*f[3]-f[2])*(d[1]*e[3]*f[2]-d[3]*e[1]),
        -mu*a[2]*a[3]*b[1]*b[3]*cc[1]*cc[2]*(f[1]*f[2]-f[3])*(d[1]*e[2]*f[3]-d[2]*e[1]),
        -mu*a[1]*a[2]*b[1]*b[3]*cc[2]*cc[3]*(f[1]-f[2]*f[3])*(d[2]*e[3]-d[3]*e[2]*f[1]),
        mu*a[1]*a[3]*b[1]*b[2]*cc[2]*cc[3]*(f[1]-f[2]*f[3])*(d[2]*e[3]*f[1]-d[3]*e[2]),
    )
    assert all(sp.expand(actual - stated) == 0 for actual, stated in zip(factors, expected))

    # Independent symbolic replay of the pointwise strictness argument.  If a
    # composition margin is nonzero, simultaneous vanishing of its paired
    # circuits would force one strict edge eigenvalue to have square one.
    cross_1 = d[1]*e[3] - d[3]*e[1]*f[2]
    cross_3 = d[1]*e[3]*f[2] - d[3]*e[1]
    cross_2 = d[1]*e[2] - d[2]*e[1]*f[3]
    cross_4 = d[1]*e[2]*f[3] - d[2]*e[1]
    cross_5 = d[2]*e[3] - d[3]*e[2]*f[1]
    cross_6 = d[2]*e[3]*f[1] - d[3]*e[2]
    cancellation_identities = (
        sp.expand(cross_1 - f[2]*cross_3 - d[1]*e[3]*(1-f[2]**2)),
        sp.expand(cross_2 - f[3]*cross_4 - d[1]*e[2]*(1-f[3]**2)),
        sp.expand(cross_5 - f[1]*cross_6 - d[2]*e[3]*(1-f[1]**2)),
    )
    assert cancellation_identities == (0, 0, 0)
    p = f[1]*f[2]*f[3]
    product_of_margin_right_sides = (f[1]*f[3])*(f[1]*f[2])*(f[2]*f[3])
    assert sp.expand(product_of_margin_right_sides - p**2) == 0
    parameters = [value for name in "abcdef" for value in arrays[name][1:]] + [lam]
    trials, smallest = numeric_separator_search(factors, parameters)
    assert all(sp.expand(expression.subs({f[index]: 1 for index in (1, 2, 3)})) == 0 for expression in factors)
    assert all(sp.expand(expression.subs({lam: 0})) == 0 for expression in factors)
    report["tree_sunlet"] = {
        "literal_six_factored_pullbacks": [str(expression) for expression in factors],
        "paired_cross_cancellation_identities": [
            "cross1-fG*cross3=dC*eT*(1-fG^2)",
            "cross2-fT*cross4=dC*eG*(1-fT^2)",
            "cross5-fC*cross6=dG*eT*(1-fC^2)",
        ],
        "all_composition_margins_zero_product_identity": "p=p^2 for p=fC*fG*fT",
        "strict_separator_conclusion": (
            "A nonzero composition margin makes its paired circuits unable to vanish together; "
            "if all three margins vanish then 0<p<1 and p=p^2, a contradiction."
        ),
        "strict_principal_random_trials": trials,
        "smallest_sum_of_squares_seen": smallest,
        "boundary_zero_checks": ["f=(1,1,1)", "lambda=0"],
    }

    annihilation = {}
    for perm in permutations(range(3)):
        value = sp.factor(h14(permuted_map(base_q, perm)))
        annihilation["".join(map(str, perm))] = value == 0
    assert all(annihilation.values())

    qvars = {word: sp.Integer(1) if word == "000" else sp.symbols("q_" + word) for word in ORDER3}
    polynomial = h14(qvars.__getitem__)
    assert sp.factor(polynomial) == polynomial
    linear_coefficient = sp.diff(polynomial, qvars["0CC"])
    constant_remainder = sp.expand(polynomial.subs(qvars["0CC"], 0))
    gcd = sp.gcd(linear_coefficient, constant_remainder)
    assert gcd == 1

    isotropic = {}
    for name in "abcde":
        isotropic.update({arrays[name][index]: sp.Rational(1, 2) for index in (1, 2, 3)})
    isotropic.update({arrays["f"][index]: sp.Rational(1, 3) for index in (1, 2, 3)})
    isotropic[lam] = sp.Rational(1, 2)
    assert min(ct_margins((sp.Rational(1, 2),) * 3)) > 0
    assert min(ct_margins((sp.Rational(1, 3),) * 3)) > 0
    expected_q0 = (
        sp.Integer(1), sp.Rational(1, 12), sp.Rational(1, 12), sp.Rational(1, 12),
        sp.Rational(1, 12), sp.Rational(1, 12), sp.Rational(1, 48), sp.Rational(1, 48),
        sp.Rational(1, 12), sp.Rational(1, 48), sp.Rational(1, 12), sp.Rational(1, 48),
        sp.Rational(1, 12), sp.Rational(1, 48), sp.Rational(1, 48), sp.Rational(1, 12),
    )
    orientations = {}
    for perm in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        qmap = permuted_map(base_q, perm)
        outputs = [qmap(word) for word in ORDER3[1:]]
        image = tuple([sp.Integer(1)] + [sp.factor(value.subs(isotropic)) for value in outputs])
        assert image == expected_q0
        jacobian = sp.Matrix(outputs).jacobian(parameters).subs(isotropic)
        rank, rows, columns, determinant = independent_square_minor(jacobian)
        assert rank == 14
        orientations["".join(map(str, perm))] = {
            "same_common_point": True,
            "rank": rank,
            "minor_rows_zero_based": rows,
            "minor_columns_zero_based": columns,
            "minor_determinant": str(determinant),
        }

    q0_substitution = {
        qvars[word]: expected_q0[index]
        for index, word in enumerate(ORDER3)
        if word != "000"
    }
    gradient = [
        sp.factor(sp.diff(polynomial, qvars[word]).subs(q0_substitution))
        for word in ORDER3[1:]
    ]
    nonzero_gradient = [value for value in gradient if value]
    assert len(nonzero_gradient) == 6
    assert {abs(value) for value in nonzero_gradient} == {sp.Rational(1, 6912)}
    report["H14"] = {
        "annihilation_under_all_six_leaf_permutations": annihilation,
        "primitive_linear_coefficient_gcd_remainder": str(gcd),
        "irreducible_over_Q_by_primitive_linear_argument": True,
        "three_orientation_common_point_and_ranks": orientations,
        "common_point_is_strict_continuous_time": True,
        "common_point_gradient_nonzero_count": len(nonzero_gradient),
        "common_point_gradient_nonzero_absolute_value": "1/6912",
        "smooth_hypersurface_germ_at_common_point": True,
    }

    uC, vC, uG, vG, uT, vT = sp.symbols("uC vC uG vG uT vT", positive=True)
    inputs = (uC, vC, uG, vG, uT, vT)
    outputs = (uC/vC, uC*vC, uG/vG, uG*vG, uT/vT, uT*vT)
    determinant = sp.factor(sp.Matrix(outputs).jacobian(inputs).det())
    asserted = 8*uC*uG*uT/(vC*vG*vT)
    assert sp.simplify(determinant - asserted) == 0
    RC, PC, RG, PG, RT, PT = sp.symbols("RC PC RG PG RT PT", positive=True)
    inverse = (
        sp.sqrt(RC*PC), sp.sqrt(PC/RC),
        sp.sqrt(RG*PG), sp.sqrt(PG/RG),
        sp.sqrt(RT*PT), sp.sqrt(PT/RT),
    )
    forward_after_inverse = (
        inverse[0]/inverse[1], inverse[0]*inverse[1],
        inverse[2]/inverse[3], inverse[2]*inverse[3],
        inverse[4]/inverse[5], inverse[4]*inverse[5],
    )
    assert all(
        sp.simplify(actual-expected) == 0
        for actual, expected in zip(forward_after_inverse, (RC, PC, RG, PG, RT, PT))
    )
    inverse_after_forward = (
        sp.sqrt(outputs[0]*outputs[1]), sp.sqrt(outputs[1]/outputs[0]),
        sp.sqrt(outputs[2]*outputs[3]), sp.sqrt(outputs[3]/outputs[2]),
        sp.sqrt(outputs[4]*outputs[5]), sp.sqrt(outputs[5]/outputs[4]),
    )
    assert all(
        sp.simplify(actual-expected) == 0
        for actual, expected in zip(inverse_after_forward, inputs)
    )
    u = (Fraction(2, 5), Fraction(4, 9), Fraction(3, 7))
    v = (Fraction(3, 7), Fraction(5, 11), Fraction(4, 9))
    determinant_at_point = Fraction(8) * u[0]*u[1]*u[2] / (v[0]*v[1]*v[2])
    assert determinant_at_point == Fraction(176, 25)
    assert min(ct_margins(u)) > 0 and min(ct_margins(v)) > 0
    report["cherry"] = {
        "jacobian_determinant": str(determinant),
        "strict_ct_point_determinant": str(determinant_at_point),
        "u_min_ct_margin": str(min(ct_margins(u))),
        "v_min_ct_margin": str(min(ct_margins(v))),
        "positive_branch_inverse": ["u_h=sqrt(R_h P_h)", "v_h=sqrt(P_h/R_h)"],
        "forward_inverse_both_compositions_exact": True,
    }

    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    destination = args.output_dir / "three_leaf_geometry.json"
    destination.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
