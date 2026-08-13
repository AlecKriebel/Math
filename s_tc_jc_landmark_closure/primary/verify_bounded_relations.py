#!/usr/bin/env python3
"""Exact primary replay of graph-bound unequal/equal bounded relations."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path

from atlas_compiler import load_bit_cache, stable_hash
from graph_model import (
    RootedGraph,
    canonical_mixed,
    mixed_local_strong,
    rooted_validation,
    sd0,
    t_quotient,
)
from hard_cover_compiler import deck_signature, load_invariants
from jc_tensor import canonicalize_rows, pullback, raw_descriptor
from sign_certificate import certify as certify_sign


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent


def bounded_full_deck(graph: RootedGraph, port_count: int):
    """Replay the bounded-atlas descriptor convention exactly.

    The bounded compiler records its rooted physical descriptor before the
    later hard-cover root-edge product normalization.  Keeping this function
    local prevents a verifier from silently changing conventions when the
    arbitrary-root hard cover is strengthened.
    """
    labels = tuple(f"L_{index}" for index in range(port_count))
    retics, signatures = raw_descriptor(graph, labels)
    answer = []
    for quartet in combinations(range(port_count), 4):
        rows = []
        for signature in signatures:
            moved = []
            for mask in signature:
                new_mask = 0
                for new_index, old_index in enumerate(quartet):
                    if mask & (1 << old_index):
                        new_mask |= 1 << new_index
                moved.append(new_mask)
            rows.append(tuple(moved))
        answer.append(canonicalize_rows(retics, rows))
    return tuple(answer)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_stream(path: Path, key: str):
    rows = {}
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for line in handle:
            digest.update(line)
            row = json.loads(line)
            identifier = row[key]
            if identifier in rows:
                raise AssertionError((path, "duplicate", identifier))
            rows[identifier] = row
    return rows, digest.hexdigest()


def graph_from_row(row: dict) -> RootedGraph:
    payload = row["rooted_graph"]
    return RootedGraph(
        int(payload["root"]),
        tuple((int(v), str(label)) for v, label in payload["labels"]),
        tuple((int(u), int(v)) for u, v in payload["arcs"]),
    )


def poly_from_row(row: dict):
    return {
        tuple(int(value) for value in exponents): int(coefficient)
        for exponents, coefficient in row["terms"]
    }


def verify_run(run: dict, bit_cache_path: Path):
    n = int(run["outgoing"])
    assert run.get("descriptor_mask_convention") == (
        "rooted_selected_side_masks_before_zero_sum_complement_zip"
    )
    cert = run["bounded_relation_certificate"]
    relation_path = PROJECT / cert["relation_path"]
    graph_path = PROJECT / cert["graph_library_path"]
    polynomial_path = PROJECT / cert["polynomial_library_path"]
    sign_path = PROJECT / cert["sign_library_path"]
    relations, relation_sha = read_stream(relation_path, "relation_id")
    graphs, graph_sha = read_stream(graph_path, "graph_id")
    polynomials, polynomial_sha = read_stream(polynomial_path, "polynomial_id")
    signs = json.loads(sign_path.read_text())
    assert relation_sha == cert["relation_stream_sha256"]
    assert graph_sha == cert["graph_library_stream_sha256"]
    assert polynomial_sha == cert["polynomial_library_stream_sha256"]
    assert sha256(sign_path) == cert["sign_library_sha256"]
    assert len(relations) == cert["canonical_decorated_relations"]
    assert len(graphs) == cert["graph_library_records"]
    assert len(polynomials) == cert["polynomial_library_records"]

    graph_objects = {}
    mixed_codes = {}
    t_codes = {}
    for graph_id, row in graphs.items():
        payload = row["rooted_graph"]
        assert stable_hash(payload) == graph_id
        graph = graph_from_row(row)
        valid, problems = rooted_validation(graph)
        assert valid == row["rooted_valid"]
        assert list(problems) == row["rooted_validation_problems"]
        mixed = sd0(graph)
        code, transport = canonical_mixed(mixed)
        t_code, t_transport = canonical_mixed(t_quotient(mixed))
        assert code == row["standard_mixed_code"]
        assert t_code == row["t_quotient_code"]
        assert tuple(sorted(transport.items())) == tuple(
            tuple(pair) for pair in row["raw_mixed_vertex_to_canonical"]
        )
        assert tuple(sorted(t_transport.items())) == tuple(
            tuple(pair) for pair in row["raw_t_quotient_vertex_to_canonical"]
        )
        assert valid and mixed_local_strong(mixed) == row["standard_strong_local"]
        graph_objects[graph_id] = graph
        mixed_codes[graph_id] = code
        t_codes[graph_id] = t_code

    poly_objects = {}
    for polynomial_id, row in polynomials.items():
        payload = {
            "schema": row["schema"],
            "variable_count": row["variable_count"],
            "terms": row["terms"],
        }
        assert stable_hash(payload) == polynomial_id
        poly = poly_from_row(row)
        exact_hash = hashlib.sha256(
            repr(tuple(sorted(poly.items()))).encode()
        ).hexdigest()
        assert exact_hash == row["exact_polynomial_sha256"]
        poly_objects[polynomial_id] = poly

    invariants = load_invariants()
    bit_cache = load_bit_cache(bit_cache_path)
    descriptor_cache = {}

    def descriptors(graph_id):
        if graph_id not in descriptor_cache:
            descriptor_cache[graph_id] = bounded_full_deck(
                graph_objects[graph_id], n + 1
            )
        return descriptor_cache[graph_id]

    counts = Counter()
    referenced_polynomials = set()
    referenced_signs = set()
    rebuilt_signs = {}
    for relation_number, (relation_id, row) in enumerate(relations.items(), 1):
        if relation_number % 1000 == 0:
            print(json.dumps({
                "bounded_relation_replay_progress": {
                    "outgoing": n,
                    "relations": relation_number,
                    "total_relations": len(relations),
                    "descriptor_cache": len(descriptor_cache),
                }
            }, sort_keys=True), flush=True)
        assert int(row["schema"]) == 3
        binding = row.pop("binding_sha256")
        assert stable_hash(row) == binding
        row["binding_sha256"] = binding
        source_id = row["source_graph_id"]
        target_id = row["target_completion_graph_id"]
        selected_target_id = row["target_selected_graph_id"]
        relation_payload = {
            "direction": "source_precedes_target",
            "outgoing": n,
            "source_rooted_graph_id": source_id,
            "target_completion_rooted_graph_id": target_id,
            "target_selected_rooted_graph_id": selected_target_id,
            "source_side_coloured_mixed_graph": mixed_codes[source_id],
            "target_completion_side_coloured_mixed_graph": mixed_codes[target_id],
            "target_selected_side_coloured_mixed_graph": (
                mixed_codes[selected_target_id]
                if selected_target_id is not None else None
            ),
            "port_matching": tuple(
                (f"L_{index}", f"L_{index}") for index in range(n + 1)
            ),
        }
        assert stable_hash(relation_payload) == relation_id
        source_deck = descriptors(source_id)
        target_deck = descriptors(target_id)
        assert stable_hash(source_deck) == row["source_descriptor_deck_sha256"]
        assert stable_hash(target_deck) == row["target_descriptor_deck_sha256"]
        source_signature = deck_signature(
            source_deck, invariants, bit_cache
        )
        target_signature = deck_signature(
            target_deck, invariants, bit_cache
        )
        assert hashlib.sha256(str(source_signature).encode()).hexdigest() == row[
            "source_signature_sha256"
        ]
        assert hashlib.sha256(str(target_signature).encode()).hexdigest() == row[
            "target_signature_sha256"
        ]
        for coverage in row["raw_coverage"]:
            assert coverage["source_graph_id"] == source_id
            assert coverage["target_completion_graph_id"] == target_id
            assert coverage["target_selected_graph_id"] == selected_target_id

        classification = row["classification"]
        counts[classification] += 1
        if classification == "strict_open_cube_separation":
            witness = row["witness"]
            chunk = int(witness["quartet_chunk"])
            invariant = int(witness["invariant_index"])
            source_poly = pullback(source_deck[chunk], invariants[invariant])
            target_poly = pullback(target_deck[chunk], invariants[invariant])
            assert not source_poly and target_poly
            polynomial_id = witness["target_pullback_id"]
            assert target_poly == poly_objects[polynomial_id]
            exact_hash = hashlib.sha256(
                repr(tuple(sorted(target_poly.items()))).encode()
            ).hexdigest()
            assert exact_hash == witness["target_pullback_exact_sha256"]
            published = signs[exact_hash]
            if exact_hash not in rebuilt_signs:
                # The certifier's in-memory proof uses tuples for ordered
                # arrays, whereas the published JSON necessarily reloads
                # those arrays as lists.  Compare the complete normalized
                # JSON value; do not weaken any polynomial, factor, sign, or
                # ordered-array field.
                rebuilt_signs[exact_hash] = json.loads(json.dumps(
                    certify_sign(target_poly), sort_keys=True
                ))
            rebuilt = rebuilt_signs[exact_hash]
            assert rebuilt == {
                key: value for key, value in published.items()
                if key not in {"exact_polynomial_sha256", "polynomial_id"}
            }
            assert rebuilt["certified"]
            referenced_polynomials.add(polynomial_id)
            referenced_signs.add(exact_hash)
        elif classification == "isomorphism_or_T":
            assert source_signature == target_signature
            assert selected_target_id is not None
            assert t_codes[source_id] == t_codes[selected_target_id]
            assert row["t_quotient_code_sha256"] == hashlib.sha256(
                t_codes[source_id].encode()
            ).hexdigest()
        elif classification == "pending_support_completion":
            assert source_signature == target_signature
            assert selected_target_id is None
        else:
            raise AssertionError((relation_id, classification))

    assert referenced_polynomials == set(polynomials)
    assert referenced_signs == set(signs)
    expected_counts = {
        key: value for key, value in cert["counts"].items()
        if "_to_" not in key
    }
    assert dict(sorted(counts.items())) == expected_counts
    assert not cert["failure_count"] and not cert["failures"]
    return {
        "outgoing": n,
        "relations": len(relations),
        "graphs": len(graphs),
        "polynomials": len(polynomials),
        "counts": dict(sorted(counts.items())),
        "status": "EXACTLY VERIFIED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path)
    parser.add_argument("--bit-cache", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.summary.read_text())
    results = [verify_run(run, args.bit_cache) for run in payload["runs"]]
    print(json.dumps({"status": "EXACTLY VERIFIED", "runs": results}, sort_keys=True))


if __name__ == "__main__":
    main()
