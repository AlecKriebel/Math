#!/usr/bin/env python3
"""Build exact signed two-minor certificates for twelve K3P target directions.

This is a theorem-certificate producer, not a numerical search.  It starts from
the frozen graph-derived switching signatures, independently compiles every
K3P Fourier coordinate, searches a fixed lexicographically ordered family of
signed pairs of flattening minors, and writes the first strict tensor-Bernstein
certificate for each requested target direction.

Only Python integers and fractions are used.
"""

from __future__ import annotations

import collections
import fractions
import hashlib
import itertools
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
PRIMITIVE = (
    PROJECT / "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json"
)
OUTPUT = HERE / "SIGNED_PAIR_CERTIFICATES.json"

TARGET_INDICES = (108, 110, 113, 114, 116, 120, 128, 175, 178, 180, 181, 184)
EXPECTED_OPERATORS = {
    108: -1,
    110: -1,
    113: -1,
    114: -1,
    116: -1,
    120: -1,
    128: 1,
    175: 1,
    178: 1,
    180: 1,
    181: 1,
    184: 1,
}
PAIRS = tuple(itertools.combinations(range(4), 2))
SECTOR_NAMES = ("C", "G", "T")


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    answer = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            answer.update(block)
    return answer.hexdigest()


def assignments(k: int):
    """All Z_2 x Z_2 character assignments with total character zero."""
    for prefix in itertools.product(range(4), repeat=k - 1):
        last = 0
        for value in prefix:
            last ^= value
        yield prefix + (last,)


def sector(mask: int, characters: tuple[int, ...]) -> int:
    value = 0
    for index, character in enumerate(characters):
        if mask & (1 << index):
            value ^= character
    return value


def permute_mask(mask: int, old_to_new: dict[int, int]) -> int:
    value = 0
    for old, new in old_to_new.items():
        if mask & (1 << old):
            value |= 1 << new
    return value


def inheritance_polynomial(bits: tuple[int, ...]):
    """Expand product_j lambda_j^b_j (1-lambda_j)^(1-b_j)."""
    polynomial = {0: 1}
    for index, bit in enumerate(bits):
        updated = collections.defaultdict(int)
        for mask, coefficient in polynomial.items():
            if bit:
                updated[mask | (1 << index)] += coefficient
            else:
                updated[mask] += coefficient
                updated[mask | (1 << index)] -= coefficient
        polynomial = {mask: coefficient for mask, coefficient in updated.items() if coefficient}
    return tuple(sorted(polynomial.items()))


def compile_descriptor(signatures: tuple[tuple[int, ...], ...], retic_count: int):
    """Compile the exact four-port descriptor directly from switch masks."""
    switch_count = 1 << retic_count
    if any(len(row) != switch_count for row in signatures):
        raise AssertionError("switch/signature width mismatch")
    outputs = []
    for characters in assignments(4):
        grouped = collections.defaultdict(lambda: collections.defaultdict(int))
        for switch_index in range(switch_count):
            bits = tuple(
                (switch_index >> (retic_count - 1 - j)) & 1
                for j in range(retic_count)
            )
            monomial = []
            for edge_index, row in enumerate(signatures):
                character = sector(row[switch_index], characters)
                if character:
                    monomial.append((edge_index, character, 1))
            monomial = tuple(monomial)
            for inheritance_mask, coefficient in inheritance_polynomial(bits):
                grouped[monomial][inheritance_mask] += coefficient
        expression = []
        for monomial, polynomial in grouped.items():
            polynomial = tuple(
                sorted((mask, coefficient) for mask, coefficient in polynomial.items() if coefficient)
            )
            if polynomial:
                expression.append((monomial, polynomial))
        outputs.append(tuple(sorted(expression)))
    return {
        "k": 4,
        "retic_count": retic_count,
        "edge_class_count": len(signatures),
        "outputs": tuple(outputs),
    }


def output_polynomials(descriptor):
    width = 3 * descriptor["edge_class_count"] + descriptor["retic_count"]
    answer = []
    for expression in descriptor["outputs"]:
        polynomial = collections.defaultdict(int)
        for monomial, inheritance in expression:
            base = [0] * width
            for edge, character, exponent in monomial:
                base[3 * edge + character - 1] += exponent
            for mask, coefficient in inheritance:
                term = list(base)
                for index in range(descriptor["retic_count"]):
                    if mask & (1 << index):
                        term[3 * descriptor["edge_class_count"] + index] += 1
                polynomial[tuple(term)] += coefficient
        answer.append({exponent: coefficient for exponent, coefficient in polynomial.items() if coefficient})
    return tuple(answer)


