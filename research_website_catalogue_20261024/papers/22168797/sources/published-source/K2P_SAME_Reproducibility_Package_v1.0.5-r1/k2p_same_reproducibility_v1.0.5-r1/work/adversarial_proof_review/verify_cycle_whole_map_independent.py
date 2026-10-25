#!/usr/bin/env python3
"""Independent replay of the corrected cycle full-map T_i truth bundle.

This verifier does not import the cycle audit implementation.  It rebuilds
the Fourier pullbacks from the atlas, independently converts exact power-basis
polynomials to tensor Bernstein form, rediscovers replacement triples when a
legacy triple fails, and recomputes every ordered truth-row hash.
"""

from __future__ import annotations

import argparse
import collections
import fractions
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    StrictJSONError,
    decode_json_document,
    iter_canonical_gzip_jsonl,
)

ATLAS_PATH = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
CYCLE = PROJECT / "work/cycle_three_port_closure"
BASE_LEDGER = CYCLE / "artifacts/base_raw_ledger.jsonl.gz"
FULL_LEDGER = CYCLE / "artifacts/full_completion_ledger.jsonl.gz"
WITNESSES = CYCLE / "artifacts/topology_witnesses.json"
DEFAULT_CERTIFICATE = HERE / "cycle_tree_sunlet_full_map_certificate.json"
DEFAULT_REPORT = HERE / "cycle_tree_sunlet_independent_replay_certificate.json"


class ReplayFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ReplayFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sparse_hash(polynomial):
    return sha([[list(exponent), str(coefficient)] for exponent, coefficient in sorted(polynomial.items())])


def import_module(name, path):
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None, f"import:{path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def load_modules():
    atlas = import_module("cycle_independent_atlas", ATLAS_PATH)
    common = import_module("cycle_common", CYCLE / "cycle_common.py")
    generator = import_module("cycle_independent_generator", CYCLE / "generate_cycle_closure.py")
    return atlas, common, generator


def t_pullback(atlas, descriptor, outputs, triple, orientation):
    assignments = atlas.orbit_assignments(descriptor.k)
    lookup = {assignment: index for index, assignment in enumerate(assignments)}
    others = sorted(set(triple) - {orientation})
    order = (others[0], others[1], orientation)

    def output_at(characters):
        assignment = [0] * descriptor.k
        for label, character in zip(order, characters):
            assignment[label] = character
        coordinate = lookup[atlas.ct_orbit_rep(tuple(assignment))]
        return outputs[coordinate]

    v_value = output_at((1, 3, 2))
    x_s = output_at((1, 1, 0))
    x_g = output_at((2, 2, 0))
    y_g = output_at((2, 0, 2))
    z_g = output_at((0, 2, 2))
    return atlas.sparse_lincomb(
        [
            atlas.sparse_mul_many((v_value, v_value, x_g)),
            atlas.sparse_mul_many((x_s, x_s, y_g, z_g)),
        ],
        (1, -1),
    )


def negative_bernstein(polynomial):
    require(polynomial, "empty signed polynomial")
    parameter_count = len(next(iter(polynomial)))
    monomial = tuple(
        min(exponent[index] for exponent in polynomial)
        for index in range(parameter_count)
    )
    active = tuple(
        index
        for index in range(parameter_count)
        if len({exponent[index] - monomial[index] for exponent in polynomial}) > 1
    )
    residual = {
        tuple(exponent[index] - monomial[index] for index in active): fractions.Fraction(coefficient)
        for exponent, coefficient in polynomial.items()
    }
    degree = tuple(max(exponent[index] for exponent in residual) for index in range(len(active)))
    shape = tuple(value + 1 for value in degree)
    coefficient_count = math.prod(shape)
    require(coefficient_count <= 2_000_000, f"Bernstein tensor bound:{coefficient_count}")
    strides = tuple(math.prod(shape[index + 1 :]) for index in range(len(shape)))
    tensor = [fractions.Fraction(0)] * coefficient_count
    for exponent, coefficient in residual.items():
        tensor[sum(value * stride for value, stride in zip(exponent, strides))] = coefficient
    for axis, axis_degree in enumerate(degree):
        stride = strides[axis]
        outer_count = math.prod(shape[:axis])
        block_size = (axis_degree + 1) * stride
        denominators = tuple(math.comb(axis_degree, alpha) for alpha in range(axis_degree + 1))
        converted = [fractions.Fraction(0)] * coefficient_count
        for outer in range(outer_count):
            base = outer * block_size
            for inner in range(stride):
                power_values = tuple(
                    tensor[base + alpha * stride + inner]
                    for alpha in range(axis_degree + 1)
                )
                for beta in range(axis_degree + 1):
                    value = fractions.Fraction(0)
                    for alpha in range(beta + 1):
                        if power_values[alpha]:
                            value += power_values[alpha] * fractions.Fraction(
                                math.comb(beta, alpha), denominators[alpha]
                            )
                    converted[base + beta * stride + inner] = value
        tensor = converted
    signs = collections.Counter(-1 if value < 0 else 1 if value > 0 else 0 for value in tensor)
    require(signs[1] == 0 and signs[-1] > 0, f"not Bernstein-strict-negative:{signs}")
    result = {
        "method": "exact_tensor_Bernstein_after_positive_monomial",
        "parameter_count": parameter_count,
        "positive_monomial_exponent": list(monomial),
        "active_parameter_indices": list(active),
        "Bernstein_multidegree": list(degree),
        "Bernstein_coefficient_count": coefficient_count,
        "negative_coefficients": signs[-1],
        "zero_coefficients": signs[0],
        "positive_coefficients": signs[1],
        "minimum_coefficient": str(min(tensor)),
        "maximum_coefficient": str(max(tensor)),
        "domain": (
            "the full open unit cube in edge-sector and inheritance variables; "
            "therefore also its physical D_plus subset"
        ),
        "conclusion": "strictly_negative",
    }
    result["certificate_sha256"] = sha(result)
    return result


