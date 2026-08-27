#!/usr/bin/env python3
"""Independent exact verifier for the complete K3P four-port replay.

The verifier imports only :mod:`independent_replay_core`, whose literal graph
grammar and algebra are separate from both the producer and the historical
atlas compiler.  No frozen fourteen-orbit lock is an input to this program.
"""
from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import itertools
import json
import os
import sys
import time
from fractions import Fraction as Q
from pathlib import Path

import independent_replay_core as core


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEFAULT_ARTIFACTS = HERE / "artifacts"
RAW_PER_SOURCE = 2_814 * 24
RAW_TOTAL = 6 * RAW_PER_SOURCE


def fail(code, detail=None):
    raise core.ReplayFailure(code if detail is None else f"{code}: {detail!r}")


def require(condition, code, detail=None):
    if not condition:
        fail(code, detail)


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def load_gzip_json(path):
    with gzip.open(path, "rb") as handle:
        return json.loads(handle.read())


def gzip_binding(path):
    compressed = file_hash(path)
    with gzip.open(path, "rb") as handle:
        payload = handle.read()
    return {"sha256": compressed,
            "uncompressed_sha256": hashlib.sha256(payload).hexdigest(),
            "uncompressed_bytes": len(payload)}


def verify_artifact_envelope(root):
    summary_path = root / "FULL_FOUR_PORT_REPLAY.json"
    summary = json.loads(summary_path.read_text())
    require(summary["schema"] == "k3p-full-four-port-universe-replay-v2",
            "SUMMARY_SCHEMA")
    atlas_path = PROJECT / "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py"
    producer_path = HERE / "generate_full_four_port_replay.py"
    require(summary["bindings"] == {
        "atlas_path": "input_frozen/k3p_cloud_artifacts/k3p_atlas_core.py",
        "atlas_sha256": file_hash(atlas_path),
        "producer_sha256": file_hash(producer_path),
    }, "SUMMARY_SOURCE_BINDINGS")
    require(summary["scope"] == {
        "starts_from_primitive_graph_grammar": True,
        "reads_frozen_fourteen_orbit_lock": False,
        "reads_frozen_companion_raw_ledger": False,
        "reads_missing_cloud_descriptor_corpus": False,
        "rank_note": "Exact nonzero Jacobian minors are regenerated for every literal map; target upper-rank binding is verified independently by the verifier.",
    }, "SUMMARY_SCOPE")
    producer_source = producer_path.read_text()
    forbidden_authorities = (
        "raw_directional_ledger.jsonl.gz",
        "K3P_14_ORBIT_LOCK.json",
        "k3p_full_relation_raw.jsonl",
        "k3p_cloud_descriptor",
    )
    require(not any(token in producer_source for token in forbidden_authorities),
            "PRODUCER_FROZEN_AUTHORITY_REFERENCE")
    unhashed = dict(summary)
    observed_payload = unhashed.pop("payload_sha256_without_hash")
    require(observed_payload == canonical_hash(unhashed), "SUMMARY_PAYLOAD_HASH")
    required = {
        "exact_rank_minor_registry.json.gz",
        "exact_rank_upper_registry.json.gz",
        "eligible_class_registry.json.gz",
        "full_directional_ledger.jsonl.gz",
        "DERIVED_RESIDUE_QUOTIENT.json",
    }
    require(set(summary["artifacts"]) == required, "SUMMARY_ARTIFACT_SET")
    for name in sorted(required):
        path = root / name
        require(path.is_file(), "ARTIFACT_MISSING", name)
        if name.endswith(".gz"):
            require(gzip_binding(path) == summary["artifacts"][name],
                    "GZIP_BINDING", name)
        else:
            require(summary["artifacts"][name] ==
                    {"sha256": file_hash(path), "bytes": path.stat().st_size},
                    "PLAIN_BINDING", name)
    rank = load_gzip_json(root / "exact_rank_minor_registry.json.gz")
    upper = load_gzip_json(root / "exact_rank_upper_registry.json.gz")
    classes = load_gzip_json(root / "eligible_class_registry.json.gz")
    quotient = json.loads((root / "DERIVED_RESIDUE_QUOTIENT.json").read_text())
    require(rank["schema"] == "k3p-four-port-rank-minors-v2", "RANK_SCHEMA")
    require(upper["schema"] == "k3p-four-port-rank-upper-vector-fields-v2", "UPPER_SCHEMA")
    require(classes["schema"] == "k3p-four-port-eligible-classes-v2", "CLASS_SCHEMA")
    require(quotient["schema"] == "k3p-four-port-derived-residue-quotient-v2",
            "QUOTIENT_SCHEMA")
    require((quotient["post_quadratic_raw_records"],
             quotient["raw_records_in_fourteen_orbits"],
             quotient["separate_sink_swap_records"],
             quotient["canonical_orbits"]) == (40, 38, 2, 14),
            "QUOTIENT_FIXED_CENSUS")
    require(len(quotient["orbits"]) == 14 and len(quotient["sink_swaps"]) == 2 and
            sum(len(row["raw_members"]) for row in quotient["orbits"]) == 38,
            "QUOTIENT_PRESENTATION_CENSUS")
    require(summary["residue_quotient"] == {
        "post_quadratic_raw_records": 40,
        "raw_records_in_fourteen_orbits": 38,
        "separate_sink_swap_records": 2,
        "canonical_orbits": 14,
    }, "SUMMARY_QUOTIENT_CENSUS")
    return summary, rank["records"], upper["records"], classes["records"], quotient


