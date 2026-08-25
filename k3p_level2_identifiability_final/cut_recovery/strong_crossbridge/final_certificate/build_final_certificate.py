#!/usr/bin/env python3
"""Build the aggregate exact strong-crossbridge certificate.

The builder independently replays all 180 strict single-minor certificates
from the frozen graph-derived switching signatures.  It also proves the
204-direction universe count and normalized-split bookkeeping, then binds the
separate signed-pair, cyclic, record-43, and record-60 proof packages.

The aggregate remains BLOCKED unless every required child proof reports PASS.
All algebra in this file uses Python integers and fractions only.
"""

from __future__ import annotations

import collections
import fractions
import hashlib
import itertools
import json
import math
import struct
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
STRONG = HERE.parent
FROZEN = PROJECT / "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json"
DISCOVERY = STRONG / "CUT_MINOR_SIGN_SEARCH.json"
DISCOVERY_RECORDS = STRONG / "cut_minor_sign_records"

SINGLE_OUTPUT = HERE / "SINGLE_MINOR_REPLAY.json"
UNIVERSE_OUTPUT = HERE / "UNIVERSE_CERTIFICATE.json"
FINAL_OUTPUT = HERE / "STRONG_CROSSBRIDGE_FINAL_CERTIFICATE.json"

SIGNED_PAIR_TARGETS = (108, 110, 113, 114, 116, 120, 128, 175, 178, 180, 181, 184)
CYCLIC_TARGETS = (107, 111, 117, 119, 177, 183, 189, 190, 191, 192)
RECORD43_TARGETS = (127,)
RECORD60_TARGETS = (174,)
RESIDUAL_TARGETS = tuple(
    sorted(SIGNED_PAIR_TARGETS + CYCLIC_TARGETS + RECORD43_TARGETS + RECORD60_TARGETS)
)

# The cyclic and record-43 paths are patched to their stable package names as
# soon as those independently running packages land.  Missing paths are an
# explicit BLOCKED state, never silently treated as evidence.
DEPENDENCY_PATHS = {
    "signed_pair": {
        "manifest": STRONG / "signed_pair_certificates/SIGNED_PAIR_CERTIFICATES.json",
        "verification": STRONG / "signed_pair_certificates/VERIFICATION_REPORT.json",
        "mutations": STRONG / "signed_pair_certificates/ADVERSARIAL_MUTATION_REPORT.json",
    },
    "cyclic": {
        "manifest": STRONG / "cyclic_certificates/THEOREM_MANIFEST.json",
        "core": STRONG / "cyclic_certificates/CYCLIC_SIX_MINOR_CERTIFICATES.json",
        "verification": STRONG / "cyclic_certificates/VERIFICATION_REPORT.json",
        "optimized_verification": STRONG / "cyclic_certificates/OPTIMIZED_VERIFICATION_REPORT.json",
        "checksums": STRONG / "cyclic_certificates/MANIFEST.sha256",
    },
    "record43": {
        "manifest": STRONG / "audit_simplex/RECORD43_CYCLIC_TRANSPORT_AUDIT.json",
        "verification_script": STRONG / "audit_simplex/verify_record43_cyclic_transport.py",
    },
    "record60": {
        "manifest": STRONG / "audit_simplex/RECORD60_CYCLIC_CERTIFICATE_AUDIT.json",
        "verification_script": STRONG / "audit_simplex/verify_record60_cyclic_certificate.py",
    },
}

PAIR_LIST = tuple(itertools.combinations(range(4), 2))
ASSIGNMENTS = tuple(
    prefix + (prefix[0] ^ prefix[1] ^ prefix[2],)
    for prefix in itertools.product(range(4), repeat=3)
)
ASSIGNMENT_INDEX = {assignment: index for index, assignment in enumerate(ASSIGNMENTS)}


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    answer = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1048576), b""):
            answer.update(block)
    return answer.hexdigest()


def relpath(path):
    return str(Path(path).resolve().relative_to(PROJECT))


def permute_mask(mask, order):
    value = 0
    for new_label, old_label in enumerate(order):
        if mask & (1 << old_label):
            value |= 1 << new_label
    return value


def character_on_mask(mask, assignment):
    answer = 0
    for label, character in enumerate(assignment):
        if mask & (1 << label):
            answer ^= character
    return answer


