#!/usr/bin/env python3
"""Whole-map truth audit for both legacy cycle tree/sunlet families.

The rooted restriction oracle is used only to recover its claimed labelled
triple.  Every accepted row is instead certified directly on the original
K2P Fourier maps by a transported T_i identity: one pullback is exactly zero
and the other has an exact strict tensor-Bernstein sign on the open unit cube.
"""

from __future__ import annotations

import collections
import importlib.util
import itertools
import json
import sys
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

CORE_PATH = HERE / "audit_raw4_tree_sunlet_full_map.py"
CYCLE_DIR = PROJECT / "work/cycle_three_port_closure"
BASE_LEDGER = CYCLE_DIR / "artifacts/base_raw_ledger.jsonl.gz"
FULL_LEDGER = CYCLE_DIR / "artifacts/full_completion_ledger.jsonl.gz"
WITNESSES = CYCLE_DIR / "artifacts/topology_witnesses.json"
OUTPUT = HERE / "cycle_tree_sunlet_full_map_certificate.json"


def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_modules():
    core = import_path("cycle_truth_full_map_core", CORE_PATH)
    # The generator uses a plain local import.  Bind that exact source under
    # its expected module name without importing any retained descriptor data.
    common = import_path("cycle_common", CYCLE_DIR / "cycle_common.py")
    generator = import_path(
        "cycle_truth_original_generator", CYCLE_DIR / "generate_cycle_closure.py"
    )
    return core, common, generator


def strict_sign(core, polynomial):
    try:
        certificate = core.bernstein_sign_certificate(polynomial)
        return "negative", certificate, polynomial
    except core.TruthFailure:
        negated = {exponent: -coefficient for exponent, coefficient in polynomial.items()}
        certificate = core.bernstein_sign_certificate(negated)
        return "positive", certificate, negated


def choose_zero_sign(core, aligned):
    """Choose the shortest exact orientation with one zero and one strict sign.

    ``aligned`` rows are (reported_orientation, source_poly, target_poly).
    """
    candidates = []
    failures = []
    for orientation, source_polynomial, target_polynomial in aligned:
        if not source_polynomial and target_polynomial:
            signed_side, signed_polynomial = "target", target_polynomial
        elif not target_polynomial and source_polynomial:
            signed_side, signed_polynomial = "source", source_polynomial
        else:
            failures.append(
                {
                    "orientation": orientation,
                    "source_terms": len(source_polynomial),
                    "target_terms": len(target_polynomial),
                }
            )
            continue
        try:
            sign_name, sign_certificate, normalized = strict_sign(
                core, signed_polynomial
            )
        except core.TruthFailure as exc:
            failures.append(
                {
                    "orientation": orientation,
                    "source_terms": len(source_polynomial),
                    "target_terms": len(target_polynomial),
                    "sign_failure": str(exc),
                }
            )
            continue
        candidates.append(
            (
                len(signed_polynomial),
                orientation,
                signed_side,
                sign_name,
                sign_certificate,
                normalized,
                source_polynomial,
                target_polynomial,
            )
        )
    if not candidates:
        return None, failures
    return sorted(candidates, key=lambda row: (row[0], row[1], row[2]))[0], failures


def register_sign(core, registry, presentations, polynomial, normalized, sign_name, sign):
    digest = core.sparse_hash(polynomial)
    normalized_digest = core.sparse_hash(normalized)
    previous = registry.setdefault(
        digest,
        {
            "pullback_sha256": digest,
            "pullback_term_count": len(polynomial),
            "strict_sign": sign_name,
            "normalized_negative_pullback_sha256": normalized_digest,
            "sign": sign,
            "presentations": [],
        },
    )
    core.require(
        previous["strict_sign"] == sign_name
        and previous["normalized_negative_pullback_sha256"] == normalized_digest
        and previous["sign"] == sign,
        "cycle sign polynomial hash collision",
    )
    presentations[digest].add(presentations.current)
    return digest


class PresentationRegistry(collections.defaultdict):
    def __init__(self):
        super().__init__(set)
        self.current = None


def graph_descriptor_polynomials(atlas, core, graph, triple):
    descriptor = atlas.model_descriptor_fast2(graph)
    outputs = atlas.output_sparse_polynomials(descriptor)
    return descriptor, {
        orientation: core.t_pullback(atlas, descriptor, outputs, triple, orientation)
        for orientation in triple
    }