def ledger_rows(path):
    with gzip.open(path, "rt") as handle:
        for line in handle:
            yield json.loads(line)


def verify_ledger_structure(root, summary):
    counts = collections.Counter()
    previous = -1
    row_by_id = {}
    for ordinal, row in enumerate(ledger_rows(root / "full_directional_ledger.jsonl.gz")):
        require(row["raw_id"] == ordinal, "LEDGER_NOT_DENSE", (ordinal, row.get("raw_id")))
        require(row["raw_id"] > previous, "LEDGER_ORDER")
        previous = row["raw_id"]
        expected_source = ordinal // RAW_PER_SOURCE
        within = ordinal % RAW_PER_SOURCE
        expected_target = within // 24
        expected_permutation = within % 24
        require((row["source_index"], row["target_index"], row["permutation_index"]) ==
                (expected_source, expected_target, expected_permutation),
                "LEDGER_COORDINATE", ordinal)
        counts[row["category"]] += 1
        row_by_id[ordinal] = row
    require(previous + 1 == RAW_TOTAL, "LEDGER_CENSUS", previous + 1)
    require(dict(sorted(counts.items())) == summary["raw_category_counts"],
            "LEDGER_CATEGORY_COUNTS")
    return row_by_id


def build_universe(summary):
    sources = core.sources()
    selected = core.targets(4, True)
    marginalized = core.targets(4, False)
    targets = selected + marginalized
    permutations = tuple(itertools.permutations(range(4)))
    require((len(sources), len(selected), len(marginalized), len(targets), len(permutations)) ==
            (6, 831, 1983, 2814, 24), "PRIMITIVE_CENSUS")
    target_signatures = tuple(core.topology_signature(target.graph) for target in targets)
    compatible = []
    reasons = []
    for source in sources:
        source_signature = core.topology_signature(source.graph)
        lane, rejected = [], collections.Counter()
        for target_index, target_signature in enumerate(target_signatures):
            for permutation_index, permutation in enumerate(permutations):
                accepted, reason = core.immediate_compatible(
                    source_signature, core.permute_signature(target_signature, permutation))
                if accepted:
                    lane.append((target_index, permutation_index, permutation))
                else:
                    rejected[reason] += 1
        compatible.append(lane)
        reasons.append(dict(sorted(rejected.items())))
    require(sum(map(len, compatible)) == 27_834, "POST_TOPOLOGY_CENSUS")
    require(reasons == summary["topology_reasons_by_source"], "TOPOLOGY_REASON_CENSUS")
    primitive = summary["primitive_counts"]
    require(primitive["raw_total"] == RAW_TOTAL and primitive["post_topology"] == 27_834,
            "SUMMARY_PRIMITIVE_COUNTS")
    return sources, targets, permutations, target_signatures, compatible


def compile_all(sources, targets, compatible, summary):
    source_descriptors = tuple(core.compile_descriptor(source.graph) for source in sources)
    keys = sorted({(target_index, permutation)
                   for lane in compatible for target_index, _, permutation in lane},
                  key=lambda row: (row[0], row[1]))
    require(len(keys) == 13_686, "COMPATIBLE_KEY_CENSUS")
    target_descriptors = {}
    descriptors = {}
    for ordinal, (target_index, permutation) in enumerate(keys):
        descriptor = core.compile_descriptor(core.relabel(targets[target_index], permutation).graph)
        digest = core.descriptor_hash(descriptor)
        if digest in descriptors:
            require(descriptors[digest] == descriptor, "DESCRIPTOR_HASH_COLLISION")
        descriptors[digest] = descriptor
        target_descriptors[(target_index, permutation)] = descriptor
        if ordinal and ordinal % 2_000 == 0:
            print(json.dumps({"independent_compiled_keys": ordinal,
                              "unique_maps": len(descriptors)}, sort_keys=True), flush=True)
    for descriptor in source_descriptors:
        digest = core.descriptor_hash(descriptor)
        if digest in descriptors:
            require(descriptors[digest] == descriptor, "SOURCE_DESCRIPTOR_COLLISION")
        descriptors[digest] = descriptor
    require(len(descriptors) == 4_379, "UNIQUE_DESCRIPTOR_CENSUS", len(descriptors))
    require(summary["primitive_counts"]["compatible_target_permutation_keys"] == len(keys),
            "SUMMARY_KEY_CENSUS")
    require(summary["primitive_counts"]["unique_map_descriptors_including_sources"] == len(descriptors),
            "SUMMARY_DESCRIPTOR_CENSUS")
    return source_descriptors, target_descriptors, descriptors


def verify_rank_registry(records, descriptors, summary):
    by_hash = {row["descriptor_sha256"]: row for row in records}
    require(len(by_hash) == len(records) == len(descriptors), "RANK_REGISTRY_CENSUS")
    require(set(by_hash) == set(descriptors), "RANK_DESCRIPTOR_SET")
    ranks = {}
    for ordinal, digest in enumerate(sorted(descriptors)):
        descriptor = descriptors[digest]
        row = by_hash[digest]
        certificate = core.rank_certificate(descriptor)
        expected = {
            "descriptor_sha256": digest,
            "edge_class_count": descriptor.edge_class_count,
            "reticulation_count": descriptor.retic_count,
            "parameter_count": 3 * descriptor.edge_class_count + descriptor.retic_count,
            **certificate,
        }
        require(row == expected, "RANK_CERTIFICATE", digest)
        ranks[digest] = certificate["rank"]
        if ordinal and ordinal % 750 == 0:
            print(json.dumps({"independent_rank_minors": ordinal}, sort_keys=True), flush=True)
    source_hashes = [core.descriptor_hash(core.compile_descriptor(source.graph))
                     for source in core.sources()]
    require([ranks[digest] for digest in source_hashes] == [20, 21, 21, 21, 23, 24],
            "SOURCE_RANKS")
    require(summary["source_ranks"] == [20, 21, 21, 21, 23, 24], "SUMMARY_SOURCE_RANKS")
    return ranks


