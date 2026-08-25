#!/usr/bin/env python3
"""Independent exact replay of the signed two-minor certificates.

The verifier deliberately does not import the producer, the exploratory
cross-bridge scripts, or the K3P atlas compiler.  It separately rebuilds the
target-direction order and Fourier polynomials from the frozen switching-mask
records, then recomputes the selected minors and every Bernstein coefficient.
"""

from __future__ import annotations

import argparse
import collections
import fractions
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
DEFAULT_MANIFEST = HERE / "SIGNED_PAIR_CERTIFICATES.json"
DEFAULT_REPORT = HERE / "VERIFICATION_REPORT.json"
FROZEN_INPUT = (
    PROJECT / "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json"
)
EXPECTED_TARGETS = (108, 110, 113, 114, 116, 120, 128, 175, 178, 180, 181, 184)
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
PAIR_ORDER = tuple(itertools.combinations(range(4), 2))
CHARACTER_LABELS = ("C", "G", "T")


class VerificationFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    answer = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while True:
            block = handle.read(1048576)
            if not block:
                break
            answer.update(block)
    return answer.hexdigest()


def zero_sum_words():
    words = []
    for a in range(4):
        for b in range(4):
            for c in range(4):
                words.append((a, b, c, a ^ b ^ c))
    return tuple(words)


ASSIGNMENTS = zero_sum_words()
ASSIGNMENT_INDEX = {word: index for index, word in enumerate(ASSIGNMENTS)}


def remap_mask(mask, order):
    result = 0
    for new_label, old_label in enumerate(order):
        if mask & (1 << old_label):
            result |= 1 << new_label
    return result


def mask_character(mask, word):
    result = 0
    bit = 0
    while mask:
        if mask & 1:
            result ^= word[bit]
        mask >>= 1
        bit += 1
    return result


def switch_weight(bits):
    """Direct subset expansion, independent of the producer's recurrence."""
    fixed_mask = sum((1 << j) for j, bit in enumerate(bits) if bit)
    zero_positions = tuple(j for j, bit in enumerate(bits) if not bit)
    terms = []
    for subset_bits in itertools.product((0, 1), repeat=len(zero_positions)):
        mask = fixed_mask
        negative_count = 0
        for position, chosen in zip(zero_positions, subset_bits):
            if chosen:
                mask |= 1 << position
                negative_count += 1
        terms.append((mask, -1 if negative_count % 2 else 1))
    return tuple(sorted(terms))


def independent_compile(signatures, reticulation_count):
    switch_total = 2**reticulation_count
    require(
        all(len(signature) == switch_total for signature in signatures),
        "frozen signature has wrong switch width",
    )
    expressions = []
    sparse_outputs = []
    parameter_width = 3 * len(signatures) + reticulation_count
    for word in ASSIGNMENTS:
        grouped = collections.defaultdict(lambda: collections.defaultdict(int))
        sparse = collections.defaultdict(int)
        for switch_number in range(switch_total):
            bits = tuple(
                (switch_number >> (reticulation_count - j - 1)) & 1
                for j in range(reticulation_count)
            )
            monomial = []
            base_exponent = [0] * parameter_width
            for edge_number, signature in enumerate(signatures):
                character = mask_character(signature[switch_number], word)
                if character:
                    monomial.append((edge_number, character, 1))
                    base_exponent[3 * edge_number + character - 1] += 1
            weight = switch_weight(bits)
            for inheritance_mask, coefficient in weight:
                grouped[tuple(monomial)][inheritance_mask] += coefficient
                exponent = list(base_exponent)
                for j in range(reticulation_count):
                    if inheritance_mask & (1 << j):
                        exponent[3 * len(signatures) + j] = 1
                sparse[tuple(exponent)] += coefficient
        expression = []
        for monomial in sorted(grouped):
            weight = tuple(
                (mask, coefficient)
                for mask, coefficient in sorted(grouped[monomial].items())
                if coefficient
            )
            if weight:
                expression.append((monomial, weight))
        expressions.append(tuple(expression))
        sparse_outputs.append(
            {exponent: coefficient for exponent, coefficient in sparse.items() if coefficient}
        )
    descriptor = {
        "k": 4,
        "retic_count": reticulation_count,
        "edge_class_count": len(signatures),
        "outputs": tuple(expressions),
    }
    return descriptor, tuple(sparse_outputs)


