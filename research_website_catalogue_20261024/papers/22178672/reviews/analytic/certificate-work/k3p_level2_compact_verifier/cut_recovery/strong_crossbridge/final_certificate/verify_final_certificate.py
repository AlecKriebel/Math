#!/usr/bin/env python3
"""Standalone independent verifier for the 204-direction final certificate.

This module does not import the producer, the exploratory cross-bridge code, or
the frozen K3P compiler.  It directly recompiles the K3P Fourier polynomials
from the frozen switching masks, replays all 180 single-minor certificates,
checks the labelled split normalization bijection, and validates every child
package by exact content and byte hash.
"""

from __future__ import annotations

import argparse
import collections
import fractions
import hashlib
import itertools
import json
import math
import struct
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
STRONG = HERE.parent
FROZEN = PROJECT / "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json"
DISCOVERY = STRONG / "CUT_MINOR_SIGN_SEARCH.json"
DISCOVERY_RECORDS = STRONG / "cut_minor_sign_records"
DEFAULT_SINGLE = HERE / "SINGLE_MINOR_REPLAY.json"
DEFAULT_UNIVERSE = HERE / "UNIVERSE_CERTIFICATE.json"
DEFAULT_FINAL = HERE / "STRONG_CROSSBRIDGE_FINAL_CERTIFICATE.json"
DEFAULT_REPORT = HERE / "VERIFICATION_REPORT.json"

SIGNED = (108, 110, 113, 114, 116, 120, 128, 175, 178, 180, 181, 184)
CYCLIC = (107, 111, 117, 119, 177, 183, 189, 190, 191, 192)
SPECIAL43 = (127,)
SPECIAL60 = (174,)
RESIDUAL = tuple(sorted(SIGNED + CYCLIC + SPECIAL43 + SPECIAL60))
ASSIGNMENTS = tuple(
    (a, b, c, a ^ b ^ c)
    for a in range(4)
    for b in range(4)
    for c in range(4)
)
INDEX = {assignment: index for index, assignment in enumerate(ASSIGNMENTS)}


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


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


def relative(path):
    return str(Path(path).resolve().relative_to(PROJECT))


def move_mask(mask, order):
    output = 0
    for new, old in enumerate(order):
        output |= ((mask >> old) & 1) << new
    return output


def evaluate_mask(mask, assignment):
    result = 0
    position = 0
    while mask:
        if mask & 1:
            result ^= assignment[position]
        mask >>= 1
        position += 1
    return result


def direct_switch_weight(bits):
    """Subset expansion, intentionally distinct from the producer recurrence."""
    forced = 0
    zero_positions = []
    for index, bit in enumerate(bits):
        if bit:
            forced |= 1 << index
        else:
            zero_positions.append(index)
    answer = []
    for selected in itertools.product((0, 1), repeat=len(zero_positions)):
        mask = forced
        parity = 0
        for index, include in zip(zero_positions, selected):
            if include:
                mask |= 1 << index
                parity ^= 1
        answer.append((mask, -1 if parity else 1))
    return tuple(sorted(answer))


def compile_direction(signatures, reticulation_count):
    switch_count = 2**reticulation_count
    require(
        all(len(signature) == switch_count for signature in signatures),
        "switch width mismatch",
    )
    width = 3 * len(signatures) + reticulation_count
    descriptor_outputs = []
    output_polynomials = []
    for assignment in ASSIGNMENTS:
        grouped = collections.defaultdict(lambda: collections.defaultdict(int))
        sparse = collections.defaultdict(int)
        for switch_index in range(switch_count):
            bits = tuple(
                (switch_index >> (reticulation_count - index - 1)) & 1
                for index in range(reticulation_count)
            )
            monomial = []
            base = [0] * width
            for edge_index, signature in enumerate(signatures):
                character = evaluate_mask(signature[switch_index], assignment)
                if character:
                    monomial.append((edge_index, character, 1))
                    base[3 * edge_index + character - 1] += 1
            for inheritance_mask, coefficient in direct_switch_weight(bits):
                grouped[tuple(monomial)][inheritance_mask] += coefficient
                power = list(base)
                for index in range(reticulation_count):
                    if inheritance_mask & (1 << index):
                        power[3 * len(signatures) + index] = 1
                sparse[tuple(power)] += coefficient
        expression = []
        for monomial in sorted(grouped):
            inheritance = tuple(
                (mask, coefficient)
                for mask, coefficient in sorted(grouped[monomial].items())
                if coefficient
            )
            if inheritance:
                expression.append((monomial, inheritance))
        descriptor_outputs.append(tuple(expression))
        output_polynomials.append(
            {power: coefficient for power, coefficient in sparse.items() if coefficient}
        )
    descriptor = {
        "k": 4,
        "retic_count": reticulation_count,
        "edge_class_count": len(signatures),
        "outputs": tuple(descriptor_outputs),
    }
    return descriptor, tuple(output_polynomials)