def verify_upper_registry(records, descriptors, ranks, summary, only_hash=None):
    by_hash = {row["descriptor_sha256"]: row for row in records}
    require(len(by_hash) == len(records), "UPPER_DUPLICATE_HASH")
    require(set(by_hash) <= set(descriptors), "UPPER_UNKNOWN_DESCRIPTOR")
    selected = [only_hash] if only_hash else sorted(by_hash)
    for ordinal, digest in enumerate(selected):
        require(digest in by_hash, "FOCUSED_UPPER_MISSING", digest)
        computed = core.syzygy_rank_upper(descriptors[digest], include_evaluation_witness=True)
        base_computed = {key: value for key, value in computed.items()
                         if not key.startswith("evaluation_")}
        expected = {**base_computed, "descriptor_sha256": digest,
                    "point_minor_rank": ranks[digest]}
        require(by_hash[digest] == expected, "SYZYGY_UPPER_CERTIFICATE", digest)
        require(computed["independent_kernel_fields"] ==
                computed["stacked_system_rank"] - computed["coefficient_system_rank"],
                "SYZYGY_LINEAR_ALGEBRA_IDENTITY", digest)
        require(computed["certified_rank_upper"] ==
                computed["parameter_count"] - computed["independent_kernel_fields"],
                "SYZYGY_UPPER_FORMULA", digest)
        require(Q(computed["evaluation_image_minor_determinant"]) != 0 and
                len(computed["evaluation_image_minor_rows"]) ==
                computed["independent_kernel_fields"] ==
                len(computed["evaluation_image_minor_columns"]),
                "SYZYGY_OPEN_MINOR_WITNESS", digest)
        if not only_hash and ordinal and ordinal % 500 == 0:
            print(json.dumps({"independent_syzygy_uppers": ordinal}, sort_keys=True), flush=True)
    if not only_hash:
        require(summary["rank_upper_certificate_count"] == len(records), "SUMMARY_UPPER_CENSUS")
    return by_hash


def strict_witness(descriptor, salt):
    edges, inheritance = core.exact_point(descriptor, salt)
    margins = []
    for c, g, t in edges:
        margins.extend((c, g, t, 1-c, 1-g, 1-t,
                        1+c-g-t, 1-c+g-t, 1-c-g+t,
                        c-g*t, g-c*t, t-c*g))
    for value in inheritance:
        margins.extend((value, 1-value))
    return {"edge_triples": [[str(value) for value in row] for row in edges],
            "inheritance": [str(value) for value in inheritance],
            "minimum_margin": str(min(margins))}


def quadratic_full(source, target, source_index):
    certificate = core.quadratic_separator(source, target)
    if certificate is None:
        return None
    edges, inheritance = core.exact_point(source, source_index)
    outputs = core.evaluate(source, edges, inheritance)
    value = sum(Q(coefficient) * outputs[pair[0]] * outputs[pair[1]]
                for pair, coefficient in zip(certificate["coordinate_pairs"],
                                             certificate["coefficients"]))
    require(value != 0, "QUADRATIC_SOURCE_EVALUATION")
    certificate["source_evaluation"] = str(value)
    certificate["strict_source_witness"] = strict_witness(source, source_index)
    return certificate


def h14_full(source, target, source_index):
    certificate = core.h14_separator(source, target, source_index)
    if certificate is not None:
        certificate["strict_source_witness"] = strict_witness(source, source_index)
    return certificate