def rebuild_target_universe(primitive):
    result = []
    for frozen_record in primitive["one_active_wrong_split"]["records"]:
        for split_record in frozen_record["splits"]:
            if split_record["displayed_by_all"]:
                continue
            split = tuple(split_record["split"])
            complement = tuple(value for value in range(4) if value not in split)
            order = split + complement
            signatures = tuple(
                tuple(remap_mask(int(mask), order) for mask in signature)
                for signature in frozen_record["signatures"]
            )
            descriptor, sparse = independent_compile(
                signatures, int(frozen_record["reticulation_count"])
            )
            result.append(
                {
                    "record_id": int(frozen_record["id"]),
                    "old_split": split,
                    "old_order": order,
                    "signatures": signatures,
                    "descriptor": descriptor,
                    "sparse_outputs": sparse,
                }
            )
    return tuple(result)


def multiply_polynomials(left, right):
    result = collections.defaultdict(int)
    for left_power, left_coefficient in left.items():
        for right_power, right_coefficient in right.items():
            result[tuple(x + y for x, y in zip(left_power, right_power))] += (
                left_coefficient * right_coefficient
            )
    return {power: coefficient for power, coefficient in result.items() if coefficient}


def combine_polynomials(left, right, multiplier):
    result = collections.defaultdict(int)
    for power, coefficient in left.items():
        result[power] += coefficient
    for power, coefficient in right.items():
        result[power] += multiplier * coefficient
    return {power: coefficient for power, coefficient in result.items() if coefficient}


def block_minor(outputs, character_sum, rows, columns):
    r0, r1 = rows
    c0, c1 = columns
    coordinates = (
        ASSIGNMENT_INDEX[(r0, character_sum ^ r0, c0, character_sum ^ c0)],
        ASSIGNMENT_INDEX[(r1, character_sum ^ r1, c1, character_sum ^ c1)],
        ASSIGNMENT_INDEX[(r0, character_sum ^ r0, c1, character_sum ^ c1)],
        ASSIGNMENT_INDEX[(r1, character_sum ^ r1, c0, character_sum ^ c0)],
    )
    first = multiply_polynomials(outputs[coordinates[0]], outputs[coordinates[1]])
    second = multiply_polynomials(outputs[coordinates[2]], outputs[coordinates[3]])
    return combine_polynomials(first, second, -1), coordinates


def remove_common_monomial(polynomial):
    require(bool(polynomial), "signed combination is zero")
    width = len(next(iter(polynomial)))
    common = tuple(min(power[j] for power in polynomial) for j in range(width))
    result = collections.defaultdict(int)
    for power, coefficient in polynomial.items():
        result[tuple(power[j] - common[j] for j in range(width))] += coefficient
    return common, {power: coefficient for power, coefficient in result.items() if coefficient}


def bernstein_coefficients(polynomial):
    parameter_width = len(next(iter(polynomial)))
    active = tuple(
        j for j in range(parameter_width) if len({power[j] for power in polynomial}) > 1
    )
    projected = collections.defaultdict(int)
    for power, coefficient in polynomial.items():
        projected[tuple(power[j] for j in active)] += coefficient
    projected = {power: coefficient for power, coefficient in projected.items() if coefficient}
    if not active:
        only = fractions.Fraction(next(iter(projected.values())))
        return active, (), (((), only),)
    degrees = tuple(max(power[j] for power in projected) for j in range(len(active)))
    result = []
    for beta in itertools.product(*(range(degree + 1) for degree in degrees)):
        coefficient = fractions.Fraction(0)
        for alpha, power_coefficient in projected.items():
            if not all(alpha[j] <= beta[j] for j in range(len(active))):
                continue
            ratio = fractions.Fraction(1)
            for j, degree in enumerate(degrees):
                ratio *= fractions.Fraction(
                    math.comb(beta[j], alpha[j]), math.comb(degree, alpha[j])
                )
            coefficient += power_coefficient * ratio
        result.append((beta, coefficient))
    return active, degrees, tuple(result)