def independent_universe(primitive):
    directions = []
    all_keys = set()
    raw_count = 0
    displayed_count = 0
    for record in primitive["one_active_wrong_split"]["records"]:
        for split_record in record["splits"]:
            raw_count += 1
            first = tuple(split_record["split"])
            if split_record["displayed_by_all"]:
                displayed_count += 1
                continue
            require(len(first) == len(set(first)) == 2, "invalid split side")
            complement = tuple(value for value in range(4) if value not in first)
            order = first + complement
            require(tuple(sorted(order)) == (0, 1, 2, 3), "normalization is not a permutation")
            canonical_split = tuple(sorted((tuple(sorted(first)), tuple(sorted(complement)))))
            key = (int(record["id"]), canonical_split)
            require(key not in all_keys, "duplicate labelled direction")
            all_keys.add(key)
            signatures = tuple(
                tuple(move_mask(int(mask), order) for mask in signature)
                for signature in record["signatures"]
            )
            descriptor, outputs = compile_direction(
                signatures, int(record["reticulation_count"])
            )
            directions.append(
                {
                    "target_index": len(directions),
                    "record_id": int(record["id"]),
                    "split": first,
                    "order": order,
                    "signatures": signatures,
                    "reticulation_count": int(record["reticulation_count"]),
                    "descriptor": descriptor,
                    "outputs": outputs,
                }
            )
    require((len(directions), raw_count, displayed_count) == (204, 216, 12), "universe counts")
    require(len(all_keys) == 204, "direction-key count")
    return tuple(directions)


def multiply(left, right):
    answer = collections.defaultdict(int)
    for power_left, coefficient_left in left.items():
        for power_right, coefficient_right in right.items():
            answer[tuple(a + b for a, b in zip(power_left, power_right))] += (
                coefficient_left * coefficient_right
            )
    return {power: coefficient for power, coefficient in answer.items() if coefficient}


def subtract(left, right):
    answer = collections.defaultdict(int)
    for power, coefficient in left.items():
        answer[power] += coefficient
    for power, coefficient in right.items():
        answer[power] -= coefficient
    return {power: coefficient for power, coefficient in answer.items() if coefficient}


def selected_minor(outputs, character_sum, rows, columns):
    r0, r1 = rows
    c0, c1 = columns
    coordinates = (
        INDEX[(r0, character_sum ^ r0, c0, character_sum ^ c0)],
        INDEX[(r1, character_sum ^ r1, c1, character_sum ^ c1)],
        INDEX[(r0, character_sum ^ r0, c1, character_sum ^ c1)],
        INDEX[(r1, character_sum ^ r1, c0, character_sum ^ c0)],
    )
    polynomial = subtract(
        multiply(outputs[coordinates[0]], outputs[coordinates[1]]),
        multiply(outputs[coordinates[2]], outputs[coordinates[3]]),
    )
    return polynomial, coordinates


def strip_monomial(polynomial):
    require(bool(polynomial), "zero selected minor")
    width = len(next(iter(polynomial)))
    common = tuple(min(power[index] for power in polynomial) for index in range(width))
    reduced = collections.defaultdict(int)
    for power, coefficient in polynomial.items():
        reduced[tuple(power[index] - common[index] for index in range(width))] += coefficient
    return common, {power: coefficient for power, coefficient in reduced.items() if coefficient}


def sparse_payload(polynomial):
    return [[list(power), str(coefficient)] for power, coefficient in sorted(polynomial.items())]