def classify(source_records, targets, compatible, source_descriptors,
             target_descriptors, ranks, upper_records, class_records, summary):
    stored = {(row["source_index"], row["class_id"]): row for row in class_records}
    require(len(stored) == len(class_records), "CLASS_KEY_DUPLICATE")
    upper = {row["descriptor_sha256"]: row for row in upper_records}
    raw = {}
    excluded = [set() for _ in source_records]
    seen_classes = set()
    for source_index, (source_record, source_descriptor, lane) in enumerate(
            zip(source_records, source_descriptors, compatible)):
        source_digest = core.descriptor_hash(source_descriptor)
        source_rank = ranks[source_digest]
        eligible = {}
        for target_index, permutation_index, permutation in lane:
            target = target_descriptors[(target_index, permutation)]
            target_digest = core.descriptor_hash(target)
            if ranks[target_digest] < source_rank:
                require(target_digest in upper, "MISSING_RANK_UPPER", target_digest)
                if upper[target_digest]["certified_rank_upper"] < source_rank:
                    excluded[source_index].add((target_index, permutation))
                    continue
            eligible.setdefault(target, []).append((target_index, permutation_index, permutation))
        for class_id, (target_descriptor, members) in enumerate(eligible.items()):
            key = (source_index, class_id)
            require(key in stored, "CLASS_RECORD_MISSING", key)
            seen_classes.add(key)
            recorded = stored[key]
            target_digest = core.descriptor_hash(target_descriptor)
            quadratic = quadratic_full(source_descriptor, target_descriptor, source_index)
            h14 = None
            algebra_category = None
            if quadratic is not None:
                algebra_category = "quadratic_separated"
            elif ranks[target_digest] < source_rank:
                h14 = h14_full(source_descriptor, target_descriptor, source_index)
                if h14 is not None:
                    algebra_category = "h14_marginal_separated"
            member_rows = []
            category_counts = collections.Counter()
            for target_index, permutation_index, permutation in members:
                relabelled = core.relabel(targets[target_index], permutation)
                selected = core.selected_graph(relabelled)
                relation = core.mixed_relation(source_record.graph, selected)
                has_dummy = bool(targets[target_index].dummy_labels)
                if algebra_category is not None:
                    category = algebra_category
                elif relation == "isomorphic":
                    category = "isomorphic"
                elif relation == "triangle":
                    category = "ordinary_triangle"
                elif has_dummy:
                    category = "restoration_obligation"
                else:
                    category = "post_quadratic_residue"
                category_counts[category] += 1
                expected_member = {
                    "target_index": target_index,
                    "permutation_index": permutation_index,
                    "port_permutation": list(permutation),
                    "category": category,
                    "graph_relation": relation,
                    "target_has_dummy_completion": has_dummy,
                    "restoration_raw_id": (
                        (source_index * 2_814 + target_index) * 24 + permutation_index
                        if category == "restoration_obligation" else None
                    ),
                    "target_graph_sha256": core.graph_hash(relabelled.graph),
                    "selected_graph_sha256": core.graph_hash(selected),
                }
                member_rows.append(expected_member)
                raw[(source_index, target_index, permutation)] = {
                    "category": category, "class_id": class_id,
                    "target_descriptor_sha256": target_digest,
                    "target_rank": ranks[target_digest],
                    "graph_relation": relation,
                    "target_has_dummy_completion": has_dummy,
                    "restoration_raw_id": (
                        (source_index * 2_814 + target_index) * 24 + permutation_index
                        if category == "restoration_obligation" else None
                    ),
                }
            expected_record = {
                "source_index": source_index, "class_id": class_id,
                "source_descriptor_sha256": source_digest,
                "source_rank": source_rank,
                "target_descriptor_sha256": target_digest,
                "target_rank": ranks[target_digest],
                "raw_member_count": len(members),
                "member_categories": dict(sorted(category_counts.items())),
                "members": member_rows,
                "quadratic_certificate": quadratic,
                "h14_marginal_certificate": h14,
            }
            require(recorded == expected_record, "CLASS_SEMANTICS", key)
        require(len(excluded[source_index]) + sum(map(len, eligible.values())) == len(lane),
                "SOURCE_CLASS_PARTITION", source_index)
    require(seen_classes == set(stored), "EXTRA_CLASS_RECORDS")
    require(len(class_records) == summary["eligible_map_class_count"], "SUMMARY_CLASS_CENSUS")
    class_counts = collections.Counter(next(iter(row["member_categories"])) for row in class_records)
    require(dict(sorted(class_counts.items())) == summary["class_member_category_counts"],
            "SUMMARY_CLASS_COUNTS")
    return raw, excluded


def expected_raw_row(raw_id, sources, targets, permutations, target_signatures,
                     source_descriptors, target_descriptors, ranks, upper,
                     raw_classification, excluded):
    source_index = raw_id // RAW_PER_SOURCE
    within = raw_id % RAW_PER_SOURCE
    target_index, permutation_index = divmod(within, 24)
    permutation = permutations[permutation_index]
    source_descriptor = source_descriptors[source_index]
    source_digest = core.descriptor_hash(source_descriptor)
    source_rank = ranks[source_digest]
    base = {"raw_id": raw_id, "source_index": source_index,
            "target_index": target_index, "permutation_index": permutation_index,
            "port_permutation": list(permutation),
            "source_descriptor_sha256": source_digest, "source_rank": source_rank}
    source_signature = core.topology_signature(sources[source_index].graph)
    accepted, reason = core.immediate_compatible(
        source_signature, core.permute_signature(target_signatures[target_index], permutation))
    if not accepted:
        return {**base, "category": "topology_excluded",
                "topology_exclusion_reason": reason}
    if (target_index, permutation) in excluded[source_index]:
        descriptor = target_descriptors[(target_index, permutation)]
        digest = core.descriptor_hash(descriptor)
        return {**base, "category": "rank_excluded",
                "target_descriptor_sha256": digest, "target_rank": ranks[digest],
                "target_rank_upper": upper[digest]["certified_rank_upper"],
                "rank_upper_mechanism": upper[digest]["mechanism"]}
    require((source_index, target_index, permutation) in raw_classification,
            "RAW_CLASSIFICATION_MISSING", raw_id)
    return {**base, **raw_classification[(source_index, target_index, permutation)]}


def verify_full_ledger(root, sources, targets, permutations, target_signatures,
                       source_descriptors, target_descriptors, ranks, upper,
                       raw_classification, excluded, summary):
    counts = collections.Counter()
    iterator = ledger_rows(root / "full_directional_ledger.jsonl.gz")
    for raw_id in range(RAW_TOTAL):
        try:
            observed = next(iterator)
        except StopIteration:
            fail("LEDGER_EARLY_EOF", raw_id)
        expected = expected_raw_row(raw_id, sources, targets, permutations,
                                   target_signatures, source_descriptors,
                                   target_descriptors, ranks, upper,
                                   raw_classification, excluded)
        require(observed == expected, "RAW_LEDGER_SEMANTICS", raw_id)
        counts[expected["category"]] += 1
    try:
        next(iterator)
        fail("LEDGER_TRAILING_ROWS")
    except StopIteration:
        pass
    require(dict(sorted(counts.items())) == summary["raw_category_counts"],
            "RAW_CATEGORY_CENSUS")