def coordinate_invariant_certificate(atlas, core, k, triple, orientation):
    """Bind T_i itself and verify its bridge-incidence multihomogeneity."""
    assignments = atlas.orbit_assignments(k)
    index = {assignment: number for number, assignment in enumerate(assignments)}
    other = sorted(set(triple) - {orientation})
    order = (other[0], other[1], orientation)

    def coordinate(values):
        row = [0] * k
        for label, value in zip(order, values):
            row[label] = value
        return index[atlas.ct_orbit_rep(tuple(row))]

    coordinates = {
        "V": coordinate((1, 3, 2)),
        "X_s": coordinate((1, 1, 0)),
        "X_g": coordinate((2, 2, 0)),
        "Y_g": coordinate((2, 0, 2)),
        "Z_g": coordinate((0, 2, 2)),
    }
    weights = atlas.coordinate_weights(k)

    def total(indices):
        return [sum(weights[index][axis] for index in indices) for axis in range(2 * k)]

    left = total((coordinates["V"], coordinates["V"], coordinates["X_g"]))
    right = total(
        (
            coordinates["X_s"],
            coordinates["X_s"],
            coordinates["Y_g"],
            coordinates["Z_g"],
        )
    )
    core.require(left == right, f"T_i bridge multihomogeneity failure:{k}:{triple}:{orientation}")
    certificate = {
        "port_count": k,
        "triple": list(triple),
        "orientation_label": orientation,
        "coordinate_indices": coordinates,
        "left_coordinate_monomial": [
            coordinates["V"],
            coordinates["V"],
            coordinates["X_g"],
        ],
        "right_coordinate_monomial": [
            coordinates["X_s"],
            coordinates["X_s"],
            coordinates["Y_g"],
            coordinates["Z_g"],
        ],
        "common_boundary_incidence_multidegree": left,
        "triple_local_sector_degrees": {
            str(label): left[2 * label : 2 * label + 2] for label in triple
        },
        "identity": "T_i=V^2*X_g-X_s^2*Y_g*Z_g",
        "conclusion": "invariant survives every two-sector bridge incidence scaling",
    }
    certificate["certificate_sha256"] = core.sha(certificate)
    return certificate


def search_all_triples(atlas, core, source_graph, target_graph):
    """Fail-closed repair for a revoked legacy triple on the same full maps."""
    source_descriptor = atlas.model_descriptor_fast2(source_graph)
    target_descriptor = atlas.model_descriptor_fast2(target_graph)
    core.require(source_descriptor.k == target_descriptor.k, "cycle full port-count drift")
    source_outputs = atlas.output_sparse_polynomials(source_descriptor)
    target_outputs = atlas.output_sparse_polynomials(target_descriptor)
    choices = []
    failure_rows = []
    for triple in itertools.combinations(range(source_descriptor.k), 3):
        aligned = []
        for orientation in triple:
            aligned.append(
                (
                    orientation,
                    core.t_pullback(
                        atlas,
                        source_descriptor,
                        source_outputs,
                        triple,
                        orientation,
                    ),
                    core.t_pullback(
                        atlas,
                        target_descriptor,
                        target_outputs,
                        triple,
                        orientation,
                    ),
                )
            )
        choice, failures = choose_zero_sign(core, aligned)
        if choice is not None:
            choices.append((choice[0], triple, choice))
        else:
            failure_rows.append({"triple": list(triple), "orientations": failures})
    if not choices:
        return None, failure_rows, source_descriptor, target_descriptor
    _, triple, choice = sorted(
        choices, key=lambda row: (row[0], row[1], row[2][1], row[2][2])
    )[0]
    return (triple, choice), failure_rows, source_descriptor, target_descriptor


