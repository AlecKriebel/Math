#!/usr/bin/env python3
"""Standalone exact audit of the frozen JC cut certificate and K3P transfer.

This program deliberately imports neither the historical producer nor either
historical reviewer.  It uses only Python's standard library, the byte-locked
certificate in ``upstream_frozen/``, and literal group/algebra definitions.

The audit has three logically separate outputs:

1. exact internal replay of all frozen JC sign certificates;
2. verification of the K3P -> CFN identity on the order-two subgroup H;
3. a scope test deciding whether that identity proves the claimed K3P cut
   theorem.  The scope test includes an exact CFN two-endpoint rank-drop
   witness reconstructed from a literal descendant-mask type in the frozen
   certificate.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb, prod
from pathlib import Path
from typing import Iterable


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "upstream_frozen" / "pointwise_cut_certificate.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "b627df5b2dc8cf1eb21c2e08c974f9e54f5a0399043e4dd96ea95dc73c2c3350"
)
EXPECTED_CERTIFICATE_BYTES = 3_077_509


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def as_fraction(value: object) -> Fraction:
    return Fraction(str(value))


Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Fraction]


@dataclass
class SparseRing:
    """Small exact sparse polynomial ring with a fail-closed AST parser."""

    names: tuple[str, ...]

    def __post_init__(self) -> None:
        self.index = {name: position for position, name in enumerate(self.names)}
        assert len(self.index) == len(self.names)
        self.zero_exponent = (0,) * len(self.names)
        self.parse_cache: dict[str, Polynomial] = {}

    def scalar(self, value: Fraction | int) -> Polynomial:
        coefficient = Fraction(value)
        return {} if coefficient == 0 else {self.zero_exponent: coefficient}

    def generator(self, name: str) -> Polynomial:
        exponent = [0] * len(self.names)
        exponent[self.index[name]] = 1
        return {tuple(exponent): Fraction(1)}

    @staticmethod
    def cleaned(polynomial: Polynomial) -> Polynomial:
        return {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}

    def add(self, left: Polynomial, right: Polynomial) -> Polynomial:
        result = dict(left)
        for monomial, coefficient in right.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
            if result[monomial] == 0:
                del result[monomial]
        return result

    @staticmethod
    def neg(polynomial: Polynomial) -> Polynomial:
        return {monomial: -coefficient for monomial, coefficient in polynomial.items()}

    def sub(self, left: Polynomial, right: Polynomial) -> Polynomial:
        return self.add(left, self.neg(right))

    def mul(self, left: Polynomial, right: Polynomial) -> Polynomial:
        if not left or not right:
            return {}
        if len(left) > len(right):
            left, right = right, left
        result: Polynomial = {}
        for left_monomial, left_coefficient in left.items():
            for right_monomial, right_coefficient in right.items():
                monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
                result[monomial] = (
                    result.get(monomial, Fraction(0)) + left_coefficient * right_coefficient
                )
        return self.cleaned(result)

    def power(self, base: Polynomial, exponent: int) -> Polynomial:
        assert exponent >= 0
        result = self.scalar(1)
        while exponent:
            if exponent & 1:
                result = self.mul(result, base)
            exponent >>= 1
            if exponent:
                base = self.mul(base, base)
        return result

    def divide_by_scalar(self, numerator: Polynomial, denominator: Polynomial) -> Polynomial:
        assert set(denominator) == {self.zero_exponent}
        scalar = denominator[self.zero_exponent]
        assert scalar != 0
        return {monomial: coefficient / scalar for monomial, coefficient in numerator.items()}

    def parse(self, expression: str) -> Polynomial:
        if expression in self.parse_cache:
            return self.parse_cache[expression]
        syntax = ast.parse(expression, mode="eval")

        def visit(node: ast.AST) -> Polynomial:
            if isinstance(node, ast.Expression):
                return visit(node.body)
            if isinstance(node, ast.Constant):
                assert isinstance(node.value, int) and not isinstance(node.value, bool)
                return self.scalar(node.value)
            if isinstance(node, ast.Name):
                assert node.id in self.index
                return self.generator(node.id)
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
                return self.neg(visit(node.operand))
            if isinstance(node, ast.BinOp):
                if isinstance(node.op, ast.Add):
                    return self.add(visit(node.left), visit(node.right))
                if isinstance(node.op, ast.Sub):
                    return self.sub(visit(node.left), visit(node.right))
                if isinstance(node.op, ast.Mult):
                    return self.mul(visit(node.left), visit(node.right))
                if isinstance(node.op, ast.Div):
                    return self.divide_by_scalar(visit(node.left), visit(node.right))
                if isinstance(node.op, ast.Pow):
                    assert isinstance(node.right, ast.Constant)
                    assert isinstance(node.right.value, int) and node.right.value >= 0
                    return self.power(visit(node.left), node.right.value)
            raise AssertionError(f"unsupported expression node: {ast.dump(node)}")

        result = self.cleaned(visit(syntax))
        self.parse_cache[expression] = result
        return result


EDGE_RING = SparseRing(tuple(f"x{index}" for index in range(15)))
BERNSTEIN_CACHE: dict[
    tuple[str, tuple[str, ...], tuple[int, ...]], tuple[Fraction, ...]
] = {}


def bernstein_coefficients(
    expression: str, active_names: tuple[str, ...], degrees: tuple[int, ...]
) -> tuple[Fraction, ...]:
    key = (expression, active_names, degrees)
    if key in BERNSTEIN_CACHE:
        return BERNSTEIN_CACHE[key]
    assert len(active_names) == len(degrees)
    assert len(set(active_names)) == len(active_names)
    polynomial = EDGE_RING.parse(expression)
    active_indices = tuple(EDGE_RING.index[name] for name in active_names)
    inactive_indices = set(range(len(EDGE_RING.names))) - set(active_indices)
    power_terms: dict[tuple[int, ...], Fraction] = {}
    for monomial, coefficient in polynomial.items():
        assert all(monomial[index] == 0 for index in inactive_indices)
        powers = tuple(monomial[index] for index in active_indices)
        assert all(power <= degree for power, degree in zip(powers, degrees))
        power_terms[powers] = power_terms.get(powers, Fraction(0)) + coefficient

    result: list[Fraction] = []
    for beta in product(*(range(degree + 1) for degree in degrees)):
        value = Fraction(0)
        for alpha, coefficient in power_terms.items():
            if not all(a <= b for a, b in zip(alpha, beta)):
                continue
            multiplier = Fraction(1)
            for degree, b, a in zip(degrees, beta, alpha):
                multiplier *= Fraction(comb(b, a), comb(degree, a))
            value += multiplier * coefficient
        result.append(value)
    answer = tuple(result)
    BERNSTEIN_CACHE[key] = answer
    return answer


def partial_bernstein_coefficients(
    expression: str, active_names: tuple[str, ...], degrees: tuple[int, ...]
) -> dict[tuple[int, ...], Polynomial]:
    """Bernstein coefficients in selected variables, polynomial in the rest."""

    polynomial = EDGE_RING.parse(expression)
    active_indices = tuple(EDGE_RING.index[name] for name in active_names)
    answer: dict[tuple[int, ...], Polynomial] = {}
    for beta in product(*(range(degree + 1) for degree in degrees)):
        coefficient_polynomial: Polynomial = {}
        for monomial, coefficient in polynomial.items():
            alpha = tuple(monomial[index] for index in active_indices)
            assert all(power <= degree for power, degree in zip(alpha, degrees))
            if not all(a <= b for a, b in zip(alpha, beta)):
                continue
            multiplier = Fraction(1)
            for degree, b, a in zip(degrees, beta, alpha):
                multiplier *= Fraction(comb(b, a), comb(degree, a))
            reduced = list(monomial)
            for index in active_indices:
                reduced[index] = 0
            reduced_monomial = tuple(reduced)
            coefficient_polynomial[reduced_monomial] = (
                coefficient_polynomial.get(reduced_monomial, Fraction(0))
                + multiplier * coefficient
            )
        answer[beta] = EDGE_RING.cleaned(coefficient_polynomial)
    return answer


def coefficient_sign(values: Iterable[Fraction]) -> tuple[int | None, bool]:
    values = tuple(values)
    positive = sum(value > 0 for value in values)
    negative = sum(value < 0 for value in values)
    if negative == 0 and positive > 0:
        return 1, True
    if positive == 0 and negative > 0:
        return -1, True
    return None, False


def verify_factor(factor: dict, nested: bool) -> tuple[int, bool]:
    active = tuple(factor["active"])
    exponent = int(factor["exponent"])
    assert exponent > 0
    metadata = factor["bernstein"] if nested else factor
    degrees = tuple(int(value) for value in metadata["degrees"])
    coefficients = bernstein_coefficients(factor["factor"], active, degrees)
    observed = {
        "negative": sum(value < 0 for value in coefficients),
        "positive": sum(value > 0 for value in coefficients),
        "zero": sum(value == 0 for value in coefficients),
        "min": min(coefficients),
        "max": max(coefficients),
    }
    assert observed["negative"] == int(metadata["negative"])
    assert observed["positive"] == int(metadata["positive"])
    assert observed["zero"] == int(metadata["zero"] if nested else metadata["zero_count"])
    assert observed["min"] == as_fraction(metadata["min"])
    assert observed["max"] == as_fraction(metadata["max"])
    if not nested:
        assert int(metadata["count"]) == prod(degree + 1 for degree in degrees)

    raw_sign, strict = coefficient_sign(coefficients)
    recorded_sign = int(factor["factor_sign"] if nested else factor["sign"])
    if raw_sign is None:
        assert nested and exponent % 2 == 0 and recorded_sign == 1
        contribution = 1
    else:
        assert raw_sign == recorded_sign
        contribution = raw_sign**exponent
    if nested:
        assert bool(factor["strict_on_open_cube"]) == strict
    return contribution, strict


FACTORIZATION_CACHE: dict[str, tuple[int, bool]] = {}


def verify_factorization(record: dict, nested: bool = False) -> tuple[int, bool]:
    cache_key = json.dumps(
        {"nested": nested, "record": record}, sort_keys=True, separators=(",", ":")
    )
    if cache_key in FACTORIZATION_CACHE:
        return FACTORIZATION_CACHE[cache_key]
    assert record["zero"] is False
    expression = EDGE_RING.parse(record["expression"])
    scalar = as_fraction(record["coefficient"])
    assert scalar != 0
    reconstructed = EDGE_RING.scalar(scalar)
    total_sign = 1 if scalar > 0 else -1
    all_factors_strict = True
    for factor in record["factors"]:
        contribution, strict = verify_factor(factor, nested=nested)
        reconstructed = EDGE_RING.mul(
            reconstructed,
            EDGE_RING.power(EDGE_RING.parse(factor["factor"]), int(factor["exponent"])),
        )
        total_sign *= contribution
        all_factors_strict &= strict
    assert reconstructed == expression
    if nested:
        assert total_sign == int(record["weak_sign"])
        assert all_factors_strict == bool(record["strict"])
    else:
        assert total_sign == int(record["total_sign"])
    result = (total_sign, all_factors_strict)
    FACTORIZATION_CACHE[cache_key] = result
    return result


SIGN_CACHE: dict[str, int] = {}


def verify_sign_certificate(record: dict) -> int:
    cache_key = json.dumps(record, sort_keys=True, separators=(",", ":"))
    if cache_key in SIGN_CACHE:
        return SIGN_CACHE[cache_key]
    if "partial_certificate" not in record:
        sign, _ = verify_factorization(record)
        SIGN_CACHE[cache_key] = sign
        return sign

    assert record["zero"] is False
    partial = record["partial_certificate"]
    active = tuple(partial["inheritance_variables"])
    degrees = tuple(int(value) for value in partial["degrees"])
    computed = partial_bernstein_coefficients(record["expression"], active, degrees)
    stored = {tuple(int(i) for i in row["index"]): row for row in partial["coefficients"]}
    assert set(stored) == set(computed)
    assert len(computed) == int(partial["coefficient_count"])
    assert len(computed) == prod(degree + 1 for degree in degrees)
    nonzero_count = 0
    strict_count = 0
    total_sign = int(partial["total_sign"])
    assert total_sign in (-1, 1)
    for index, polynomial in computed.items():
        row = stored[index]
        if not polynomial:
            assert row["zero"] is True
            continue
        nonzero_count += 1
        assert row["zero"] is False
        nested_record = row["coefficient_certificate"]
        assert polynomial == EDGE_RING.parse(nested_record["expression"])
        sign, strict = verify_factorization(nested_record, nested=True)
        assert sign == total_sign
        strict_count += int(strict)
    assert nonzero_count == int(partial["nonzero_count"])
    assert bool(strict_count) == bool(partial["at_least_one_coefficient_strict"])
    assert int(record["total_sign"]) == total_sign
    SIGN_CACHE[cache_key] = total_sign
    return total_sign


def parse_tensor_type(text: str, boundary_count: int) -> tuple[tuple[int, ...], ...]:
    tensor = ast.literal_eval(text)
    assert isinstance(tensor, tuple) and tensor
    assert tuple(sorted(tensor)) == tensor
    switching_count = len(tensor[0])
    assert switching_count in (2, 4)
    for signature in tensor:
        assert isinstance(signature, tuple) and len(signature) == switching_count
        assert all(isinstance(mask, int) and 0 <= mask < (1 << boundary_count) for mask in signature)
    return tensor


def verify_jc_certificate(data: dict) -> dict:
    assert data["status"] == "PROVED"
    endpoints = data["endpoint_records"]
    singles = data["single_blob_records"]
    assert len(endpoints) == int(data["endpoint_type_count"]) == 177
    assert len(singles) == int(data["single_blob_type_count"]) == 453
    assert len({row["type_key"] for row in endpoints}) == len(endpoints)
    assert len({row["type_key"] for row in singles}) == len(singles)

    endpoint_branches: Counter[str] = Counter()
    endpoint_origins: Counter[str] = Counter()
    ordinary_signs = 0
    partial_signs = 0
    for row in endpoints:
        parse_tensor_type(row["type_key"], boundary_count=3)
        assert isinstance(row["origins"], list) and len(row["origins"]) == 1
        endpoint_origins.update(row["origins"])
        certificate = row["certificate"]
        branch = certificate["branch"]
        endpoint_branches[branch] += 1
        if branch == "F_positive":
            sign_record = certificate["F"]
            assert sign_record["zero"] is False
            assert verify_sign_certificate(sign_record) == 1
        else:
            assert branch == "F_zero_G_positive"
            assert certificate["F"] == {"expression": "0", "zero": True}
            sign_record = certificate["G"]
            assert sign_record["zero"] is False
            assert verify_sign_certificate(sign_record) == 1
        partial_signs += int("partial_certificate" in sign_record)
        ordinary_signs += int("partial_certificate" not in sign_record)

    expected_endpoint_branches = {"F_positive": 151, "F_zero_G_positive": 26}
    assert dict(endpoint_branches) == data["endpoint_dichotomy"] == expected_endpoint_branches
    assert dict(endpoint_origins) == data["endpoint_origin_type_counts"]

    single_classes: Counter[str] = Counter()
    single_origins: Counter[str] = Counter()
    true_bridge_types = 0
    for row in singles:
        tensor = parse_tensor_type(row["type_key"], boundary_count=4)
        assert isinstance(row["origins"], list) and len(row["origins"]) == 1
        single_origins.update(row["origins"])
        certificate = row["certificate"]
        classification = certificate["classification"]
        single_classes[classification] += 1
        if classification == "wrong_split_strict":
            assert certificate["displayed_bridge"] is False
            sign_record = certificate["sign"]
            assert sign_record["zero"] is False
            assert verify_sign_certificate(sign_record) in (-1, 1)
            partial_signs += int("partial_certificate" in sign_record)
            ordinary_signs += int("partial_certificate" not in sign_record)
        else:
            assert classification == "rank_one_all_blocks"
            assert certificate["displayed_bridge"] is True
            # Masks 0011 and 1100 are the two sides of the tested 12|34 split.
            assert any(len(set(signature)) == 1 and signature[0] in (3, 12) for signature in tensor)
            true_bridge_types += 1

    expected_single_classes = {"wrong_split_strict": 421, "rank_one_all_blocks": 32}
    assert dict(single_classes) == data["single_blob_classification"] == expected_single_classes
    assert dict(single_origins) == data["single_blob_origin_type_counts"]
    assert true_bridge_types == 32
    assert ordinary_signs == 591 and partial_signs == 7
    assert len(BERNSTEIN_CACHE) == 547

    return {
        "status": "PASS_INTERNAL_EXACT_REPLAY",
        "endpoint_types": len(endpoints),
        "endpoint_dichotomy": dict(endpoint_branches),
        "endpoint_origin_type_counts": dict(endpoint_origins),
        "single_blob_types": len(singles),
        "single_blob_classification": dict(single_classes),
        "single_blob_origin_type_counts": dict(single_origins),
        "strict_wrong_split_signs": single_classes["wrong_split_strict"],
        "true_bridge_signatures": true_bridge_types,
        "ordinary_factored_sign_records": ordinary_signs,
        "partial_Bernstein_sign_records": partial_signs,
        "distinct_factor_Bernstein_expansions": len(BERNSTEIN_CACHE),
        "scope": "certificate algebra/type-key consistency; not primitive graph-universe regeneration",
    }


def verify_jc_two_active_identities(data: dict) -> dict:
    names = ("a", "b", "c", "t", "A", "B", "C", "T", "z")
    ring = SparseRing(names)
    stored = data["two_active_endpoint_case"]["decisive_minors"]
    expected = {
        "m0": "a*A-b*c*B*C*z**2",
        "m1": "(a*A-T*t*z)*(a*A+T*t*z)",
        "m2": "a*A**2-b*c*T**2*z**2",
        "m3": "a**2*A-t**2*B*C*z**2",
    }
    for name, expression in expected.items():
        assert ring.parse(stored[name]) == ring.parse(expression)
    m0 = ring.parse(expected["m0"])
    m2 = ring.parse(expected["m2"])
    m3 = ring.parse(expected["m3"])
    identity_left = ring.sub(m2, ring.mul(ring.parse("A"), m0))
    identity_right = ring.parse("b*c*z**2*(A*B*C-T**2)")
    assert identity_left == identity_right
    identity_left = ring.sub(m3, ring.mul(ring.parse("a"), m0))
    identity_right = ring.parse("B*C*z**2*(a*b*c-t**2)")
    assert identity_left == identity_right
    assert data["two_active_endpoint_case"]["derived_rank_one_equations"] == [
        "a*b*c=t**2",
        "A*B*C=T**2",
        "a*A=b*c*B*C*z**2",
    ]
    return {
        "status": "PASS_JC_IDENTITIES",
        "minors_checked": 4,
        "elimination_identities_checked": 2,
        "logical_use": (
            "m0=m2=m3=0 forces both JC endpoint Delta equations; the frozen "
            "endpoint dichotomy then supplies Gamma>0 and contradicts 0<z<1"
        ),
    }


def verify_order_two_projection_identity() -> dict:
    """Verify exactly the identity on H and identify its strict scope."""

    zero = (0, 0)
    C = (1, 0)
    G = (0, 1)
    T = (1, 1)

    def group_add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
        return (left[0] ^ right[0], left[1] ^ right[1])

    embed = {0: zero, 1: C}
    for left, right in product((0, 1), repeat=2):
        assert group_add(embed[left], embed[right]) == embed[left ^ right]
    H = {zero, C}
    assert {group_add(left, right) for left in H for right in H} == H
    k3p_multiplier = {zero: "1", C: "c_e", G: "g_e", T: "t_e"}
    cfn_multiplier = {0: "1", 1: "c_e"}
    for bit in (0, 1):
        assert k3p_multiplier[embed[bit]] == cfn_multiplier[bit]

    # For every descendant set, summing H-supported leaf characters is the
    # embedded parity.  The two-element homomorphism check above proves this
    # for arbitrary set size by induction, hence proves equality of every
    # displayed-tree monomial and every inheritance mixture on H-coordinates.

    # The projection of D_{3,+} onto c is the full interval (0,1): for any
    # c in (0,1), choosing g=t=1/2 gives margins c, 1-c, 1-c.
    domain_extension_margins = ["c", "1-c", "1-c"]

    # Scope check: the JC endpoint Delta uses P(C,G,T).  That coordinate is
    # outside H and, already on a three-edge star, its K3P edge monomial is
    # c_1*g_2*t_3 rather than a c-only monomial.  Thus the H identity cannot
    # transport Delta=abc-t^2 or the t/T-containing minors m1--m3.
    all_distinct_pattern = (C, G, T)
    assert any(character not in H for character in all_distinct_pattern)
    star_k3p_monomial = "c_1*g_2*t_3"
    star_jc_monomial = "x_1*x_2*x_3"
    assert star_k3p_monomial != star_jc_monomial.replace("x", "c")

    return {
        "status": "PASS_WITH_STRICT_SCOPE",
        "subgroup": {"0": list(zero), "C": list(C)},
        "homomorphism_table_checked": 4,
        "edge_multiplier_identity": {"0": "1", "C": "c_e"},
        "displayed_tree_and_network_map_identity_on_H": True,
        "D3_plus_projection_onto_c": "(0,1)",
        "D3_plus_extension_choice": "g=t=1/2",
        "D3_plus_extension_margins": domain_extension_margins,
        "identity_scope": "Fourier coordinates whose every leaf character lies in H={0,C}",
        "JC_all_distinct_coordinate": "P(C,G,T)",
        "JC_all_distinct_coordinate_lies_in_H": False,
        "three_edge_star_K3P_monomial": star_k3p_monomial,
        "three_edge_star_JC_monomial": star_jc_monomial,
        "transports_JC_Delta_or_m1_m2_m3": False,
    }


CFN_WITNESS_TYPE = (
    (0, 0, 0, 4),
    (0, 0, 4, 0),
    (0, 0, 4, 4),
    (1, 1, 1, 1),
    (1, 1, 1, 5),
    (1, 1, 5, 5),
    (2, 2, 2, 2),
    (4, 4, 0, 0),
    (4, 4, 4, 4),
    (5, 5, 5, 5),
)
CFN_NORMALIZED_EDGE_PARAMETERS = (
    Fraction(3, 4),
    Fraction(9, 10),
    Fraction(2, 3),
    Fraction(1, 3),
    Fraction(3, 4),
    Fraction(1, 10),
    Fraction(1, 2),
    Fraction(5, 6),
    Fraction(1),  # normalized complete central singleton-signature class
    Fraction(1, 2),
)
CFN_INHERITANCE_PARAMETERS = (Fraction(1, 6), Fraction(1, 2))


def switching_weights(deltas: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    result = []
    for switching in range(1 << len(deltas)):
        weight = Fraction(1)
        for bit, delta in enumerate(deltas):
            weight *= delta if switching & (1 << bit) else 1 - delta
        result.append(weight)
    assert sum(result) == 1
    return tuple(result)


def cfn_endpoint_coordinate(
    tensor: tuple[tuple[int, ...], ...],
    edge_parameters: tuple[Fraction, ...],
    inheritance_parameters: tuple[Fraction, ...],
    boundary_pattern: int,
) -> Fraction:
    assert len(tensor) == len(edge_parameters)
    weights = switching_weights(inheritance_parameters)
    assert len(weights) == len(tensor[0])
    total = Fraction(0)
    for switching, weight in enumerate(weights):
        monomial = Fraction(1)
        for signature, edge_parameter in zip(tensor, edge_parameters):
            descendant_mask = signature[switching]
            if (descendant_mask & boundary_pattern).bit_count() % 2:
                monomial *= edge_parameter
        total += weight * monomial
    return total


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    rank = 0
    for column in range(columns):
        pivot = next((row for row in range(rank, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(rows):
            if row == rank or work[row][column] == 0:
                continue
            multiplier = work[row][column]
            work[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def verify_cfn_projection_counterexample(data: dict) -> dict:
    matching = [
        row for row in data["endpoint_records"] if ast.literal_eval(row["type_key"]) == CFN_WITNESS_TYPE
    ]
    assert len(matching) == 1
    record = matching[0]
    assert record["origins"] == ["theta_incoming_active"]
    assert record["certificate"]["branch"] == "F_positive"
    assert all(Fraction(0) < value < Fraction(1) for i, value in enumerate(CFN_NORMALIZED_EDGE_PARAMETERS) if i != 8)
    assert CFN_NORMALIZED_EDGE_PARAMETERS[8] == 1
    assert CFN_WITNESS_TYPE[8] == (4, 4, 4, 4)
    assert all(Fraction(0) < value < Fraction(1) for value in CFN_INHERITANCE_PARAMETERS)

    # JC notation: a=P(C,C,0), b=P(C,0,C), c=P(0,C,C).
    a = cfn_endpoint_coordinate(
        CFN_WITNESS_TYPE,
        CFN_NORMALIZED_EDGE_PARAMETERS,
        CFN_INHERITANCE_PARAMETERS,
        0b011,
    )
    b = cfn_endpoint_coordinate(
        CFN_WITNESS_TYPE,
        CFN_NORMALIZED_EDGE_PARAMETERS,
        CFN_INHERITANCE_PARAMETERS,
        0b101,
    )
    c = cfn_endpoint_coordinate(
        CFN_WITNESS_TYPE,
        CFN_NORMALIZED_EDGE_PARAMETERS,
        CFN_INHERITANCE_PARAMETERS,
        0b110,
    )
    gamma = a - b * c
    assert (a, b, c) == (Fraction(1, 160), Fraction(25, 288), Fraction(427, 3840))
    assert gamma == Fraction(-3763, 1_105_920) < 0

    # Join two copies of this normalized endpoint.  Taking z=a/(bc) makes
    # both CFN wrong-split block determinants vanish.  It is strict because
    # Gamma<0 implies 0<z<1.
    z = a / (b * c)
    assert z == Fraction(6912, 10675) and 0 < z < 1
    physical_endpoint_central_scale = Fraction(9, 10)
    physical_bridge_scale = z / physical_endpoint_central_scale**2
    assert physical_bridge_scale == Fraction(1024, 1281)
    assert 0 < physical_bridge_scale < 1

    physical_edge_parameters = list(CFN_NORMALIZED_EDGE_PARAMETERS)
    physical_edge_parameters[8] = physical_endpoint_central_scale
    physical_a = cfn_endpoint_coordinate(
        CFN_WITNESS_TYPE,
        tuple(physical_edge_parameters),
        CFN_INHERITANCE_PARAMETERS,
        0b011,
    )
    physical_b = cfn_endpoint_coordinate(
        CFN_WITNESS_TYPE,
        tuple(physical_edge_parameters),
        CFN_INHERITANCE_PARAMETERS,
        0b101,
    )
    physical_c = cfn_endpoint_coordinate(
        CFN_WITNESS_TYPE,
        tuple(physical_edge_parameters),
        CFN_INHERITANCE_PARAMETERS,
        0b110,
    )
    assert (physical_a, physical_b, physical_c) == (
        a,
        physical_endpoint_central_scale * b,
        physical_endpoint_central_scale * c,
    )

    endpoint = {
        (0, 0, 0): Fraction(1),
        (1, 1, 0): a,
        (1, 0, 1): b,
        (0, 1, 1): c,
    }
    pairs = tuple(product((0, 1), repeat=2))
    flattening: list[list[Fraction]] = []
    for g1, g3 in pairs:
        row = []
        for g2, g4 in pairs:
            h = g1 ^ g2
            if h != (g3 ^ g4):
                row.append(Fraction(0))
            else:
                row.append(
                    endpoint[(g1, g2, h)]
                    * (z if h else 1)
                    * endpoint[(g3, g4, h)]
                )
        flattening.append(row)

    block_determinants = []
    for total in (0, 1):
        indices = [index for index, pair in enumerate(pairs) if pair[0] ^ pair[1] == total]
        assert len(indices) == 2
        determinant = (
            flattening[indices[0]][indices[0]] * flattening[indices[1]][indices[1]]
            - flattening[indices[0]][indices[1]] * flattening[indices[1]][indices[0]]
        )
        block_determinants.append(determinant)
    assert block_determinants == [0, 0]
    rank = matrix_rank(flattening)
    assert rank == 2

    # Recompute from strictly physical endpoints and the actual central bridge;
    # this must equal the normalized contraction entry by entry.
    physical_endpoint = {
        (0, 0, 0): Fraction(1),
        (1, 1, 0): physical_a,
        (1, 0, 1): physical_b,
        (0, 1, 1): physical_c,
    }
    physical_flattening: list[list[Fraction]] = []
    for g1, g3 in pairs:
        row = []
        for g2, g4 in pairs:
            h = g1 ^ g2
            if h != (g3 ^ g4):
                row.append(Fraction(0))
            else:
                row.append(
                    physical_endpoint[(g1, g2, h)]
                    * (physical_bridge_scale if h else 1)
                    * physical_endpoint[(g3, g4, h)]
                )
        physical_flattening.append(row)
    assert physical_flattening == flattening

    return {
        "status": "EXACT_COUNTEREXAMPLE_TO_CFN_POINTWISE_NONCUT_RANK_CLAIM",
        "frozen_endpoint_type_key": record["type_key"],
        "frozen_endpoint_origin": record["origins"][0],
        "frozen_JC_branch": record["certificate"]["branch"],
        "inheritance_parameters": [str(value) for value in CFN_INHERITANCE_PARAMETERS],
        "normalized_edge_parameters_in_type_key_order": [
            str(value) for value in CFN_NORMALIZED_EDGE_PARAMETERS
        ],
        "normalized_central_signature": "(4,4,4,4)",
        "endpoint_coordinates": {"a": str(a), "b": str(b), "c": str(c)},
        "Gamma=a-bc": str(gamma),
        "effective_bridge_z": str(z),
        "physical_endpoint_central_scale_each_side": str(physical_endpoint_central_scale),
        "physical_bridge_scale": str(physical_bridge_scale),
        "strict_physical_contraction_equals_normalized_contraction": True,
        "all_physical_parameters_strict_open_cube": True,
        "wrong_split_block_determinants": [str(value) for value in block_determinants],
        "wrong_split_CFN_Fourier_flattening": [
            [str(value) for value in row] for row in flattening
        ],
        "wrong_split_CFN_flattening_rank": rank,
        "true_cut_CFN_rank_threshold": 2,
        "consequence": (
            "The H={0,C} projection can have cut-threshold rank at a noncut "
            "two-active crossing, so it cannot supply the claimed K3P rank>=5 lower bound."
        ),
    }


def build_report() -> dict:
    assert CERTIFICATE.is_file()
    observed_hash = sha256_file(CERTIFICATE)
    assert observed_hash == EXPECTED_CERTIFICATE_SHA256
    assert CERTIFICATE.stat().st_size == EXPECTED_CERTIFICATE_BYTES
    data = json.loads(CERTIFICATE.read_text())
    jc_replay = verify_jc_certificate(data)
    jc_identities = verify_jc_two_active_identities(data)
    projection = verify_order_two_projection_identity()
    cfn_counterexample = verify_cfn_projection_counterexample(data)
    return {
        "schema": "k3p-cut-recovery-independent-audit-v2",
        "upstream_frozen_dependency": {
            "path": str(CERTIFICATE.relative_to(HERE)),
            "sha256": observed_hash,
            "bytes": CERTIFICATE.stat().st_size,
            "status": "FOUND_AND_BYTE_LOCKED",
        },
        "frozen_JC_certificate_replay": jc_replay,
        "frozen_JC_two_active_algebra": jc_identities,
        "K3P_order_two_projection": projection,
        "CFN_scope_falsification": cfn_counterexample,
        "transfer_audit": {
            "claimed_transfer": (
                "All frozen JC cut polynomials become c-only K3P polynomials on H={0,C}."
            ),
            "status": "FAIL",
            "reason": (
                "The H-coordinate identity is exact but the JC endpoint certificate uses "
                "P(C,G,T), and its two-active proof needs m1--m3. Those coordinates are "
                "outside H. The literal CFN rank-drop witness independently shows that "
                "the H projection alone does not prove the noncut lower bound."
            ),
        },
        "K3P_pointwise_cut_theorem": {
            "theorem_disproved_by_this_audit": False,
            "supplied_proof_certified": False,
            "status": "BLOCKED",
            "exact_remaining_gap": (
                "A K3P-specific proof/certificate controlling the G and T character "
                "blocks at two-active crossings, or an exact strict K3P counterexample."
            ),
        },
        "primary_item_6": {
            "claim": "Pointwise K3P cut recovery on D_{3,+}",
            "status": "BLOCKED",
            "can_honestly_pass": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--report",
        type=Path,
        help="Optional deterministic JSON output path (must remain inside cut_recovery).",
    )
    parser.add_argument(
        "--require-primary-pass",
        action="store_true",
        help="Exit nonzero unless primary item 6 passes (expected to fail for this audit).",
    )
    arguments = parser.parse_args()
    report = build_report()
    if arguments.report is not None:
        output = arguments.report.resolve()
        output.relative_to(HERE)
        output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    print("CUT_RECOVERY_INDEPENDENT_AUDIT_COMPLETE")
    print("PRIMARY_ITEM_6_BLOCKED")
    if arguments.require_primary_pass and not report["primary_item_6"]["can_honestly_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