def build_targets(primitive):
    targets = []
    for record in primitive["one_active_wrong_split"]["records"]:
        for split in record["splits"]:
            if split["displayed_by_all"]:
                continue
            first = tuple(split["split"])
            second = tuple(sorted(set(range(4)) - set(first)))
            old_order = first + second
            old_to_new = {old: new for new, old in enumerate(old_order)}
            signatures = tuple(
                tuple(permute_mask(int(mask), old_to_new) for mask in row)
                for row in record["signatures"]
            )
            descriptor = compile_descriptor(signatures, int(record["reticulation_count"]))
            targets.append(
                {
                    "record_id": int(record["id"]),
                    "old_split": first,
                    "old_order": old_order,
                    "signatures": signatures,
                    "descriptor": descriptor,
                }
            )
    return tuple(targets)


def sparse_multiply(left, right):
    answer = collections.defaultdict(int)
    for exponent_left, coefficient_left in left.items():
        for exponent_right, coefficient_right in right.items():
            exponent = tuple(a + b for a, b in zip(exponent_left, exponent_right))
            answer[exponent] += coefficient_left * coefficient_right
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def sparse_add(left, right, right_multiplier: int):
    answer = collections.defaultdict(int)
    answer.update(left)
    for exponent, coefficient in right.items():
        answer[exponent] += right_multiplier * coefficient
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def minor_polynomial(outputs, coordinate_index, character_sum, rows, columns):
    r0, r1 = rows
    c0, c1 = columns
    coordinate_indices = (
        coordinate_index[(r0, character_sum ^ r0, c0, character_sum ^ c0)],
        coordinate_index[(r1, character_sum ^ r1, c1, character_sum ^ c1)],
        coordinate_index[(r0, character_sum ^ r0, c1, character_sum ^ c1)],
        coordinate_index[(r1, character_sum ^ r1, c0, character_sum ^ c0)],
    )
    a, b, c, d = coordinate_indices
    polynomial = sparse_add(
        sparse_multiply(outputs[a], outputs[b]),
        sparse_multiply(outputs[c], outputs[d]),
        -1,
    )
    return polynomial, coordinate_indices


def factor_positive_monomial(polynomial):
    if not polynomial:
        raise ValueError("zero polynomial")
    width = len(next(iter(polynomial)))
    common = tuple(min(exponent[index] for exponent in polynomial) for index in range(width))
    reduced = collections.defaultdict(int)
    for exponent, coefficient in polynomial.items():
        reduced[tuple(exponent[index] - common[index] for index in range(width))] += coefficient
    return common, {exponent: coefficient for exponent, coefficient in reduced.items() if coefficient}