def inheritance_expansion(bits):
    result = {0: 1}
    for index, bit in enumerate(bits):
        updated = collections.defaultdict(int)
        for mask, coefficient in result.items():
            if bit:
                updated[mask | (1 << index)] += coefficient
            else:
                updated[mask] += coefficient
                updated[mask | (1 << index)] -= coefficient
        result = {mask: coefficient for mask, coefficient in updated.items() if coefficient}
    return tuple(sorted(result.items()))


def compile_descriptor(signatures, reticulation_count):
    switch_count = 1 << reticulation_count
    if any(len(row) != switch_count for row in signatures):
        raise AssertionError("signature switch count")
    expressions = []
    for assignment in ASSIGNMENTS:
        grouped = collections.defaultdict(lambda: collections.defaultdict(int))
        for switch_index in range(switch_count):
            bits = tuple(
                (switch_index >> (reticulation_count - 1 - j)) & 1
                for j in range(reticulation_count)
            )
            monomial = []
            for edge_index, signature in enumerate(signatures):
                character = character_on_mask(signature[switch_index], assignment)
                if character:
                    monomial.append((edge_index, character, 1))
            for inheritance_mask, coefficient in inheritance_expansion(bits):
                grouped[tuple(monomial)][inheritance_mask] += coefficient
        expression = []
        for monomial, polynomial in grouped.items():
            polynomial = tuple(
                sorted((mask, coefficient) for mask, coefficient in polynomial.items() if coefficient)
            )
            if polynomial:
                expression.append((monomial, polynomial))
        expressions.append(tuple(sorted(expression)))
    return {
        "k": 4,
        "retic_count": reticulation_count,
        "edge_class_count": len(signatures),
        "outputs": tuple(expressions),
    }


def sparse_outputs(descriptor):
    width = 3 * descriptor["edge_class_count"] + descriptor["retic_count"]
    result = []
    for expression in descriptor["outputs"]:
        polynomial = collections.defaultdict(int)
        for monomial, inheritance in expression:
            base = [0] * width
            for edge, character, exponent in monomial:
                base[3 * edge + character - 1] += exponent
            for mask, coefficient in inheritance:
                power = list(base)
                for index in range(descriptor["retic_count"]):
                    if mask & (1 << index):
                        power[3 * descriptor["edge_class_count"] + index] = 1
                polynomial[tuple(power)] += coefficient
        result.append({power: coefficient for power, coefficient in polynomial.items() if coefficient})
    return tuple(result)


def build_universe(primitive):
    directions = []
    displayed_count = 0
    raw_split_count = 0
    seen_keys = set()
    for record in primitive["one_active_wrong_split"]["records"]:
        record_id = int(record["id"])
        for split_record in record["splits"]:
            raw_split_count += 1
            first = tuple(int(value) for value in split_record["split"])
            if split_record["displayed_by_all"]:
                displayed_count += 1
                continue
            if len(first) != 2 or len(set(first)) != 2 or any(value not in range(4) for value in first):
                raise AssertionError((record_id, "invalid split", first))
            complement = tuple(sorted(set(range(4)) - set(first)))
            order = first + complement
            if tuple(sorted(order)) != (0, 1, 2, 3):
                raise AssertionError((record_id, "non-bijection", order))
            key = (record_id, tuple(sorted((tuple(sorted(first)), complement))))
            if key in seen_keys:
                raise AssertionError(("duplicate direction", key))
            seen_keys.add(key)
            signatures = tuple(
                tuple(permute_mask(int(mask), order) for mask in signature)
                for signature in record["signatures"]
            )
            descriptor = compile_descriptor(signatures, int(record["reticulation_count"]))
            directions.append(
                {
                    "target_index": len(directions),
                    "record_id": record_id,
                    "old_split": first,
                    "old_order": order,
                    "normalized_split": ((0, 1), (2, 3)),
                    "reticulation_count": int(record["reticulation_count"]),
                    "signatures": signatures,
                    "descriptor": descriptor,
                    "outputs": sparse_outputs(descriptor),
                    "direction_key": key,
                }
            )
    if len(directions) != 204 or raw_split_count != 216 or displayed_count != 12:
        raise AssertionError((len(directions), raw_split_count, displayed_count))
    if primitive["one_active_wrong_split"]["common_displayed_splits_skipped"] != 12:
        raise AssertionError("frozen displayed-split count")
    return tuple(directions), raw_split_count, displayed_count