def sparse_hash(polynomial):
    return digest(sparse_payload(polynomial))


def replay_bernstein(polynomial):
    width = len(next(iter(polynomial)))
    active = tuple(
        index for index in range(width) if len({power[index] for power in polynomial}) > 1
    )
    projected = collections.defaultdict(int)
    for power, coefficient in polynomial.items():
        projected[tuple(power[index] for index in active)] += coefficient
    projected = {power: coefficient for power, coefficient in projected.items() if coefficient}
    degrees = tuple(max(power[index] for power in projected) for index in range(len(active)))
    require(all(degree in (1, 2) for degree in degrees), "unsupported Bernstein degree")
    coefficients = []
    for beta in itertools.product(*(range(degree + 1) for degree in degrees)):
        value = fractions.Fraction(0)
        for alpha, coefficient in projected.items():
            if all(alpha[index] <= beta[index] for index in range(len(active))):
                factor = fractions.Fraction(1)
                for index, degree in enumerate(degrees):
                    factor *= fractions.Fraction(
                        math.comb(beta[index], alpha[index]),
                        math.comb(degree, alpha[index]),
                    )
                value += coefficient * factor
        coefficients.append((beta, value))
    denominator_power = sum(degree == 2 for degree in degrees)
    denominator = 2**denominator_power
    numerators = []
    for _, value in coefficients:
        scaled = value * denominator
        require(scaled.denominator == 1, "bad Bernstein denominator")
        numerators.append(scaled.numerator)
    legacy_hash = hashlib.sha256()
    for numerator in numerators:
        legacy_hash.update(struct.pack("<q", numerator))
    legacy_hash.update(str(denominator_power).encode())
    sign = 0
    if all(value >= 0 for value in numerators) and any(value > 0 for value in numerators):
        sign = 1
    elif all(value <= 0 for value in numerators) and any(value < 0 for value in numerators):
        sign = -1
    return {
        "sign": sign,
        "active": active,
        "degrees": degrees,
        "numerators": tuple(numerators),
        "denominator_power": denominator_power,
        "legacy_hash": legacy_hash.hexdigest(),
        "nonzero": tuple(
            (beta, numerator)
            for (beta, _), numerator in zip(coefficients, numerators)
            if numerator
        ),
    }


def certificate_category(index):
    if index in SIGNED:
        return "signed_pair"
    if index in CYCLIC:
        return "cyclic"
    if index in SPECIAL43:
        return "record43"
    if index in SPECIAL60:
        return "record60"
    return "single_minor"