def signed_certificate(polynomial):
    try:
        return "negative", polynomial, negative_bernstein(polynomial)
    except ReplayFailure:
        negated = {exponent: -coefficient for exponent, coefficient in polynomial.items()}
        return "positive", negated, negative_bernstein(negated)


def choose_separator(rows):
    choices = []
    for orientation, source_polynomial, target_polynomial in rows:
        if not source_polynomial and target_polynomial:
            signed_side, polynomial = "target", target_polynomial
        elif not target_polynomial and source_polynomial:
            signed_side, polynomial = "source", source_polynomial
        else:
            continue
        try:
            sign_name, normalized, sign = signed_certificate(polynomial)
        except ReplayFailure:
            continue
        choices.append((
            len(polynomial), orientation, signed_side, sign_name, sign,
            normalized, source_polynomial, target_polynomial,
        ))
    return min(choices, key=lambda row: (row[0], row[1], row[2])) if choices else None


def compile_polynomials(atlas, graph, triple):
    descriptor = atlas.model_descriptor_fast2(graph)
    outputs = atlas.output_sparse_polynomials(descriptor)
    return descriptor, {
        orientation: t_pullback(atlas, descriptor, outputs, triple, orientation)
        for orientation in triple
    }


def discover_separator(atlas, source_graph, target_graph):
    source_descriptor = atlas.model_descriptor_fast2(source_graph)
    target_descriptor = atlas.model_descriptor_fast2(target_graph)
    require(source_descriptor.k == target_descriptor.k, "port count mismatch")
    source_outputs = atlas.output_sparse_polynomials(source_descriptor)
    target_outputs = atlas.output_sparse_polynomials(target_descriptor)
    choices = []
    for triple in itertools.combinations(range(source_descriptor.k), 3):
        separator = choose_separator([
            (
                orientation,
                t_pullback(atlas, source_descriptor, source_outputs, triple, orientation),
                t_pullback(atlas, target_descriptor, target_outputs, triple, orientation),
            )
            for orientation in triple
        ])
        if separator is not None:
            choices.append((separator[0], triple, separator))
    require(choices, "no full-map T_i separator")
    _, triple, separator = min(
        choices, key=lambda row: (row[0], row[1], row[2][1], row[2][2])
    )
    return triple, separator, source_descriptor, target_descriptor