def double_coset(left, representative, right):
    return tuple(sorted({core.compose(first, core.compose(representative, second))
                         for first in left for second in right}))


def derive_quotient(sources, targets, permutations, source_descriptors,
                    target_descriptors, ranks, raw):
    residue = sorted((source_index, target_index, permutation)
                     for (source_index, target_index, permutation), binding in raw.items()
                     if binding["category"] == "post_quadratic_residue")
    require(len(residue) == 40, "RESIDUE_CENSUS", len(residue))
    pairs = collections.defaultdict(set)
    for source_index, target_index, permutation in residue:
        pairs[(source_index, target_index)].add(permutation)
    require(sorted(map(len, pairs.values())) == [2, 4, 4, 4, 4, 22], "RESIDUE_PAIR_SHAPE")
    h_pair = next(pair for pair, members in pairs.items() if len(members) == 22)
    sink_pair = next(pair for pair, members in pairs.items() if len(members) == 2)
    lower_pairs = sorted(pair for pair, members in pairs.items() if len(members) == 4)
    h_source, h_target = h_pair
    source_group = core.mixed_automorphisms(sources[h_source], permutations)
    target_group = core.mixed_automorphisms(targets[h_target], permutations)
    remaining = set(pairs[h_pair])
    h_orbits = []
    while remaining:
        representative = min(remaining)
        orbit = set(double_coset(source_group, representative, target_group))
        require(orbit <= remaining, "H21_ORBIT_ESCAPE")
        h_orbits.append(tuple(sorted(orbit)))
        remaining -= orbit
    require(len(h_orbits) == 6, "H21_ORBIT_COUNT")
    rows = []
    for index, members in enumerate(sorted(h_orbits), 1):
        representative = min(members)
        target_descriptor = target_descriptors[(h_target, representative)]
        rows.append({"orbit_id": f"H21-{index:02d}",
                     "family": "rank21_nonautomorphic_relabelling",
                     "source_index": h_source, "target_index": h_target,
                     "source_rank": ranks[core.descriptor_hash(source_descriptors[h_source])],
                     "target_rank": ranks[core.descriptor_hash(target_descriptor)],
                     "representative_permutation": list(representative),
                     "raw_members": [list(member) for member in members],
                     "source_automorphism_group": [list(member) for member in source_group],
                     "target_automorphism_group": [list(member) for member in target_group],
                     "source_map_sha256": core.descriptor_hash(source_descriptors[h_source]),
                     "target_map_sha256": core.descriptor_hash(target_descriptor)})
    identity = (0, 1, 2, 3)
    lower_21 = 0
    for source_index, target_index in lower_pairs:
        target_group = core.mixed_automorphisms(targets[target_index], permutations)
        remaining = set(pairs[(source_index, target_index)])
        local = []
        while remaining:
            representative = min(remaining)
            orbit = set(double_coset((identity,), representative, target_group))
            require(orbit <= remaining, "LOWER_ORBIT_ESCAPE")
            local.append(tuple(sorted(orbit)))
            remaining -= orbit
        require(len(local) == 2, "LOWER_ORBIT_COUNT")
        rank = ranks[core.descriptor_hash(source_descriptors[source_index])]
        if rank == 20:
            prefix = "L20"
        elif rank == 23:
            prefix = "L23"
        elif rank == 21:
            lower_21 += 1
            prefix = "L21a" if lower_21 == 1 else "L21b"
        else:
            fail("LOWER_RANK_PREFIX", rank)
        for index, members in enumerate(sorted(local), 1):
            representative = min(members)
            target_descriptor = target_descriptors[(target_index, representative)]
            rows.append({"orbit_id": f"{prefix}-{index:02d}",
                         "family": "lower_to_rank24", "source_index": source_index,
                         "target_index": target_index, "source_rank": rank,
                         "target_rank": ranks[core.descriptor_hash(target_descriptor)],
                         "representative_permutation": list(representative),
                         "raw_members": [list(member) for member in members],
                         "source_automorphism_group": [list(identity)],
                         "target_automorphism_group": [list(member) for member in target_group],
                         "source_map_sha256": core.descriptor_hash(source_descriptors[source_index]),
                         "target_map_sha256": core.descriptor_hash(target_descriptor)})
    sink_source, sink_target = sink_pair
    sinks = []
    for permutation in sorted(pairs[sink_pair]):
        target_descriptor = target_descriptors[(sink_target, permutation)]
        sinks.append({"source_index": sink_source, "target_index": sink_target,
                      "port_permutation": list(permutation),
                      "source_rank": ranks[core.descriptor_hash(source_descriptors[sink_source])],
                      "target_rank": ranks[core.descriptor_hash(target_descriptor)],
                      "source_map_sha256": core.descriptor_hash(source_descriptors[sink_source]),
                      "target_map_sha256": core.descriptor_hash(target_descriptor)})
    require(len(rows) == 14 and sum(len(row["raw_members"]) for row in rows) == 38,
            "FOURTEEN_ORBIT_CENSUS")
    return {"schema": "k3p-four-port-derived-residue-quotient-v2",
            "post_quadratic_raw_records": 40,
            "raw_records_in_fourteen_orbits": 38,
            "separate_sink_swap_records": 2,
            "canonical_orbits": 14,
            "orbits": sorted(rows, key=lambda row: row["orbit_id"]),
            "sink_swaps": sinks}