def sparse_multiply(left, right):
    result = collections.defaultdict(int)
    for power_left, coefficient_left in left.items():
        for power_right, coefficient_right in right.items():
            power = tuple(a + b for a, b in zip(power_left, power_right))
            result[power] += coefficient_left * coefficient_right
    return {power: coefficient for power, coefficient in result.items() if coefficient}


def sparse_subtract(left, right):
    result = collections.defaultdict(int)
    result.update(left)
    for power, coefficient in right.items():
        result[power] -= coefficient
    return {power: coefficient for power, coefficient in result.items() if coefficient}


def minor(outputs, character_sum, rows, columns):
    r0, r1 = rows
    c0, c1 = columns
    indices = (
        ASSIGNMENT_INDEX[(r0, character_sum ^ r0, c0, character_sum ^ c0)],
        ASSIGNMENT_INDEX[(r1, character_sum ^ r1, c1, character_sum ^ c1)],
        ASSIGNMENT_INDEX[(r0, character_sum ^ r0, c1, character_sum ^ c1)],
        ASSIGNMENT_INDEX[(r1, character_sum ^ r1, c0, character_sum ^ c0)],
    )
    return sparse_subtract(
        sparse_multiply(outputs[indices[0]], outputs[indices[1]]),
        sparse_multiply(outputs[indices[2]], outputs[indices[3]]),
    ), indices


def factor_monomial(polynomial):
    width = len(next(iter(polynomial)))
    common = tuple(min(power[index] for power in polynomial) for index in range(width))
    result = collections.defaultdict(int)
    for power, coefficient in polynomial.items():
        result[tuple(power[index] - common[index] for index in range(width))] += coefficient
    return common, {power: coefficient for power, coefficient in result.items() if coefficient}


def polynomial_payload(polynomial):
    return [[list(power), str(coefficient)] for power, coefficient in sorted(polynomial.items())]


def polynomial_digest(polynomial):
    return digest(polynomial_payload(polynomial))


def exact_bernstein(polynomial):
    width = len(next(iter(polynomial)))
    active = tuple(
        index for index in range(width) if len({power[index] for power in polynomial}) > 1
    )
    projected = collections.defaultdict(int)
    for power, coefficient in polynomial.items():
        projected[tuple(power[index] for index in active)] += coefficient
    projected = {power: coefficient for power, coefficient in projected.items() if coefficient}
    degrees = tuple(max(power[index] for power in projected) for index in range(len(active)))
    if any(degree not in (1, 2) for degree in degrees):
        raise AssertionError(("unexpected Bernstein degree", degrees))
    ordered = []
    for beta in itertools.product(*(range(degree + 1) for degree in degrees)):
        value = fractions.Fraction(0)
        for alpha, coefficient in projected.items():
            if all(alpha[index] <= beta[index] for index in range(len(active))):
                multiplier = fractions.Fraction(1)
                for index, degree in enumerate(degrees):
                    multiplier *= fractions.Fraction(
                        math.comb(beta[index], alpha[index]),
                        math.comb(degree, alpha[index]),
                    )
                value += coefficient * multiplier
        ordered.append((beta, value))
    sign = 0
    values = tuple(value for _, value in ordered)
    if all(value >= 0 for value in values) and any(value > 0 for value in values):
        sign = 1
    elif all(value <= 0 for value in values) and any(value < 0 for value in values):
        sign = -1
    denominator_power = sum(degree == 2 for degree in degrees)
    scale = 1 << denominator_power
    numerators = []
    for value in values:
        scaled = value * scale
        if scaled.denominator != 1:
            raise AssertionError(("nonintegral common scale", degrees, value))
        numerators.append(scaled.numerator)
    coefficient_hash = hashlib.sha256()
    for numerator in numerators:
        coefficient_hash.update(struct.pack("<q", numerator))
    coefficient_hash.update(str(denominator_power).encode())
    return {
        "sign": sign,
        "active_parameter_indices": active,
        "degrees": degrees,
        "coefficient_count": len(numerators),
        "common_denominator": f"2^{denominator_power}",
        "negative": sum(value < 0 for value in numerators),
        "zero": sum(value == 0 for value in numerators),
        "positive": sum(value > 0 for value in numerators),
        "minimum_numerator": min(numerators),
        "maximum_numerator": max(numerators),
        "ordered_numerators_sha256": coefficient_hash.hexdigest(),
        "nonzero_coefficients": tuple(
            (beta, numerator)
            for (beta, _), numerator in zip(ordered, numerators)
            if numerator
        ),
    }