def invariant_certificate(atlas, k, triple, orientation):
    assignments = atlas.orbit_assignments(k)
    lookup = {assignment: index for index, assignment in enumerate(assignments)}
    others = sorted(set(triple) - {orientation})
    order = (others[0], others[1], orientation)

    def coordinate(characters):
        assignment = [0] * k
        for label, character in zip(order, characters):
            assignment[label] = character
        return lookup[atlas.ct_orbit_rep(tuple(assignment))]

    coordinates = {
        "V": coordinate((1, 3, 2)),
        "X_s": coordinate((1, 1, 0)),
        "X_g": coordinate((2, 2, 0)),
        "Y_g": coordinate((2, 0, 2)),
        "Z_g": coordinate((0, 2, 2)),
    }
    weights = atlas.coordinate_weights(k)

    def sum_weights(indices):
        return [sum(weights[index][axis] for index in indices) for axis in range(2 * k)]

    left = sum_weights((coordinates["V"], coordinates["V"], coordinates["X_g"]))
    right = sum_weights((
        coordinates["X_s"], coordinates["X_s"], coordinates["Y_g"], coordinates["Z_g"]
    ))
    require(left == right, f"bridge multihomogeneity:{k}:{triple}:{orientation}")
    result = {
        "port_count": k,
        "triple": list(triple),
        "orientation_label": orientation,
        "coordinate_indices": coordinates,
        "left_coordinate_monomial": [coordinates["V"], coordinates["V"], coordinates["X_g"]],
        "right_coordinate_monomial": [
            coordinates["X_s"], coordinates["X_s"], coordinates["Y_g"], coordinates["Z_g"]
        ],
        "common_boundary_incidence_multidegree": left,
        "triple_local_sector_degrees": {
            str(label): left[2 * label : 2 * label + 2] for label in triple
        },
        "identity": "T_i=V^2*X_g-X_s^2*Y_g*Z_g",
        "conclusion": "invariant survives every two-sector bridge incidence scaling",
    }
    result["certificate_sha256"] = sha(result)
    return result


def register(registry, presentations, family, presentation, polynomial, normalized, sign_name, sign):
    digest = sparse_hash(polynomial)
    record = {
        "pullback_sha256": digest,
        "pullback_term_count": len(polynomial),
        "strict_sign": sign_name,
        "normalized_negative_pullback_sha256": sparse_hash(normalized),
        "sign": sign,
    }
    require(digest not in registry or registry[digest] == record, f"sign hash collision:{digest}")
    registry[digest] = record
    presentations[digest].add((family, *presentation))
    return digest


def validate_claim_structure(claimed):
    require(claimed.get("schema") == "k2p-cycle-tree-sunlet-whole-map-truth-v1", "schema")
    require(claimed.get("status") == "PASS", "status")
    require(claimed.get("unresolved") == claimed.get("incoherent") == 0, "terminal status")
    expected = {"cycle_base": 7452, "cycle_full_equal_topology": 300}
    for family, count in expected.items():
        report = claimed["families"][family]
        require(report["input_rows"] == count, f"input rows:{family}")
        require(report["direct_full_map_zero_sign_rows"] == count, f"certified rows:{family}")
        require(report["exact_full_graph_relation_census"] == {"none": count}, f"relations:{family}")
        require(report["false_iso_or_triangle_conflicts"] == 0, f"conflicts:{family}")
        require(report["reopened_obligations"] == 0, f"reopened:{family}")
        hashes = report["ordered_truth_row_hashes"]
        require(len(hashes) == count, f"truth coverage:{family}")
        require(report["ordered_truth_row_hash_root"] == sha(hashes), f"truth root:{family}")
    repairs = claimed["revoked_legacy_witness_repairs"]
    require(claimed["revoked_legacy_witness_count"] == len(repairs) == 24, "repair census")
    require(len({row["raw_id"] for row in repairs}) == 24, "repair raw uniqueness")
    for row in repairs:
        require(row["legacy_triple"] == [0, 1, 3], f"repair legacy triple:{row['raw_id']}")
        require(row["replacement_full_map_triple"] == [0, 3, 4], f"repair triple:{row['raw_id']}")
        require(row["replacement_orientation"] in (0, 3), f"repair orientation:{row['raw_id']}")
        require(row["replacement_signed_side"] == "target", f"repair side:{row['raw_id']}")
    require(len(claimed["sign_certificates"]) == 92, "sign polynomial census")
    for digest, record in claimed["sign_certificates"].items():
        require(record["pullback_sha256"] == digest, f"sign digest key:{digest}")
        sign = record["sign"]
        sign_unhashed = dict(sign)
        sign_payload = sign_unhashed.pop("certificate_sha256", None)
        require(sign_payload == sha(sign_unhashed), f"sign payload:{digest}")
        require(sign["positive_coefficients"] == 0 and sign["negative_coefficients"] > 0, f"strict sign:{digest}")
        require(
            sign["negative_coefficients"] + sign["zero_coefficients"]
            == sign["Bernstein_coefficient_count"],
            f"Bernstein census:{digest}",
        )
        require(
            sign["domain"]
            == "the full open unit cube in edge-sector and inheritance variables; therefore also its physical D_plus subset",
            f"sign domain:{digest}",
        )
    require(len(claimed["coordinate_invariant_certificates"]) == 12, "invariant census")
    for key, record in claimed["coordinate_invariant_certificates"].items():
        unhashed = dict(record)
        payload = unhashed.pop("certificate_sha256", None)
        require(payload == sha(unhashed), f"invariant payload:{key}")
        k, triple, orientation = record["port_count"], record["triple"], record["orientation_label"]
        degrees = record["common_boundary_incidence_multidegree"]
        require(len(degrees) == 2 * k, f"invariant degree length:{key}")
        expected_degrees = [0] * (2 * k)
        for label in triple:
            expected_degrees[2 * label : 2 * label + 2] = [0, 2] if label == orientation else [2, 1]
        require(degrees == expected_degrees, f"invariant multidegree:{key}")
        require(
            record["triple_local_sector_degrees"]
            == {str(label): expected_degrees[2 * label : 2 * label + 2] for label in triple},
            f"local sector degrees:{key}",
        )


