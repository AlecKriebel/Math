#!/usr/bin/env python3
"""Fresh review-owned exact checks for the R5 K2P-SAME referee run.

This script imports no submitted code, classifier, graph generator, ledger, or
expected-output file.  All arithmetic is ``Fraction`` or SymPy exact arithmetic.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path

import sympy as sp


GROUP = {"0": 0, "C": 1, "G": 2, "T": 3}
ORBIT_WORDS = ["000", "0CC", "0GG", "C0C", "CC0",
               "CGT", "CTG", "G0G", "GCT", "GG0"]


def fstr(value: F | sp.Expr) -> str:
    return str(sp.factor(value))


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def completion_counts() -> dict[str, object]:
    # (name, directed segments m, path sinks q, minimal repair tags r)
    cores = [("cycle", 2, 1, 1), ("theta0", 5, 1, 2),
             ("theta1", 5, 1, 2), ("theta2", 6, 2, 4),
             ("theta3", 6, 2, 2)]

    def breakdown(k: int, epsilon: int) -> dict[str, int]:
        return {
            name: repairs * sum(
                comb(sinks, j)
                * comb(k - epsilon - j + segments - 1, segments - 1)
                for j in range(sinks + 1)
            )
            for name, segments, sinks, repairs in cores
        }

    cases = {}
    expected = {
        "4,1": ([7, 100, 100, 416, 208], 831),
        "4,0": ([9, 210, 210, 1036, 518], 1983),
        "5,1": ([9, 210, 210, 1036, 518], 1983),
        "5,0": ([11, 392, 392, 2240, 1120], 4155),
    }
    for key, (parts, total) in expected.items():
        k, epsilon = map(int, key.split(","))
        row = breakdown(k, epsilon)
        assert list(row.values()) == parts
        assert sum(row.values()) == total
        cases[key] = {"subtotals": row, "total": total}

    c31 = sum(breakdown(3, 1).values())
    c30 = sum(breakdown(3, 0).values())
    raw = {
        "four_port": 6 * (831 + 1983) * 24,
        "five_port": 4 * (1983 + 4155) * 120,
        "cycle_base": 2 * (c31 + c30) * 6,
    }
    assert (c31, c30) == (289, 831)
    assert raw == {"four_port": 405216, "five_port": 2946240,
                   "cycle_base": 13440}
    return {"formula": "r*sum_j binom(q,j)binom(k-epsilon-j+m-1,m-1)",
            "cases": cases, "C(3,1)": c31, "C(3,0)": c30,
            "raw_direction_totals": raw}


def dplus_check(s: F, g: F) -> dict[str, str]:
    margins = {
        "s": s, "1-s": 1 - s, "g": g, "1-g": 1 - g,
        "g-(2s-1)": g - (2 * s - 1),
    }
    assert all(value > 0 for value in margins.values())
    probabilities = [(1 + 2 * s + g) / 4, (1 - g) / 4,
                     (1 - 2 * s + g) / 4, (1 - g) / 4]
    assert all(value > 0 for value in probabilities)
    assert sum(probabilities) == 1
    return {key: fstr(value) for key, value in margins.items()} | {
        "transition_probabilities": [fstr(value) for value in probabilities]
    }


def domain_and_section_checks() -> dict[str, object]:
    points = {
        "near_slanted_face": (F(999, 1000), F(998000001, 10**9)),
        "near_g_zero": (F(1, 4), F(1, 10**9)),
        "near_g_one": (F(3, 4), 1 - F(1, 10**9)),
        "near_ct_face": (F(999, 1000), F(99800101, 100000000)),
    }
    point_results = {
        name: {"point": [fstr(s), fstr(g)], "margins": dplus_check(s, g)}
        for name, (s, g) in points.items()
    }
    ct_s, ct_g = points["near_ct_face"]
    assert ct_g - ct_s**2 == F(1, 100000000)
    point_results["near_ct_face"]["g-s^2"] = "1/100000000"

    products = []
    values = list(points.items())
    for left_name, (s1, g1) in values:
        for right_name, (s2, g2) in values:
            dplus_check(s1 * s2, g1 * g2)
            products.append({"left": left_name, "right": right_name,
                             "product": [fstr(s1 * s2), fstr(g1 * g2)]})

    # In the only nonautomatic case s1,s2>1/2, write gi=2si-1+ei.
    s1, s2, e1, e2 = sp.symbols("s1 s2 e1 e2")
    closure_gap = sp.expand(
        (2 * s1 - 1 + e1) * (2 * s2 - 1 + e2)
        - (2 * s1 * s2 - 1)
    )
    expected_gap = (2 * (1 - s1) * (1 - s2)
                    + e1 * (2 * s2 - 1) + e2 * (2 * s1 - 1) + e1 * e2)
    assert sp.expand(closure_gap - expected_gap) == 0

    target_s = F(999, 1000)
    target_g = F(99800101, 100000000)
    m = 4
    r = F(9999999, 10000000)
    power = r ** (m - 1)
    bound = max(target_s, target_g, 2 * target_s - target_g, F(0))
    assert bound < power < 1
    factors = [(r, r)] * (m - 1) + [(target_s / power, target_g / power)]
    for pair in factors:
        dplus_check(*pair)
    product_s = product_g = F(1)
    for factor_s, factor_g in factors:
        product_s *= factor_s
        product_g *= factor_g
    assert (product_s, product_g) == (target_s, target_g)

    return {
        "arithmetic": "fractions.Fraction and exact SymPy only",
        "boundary_points": point_results,
        "pair_product_checks": len(products),
        "symbolic_product_gap_identity": fstr(closure_gap),
        "four_factor_section": {
            "target": [fstr(target_s), fstr(target_g)],
            "r": fstr(r), "r^3": fstr(power), "bound": fstr(bound),
            "last_factor": [fstr(x) for x in factors[-1]],
            "recovered_product": [fstr(product_s), fstr(product_g)],
        },
    }


def triangle_checks() -> dict[str, object]:
    half, third, delta = sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 2)

    def eigen(character: int, value: sp.Rational) -> sp.Expr:
        return sp.Integer(1) if character == 0 else value

    def q(x: int, y: int, z: int) -> sp.Expr:
        return (eigen(x, half) * eigen(y, half) * eigen(z, half)
                * (delta * eigen(y, third) * eigen(z, half)
                   + (1 - delta) * eigen(x, third) * eigen(z, half)))

    pair = [q(1, 1, 0), q(2, 2, 0), q(1, 0, 1),
            q(2, 0, 2), q(0, 1, 1), q(0, 2, 2)]
    triple = [q(1, 2, 3), q(1, 3, 2), q(2, 1, 3)]
    assert set(pair) == {sp.Rational(1, 12)}
    assert set(triple) == {sp.Rational(1, 48)}

    j0 = sp.Matrix([[1, 1, 0, 1], [1, 0, 1, sp.Rational(1, 4)],
                    [0, 1, 1, sp.Rational(1, 4)], [1, 1, 1, 1]])
    jp = sp.Matrix([
        [1, 1, 0, 0, 1], [1, 0, 1, sp.Rational(3, 4), sp.Rational(1, 4)],
        [0, 1, 1, sp.Rational(1, 4), sp.Rational(1, 4)], [-1, 1, 0, 0, 0],
        [-1, 0, 1, sp.Rational(1, 2), sp.Rational(-1, 2)],
    ])
    assert j0.det() == sp.Rational(-1, 2)
    assert jp.det() == sp.Rational(-1, 4)
    assert j0.det() * jp.det() == sp.Rational(1, 8)
    return {"six_pair_coordinates": [fstr(x) for x in pair],
            "three_triple_coordinates": [fstr(x) for x in triple],
            "det_4x4": "-1/2", "det_5x5": "-1/4",
            "det_product": "1/8"}


def descendants(vertices: set[str], active_arcs: list[tuple[str, str]],
                leaves: dict[str, int]) -> dict[tuple[str, str], set[int]]:
    children = {vertex: [] for vertex in vertices}
    for parent, child in active_arcs:
        children[parent].append(child)
    memo: dict[str, set[int]] = {}

    def below(vertex: str) -> set[int]:
        if vertex not in memo:
            memo[vertex] = ({leaves[vertex]} if vertex in leaves else
                            set().union(*(below(child) for child in children[vertex])))
        return memo[vertex]

    return {arc: below(arc[1]) for arc in active_arcs}


def network_fourier(arcs, leaves, reticulation_choices, edge_parameters, assignment):
    vertices = set(sum(([u, v] for u, v in arcs), []))
    answer = sp.Integer(0)
    for selections in product(*[choices for _, choices in reticulation_choices]):
        chosen_arcs = {entry[0] for entry in selections}
        reticulation_arcs = {arc for _, choices in reticulation_choices for arc, _ in choices}
        active = [arc for arc in arcs if arc not in reticulation_arcs or arc in chosen_arcs]
        term = sp.prod(probability for _, probability in selections)
        below = descendants(vertices, active, leaves)
        for arc in active:
            character = 0
            for label in below[arc]:
                character ^= assignment[label]
            if character:
                s, g = edge_parameters[arc]
                term *= g if character == 2 else s
        answer += term
    return sp.expand(answer)


def weak_sharpness_checks() -> dict[str, object]:
    delta = F(1, 2**30)
    cases = [
        {
            "name": "W",
            "arcs": [("r", "S"), ("r", "L0"), ("S", "U"), ("S", "V"),
                     ("U", "X"), ("V", "Z"), ("Z", "X"), ("U", "V"),
                     ("Z", "L1"), ("X", "L2")],
            "internal": [("r", "S"), ("S", "U"), ("S", "V"), ("U", "X"),
                         ("V", "Z"), ("Z", "X"), ("U", "V")],
            "pendant": {("r", "L0"): F(86779, 80) * delta,
                        ("Z", "L1"): F(320, 253) * delta,
                        ("X", "L2"): F(114373, 20240) * delta},
            "choices": [("X", [(('Z', 'X'), sp.Rational(15996, 16339)),
                                  (('U', 'X'), sp.Rational(343, 16339))]),
                        ("V", [(('S', 'V'), sp.Rational(1, 8)),
                                  (('U', 'V'), sp.Rational(7, 8))])],
            "value": sp.Rational(1, 7),
            "edge_order": [("Z", "X"), ("S", "V"), ("r", "S"), ("S", "U"),
                           ("U", "V"), ("V", "Z"), ("U", "X")],
            "rows": [1, 2, 3, 5, 4, 7, 6, 8, 9],
            "expected_det": sp.Rational(
                10368019213741323,
                563981315074464023964442388464888915634290688),
        },
        {
            "name": "Wprime",
            "arcs": [("r", "S"), ("r", "L0"), ("S", "U"), ("S", "X0"),
                     ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V"),
                     ("X0", "L1"), ("X1", "L2")],
            "internal": [("r", "S"), ("S", "U"), ("S", "X0"), ("V", "X0"),
                         ("U", "X1"), ("V", "X1"), ("U", "V")],
            "pendant": {("r", "L0"): F(16, 3) * delta,
                        ("X0", "L1"): F(32, 9) * delta,
                        ("X1", "L2"): F(96, 5) * delta},
            "choices": [("X0", [(('V', 'X0'), sp.Rational(1, 6)),
                                   (('S', 'X0'), sp.Rational(5, 6))]),
                        ("X1", [(('V', 'X1'), sp.Rational(1, 2)),
                                   (('U', 'X1'), sp.Rational(1, 2))])],
            "value": sp.Rational(1, 4),
            "edge_order": [("V", "X1"), ("V", "X0"), ("U", "V"), ("r", "S"),
                           ("S", "X0"), ("S", "U"), ("U", "X1")],
            "rows": [1, 2, 3, 5, 4, 6, 7, 8, 9],
            "expected_det": sp.Rational(1435825, 85002596691653613846528),
        },
    ]
    tensors, determinants = {}, {}
    for case in cases:
        parameters, symbols = {}, {}
        for index, edge in enumerate(case["internal"]):
            symbols[edge] = (sp.Symbol(f'{case["name"]}_s{index}'),
                             sp.Symbol(f'{case["name"]}_g{index}'))
            parameters[edge] = symbols[edge]
        for edge, value in case["pendant"].items():
            parameters[edge] = (sp.Rational(value.numerator, value.denominator),) * 2
        normalized = dict(parameters)
        for edge in case["pendant"]:
            normalized[edge] = (sp.Integer(1), sp.Integer(1))

        outputs, normalized_outputs = [], []
        for word in ORBIT_WORDS:
            assignment = {i: GROUP[word[i]] for i in range(3)}
            outputs.append(network_fourier(case["arcs"], {"L0": 0, "L1": 1, "L2": 2},
                                           case["choices"], parameters, assignment))
            normalized_outputs.append(network_fourier(
                case["arcs"], {"L0": 0, "L1": 1, "L2": 2},
                case["choices"], normalized, assignment))
        substitutions = {symbol: case["value"] for pair in symbols.values() for symbol in pair}
        tensors[case["name"]] = [sp.factor(q.subs(substitutions)) for q in outputs]
        columns = [symbol for edge in case["edge_order"] for symbol in symbols[edge]][:9]
        jacobian = sp.Matrix(normalized_outputs).jacobian(columns)
        determinant = sp.factor(jacobian.extract(case["rows"], range(9)).subs(substitutions).det())
        assert determinant == case["expected_det"]
        determinants[case["name"]] = determinant

    d = sp.Rational(delta.numerator, delta.denominator)
    expected = [sp.Integer(1)] + [None] * 9
    for index in [1, 2, 3, 4, 7, 9]:
        expected[index] = d**2
    for index in [5, 6, 8]:
        expected[index] = sp.Rational(4, 5) * d**3
    assert tensors["W"] == expected == tensors["Wprime"]

    us, vs, ug, vg = sp.symbols("us vs ug vg", positive=True)
    observables = sp.Matrix([us / vs, us * vs, ug / vg, ug * vg])
    cherry_det = sp.factor(observables.jacobian([us, vs, ug, vg]).det())
    assert cherry_det == 4 * us * ug / (vs * vg)
    witness = {us: sp.Rational(2, 5), vs: sp.Rational(3, 7),
               ug: sp.Rational(4, 9), vg: sp.Rational(5, 11)}
    assert cherry_det.subs(witness) == sp.Rational(2464, 675)

    return {
        "orbit_order": ORBIT_WORDS,
        "common_tensor": [fstr(value) for value in expected],
        "exact_9x9_determinants": {name: fstr(value) for name, value in determinants.items()},
        "cherry_jacobian_determinant": fstr(cherry_det),
        "cherry_witness_determinant": "2464/675",
    }


def main() -> None:
    result = {
        "schema": "k2p-r5-independent-exact-math-check-v1",
        "independence": "No submitted code, classifier, graph generator, ledger, or expected file imported.",
        "completion_and_raw_counts": completion_counts(),
        "domain_products_and_section": domain_and_section_checks(),
        "ordinary_triangle": triangle_checks(),
        "weak_sharpness": weak_sharpness_checks(),
        "status": "PASS",
    }
    result["payload_sha256"] = canonical_hash(result)
    output = Path(__file__).with_name("r5_exact_math_checks_result.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"],
                      "payload_sha256": result["payload_sha256"],
                      "result": str(output)}, sort_keys=True))


if __name__ == "__main__":
    main()