def verify_restoration_and_probe_bindings(generated_rows):
    generated_restoration = {row["raw_id"]: row for row in generated_rows.values()
                             if row["category"] == "restoration_obligation"}
    require(len(generated_restoration) == 2_540, "GENERATED_RESTORATION_CENSUS",
            len(generated_restoration))
    require(len({(row["source_index"], row["class_id"])
                 for row in generated_restoration.values()}) == 997,
            "GENERATED_RESTORATION_LOCAL_CLASS_CENSUS")
    for raw_id, row in generated_restoration.items():
        require(row.get("restoration_raw_id") == raw_id,
                "GENERATED_RESTORATION_RAW_BINDING", raw_id)
    import re
    root_pattern = re.compile(r"^s([0-5]):c([0-9]+):t([0-9]+):p([0-3]{4})$")
    generated_presentations = {
        (row["source_index"], row["target_index"],
         "".join(map(str, row["port_permutation"]))): raw_id
        for raw_id, row in generated_restoration.items()
    }
    require(len(generated_presentations) == 2_540,
            "GENERATED_RESTORATION_PRESENTATION_UNIQUENESS")
    forest_path = PROJECT / "input_frozen/model_independent_topology_package/anchor_inputs/corrected_restoration_forest.json"
    forest = json.loads(forest_path.read_text())
    forest_roots = {row["root_id"] for row in forest["first_coverage"]}
    require(len(forest_roots) == 2_540, "FOREST_RESTORATION_ROOT_SET")
    forest_presentations = {}
    for root in forest_roots:
        match = root_pattern.fullmatch(root)
        require(match is not None, "FOREST_ROOT_ID_GRAMMAR", root)
        source, _, target, permutation = match.groups()
        key = (int(source), int(target), permutation)
        require(key not in forest_presentations, "FOREST_PRESENTATION_DUPLICATE", key)
        forest_presentations[key] = root
    require(set(forest_presentations) == set(generated_presentations),
            "FOREST_RESTORATION_PRESENTATION_BIJECTION")
    require(forest["census"]["member_roots"] == 2_540 and
            forest["census"]["canonical_restoration_parents"] == 997 and
            forest["census"]["first_children"] == 36_568,
            "FOREST_CENSUS")
    active_path = PROJECT / "restoration/restoration_ledger.jsonl.gz"
    active_rows = list(ledger_rows(active_path))
    active_roots = {row["root_id"] for row in active_rows}
    require(active_roots == forest_roots, "ACTIVE_RESTORATION_ROOT_SET")
    first_active = [row for row in active_rows if row["layer"] == 1]
    require(len(first_active) == 36_568, "ACTIVE_FIRST_LAYER_CENSUS")
    forest_legacy = collections.Counter(row["row_sha256"] for row in forest["first_coverage"])
    active_legacy = collections.Counter(row["legacy_row_sha256"] for row in first_active)
    require(active_legacy == forest_legacy, "ACTIVE_LEGACY_CROSSWALK")
    registry = load_gzip_json(PROJECT / "restoration/restoration_proof_registry.json.gz")
    proof_ids = {proof_id for group in registry["proofs"].values() for proof_id in group}
    proof_counts = collections.Counter()
    for row in first_active:
        require(row["active_k3p_status"] == "separated", "ACTIVE_RESTORATION_UNRESOLVED")
        require(row["uses_frozen_algebra"] is False, "ACTIVE_RESTORATION_FROZEN_ALGEBRA")
        require(row["proof_id"] in proof_ids, "ACTIVE_RESTORATION_PROOF_ID")
        proof_counts[row["proof_kind"]] += 1
    require(proof_counts == collections.Counter({
        "displayed_quartet_mismatch": 35_758,
        "k3p_tree_sunlet_sos": 606,
        "k3p_exact_multihomogeneous_quadratic": 148,
        "k3p_direct_marginal_quartic": 56,
    }), "ACTIVE_RESTORATION_PROOF_COUNTS", proof_counts)
    independent = json.loads((PROJECT / "restoration/K3P_RESTORATION_INDEPENDENT_VERIFICATION.json").read_text())
    mutation = json.loads((PROJECT / "restoration/K3P_RESTORATION_MUTATION_CERTIFICATE.json").read_text())
    require(independent["status"] == "PASS", "RESTORATION_INDEPENDENT_STATUS")
    require(mutation["status"] == "PASS" and mutation["mutation_count"] == 20 and
            mutation["rejected"] == 20 and mutation["accepted"] == 0,
            "RESTORATION_MUTATION_STATUS")

    contract_path = PROJECT / "input_frozen/model_independent_topology_package/anchor_inputs/probe_input_contract.json"
    contract = json.loads(contract_path.read_text())
    four = [anchor for anchor in contract["anchors"]
            if anchor["origin"] in {"four_port_direct_physical", "four_port_restored_physical_k5"}]
    require(len(four) == 43, "FOUR_PORT_PROBE_ANCHOR_CENSUS")
    origin_counts, relation_counts = collections.Counter(), collections.Counter()
    for anchor in four:
        raw_id = anchor["locator"]["raw_id"]
        require(raw_id in generated_rows, "PROBE_RAW_ID")
        row = generated_rows[raw_id]
        require(row["source_index"] == anchor["locator"]["source_index"] and
                row["target_index"] == anchor["locator"]["target_index"] and
                row["permutation_index"] == anchor["locator"]["permutation_index"],
                "PROBE_LOCATOR", anchor["anchor_id"])
        expected_category = "isomorphic" if anchor["relation"] == "isomorphic" else "ordinary_triangle"
        require(row["category"] == expected_category and row["graph_relation"] == anchor["relation"],
                "PROBE_RELATION", anchor["anchor_id"])
        origin_counts[anchor["origin"]] += 1
        relation_counts[anchor["relation"]] += 1
    require(origin_counts == collections.Counter({"four_port_direct_physical": 26,
                                                  "four_port_restored_physical_k5": 17}),
            "PROBE_ORIGIN_COUNTS")
    require(relation_counts == collections.Counter({"isomorphic": 26, "triangle": 17}),
            "PROBE_RELATION_COUNTS")
    input_replay = json.loads((PROJECT / "input_frozen/model_independent_topology_package/anchor_inputs/probe_input_independent_verification.json").read_text())
    semantic = json.loads((PROJECT / "probes/K3P_PROBE_SEMANTIC_VERIFICATION.json").read_text())
    require(input_replay["status"] == "PASS" and input_replay["anchors_reconstructed"] == 176 and
            input_replay["unresolved"] == 0, "PROBE_INPUT_REPLAY")
    require(semantic["status"] == "PASS" and semantic["independence"]["producer_imported"] is False and
            semantic["independence"]["atlas_imported"] is False and
            semantic["coverage"]["all_probe_rows"] == 574_535,
            "PROBE_SEMANTIC_REPLAY")
    return {"restoration_presentations": 2_540,
            "restoration_canonical_classes": 997,
            "restoration_first_children": 36_568,
            "probe_four_port_anchors": 43}


