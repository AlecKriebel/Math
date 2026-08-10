#!/usr/bin/env python3
"""Exact structural and graph-to-polynomial replay of hard-cover artifacts.

This is the primary verifier.  The release also requires a clean-room
implementation under ``reviews/`` that imports none of these modules.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
import gzip
import hashlib
import json
from pathlib import Path

from atlas_compiler import stable_hash
from graph_model import (
    RootedGraph,
    canonical_mixed,
    mixed_local_strong,
    rooted_validation,
    sd0,
    t_quotient,
)
from hard_cover_compiler import full_deck, load_invariants, quick_power_sign
from jc_tensor import pullback
from sign_certificate import certify as certify_sign


def read_stream(path: Path, key: str):
    rows = {}
    hasher = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for line in handle:
            hasher.update(line)
            row = json.loads(line)
            identity = row[key]
            if identity in rows:
                raise AssertionError((path, "duplicate", identity))
            rows[identity] = row
    return rows, hasher.hexdigest()


def graph_from_payload(payload):
    return RootedGraph(
        int(payload["root"]),
        tuple((int(v), str(label)) for v, label in payload["labels"]),
        tuple((int(u), int(v)) for u, v in payload["arcs"]),
    )


def poly_from_row(row):
    return {
        tuple(int(value) for value in exponents): int(coefficient)
        for exponents, coefficient in row["terms"]
    }


def verify_run(summary: dict, project: Path):
    assert summary.get("descriptor_cache_scope") == (
        "selected_port_count_and_exact_rooted_graph_id"
    )
    assert summary.get("descriptor_mask_normalization") == (
        "minimum_of_quartet_side_and_complement_on_zero_sum_characters"
    )
    relation_path = project / summary["relation_path"]
    graph_path = project / summary["graph_library_path"]
    polynomial_path = project / summary["polynomial_library_path"]
    root_path = project / summary["root_case_path"]

    states, state_sha = read_stream(relation_path, "state_id")
    graphs, graph_sha = read_stream(graph_path, "graph_id")
    polynomials, polynomial_sha = read_stream(polynomial_path, "polynomial_id")
    roots, root_sha = read_stream(root_path, "root_case_id")
    assert state_sha == summary["relation_stream_sha256"]
    assert graph_sha == summary["graph_library_stream_sha256"]
    assert polynomial_sha == summary["polynomial_library_stream_sha256"]
    assert root_sha == summary["root_case_stream_sha256"]
    assert len(states) == summary["canonical_restored_relations"]
    assert len(graphs) == summary["graph_library_records"]
    assert len(polynomials) == summary["polynomial_library_records"]
    assert len(roots) == summary["root_case_records"]

    graph_objects = {}
    graph_codes = {}
    for graph_id, row in graphs.items():
        payload = row["rooted_graph"]
        assert stable_hash(payload) == graph_id
        graph = graph_from_payload(payload)
        valid, problems = rooted_validation(graph)
        assert valid == row["rooted_valid"] and list(problems) == row[
            "rooted_validation_problems"
        ]
        mixed = sd0(graph)
        code, transport = canonical_mixed(mixed)
        t_code, _ = canonical_mixed(t_quotient(mixed))
        assert code == row["standard_mixed_code"]
        assert hashlib.sha256(code.encode()).hexdigest() == row["standard_mixed_code_sha256"]
        assert t_code == row["t_quotient_code"]
        assert hashlib.sha256(t_code.encode()).hexdigest() == row["t_quotient_code_sha256"]
        assert tuple(sorted(transport.items())) == tuple(
            tuple(pair) for pair in row["raw_mixed_vertex_to_canonical"]
        )
        assert mixed_local_strong(mixed) == row["standard_strong_local"]
        assert valid and row["standard_strong_local"]
        graph_objects[graph_id] = graph
        graph_codes[graph_id] = code

    poly_objects = {}
    for polynomial_id, row in polynomials.items():
        payload = {
            "schema": row["schema"],
            "variable_count": row["variable_count"],
            "terms": row["terms"],
        }
        assert stable_hash(payload) == polynomial_id
        poly = poly_from_row(row)
        assert poly
        assert all(len(monomial) == row["variable_count"] for monomial in poly)
        poly_objects[polynomial_id] = poly

    invariant_templates = load_invariants()
    descriptor_cache = {}
    standard_tensor_descriptors = {}

    def descriptors(graph_id, p):
        key = graph_id, p
        if key not in descriptor_cache:
            deck = full_deck(graph_objects[graph_id], p)
            descriptor_cache[key] = deck
            # Complement normalization must make the selected JC tensor
            # independent of the admissible root placement representing one
            # labelled standard mixed graph.  This assertion detects both a
            # missing zero-sum quotient and presentation-dependent cache
            # contamination on every graph actually cited by a state.
            standard_key = graph_codes[graph_id], p
            prior = standard_tensor_descriptors.setdefault(standard_key, deck)
            assert prior == deck, (
                "root-dependent normalized descriptor",
                graph_id,
                p,
            )
        return descriptor_cache[key]

    path_ids = set()
    parent_ids = []
    path_index = {}
    root_coverage = Counter()
    counts = Counter()
    for state_id, row in states.items():
        binding = row.pop("binding_sha256")
        assert stable_hash(row) == binding
        row["binding_sha256"] = binding
        source_id = row["source_graph_id"]
        target_id = row["target_graph_id"]
        assert source_id in graphs and target_id in graphs
        p = int(row["selected_port_count"])
        expected_matching = [[f"L_{i}", f"L_{i}"] for i in range(p)]
        assert row["port_matching"] == expected_matching
        state_payload = {
            "fixed_full_root_case_id": row["fixed_full_root_case_id"],
            "selected_port_count": p,
            "source_rooted_graph_id": source_id,
            "target_rooted_graph_id": target_id,
            "source_mixed_code": graph_codes[source_id],
            "target_completion_mixed_code": graph_codes[target_id],
            "remaining_target_roles": tuple(row["remaining_target_roles"]),
            "port_matching": tuple(range(p)),
        }
        assert stable_hash(state_payload) == state_id
        assert len(row["remaining_target_roles"]) == row["remaining_target_role_count"]
        assert row["source_mixed_code_sha256"] == hashlib.sha256(
            graph_codes[source_id].encode()
        ).hexdigest()
        assert row["target_completion_mixed_code_sha256"] == hashlib.sha256(
            graph_codes[target_id].encode()
        ).hexdigest()

        terminal = row["terminal_classification"]
        counts[terminal] += 1
        children = tuple(row["children"])
        if terminal == "refined_by_next_restoration":
            assert children
        else:
            assert not children
        for child in children:
            assert child in states
            assert states[child]["selected_port_count"] == p + 1
            assert states[child]["remaining_target_role_count"] == row[
                "remaining_target_role_count"
            ] - 1

        witness = row["probe_witness"]
        classification = row["probe_classification"]
        if classification == "generic_polynomial_separation":
            polynomial_id = witness["source_pullback_id"]
            assert polynomial_id in poly_objects and witness["target_pullback"] == "0"
            chunk, inv = witness["quartet_chunk"], witness["invariant_index"]
            actual = pullback(descriptors(source_id, p)[chunk], invariant_templates[inv])
            target = pullback(descriptors(target_id, p)[chunk], invariant_templates[inv])
            assert actual == poly_objects[polynomial_id] and not target
        elif classification == "strict_open_cube_separation":
            polynomial_id = witness["target_pullback_id"]
            assert polynomial_id in poly_objects and witness["source_pullback"] == "0"
            chunk, inv = witness["quartet_chunk"], witness["invariant_index"]
            source = pullback(descriptors(source_id, p)[chunk], invariant_templates[inv])
            actual = pullback(descriptors(target_id, p)[chunk], invariant_templates[inv])
            assert not source and actual == poly_objects[polynomial_id], {
                "state_id": state_id,
                "source_graph_id": source_id,
                "target_graph_id": target_id,
                "selected_port_count": p,
                "quartet_chunk": chunk,
                "invariant_index": inv,
                "polynomial_id": polynomial_id,
                "source_term_count": len(source),
                "actual_term_count": len(actual),
                "stored_term_count": len(poly_objects[polynomial_id]),
                "actual_exact_sha256": hashlib.sha256(
                    repr(tuple(sorted(actual.items()))).encode()
                ).hexdigest(),
                "stored_exact_sha256": hashlib.sha256(
                    repr(tuple(sorted(poly_objects[polynomial_id].items()))).encode()
                ).hexdigest(),
            }
            published_sign = witness["target_sign_certificate"]
            # Never trust a stored ``certified`` flag.  Rebuild the exact
            # sparse-coefficient proof, or refactor and recompute every
            # Bernstein coefficient when the terminal factor pass was used.
            if "factors" in published_sign:
                rebuilt_sign = certify_sign(actual, max_elevation=5)
            else:
                rebuilt_sign = quick_power_sign(actual)
            normalized_rebuilt_sign = json.loads(json.dumps(rebuilt_sign))
            assert normalized_rebuilt_sign == published_sign, {
                "state_id": state_id,
                "polynomial_id": polynomial_id,
                "rebuilt_sign": normalized_rebuilt_sign,
                "published_sign": published_sign,
            }
            assert rebuilt_sign["certified"]

        for coverage in row["raw_coverage"]:
            assert coverage["root_case_id"] == row["fixed_full_root_case_id"]
            assert coverage["canonical_state_id"] == state_id
            assert coverage["source_graph_id"] == source_id
            assert coverage["target_graph_id"] == target_id
            assert tuple(coverage["child_state_ids"]) == children
            payload = dict(coverage)
            path_id = payload.pop("path_binding_id")
            payload_sha = payload.pop("path_binding_payload_sha256")
            payload.pop("child_state_ids")
            assert stable_hash(payload) == path_id == payload_sha
            path_ids.add(path_id)
            if path_id in path_index:
                raise AssertionError(("duplicate path binding", path_id))
            path_index[path_id] = (state_id, coverage)
            parent_ids.append(coverage["parent_path_binding_id"])
            root_id = coverage["root_case_id"]
            assert root_id in roots
            root_coverage[root_id] += 1
            assert tuple(coverage["dummy_order"]) == tuple(
                roots[root_id]["root_case"]["target_dummy_roles"]
            )
            assert len(coverage["restoration_path"]) == p - summary[
                "selected_port_count"
            ]

    assert dict(sorted(counts.items())) == summary["counts"]
    assert not any(key.startswith("unresolved") for key in counts)
    assert not any("non_T" in key for key in counts)
    for parent in parent_ids:
        assert parent is None or parent in path_ids

    children_by_parent_path = {}
    for child_state_id, child_row in states.items():
        for child_coverage in child_row["raw_coverage"]:
            parent_path = child_coverage["parent_path_binding_id"]
            if parent_path is None:
                continue
            children_by_parent_path.setdefault(parent_path, set()).add(
                child_state_id
            )
            parent_state_id, parent_coverage = path_index[parent_path]
            assert child_coverage["parent_state_id"] == parent_state_id
            assert child_coverage["root_case_id"] == parent_coverage["root_case_id"]
            assert tuple(child_coverage["restoration_path"]) == tuple(
                parent_coverage["restoration_path"]
            ) + (child_coverage["restoration_path"][-1],)
    for path_id, (state_id, coverage) in path_index.items():
        expected = set(coverage["child_state_ids"])
        actual = children_by_parent_path.get(path_id, set())
        assert actual == expected, (
            "path-specific child coverage mismatch",
            path_id,
            sorted(expected - actual),
            sorted(actual - expected),
        )

    entries = set()
    for root_id, row in roots.items():
        assert stable_hash(row["root_case"]) == root_id
        entry = tuple(row["entry_state_ids"])
        assert entry and all(state in states for state in entry)
        entries.update(entry)
        assert root_coverage[root_id]
        assert any(
            coverage["root_case_id"] == root_id
            for state in entry
            for coverage in states[state]["raw_coverage"]
        )

    reached = set(entries)
    queue = deque(entries)
    while queue:
        state = queue.popleft()
        for child in states[state]["children"]:
            if child not in reached:
                reached.add(child)
                queue.append(child)
    assert reached == set(states)
    return {
        "states": len(states),
        "graphs": len(graphs),
        "polynomials": len(polynomials),
        "root_cases": len(roots),
        "standard_tensor_descriptor_orbits": len(standard_tensor_descriptors),
        "counts": dict(sorted(counts.items())),
        "status": "EXACTLY VERIFIED",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    summary_path = args.summary.resolve()
    payload = json.loads(summary_path.read_text())
    project = Path(__file__).resolve().parent.parent
    results = [verify_run(row["hard_cover"], project) for row in payload["runs"]]
    result = {
        "schema": "schema3-hard-cover-primary-replay-v1",
        "status": "EXACTLY_VERIFIED",
        "summary": str(summary_path.relative_to(project)),
        "summary_sha256": hashlib.sha256(summary_path.read_bytes()).hexdigest(),
        "runs": results,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
