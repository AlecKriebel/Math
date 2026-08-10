#!/usr/bin/env python3
"""Independent terminal algebra/topology audit for merged schema-3 n=3.

This audit consumes primary JSONL only as a comparison stream.  It rebuilds
every displayed-tree JC descriptor from the exact rooted graphs, derives its
own coordinate relations, expands those relations on every exact graph pair,
and proves every claimed strict sign with an independent QQ-factorization and
Bernstein-coefficient certificate.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import argparse
import gzip
import hashlib
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from audit_candidate_stream import load_family, polynomial_library
from derived_invariants import derive_pair_separator_on_quartet, relation_poly
from family_engine import find_generic_identity_separator_on_quartet
from graph_model import digest, mixed_code, semidirected, stable_json
from jc_exact import (
    canonical_descriptor_key, descriptor_from_graph, p_add, p_hash, p_mul,
    quartet_coordinates,
)
from relation_universe import graph_from_object
from sign_certifier import certify_factorized_strict_sign


EXPECTED_SUMMARY_SHA256 = (
    "791844a802af61f64cba937a5adbe9d1d381d3fd7e55165914d4e4c885908e65"
)


def file_sha256(path):
    answer = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def logical_sha256(path):
    answer = hashlib.sha256()
    with gzip.open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def load_jsonl_gzip(path):
    with gzip.open(path, "rt") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def relation_id(relation):
    return digest([[coefficient, list(monomial)] for coefficient, monomial in relation])


def triangle_count(graph):
    vertices, edges, _ = semidirected(graph)
    adjacency = defaultdict(set)
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    triangles = set()
    for a in vertices:
        for b in adjacency[a]:
            if b <= a:
                continue
            for c in adjacency[a] & adjacency[b]:
                triangles.add(tuple(sorted((a, b, c))))
    return len(triangles)


def quartet_and_metadata(state, metadata):
    witness = state.get("probe_witness", {})
    port_count = int(state["selected_port_count"])
    quartets = tuple(itertools.combinations(range(port_count), 4))
    chunk = witness.get("quartet_chunk")
    invariant = witness.get("invariant_index")
    if not isinstance(chunk, int) or not (0 <= chunk < len(quartets)):
        raise ValueError(("invalid quartet chunk", state["state_id"], chunk))
    if not isinstance(invariant, int) or not (0 <= invariant < len(metadata)):
        raise ValueError(("invalid invariant index", state["state_id"], invariant))
    arm_degree = tuple(int(x) for x in metadata[invariant]["port_arm_multidegree"])
    return quartets[chunk], invariant, arm_degree


class PullbackCache:
    def __init__(self):
        self.contexts = {}
        self.values = {}

    def __call__(self, descriptor, quartet, relation):
        rid = relation_id(relation)
        key = (descriptor.key, tuple(quartet), rid)
        if key in self.values:
            return self.values[key]
        context_key = (descriptor.key, tuple(quartet))
        if context_key not in self.contexts:
            self.contexts[context_key] = (
                quartet_coordinates(descriptor, quartet), {}
            )
        coordinates, monomial_cache = self.contexts[context_key]
        polynomial = {}
        for coefficient, monomial in relation:
            if monomial not in monomial_cache:
                value = {tuple([0] * descriptor.variable_count): 1}
                for coordinate in monomial:
                    value = p_mul(value, coordinates[coordinate])
                monomial_cache[monomial] = value
            polynomial = p_add(polynomial, monomial_cache[monomial], coefficient)
        self.values[key] = polynomial
        return polynomial


def canonical_group_key(classification, source_descriptor, target_descriptor,
                        port_count, quartet, arm_degree):
    return (
        classification,
        canonical_descriptor_key(source_descriptor),
        canonical_descriptor_key(target_descriptor),
        int(port_count), tuple(quartet), tuple(arm_degree),
    )


def write_jsonl_gzip(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.GzipFile(filename=str(path), mode="wb", mtime=0) as stream:
        for record in records:
            stream.write((stable_json(record) + "\n").encode())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--relations", type=Path, required=True)
    parser.add_argument("--graphs", type=Path, required=True)
    parser.add_argument("--polynomials", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--invariant-metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--terminal-records-output", type=Path, required=True)
    parser.add_argument("--relation-library-output", type=Path, required=True)
    parser.add_argument("--sign-library-output", type=Path, required=True)
    args = parser.parse_args()

    failures = []
    if file_sha256(args.summary) != EXPECTED_SUMMARY_SHA256:
        failures.append(("summary SHA-256", file_sha256(args.summary), EXPECTED_SUMMARY_SHA256))
    summary = json.loads(args.summary.read_text())
    hard_cover = summary["runs"][0]["hard_cover"]
    stream_expectations = {
        "relations": (args.relations, hard_cover["relation_stream_sha256"],
                      hard_cover["canonical_restored_relations"]),
        "graphs": (args.graphs, hard_cover["graph_library_stream_sha256"],
                   hard_cover["graph_library_records"]),
        "polynomials": (args.polynomials, hard_cover["polynomial_library_stream_sha256"],
                        hard_cover["polynomial_library_records"]),
    }

    graph_records = load_jsonl_gzip(args.graphs)
    graphs = {}
    for record in graph_records:
        graph_id = record["graph_id"]
        if graph_id in graphs:
            failures.append(("duplicate graph ID", graph_id))
        graphs[graph_id] = graph_from_object(record["rooted_graph"])
    descriptors = {graph_id: descriptor_from_graph(graph) for graph_id, graph in graphs.items()}

    polynomial_records, primary_polynomials, polynomial_problems = polynomial_library(args.polynomials)
    failures.extend(polynomial_problems)
    metadata_object = json.loads(args.invariant_metadata.read_text())
    metadata = metadata_object.get("records", [])
    if len(metadata) != 84:
        failures.append(("invariant metadata record count", len(metadata), 84))

    state_records = load_jsonl_gzip(args.relations)
    actual_counts = {
        "relations": len(state_records), "graphs": len(graph_records),
        "polynomials": len(polynomial_records),
    }
    stream_audit = {}
    for name, (path, expected_logical, expected_records) in stream_expectations.items():
        logical = logical_sha256(path)
        stream_audit[name] = {
            "path": str(path), "physical_sha256": file_sha256(path),
            "logical_sha256": logical, "records": actual_counts[name],
        }
        if logical != expected_logical:
            failures.append((name, "logical SHA-256", logical, expected_logical))
        if actual_counts[name] != expected_records:
            failures.append((name, "record count", actual_counts[name], expected_records))

    _, family = load_family("n3")
    classes = Counter()
    canonical_groups = {}
    primary_references = Counter()
    primary_exact_hashes = defaultdict(set)
    seen_state_ids = set()
    for state in state_records:
        state_id = state["state_id"]
        if state_id in seen_state_ids:
            failures.append(("duplicate state ID", state_id))
        seen_state_ids.add(state_id)
        classification = state["terminal_classification"]
        classes[classification] += 1
        if classification not in (
            "generic_polynomial_separation", "strict_open_cube_separation",
        ):
            continue
        try:
            quartet, invariant, arm_degree = quartet_and_metadata(state, metadata)
        except Exception as exc:
            failures.append((state_id, "metadata", repr(exc)))
            continue
        source_id = state["source_graph_id"]
        target_id = state["target_graph_id"]
        if source_id not in descriptors or target_id not in descriptors:
            failures.append((state_id, "missing graph descriptor"))
            continue
        key = canonical_group_key(
            classification, descriptors[source_id], descriptors[target_id],
            state["selected_port_count"], quartet, arm_degree,
        )
        canonical_groups.setdefault(key, {
            "source_graph_id": source_id,
            "target_graph_id": target_id,
            "quartet": quartet,
            "port_count": int(state["selected_port_count"]),
            "arm_degree": arm_degree,
        })
        witness = state["probe_witness"]
        if classification == "generic_polynomial_separation":
            primary_id = witness.get("source_pullback_id")
            primary_exact = witness.get("source_pullback_exact_sha256")
            if witness.get("target_pullback") != "0":
                failures.append((state_id, "primary target does not claim zero"))
        else:
            primary_id = witness.get("target_pullback_id")
            primary_exact = witness.get("target_pullback_exact_sha256")
            if witness.get("source_pullback") != "0":
                failures.append((state_id, "primary source does not claim zero"))
        if primary_id not in primary_polynomials:
            failures.append((state_id, "missing primary polynomial", primary_id))
        else:
            primary_references[primary_id] += 1
            primary_exact_hashes[primary_id].add(primary_exact)

    unreferenced = sorted(set(primary_polynomials) - set(primary_references))
    if unreferenced:
        failures.append(("unreferenced primary polynomial bodies", unreferenced))
    primary_hash_conflicts = {
        polynomial_id: sorted(values)
        for polynomial_id, values in primary_exact_hashes.items()
        if len(values) != 1
    }
    if primary_hash_conflicts:
        failures.append(("primary polynomial exact-hash conflicts", primary_hash_conflicts))

    class_witnesses = {}
    relation_library = {}
    method_counts = Counter()
    derivation_failures = []
    group_items = sorted(canonical_groups.items(), key=lambda item: repr(item[0]))
    for index, (key, representative) in enumerate(group_items, 1):
        classification = key[0]
        source = descriptors[representative["source_graph_id"]]
        target = descriptors[representative["target_graph_id"]]
        quartet = representative["quartet"]
        arm_degree = representative["arm_degree"]
        if classification == "generic_polynomial_separation":
            result = find_generic_identity_separator_on_quartet(
                source, target, quartet, representative["port_count"], family,
            )
            if result is not None:
                relation = family[result["invariant"]]
                method = "independently_derived_finite_family"
            else:
                result = derive_pair_separator_on_quartet(
                    source, target, quartet, max_degree=6,
                    arm_degree_hint=arm_degree,
                )
                if result is None:
                    derivation_failures.append((digest(key), "no target identity separator"))
                    continue
                relation = result["relation"]
                method = "exact_target_nullspace"
        else:
            result = derive_pair_separator_on_quartet(
                target, source, quartet, max_degree=6,
                arm_degree_hint=arm_degree,
            )
            if result is None:
                derivation_failures.append((digest(key), "no source identity separator"))
                continue
            relation = result["relation"]
            method = "exact_source_nullspace_plus_Bernstein"
            representative_target = relation_poly(
                quartet_coordinates(target, quartet), relation,
                target.variable_count,
            )
            sign = certify_factorized_strict_sign(
                representative_target, target.variable_count,
            )
            if sign is None:
                derivation_failures.append((digest(key), "representative strict sign not certified"))
                continue
        rid = relation_id(relation)
        relation_library.setdefault(rid, {
            "relation_id": rid,
            "terms": [[coefficient, list(monomial)] for coefficient, monomial in relation],
        })
        class_witnesses[key] = {"relation": relation, "relation_id": rid, "method": method}
        method_counts[method] += 1
        if index % 500 == 0:
            print(stable_json({
                "phase": "canonical_relation_derivation", "completed": index,
                "total": len(group_items), "failures": len(derivation_failures),
            }), flush=True)
    failures.extend(derivation_failures)

    pullback = PullbackCache()
    exact_binding_cache = {}
    sign_library = {}
    terminal_rows = []
    exact_binding_classes = Counter()
    for index, state in enumerate(sorted(state_records, key=lambda row: row["state_id"]), 1):
        state_id = state["state_id"]
        classification = state["terminal_classification"]
        source_id = state["source_graph_id"]
        target_id = state["target_graph_id"]
        source_graph = graphs[source_id]
        target_graph = graphs[target_id]
        if classification == "refined_by_next_restoration":
            continue
        if classification == "support_prefix_labelled_isomorphism":
            source_code = mixed_code(source_graph)[0]
            target_code = mixed_code(target_graph)[0]
            if source_code != target_code:
                failures.append((state_id, "claimed isomorphism has unequal mixed codes"))
            terminal_rows.append({
                "state_id": state_id, "classification": "labelled_isomorphism",
                "source_graph_id": source_id, "target_graph_id": target_id,
                "mixed_code_sha256": digest(source_code),
            })
            continue
        if classification == "support_prefix_ordinary_T":
            source_code = mixed_code(source_graph)[0]
            target_code = mixed_code(target_graph)[0]
            source_t = mixed_code(source_graph, True)[0]
            target_t = mixed_code(target_graph, True)[0]
            source_triangles = triangle_count(source_graph)
            target_triangles = triangle_count(target_graph)
            if source_code == target_code:
                failures.append((state_id, "ordinary T terminal is already isomorphic"))
            if source_t != target_t:
                failures.append((state_id, "ordinary T quotient codes differ"))
            if (source_triangles, target_triangles) != (1, 1):
                failures.append((state_id, "ordinary T terminal lacks one triangle",
                                 source_triangles, target_triangles))
            terminal_rows.append({
                "state_id": state_id, "classification": "ordinary_triangle_redirection",
                "source_graph_id": source_id, "target_graph_id": target_id,
                "source_mixed_sha256": digest(source_code),
                "target_mixed_sha256": digest(target_code),
                "t_quotient_sha256": digest(source_t),
                "source_triangle_count": source_triangles,
                "target_triangle_count": target_triangles,
            })
            continue
        if classification not in (
            "generic_polynomial_separation", "strict_open_cube_separation",
        ):
            failures.append((state_id, "unknown terminal classification", classification))
            continue
        try:
            quartet, invariant, arm_degree = quartet_and_metadata(state, metadata)
        except Exception as exc:
            failures.append((state_id, "terminal metadata", repr(exc)))
            continue
        source_descriptor = descriptors[source_id]
        target_descriptor = descriptors[target_id]
        key = canonical_group_key(
            classification, source_descriptor, target_descriptor,
            state["selected_port_count"], quartet, arm_degree,
        )
        if key not in class_witnesses:
            failures.append((state_id, "missing canonical relation witness"))
            continue
        witness = class_witnesses[key]
        relation = witness["relation"]
        rid = witness["relation_id"]
        binding_key = (
            classification, source_descriptor.key, target_descriptor.key,
            tuple(quartet), rid,
        )
        if binding_key not in exact_binding_cache:
            source_polynomial = pullback(source_descriptor, quartet, relation)
            target_polynomial = pullback(target_descriptor, quartet, relation)
            binding = {
                "source_pullback_sha256": p_hash(source_polynomial),
                "source_pullback_term_count": len(source_polynomial),
                "target_pullback_sha256": p_hash(target_polynomial),
                "target_pullback_term_count": len(target_polynomial),
            }
            if classification == "generic_polynomial_separation":
                if not source_polynomial or target_polynomial:
                    failures.append((digest(binding_key), "invalid exact generic binding"))
                binding["sign_certificate_sha256"] = None
            else:
                if source_polynomial or not target_polynomial:
                    failures.append((digest(binding_key), "invalid exact strict binding"))
                    sign_certificate = None
                else:
                    sign_certificate = certify_factorized_strict_sign(
                        target_polynomial, target_descriptor.variable_count,
                    )
                if sign_certificate is None:
                    failures.append((digest(binding_key), "exact strict sign not certified"))
                    binding["sign_certificate_sha256"] = None
                else:
                    certificate_id = sign_certificate["certificate_sha256"]
                    sign_library.setdefault(certificate_id, sign_certificate)
                    binding["sign_certificate_sha256"] = certificate_id
                    binding["strict_sign"] = sign_certificate["strict_sign"]
            exact_binding_cache[binding_key] = binding
            exact_binding_classes[classification] += 1
        binding = exact_binding_cache[binding_key]
        primary = state["probe_witness"]
        if classification == "generic_polynomial_separation":
            primary_id = primary["source_pullback_id"]
            primary_exact = primary["source_pullback_exact_sha256"]
            output_classification = "generic_identity_separation"
        else:
            primary_id = primary["target_pullback_id"]
            primary_exact = primary["target_pullback_exact_sha256"]
            output_classification = "strict_open_cube_separation"
        terminal_rows.append({
            "state_id": state_id,
            "classification": output_classification,
            "source_graph_id": source_id,
            "target_graph_id": target_id,
            "quartet": list(quartet),
            "independent_relation_id": rid,
            "independent_derivation_method": witness["method"],
            **binding,
            "primary_invariant_index": invariant,
            "primary_polynomial_id": primary_id,
            "primary_polynomial_body_sha256": digest({
                "variable_count": primary_polynomials[primary_id]["variable_count"],
                "terms": primary_polynomials[primary_id]["terms"],
            }) if primary_id in primary_polynomials else None,
            "primary_exact_pullback_sha256": primary_exact,
        })
        if index % 5_000 == 0:
            print(stable_json({
                "phase": "exact_terminal_binding", "completed_states": index,
                "terminal_records": len(terminal_rows), "failures": len(failures),
            }), flush=True)

    relation_records = sorted(relation_library.values(), key=lambda row: row["relation_id"])
    sign_records = sorted(sign_library.values(), key=lambda row: row["certificate_sha256"])
    write_jsonl_gzip(args.terminal_records_output, terminal_rows)
    write_jsonl_gzip(args.relation_library_output, relation_records)
    write_jsonl_gzip(args.sign_library_output, sign_records)

    expected_counts = {
        "generic_polynomial_separation": 56_055,
        "refined_by_next_restoration": 8_349,
        "strict_open_cube_separation": 4_036,
        "support_prefix_labelled_isomorphism": 120,
        "support_prefix_ordinary_T": 24,
    }
    if dict(classes) != expected_counts:
        failures.append(("terminal classification totals", dict(classes), expected_counts))
    cert = {
        "schema": 1,
        "status": "VERIFIED" if not failures else "FALSE",
        "inputs": {
            str(args.relations): file_sha256(args.relations),
            str(args.graphs): file_sha256(args.graphs),
            str(args.polynomials): file_sha256(args.polynomials),
            str(args.summary): file_sha256(args.summary),
            str(args.invariant_metadata): file_sha256(args.invariant_metadata),
        },
        "summary_sha256": file_sha256(args.summary),
        "stream_audit": stream_audit,
        "state_count": len(state_records),
        "graph_count": len(graph_records),
        "polynomial_count": len(polynomial_records),
        "terminal_classification_counts": dict(sorted(classes.items())),
        "canonical_relation_group_count": len(canonical_groups),
        "canonical_relation_group_counts": dict(sorted(Counter(key[0] for key in canonical_groups).items())),
        "derivation_method_counts": dict(sorted(method_counts.items())),
        "independent_relation_count": len(relation_records),
        "exact_binding_class_counts": dict(sorted(exact_binding_classes.items())),
        "sign_certificate_count": len(sign_records),
        "terminal_record_count": len(terminal_rows),
        "terminal_record_commitment": digest(terminal_rows),
        "relation_library_commitment": digest(relation_records),
        "sign_library_commitment": digest(sign_records),
        "primary_polynomial_bodies_referenced": len(primary_references),
        "primary_polynomial_exact_hash_conflicts": len(primary_hash_conflicts),
        "failure_count": len(failures),
        "first_failures": failures[:100],
    }
    cert["normalized_sha256_without_hash"] = digest(cert)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(stable_json(cert) + "\n")
    print(stable_json({
        "status": cert["status"], "terminal_records": len(terminal_rows),
        "canonical_groups": len(canonical_groups), "failure_count": len(failures),
        "hash": cert["normalized_sha256_without_hash"],
    }))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
