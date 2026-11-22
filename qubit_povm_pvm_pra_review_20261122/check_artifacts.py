#!/usr/bin/env python3
"""Independently cross-check the paper's physical witnesses and rational SOS inputs.

Requires SymPy 1.14.0. Paths are relative to this file. The checker imports
neither the manuscript's verification scripts nor any Lean proof results.
It checks the SOS operator polynomial for auxiliary support {0,2}. The other
two supports are checked separately by bell_lean/scripts/sos_checks.py.
"""

from collections import defaultdict
import csv
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import re

import sympy as sp


PAPER = Path(__file__).resolve().parent.parent / "qubit_povm_pvm_minimum_settings"
WITNESSES = PAPER / "artifacts" / "three_by_two_separation"
LEAN = PAPER / "bell_lean"
IDENTITY_WORD = ((), ())


def require(condition, description):
    if not condition:
        raise ValueError(description)


def read_coefficients(filename):
    coefficients = {}
    with (WITNESSES / filename).open(newline="") as stream:
        for row in csv.DictReader(stream):
            key = tuple(int(row[column]) for column in ("x", "y", "a", "b"))
            require(key not in coefficients, f"Duplicate row {key} in {filename}")
            coefficients[key] = Fraction(row["c_abxy"])
    return coefficients


def check_functional():
    dense = read_coefficients("bell_coefficients_dense.csv")
    sparse = read_coefficients("bell_coefficients_sparse.csv")
    expected_keys = set(product(range(3), range(2), range(3), range(2)))
    require(set(dense) == expected_keys, "Incorrect dense Bell alphabet")
    require(sparse == {k: v for k, v in dense.items() if v}, "Sparse and dense tables differ")

    discrimination = {
        (2, 0, 0, 0): Fraction(3, 5),
        (2, 0, 1, 1): Fraction(3, 5),
        (2, 1, 2, 0): Fraction(4, 5),
    }
    for (x, y, a, b), coefficient in dense.items():
        if x < 2:
            # 10 times the CHSH sign, Alice's coarse sign, and Bob's sign.
            expected = 10 * (-1) ** (x*y + int(a == 1) + b)
        else:
            expected = discrimination.get((x, y, a, b), 0)
        require(coefficient == expected, f"Coefficient disagrees with the paper at {(x,y,a,b)}")
    print(f"Bell coefficients agree with the paper ({len(dense)} dense, {len(sparse)} nonzero).")
    return dense


def matrix_zero(matrix):
    return all(sp.simplify(entry) == 0 for entry in matrix)


def check_psd(effect):
    # For a 2-by-2 Hermitian matrix, trace and determinant characterize PSD.
    require(effect.shape == (2, 2) and matrix_zero(effect - effect.H), "Expected a Hermitian qubit effect")
    require(sp.simplify(effect.trace()).is_nonnegative, "Could not certify nonnegative trace")
    require(sp.simplify(effect.det()).is_nonnegative, "Could not certify nonnegative determinant")


def check_witness(filename, coefficients, strengthened):
    strategy = json.loads((WITNESSES / filename).read_text())
    names = {"sqrt": sp.sqrt}
    for name, formula in strategy.get("definitions", {}).items():
        names[name] = sp.sympify(formula, locals=names)

    def parse(value):
        return sp.sympify(value, locals=names)

    def matrix(rows):
        return sp.Matrix([[parse(entry) for entry in row] for row in rows])

    def binary(observable):
        return [(sp.eye(2) + observable)/2, (sp.eye(2) - observable)/2]

    if strengthened:
        alice = [binary(matrix(strategy["alice_observables"][f"A{x}"])) + [sp.zeros(2)] for x in range(2)]
        alice.append([matrix(effect) for effect in strategy["alice_x2"]])
        bob = [binary(matrix(strategy["bob_observables"][f"B{y}"])) for y in range(2)]
    else:
        alice = [[matrix(effect) for effect in strategy["alice"][f"x{x}"]] for x in range(3)]
        bob = [[matrix(effect) for effect in strategy["bob"][f"y{y}"]] for y in range(2)]

    state = sp.Matrix(2, 2, [parse(value) for value in strategy["state"]])
    require(sp.simplify((state.H * state).trace() - 1) == 0, "State is not normalized")
    require([len(m) for m in alice + bob] == [3, 3, 3, 2, 2], "Incorrect outcome counts")
    for measurement in alice + bob:
        require(matrix_zero(sum(measurement, sp.zeros(2)) - sp.eye(2)), "Effects do not sum to identity")
        for effect in measurement:
            check_psd(effect)
    for measurement in alice[:2] + bob:
        for effect in measurement:
            require(matrix_zero(effect*effect - effect), "Nonprojective binary or padded binary effect")

    # C reshapes the bipartite state into a 2-by-2 matrix. Contraction by
    # tr(C† A C Bᵀ) is independent of the supplied tensor-product calculation.
    probabilities = {}
    for x, y, a, b in coefficients:
        value = (state.H * alice[x][a] * state * bob[y][b].T).trace()
        probabilities[x, y, a, b] = sp.simplify(value)
    for x, y in product(range(3), range(2)):
        total = sum(probabilities[x, y, a, b] for a, b in product(range(3), range(2)))
        require(sp.simplify(total - 1) == 0, "Born probability block is not normalized")

    score = sp.simplify(sum(coefficient * probabilities[key] for key, coefficient in coefficients.items()))
    require(sp.simplify(score - parse(strategy["attained_value"])) == 0, "Incorrect recorded score")
    if strengthened:
        gamma = matrix(strategy["dual_Gamma"])
        bonus_terms = [(sp.Rational(3, 5), 0, 0), (sp.Rational(3, 5), 0, 1), (sp.Rational(4, 5), 1, 0)]
        for effect, (weight, y, b) in zip(alice[2], bonus_terms):
            slack = gamma - weight * state * bob[y][b].T * state.H
            check_psd(slack)
            require(matrix_zero(slack * effect), "Nonzero complementary slack")
    print(f"{filename} gives {score}.")
    return score