def exact_bernstein(polynomial):
    """Return a strict-sign tensor-Bernstein certificate, or None."""
    width = len(next(iter(polynomial)))
    active = tuple(
        index
        for index in range(width)
        if len({exponent[index] for exponent in polynomial}) > 1
    )
    if not active:
        coefficient = next(iter(polynomial.values()))
        if coefficient == 0:
            return None
        sign = 1 if coefficient > 0 else -1
        return {
            "sign": sign,
            "active_parameter_indices": (),
            "degrees": (),
            "coefficient_count": 1,
            "negative": int(coefficient < 0),
            "zero": 0,
            "positive": int(coefficient > 0),
            "common_denominator": 1,
            "minimum_numerator": coefficient,
            "maximum_numerator": coefficient,
            "ordered_numerators_sha256": digest([coefficient]),
            "nonzero_coefficients": (((), coefficient),),
        }
    reduced = collections.defaultdict(int)
    for exponent, coefficient in polynomial.items():
        reduced[tuple(exponent[index] for index in active)] += coefficient
    reduced = {exponent: coefficient for exponent, coefficient in reduced.items() if coefficient}
    degrees = tuple(max(exponent[index] for exponent in reduced) for index in range(len(active)))
    if any(degree <= 0 for degree in degrees):
        raise AssertionError("invalid active degree")
    coefficients = []
    nonzero = []
    for beta in itertools.product(*(range(degree + 1) for degree in degrees)):
        value = fractions.Fraction(0)
        for alpha, coefficient in reduced.items():
            if all(alpha[index] <= beta[index] for index in range(len(active))):
                multiplier = fractions.Fraction(1)
                for index, degree in enumerate(degrees):
                    multiplier *= fractions.Fraction(
                        math.comb(beta[index], alpha[index]),
                        math.comb(degree, alpha[index]),
                    )
                value += coefficient * multiplier
        coefficients.append((beta, value))
        if value:
            nonzero.append((beta, value))
    values = [value for _, value in coefficients]
    sign = 0
    if all(value >= 0 for value in values) and any(value > 0 for value in values):
        sign = 1
    elif all(value <= 0 for value in values) and any(value < 0 for value in values):
        sign = -1
    if not sign:
        return None
    common_denominator = 1
    for value in values:
        common_denominator = math.lcm(common_denominator, value.denominator)
    numerators = [value.numerator * (common_denominator // value.denominator) for value in values]
    return {
        "sign": sign,
        "active_parameter_indices": active,
        "degrees": degrees,
        "coefficient_count": len(values),
        "negative": sum(value < 0 for value in values),
        "zero": sum(value == 0 for value in values),
        "positive": sum(value > 0 for value in values),
        "common_denominator": common_denominator,
        "minimum_numerator": min(numerators),
        "maximum_numerator": max(numerators),
        "ordered_numerators_sha256": digest(numerators),
        "nonzero_coefficients": tuple(
            (beta, value.numerator * (common_denominator // value.denominator))
            for beta, value in nonzero
        ),
    }


def polynomial_payload(polynomial):
    return [[list(exponent), str(coefficient)] for exponent, coefficient in sorted(polynomial.items())]


def polynomial_digest(polynomial):
    return digest(polynomial_payload(polynomial))


def parameter_label(index: int, edge_count: int) -> str:
    if index < 3 * edge_count:
        return f"{SECTOR_NAMES[index % 3].lower()}{index // 3}"
    return f"lambda{index - 3 * edge_count}"


def choose_certificate(outputs, edge_count: int):
    coordinate_index = {assignment: index for index, assignment in enumerate(assignments(4))}
    tested = 0
    for character_sums in itertools.combinations(range(4), 2):
        for rows in PAIRS:
            for columns in PAIRS:
                left, left_coordinates = minor_polynomial(
                    outputs, coordinate_index, character_sums[0], rows, columns
                )
                right, right_coordinates = minor_polynomial(
                    outputs, coordinate_index, character_sums[1], rows, columns
                )
                for operator in (-1, 1):
                    tested += 1
                    combination = sparse_add(left, right, operator)
                    if not combination:
                        continue
                    common, reduced = factor_positive_monomial(combination)
                    bernstein = exact_bernstein(reduced)
                    if bernstein is None:
                        continue
                    return {
                        "character_sums": character_sums,
                        "rows": rows,
                        "columns": columns,
                        "operator": operator,
                        "candidates_tested": tested,
                        "left_coordinates": left_coordinates,
                        "right_coordinates": right_coordinates,
                        "left": left,
                        "right": right,
                        "combination": combination,
                        "common": common,
                        "reduced": reduced,
                        "bernstein": bernstein,
                        "active_parameter_labels": tuple(
                            parameter_label(index, edge_count)
                            for index in bernstein["active_parameter_indices"]
                        ),
                    }
    raise AssertionError("no signed-pair certificate in deterministic family")


def jsonable_certificate(target_index: int, target, selected):
    descriptor = target["descriptor"]
    edge_count = descriptor["edge_class_count"]
    bernstein = selected["bernstein"]
    nonzero_common = [
        {
            "parameter_index": index,
            "parameter": parameter_label(index, edge_count),
            "exponent": exponent,
        }
        for index, exponent in enumerate(selected["common"])
        if exponent
    ]
    return {
        "target_index": target_index,
        "record_id": target["record_id"],
        "old_split": list(target["old_split"]),
        "old_order": list(target["old_order"]),
        "reticulation_count": descriptor["retic_count"],
        "edge_class_count": edge_count,
        "normalized_signatures_sha256": digest(target["signatures"]),
        "descriptor_sha256": digest(descriptor),
        "output_polynomial_family_sha256": digest(
            [polynomial_payload(polynomial) for polynomial in output_polynomials(descriptor)]
        ),
        "selection": {
            "candidate_order": (
                "lexicographic (character_sum_pair, rows, columns, operator), "
                "with operator order (-1,+1)"
            ),
            "candidates_tested": selected["candidates_tested"],
            "character_sums": list(selected["character_sums"]),
            "rows": list(selected["rows"]),
            "columns": list(selected["columns"]),
            "combination_coefficients": [1, selected["operator"]],
            "left_coordinate_indices": list(selected["left_coordinates"]),
            "right_coordinate_indices": list(selected["right_coordinates"]),
        },
        "polynomials": {
            "left_minor_term_count": len(selected["left"]),
            "left_minor_sha256": polynomial_digest(selected["left"]),
            "right_minor_term_count": len(selected["right"]),
            "right_minor_sha256": polynomial_digest(selected["right"]),
            "signed_combination_term_count": len(selected["combination"]),
            "signed_combination_sha256": polynomial_digest(selected["combination"]),
            "positive_monomial_exponent": list(selected["common"]),
            "positive_monomial_factors": nonzero_common,
            "reduced_term_count": len(selected["reduced"]),
            "reduced_polynomial_sha256": polynomial_digest(selected["reduced"]),
            "reduced_polynomial": polynomial_payload(selected["reduced"]),
        },
        "bernstein": {
            "sign": bernstein["sign"],
            "active_parameter_indices": list(bernstein["active_parameter_indices"]),
            "active_parameter_labels": list(selected["active_parameter_labels"]),
            "degrees": list(bernstein["degrees"]),
            "coefficient_count": bernstein["coefficient_count"],
            "negative": bernstein["negative"],
            "zero": bernstein["zero"],
            "positive": bernstein["positive"],
            "common_denominator": bernstein["common_denominator"],
            "minimum_numerator": bernstein["minimum_numerator"],
            "maximum_numerator": bernstein["maximum_numerator"],
            "ordered_numerators_sha256": bernstein["ordered_numerators_sha256"],
            "nonzero_coefficients": [
                {"multi_index": list(beta), "numerator": numerator}
                for beta, numerator in bernstein["nonzero_coefficients"]
            ],
        },
        "conclusion": (
            "If this target realized the source bridge cut, every Fourier "
            "character block would have rank one and both selected block minors "
            "would vanish.  Their recorded signed combination is strictly "
            "positive on the open unit cube, a contradiction."
        ),
    }


def atomic_write(path: Path, value) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> None:
    primitive = json.loads(PRIMITIVE.read_text())
    targets = build_targets(primitive)
    if len(targets) != 204:
        raise AssertionError(("wrong target-direction count", len(targets)))
    records = []
    for target_index in TARGET_INDICES:
        target = targets[target_index]
        descriptor = target["descriptor"]
        outputs = output_polynomials(descriptor)
        selected = choose_certificate(outputs, descriptor["edge_class_count"])
        if selected["operator"] != EXPECTED_OPERATORS[target_index]:
            raise AssertionError(
                (target_index, "unexpected deterministic operator", selected["operator"])
            )
        if selected["character_sums"] != (0, 1):
            raise AssertionError((target_index, "unexpected character sums"))
        if selected["rows"] != (0, 1) or selected["columns"] != (0, 1):
            raise AssertionError((target_index, "unexpected selected minor"))
        if selected["bernstein"]["sign"] != 1:
            raise AssertionError((target_index, "expected positive combination"))
        records.append(jsonable_certificate(target_index, target, selected))
        print(
            json.dumps(
                {
                    "target_index": target_index,
                    "record_id": target["record_id"],
                    "operator": selected["operator"],
                    "reduced_terms": len(selected["reduced"]),
                    "bernstein_coefficients": selected["bernstein"]["coefficient_count"],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    payload = {
        "schema": "k3p-strong-crossbridge-signed-pair-certificates-v1",
        "status": "CERTIFIED_EXACT",
        "inputs": {
            "primitive_certificate": str(PRIMITIVE.relative_to(PROJECT)),
            "primitive_certificate_sha256": sha_file(PRIMITIVE),
            "producer": str(Path(__file__).resolve().relative_to(PROJECT)),
            "producer_sha256": sha_file(Path(__file__).resolve()),
        },
        "arithmetic": "Python integers and fractions only",
        "domain": {
            "certificate_domain": (
                "every edge Fourier spectrum and inheritance parameter is in (0,1)"
            ),
            "k3p_principal_domain_implication": (
                "D3,+ is a subset of the certified open edge-spectrum cube"
            ),
            "strictness": (
                "after a strictly positive monomial factor, every tensor Bernstein "
                "coefficient is nonnegative and at least one is positive; every "
                "Bernstein basis function is positive in the open cube"
            ),
        },
        "claim": {
            "target_indices": list(TARGET_INDICES),
            "target_count": len(TARGET_INDICES),
            "result": (
                "none of the twelve one-active wrong-split target directions can "
                "satisfy the source-bridge rank-one character-block equations at "
                "a strict K3P point"
            ),
            "logical_use": (
                "each certificate excludes its target from swallowing a source "
                "bridge, because cut rank would force both selected 2x2 block "
                "minors, and hence their signed combination, to vanish"
            ),
        },
        "search": {
            "candidate_family": (
                "pairs of character-block 2x2 minors with a common row pair and "
                "column pair, combined with coefficients (1,-1) or (1,+1)"
            ),
            "ordering": (
                "character-sum pairs, row pairs, and column pairs are lexicographic; "
                "operator -1 precedes +1"
            ),
            "selection_rule": "first strict exact tensor-Bernstein certificate",
        },
        "records": records,
    }
    payload["records_sha256"] = digest(records)
    atomic_write(OUTPUT, payload)
    print(
        json.dumps(
            {
                "status": payload["status"],
                "records": len(records),
                "records_sha256": payload["records_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