def verify_single(single, directions):
    require(single["schema"] == "k3p-strong-crossbridge-single-minor-replay-v1", "single schema")
    require(single["status"] == "PASS", "single status")
    require(single["inputs"]["frozen_primitive_sha256"] == sha_file(FROZEN), "single frozen hash")
    require(single["inputs"]["discovery_manifest_sha256"] == sha_file(DISCOVERY), "discovery hash")
    producer = PROJECT / single["inputs"]["producer"]
    require(producer.is_file(), "producer path")
    require(single["inputs"]["producer_sha256"] == sha_file(producer), "producer hash")
    require(tuple(single["residual_target_indices"]) == RESIDUAL, "residual list")
    bindings = []
    discovery_records = {}
    for target_index in range(204):
        path = DISCOVERY_RECORDS / f"{target_index:03d}.json"
        bindings.append({"target_index": target_index, "path": relative(path), "sha256": sha_file(path)})
        discovery_records[target_index] = json.loads(path.read_text())
    require(single["source_record_bindings"] == bindings, "source-record bindings")
    require(single["inputs"]["discovery_record_tree_sha256"] == digest(bindings), "record tree hash")
    expected_single_indices = tuple(index for index in range(204) if index not in RESIDUAL)
    require(len(single["records"]) == 180, "single record count")
    require(single["records_sha256"] == digest(single["records"]), "single aggregate hash")
    summaries = []
    for position, target_index in enumerate(expected_single_indices):
        stored = single["records"][position]
        direction = directions[target_index]
        discovery = discovery_records[target_index]
        certificate = discovery["certificate"]
        require(certificate is not None, f"target {target_index}: discovery certificate")
        require(stored["target_index"] == target_index, f"target {target_index}: stored index")
        require(stored["record_id"] == direction["record_id"] == discovery["record_id"], f"target {target_index}: record")
        require(stored["old_split"] == list(direction["split"]) == discovery["old_split"], f"target {target_index}: split")
        require(stored["old_order"] == list(direction["order"]) == discovery["old_order"], f"target {target_index}: order")
        descriptor_hash = digest(direction["descriptor"])
        require(stored["descriptor_sha256"] == descriptor_hash == discovery["descriptor_sha256"], f"target {target_index}: descriptor")
        minor_data = stored["minor"]
        polynomial, coordinates = selected_minor(
            direction["outputs"],
            certificate["character_sum"],
            tuple(certificate["rows"]),
            tuple(certificate["columns"]),
        )
        common, reduced = strip_monomial(polynomial)
        bernstein = replay_bernstein(reduced)
        require(bernstein["sign"] == 1, f"target {target_index}: strict sign")
        require(minor_data["character_sum"] == certificate["character_sum"], f"target {target_index}: character sum")
        require(minor_data["rows"] == certificate["rows"], f"target {target_index}: rows")
        require(minor_data["columns"] == certificate["columns"], f"target {target_index}: columns")
        require(minor_data["coordinate_indices"] == list(coordinates) == certificate["coordinate_indices"], f"target {target_index}: coordinates")
        require(minor_data["full_polynomial_sha256"] == sparse_hash(polynomial), f"target {target_index}: full hash")
        require(minor_data["positive_monomial_exponent"] == list(common) == certificate["positive_monomial_exponent"], f"target {target_index}: monomial")
        require(minor_data["reduced_term_count"] == len(reduced) == certificate["term_count"], f"target {target_index}: term count")
        require(minor_data["reduced_polynomial_sha256"] == sparse_hash(reduced) == certificate["reduced_polynomial_sha256"], f"target {target_index}: reduced hash")
        require(minor_data["reduced_polynomial"] == sparse_payload(reduced), f"target {target_index}: explicit polynomial")
        stored_b = stored["bernstein"]
        expected_nonzero = [
            {"multi_index": list(beta), "numerator": numerator}
            for beta, numerator in bernstein["nonzero"]
        ]
        legacy = certificate["full_bernstein"]
        require(stored_b["active_parameter_indices"] == list(bernstein["active"]) == legacy["active_parameter_indices"], f"target {target_index}: active")
        require(stored_b["degrees"] == list(bernstein["degrees"]) == legacy["degrees"], f"target {target_index}: degrees")
        require(stored_b["coefficient_count"] == len(bernstein["numerators"]) == legacy["coefficient_count"], f"target {target_index}: coefficient count")
        require(stored_b["common_denominator"] == f"2^{bernstein['denominator_power']}" == legacy["common_denominator"], f"target {target_index}: denominator")
        require(stored_b["negative"] == sum(value < 0 for value in bernstein["numerators"]) == legacy["negative"], f"target {target_index}: negative")
        require(stored_b["zero"] == sum(value == 0 for value in bernstein["numerators"]) == legacy["zero"], f"target {target_index}: zero")
        require(stored_b["positive"] == sum(value > 0 for value in bernstein["numerators"]) == legacy["positive"], f"target {target_index}: positive")
        require(stored_b["minimum_numerator"] == str(min(bernstein["numerators"])) == legacy["minimum_numerator"], f"target {target_index}: minimum")
        require(stored_b["maximum_numerator"] == str(max(bernstein["numerators"])) == legacy["maximum_numerator"], f"target {target_index}: maximum")
        require(stored_b["ordered_numerators_sha256"] == bernstein["legacy_hash"] == legacy["ordered_numerators_sha256"], f"target {target_index}: numerator hash")
        require(stored_b["sign"] == 1 == legacy["sign"], f"target {target_index}: sign binding")
        require(stored_b["nonzero_coefficients"] == expected_nonzero, f"target {target_index}: nonzero coefficients")
        summaries.append(
            {
                "target_index": target_index,
                "descriptor_sha256": descriptor_hash,
                "minor_sha256": sparse_hash(reduced),
                "bernstein_coefficient_count": len(bernstein["numerators"]),
            }
        )
    for target_index in RESIDUAL:
        require(discovery_records[target_index]["certificate"] is None, f"target {target_index}: expected residual")
    return summaries