def reduce_involutions(sequence):
    """Reduce a word, using only the adjacent relation g g = identity."""
    result = []
    for letter in sequence:
        if result and result[-1] == letter:
            result.pop()
        else:
            result.append(letter)
    return tuple(result)


def support_02_polynomial(coefficients):
    """Expand the probability CSV using the two complementary projectors per input."""
    polynomial = defaultdict(Fraction)
    for (x, y, a, b), coefficient in coefficients.items():
        # x=0,1 use the coarse binary PVM; for x=2 the support is {0,2}.
        # This expands (I+sA_x)(I+tB_y)/4 entry by entry.
        labels = [0, 1] if x < 2 else [0, 2]
        if a not in labels:
            continue
        alice_sign = (-1) ** labels.index(a)
        bob_sign = (-1) ** b
        polynomial[IDENTITY_WORD] += coefficient / 4
        polynomial[(x,), ()] += coefficient * alice_sign / 4
        polynomial[(), (y,)] += coefficient * bob_sign / 4
        polynomial[(x,), (y,)] += coefficient * alice_sign * bob_sign / 4
    return {key: value for key, value in polynomial.items() if value}


def check_sos(coefficients):
    data = json.loads((LEAN / "certificates" / "binary_pair_sos.json").read_text())
    polynomial = support_02_polynomial(coefficients)
    listed = {IDENTITY_WORD: Fraction(data["bell_constant"])}
    for entry in data["bell_nonconstant_coefficients"]:
        a, b = entry["word"]
        word = tuple(a), tuple(b)
        require(word not in listed, "Duplicate SOS functional coefficient")
        listed[word] = Fraction(entry["coefficient"])
    require(listed == polynomial, "SOS functional metadata differs from the probability CSV")

    bound = Fraction(data["bound"])
    require(bound == Fraction(289, 10), "Wrong target bound")
    target = {word: -value for word, value in polynomial.items()}
    target[IDENTITY_WORD] += bound

    words = [(tuple(a), tuple(b)) for a, b in data["words"]]
    numerator = data["gram_integer_numerator"]
    denominator = data["gram_common_denominator"]
    gram = defaultdict(Fraction)
    for i, (a, b) in enumerate(words):
        for j, (c, d) in enumerate(words):
            word = (reduce_involutions(a[::-1] + c), reduce_involutions(b[::-1] + d))
            gram[word] += Fraction(numerator[i][j], denominator)
    require({k: v for k, v in gram.items() if v} == target, "The Gram polynomial differs from bound minus Bell")

    integer_matrix = sp.Matrix(numerator)
    require(denominator > 0 and integer_matrix == integer_matrix.T, "Invalid Gram symmetry or scale")
    require(integer_matrix.shape == (12, 12), "Incorrect Gram shape")
    minors = [integer_matrix[:k, :k].det(method="berkowitz") for k in range(1, 13)]
    require(all(minor > 0 for minor in minors), "Nonpositive leading principal minor")
    print(f"All 12 Berkowitz principal minors are positive. Integer Gram determinant = {minors[-1]}.")

    lean_text = (LEAN / "Bell" / "SOSCertificate.lean").read_text()
    for lean_name, json_key in [("numerator", "gram_integer_numerator"), ("L", "ldl_unit_lower"),
                                ("d", "ldl_positive_diagonal")]:
        # Read the literal numeral arrays only. Checking their arithmetic in
        # Lean is a separate task. Exact Fractions forbid float coincidences.
        block = lean_text.split(f"def {lean_name} :", 1)[1].split(":=", 1)[1].split("\n\n")[0]
        values = [Fraction(z) for z in re.findall(r"-?\d+(?:/\d+)?", block)]
        raw = data[json_key]
        flat = raw if lean_name == "d" else [entry for row in raw for entry in row]
        require(values == list(map(Fraction, flat)), f"Lean literal mismatch in {lean_name}")
        print(f"All {len(values)} Lean literals agree with JSON for {lean_name}.")
    return bound


def main():
    coefficients = check_functional()
    simple = check_witness("strategy_simple_qsqrt2.json", coefficients, strengthened=False)
    strengthened = check_witness("strategy_strengthened_algebraic.json", coefficients, strengthened=True)
    bound = check_sos(coefficients)
    require(sp.simplify(simple - (20*sp.sqrt(2) + sp.Rational(16, 25))) == 0, "Wrong simple score")
    require(sp.simplify(strengthened - (16 + 8*sp.sqrt(7813))/25) == 0, "Wrong strengthened score")
    gap = sp.simplify(strengthened - bound)
    require(gap.is_positive, "Could not certify a strictly positive gap")
    print(f"Strengthened witness minus the SOS bound = {gap} (about {float(gap):.12f}).")


if __name__ == "__main__":
    main()
