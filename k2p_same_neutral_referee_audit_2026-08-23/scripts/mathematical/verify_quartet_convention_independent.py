#!/usr/bin/env python3
"""Independent symbolic check of the quartet-separator character convention."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


ZERO, C, G, T = 0, 1, 2, 3
SPLITS = {
    "A=12|34": ({0, 1}, {2, 3}),
    "B=13|24": ({0, 2}, {1, 3}),
    "C=14|23": ({0, 3}, {1, 2}),
}


def edge_value(char: int, s_value: sp.Expr, g_value: sp.Expr) -> sp.Expr:
    if char == ZERO:
        return sp.Integer(1)
    if char in {C, T}:
        return s_value
    if char == G:
        return g_value
    raise ValueError(char)


def quartet_q(
    pattern: tuple[int, int, int, int],
    split: tuple[set[int], set[int]],
    pendant: list[tuple[sp.Expr, sp.Expr]],
    internal: tuple[sp.Expr, sp.Expr],
) -> sp.Expr:
    if pattern[0] ^ pattern[1] ^ pattern[2] ^ pattern[3]:
        return sp.Integer(0)
    value = sp.Integer(1)
    for char, pair in zip(pattern, pendant):
        value *= edge_value(char, *pair)
    internal_char = ZERO
    for leaf in split[0]:
        internal_char ^= pattern[leaf]
    return sp.factor(value * edge_value(internal_char, *internal))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    s = sp.symbols("s1:5", positive=True)
    g = sp.symbols("g1:5", positive=True)
    si, gi = sp.symbols("sI gI", positive=True)
    pendant = list(zip(s, g))
    internal = (si, gi)

    printed_f_patterns = [(G, G, G, G), (G, G, T, T)]
    printed_g_patterns = [(G, G, G, G), (G, G, T, T), (G, T, T, G), (G, T, G, T)]
    corrected_f_patterns = [(C, C, C, C), (C, C, T, T)]
    corrected_g_patterns = [(C, C, C, C), (C, C, T, T), (C, T, T, C), (C, T, C, T)]
    signs = [1, -1, -1, 1]

    result: dict[str, dict[str, str]] = {}
    expressions: dict[str, dict[str, sp.Expr]] = {}
    for name, split in SPLITS.items():
        q = lambda pattern: quartet_q(pattern, split, pendant, internal)
        printed_f = sp.factor(q(printed_f_patterns[0]) - q(printed_f_patterns[1]))
        printed_g = sp.factor(sum(sign * q(pattern) for sign, pattern in zip(signs, printed_g_patterns)))
        corrected_f = sp.factor(q(corrected_f_patterns[0]) - q(corrected_f_patterns[1]))
        corrected_g = sp.factor(sum(sign * q(pattern) for sign, pattern in zip(signs, corrected_g_patterns)))
        expressions[name] = {
            "printed_F": printed_f,
            "printed_G": printed_g,
            "corrected_F": corrected_f,
            "corrected_G": corrected_g,
        }
        result[name] = {
            "printed_F": str(printed_f),
            "printed_G": str(printed_g),
            "corrected_F": str(corrected_f),
            "corrected_G": str(corrected_g),
        }

    expected_product = sp.prod(s)
    assert expressions["A=12|34"]["corrected_F"] == 0
    assert sp.simplify(expressions["B=13|24"]["corrected_F"] - expected_product * (1 - gi)) == 0
    assert sp.simplify(expressions["C=14|23"]["corrected_F"] - expected_product * (1 - gi)) == 0
    assert expressions["A=12|34"]["corrected_G"] == 0
    assert sp.simplify(expressions["B=13|24"]["corrected_G"] - 2 * expected_product * (1 - gi)) == 0
    assert expressions["C=14|23"]["corrected_G"] == 0
    assert expressions["A=12|34"]["printed_F"] != 0

    half = sp.Rational(1, 2)
    counterexample_pendant = [(half, half), (half, half), (half, sp.Rational(1, 3)), (half, half)]
    counterexample_internal = (half, half)
    q_counter = lambda pattern: quartet_q(
        pattern,
        SPLITS["A=12|34"],
        counterexample_pendant,
        counterexample_internal,
    )
    q_gggg = q_counter((G, G, G, G))
    q_ggtt = q_counter((G, G, T, T))
    assert q_gggg == sp.Rational(1, 24)
    assert q_ggtt == sp.Rational(1, 16)
    assert q_gggg - q_ggtt == sp.Rational(-1, 48)
    assert all(pair[1] > pair[0] ** 2 for pair in counterexample_pendant + [counterexample_internal])

    payload = {
        "schema": "independent-k2p-quartet-convention-v1",
        "imports_submission_code": False,
        "submission_character_order": ["0", "C", "G", "T"],
        "submission_edge_spectrum": ["1", "s", "g", "s"],
        "equal_sector": ["C", "T"],
        "split_pullbacks": result,
        "strict_continuous_time_counterexample": {
            "topology": "12|34",
            "pendant_pairs": [["1/2", "1/2"], ["1/2", "1/2"], ["1/2", "1/3"], ["1/2", "1/2"]],
            "internal_pair": ["1/2", "1/2"],
            "q_GGGG": str(q_gggg),
            "q_GGTT": str(q_ggtt),
            "printed_F": str(q_gggg - q_ggtt),
        },
        "printed_formula_status": "FAIL",
        "corrected_formula_status": "PASS",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("INDEPENDENT_QUARTET_CONVENTION_DEFECT_CONFIRMED")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