def verify_universe(certificate, directions):
    require(certificate["schema"] == "k3p-strong-crossbridge-direction-universe-v1", "universe schema")
    require(certificate["status"] == "PASS", "universe status")
    require(certificate["input"] == {"path": relative(FROZEN), "sha256": sha_file(FROZEN)}, "universe input")
    require(certificate["construction"]["raw_split_entries"] == 216, "raw split count")
    require(certificate["construction"]["common_displayed_splits_removed"] == 12, "displayed count")
    require(certificate["construction"]["wrong_split_directions"] == 204, "wrong split count")
    require(certificate["automorphism_audit"]["used"] is False, "automorphism dependency")
    require(certificate["automorphism_audit"]["known_record60_dummy_label_bug"] == "SUPERSEDED", "record60 bug status")
    rows = certificate["directions"]
    require(len(rows) == 204, "universe row count")
    require(certificate["directions_sha256"] == digest(rows), "universe row hash")
    category_sets = collections.defaultdict(set)
    for target_index, direction in enumerate(directions):
        row = rows[target_index]
        require(row["target_index"] == target_index, f"direction {target_index}: index")
        require(row["record_id"] == direction["record_id"], f"direction {target_index}: record")
        require(row["old_split"] == list(direction["split"]), f"direction {target_index}: split")
        require(row["old_order"] == list(direction["order"]), f"direction {target_index}: order")
        inverse = [direction["order"].index(old) for old in range(4)]
        require(row["old_to_normalized_port_map"] == inverse, f"direction {target_index}: port map")
        require(sorted(inverse) == [0, 1, 2, 3], f"direction {target_index}: map bijection")
        require(row["normalized_split"] == [[0, 1], [2, 3]], f"direction {target_index}: normalized split")
        require(row["normalized_signatures_sha256"] == digest(direction["signatures"]), f"direction {target_index}: signature hash")
        require(row["descriptor_sha256"] == digest(direction["descriptor"]), f"direction {target_index}: descriptor hash")
        expected_category = certificate_category(target_index)
        require(row["certificate_category"] == expected_category, f"direction {target_index}: category")
        category_sets[expected_category].add(target_index)
    expected_partition = {
        "single_minor": sorted(set(range(204)) - set(RESIDUAL)),
        "signed_pair": list(SIGNED),
        "cyclic": list(CYCLIC),
        "record43": list(SPECIAL43),
        "record60": list(SPECIAL60),
    }
    for name, values in expected_partition.items():
        require(certificate["partition"][name] == values, f"partition {name}")
        require(category_sets[name] == set(values), f"row partition {name}")
    union = set().union(*(set(values) for values in expected_partition.values()))
    total = sum(len(values) for values in expected_partition.values())
    require(union == set(range(204)) and total == 204, "partition disjoint union")
    require(certificate["partition"]["pairwise_disjoint"] is True, "partition flag")
    require(certificate["partition"]["union_is_all_204"] is True, "union flag")
    return expected_partition


def artifact_map(dependency):
    result = {}
    for artifact in dependency["artifacts"]:
        path = PROJECT / artifact["path"]
        require(path.is_file(), f"dependency artifact missing: {artifact['path']}")
        require(artifact["sha256"] == sha_file(path), f"dependency hash: {artifact['path']}")
        result[Path(artifact["path"]).name] = path
    return result