def compare_single_certificate(discovery_record, direction, source_sha):
    certificate = discovery_record["certificate"]
    if certificate is None:
        raise AssertionError((direction["target_index"], "missing certificate"))
    if discovery_record["target_index"] != direction["target_index"]:
        raise AssertionError("target index")
    if discovery_record["record_id"] != direction["record_id"]:
        raise AssertionError("record id")
    if discovery_record["old_split"] != list(direction["old_split"]):
        raise AssertionError("old split")
    if discovery_record["old_order"] != list(direction["old_order"]):
        raise AssertionError("old order")
    if discovery_record["reticulation_count"] != direction["reticulation_count"]:
        raise AssertionError("reticulation count")
    descriptor_hash = digest(direction["descriptor"])
    if discovery_record["descriptor_sha256"] != descriptor_hash:
        raise AssertionError((direction["target_index"], "descriptor hash"))
    if certificate["method"] != "exact full tensor Bernstein on the open unit cube":
        raise AssertionError((direction["target_index"], "method"))
    polynomial, coordinates = minor(
        direction["outputs"],
        int(certificate["character_sum"]),
        tuple(certificate["rows"]),
        tuple(certificate["columns"]),
    )
    common, reduced = factor_monomial(polynomial)
    bernstein = exact_bernstein(reduced)
    stored_bernstein = certificate["full_bernstein"]
    comparisons = {
        "active_parameter_indices": list(bernstein["active_parameter_indices"]),
        "degrees": list(bernstein["degrees"]),
        "coefficient_count": bernstein["coefficient_count"],
        "common_denominator": bernstein["common_denominator"],
        "negative": bernstein["negative"],
        "zero": bernstein["zero"],
        "positive": bernstein["positive"],
        "minimum_numerator": str(bernstein["minimum_numerator"]),
        "maximum_numerator": str(bernstein["maximum_numerator"]),
        "ordered_numerators_sha256": bernstein["ordered_numerators_sha256"],
        "sign": bernstein["sign"],
    }
    if stored_bernstein != comparisons:
        raise AssertionError((direction["target_index"], "Bernstein mismatch"))
    if certificate["coordinate_indices"] != list(coordinates):
        raise AssertionError((direction["target_index"], "coordinate indices"))
    if certificate["positive_monomial_exponent"] != list(common):
        raise AssertionError((direction["target_index"], "monomial factor"))
    if certificate["term_count"] != len(reduced):
        raise AssertionError((direction["target_index"], "term count"))
    if certificate["reduced_polynomial_sha256"] != polynomial_digest(reduced):
        raise AssertionError((direction["target_index"], "reduced polynomial hash"))
    if certificate["sign"] != bernstein["sign"] or bernstein["sign"] != 1:
        raise AssertionError((direction["target_index"], "strict sign"))
    if bernstein["negative"] != 0 or bernstein["positive"] == 0:
        raise AssertionError((direction["target_index"], "strict positivity"))
    return {
        "target_index": direction["target_index"],
        "record_id": direction["record_id"],
        "old_split": list(direction["old_split"]),
        "old_order": list(direction["old_order"]),
        "normalized_split": [[0, 1], [2, 3]],
        "reticulation_count": direction["reticulation_count"],
        "descriptor_sha256": descriptor_hash,
        "discovery_record_sha256": source_sha,
        "minor": {
            "character_sum": certificate["character_sum"],
            "rows": certificate["rows"],
            "columns": certificate["columns"],
            "coordinate_indices": list(coordinates),
            "full_polynomial_sha256": polynomial_digest(polynomial),
            "positive_monomial_exponent": list(common),
            "reduced_term_count": len(reduced),
            "reduced_polynomial_sha256": polynomial_digest(reduced),
            "reduced_polynomial": polynomial_payload(reduced),
        },
        "bernstein": {
            **comparisons,
            "nonzero_coefficients": [
                {"multi_index": list(beta), "numerator": numerator}
                for beta, numerator in bernstein["nonzero_coefficients"]
            ],
        },
        "conclusion": (
            "the selected Fourier-block 2x2 minor is strictly positive on the "
            "open edge-spectrum and inheritance cube"
        ),
    }


