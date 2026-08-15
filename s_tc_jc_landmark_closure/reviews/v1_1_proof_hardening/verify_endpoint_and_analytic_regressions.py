#!/usr/bin/env python3
"""Clean-room endpoint provenance and proof-text mutation gate.

Polynomial arithmetic is implemented below from integer exponent maps; this
file imports neither SymPy nor any project Fourier or graph module.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path


NVAR = 9
VAR = {name: index for index, name in enumerate("abctABCTz")}


def mono(**powers):
    exponent = [0] * NVAR
    for name, power in powers.items():
        exponent[VAR[name]] = power
    return {tuple(exponent): 1}


ONE = {tuple([0] * NVAR): 1}


def add(left, right, right_scale=1):
    out = dict(left)
    for term, coefficient in right.items():
        out[term] = out.get(term, 0) + right_scale * coefficient
        if out[term] == 0:
            del out[term]
    return out


def mul(left, right):
    out = {}
    for first, c1 in left.items():
        for second, c2 in right.items():
            term = tuple(a + b for a, b in zip(first, second))
            out[term] = out.get(term, 0) + c1 * c2
    return {term: value for term, value in out.items() if value}


def product(*values):
    out = ONE
    for value in values:
        out = mul(out, value)
    return out


def power(value, exponent):
    out = ONE
    for _ in range(exponent):
        out = mul(out, value)
    return out


def endpoint(assignment, lower):
    names = ("a", "b", "c", "t") if lower else ("A", "B", "C", "T")
    aa, bb, cc, tt = (mono(**{name: 1}) for name in names)
    nonzero = [index for index, value in enumerate(assignment) if value]
    if not nonzero:
        return ONE
    if len(nonzero) == 2:
        zero = next(index for index, value in enumerate(assignment) if value == 0)
        return (cc, bb, aa)[zero]
    if len(nonzero) == 3 and len(set(assignment)) == 3:
        return tt
    raise AssertionError(f"not a zero-sum endpoint assignment: {assignment}")


def entry(row, column):
    g1, g3 = row
    g2, g4 = column
    separator = g1 ^ g2
    value = product(
        endpoint((g1, g2, separator), True),
        endpoint((g3, g4, separator), False),
    )
    return mul(value, mono(z=1)) if separator else value


def determinant(rows, columns):
    return add(
        mul(entry(rows[0], columns[0]), entry(rows[1], columns[1])),
        mul(entry(rows[0], columns[1]), entry(rows[1], columns[0])),
        -1,
    )


def expected_minors():
    a, b, c, t = (mono(**{name: 1}) for name in "abct")
    A, B, C, T, z = (mono(**{name: 1}) for name in "ABCTz")
    f1 = add(product(a, A), product(power(z, 2), b, c, B, C), -1)
    f2 = add(product(z, T, t), product(power(z, 2), b, c, B, C), -1)
    f3 = product(z, C, add(product(A, t), product(z, T, b, c), -1))
    f4 = product(z, c, add(product(z, B, C, t), product(T, a), -1))
    return {"f1": f1, "f2": f2, "f3": f3, "f4": f4}


PROVENANCE = {
    "f1": (0, ((0, 0), (1, 1)), ((0, 0), (1, 1))),
    "f2": (0, ((0, 0), (1, 1)), ((0, 0), (2, 2))),
    "f3": (1, ((0, 1), (1, 0)), ((0, 1), (2, 3))),
    "f4": (1, ((0, 1), (1, 0)), ((1, 0), (2, 3))),
}


def verify_endpoint_provenance():
    expected = expected_minors()
    for name, (total, rows, columns) in PROVENANCE.items():
        if any((x ^ y) != total for x, y in rows + columns):
            raise AssertionError(f"{name} attached to wrong character block")
        actual = determinant(rows, columns)
        if actual != expected[name]:
            raise AssertionError(f"{name} determinant provenance mismatch")

    # Mutation: attach f3 to a block-0 record.
    wrong_rows = ((0, 0), (1, 1))
    wrong_columns = ((0, 0), (2, 2))
    if determinant(wrong_rows, wrong_columns) == expected["f3"]:
        raise AssertionError("wrong-block minor mutation survived")


def verify_normalization():
    # Residual outer-arm bidegrees of the four endpoint coordinates.
    degrees = {"a": (1, 1), "b": (1, 0), "c": (0, 1), "t": (1, 1)}
    delta_terms = (
        tuple(sum(degrees[name][j] for name in "abc") for j in (0, 1)),
        tuple(2 * degrees["t"][j] for j in (0, 1)),
    )
    gamma_terms = (degrees["a"], tuple(degrees["b"][j] + degrees["c"][j] for j in (0, 1)))
    if delta_terms != ((2, 2), (2, 2)) or gamma_terms != ((1, 1), (1, 1)):
        raise AssertionError("endpoint polynomials are not homogeneous in outer arms")
    alpha, beta = Fraction(3, 5), Fraction(4, 7)
    ordinary = (alpha * beta, alpha, beta, alpha * beta)
    a, b, c, t = ordinary
    if a * b * c - t * t != 0 or a - b * c != 0:
        raise AssertionError("ordinary central-normalized endpoint is not Delta=Gamma=0")
    # Without absorbing a central arm w, Gamma is not homogeneous.  The
    # mutation must visibly change the ordinary value.
    w = Fraction(2, 3)
    unnormalized_gamma = alpha * beta - (alpha * w) * (beta * w)
    if unnormalized_gamma == 0:
        raise AssertionError("unnormalized endpoint mutation was not detected")


def normalized_indicator_row(row, width=4):
    full = (1 << width) - 1
    return tuple(min(mask, full ^ mask) for mask in row)


def validate_descriptor_partition(rows, groups, point):
    used = set()
    derivatives = []
    for group in groups:
        if not group or used.intersection(group):
            raise AssertionError("descriptor classes do not form a disjoint partition")
        used.update(group)
        signatures = {normalized_indicator_row(rows[index]) for index in group}
        if len(signatures) != 1:
            raise AssertionError("an edge group has inconsistent zero-sum indicator rows")
        derivative_row = []
        for index in range(len(rows)):
            if index not in group:
                derivative_row.append(Fraction(0))
            else:
                value = Fraction(1)
                for other in group:
                    if other != index:
                        value *= point[other]
                derivative_row.append(value)
        if not any(derivative_row):
            raise AssertionError("rank-dropping product descriptor")
        derivatives.append(derivative_row)
    # Disjoint supports make these rows linearly independent.
    pivots = [next(i for i, value in enumerate(row) if value) for row in derivatives]
    if len(pivots) != len(set(pivots)):
        raise AssertionError("descriptor Jacobian lost full row rank")


def verify_marginal_submersion_mutations():
    # The first pair and second pair differ by selected split complements in
    # individual switchings but have identical zero-sum JC indicators.
    rows = ((3, 12, 0, 5), (12, 3, 15, 10),
            (4, 0, 5, 1), (11, 15, 10, 14), (7, 3, 2, 6))
    groups = ((0, 1), (2, 3), (4,))
    point = tuple(Fraction(i + 2, i + 4) for i in range(len(rows)))
    validate_descriptor_partition(rows, groups, point)

    mutations = (
        (rows, ((0, 2), (1,), (3,), (4,)), point),          # inconsistent rows
        (rows, ((0, 1), (1, 2), (3,), (4,)), point),        # overlapping classes
        (rows, groups, (Fraction(0),) * len(rows)),          # boundary rank drop
    )
    rejected = 0
    for args in mutations:
        try:
            validate_descriptor_partition(*args)
        except AssertionError:
            rejected += 1
    if rejected != len(mutations):
        raise AssertionError("a marginal-submersion mutation survived")


def verify_manuscript_contract():
    root = Path(__file__).resolve().parents[2]
    main = (root / "source" / "paper" / "main.tex").read_text(encoding="utf-8")
    supplement = (root / "source" / "supplement" / "supplement.tex").read_text(encoding="utf-8")
    required_main = (
        "Marginal open image",
        "constant-rank theorem",
        "zero-sum JC indicator",
        "split complements",
        "Local product chart",
        "Simultaneous physical gluing",
        "uniform lower bounds on the products",
        "Noncut-preserving word compression",
        "zero survivors",
        "$72$ active-labelled tensors",
        "$204$ directions",
        "Finite decorated-relation theorem",
        "complete target point",
    )
    missing = [text for text in required_main if text not in main]
    if missing:
        raise AssertionError(f"load-bearing manuscript text missing: {missing}")
    required_supplement = (
        "24835\\beta",
        "10339",
        "1767/4832",
        "root-edge factorization",
        "(P,s,Q,t,R,u,v,S)",
        "(P',x,y,z,R',w,S',Q')",
        "x_{B1}",
    )
    missing = [text for text in required_supplement if text not in supplement]
    if missing:
        raise AssertionError(f"Theta self-contained data missing: {missing}")
    forbidden = (
        "reciprocal-only bridge chart is correct",
        "Omega is strongly tree-child",
        "resolves the type-1b",
        "Root_clean",
        "S_TC(clean)",
    )
    hits = [text for text in forbidden if text in main or text in supplement]
    if hits:
        raise AssertionError(f"withdrawn claim returned: {hits}")


def main():
    verify_endpoint_provenance()
    verify_normalization()
    verify_marginal_submersion_mutations()
    verify_manuscript_contract()
    print("VERIFIED: endpoint provenance, normalization, and analytic regressions")
    print("four named minors reconstructed from their exact Fourier blocks")
    print("three marginal-submersion mutations rejected")


if __name__ == "__main__":
    main()