def validate_dependencies(final, partition, single_path):
    dependencies = final["dependencies"]
    require(final["dependencies_sha256"] == digest(dependencies), "dependency aggregate hash")
    require([row["name"] for row in dependencies] == ["single_minor", "signed_pair", "cyclic", "record43", "record60"], "dependency order")
    statuses = []
    for dependency in dependencies:
        name = dependency["name"]
        require(dependency["required_targets"] == partition[name], f"dependency target set: {name}")
        passed = False
        if name == "single_minor":
            require(len(dependency["artifacts"]) == 1, "single dependency artifact count")
            binding = dependency["artifacts"][0]
            require(binding["path"] == relative(DEFAULT_SINGLE), "single dependency path")
            require(binding["sha256"] == sha_file(single_path), "single dependency hash")
            passed = True
            artifacts = {}
        else:
            artifacts = artifact_map(dependency)
        if name == "signed_pair":
            manifest = json.loads(artifacts["SIGNED_PAIR_CERTIFICATES.json"].read_text())
            replay = json.loads(artifacts["VERIFICATION_REPORT.json"].read_text())
            mutations = json.loads(artifacts["ADVERSARIAL_MUTATION_REPORT.json"].read_text())
            passed = bool(
                manifest.get("status") == "CERTIFIED_EXACT"
                and tuple(manifest.get("claim", {}).get("target_indices", ())) == SIGNED
                and replay.get("status") == "PASS"
                and replay.get("manifest_sha256") == sha_file(artifacts["SIGNED_PAIR_CERTIFICATES.json"])
                and mutations.get("status") == "PASS"
                and mutations.get("all_mutations_rejected") is True
            )
        elif name == "cyclic":
            theorem = json.loads(artifacts["THEOREM_MANIFEST.json"].read_text())
            core = json.loads(artifacts["CYCLIC_SIX_MINOR_CERTIFICATES.json"].read_text())
            replay = json.loads(artifacts["VERIFICATION_REPORT.json"].read_text())
            optimized = json.loads(artifacts["OPTIMIZED_VERIFICATION_REPORT.json"].read_text())
            core_sha = sha_file(artifacts["CYCLIC_SIX_MINOR_CERTIFICATES.json"])
            passed = bool(
                theorem.get("status") == "PASS"
                and tuple(theorem.get("scope", {}).get("target_indices", ())) == CYCLIC
                and core.get("status") == "PASS"
                and tuple(core.get("target_indices", ())) == CYCLIC
                and replay.get("status") == optimized.get("status") == "PASS"
                and replay.get("artifact_sha256") == optimized.get("artifact_sha256") == core_sha
                and replay.get("mutation_count") == optimized.get("mutation_count") == 40
                and all(row.get("result") == "REJECTED" for row in replay.get("mutations", ()))
                and all(row.get("result") == "REJECTED" for row in optimized.get("mutations", ()))
                and theorem.get("files", {}).get("CYCLIC_SIX_MINOR_CERTIFICATES.json") == core_sha
            )
        elif name in ("record43", "record60"):
            json_name = (
                "RECORD43_CYCLIC_TRANSPORT_AUDIT.json"
                if name == "record43"
                else "RECORD60_CYCLIC_CERTIFICATE_AUDIT.json"
            )
            script_name = (
                "verify_record43_cyclic_transport.py"
                if name == "record43"
                else "verify_record60_cyclic_certificate.py"
            )
            audit = json.loads(artifacts[json_name].read_text())
            expected_target = 127 if name == "record43" else 174
            expected_record = 43 if name == "record43" else 60
            passed = bool(
                audit.get("status") == "PASS"
                and audit.get("target_index") == expected_target
                and audit.get("record_id") == expected_record
                and audit.get("inputs", {}).get("audit_script_sha256") == sha_file(artifacts[script_name])
                and audit.get("mutation_tests")
                and all(row.get("result") == "REJECTED" for row in audit["mutation_tests"])
            )
        require(dependency["status"] == ("PASS" if passed else "BLOCKED"), f"dependency status: {name}")
        require((dependency["reason"] is None) == passed, f"dependency reason: {name}")
        statuses.append(passed)
    return statuses