def main():
    if not __debug__:
        raise ReplayFailure("CYCLE_WHOLE_MAP_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--structure-only", action="store_true")
    arguments = parser.parse_args()
    started = time.monotonic()
    claimed = decode_json_document(
        arguments.certificate.read_bytes(),
        label=arguments.certificate.name,
        require_object=True,
    )
    unhashed = dict(claimed)
    claimed_payload = unhashed.pop("payload_sha256", None)
    require(claimed_payload == sha(unhashed), "certificate payload")
    validate_claim_structure(claimed)
    require(claimed["inputs"]["atlas_sha256"] == sha_file(ATLAS_PATH), "atlas binding")
    require(claimed["inputs"]["base_ledger_sha256"] == sha_file(BASE_LEDGER), "base binding")
    require(claimed["inputs"]["full_ledger_sha256"] == sha_file(FULL_LEDGER), "full binding")
    require(claimed["inputs"]["topology_witnesses_sha256"] == sha_file(WITNESSES), "witness binding")
    if arguments.structure_only:
        result = {
            "schema": "k2p-cycle-whole-map-structure-preflight-v1",
            "status": "PASS",
            "source_certificate_sha256": sha_file(arguments.certificate),
            "source_certificate_payload_sha256": claimed_payload,
            "base_rows": 7452,
            "full_rows": 300,
            "repairs": 24,
            "unresolved": 0,
        }
        result["payload_sha256"] = sha(result)
        arguments.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps(result, sort_keys=True))
        return

    atlas, common, generator = load_modules()
    sources = tuple(atlas.source_supports(("cycle",)))
    targets = tuple(atlas.target_completions(3, True) + atlas.target_completions(3, False))
    permutations = tuple(itertools.permutations(range(3)))
    require((len(sources), len(targets), len(permutations)) == (2, 1120, 6), "primitive census")
    witness_table = decode_json_document(
        WITNESSES.read_bytes(), label=WITNESSES.name, require_object=True
    )["witnesses"]
    base_rows = [
        row
        for row in iter_canonical_gzip_jsonl(BASE_LEDGER, label=BASE_LEDGER.name)
        if row.get("category") == "tree_sunlet_pointwise_excluded"
    ]
    full_rows = [
        row
        for row in iter_canonical_gzip_jsonl(FULL_LEDGER, label=FULL_LEDGER.name)
        if row.get("category") == "tree_sunlet_pointwise_excluded"
    ]
    require(len(base_rows) == 7452 and len(full_rows) == 300, "row census")

    sign_registry = {}
    presentations = collections.defaultdict(set)
    relation_counts = {"cycle_base": collections.Counter(), "cycle_full_equal_topology": collections.Counter()}
    side_counts = {"cycle_base": collections.Counter(), "cycle_full_equal_topology": collections.Counter()}
    class_counts = {"cycle_base": collections.Counter(), "cycle_full_equal_topology": collections.Counter()}
    truth_hashes = {"cycle_base": [], "cycle_full_equal_topology": []}
    invariant_registry = {}
    repairs = []

    base_source_polynomials = {
        index: compile_polynomials(atlas, source.graph, (0, 1, 2))[1]
        for index, source in enumerate(sources)
    }
    target_cache = {}
    prepared_sources = [atlas.prepare_mixed_source(source.graph) for source in sources]
    for row in base_rows:
        target_index = row["target_index"]
        if target_index not in target_cache:
            target_cache[target_index] = compile_polynomials(
                atlas, targets[target_index].graph, (0, 1, 2)
            )[1]
        permutation = tuple(row["port_permutation"])
        selected = atlas.selected_graph_from_completion(atlas.relabel_record(targets[target_index], permutation))
        relation = atlas.mixed_relation_exact_prepared(prepared_sources[row["source_index"]], selected)
        require(relation == "none", f"base exact relation:{row['raw_id']}:{relation}")
        relation_counts["cycle_base"][relation] += 1
        separator = choose_separator([
            (
                permutation[orientation],
                base_source_polynomials[row["source_index"]][permutation[orientation]],
                target_cache[target_index][orientation],
            )
            for orientation in (0, 1, 2)
        ])
        require(separator is not None, f"base separator:{row['raw_id']}")
        _, orientation, signed_side, sign_name, sign, normalized, source_poly, target_poly = separator
        signed_poly = source_poly if signed_side == "source" else target_poly
        digest = register(
            sign_registry, presentations, "cycle_base",
            (row["source_index"], target_index, row["permutation_index"], orientation, signed_side),
            signed_poly, normalized, sign_name, sign,
        )
        invariant_key = f"k3:t012:i{orientation}"
        invariant_registry.setdefault(
            invariant_key, invariant_certificate(atlas, 3, (0, 1, 2), orientation)
        )
        source_digest, target_digest = sparse_hash(source_poly), sparse_hash(target_poly)
        side_counts["cycle_base"][signed_side] += 1
        class_counts["cycle_base"][(source_digest, target_digest)] += 1
        truth = {
            "raw_id": row["raw_id"], "source_index": row["source_index"],
            "target_index": target_index, "permutation_index": row["permutation_index"],
            "chosen_T_orientation_label": orientation,
            "source_pullback_sha256": source_digest, "target_pullback_sha256": target_digest,
            "signed_pullback_sha256": digest, "strict_sign": sign_name,
            "exact_full_graph_relation": "none",
            "result": (
                f"strict_source_{sign_name}_target_zero" if signed_side == "source"
                else f"source_zero_strict_target_{sign_name}"
            ),
        }
        truth_hashes["cycle_base"].append(sha(truth))

    configurations = generator.build_source_configurations(atlas, sources)
    configuration_index = {
        (source_index, depth, tuple(item["placement_path"])): item
        for (source_index, depth), items in configurations.items() for item in items
    }
    source_poly_cache = {}
    target_poly_cache = {}
    discovery_cache = {}
    for ordinal, row in enumerate(full_rows):
        legacy_triple = tuple(witness_table[row["certificate_id"]]["triple"])
        depth = len(row["dummy_roles_in_label_order"])
        source_key = (row["source_index"], depth, tuple(row["source_placement_path"]))
        target_key = (row["target_index"], row["permutation_index"], tuple(row["dummy_roles_in_label_order"]))
        source_graph = configuration_index[source_key]["graph"]
        target_graph = common.relabel_and_promote_all(
            atlas, targets[row["target_index"]], permutations[row["permutation_index"]],
            tuple(row["dummy_roles_in_label_order"]),
        )
        source_map_key = (source_key, legacy_triple)
        target_map_key = (target_key, legacy_triple)
        if source_map_key not in source_poly_cache:
            source_poly_cache[source_map_key] = compile_polynomials(atlas, source_graph, legacy_triple)[1]
        if target_map_key not in target_poly_cache:
            target_poly_cache[target_map_key] = compile_polynomials(atlas, target_graph, legacy_triple)[1]
        relation = atlas.mixed_relation_exact(source_graph, target_graph)
        require(relation == "none", f"full exact relation:{row['raw_id']}:{relation}")
        relation_counts["cycle_full_equal_topology"][relation] += 1
        separator = choose_separator([
            (orientation, source_poly_cache[source_map_key][orientation], target_poly_cache[target_map_key][orientation])
            for orientation in legacy_triple
        ])
        certified_triple = legacy_triple
        if separator is None:
            source_descriptor = atlas.model_descriptor_fast2(source_graph)
            target_descriptor = atlas.model_descriptor_fast2(target_graph)
            discovery_key = (source_descriptor, target_descriptor)
            if discovery_key not in discovery_cache:
                discovery_cache[discovery_key] = discover_separator(atlas, source_graph, target_graph)
            certified_triple, separator, _, _ = discovery_cache[discovery_key]
            repairs.append({
                "raw_id": row["raw_id"], "root_id": row["root_id"],
                "legacy_triple": list(legacy_triple),
                "replacement_full_map_triple": list(certified_triple),
                "replacement_orientation": separator[1],
                "replacement_signed_side": separator[2],
            })
        _, orientation, signed_side, sign_name, sign, normalized, source_poly, target_poly = separator
        signed_poly = source_poly if signed_side == "source" else target_poly
        digest = register(
            sign_registry, presentations, "cycle_full_equal_topology",
            (row["raw_id"], row["root_id"], orientation, signed_side),
            signed_poly, normalized, sign_name, sign,
        )
        invariant_key = f"k{row['port_count']}:t{''.join(map(str, certified_triple))}:i{orientation}"
        invariant_registry.setdefault(
            invariant_key, invariant_certificate(
                atlas, row["port_count"], certified_triple, orientation
            )
        )
        source_digest, target_digest = sparse_hash(source_poly), sparse_hash(target_poly)
        side_counts["cycle_full_equal_topology"][signed_side] += 1
        class_counts["cycle_full_equal_topology"][(source_digest, target_digest)] += 1
        truth = {
            "raw_id": row["raw_id"], "root_id": row["root_id"],
            "base_raw_id": row["base_raw_id"], "port_count": row["port_count"],
            "source_placement_path": row["source_placement_path"],
            "legacy_witness_triple": list(legacy_triple),
            "certified_full_map_triple": list(certified_triple),
            "chosen_T_orientation_label": orientation,
            "source_pullback_sha256": source_digest, "target_pullback_sha256": target_digest,
            "signed_pullback_sha256": digest, "strict_sign": sign_name,
            "exact_full_graph_relation": "none",
            "result": (
                f"strict_source_{sign_name}_target_zero" if signed_side == "source"
                else f"source_zero_strict_target_{sign_name}"
            ),
        }
        truth_hashes["cycle_full_equal_topology"].append(sha(truth))
        if (ordinal + 1) % 100 == 0:
            print(json.dumps({"event": "independent_full_progress", "processed": ordinal + 1}), flush=True)

    rebuilt_sign_records = {}
    for digest, record in sign_registry.items():
        rebuilt_sign_records[digest] = {
            **record,
            "presentations": [list(item) for item in sorted(presentations[digest], key=repr)],
        }
    require(rebuilt_sign_records == claimed["sign_certificates"], "sign certificate bundle mismatch")
    require(invariant_registry == claimed["coordinate_invariant_certificates"], "invariant bundle mismatch")
    require(repairs == claimed["revoked_legacy_witness_repairs"], "legacy repair ledger mismatch")
    require(len(repairs) == 24, f"repair census:{len(repairs)}")

    for family, expected_count in (("cycle_base", 7452), ("cycle_full_equal_topology", 300)):
        report = claimed["families"][family]
        require(truth_hashes[family] == report["ordered_truth_row_hashes"], f"truth rows:{family}")
        require(sha(truth_hashes[family]) == report["ordered_truth_row_hash_root"], f"truth root:{family}")
        require(dict(relation_counts[family]) == report["exact_full_graph_relation_census"], f"relations:{family}")
        require(dict(side_counts[family]) == report["signed_side_census"], f"signed sides:{family}")
        expected_classes = {
            f"{source}:{target}": count for (source, target), count in sorted(class_counts[family].items())
        }
        require(expected_classes == report["polynomial_relation_class_multiplicities"], f"class multiplicities:{family}")
        require(len(truth_hashes[family]) == expected_count, f"coverage:{family}")

    result = {
        "schema": "k2p-cycle-whole-map-independent-replay-v1",
        "status": "PASS",
        "source_certificate_sha256": sha_file(arguments.certificate),
        "source_certificate_payload_sha256": claimed_payload,
        "base_rows_replayed": len(truth_hashes["cycle_base"]),
        "full_rows_replayed": len(truth_hashes["cycle_full_equal_topology"]),
        "legacy_witness_repairs_replayed": len(repairs),
        "sign_polynomials_replayed": len(rebuilt_sign_records),
        "bridge_multihomogeneous_invariants_replayed": len(invariant_registry),
        "unresolved": 0,
        "incoherent": 0,
    }
    result["payload_sha256"] = sha(result)
    arguments.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (
        ReplayFailure,
        StrictJSONError,
        KeyError,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
        raise SystemExit(f"CYCLE_WHOLE_MAP_REPLAY_FAIL:{exc}") from exc