def logical_payload(value):
    if isinstance(value, dict):
        return {key: logical_payload(item) for key, item in value.items()
                if key not in {"payload_sha256", "operational"}
                and not key.endswith("_path")}
    if isinstance(value, list):
        return [logical_payload(item) for item in value]
    return value


def write_report(path, summary, bindings, runtime, artifact_root):
    report = {
        "schema": "k3p-full-four-port-independent-verification-v1",
        "status": "PASS",
        "conclusion": "The complete 405,216-record primitive four-port universe was independently replayed; exactly 27,834 presentations survive topology, the final residue is 40=38+2 in fourteen canonical orbits, and every restoration/probe handoff is actively bound.",
        "independence": {
            "producer_imported": False,
            "historical_atlas_core_imported": False,
            "frozen_fourteen_orbit_lock_read": False,
            "primitive_graph_grammar_reconstructed": True,
        },
        "syzygy_rank_upper_proof": {
            "coefficientwise_identity": "Every kernel vector of A is a literal polynomial vector field V with J_f V=0 coefficient by coefficient.",
            "linear_algebra_identity": "dim E(ker A)=rank([A;E])-rank(A), by rank-nullity applied to E restricted to ker A.",
            "generic_open_argument": "The verified evaluation rank has a nonzero minor. Its entries are polynomial/rational functions of the strict parameters, so that minor remains nonzero on a nonempty Zariski-open set. Thus p-dim E(ker A) is a generic rank upper. A sampled Jacobian rank is used only as a nonzero-minor lower bound, never as an upper bound.",
        },
        "counts": {
            "raw": 405_216, "post_topology": 27_834,
            "compatible_target_permutation_keys": 13_686,
            "unique_map_descriptors": 4_379,
            "residue": 40, "orbit_members": 38, "sink_swaps": 2,
            "canonical_orbits": 14,
            **bindings,
        },
        "bindings": {
            "independent_verifier_sha256": file_hash(Path(__file__)),
            "independent_core_sha256": file_hash(HERE / "independent_replay_core.py"),
            "mutation_runner_sha256": file_hash(HERE / "test_full_four_port_mutations.py"),
            "producer_sha256": file_hash(HERE / "generate_full_four_port_replay.py"),
            "summary_sha256": file_hash(artifact_root / "FULL_FOUR_PORT_REPLAY.json"),
            "artifacts": summary["artifacts"],
        },
        "verified_summary_payload_sha256": summary["payload_sha256_without_hash"],
        "operational": {"runtime_seconds": runtime},
    }
    report["payload_sha256"] = canonical_hash(logical_payload(report))
    temporary = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def focused_raw(root, raw_id, summary, rank_records, upper_records, class_records):
    rows = verify_ledger_structure(root, summary)
    sources = core.sources()
    targets = core.targets(4, True) + core.targets(4, False)
    permutations = tuple(itertools.permutations(range(4)))
    source_index = raw_id // RAW_PER_SOURCE
    within = raw_id % RAW_PER_SOURCE
    target_index, permutation_index = divmod(within, 24)
    permutation = permutations[permutation_index]
    source_signature = core.topology_signature(sources[source_index].graph)
    target_signature = core.topology_signature(targets[target_index].graph)
    accepted, reason = core.immediate_compatible(source_signature,
        core.permute_signature(target_signature, permutation))
    observed = rows[raw_id]
    if not accepted:
        require(observed["category"] == "topology_excluded" and
                observed["topology_exclusion_reason"] == reason, "FOCUS_RAW_TOPOLOGY")
        return
    source_descriptor = core.compile_descriptor(sources[source_index].graph)
    target_descriptor = core.compile_descriptor(core.relabel(targets[target_index], permutation).graph)
    source_digest, target_digest = map(core.descriptor_hash, (source_descriptor, target_descriptor))
    rank = {row["descriptor_sha256"]: row["rank"] for row in rank_records}
    upper = {row["descriptor_sha256"]: row for row in upper_records}
    if rank[target_digest] < rank[source_digest] and upper[target_digest]["certified_rank_upper"] < rank[source_digest]:
        require(observed["category"] == "rank_excluded", "FOCUS_RAW_RANK")
        return
    quadratic = quadratic_full(source_descriptor, target_descriptor, source_index)
    if quadratic is not None:
        category = "quadratic_separated"
    else:
        h14 = h14_full(source_descriptor, target_descriptor, source_index) if rank[target_digest] < rank[source_digest] else None
        if h14 is not None:
            category = "h14_marginal_separated"
        else:
            relabelled = core.relabel(targets[target_index], permutation)
            relation = core.mixed_relation(sources[source_index].graph, core.selected_graph(relabelled))
            category = ("isomorphic" if relation == "isomorphic" else
                        "ordinary_triangle" if relation == "triangle" else
                        "restoration_obligation" if targets[target_index].dummy_labels else
                        "post_quadratic_residue")
    require(observed["category"] == category, "FOCUS_RAW_CATEGORY", (raw_id, category, observed["category"]))