def verify_all(single_path, universe_path, final_path):
    primitive = json.loads(FROZEN.read_text())
    directions = independent_universe(primitive)
    single = json.loads(single_path.read_text())
    universe = json.loads(universe_path.read_text())
    final = json.loads(final_path.read_text())
    single_summaries = verify_single(single, directions)
    partition = verify_universe(universe, directions)
    require(final["schema"] == "k3p-strong-crossbridge-final-certificate-v1", "final schema")
    for name, expected_path, content_path in (
        ("frozen_primitive", FROZEN, FROZEN),
        ("builder", PROJECT / final["inputs"]["builder"]["path"], PROJECT / final["inputs"]["builder"]["path"]),
        ("single_minor_replay", DEFAULT_SINGLE, single_path),
        ("universe_certificate", DEFAULT_UNIVERSE, universe_path),
    ):
        binding = final["inputs"][name]
        require(binding["path"] == relative(expected_path), f"final input path: {name}")
        require(binding["sha256"] == sha_file(content_path), f"final input hash: {name}")
    statuses = validate_dependencies(final, partition, single_path)
    all_pass = all(statuses)
    require(final["status"] == ("PASS" if all_pass else "BLOCKED"), "final status")
    require(final["blocked_dependencies"] == ([] if all_pass else [name for name, passed in zip(["single_minor", "signed_pair", "cyclic", "record43", "record60"], statuses) if not passed]), "blocked list")
    require(final["coverage"]["target_directions"] == 204, "final coverage count")
    require(
        final["coverage"]["partition_counts"]
        == {"single_minor": 180, "signed_pair": 12, "cyclic": 10, "record43": 1, "record60": 1},
        "final partition counts",
    )
    require(final["coverage"]["pairwise_disjoint"] is True, "final disjoint flag")
    require(final["coverage"]["union_is_all_204"] is True, "final union flag")
    require(final["coverage"]["normalization_replayed"] is True, "final normalization flag")
    require(final["coverage"]["automorphism_transport_used"] is False, "final automorphism flag")
    return {
        "schema": "k3p-strong-crossbridge-final-verification-v1",
        "status": "PASS" if all_pass else "PASS_BLOCKED",
        "final_certificate_status": final["status"],
        "verifier": {
            "path": relative(Path(__file__).resolve()),
            "sha256": sha_file(Path(__file__).resolve()),
        },
        "artifacts": {
            "single_minor_replay_sha256": sha_file(single_path),
            "universe_certificate_sha256": sha_file(universe_path),
            "final_certificate_sha256": sha_file(final_path),
        },
        "independence": {
            "producer_imported": False,
            "exploration_module_imported": False,
            "k3p_atlas_compiler_imported": False,
            "direct_switch_mask_compilation": True,
            "exact_integer_fraction_arithmetic": True,
        },
        "checks": {
            "raw_split_entries": 216,
            "displayed_splits_removed": 12,
            "normalized_wrong_split_directions": 204,
            "normalization_bijections": 204,
            "duplicate_direction_keys": 0,
            "single_minors_replayed": len(single_summaries),
            "single_bernstein_certificates_strict": len(single_summaries),
            "signed_pair_targets_bound": len(SIGNED),
            "cyclic_targets_bound": len(CYCLIC),
            "record43_targets_bound": len(SPECIAL43),
            "record60_targets_bound": len(SPECIAL60),
            "partition_union": 204,
            "child_dependencies_pass": sum(statuses),
            "record60_dummy_label_automorphism_bug": "SUPERSEDED_BY_DIRECT_LABELLED_ENUMERATION",
        },
        "single_minor_summary_sha256": digest(single_summaries),
    }


def atomic_write(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--single", type=Path, default=DEFAULT_SINGLE)
    parser.add_argument("--universe", type=Path, default=DEFAULT_UNIVERSE)
    parser.add_argument("--final", type=Path, default=DEFAULT_FINAL)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--no-report", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    arguments = parser.parse_args()
    try:
        report = verify_all(
            arguments.single.resolve(),
            arguments.universe.resolve(),
            arguments.final.resolve(),
        )
    except Exception as error:
        if not arguments.quiet:
            print(json.dumps({"status": "FAIL", "error": f"{type(error).__name__}: {error}"}, sort_keys=True))
        return 1
    if not arguments.no_report:
        atomic_write(arguments.report, report)
    if not arguments.quiet:
        print(
            json.dumps(
                {
                    "status": report["status"],
                    "final_certificate_status": report["final_certificate_status"],
                    "directions": report["checks"]["normalized_wrong_split_directions"],
                    "single_minors": report["checks"]["single_minors_replayed"],
                },
                sort_keys=True,
            )
        )
    # A structurally valid aggregate with unresolved child dependencies is a
    # useful diagnostic report, but it is not a passing theorem certificate.
    # Fail closed for standalone callers as well as for the later global gate.
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