def main():
    core, common, generator = load_modules()
    atlas = core.load_atlas()
    sources = tuple(atlas.source_supports(("cycle",)))
    targets = tuple(
        atlas.target_completions(3, True) + atlas.target_completions(3, False)
    )
    permutations = tuple(itertools.permutations(range(3)))
    core.require(
        (len(sources), len(targets), len(permutations)) == (2, 1120, 6),
        "cycle primitive census",
    )
    witness_payload = decode_json_document(
        WITNESSES.read_bytes(), label=WITNESSES.name, require_object=True
    )
    witnesses = witness_payload["witnesses"]

    base_rows = []
    for row in iter_canonical_gzip_jsonl(BASE_LEDGER, label=BASE_LEDGER.name):
        if row["category"] == "tree_sunlet_pointwise_excluded":
            base_rows.append(row)
    full_rows = []
    for row in iter_canonical_gzip_jsonl(FULL_LEDGER, label=FULL_LEDGER.name):
        if row["category"] == "tree_sunlet_pointwise_excluded":
            full_rows.append(row)
    core.require(len(base_rows) == 7452, f"cycle base sign census:{len(base_rows)}")
    core.require(len(full_rows) == 300, f"cycle full sign census:{len(full_rows)}")

    sign_certificates = {}
    presentations = PresentationRegistry()
    exact_relations = {
        "cycle_base": collections.Counter(),
        "cycle_full_equal_topology": collections.Counter(),
    }
    signed_sides = {
        "cycle_base": collections.Counter(),
        "cycle_full_equal_topology": collections.Counter(),
    }
    row_hashes = {"cycle_base": [], "cycle_full_equal_topology": []}
    relation_classes = {
        "cycle_base": collections.Counter(),
        "cycle_full_equal_topology": collections.Counter(),
    }
    coordinate_invariant_certificates = {}
    unresolved = []
    conflicts = []
    revoked_legacy_witness_repairs = []
    all_triple_repair_cache = {}

    # Base maps: compile each source and each unpermuted target once.  The
    # target triple/orientation is transported through old->new permutation.
    source_base = {}
    for source_index, source in enumerate(sources):
        triple = (0, 1, 2)
        _, source_base[source_index] = graph_descriptor_polynomials(
            atlas, core, source.graph, triple
        )
    target_base = {}
    prepared_sources = [atlas.prepare_mixed_source(source.graph) for source in sources]
    for row in base_rows:
        witness = witnesses[row["certificate_id"]]
        triple = tuple(witness["triple"])
        core.require(triple == (0, 1, 2), "cycle base witness triple drift")
        target_index = row["target_index"]
        if target_index not in target_base:
            _, target_base[target_index] = graph_descriptor_polynomials(
                atlas, core, targets[target_index].graph, triple
            )
        permutation = tuple(row["port_permutation"])
        selected = atlas.selected_graph_from_completion(
            atlas.relabel_record(targets[target_index], permutation)
        )
        relation = atlas.mixed_relation_exact_prepared(
            prepared_sources[row["source_index"]], selected
        )
        exact_relations["cycle_base"][relation] += 1
        if relation != "none":
            conflicts.append(
                {"family": "cycle_base", "raw_id": row["raw_id"], "relation": relation}
            )
            continue
        aligned = []
        for base_orientation in triple:
            reported_orientation = permutation[base_orientation]
            aligned.append(
                (
                    reported_orientation,
                    source_base[row["source_index"]][reported_orientation],
                    target_base[target_index][base_orientation],
                )
            )
        choice, failures = choose_zero_sign(core, aligned)
        if choice is None:
            unresolved.append(
                {"family": "cycle_base", "raw_id": row["raw_id"], "failures": failures}
            )
            continue
        (
            _,
            orientation,
            signed_side,
            sign_name,
            sign,
            normalized,
            source_polynomial,
            target_polynomial,
        ) = choice
        signed_polynomial = (
            source_polynomial if signed_side == "source" else target_polynomial
        )
        invariant_key = f"k3:t012:i{orientation}"
        coordinate_invariant_certificates.setdefault(
            invariant_key,
            coordinate_invariant_certificate(atlas, core, 3, triple, orientation),
        )
        presentations.current = (
            "cycle_base",
            row["source_index"],
            target_index,
            row["permutation_index"],
            orientation,
            signed_side,
        )
        signed_digest = register_sign(
            core,
            sign_certificates,
            presentations,
            signed_polynomial,
            normalized,
            sign_name,
            sign,
        )
        source_digest = core.sparse_hash(source_polynomial)
        target_digest = core.sparse_hash(target_polynomial)
        signed_sides["cycle_base"][signed_side] += 1
        relation_classes["cycle_base"][(source_digest, target_digest)] += 1
        truth = {
            "raw_id": row["raw_id"],
            "source_index": row["source_index"],
            "target_index": target_index,
            "permutation_index": row["permutation_index"],
            "chosen_T_orientation_label": orientation,
            "source_pullback_sha256": source_digest,
            "target_pullback_sha256": target_digest,
            "signed_pullback_sha256": signed_digest,
            "strict_sign": sign_name,
            "exact_full_graph_relation": "none",
            "result": (
                f"strict_source_{sign_name}_target_zero"
                if signed_side == "source"
                else f"source_zero_strict_target_{sign_name}"
            ),
        }
        row_hashes["cycle_base"].append(core.sha(truth))

    # Full completions: replay every placement path and target promotion from
    # primitive graphs.  No graph or polynomial descriptor is retained.
    configurations = generator.build_source_configurations(atlas, sources)
    configuration_index = {
        (source_index, depth, tuple(row["placement_path"])): row
        for (source_index, depth), rows in configurations.items()
        for row in rows
    }
    source_full_cache = {}
    target_full_cache = {}
    for ordinal, row in enumerate(full_rows):
        witness = witnesses[row["certificate_id"]]
        triple = tuple(witness["triple"])
        depth = len(row["dummy_roles_in_label_order"])
        source_key = (
            row["source_index"],
            depth,
            tuple(row["source_placement_path"]),
        )
        target_key = (
            row["target_index"],
            row["permutation_index"],
            tuple(row["dummy_roles_in_label_order"]),
        )
        source_graph = configuration_index[source_key]["graph"]
        source_polynomial_key = (source_key, triple)
        target_polynomial_key = (target_key, triple)
        if source_polynomial_key not in source_full_cache:
            _, source_full_cache[source_polynomial_key] = graph_descriptor_polynomials(
                atlas, core, source_graph, triple
            )
        if target_polynomial_key not in target_full_cache:
            target_graph = common.relabel_and_promote_all(
                atlas,
                targets[row["target_index"]],
                permutations[row["permutation_index"]],
                tuple(row["dummy_roles_in_label_order"]),
            )
            _, target_full_cache[target_polynomial_key] = graph_descriptor_polynomials(
                atlas, core, target_graph, triple
            )
        else:
            target_graph = common.relabel_and_promote_all(
                atlas,
                targets[row["target_index"]],
                permutations[row["permutation_index"]],
                tuple(row["dummy_roles_in_label_order"]),
            )
        relation = atlas.mixed_relation_exact(source_graph, target_graph)
        exact_relations["cycle_full_equal_topology"][relation] += 1
        if relation != "none":
            conflicts.append(
                {"family": "cycle_full_equal_topology", "raw_id": row["raw_id"], "relation": relation}
            )
            continue
        aligned = [
            (
                orientation,
                source_full_cache[source_polynomial_key][orientation],
                target_full_cache[target_polynomial_key][orientation],
            )
            for orientation in triple
        ]
        choice, failures = choose_zero_sign(core, aligned)
        chosen_triple = triple
        if choice is None:
            source_descriptor = atlas.model_descriptor_fast2(source_graph)
            target_descriptor = atlas.model_descriptor_fast2(target_graph)
            repair_key = (source_descriptor, target_descriptor)
            if repair_key not in all_triple_repair_cache:
                all_triple_repair_cache[repair_key] = search_all_triples(
                    atlas, core, source_graph, target_graph
                )
            repair, all_failures, _, _ = all_triple_repair_cache[repair_key]
            if repair is None:
                unresolved.append(
                    {
                        "family": "cycle_full_equal_topology",
                        "raw_id": row["raw_id"],
                        "root_id": row["root_id"],
                        "legacy_triple": list(triple),
                        "legacy_failures": failures,
                        "all_triple_failures": all_failures,
                    }
                )
                continue
            chosen_triple, choice = repair
            revoked_legacy_witness_repairs.append(
                {
                    "raw_id": row["raw_id"],
                    "root_id": row["root_id"],
                    "legacy_triple": list(triple),
                    "replacement_full_map_triple": list(chosen_triple),
                    "replacement_orientation": choice[1],
                    "replacement_signed_side": choice[2],
                }
            )
        (
            _,
            orientation,
            signed_side,
            sign_name,
            sign,
            normalized,
            source_polynomial,
            target_polynomial,
        ) = choice
        signed_polynomial = (
            source_polynomial if signed_side == "source" else target_polynomial
        )
        invariant_key = (
            f"k{row['port_count']}:t{''.join(map(str, chosen_triple))}:i{orientation}"
        )
        coordinate_invariant_certificates.setdefault(
            invariant_key,
            coordinate_invariant_certificate(
                atlas, core, row["port_count"], chosen_triple, orientation
            ),
        )
        presentations.current = (
            "cycle_full_equal_topology",
            row["raw_id"],
            row["root_id"],
            orientation,
            signed_side,
        )
        signed_digest = register_sign(
            core,
            sign_certificates,
            presentations,
            signed_polynomial,
            normalized,
            sign_name,
            sign,
        )
        source_digest = core.sparse_hash(source_polynomial)
        target_digest = core.sparse_hash(target_polynomial)
        signed_sides["cycle_full_equal_topology"][signed_side] += 1
        relation_classes["cycle_full_equal_topology"][(source_digest, target_digest)] += 1
        truth = {
            "raw_id": row["raw_id"],
            "root_id": row["root_id"],
            "base_raw_id": row["base_raw_id"],
            "port_count": row["port_count"],
            "source_placement_path": row["source_placement_path"],
            "legacy_witness_triple": list(triple),
            "certified_full_map_triple": list(chosen_triple),
            "chosen_T_orientation_label": orientation,
            "source_pullback_sha256": source_digest,
            "target_pullback_sha256": target_digest,
            "signed_pullback_sha256": signed_digest,
            "strict_sign": sign_name,
            "exact_full_graph_relation": "none",
            "result": (
                f"strict_source_{sign_name}_target_zero"
                if signed_side == "source"
                else f"source_zero_strict_target_{sign_name}"
            ),
        }
        row_hashes["cycle_full_equal_topology"].append(core.sha(truth))
        if (ordinal + 1) % 50 == 0:
            print(
                json.dumps(
                    {
                        "event": "cycle_full_progress",
                        "processed": ordinal + 1,
                        "certified": len(row_hashes["cycle_full_equal_topology"]),
                        "unresolved": len(unresolved),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

    for digest, certificate in sign_certificates.items():
        certificate["presentations"] = [
            list(row) for row in sorted(presentations[digest], key=repr)
        ]

    expected = {"cycle_base": 7452, "cycle_full_equal_topology": 300}
    family_reports = {}
    for family, count in expected.items():
        family_unresolved = [row for row in unresolved if row["family"] == family]
        family_conflicts = [row for row in conflicts if row["family"] == family]
        family_reports[family] = {
            "input_rows": count,
            "exact_full_graph_relation_census": dict(
                sorted(exact_relations[family].items())
            ),
            "direct_full_map_zero_sign_rows": len(row_hashes[family]),
            "signed_side_census": dict(sorted(signed_sides[family].items())),
            "polynomial_relation_classes": len(relation_classes[family]),
            "polynomial_relation_class_multiplicities": {
                f"{source}:{target}": multiplicity
                for (source, target), multiplicity in sorted(
                    relation_classes[family].items()
                )
            },
            "false_iso_or_triangle_conflicts": len(family_conflicts),
            "reopened_obligations": len(family_unresolved),
            "ordered_truth_row_hashes": row_hashes[family],
            "ordered_truth_row_hash_root": core.sha(row_hashes[family]),
        }
    status = "PASS" if not unresolved and not conflicts else "BLOCKED"
    report = {
        "schema": "k2p-cycle-tree-sunlet-whole-map-truth-v1",
        "status": status,
        "claim_boundary": (
            "The former rooted restriction type is not a theorem.  Each accepted "
            "row is rebound to an exact T_i zero/strict-sign identity on the original "
            "full graph-derived Fourier maps."
        ),
        "inputs": {
            "atlas_sha256": core.sha_file(core.ATLAS_PATH),
            "cycle_common_sha256": core.sha_file(CYCLE_DIR / "cycle_common.py"),
            "cycle_generator_sha256": core.sha_file(
                CYCLE_DIR / "generate_cycle_closure.py"
            ),
            "base_ledger_sha256": core.sha_file(BASE_LEDGER),
            "full_ledger_sha256": core.sha_file(FULL_LEDGER),
            "topology_witnesses_sha256": core.sha_file(WITNESSES),
        },
        "families": family_reports,
        "sign_certificates": dict(sorted(sign_certificates.items())),
        "coordinate_invariant_certificates": dict(
            sorted(coordinate_invariant_certificates.items())
        ),
        "false_terminal_conflicts": conflicts,
        "revoked_legacy_witness_repairs": revoked_legacy_witness_repairs,
        "revoked_legacy_witness_count": len(revoked_legacy_witness_repairs),
        "reopened_obligations": unresolved,
        "false_topology_oracle_count": len(conflicts) + len(unresolved),
        "unresolved": len(unresolved),
        "incoherent": 0,
    }
    report["payload_sha256"] = core.sha(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": status,
                "base_certified": len(row_hashes["cycle_base"]),
                "full_certified": len(row_hashes["cycle_full_equal_topology"]),
                "false_conflicts": len(conflicts),
                "reopened": len(unresolved),
                "sign_polynomials": len(sign_certificates),
                "payload_sha256": report["payload_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except (
        RuntimeError,
        StrictJSONError,
        AssertionError,
        KeyError,
        OSError,
        json.JSONDecodeError,
    ) as exc:
        raise SystemExit(f"CYCLE_TREE_SUNLET_TRUTH_FAIL:{exc}") from exc