def json_status(path):
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def artifact_binding(path):
    return {"path": relpath(path), "sha256": sha_file(path)}


def bind_signed_pair():
    paths = DEPENDENCY_PATHS["signed_pair"]
    manifest = json_status(paths["manifest"])
    verification = json_status(paths["verification"])
    mutations = json_status(paths["mutations"])
    artifacts = [artifact_binding(path) for path in paths.values() if path.is_file()]
    passed = bool(
        manifest
        and verification
        and mutations
        and manifest.get("status") == "CERTIFIED_EXACT"
        and tuple(manifest.get("claim", {}).get("target_indices", ())) == SIGNED_PAIR_TARGETS
        and verification.get("status") == "PASS"
        and verification.get("manifest_sha256") == sha_file(paths["manifest"])
        and mutations.get("status") == "PASS"
        and mutations.get("all_mutations_rejected") is True
    )
    return {
        "name": "signed_pair",
        "required_targets": list(SIGNED_PAIR_TARGETS),
        "status": "PASS" if passed else "BLOCKED",
        "artifacts": artifacts,
        "reason": None if passed else "signed-pair manifest, independent replay, or mutations missing/failing",
    }


def bind_cyclic():
    paths = DEPENDENCY_PATHS["cyclic"]
    manifest = json_status(paths["manifest"])
    core = json_status(paths["core"])
    verification = json_status(paths["verification"])
    optimized = json_status(paths["optimized_verification"])
    artifacts = [artifact_binding(path) for path in paths.values() if path.is_file()]
    manifest_targets = tuple(manifest.get("scope", {}).get("target_indices", ())) if manifest else ()
    core_hash = sha_file(paths["core"]) if paths["core"].is_file() else None
    passed = bool(
        manifest
        and core
        and verification
        and optimized
        and manifest.get("schema") == "k3p-cyclic-six-minor-theorem-manifest-v1"
        and manifest.get("status") == "PASS"
        and manifest_targets == CYCLIC_TARGETS
        and core.get("schema") == "k3p-cyclic-six-minor-certificates-v1"
        and core.get("status") == "PASS"
        and tuple(core.get("target_indices", ())) == CYCLIC_TARGETS
        and verification.get("status") == "PASS"
        and optimized.get("status") == "PASS"
        and verification.get("artifact_sha256") == core_hash
        and optimized.get("artifact_sha256") == core_hash
        and verification.get("identity_count") == optimized.get("identity_count") == 30
        and verification.get("mutation_count") == optimized.get("mutation_count") == 40
        and all(row.get("result") == "REJECTED" for row in verification.get("mutations", ()))
        and all(row.get("result") == "REJECTED" for row in optimized.get("mutations", ()))
        and manifest.get("files", {}).get("CYCLIC_SIX_MINOR_CERTIFICATES.json") == core_hash
    )
    return {
        "name": "cyclic",
        "required_targets": list(CYCLIC_TARGETS),
        "status": "PASS" if passed else "BLOCKED",
        "artifacts": artifacts,
        "reason": None if passed else "ten-target cyclic manifest, independent replay, or mutations missing/failing",
    }


def bind_record_audit(name, target, record_id, expected_schema):
    paths = DEPENDENCY_PATHS[name]
    manifest = json_status(paths["manifest"])
    script = paths["verification_script"]
    artifacts = [artifact_binding(path) for path in paths.values() if path.is_file()]
    passed = bool(
        manifest
        and script.is_file()
        and manifest.get("status") == "PASS"
        and manifest.get("schema") == expected_schema
        and manifest.get("target_index") == target
        and manifest.get("record_id") == record_id
        and manifest.get("inputs", {}).get("audit_script_sha256") == sha_file(script)
        and manifest.get("mutation_tests")
        and all(row.get("result") == "REJECTED" for row in manifest["mutation_tests"])
    )
    return {
        "name": name,
        "required_targets": [target],
        "status": "PASS" if passed else "BLOCKED",
        "artifacts": artifacts,
        "reason": None if passed else f"target-{target} exact audit or mutation evidence missing/failing",
    }


