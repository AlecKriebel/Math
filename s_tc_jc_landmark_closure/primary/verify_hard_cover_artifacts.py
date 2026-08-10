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

    def descriptors(graph_id, p):
        key = graph_id, p
        if key not in descriptor_cache:
            descriptor_cache[key] = full_deck(graph_objects[graph_id], p)
        return descriptor_cache[key]

    path_ids = set()
    parent_ids = []
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
            "selected_port_count": p,
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
            assert not source and actual == poly_objects[polynomial_id]
            published_sign = witness["target_sign_certificate"]
            # Never trust a stored ``certified`` flag.  Rebuild the exact
            # sparse-coefficient proof, or refactor and recompute every
            # Bernstein coefficient when the terminal factor pass was used.
            if "factors" in published_sign:
                rebuilt_sign = certify_sign(actual, max_elevation=5)
            else:
                rebuilt_sign = quick_power_sign(actual)
            assert rebuilt_sign == published_sign
            assert rebuilt_sign["certified"]

        for coverage in row["raw_coverage"]:
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
        "counts": dict(sorted(counts.items())),
        "status": "EXACTLY VERIFIED",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.summary.read_text())
    project = Path(__file__).resolve().parent.parent
    results = [verify_run(row["hard_cover"], project) for row in payload["runs"]]
    print(json.dumps({"status": "EXACTLY VERIFIED", "runs": results}, sort_keys=True))


if __name__ == "__main__":
    main()