def strict_sign(ordered_coefficients):
    values = tuple(value for _, value in ordered_coefficients)
    if all(value >= 0 for value in values) and any(value > 0 for value in values):
        return 1
    if all(value <= 0 for value in values) and any(value < 0 for value in values):
        return -1
    return 0


def certificate_summary(polynomial):
    common, reduced = remove_common_monomial(polynomial)
    active, degrees, coefficients = bernstein_coefficients(reduced)
    sign = strict_sign(coefficients)
    if sign == 0:
        return None
    denominator = 1
    for _, value in coefficients:
        denominator = math.lcm(denominator, value.denominator)
    numerators = tuple(
        value.numerator * (denominator // value.denominator) for _, value in coefficients
    )
    nonzero = tuple(
        (beta, numerator)
        for (beta, _), numerator in zip(coefficients, numerators)
        if numerator
    )
    return {
        "common": common,
        "reduced": reduced,
        "active": active,
        "degrees": degrees,
        "sign": sign,
        "denominator": denominator,
        "numerators": numerators,
        "nonzero": nonzero,
    }


def sparse_payload(polynomial):
    return [[list(power), str(coefficient)] for power, coefficient in sorted(polynomial.items())]


def sparse_hash(polynomial):
    return digest(sparse_payload(polynomial))


def label_parameter(index, edge_count):
    if index < 3 * edge_count:
        return f"{CHARACTER_LABELS[index % 3].lower()}{index // 3}"
    return f"lambda{index - 3 * edge_count}"


def first_certificate(outputs):
    attempts = 0
    for sums in itertools.combinations(range(4), 2):
        for rows in PAIR_ORDER:
            for columns in PAIR_ORDER:
                left, left_coordinates = block_minor(outputs, sums[0], rows, columns)
                right, right_coordinates = block_minor(outputs, sums[1], rows, columns)
                for operator in (-1, 1):
                    attempts += 1
                    signed = combine_polynomials(left, right, operator)
                    if not signed:
                        continue
                    summary = certificate_summary(signed)
                    if summary is not None:
                        return {
                            "attempts": attempts,
                            "sums": sums,
                            "rows": rows,
                            "columns": columns,
                            "operator": operator,
                            "left": left,
                            "right": right,
                            "signed": signed,
                            "left_coordinates": left_coordinates,
                            "right_coordinates": right_coordinates,
                            "summary": summary,
                        }
    raise VerificationFailure("deterministic certificate search failed")


def verify_record(stored, target_index, target):
    descriptor = target["descriptor"]
    edge_count = descriptor["edge_class_count"]
    require(stored["target_index"] == target_index, f"target {target_index}: index")
    require(stored["record_id"] == target["record_id"], f"target {target_index}: record id")
    require(stored["old_split"] == list(target["old_split"]), f"target {target_index}: split")
    require(stored["old_order"] == list(target["old_order"]), f"target {target_index}: order")
    require(
        stored["reticulation_count"] == descriptor["retic_count"],
        f"target {target_index}: reticulation count",
    )
    require(stored["edge_class_count"] == edge_count, f"target {target_index}: edge count")
    require(
        stored["normalized_signatures_sha256"] == digest(target["signatures"]),
        f"target {target_index}: signature hash",
    )
    require(
        stored["descriptor_sha256"] == digest(descriptor),
        f"target {target_index}: descriptor hash",
    )
    require(
        stored["output_polynomial_family_sha256"]
        == digest([sparse_payload(polynomial) for polynomial in target["sparse_outputs"]]),
        f"target {target_index}: output-polynomial family hash",
    )

    selected = first_certificate(target["sparse_outputs"])
    selection = stored["selection"]
    require(selected["operator"] == EXPECTED_OPERATORS[target_index], f"target {target_index}: operator theorem table")
    require(selection["candidates_tested"] == selected["attempts"], f"target {target_index}: attempt count")
    require(selection["character_sums"] == list(selected["sums"]), f"target {target_index}: sums")
    require(selection["rows"] == list(selected["rows"]), f"target {target_index}: rows")
    require(selection["columns"] == list(selected["columns"]), f"target {target_index}: columns")
    require(
        selection["combination_coefficients"] == [1, selected["operator"]],
        f"target {target_index}: signed combination",
    )
    require(
        selection["left_coordinate_indices"] == list(selected["left_coordinates"]),
        f"target {target_index}: left coordinates",
    )
    require(
        selection["right_coordinate_indices"] == list(selected["right_coordinates"]),
        f"target {target_index}: right coordinates",
    )

    polynomial = stored["polynomials"]
    summary = selected["summary"]
    require(polynomial["left_minor_term_count"] == len(selected["left"]), f"target {target_index}: left terms")
    require(polynomial["left_minor_sha256"] == sparse_hash(selected["left"]), f"target {target_index}: left hash")
    require(polynomial["right_minor_term_count"] == len(selected["right"]), f"target {target_index}: right terms")
    require(polynomial["right_minor_sha256"] == sparse_hash(selected["right"]), f"target {target_index}: right hash")
    require(polynomial["signed_combination_term_count"] == len(selected["signed"]), f"target {target_index}: signed terms")
    require(polynomial["signed_combination_sha256"] == sparse_hash(selected["signed"]), f"target {target_index}: signed hash")
    require(polynomial["positive_monomial_exponent"] == list(summary["common"]), f"target {target_index}: common monomial")
    expected_factors = [
        {
            "parameter_index": index,
            "parameter": label_parameter(index, edge_count),
            "exponent": exponent,
        }
        for index, exponent in enumerate(summary["common"])
        if exponent
    ]
    require(polynomial["positive_monomial_factors"] == expected_factors, f"target {target_index}: common factors")
    require(polynomial["reduced_term_count"] == len(summary["reduced"]), f"target {target_index}: reduced terms")
    require(polynomial["reduced_polynomial_sha256"] == sparse_hash(summary["reduced"]), f"target {target_index}: reduced hash")
    require(polynomial["reduced_polynomial"] == sparse_payload(summary["reduced"]), f"target {target_index}: reduced payload")

    bernstein = stored["bernstein"]
    numerators = summary["numerators"]
    require(summary["sign"] == 1, f"target {target_index}: recomputed strict sign")
    require(bernstein["sign"] == summary["sign"], f"target {target_index}: sign")
    require(bernstein["active_parameter_indices"] == list(summary["active"]), f"target {target_index}: active parameters")
    require(
        bernstein["active_parameter_labels"]
        == [label_parameter(index, edge_count) for index in summary["active"]],
        f"target {target_index}: active labels",
    )
    require(bernstein["degrees"] == list(summary["degrees"]), f"target {target_index}: degrees")
    require(bernstein["coefficient_count"] == len(numerators), f"target {target_index}: coefficient count")
    require(bernstein["negative"] == sum(value < 0 for value in numerators), f"target {target_index}: negative count")
    require(bernstein["zero"] == sum(value == 0 for value in numerators), f"target {target_index}: zero count")
    require(bernstein["positive"] == sum(value > 0 for value in numerators), f"target {target_index}: positive count")
    require(bernstein["common_denominator"] == summary["denominator"], f"target {target_index}: denominator")
    require(bernstein["minimum_numerator"] == min(numerators), f"target {target_index}: minimum numerator")
    require(bernstein["maximum_numerator"] == max(numerators), f"target {target_index}: maximum numerator")
    require(bernstein["ordered_numerators_sha256"] == digest(numerators), f"target {target_index}: numerator hash")
    expected_nonzero = [
        {"multi_index": list(beta), "numerator": numerator}
        for beta, numerator in summary["nonzero"]
    ]
    require(bernstein["nonzero_coefficients"] == expected_nonzero, f"target {target_index}: nonzero coefficients")
    require(bernstein["negative"] == 0 and bernstein["positive"] > 0, f"target {target_index}: strict positivity")
    return {
        "target_index": target_index,
        "record_id": target["record_id"],
        "operator": selected["operator"],
        "reduced_polynomial_sha256": sparse_hash(summary["reduced"]),
        "bernstein_coefficients": len(numerators),
        "positive_bernstein_coefficients": sum(value > 0 for value in numerators),
    }


def verify_manifest_data(manifest, manifest_path=DEFAULT_MANIFEST, check_producer=True):
    require(
        manifest["schema"] == "k3p-strong-crossbridge-signed-pair-certificates-v1",
        "schema",
    )
    require(manifest["status"] == "CERTIFIED_EXACT", "status")
    expected_input_relative = str(FROZEN_INPUT.relative_to(PROJECT))
    require(
        manifest["inputs"]["primitive_certificate"] == expected_input_relative,
        "input path",
    )
    frozen_sha = sha_file(FROZEN_INPUT)
    require(
        manifest["inputs"]["primitive_certificate_sha256"] == frozen_sha,
        "frozen input hash",
    )
    if check_producer:
        producer_path = PROJECT / manifest["inputs"]["producer"]
        require(producer_path.is_file(), "producer path")
        require(manifest["inputs"]["producer_sha256"] == sha_file(producer_path), "producer hash")
    require(tuple(manifest["claim"]["target_indices"]) == EXPECTED_TARGETS, "claim target list")
    require(manifest["claim"]["target_count"] == len(EXPECTED_TARGETS), "claim target count")
    records = manifest["records"]
    require(len(records) == len(EXPECTED_TARGETS), "record count")
    require(manifest["records_sha256"] == digest(records), "records aggregate hash")
    primitive = json.loads(FROZEN_INPUT.read_text())
    universe = rebuild_target_universe(primitive)
    require(len(universe) == 204, "target universe count")
    summaries = []
    for position, target_index in enumerate(EXPECTED_TARGETS):
        summaries.append(verify_record(records[position], target_index, universe[target_index]))
    return {
        "schema": "k3p-signed-pair-certificate-verification-v1",
        "status": "PASS",
        "manifest": str(Path(manifest_path).resolve().relative_to(PROJECT)),
        "manifest_sha256": sha_file(manifest_path),
        "frozen_input_sha256": frozen_sha,
        "independence": {
            "producer_imported": False,
            "exploration_scripts_imported": False,
            "k3p_atlas_compiler_imported": False,
            "fourier_compilation": "independent direct switch-mask expansion",
            "arithmetic": "Python integers and fractions only",
        },
        "checks": {
            "target_universe_count": 204,
            "certificate_count": len(summaries),
            "all_target_bindings_replayed": True,
            "all_selected_minors_rebuilt": True,
            "all_signed_combinations_rebuilt": True,
            "all_bernstein_coefficients_recomputed": True,
            "all_combinations_strictly_positive": True,
            "cut_rank_contradiction_valid": True,
        },
        "records": summaries,
    }


def atomic_write(path, value):
    temporary = Path(str(path) + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--no-report", action="store_true")
    parser.add_argument("--skip-producer-hash", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    arguments = parser.parse_args()
    try:
        manifest = json.loads(arguments.manifest.read_text())
        report = verify_manifest_data(
            manifest,
            manifest_path=arguments.manifest,
            check_producer=not arguments.skip_producer_hash,
        )
    except Exception as error:
        failure = {"status": "FAIL", "error": f"{type(error).__name__}: {error}"}
        if not arguments.quiet:
            print(json.dumps(failure, sort_keys=True))
        return 1
    if not arguments.no_report:
        atomic_write(arguments.report, report)
    if not arguments.quiet:
        print(
            json.dumps(
                {
                    "status": report["status"],
                    "certificates": report["checks"]["certificate_count"],
                    "manifest_sha256": report["manifest_sha256"],
                },
                sort_keys=True,
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
