#!/usr/bin/env python3
"""Generate the literal-map K3P tree--sunlet separator certificate.

The implemented sunlet convention is exactly

    q_xyz = a_x b_y c_z [L f_y d_z + (1-L) f_x e_z].

Only Python's standard library is used.  Polynomials are expanded over ZZ by
an elementary sparse-polynomial implementation, so certificate generation is
deterministic and does not depend on a computer-algebra system.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable


CHARACTERS = "0CGT"
EDGE_ORDER = ("a", "b", "c", "d", "e", "f")
VARIABLE_ORDER = ("L",) + tuple(
    edge + character for edge in EDGE_ORDER for character in "CGT"
)
VARIABLE_INDEX = {name: index for index, name in enumerate(VARIABLE_ORDER)}
Monomial = tuple[int, ...]
Polynomial = dict[Monomial, int]
ZERO_MONOMIAL = (0,) * len(VARIABLE_ORDER)


def add(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            value = answer.get(monomial, 0) + coefficient
            if value:
                answer[monomial] = value
            elif monomial in answer:
                del answer[monomial]
    return answer


def scale(coefficient: int, polynomial: Polynomial) -> Polynomial:
    if not coefficient:
        return {}
    return {monomial: coefficient * value for monomial, value in polynomial.items()}


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                x + y for x, y in zip(left_monomial, right_monomial)
            )
            answer[monomial] = (
                answer.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def product(polynomials: Iterable[Polynomial]) -> Polynomial:
    answer = {ZERO_MONOMIAL: 1}
    for polynomial in polynomials:
        answer = multiply(answer, polynomial)
    return answer


def variable(name: str) -> Polynomial:
    exponent = [0] * len(VARIABLE_ORDER)
    exponent[VARIABLE_INDEX[name]] = 1
    return {tuple(exponent): 1}


ONE = {ZERO_MONOMIAL: 1}
L = variable("L")
ONE_MINUS_L = add(ONE, scale(-1, L))


def edge_value(edge: str, character: str) -> Polynomial:
    return ONE if character == "0" else variable(edge + character)


def literal_sunlet_coordinate(word: str) -> Polynomial:
    x, y, z = word
    arms = product((edge_value("a", x), edge_value("b", y), edge_value("c", z)))
    first = product((L, edge_value("f", y), edge_value("d", z)))
    second = product((ONE_MINUS_L, edge_value("f", x), edge_value("e", z)))
    return multiply(arms, add(first, second))


def tree_coordinate(word: str) -> Polynomial:
    x, y, z = word
    return product((edge_value("a", x), edge_value("b", y), edge_value("c", z)))


def binomial(positive: tuple[str, ...], negative: tuple[str, ...]) -> Polynomial:
    return add(
        product(variable(name) for name in positive),
        scale(-1, product(variable(name) for name in negative)),
    )


def circuit_pullback(
    coordinate_map, left: tuple[str, ...], right: tuple[str, ...]
) -> Polynomial:
    return add(
        product(coordinate_map(word) for word in left),
        scale(-1, product(coordinate_map(word) for word in right)),
    )


SPECS = (
    {
        "id": "I1",
        "left": ("000", "CGT", "GTC"),
        "right": ("0TT", "C0C", "GG0"),
        "sign": 1,
        "arms": ("aC", "aG", "bG", "bT", "cC", "cT"),
        "margin": (("fC", "fT"), ("fG",)),
        "cross": (("dC", "eT"), ("dT", "eC", "fG")),
    },
    {
        "id": "I2",
        "left": ("000", "CTG", "TGC"),
        "right": ("0GG", "C0C", "TT0"),
        "sign": 1,
        "arms": ("aC", "aT", "bG", "bT", "cC", "cG"),
        "margin": (("fC", "fG"), ("fT",)),
        "cross": (("dC", "eG"), ("dG", "eC", "fT")),
    },
    {
        "id": "I3",
        "left": ("000", "GCT", "TGC"),
        "right": ("0CC", "GG0", "T0T"),
        "sign": -1,
        "arms": ("aG", "aT", "bC", "bG", "cC", "cT"),
        "margin": (("fC", "fT"), ("fG",)),
        "cross": (("dC", "eT", "fG"), ("dT", "eC")),
    },
    {
        "id": "I4",
        "left": ("000", "GTC", "TCG"),
        "right": ("0CC", "G0G", "TT0"),
        "sign": -1,
        "arms": ("aG", "aT", "bC", "bT", "cC", "cG"),
        "margin": (("fC", "fG"), ("fT",)),
        "cross": (("dC", "eG", "fT"), ("dG", "eC")),
    },
    {
        "id": "I5",
        "left": ("000", "CTG", "GCT"),
        "right": ("0TT", "CC0", "G0G"),
        "sign": -1,
        "arms": ("aC", "aG", "bC", "bT", "cG", "cT"),
        "margin": (("fC",), ("fG", "fT")),
        "cross": (("dG", "eT"), ("dT", "eG", "fC")),
    },
    {
        "id": "I6",
        "left": ("000", "CGT", "TCG"),
        "right": ("0GG", "CC0", "T0T"),
        "sign": 1,
        "arms": ("aC", "aT", "bC", "bG", "cG", "cT"),
        "margin": (("fC",), ("fG", "fT")),
        "cross": (("dG", "eT", "fC"), ("dT", "eG")),
    },
)


def binomial_text(terms: tuple[tuple[str, ...], tuple[str, ...]]) -> str:
    positive, negative = terms
    return "*".join(positive) + "-" + "*".join(negative)


def serialize_polynomial(polynomial: Polynomial) -> list[dict]:
    records = []
    for monomial in sorted(polynomial):
        factors = []
        for name, exponent in zip(VARIABLE_ORDER, monomial):
            if exponent == 1:
                factors.append(name)
            elif exponent > 1:
                factors.append(f"{name}^{exponent}")
        records.append(
            {
                "coefficient": polynomial[monomial],
                "monomial": "*".join(factors) if factors else "1",
            }
        )
    return records


def circuit_record(spec: dict) -> dict:
    left = spec["left"]
    right = spec["right"]
    tree_pullback = circuit_pullback(tree_coordinate, left, right)
    if tree_pullback:
        raise AssertionError((spec["id"], "tree pullback is nonzero"))

    pullback = circuit_pullback(literal_sunlet_coordinate, left, right)
    margin = binomial(*spec["margin"])
    cross = binomial(*spec["cross"])
    positive_prefactor = product(
        (L, ONE_MINUS_L, *(variable(name) for name in spec["arms"]))
    )
    expected = scale(spec["sign"], product((positive_prefactor, margin, cross)))
    if pullback != expected:
        raise AssertionError((spec["id"], "literal-map factor mismatch"))

    prefactor_text = "L*(1-L)*" + "*".join(spec["arms"])
    margin_text = binomial_text(spec["margin"])
    cross_text = binomial_text(spec["cross"])
    sign_text = "-" if spec["sign"] < 0 else ""
    factor_text = f"{sign_text}{prefactor_text}*({margin_text})*({cross_text})"
    return {
        "id": spec["id"],
        "observable": (
            "*".join("q" + word for word in left)
            + "-"
            + "*".join("q" + word for word in right)
        ),
        "left": list(left),
        "right": list(right),
        "tree_pullback": "identically_zero",
        "literal_sunlet_factor": factor_text,
        "factor_sign": spec["sign"],
        "positive_prefactor": prefactor_text,
        "composition_margin": margin_text,
        "cross_factor": cross_text,
        "expanded_term_count": len(pullback),
        "expanded_pullback_sha256": hashlib.sha256(
            canonical_bytes({"terms": serialize_polynomial(pullback)})
        ).hexdigest(),
    }


def canonical_bytes(value: dict) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def build_certificate() -> dict:
    payload = {
        "schema": "k3p-tree-sunlet-literal-separator-v2",
        "claim": (
            "The six cubic circuits vanish on the three-leaf K3P tree and "
            "their squared sum is strictly positive on every strict ordinary "
            "three-sunlet in the stated literal edge convention."
        ),
        "character_group": {
            "name": "Z2xZ2",
            "characters": list(CHARACTERS),
            "coordinate_condition": "x+y+z=0",
        },
        "edge_order": list(EDGE_ORDER),
        "map_formula": "q_xyz=a_x*b_y*c_z*(L*f_y*d_z+(1-L)*f_x*e_z)",
        "tree_map_formula": "q_xyz=a_x*b_y*c_z",
        "parameter_domain": {
            "inheritance": "0<L<1",
            "nontrivial_edge_characters": "0<edge_h<1 for edge in {a,b,c,d,e,f} and h in {C,G,T}",
        },
        "observable_separator": "S=I1^2+I2^2+I3^2+I4^2+I5^2+I6^2",
        "circuits": [circuit_record(spec) for spec in SPECS],
        "strictness_argument": {
            "paired_cross_cancellations": [
                {
                    "circuits": ["I1", "I3"],
                    "composition_margin": "fC*fT-fG",
                    "identity": "cross_I1-fG*cross_I3=dC*eT*(1-fG^2)",
                    "forced_boundary_if_margin_nonzero_and_both_vanish": "fG^2=1",
                },
                {
                    "circuits": ["I2", "I4"],
                    "composition_margin": "fC*fG-fT",
                    "identity": "cross_I2-fT*cross_I4=dC*eG*(1-fT^2)",
                    "forced_boundary_if_margin_nonzero_and_both_vanish": "fT^2=1",
                },
                {
                    "circuits": ["I5", "I6"],
                    "composition_margin": "fC-fG*fT",
                    "identity": "cross_I5-fC*cross_I6=dG*eT*(1-fC^2)",
                    "forced_boundary_if_margin_nonzero_and_both_vanish": "fC^2=1",
                },
            ],
            "all_composition_margins_zero": {
                "equations": ["fC=fG*fT", "fG=fC*fT", "fT=fC*fG"],
                "product_identity": "p=p^2 for p=fC*fG*fT",
                "domain_contradiction": "0<p<1",
            },
            "conclusion": "At least one Ij is nonzero, so S>0.",
        },
        "generation": {
            "arithmetic": "exact sparse expansion over ZZ",
            "external_cas": False,
            "deterministic": True,
        },
    }
    payload["payload_sha256"] = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    if args.output and args.check:
        parser.error("--output and --check are mutually exclusive")

    certificate = build_certificate()
    rendered = json.dumps(certificate, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    if args.check:
        observed = json.loads(args.check.read_text())
        if observed != certificate:
            raise SystemExit("LITERAL_SEPARATOR_V2_GENERATION_MISMATCH")
        print("LITERAL_SEPARATOR_V2_GENERATION_PASS")
        print(f"payload_sha256={certificate['payload_sha256']}")
        return 0
    if args.output:
        args.output.write_text(rendered)
        print("LITERAL_SEPARATOR_V2_GENERATED")
        print(f"output={args.output}")
        print(f"payload_sha256={certificate['payload_sha256']}")
        return 0
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
