#!/usr/bin/env python3
"""Clean-room exact audit of pointwise JC cut preservation.

No historical Python module is imported.  The five orientation-core encodings,
the submitted three-port edge-mask deck, and the proposed certificate JSON are
read only as untrusted data.
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import sympy as sp

from audit_cut_switching import audit as audit_cut_switching
from exact_poly import (
    ExpressionParser,
    Polynomial,
    bernstein_decomposition,
    strict_bernstein_sign,
    text_sha256,
)
from tensor_models import (
    TREE_TENSOR,
    Tensor,
    enumerate_nonroot_tensors,
    enumerate_root_tensors,
    load_cores,
    three_port_structural_variants,
)


DEFAULT_PROJECT = Path(
    "/Users/alec/Documents/Math/strong_level2_phylo_identifiability"
)

THREE_ASSIGNMENTS = {
    "a": (1, 1, 0),
    "b": (1, 0, 1),
    "c": (0, 1, 1),
    "t": (1, 2, 3),
}


def file_hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def xor_on_mask(assignment: Sequence[int], mask: int) -> int:
    value = 0
    for position, character in enumerate(assignment):
        if mask & (1 << position):
            value ^= character
    return value


def tensor_coordinates(
    signatures: Tensor, reticulations: int, names: Sequence[str]
) -> dict[str, Polynomial]:
    edge_count = len(signatures)
    if len(names) != edge_count + reticulations:
        raise ValueError("parameter-name count does not fit tensor")
    width = 1 << reticulations
    if any(len(row) != width for row in signatures):
        raise ValueError("tensor choice width does not fit reticulation count")
    variables = [Polynomial.variable(len(names), index) for index in range(len(names))]
    edges = variables[:edge_count]
    inheritances = variables[edge_count:]
    choices = tuple(itertools.product((0, 1), repeat=reticulations))
    result: dict[str, Polynomial] = {}
    for coordinate, assignment in THREE_ASSIGNMENTS.items():
        total = Polynomial.constant(len(names), 0)
        for choice_index, choice in enumerate(choices):
            term = Polynomial.constant(len(names), 1)
            for bit, inheritance in zip(choice, inheritances):
                term *= inheritance if bit == 0 else 1 - inheritance
            for edge, row in zip(edges, signatures):
                if xor_on_mask(assignment, row[choice_index]):
                    term *= edge
            total += term
        result[coordinate] = total
    return result


def verify_expression_factor_certificate(
    target: Polynomial,
    certificate: Mapping[str, object],
    names: Sequence[str],
) -> dict[str, object]:
    parser = ExpressionParser(names)
    constant = Fraction(str(certificate["constant"]))
    product = Polynomial.constant(len(names), constant)
    sign = 1 if constant > 0 else -1
    total_coefficients = 0
    maximum_coefficients = 0
    for row in certificate["factors"]:
        expression = str(row["factor"])
        if text_sha256(expression) != row["factor_sha256"]:
            raise AssertionError("factor text hash mismatch")
        factor = parser.parse(expression)
        exponent = int(row["exponent"])
        product *= factor ** exponent
        nested = row["certificate"]
        variable_names = tuple(str(name) for name in nested.get("variables", ()))
        indices = tuple(names.index(name) for name in variable_names)
        factor_sign, metadata = strict_bernstein_sign(factor, indices)
        total_coefficients += int(metadata["coefficient_count"])
        maximum_coefficients = max(
            maximum_coefficients, int(metadata["coefficient_count"])
        )
        if factor_sign != int(row["factor_strict_sign"]):
            raise AssertionError("factor sign does not match exact Bernstein replay")
        for key, nested_key in (
            ("degrees", "degrees"),
            ("coefficient_count", "coefficient_count"),
            ("minimum", "minimum"),
            ("maximum", "maximum"),
        ):
            if nested.get(nested_key) is not None and metadata[key] != nested[nested_key]:
                raise AssertionError(f"factor Bernstein {key} mismatch")
        if exponent % 2:
            if factor_sign not in {-1, 1}:
                raise AssertionError("odd factor lacks a strict sign")
            sign *= factor_sign
    if product != target:
        raise AssertionError("factor product does not equal reconstructed polynomial")
    if parser.variable_denominators:
        raise AssertionError("certificate used a nonconstant denominator")
    if certificate.get("strict_sign") is not None and sign != int(certificate["strict_sign"]):
        raise AssertionError("product strict sign mismatch")
    return {
        "strict_sign": sign,
        "factor_count": len(certificate["factors"]),
        "total_bernstein_coefficients": total_coefficients,
        "maximum_factor_bernstein_coefficients": maximum_coefficients,
    }


WORK_NAME = re.compile(r"cross3_t(?P<tensor>\d+)_p(?P<parameter>\d+)")


def normalize_work_expression(
    expression: str, tensor_id: int, edge_count: int
) -> str:
    def replacement(match: re.Match[str]) -> str:
        if int(match.group("tensor")) != tensor_id:
            raise ValueError("inheritance certificate refers to another tensor")
        parameter = int(match.group("parameter"))
        return f"x{parameter}" if parameter < edge_count else f"l{parameter - edge_count}"

    return WORK_NAME.sub(replacement, expression)


def verify_inheritance_bernstein_certificate(
    target: Polynomial,
    names: Sequence[str],
    tensor_id: int,
    edge_count: int,
    certificate: Mapping[str, object],
) -> dict[str, object]:
    inheritance_indices = tuple(range(edge_count, len(names)))
    degrees, coefficients = bernstein_decomposition(target, inheritance_indices)
    if list(degrees) != certificate["inheritance_degrees"]:
        raise AssertionError("inheritance Bernstein degrees mismatch")
    proposed = {
        tuple(int(value) for value in row["index"]): row
        for row in certificate["coefficients"]
    }
    if set(proposed) != set(coefficients):
        raise AssertionError("inheritance Bernstein indices mismatch")
    parser = ExpressionParser(names)
    strictly_positive: set[tuple[int, ...]] = set()
    nonnegative = 0
    even_factors_independently_nonzero = 0
    for index, coefficient in coefficients.items():
        row = proposed[index]
        if not coefficient:
            if not row["zero"]:
                raise AssertionError("zero coefficient called nonzero")
            nonnegative += 1
            continue
        if row["zero"]:
            raise AssertionError("nonzero coefficient called zero")
        expression = normalize_work_expression(
            str(row["factored_coefficient"]), tensor_id, edge_count
        )
        if parser.parse(expression) != coefficient:
            raise AssertionError("factored inheritance coefficient is not exact")
        constant = Fraction(str(row["coefficient"]))
        if constant <= 0:
            raise AssertionError("inheritance coefficient has nonpositive constant")
        product = Polynomial.constant(len(names), constant)
        coefficient_strict = True
        for factor_row in row["factors"]:
            factor_text = normalize_work_expression(
                str(factor_row["factor"]), tensor_id, edge_count
            )
            factor = parser.parse(factor_text)
            exponent = int(factor_row["exponent"])
            product *= factor ** exponent
            reason = factor_row["reason"]
            factor_sign, _ = strict_bernstein_sign(factor)
            if reason == "positive_monomial":
                if factor_sign != 1:
                    raise AssertionError("claimed positive monomial is not positive")
            elif reason == "even_power":
                if exponent % 2:
                    raise AssertionError("claimed even power has odd exponent")
                # Do not trust `strictly_nonzero_before_even_power`: prove it.
                if factor_sign not in {-1, 1}:
                    coefficient_strict = False
                else:
                    even_factors_independently_nonzero += 1
            else:
                raise AssertionError("unknown coefficient factor reason")
        if product != coefficient:
            raise AssertionError("inheritance coefficient factor product mismatch")
        if not row["nonnegative_on_open_edge_cube"]:
            raise AssertionError("certificate itself disclaims nonnegativity")
        nonnegative += 1
        if coefficient_strict:
            strictly_positive.add(index)
    expected_strict = {
        tuple(int(value) for value in index)
        for index in certificate["strictly_positive_coefficient_indices"]
    }
    if strictly_positive != expected_strict:
        raise AssertionError("strict inheritance coefficient set mismatch")
    if not strictly_positive:
        raise AssertionError("no uniformly strict inheritance coefficient")
    if parser.variable_denominators:
        raise AssertionError("inheritance certificate has variable denominator")
    return {
        "inheritance_degrees": list(degrees),
        "coefficient_count": len(coefficients),
        "nonnegative_coefficients": nonnegative,
        "strictly_positive_coefficient_indices": [
            list(index) for index in sorted(strictly_positive)
        ],
        "even_factors_independently_proved_nonzero": even_factors_independently_nonzero,
    }


def audit_three_port_signs(
    submitted: Mapping[str, object], algebra: Mapping[str, object]
) -> dict[str, object]:
    records = submitted["records"]
    algebra_rows = {int(row["tensor_id"]): row for row in algebra["records"]}
    failures: list[dict[str, object]] = []
    counts = Counter()
    methods = Counter()
    total_factor_bernstein = 0
    maximum_factor_bernstein = 0
    reconstructed: set[tuple[int, Tensor]] = set()
    for expected_id, record in enumerate(records):
        tensor_id = int(record["tensor_id"])
        try:
            if tensor_id != expected_id:
                raise AssertionError("tensor ids are not contiguous")
            reticulations = int(record["reticulation_count"])
            signatures = tuple(
                tuple(int(value) for value in row) for row in record["signatures"]
            )
            reconstructed.add((reticulations, signatures))
            expected_hash = sha256(repr((reticulations, signatures)).encode()).hexdigest()
            if expected_hash != record["tensor_sha256"]:
                raise AssertionError("submitted tensor hash mismatch")
            names = tuple(
                [f"x{index}" for index in range(len(signatures))]
                + [f"l{index}" for index in range(reticulations)]
            )
            coordinates = tensor_coordinates(signatures, reticulations, names)
            F = (
                coordinates["a"] * coordinates["b"] * coordinates["c"]
                - coordinates["t"] ** 2
            )
            G = coordinates["a"] - coordinates["b"] * coordinates["c"]
            row = algebra_rows[tensor_id]
            if row["tensor_sha256"] != record["tensor_sha256"]:
                raise AssertionError("algebra row binds to another tensor")
            if not F:
                metadata = verify_expression_factor_certificate(
                    G, row["G_certificate"], names
                )
                if metadata["strict_sign"] != 1:
                    raise AssertionError("G is not strictly positive")
                total_factor_bernstein += int(
                    metadata["total_bernstein_coefficients"]
                )
                maximum_factor_bernstein = max(
                    maximum_factor_bernstein,
                    int(metadata["maximum_factor_bernstein_coefficients"]),
                )
                counts["F_zero_G_positive"] += 1
                methods["G_factor"] += 1
            else:
                method = str(row["F_method"])
                if method == "factor_then_full_bernstein":
                    metadata = verify_expression_factor_certificate(
                        F, row["F_certificate"], names
                    )
                    if metadata["strict_sign"] != 1:
                        raise AssertionError("F is not strictly positive")
                    total_factor_bernstein += int(
                        metadata["total_bernstein_coefficients"]
                    )
                    maximum_factor_bernstein = max(
                        maximum_factor_bernstein,
                        int(metadata["maximum_factor_bernstein_coefficients"]),
                    )
                elif method == "inheritance_bernstein":
                    verify_inheritance_bernstein_certificate(
                        F,
                        names,
                        tensor_id,
                        len(signatures),
                        record["F_inheritance_Bernstein_certificate"],
                    )
                else:
                    raise AssertionError("unknown F proof method")
                counts["F_positive"] += 1
                methods[method] += 1
        except Exception as error:
            failures.append(
                {
                    "tensor_id": tensor_id,
                    "error": f"{type(error).__name__}: {error}",
                }
            )
    return {
        "status": "EXACTLY COMPUTED" if not failures else "FALSE",
        "record_count": len(records),
        "unique_structural_signatures": len(reconstructed),
        "counts": dict(sorted(counts.items())),
        "methods": dict(sorted(methods.items())),
        "total_factor_bernstein_coefficients": total_factor_bernstein,
        "maximum_factor_bernstein_coefficients": maximum_factor_bernstein,
        "failures": failures,
        "structural_signatures": reconstructed,
    }


def endpoint_value(
    assignment: tuple[int, int, int],
    a: Polynomial,
    b: Polynomial,
    c: Polynomial,
    t: Polynomial,
) -> Polynomial:
    nonzero = [index for index, value in enumerate(assignment) if value]
    if not nonzero:
        return Polynomial.constant(a.width, 1)
    if len(nonzero) == 2:
        zero = next(index for index, value in enumerate(assignment) if not value)
        # a=r12 has zero on port 3, b=r13 has zero on port 2,
        # and c=r23 has zero on port 1.
        return (c, b, a)[zero]
    if len(nonzero) == 3 and len(set(assignment)) == 3:
        return t
    raise ValueError("assignment is not a zero-sum three-boundary orbit")


def crossing_blocks() -> tuple[dict[int, list[list[Polynomial]]], tuple[str, ...]]:
    names = ("a", "b", "c", "t", "A", "B", "C", "T", "z")
    variables = [Polynomial.variable(len(names), index) for index in range(len(names))]
    a, b, c, t, A, B, C, T, z = variables
    blocks: dict[int, list[list[Polynomial]]] = {}
    # Physical bridge is 12|34; test wrong split 13|24.
    for character_sum in range(4):
        pairs = tuple(
            pair
            for pair in itertools.product(range(4), repeat=2)
            if pair[0] ^ pair[1] == character_sum
        )
        matrix: list[list[Polynomial]] = []
        for g1, g3 in pairs:
            line = []
            for g2, g4 in pairs:
                bridge_character = g1 ^ g2
                left = endpoint_value((g1, g2, bridge_character), a, b, c, t)
                # Both endpoint tensors use their third port as the physical
                # connector: P=(g1,g2,k), Q=(g3,g4,k).  Putting k first on Q
                # permutes A,B,C and produces a different, non-topological
                # gluing.
                right = endpoint_value((g3, g4, bridge_character), A, B, C, T)
                line.append(left * right * (z if bridge_character else 1))
            matrix.append(line)
        blocks[character_sum] = matrix
    return blocks, names


def polynomial_up_to_sign(polynomial: Polynomial) -> tuple[tuple[tuple[int, ...], Fraction], ...]:
    if not polynomial:
        return ()
    terms = polynomial.terms
    return terms if terms[0][1] > 0 else tuple((monomial, -coefficient) for monomial, coefficient in terms)


def two_by_two_minors(blocks: Mapping[int, Sequence[Sequence[Polynomial]]]) -> set[tuple[tuple[tuple[int, ...], Fraction], ...]]:
    result = set()
    for matrix in blocks.values():
        for rows in itertools.combinations(range(4), 2):
            for columns in itertools.combinations(range(4), 2):
                determinant = (
                    matrix[rows[0]][columns[0]] * matrix[rows[1]][columns[1]]
                    - matrix[rows[0]][columns[1]] * matrix[rows[1]][columns[0]]
                )
                if determinant:
                    result.add(polynomial_up_to_sign(determinant))
    return result


def audit_two_active_algebra() -> dict[str, object]:
    blocks, names = crossing_blocks()
    variables = [Polynomial.variable(len(names), index) for index in range(len(names))]
    a, b, c, t, A, B, C, T, z = variables
    minors = two_by_two_minors(blocks)
    f1 = a * A - z**2 * B * C * b * c
    f2 = z * T * t - z**2 * B * C * b * c
    f3 = z * C * (A * t - z * T * b * c)
    f4 = z * c * (z * B * C * t - T * a)
    decisive = {"f1": f1, "f2": f2, "f3": f3, "f4": f4}
    decisive_membership = {
        name: polynomial_up_to_sign(polynomial) in minors
        for name, polynomial in decisive.items()
    }
    # These additional minors are useful cross-checks because their forms are
    # not generated by the three displayed syzygies below.
    auxiliary = {
        "square_difference": (a * A - T * t * z) * (a * A + T * t * z),
        "left_mixed": a * A**2 - b * c * T**2 * z**2,
        "right_mixed": a**2 * A - t**2 * B * C * z**2,
    }
    auxiliary_membership = {
        name: polynomial_up_to_sign(polynomial) in minors
        for name, polynomial in auxiliary.items()
    }
    identities = {
        "Aa_minus_zTt": a * A - z * T * t - (f1 - f2),
        "left_endpoint": z**2 * C * T * (a * b * c - t**2)
        - (z * C * t * (f1 - f2) - a * f3),
        "right_endpoint": z**2 * c * t * (A * B * C - T**2)
        - (A * f4 + z * c * T * (f1 - f2)),
    }
    return {
        "status": (
            "PROVED"
            if all(decisive_membership.values())
            and all(auxiliary_membership.values())
            and not any(identities.values())
            else "FALSE"
        ),
        "block_shapes": {str(key): [len(value), len(value[0])] for key, value in blocks.items()},
        "distinct_nonzero_minors_up_to_sign": len(minors),
        "decisive_minors_present": decisive_membership,
        "auxiliary_minors_present": auxiliary_membership,
        "identity_remainders_zero": {
            name: not bool(value) for name, value in identities.items()
        },
        "rank_one_consequences": [
            "a*A=z*T*t",
            "a*b*c=t^2",
            "A*B*C=T^2",
        ],
        "open_domain_contradiction": (
            "F=0 at both endpoints gives a>b*c and A>B*C; hence "
            "a*A>b*c*B*C>z^2*b*c*B*C for 0<z<1, contradicting f1=0"
        ),
    }


def tensor_hash(tensor: Tensor) -> str:
    return sha256(repr(tensor).encode()).hexdigest()


def zero_sum_assignments(count: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        assignment
        for assignment in itertools.product(range(4), repeat=count)
        if not _xor_tuple(assignment)
    )


def _xor_tuple(values: Iterable[int]) -> int:
    result = 0
    for value in values:
        result ^= value
    return result


class FourLeafTensor:
    def __init__(self, tensor_id: int, signatures: Tensor):
        self.tensor_id = tensor_id
        self.signatures = signatures
        self.displayed_count = len(signatures[0])
        self.reticulations = {1: 0, 2: 1, 4: 2}[self.displayed_count]
        self.names = tuple(
            f"crossing_t{tensor_id}_p{index}"
            for index in range(len(signatures) + self.reticulations)
        )
        self.variables = [
            Polynomial.variable(len(self.names), index)
            for index in range(len(self.names))
        ]
        self.coordinate_cache: dict[tuple[int, ...], Polynomial] = {}

    def coordinate(self, assignment: tuple[int, ...]) -> Polynomial:
        if assignment in self.coordinate_cache:
            return self.coordinate_cache[assignment]
        edges = self.variables[: len(self.signatures)]
        inheritances = self.variables[len(self.signatures) :]
        choices = tuple(itertools.product((0, 1), repeat=self.reticulations))
        total = Polynomial.constant(len(self.names), 0)
        for choice_index, choice in enumerate(choices):
            term = Polynomial.constant(len(self.names), 1)
            for bit, inheritance in zip(choice, inheritances):
                term *= inheritance if bit == 0 else 1 - inheritance
            for edge, row in zip(edges, self.signatures):
                if xor_on_mask(assignment, row[choice_index]):
                    term *= edge
            total += term
        self.coordinate_cache[assignment] = total
        return total

    def displayed_split_status(self, split: Sequence[int]) -> tuple[bool, ...]:
        mask = sum(1 << (label - 1) for label in split)
        complement = 15 ^ mask
        return tuple(
            any(row[index] in {mask, complement} for row in self.signatures)
            for index in range(self.displayed_count)
        )

    def witness_minor(
        self,
        split: Sequence[int],
        character_sum: int,
        rows: Sequence[int],
        columns: Sequence[int],
    ) -> Polynomial:
        left_positions = tuple(label - 1 for label in split)
        right_positions = tuple(
            position for position in range(4) if position not in left_positions
        )
        pairs = tuple(
            pair
            for pair in itertools.product(range(4), repeat=2)
            if pair[0] ^ pair[1] == character_sum
        )

        def entry(row: int, column: int) -> Polynomial:
            assignment = [0] * 4
            for position, value in zip(left_positions, pairs[row]):
                assignment[position] = value
            for position, value in zip(right_positions, pairs[column]):
                assignment[position] = value
            return self.coordinate(tuple(assignment))

        return (
            entry(rows[0], columns[0]) * entry(rows[1], columns[1])
            - entry(rows[0], columns[1]) * entry(rows[1], columns[0])
        )


def to_sympy(polynomial: Polynomial, names: Sequence[str]) -> sp.Poly:
    symbols = sp.symbols(" ".join(names))
    if len(names) == 1:
        symbols = (symbols,)
    values = {
        monomial: sp.Rational(coefficient.numerator, coefficient.denominator)
        for monomial, coefficient in polynomial.terms
    }
    return sp.Poly.from_dict(values, *symbols, domain=sp.QQ)


def from_sympy(polynomial: sp.Poly, width: int) -> Polynomial:
    return Polynomial.from_dict(
        width,
        {
            tuple(int(exponent) for exponent in monomial): Fraction(
                int(coefficient.p), int(coefficient.q)
            )
            for monomial, coefficient in polynomial.terms()
        },
    )


def independently_factor_and_sign(
    target: Polynomial,
    names: Sequence[str],
    factor_sign_cache: dict[tuple[tuple[tuple[int, ...], Fraction], ...], tuple[int | None, dict[str, object]]],
) -> dict[str, object]:
    sympy_target = to_sympy(target, names)
    constant, factors = sp.factor_list(sympy_target)
    constant_fraction = Fraction(int(constant.p), int(constant.q))
    product = Polynomial.constant(target.width, constant_fraction)
    total_coefficients = 0
    maximum_coefficients = 0
    factor_rows = []
    for sympy_factor, exponent in factors:
        factor = from_sympy(sympy_factor, target.width)
        product *= factor ** int(exponent)
        key = factor.terms
        if key not in factor_sign_cache:
            factor_sign_cache[key] = strict_bernstein_sign(factor)
        sign, metadata = factor_sign_cache[key]
        total_coefficients += int(metadata["coefficient_count"])
        maximum_coefficients = max(
            maximum_coefficients, int(metadata["coefficient_count"])
        )
        if sign not in {-1, 1}:
            raise AssertionError("independent irreducible factor lacks strict open-cube sign")
        factor_rows.append(
            {
                "exponent": int(exponent),
                "terms": len(factor.terms),
                "strict_sign": sign,
                "bernstein": metadata,
            }
        )
    if product != target:
        raise AssertionError("independent factorization does not multiply back")
    return {
        "constant": str(constant_fraction),
        "factor_count": len(factors),
        "factors": factor_rows,
        "total_bernstein_coefficients": total_coefficients,
        "maximum_factor_bernstein_coefficients": maximum_coefficients,
    }


def audit_one_active_atlas(
    strict: Mapping[str, object], tensor_by_hash: Mapping[str, Tensor]
) -> dict[str, object]:
    failures: list[dict[str, object]] = []
    statuses = Counter()
    factor_sign_cache: dict[
        tuple[tuple[tuple[int, ...], Fraction], ...],
        tuple[int | None, dict[str, object]],
    ] = {}
    factorizations = 0
    total_bernstein = 0
    maximum_bernstein = 0
    for record_index, record in enumerate(strict["records"]):
        tensor_id = int(record["tensor_id"])
        tensor_key = str(record["tensor_sha256"])
        try:
            if tensor_key not in tensor_by_hash:
                raise AssertionError("tensor encoding missing from independent universe")
            tensor = FourLeafTensor(tensor_id, tensor_by_hash[tensor_key])
            if len(tensor.signatures) != int(record["edge_signature_count"]):
                raise AssertionError("edge-signature count mismatch")
            if tensor.displayed_count != int(record["displayed_tree_count"]):
                raise AssertionError("displayed-tree count mismatch")
            for split_record in record["splits"]:
                split = tuple(int(value) for value in split_record["split"])
                displayed = tensor.displayed_split_status(split)
                if list(displayed) != split_record["displayed_tree_split_status"]:
                    raise AssertionError("displayed-split status mismatch")
                status = str(split_record["status"])
                statuses[status] += 1
                if all(displayed):
                    if status != "SKIPPED_COMMON_DISPLAYED_SPLIT":
                        raise AssertionError("common displayed split was not skipped")
                    continue
                witness = split_record["witness"]
                if witness is None:
                    raise AssertionError("crossing split has no witness")
                minor = tensor.witness_minor(
                    split,
                    int(witness["character_sum"]),
                    tuple(int(value) for value in witness["rows"]),
                    tuple(int(value) for value in witness["columns"]),
                )
                if not minor:
                    raise AssertionError("selected witness minor is the zero polynomial")
                if len(minor.terms) != int(witness["terms"]):
                    raise AssertionError("witness term count mismatch")
                metadata = independently_factor_and_sign(
                    minor, tensor.names, factor_sign_cache
                )
                factorizations += 1
                total_bernstein += int(metadata["total_bernstein_coefficients"])
                maximum_bernstein = max(
                    maximum_bernstein,
                    int(metadata["maximum_factor_bernstein_coefficients"]),
                )
        except Exception as error:
            failures.append(
                {
                    "tensor_id": tensor_id,
                    "error": f"{type(error).__name__}: {error}",
                }
            )
        if (record_index + 1) % 50 == 0:
            print(
                f"independent one-active replay {record_index + 1}/{len(strict['records'])}",
                file=sys.stderr,
                flush=True,
            )
    return {
        "status": "EXACTLY COMPUTED" if not failures else "FALSE",
        "tensor_records": len(strict["records"]),
        "split_statuses": dict(sorted(statuses.items())),
        "independently_refactored_crossing_minors": factorizations,
        "distinct_irreducible_factor_polynomials": len(factor_sign_cache),
        "total_factor_bernstein_coefficients": total_bernstein,
        "maximum_factor_bernstein_coefficients": maximum_bernstein,
        "failures": failures,
    }


def audit(project: Path, failure_directory: Path) -> dict[str, object]:
    paths = {
        "cores": project / "AUDIT/INDEPENDENT_IMPLEMENTATION/level2_orientation_core_audit.json",
        "submitted": project / "WORK/gate3_two_blob_three_port_signs.json",
        "three_algebra": project / "AUDIT/INDEPENDENT_IMPLEMENTATION/gate3_crossing_certificate_audit.json",
        "strict": project / "AUDIT/INDEPENDENT_IMPLEMENTATION/strict_crossing_tensor_flattening_audit.json",
        "review": project / "AUDIT/REVIEWS/gate3_cut_preservation_adversarial_crosscheck.json",
    }
    raw_cores = json.loads(paths["cores"].read_text())
    submitted = json.loads(paths["submitted"].read_text())
    three_algebra = json.loads(paths["three_algebra"].read_text())
    strict = json.loads(paths["strict"].read_text())
    cores = load_cores(raw_cores)

    # Rebuild the complete three-port structural universe using only literal
    # standard-class full completions.
    root_three, root_three_metrics, _ = enumerate_root_tensors(
        cores, selected_count=3, force_four_columns=False
    )
    incoming_three, incoming_three_metrics, _ = enumerate_nonroot_tensors(
        cores, outgoing_count=2, include_incoming=True
    )
    outgoing_three, outgoing_three_metrics, _ = enumerate_nonroot_tensors(
        cores, outgoing_count=3, include_incoming=False
    )
    structural_root = set().union(
        *(three_port_structural_variants(tensor) for tensor in root_three)
    )
    structural_incoming = set().union(
        *(three_port_structural_variants(tensor) for tensor in incoming_three)
    )
    structural_outgoing = set().union(
        *(three_port_structural_variants(tensor) for tensor in outgoing_three)
    )
    structural_union = structural_root | structural_incoming | structural_outgoing

    sign_audit = audit_three_port_signs(submitted, three_algebra)
    submitted_structural = sign_audit.pop("structural_signatures")
    structural_match = structural_union == submitted_structural

    # Rebuild all 359 one-active tensors.  No historical tensor catalogue is
    # used for the join to the frozen minor records.
    root_four, root_four_metrics, _ = enumerate_root_tensors(cores)
    incoming_four, incoming_four_metrics, _ = enumerate_nonroot_tensors(
        cores, outgoing_count=3, include_incoming=True
    )
    outgoing_four, outgoing_four_metrics, _ = enumerate_nonroot_tensors(
        cores, outgoing_count=4, include_incoming=False
    )
    four_union = root_four | incoming_four | outgoing_four | {TREE_TENSOR}
    tensor_by_hash = {tensor_hash(tensor): tensor for tensor in four_union}
    frozen_hashes = {str(record["tensor_sha256"]) for record in strict["records"]}
    hash_match = set(tensor_by_hash) == frozen_hashes
    one_active = audit_one_active_atlas(strict, tensor_by_hash)
    two_active = audit_two_active_algebra()
    switching = audit_cut_switching(project)

    failure_directory.mkdir(parents=True, exist_ok=True)
    root_failures = {
        "status": "FALSE_PRESENTATIONS_WITH_VALID_ALTERNATIVE_WITNESSES",
        "meaning": (
            "These rooted completions fail the literal one-suppression standard "
            "semi-directed convention.  They were excluded before forming the "
            "independent tensor universe; every resulting tensor type still has a "
            "different literal-standard witness."
        ),
        "three_port": root_three_metrics.pop("literal_failure_rows"),
        "four_port": root_four_metrics.pop("literal_failure_rows"),
    }
    root_failure_path = failure_directory / "gate3_nonstandard_root_presentations.json"
    root_failure_path.write_text(json.dumps(root_failures, indent=2, sort_keys=True) + "\n")
    algebra_failures = {
        "three_port": sign_audit["failures"],
        "one_active": one_active["failures"],
        "two_active_status": two_active["status"],
    }
    algebra_failure_path = failure_directory / "gate3_algebra_failures.json"
    algebra_failure_path.write_text(json.dumps(algebra_failures, indent=2, sort_keys=True) + "\n")

    structural = {
        "three_port": {
            "root_model_types_before_central_designation": len(root_three),
            "incoming_model_types_before_central_designation": len(incoming_three),
            "outgoing_model_types_before_central_designation": len(outgoing_three),
            "root_structural_types": len(structural_root),
            "incoming_structural_types": len(structural_incoming),
            "outgoing_structural_types": len(structural_outgoing),
            "union_structural_types": len(structural_union),
            "submitted_set_matches_exactly": structural_match,
            "root_metrics": root_three_metrics,
            "incoming_metrics": incoming_three_metrics,
            "outgoing_metrics": outgoing_three_metrics,
        },
        "four_port_one_active": {
            "root_types": len(root_four),
            "incoming_types": len(incoming_four),
            "outgoing_types": len(outgoing_four),
            "ordinary_tree_types": 1,
            "union_types": len(four_union),
            "frozen_tensor_hash_set_matches_exactly": hash_match,
            "root_metrics": root_four_metrics,
            "incoming_metrics": incoming_four_metrics,
            "outgoing_metrics": outgoing_four_metrics,
        },
        "arbitrary_serial_subdivision_reduction": {
            "status": "PROVED",
            "reason": (
                "An additional marginalized port subdivision repeats the same "
                "displayed-choice descendant-mask row on the two serial edges.  "
                "Their JC multipliers occur only through their product, and "
                "(0,1)^k -> (0,1) by product is surjective.  One subdivision per "
                "core segment already realizes every possible local repair incidence."
            ),
        },
    }

    finite_success = (
        structural_match
        and hash_match
        and sign_audit["status"] == "EXACTLY COMPUTED"
        and one_active["status"] == "EXACTLY COMPUTED"
        and two_active["status"] == "PROVED"
        and switching["conclusion"] == "PROVED"
    )
    return {
        "inputs": {str(path): file_hash(path) for path in paths.values()},
        "structural_universe": structural,
        "three_port_endpoint_dichotomy": sign_audit,
        "one_active_atlas": one_active,
        "two_active_crossing": two_active,
        "arbitrary_cut_switching_lift": switching,
        "open_Theta_0_logic": {
            "edge_multipliers": "strictly between 0 and 1",
            "inheritance_probabilities": "strictly between 0 and 1",
            "Fourier_coordinates_positive": (
                "each is a positive inheritance-weighted sum of positive edge monomials"
            ),
            "inactive_connector": (
                "a positive convex combination of nonempty path products in (0,1), "
                "and serial products of such scalars, remains in (0,1)"
            ),
            "boundary_specializations_used": False,
        },
        "quantified_direction": {
            "pointwise_statement": (
                "At every open model point, true bridge splits have rank <=4 and "
                "non-bridge splits have rank >4."
            ),
            "one_sided_consequence": (
                "A common point already forces equal cut sets; therefore a fortiori "
                "a source-relative-open subset contained in a target cannot have "
                "different cut sets.  No reversal of preceq is used."
            ),
            "quartet_to_full_rank_direction": (
                "marginalization is left/right linear multiplication, so "
                "rank(quartet)<=rank(full); quartet rank >4 implies full rank >4"
            ),
        },
        "preserved_failure_files": [str(root_failure_path), str(algebra_failure_path)],
        "conclusions": {
            "finite_endpoint_and_one_active_certificates": (
                "EXACTLY COMPUTED" if finite_success else "FALSE"
            ),
            "omitted_two_active_equations": two_active["status"],
            "pointwise_cut_characterization_under_literal_standard_core_convention": (
                "PROVED" if finite_success else "UNRESOLVED"
            ),
            "one_sided_cut_preservation_under_literal_standard_core_convention": (
                "PROVED" if finite_success else "UNRESOLVED"
            ),
            "safe_as_current_manuscript_lemma_before_definitions_gate_is_repaired": False,
            "safe_after_locking_the_literal_standard_convention_and_five_core_reduction": finite_success,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--failures", type=Path, required=True)
    arguments = parser.parse_args()
    result = audit(arguments.project.resolve(), arguments.failures.resolve())
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["conclusions"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