def category(target_index, single_indices):
    memberships = []
    if target_index in single_indices:
        memberships.append("single_minor")
    if target_index in SIGNED_PAIR_TARGETS:
        memberships.append("signed_pair")
    if target_index in CYCLIC_TARGETS:
        memberships.append("cyclic")
    if target_index in RECORD43_TARGETS:
        memberships.append("record43")
    if target_index in RECORD60_TARGETS:
        memberships.append("record60")
    if len(memberships) != 1:
        raise AssertionError((target_index, memberships))
    return memberships[0]


def atomic_write(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main():
    primitive = json.loads(FROZEN.read_text())
    directions, raw_split_count, displayed_count = build_universe(primitive)
    discovery = json.loads(DISCOVERY.read_text())
    if discovery["target_directions"] != 204 or discovery["solved"] != 180:
        raise AssertionError("discovery count binding")
    if tuple(discovery["unsolved_target_indices"]) != RESIDUAL_TARGETS:
        raise AssertionError("discovery residual list")

    replay_records = []
    source_bindings = []
    single_indices = set()
    for direction in directions:
        target_index = direction["target_index"]
        source_path = DISCOVERY_RECORDS / f"{target_index:03d}.json"
        source_sha = sha_file(source_path)
        source_record = json.loads(source_path.read_text())
        source_bindings.append(
            {"target_index": target_index, "path": relpath(source_path), "sha256": source_sha}
        )
        if source_record["certificate"] is None:
            if target_index not in RESIDUAL_TARGETS:
                raise AssertionError((target_index, "unexpected missing certificate"))
            continue
        if target_index in RESIDUAL_TARGETS:
            raise AssertionError((target_index, "unexpected single certificate"))
        replay_records.append(compare_single_certificate(source_record, direction, source_sha))
        single_indices.add(target_index)
    if len(replay_records) != 180 or len(single_indices) != 180:
        raise AssertionError("single-minor replay count")

    producer_sha = sha_file(Path(__file__).resolve())
    single_payload = {
        "schema": "k3p-strong-crossbridge-single-minor-replay-v1",
        "status": "PASS",
        "inputs": {
            "frozen_primitive": relpath(FROZEN),
            "frozen_primitive_sha256": sha_file(FROZEN),
            "discovery_manifest": relpath(DISCOVERY),
            "discovery_manifest_sha256": sha_file(DISCOVERY),
            "discovery_record_tree_sha256": digest(source_bindings),
            "producer": relpath(Path(__file__).resolve()),
            "producer_sha256": producer_sha,
        },
        "independence": {
            "exploration_module_imported": False,
            "k3p_atlas_compiler_imported": False,
            "fourier_maps_rebuilt_from_frozen_switching_signatures": True,
            "bernstein_coefficients_recomputed_as_exact_fractions": True,
            "legacy_numpy_hash_replayed_with_explicit_little_endian_int64_packing": True,
        },
        "domain": (
            "the full strict unit cube in all edge Fourier spectra and inheritance "
            "parameters; therefore the K3P principal domain D3,+"
        ),
        "counts": {
            "target_universe": 204,
            "single_minor_certificates": 180,
            "residual_directions": 24,
        },
        "residual_target_indices": list(RESIDUAL_TARGETS),
        "source_record_bindings": source_bindings,
        "records": replay_records,
    }
    single_payload["records_sha256"] = digest(replay_records)
    atomic_write(SINGLE_OUTPUT, single_payload)

    universe_rows = []
    for direction in directions:
        universe_rows.append(
            {
                "target_index": direction["target_index"],
                "record_id": direction["record_id"],
                "old_split": list(direction["old_split"]),
                "old_order": list(direction["old_order"]),
                "old_to_normalized_port_map": [
                    direction["old_order"].index(old) for old in range(4)
                ],
                "normalized_split": [[0, 1], [2, 3]],
                "normalized_signatures_sha256": digest(direction["signatures"]),
                "descriptor_sha256": digest(direction["descriptor"]),
                "certificate_category": category(direction["target_index"], single_indices),
            }
        )
    universe_payload = {
        "schema": "k3p-strong-crossbridge-direction-universe-v1",
        "status": "PASS",
        "input": {"path": relpath(FROZEN), "sha256": sha_file(FROZEN)},
        "construction": {
            "primitive_record_count": len(primitive["one_active_wrong_split"]["records"]),
            "raw_split_entries": raw_split_count,
            "common_displayed_splits_removed": displayed_count,
            "wrong_split_directions": len(directions),
            "direction_key": "(primitive record id, unordered labelled 2|2 split)",
            "duplicate_direction_keys": 0,
            "normalization": (
                "the listed first split side is placed at ports 0,1 and its sorted "
                "complement at ports 2,3; the resulting map is a permutation"
            ),
            "normalized_split_for_every_direction": [[0, 1], [2, 3]],
        },
        "partition": {
            "single_minor": sorted(single_indices),
            "signed_pair": list(SIGNED_PAIR_TARGETS),
            "cyclic": list(CYCLIC_TARGETS),
            "record43": list(RECORD43_TARGETS),
            "record60": list(RECORD60_TARGETS),
            "counts": {"single_minor": 180, "signed_pair": 12, "cyclic": 10, "record43": 1, "record60": 1},
            "pairwise_disjoint": True,
            "union_is_all_204": True,
        },
        "automorphism_audit": {
            "used": False,
            "known_record60_dummy_label_bug": "SUPERSEDED",
            "reason": (
                "all 204 labelled directions are enumerated and certified directly; "
                "no automorphism orbit, dummy-label map, or transported representative "
                "is used for completeness"
            ),
        },
        "directions": universe_rows,
    }
    universe_payload["directions_sha256"] = digest(universe_rows)
    atomic_write(UNIVERSE_OUTPUT, universe_payload)

    dependencies = [
        {
            "name": "single_minor",
            "required_targets": sorted(single_indices),
            "status": "PASS",
            "artifacts": [artifact_binding(SINGLE_OUTPUT)],
            "reason": None,
        },
        bind_signed_pair(),
        bind_cyclic(),
        bind_record_audit(
            "record43", 127, 43, "k3p-record43-cyclic-transport-audit-v1"
        ),
        bind_record_audit(
            "record60", 174, 60, "k3p-record60-cyclic-nine-minor-audit-v1"
        ),
    ]
    all_pass = all(dependency["status"] == "PASS" for dependency in dependencies)
    final_payload = {
        "schema": "k3p-strong-crossbridge-final-certificate-v1",
        "status": "PASS" if all_pass else "BLOCKED",
        "claim_status": (
            "CERTIFIED: all 204 one-active wrong-split target directions exclude "
            "a swallowed source bridge on the strict K3P principal domain"
            if all_pass
            else "NOT YET CERTIFIED: one or more required child proof packages is missing or failing"
        ),
        "inputs": {
            "frozen_primitive": artifact_binding(FROZEN),
            "builder": artifact_binding(Path(__file__).resolve()),
            "single_minor_replay": artifact_binding(SINGLE_OUTPUT),
            "universe_certificate": artifact_binding(UNIVERSE_OUTPUT),
        },
        "coverage": {
            "target_directions": 204,
            "partition_counts": {"single_minor": 180, "signed_pair": 12, "cyclic": 10, "record43": 1, "record60": 1},
            "pairwise_disjoint": True,
            "union_is_all_204": True,
            "normalization_replayed": True,
            "automorphism_transport_used": False,
        },
        "dependencies": dependencies,
        "blocked_dependencies": [
            dependency["name"] for dependency in dependencies if dependency["status"] != "PASS"
        ],
        "logical_conclusion": (
            "For every graph-derived one-active wrong-split direction, at least one "
            "exact certificate contradicts the rank-one Fourier-block equations "
            "forced by a source bridge.  This implication is active only when status=PASS."
        ),
    }
    final_payload["dependencies_sha256"] = digest(dependencies)
    atomic_write(FINAL_OUTPUT, final_payload)
    print(
        json.dumps(
            {
                "status": final_payload["status"],
                "single_minor_replayed": len(replay_records),
                "universe": len(directions),
                "blocked_dependencies": final_payload["blocked_dependencies"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
