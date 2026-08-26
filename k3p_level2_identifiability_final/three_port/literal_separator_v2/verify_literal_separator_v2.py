#!/usr/bin/env python3
"""Independent verifier for the literal-map tree--sunlet separator v2.

This verifier deliberately imports no producer code.  It reconstructs the
printed sunlet map, the tree map, every circuit pullback, every printed factor,
the expanded-polynomial digests, and the strictness cancellation identities
using its own sparse-polynomial implementation.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
from typing import Callable


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = HERE / "K3P_TREE_SUNLET_LITERAL_SEPARATOR_V2.json"
CHARACTERS = "0CGT"
GROUP_VALUE = {"0": 0, "C": 1, "G": 2, "T": 3}
EDGE_ORDER = ("a", "b", "c", "d", "e", "f")
VARIABLE_ORDER = ("L",) + tuple(
    edge + character for edge in EDGE_ORDER for character in "CGT"
)
Monomial = tuple[tuple[str, int], ...]
Polynomial = dict[Monomial, int]


class VerificationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationFailure(message)


def canonical_bytes(value: dict) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def make_monomial(powers: dict[str, int]) -> Monomial:
    return tuple(sorted((name, exponent) for name, exponent in powers.items() if exponent))


def constant(value: int) -> Polynomial:
    return {} if value == 0 else {(): value}


def symbol(name: str) -> Polynomial:
    require(name in VARIABLE_ORDER, f"unknown factor symbol: {name}")
    return {((name, 1),): 1}


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    answer = dict(left)
    for monomial, coefficient in right.items():
        new_coefficient = answer.get(monomial, 0) + coefficient
        if new_coefficient:
            answer[monomial] = new_coefficient
        else:
            answer.pop(monomial, None)
    return answer


def negate(polynomial: Polynomial) -> Polynomial:
    return {monomial: -coefficient for monomial, coefficient in polynomial.items()}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        left_powers = dict(left_monomial)
        for right_monomial, right_coefficient in right.items():
            powers = dict(left_powers)
            for name, exponent in right_monomial:
                powers[name] = powers.get(name, 0) + exponent
            monomial = make_monomial(powers)
            answer[monomial] = (
                answer.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def product(polynomials) -> Polynomial:
    answer = constant(1)
    for polynomial in polynomials:
        answer = multiply(answer, polynomial)
    return answer


def parse_polynomial(text: str) -> Polynomial:
    syntax = ast.parse(text, mode="eval")

    def visit(node: ast.AST) -> Polynomial:
        if isinstance(node, ast.Name):
            return symbol(node.id)
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return constant(node.value)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return negate(visit(node.operand))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return add(visit(node.left), visit(node.right))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub):
            return add(visit(node.left), negate(visit(node.right)))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
            return multiply(visit(node.left), visit(node.right))
        raise VerificationFailure(f"unsupported factor syntax: {ast.dump(node)}")

    return visit(syntax.body)


ONE = constant(1)
L = symbol("L")
ONE_MINUS_L = add(ONE, negate(L))


def edge_character(edge: str, character: str) -> Polynomial:
    require(edge in EDGE_ORDER, f"invalid edge: {edge}")
    require(character in CHARACTERS, f"invalid character: {character}")
    return ONE if character == "0" else symbol(edge + character)


def literal_coordinate(word: str) -> Polynomial:
    require(len(word) == 3, f"invalid coordinate word: {word}")
    require(all(character in CHARACTERS for character in word), f"invalid coordinate: {word}")
    require(
        GROUP_VALUE[word[0]] ^ GROUP_VALUE[word[1]] ^ GROUP_VALUE[word[2]] == 0,
        f"nonconserved coordinate: {word}",
    )
    x, y, z = word
    arm = product(
        (edge_character("a", x), edge_character("b", y), edge_character("c", z))
    )
    displayed_first = product((L, edge_character("f", y), edge_character("d", z)))
    displayed_second = product(
        (ONE_MINUS_L, edge_character("f", x), edge_character("e", z))
    )
    return multiply(arm, add(displayed_first, displayed_second))


def tree_coordinate(word: str) -> Polynomial:
    require(len(word) == 3, f"invalid tree coordinate word: {word}")
    x, y, z = word
    return product(
        (edge_character("a", x), edge_character("b", y), edge_character("c", z))
    )


def circuit_pullback(
    coordinate_map: Callable[[str], Polynomial], left: list[str], right: list[str]
) -> Polynomial:
    return add(
        product(coordinate_map(word) for word in left),
        negate(product(coordinate_map(word) for word in right)),
    )


def generator_order_monomial(monomial: Monomial) -> tuple[int, ...]:
    powers = dict(monomial)
    return tuple(powers.get(name, 0) for name in VARIABLE_ORDER)


def monomial_text(monomial: Monomial) -> str:
    powers = dict(monomial)
    factors = []
    for name in VARIABLE_ORDER:
        exponent = powers.get(name, 0)
        if exponent == 1:
            factors.append(name)
        elif exponent > 1:
            factors.append(f"{name}^{exponent}")
    return "*".join(factors) if factors else "1"


def expanded_digest(polynomial: Polynomial) -> str:
    terms = [
        {"coefficient": polynomial[monomial], "monomial": monomial_text(monomial)}
        for monomial in sorted(polynomial, key=generator_order_monomial)
    ]
    return hashlib.sha256(canonical_bytes({"terms": terms})).hexdigest()


def observable_text(left: list[str], right: list[str]) -> str:
    return "*".join("q" + word for word in left) + "-" + "*".join(
        "q" + word for word in right
    )


def verify_seal(certificate: dict) -> str:
    observed = certificate.get("payload_sha256")
    require(isinstance(observed, str) and len(observed) == 64, "payload seal missing")
    payload = dict(certificate)
    payload.pop("payload_sha256")
    expected = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    require(observed == expected, "payload seal mismatch")
    return observed


def verify_strictness(certificate: dict, records: dict[str, dict]) -> None:
    strictness = certificate.get("strictness_argument", {})
    pairs = strictness.get("paired_cross_cancellations", [])
    require(len(pairs) == 3, "strictness pair census")
    expected_pairs = (
        ("I1", "I3", "fG", "dC*eT*(1-fG*fG)", "fG^2=1"),
        ("I2", "I4", "fT", "dC*eG*(1-fT*fT)", "fT^2=1"),
        ("I5", "I6", "fC", "dG*eT*(1-fC*fC)", "fC^2=1"),
    )
    for row, expected in zip(pairs, expected_pairs):
        first, second, multiplier, right_identity, boundary = expected
        require(row.get("circuits") == [first, second], "strictness circuit pair")
        require(
            row.get("composition_margin") == records[first]["composition_margin"]
            == records[second]["composition_margin"],
            "strictness composition-margin pairing",
        )
        left_identity = add(
            parse_polynomial(records[first]["cross_factor"]),
            negate(
                multiply(
                    symbol(multiplier),
                    parse_polynomial(records[second]["cross_factor"]),
                )
            ),
        )
        require(
            left_identity == parse_polynomial(right_identity),
            f"strictness cross-cancellation mismatch: {first}/{second}",
        )
        require(
            row.get("forced_boundary_if_margin_nonzero_and_both_vanish") == boundary,
            "strictness boundary conclusion",
        )

    all_zero = strictness.get("all_composition_margins_zero", {})
    require(
        all_zero.get("equations")
        == ["fC=fG*fT", "fG=fC*fT", "fT=fC*fG"],
        "all-zero composition equations",
    )
    p = product((symbol("fC"), symbol("fG"), symbol("fT")))
    product_of_right_sides = product(
        (
            multiply(symbol("fG"), symbol("fT")),
            multiply(symbol("fC"), symbol("fT")),
            multiply(symbol("fC"), symbol("fG")),
        )
    )
    require(product_of_right_sides == multiply(p, p), "all-zero product identity")
    require(
        all_zero.get("product_identity") == "p=p^2 for p=fC*fG*fT"
        and all_zero.get("domain_contradiction") == "0<p<1",
        "all-zero domain contradiction",
    )
    require(strictness.get("conclusion") == "At least one Ij is nonzero, so S>0.",
            "strictness conclusion")


def verify(certificate_path: Path) -> dict:
    certificate = json.loads(certificate_path.read_text())
    seal = verify_seal(certificate)
    require(certificate.get("schema") == "k3p-tree-sunlet-literal-separator-v2", "schema")
    require(certificate.get("edge_order") == list(EDGE_ORDER), "literal edge order")
    require(
        certificate.get("map_formula")
        == "q_xyz=a_x*b_y*c_z*(L*f_y*d_z+(1-L)*f_x*e_z)",
        "literal map formula mismatch",
    )
    require(certificate.get("tree_map_formula") == "q_xyz=a_x*b_y*c_z", "tree map formula")
    require(
        certificate.get("observable_separator")
        == "S=I1^2+I2^2+I3^2+I4^2+I5^2+I6^2",
        "separator definition",
    )

    circuits = certificate.get("circuits")
    require(isinstance(circuits, list) and len(circuits) == 6, "six-circuit census")
    require([row.get("id") for row in circuits] == [f"I{i}" for i in range(1, 7)],
            "circuit identifiers")
    records = {row["id"]: row for row in circuits}
    results = []
    for row in circuits:
        circuit_id = row["id"]
        left = row.get("left")
        right = row.get("right")
        require(isinstance(left, list) and isinstance(right, list), f"circuit sides: {circuit_id}")
        require(len(left) == len(right) == 3, f"circuit degree: {circuit_id}")
        require(row.get("observable") == observable_text(left, right),
                f"observable text mismatch: {circuit_id}")

        tree_pullback = circuit_pullback(tree_coordinate, left, right)
        require(not tree_pullback, f"tree pullback nonzero: {circuit_id}")
        require(row.get("tree_pullback") == "identically_zero",
                f"tree certificate wording: {circuit_id}")

        literal_pullback = circuit_pullback(literal_coordinate, left, right)
        require(literal_pullback, f"literal pullback unexpectedly zero: {circuit_id}")
        require(len(literal_pullback) == row.get("expanded_term_count"),
                f"expanded term count mismatch: {circuit_id}")
        require(expanded_digest(literal_pullback) == row.get("expanded_pullback_sha256"),
                f"expanded pullback digest mismatch: {circuit_id}")

        full_factor = parse_polynomial(row.get("literal_sunlet_factor", ""))
        component_factor = product(
            (
                constant(row.get("factor_sign")),
                parse_polynomial(row.get("positive_prefactor", "")),
                parse_polynomial(row.get("composition_margin", "")),
                parse_polynomial(row.get("cross_factor", "")),
            )
        )
        require(full_factor == component_factor,
                f"printed factor/component mismatch: {circuit_id}")
        require(literal_pullback == full_factor,
                f"literal pullback mismatch: {circuit_id}")
        results.append(
            {
                "id": circuit_id,
                "expanded_term_count": len(literal_pullback),
                "expanded_pullback_sha256": expanded_digest(literal_pullback),
                "tree_pullback": "identically_zero",
                "factorization": "PASS",
            }
        )

    verify_strictness(certificate, records)
    return {
        "schema": "k3p-tree-sunlet-literal-separator-v2-independent-verification-v1",
        "status": "PASS",
        "certificate": str(certificate_path),
        "certificate_payload_sha256": seal,
        "literal_map_reexpanded": True,
        "producer_code_imported": False,
        "circuits": results,
        "strictness_argument": "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    args = parser.parse_args()
    try:
        report = verify(args.certificate.resolve())
    except (VerificationFailure, json.JSONDecodeError, OSError, TypeError, ValueError) as error:
        print(f"LITERAL_SEPARATOR_V2_VERIFY_FAIL: {error}", file=sys.stderr)
        return 1
    print("LITERAL_SEPARATOR_V2_VERIFY_PASS")
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