def focused_upper(digest, rank_records, upper_records, class_records):
    targets = core.targets(4, True) + core.targets(4, False)
    descriptor = None
    for record in class_records:
        if record["target_descriptor_sha256"] != digest:
            continue
        member = record["members"][0]
        descriptor = core.compile_descriptor(core.relabel(
            targets[member["target_index"]], tuple(member["port_permutation"])).graph)
        break
    if descriptor is None:
        for source in core.sources():
            candidate = core.compile_descriptor(source.graph)
            if core.descriptor_hash(candidate) == digest:
                descriptor = candidate
                break
    require(descriptor is not None and core.descriptor_hash(descriptor) == digest,
            "FOCUSED_UPPER_DESCRIPTOR", digest)
    rank = {row["descriptor_sha256"]: row["rank"] for row in rank_records}
    stored = {row["descriptor_sha256"]: row for row in upper_records}
    require(digest in stored and digest in rank, "FOCUSED_UPPER_RECORD", digest)
    computed = core.syzygy_rank_upper(descriptor, include_evaluation_witness=True)
    expected = {**{key: value for key, value in computed.items()
                   if not key.startswith("evaluation_")}, "descriptor_sha256": digest,
                "point_minor_rank": rank[digest]}
    require(stored[digest] == expected, "FOCUSED_UPPER_SEMANTICS", digest)
    require(Q(computed["evaluation_image_minor_determinant"]) != 0,
            "FOCUSED_UPPER_MINOR_WITNESS", digest)


def main():
    if not __debug__ or sys.flags.optimize:
        fail("OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACTS)
    parser.add_argument("--report", type=Path, default=HERE / "INDEPENDENT_FULL_FOUR_PORT_VERIFICATION.json")
    parser.add_argument("--structure-only", action="store_true")
    parser.add_argument("--focus-restoration", action="store_true")
    parser.add_argument("--focus-quotient", action="store_true")
    parser.add_argument("--focus-raw-id", type=int)
    parser.add_argument("--focus-upper-hash")
    args = parser.parse_args()
    started = time.monotonic()
    root = args.artifact_root.resolve()
    summary, rank_records, upper_records, class_records, quotient = verify_artifact_envelope(root)
    if args.structure_only:
        verify_ledger_structure(root, summary)
        print("K3P_FULL_FOUR_PORT_INDEPENDENT_STRUCTURE_PASS")
        return
    if args.focus_restoration:
        rows = verify_ledger_structure(root, summary)
        verify_restoration_and_probe_bindings(rows)
        print("K3P_FULL_FOUR_PORT_FOCUSED_RESTORATION_PASS")
        return
    if args.focus_raw_id is not None:
        require(0 <= args.focus_raw_id < RAW_TOTAL, "FOCUS_RAW_RANGE")
        focused_raw(root, args.focus_raw_id, summary, rank_records, upper_records, class_records)
        print("K3P_FULL_FOUR_PORT_FOCUSED_RAW_PASS")
        return
    if args.focus_upper_hash:
        verify_ledger_structure(root, summary)
        focused_upper(args.focus_upper_hash, rank_records, upper_records, class_records)
        print("K3P_FULL_FOUR_PORT_FOCUSED_UPPER_PASS")
        return

    sources, targets, permutations, target_signatures, compatible = build_universe(summary)
    source_descriptors, target_descriptors, descriptors = compile_all(
        sources, targets, compatible, summary)
    ranks = verify_rank_registry(rank_records, descriptors, summary)
    upper = verify_upper_registry(upper_records, descriptors, ranks, summary)
    raw, excluded = classify(sources, targets, compatible, source_descriptors,
                             target_descriptors, ranks, upper_records,
                             class_records, summary)
    verify_full_ledger(root, sources, targets, permutations, target_signatures,
                       source_descriptors, target_descriptors, ranks, upper,
                       raw, excluded, summary)
    derived = derive_quotient(sources, targets, permutations, source_descriptors,
                              target_descriptors, ranks, raw)
    require(derived == quotient, "DERIVED_QUOTIENT_SEMANTICS")
    if args.focus_quotient:
        print("K3P_FULL_FOUR_PORT_FOCUSED_QUOTIENT_PASS")
        return
    rows = {row["raw_id"]: row for row in ledger_rows(root / "full_directional_ledger.jsonl.gz")}
    bindings = verify_restoration_and_probe_bindings(rows)
    runtime = time.monotonic() - started
    write_report(args.report.resolve(), summary, bindings, runtime, root)
    print("K3P_FULL_FOUR_PORT_INDEPENDENT_VERIFICATION_PASS")
    print(json.dumps({"runtime_seconds": runtime,
                      "report": str(args.report.resolve())}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except core.ReplayFailure as error:
        print(f"K3P_FULL_FOUR_PORT_INDEPENDENT_VERIFICATION_FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
