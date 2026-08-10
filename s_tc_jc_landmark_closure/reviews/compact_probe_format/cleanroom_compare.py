#!/usr/bin/env python3
"""Clean-room audit of compact path-bound probe certificates.

This program intentionally imports only the Python standard library.  It
does not import code from ``primary`` or from another review directory.  The
already-audited verbose stream is treated as the reference serialization of
the directed relation universe; all compact indices, graph insertions,
deletions, evidence bodies, and transports are decoded independently.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEFAULT_COMPACT = PROJECT / "primary/certificates/compact_probe_theta2_smoke0_summary.json"
DEFAULT_VERBOSE = PROJECT / "primary/certificates/probe_extension_theta2_schema3_summary.json"

ALLOWED_BASE = {
    "support_prefix_labelled_isomorphism": "labelled_isomorphism",
    "support_prefix_ordinary_T": "ordinary_T",
}
ALLOWED_CHILD = {"labelled_isomorphism", "ordinary_T"}
SEPARATED = {"generic_polynomial_separation", "strict_open_cube_separation"}
CODE_CLASS = {
    0: "generic_polynomial_separation",
    1: "strict_open_cube_separation",
    2: "labelled_isomorphism",
    3: "ordinary_T",
}
INDEX_MASK = (1 << 29) - 1


class AuditFailure(RuntimeError):
    pass


def stable_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def stable_hash(value) -> str:
    return hashlib.sha256(stable_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def normalized_path(path: Path) -> str:
    path = path.resolve()
    try:
        return str(path.relative_to(PROJECT.resolve()))
    except ValueError:
        return str(path)


def resolve_path(name: str | Path, relative_to: Path | None = None) -> Path:
    path = Path(name)
    if path.is_absolute():
        return path.resolve()
    candidates = [PROJECT / path]
    if relative_to is not None:
        candidates.append(relative_to.resolve().parent / path)
    candidates.append(path)
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return candidates[0].resolve()


def require(condition: bool, category: str, **details) -> None:
    if not condition:
        raise AuditFailure(json.dumps({"category": category, **details}, sort_keys=True))


def read_gzip_rows(path: Path, key: str | None = None):
    rows = []
    seen = set()
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for line_number, raw in enumerate(handle, 1):
            digest.update(raw)
            row = json.loads(raw)
            if key is not None:
                identifier = row[key]
                require(identifier not in seen, "duplicate_stream_key",
                        path=normalized_path(path), key=key,
                        identifier=identifier, line=line_number)
                seen.add(identifier)
            rows.append(row)
    return rows, digest.hexdigest()


def graph_payload(value: dict) -> dict:
    return {
        "root": int(value["root"]),
        "labels": sorted([[int(v), str(label)] for v, label in value["labels"]]),
        "arcs": sorted([[int(u), int(v)] for u, v in value["arcs"]]),
    }


def graph_id(graph: dict) -> str:
    return stable_hash(graph_payload(graph))


def graph_vertices(graph: dict) -> tuple[int, ...]:
    answer = {int(graph["root"])}
    answer.update(int(v) for v, _ in graph["labels"])
    for u, v in graph["arcs"]:
        answer.add(int(u)); answer.add(int(v))
    return tuple(sorted(answer))


def graph_degrees(graph: dict):
    vertices = graph_vertices(graph)
    indegree = {v: 0 for v in vertices}
    outdegree = {v: 0 for v in vertices}
    for u, v in graph["arcs"]:
        outdegree[int(u)] += 1
        indegree[int(v)] += 1
    return indegree, outdegree


def validate_rooted(graph: dict) -> None:
    graph = graph_payload(graph)
    arcs = [tuple(row) for row in graph["arcs"]]
    labels = {int(v): str(label) for v, label in graph["labels"]}
    vertices = graph_vertices(graph)
    indegree, outdegree = graph_degrees(graph)
    root = int(graph["root"])
    require(len(arcs) == len(set(arcs)), "rooted_parallel_arc")
    require(len(labels) == len(set(labels.values())), "duplicate_leaf_label")
    require((indegree[root], outdegree[root]) == (0, 2), "root_bidegree")
    for vertex in vertices:
        if vertex == root:
            continue
        degree = indegree[vertex], outdegree[vertex]
        expected = (1, 0) if vertex in labels else None
        if expected is not None:
            require(degree == expected, "leaf_bidegree", vertex=vertex, degree=degree)
        else:
            require(degree in {(1, 2), (2, 1)}, "internal_bidegree",
                    vertex=vertex, degree=degree)
    children = defaultdict(list)
    for u, v in arcs:
        children[u].append(v)
    work = dict(indegree)
    queue = sorted(v for v in vertices if work[v] == 0)
    order = []
    while queue:
        vertex = queue.pop(0)
        order.append(vertex)
        for child in children[vertex]:
            work[child] -= 1
            if work[child] == 0:
                queue.append(child)
                queue.sort()
    require(len(order) == len(vertices), "directed_cycle")
    reached = {root}; stack = [root]
    while stack:
        vertex = stack.pop()
        for child in children[vertex]:
            if child not in reached:
                reached.add(child); stack.append(child)
    require(reached == set(vertices), "not_root_reachable")


def mixed_edge(u: int, v: int, heads=()) -> tuple[int, int, int, int]:
    heads = set(int(x) for x in heads)
    if u < v:
        return int(u), int(v), int(u in heads), int(v in heads)
    return int(v), int(u), int(v in heads), int(u in heads)


def standard_mixed_edges(graph: dict):
    """Independent narrow sd0 edge set, sufficient for blob-arc recovery."""
    validate_rooted(graph)
    graph = graph_payload(graph)
    indegree, _ = graph_degrees(graph)
    root = int(graph["root"])
    edges = [mixed_edge(u, v, (v,) if indegree[v] == 2 else ())
             for u, v in graph["arcs"]]
    incident = [edge for edge in edges if root in edge[:2]]
    require(len(incident) == 2, "sd0_root_incidence")
    retained = [edge for edge in edges if root not in edge[:2]]

    def other(edge):
        return edge[1] if edge[0] == root else edge[0]

    a, b = other(incident[0]), other(incident[1])
    require(a != b, "sd0_root_loop")
    heads = []
    for endpoint, edge in ((a, incident[0]), (b, incident[1])):
        position = 0 if edge[0] == endpoint else 1
        if edge[2 + position]:
            heads.append(endpoint)
    retained.append(mixed_edge(a, b, heads))
    require(len(retained) == len(set(retained)), "sd0_parallel_edge")
    return tuple(sorted(retained))


def underlying_bridges(edges) -> set[tuple[int, int]]:
    adjacency = defaultdict(set)
    for u, v, _hu, _hv in edges:
        adjacency[u].add(v); adjacency[v].add(u)
    bridges = set()
    for u, v, _hu, _hv in edges:
        seen = {u}; stack = [u]
        while stack:
            x = stack.pop()
            for y in adjacency[x]:
                if {x, y} == {u, v}:
                    continue
                if y not in seen:
                    seen.add(y); stack.append(y)
        if v not in seen:
            bridges.add(tuple(sorted((u, v))))
    return bridges


def admissible_internal_arcs(graph: dict) -> tuple[tuple[int, int], ...]:
    graph = graph_payload(graph)
    edges = standard_mixed_edges(graph)
    bridges = underlying_bridges(edges)
    blob_pairs = {tuple(sorted((u, v))) for u, v, _hu, _hv in edges
                  if tuple(sorted((u, v))) not in bridges}
    leaves = {int(v) for v, _ in graph["labels"]}
    root = int(graph["root"])
    answer = tuple(sorted((int(u), int(v)) for u, v in graph["arcs"]
                          if int(u) != root and int(v) not in leaves
                          and tuple(sorted((int(u), int(v)))) in blob_pairs))
    require(bool(answer), "no_admissible_blob_arc")
    return answer


def insert_port(parent: dict, arc: tuple[int, int], label: str):
    parent = graph_payload(parent)
    arc = tuple(int(x) for x in arc)
    arcs = [tuple(row) for row in parent["arcs"]]
    require(arcs.count(arc) == 1, "insertion_parent_arc", arc=arc)
    require(label not in {value for _, value in parent["labels"]},
            "insertion_duplicate_label", label=label)
    new_tree = max(graph_vertices(parent)) + 1
    new_leaf = new_tree + 1
    arcs.remove(arc)
    arcs.extend(((arc[0], new_tree), (new_tree, arc[1]), (new_tree, new_leaf)))
    child = graph_payload({
        "root": parent["root"],
        "labels": [*parent["labels"], [new_leaf, label]],
        "arcs": arcs,
    })
    validate_rooted(child)
    insertion = {
        "subdivided_parent_arc": list(arc),
        "inserted_tree_vertex": new_tree,
        "inserted_leaf_vertex": new_leaf,
        "inserted_label": label,
    }
    require(delete_port(child, insertion) == parent, "insertion_deletion_round_trip")
    return child, insertion


def delete_port(child: dict, insertion: dict) -> dict:
    child = graph_payload(child)
    u, v = (int(x) for x in insertion["subdivided_parent_arc"])
    tree = int(insertion["inserted_tree_vertex"])
    leaf = int(insertion["inserted_leaf_vertex"])
    label = str(insertion["inserted_label"])
    required = {(u, tree), (tree, v), (tree, leaf)}
    arcs = [tuple(row) for row in child["arcs"]]
    require(required <= set(arcs), "deletion_required_arcs")
    require([leaf, label] in child["labels"], "deletion_leaf_label")
    kept_arcs = [row for row in arcs if row not in required]
    kept_arcs.append((u, v))
    kept_labels = [row for row in child["labels"] if row != [leaf, label]]
    return graph_payload({"root": child["root"], "labels": kept_labels,
                          "arcs": kept_arcs})


def decode_words(text: str, expected: int) -> list[int]:
    try:
        raw = base64.b64decode(text, validate=True) if text else b""
    except Exception as exc:
        raise AuditFailure(json.dumps({"category": "invalid_base64", "error": str(exc)}))
    require(len(raw) == 4 * expected, "packed_word_byte_length",
            actual=len(raw), expected=4 * expected)
    return list(struct.unpack(f"<{expected}I", raw)) if expected else []


def encode_words(words: list[int]) -> str:
    if not words:
        return ""
    return base64.b64encode(struct.pack(f"<{len(words)}I", *words)).decode("ascii")


def inventory_commitment(rows: list[dict]) -> str:
    digest = hashlib.sha256()
    for row in rows:
        digest.update(stable_bytes(row) + b"\n")
    return digest.hexdigest()


def load_keyed_gzip(path: Path, key: str):
    rows, digest = read_gzip_rows(path, key)
    return {row[key]: row for row in rows}, digest


def build_inventory(base_summaries: list[Path]):
    inventory = []
    commitment_rows = []
    input_hashes = {}
    for summary_path in sorted((p.resolve() for p in base_summaries),
                               key=normalized_path):
        summary = json.loads(summary_path.read_text())
        input_hashes[normalized_path(summary_path)] = file_sha256(summary_path)
        for run_index, run in enumerate(summary["runs"]):
            cover = run["hard_cover"]
            state_path = resolve_path(cover["relation_path"], summary_path)
            graph_path = resolve_path(cover["graph_library_path"], summary_path)
            input_hashes[normalized_path(state_path)] = file_sha256(state_path)
            input_hashes[normalized_path(graph_path)] = file_sha256(graph_path)
            states, _ = load_keyed_gzip(state_path, "state_id")
            graph_rows, _ = load_keyed_gzip(graph_path, "graph_id")
            for state_id in sorted(states):
                state = states[state_id]
                terminal = state["terminal_classification"]
                if terminal not in ALLOWED_BASE:
                    continue
                for coverage in sorted(state["raw_coverage"],
                                       key=lambda row: row["path_binding_id"]):
                    source_id = str(coverage["source_graph_id"])
                    target_id = str(coverage["target_graph_id"])
                    require(source_id in graph_rows and target_id in graph_rows,
                            "inventory_missing_parent_graph")
                    source = graph_payload(graph_rows[source_id]["rooted_graph"])
                    target = graph_payload(graph_rows[target_id]["rooted_graph"])
                    inventory.append({
                        "base_summary": normalized_path(summary_path),
                        "base_run_index": run_index,
                        "base_state_id": state_id,
                        "base_terminal_classification": terminal,
                        "base_path_binding_id": str(coverage["path_binding_id"]),
                        "fixed_full_root_case_id": str(coverage["root_case_id"]),
                        "selected_port_count": int(state["selected_port_count"]),
                        "source_parent_graph_id": source_id,
                        "target_parent_graph_id": target_id,
                        "source_parent_normalized_graph_id": graph_id(source),
                        "target_parent_normalized_graph_id": graph_id(target),
                        "base_dummy_order": coverage["dummy_order"],
                        "base_restored_role_to_label": coverage["restored_role_to_label"],
                        "source": source,
                        "target": target,
                    })
    inventory.sort(key=lambda row: (
        row["base_summary"], row["base_run_index"], row["base_state_id"],
        row["base_path_binding_id"],
    ))
    fields = (
        "base_summary", "base_run_index", "base_state_id",
        "base_path_binding_id", "fixed_full_root_case_id",
        "selected_port_count", "source_parent_graph_id",
        "target_parent_graph_id", "source_parent_normalized_graph_id",
        "target_parent_normalized_graph_id", "base_dummy_order",
        "base_restored_role_to_label",
    )
    for index, row in enumerate(inventory):
        commitment_rows.append({"path_index": index,
                                **{key: row[key] for key in fields}})
    return inventory, commitment_rows, input_hashes


def verify_stream_metadata(summary_path: Path, metadata: dict, key: str):
    path = resolve_path(metadata["path"], summary_path)
    require(file_sha256(path) == metadata["file_sha256"],
            "compact_file_sha256", stream=key)
    rows, logical = read_gzip_rows(path, key)
    require(len(rows) == int(metadata["records"]),
            "compact_stream_record_count", stream=key)
    require(logical == metadata["sha256"], "compact_logical_sha256", stream=key)
    return rows, logical, path


def load_compact(summary_path: Path):
    summary = json.loads(summary_path.read_text())
    require(summary.get("schema") == "compact-path-bound-probe-extension-v1",
            "compact_summary_schema")
    require(summary.get("status") == "EXACTLY_COMPUTED", "compact_status")
    require("schema_specification_sha256" in summary,
            "schema_specification_sha256_missing")
    schema_path = resolve_path(summary["schema_specification"], summary_path)
    require(file_sha256(schema_path) == summary["schema_specification_sha256"],
            "schema_specification_sha256")
    for name, expected in summary["input_sha256"].items():
        require(file_sha256(resolve_path(name, summary_path)) == expected,
                "compact_input_sha256", input=name)
    bit_path = resolve_path(summary["bit_cache"]["path"], summary_path)
    require(file_sha256(bit_path) == summary["bit_cache"]["sha256"],
            "compact_bit_cache_sha256")

    key_map = {
        "paths": "path_index",
        "witnesses": "witness_index",
        "transports": "transport_index",
        "polynomials": "polynomial_id",
    }
    streams = {}; stream_sha = {}; stream_paths = {}
    for name, key in key_map.items():
        rows, logical, path = verify_stream_metadata(
            summary_path, summary["streams"][name], key)
        streams[name] = rows; stream_sha[name] = logical; stream_paths[name] = path

    start, stop = (int(x) for x in summary["path_range"])
    indices = [int(row["path_index"]) for row in streams["paths"]]
    require(indices == list(range(start, stop)), "compact_path_range_order",
            actual=indices[:10], expected=[start, stop])
    require(len(indices) == int(summary["path_records"]), "compact_path_records")

    witnesses = {int(row["witness_index"]): row for row in streams["witnesses"]}
    transports = {int(row["transport_index"]): row for row in streams["transports"]}
    polynomials = {str(row["polynomial_id"]): row for row in streams["polynomials"]}
    require(set(witnesses) == set(range(len(witnesses))), "witness_index_contiguity")
    require(set(transports) == set(range(len(transports))), "transport_index_contiguity")

    for index, row in witnesses.items():
        payload = {key: row[key] for key in
                   ("classification", "probe_classification", "probe_witness")}
        require(stable_hash(payload) == row["witness_id"],
                "witness_content_address", index=index)
    for index, row in transports.items():
        payload = {key: row[key] for key in
                   ("classification", "transport", "canonicalization",
                    "fourier_coordinate_transport")}
        require(stable_hash(payload) == row["transport_id"],
                "transport_content_address", index=index)
        require(row["fourier_coordinate_transport"] ==
                "identity_on_fixed_port_labels", "fourier_transport", index=index)
    for identifier, row in polynomials.items():
        payload = {key: row[key] for key in ("schema", "variable_count", "terms")}
        require(stable_hash(payload) == identifier, "polynomial_content_address",
                polynomial_id=identifier)

    return {
        "summary": summary,
        "summary_path": summary_path,
        "paths": streams["paths"],
        "witnesses": witnesses,
        "transports": transports,
        "polynomials": polynomials,
        "stream_sha": stream_sha,
        "stream_paths": stream_paths,
        "schema_path": schema_path,
    }


def verify_verbose_stream(summary_path: Path, name: str, key: str | None = None):
    summary = json.loads(summary_path.read_text())
    metadata = summary["streams"][name]
    path = resolve_path(metadata["path"], summary_path)
    rows, logical = read_gzip_rows(path, key)
    require(len(rows) == int(metadata["records"]), "verbose_stream_record_count",
            stream=name)
    require(logical == metadata["sha256"], "verbose_stream_sha256", stream=name)
    return rows, path, logical


def load_verbose(summary_path: Path, base_path_ids: set[str]):
    summary = json.loads(summary_path.read_text())
    require(summary.get("schema") == "path-bound-common-anchor-probe-extension-v1",
            "verbose_summary_schema")
    require(summary.get("status") == "EXACTLY_COMPUTED", "verbose_status")
    binding_rows, binding_path, binding_sha = verify_verbose_stream(
        summary_path, "bindings", "probe_path_binding_id")
    relevant_bindings = [row for row in binding_rows
                         if str(row["base_path_binding_id"]) in base_path_ids]
    needed_state_ids = {str(row["state_id"]) for row in relevant_bindings}
    state_rows, state_path, state_sha = verify_verbose_stream(
        summary_path, "states", "state_id")
    states = {str(row["state_id"]): row for row in state_rows
              if str(row["state_id"]) in needed_state_ids}
    require(set(states) == needed_state_ids, "verbose_missing_states")

    needed_graph_ids = set()
    for row in relevant_bindings:
        needed_graph_ids.update(str(row[key]) for key in (
            "source_parent_graph_id", "target_parent_graph_id",
            "source_child_graph_id", "target_child_graph_id"))
    graph_rows, graph_path, graph_sha = verify_verbose_stream(
        summary_path, "graphs", "graph_id")
    graphs = {}
    for row in graph_rows:
        identifier = str(row["graph_id"])
        body = graph_payload(row["rooted_graph"])
        require(graph_id(body) == identifier, "verbose_graph_content_address",
                graph_id=identifier)
        if identifier in needed_graph_ids:
            graphs[identifier] = row
    require(set(graphs) == needed_graph_ids, "verbose_missing_graphs",
            missing=sorted(needed_graph_ids - set(graphs))[:5])

    polynomial_rows, polynomial_path, polynomial_sha = verify_verbose_stream(
        summary_path, "polynomials", "polynomial_id")
    polynomials = {}
    for row in polynomial_rows:
        identifier = str(row["polynomial_id"])
        payload = {key: row[key] for key in ("schema", "variable_count", "terms")}
        require(stable_hash(payload) == identifier,
                "verbose_polynomial_content_address", polynomial_id=identifier)
        polynomials[identifier] = row

    for row in relevant_bindings:
        payload = {key: value for key, value in row.items()
                   if key not in {"schema", "probe_path_binding_id"}}
        require(stable_hash(payload) == row["probe_path_binding_id"],
                "verbose_binding_content_address",
                binding_id=row["probe_path_binding_id"])
    for row in states.values():
        payload = {key: value for key, value in row.items()
                   if key not in {"schema", "state_id"}}
        require(stable_hash(payload) == row["state_id"],
                "verbose_state_content_address", state_id=row["state_id"])

    return {
        "summary": summary,
        "summary_path": summary_path,
        "bindings": relevant_bindings,
        "states": states,
        "graphs": graphs,
        "polynomials": polynomials,
        "stream_paths": {
            "bindings": binding_path, "states": state_path,
            "graphs": graph_path, "polynomials": polynomial_path,
        },
        "stream_sha": {
            "bindings": binding_sha, "states": state_sha,
            "graphs": graph_sha, "polynomials": polynomial_sha,
        },
    }


def verify_graph_library_entry(verbose: dict, identifier: str, expected: dict,
                               expected_arcs=None):
    require(identifier in verbose["graphs"], "verbose_graph_not_loaded",
            graph_id=identifier)
    row = verbose["graphs"][identifier]
    actual = graph_payload(row["rooted_graph"])
    require(actual == graph_payload(expected), "verbose_graph_body", graph_id=identifier)
    require(bool(row["rooted_valid"]), "verbose_rooted_valid_flag", graph_id=identifier)
    require(bool(row["standard_strong_local"]), "verbose_strong_flag", graph_id=identifier)
    if expected_arcs is not None:
        require(tuple(tuple(x) for x in row["admissible_internal_arcs"]) ==
                tuple(expected_arcs), "verbose_admissible_arcs", graph_id=identifier)


def word_relation(word: int, compact: dict, state: dict, context, used):
    code = int(word) >> 29
    index = int(word) & INDEX_MASK
    require(code in CODE_CLASS, "reserved_class_code", context=context, code=code)
    classification = CODE_CLASS[code]
    require(classification == state["classification"], "word_classification",
            context=context, compact=classification, verbose=state["classification"])
    if classification in SEPARATED:
        require(index in compact["witnesses"], "missing_witness_index",
                context=context, index=index)
        witness = compact["witnesses"][index]
        expected = {
            "classification": state["classification"],
            "probe_classification": state["probe_classification"],
            "probe_witness": state["probe_witness"],
        }
        actual = {key: witness[key] for key in expected}
        require(actual == expected, "witness_verbose_mismatch", context=context,
                index=index)
        used["witnesses"].add(index)
        evidence = {"kind": "witness", "index": index, "body": actual}
    else:
        require(index in compact["transports"], "missing_transport_index",
                context=context, index=index)
        transport = compact["transports"][index]
        expected = {
            "classification": state["classification"],
            "transport": state["transport"],
            "canonicalization": state["canonicalization"],
            "fourier_coordinate_transport": "identity_on_fixed_port_labels",
        }
        actual = {key: transport[key] for key in expected}
        require(actual == expected, "transport_verbose_mismatch", context=context,
                index=index)
        used["transports"].add(index)
        evidence = {"kind": "transport", "index": index, "body": actual}
    return classification, evidence


def compare_binding_common(binding: dict, state: dict, *, stage: str,
                           row: dict, source_parent_id: str,
                           target_parent_id: str, source_child_id: str,
                           target_child_id: str, source_insertion: dict,
                           target_insertion: dict, selected_count: int):
    require(binding["stage"] == stage and state["stage"] == stage,
            "stage_direction", stage=stage)
    require(int(state["selected_port_count"]) == selected_count,
            "selected_port_count", stage=stage)
    for key in ("base_summary", "base_state_id", "base_path_binding_id",
                "base_dummy_order", "base_restored_role_to_label"):
        require(binding[key] == row[key], "binding_base_provenance",
                stage=stage, key=key)
    require(binding["restoration_root_id"] == row["fixed_full_root_case_id"],
            "binding_root", stage=stage)
    expected_ids = {
        "source_parent_graph_id": source_parent_id,
        "target_parent_graph_id": target_parent_id,
        "source_child_graph_id": source_child_id,
        "target_child_graph_id": target_child_id,
    }
    for key, expected in expected_ids.items():
        require(binding[key] == expected, "binding_graph_direction",
                stage=stage, key=key, expected=expected, actual=binding[key])
    require(binding["source_insertion"] == source_insertion,
            "source_insertion", stage=stage)
    require(binding["target_insertion"] == target_insertion,
            "target_insertion", stage=stage)
    require(binding["source_deletion_exact_parent"] is True and
            binding["target_deletion_exact_parent"] is True,
            "deletion_flags", stage=stage)
    require(state["source_graph_id"] == source_child_id and
            state["target_graph_id"] == target_child_id,
            "state_graph_direction", stage=stage)
    require(binding["state_id"] == state["state_id"], "binding_state_link", stage=stage)


def compare_semantics(compact: dict, verbose: dict, inventory: list[dict],
                      *, path_rows: list[dict] | None = None):
    summary = compact["summary"]
    rows = compact["paths"] if path_rows is None else path_rows
    start, stop = (int(x) for x in summary["path_range"])
    indices = [int(row["path_index"]) for row in rows]
    require(len(indices) == len(set(indices)), "duplicate_path_index")
    require(indices == list(range(start, stop)), "semantic_path_range",
            actual=indices, expected=[start, stop])

    bindings_by_base = defaultdict(list)
    for binding in verbose["bindings"]:
        bindings_by_base[str(binding["base_path_binding_id"])].append(binding)
    used_bindings = set()
    used = {"witnesses": set(), "transports": set(), "polynomials": set()}
    counts = Counter()
    relation_digest = hashlib.sha256()
    p_relation_count = 0; q_relation_count = 0

    inventory_fields = (
        "base_summary", "base_run_index", "base_state_id",
        "base_path_binding_id", "fixed_full_root_case_id",
        "selected_port_count", "source_parent_graph_id",
        "target_parent_graph_id", "source_parent_normalized_graph_id",
        "target_parent_normalized_graph_id", "base_dummy_order",
        "base_restored_role_to_label",
    )

    for row in rows:
        path_index = int(row["path_index"])
        require(path_index < len(inventory), "path_index_outside_inventory",
                path_index=path_index)
        row_without_id = {key: value for key, value in row.items()
                          if key != "path_record_id"}
        require(stable_hash(row_without_id) == row["path_record_id"],
                "path_record_content_address", path_index=path_index)
        expected_entry = inventory[path_index]
        for key in inventory_fields:
            require(row[key] == expected_entry[key], "path_inventory_binding",
                    path_index=path_index, key=key)

        source_parent = expected_entry["source"]
        target_parent = expected_entry["target"]
        source_parent_id = graph_id(source_parent)
        target_parent_id = graph_id(target_parent)
        require(source_parent_id == row["source_parent_normalized_graph_id"],
                "source_parent_normalized_id", path_index=path_index)
        require(target_parent_id == row["target_parent_normalized_graph_id"],
                "target_parent_normalized_id", path_index=path_index)

        source_p_arcs = admissible_internal_arcs(source_parent)
        target_p_arcs = admissible_internal_arcs(target_parent)
        require(tuple(tuple(x) for x in row["source_p_arcs"]) == source_p_arcs,
                "source_p_arc_order", path_index=path_index)
        require(tuple(tuple(x) for x in row["target_p_arcs"]) == target_p_arcs,
                "target_p_arc_order", path_index=path_index)

        base_class = ALLOWED_BASE[expected_entry["base_terminal_classification"]]
        base_index = int(row["base_transport_index"])
        require(base_index in compact["transports"], "base_transport_index",
                path_index=path_index)
        base_transport_record = compact["transports"][base_index]
        require(base_transport_record["classification"] == base_class,
                "base_transport_classification", path_index=path_index)
        used["transports"].add(base_index)

        path_bindings = bindings_by_base[row["base_path_binding_id"]]
        p_bindings = [b for b in path_bindings if b["stage"] == "A_plus_p"]
        q_bindings = [b for b in path_bindings if b["stage"] == "A_plus_p_plus_q"]
        p_by_arcs = {}
        for binding in p_bindings:
            key = (tuple(binding["source_insertion"]["subdivided_parent_arc"]),
                   tuple(binding["target_insertion"]["subdivided_parent_arc"]))
            require(key not in p_by_arcs, "duplicate_verbose_p_arc_pair",
                    path_index=path_index, key=key)
            p_by_arcs[key] = binding
        expected_p_keys = [(s, t) for s in source_p_arcs for t in target_p_arcs]
        require(set(p_by_arcs) == set(expected_p_keys), "p_arc_pair_bijection",
                path_index=path_index, expected=len(expected_p_keys),
                actual=len(p_by_arcs))

        p_count = len(expected_p_keys)
        require(int(row["p_word_count"]) == p_count, "p_word_count",
                path_index=path_index)
        p_words = decode_words(row["p_words_base64_le_u32"], p_count)
        q_words = decode_words(row["q_words_base64_le_u32"],
                               int(row["q_word_count"]))
        allowed_indices = []
        expected_q_shapes = []
        q_cursor = 0
        p0 = int(row["selected_port_count"])
        p_label = f"L_{p0}"; q_label = f"L_{p0 + 1}"

        for p_flat, (source_arc, target_arc) in enumerate(expected_p_keys):
            binding = p_by_arcs[(source_arc, target_arc)]
            source_p, source_meta = insert_port(source_parent, source_arc, p_label)
            target_p, target_meta = insert_port(target_parent, target_arc, p_label)
            source_p_id, target_p_id = graph_id(source_p), graph_id(target_p)
            state = verbose["states"][binding["state_id"]]
            compare_binding_common(
                binding, state, stage="A_plus_p", row=row,
                source_parent_id=source_parent_id,
                target_parent_id=target_parent_id,
                source_child_id=source_p_id, target_child_id=target_p_id,
                source_insertion=source_meta, target_insertion=target_meta,
                selected_count=p0 + 1,
            )
            require(binding["parent_probe_path_binding_id"] is None,
                    "p_parent_binding", path_index=path_index, p_flat=p_flat)
            require(binding["base_transport"] == base_transport_record["transport"],
                    "base_transport_verbose", path_index=path_index, p_flat=p_flat)
            require(binding["base_canonicalization"] ==
                    base_transport_record["canonicalization"],
                    "base_canonicalization_verbose", path_index=path_index,
                    p_flat=p_flat)
            verify_graph_library_entry(verbose, source_p_id, source_p,
                                       admissible_internal_arcs(source_p))
            verify_graph_library_entry(verbose, target_p_id, target_p,
                                       admissible_internal_arcs(target_p))
            classification, evidence = word_relation(
                p_words[p_flat], compact, state, (path_index, "p", p_flat), used)
            counts[classification] += 1; p_relation_count += 1
            used_bindings.add(binding["probe_path_binding_id"])
            relation_digest.update(stable_bytes({
                "path_index": path_index, "stage": "A_plus_p",
                "flat_index": p_flat,
                "source_parent": source_parent_id, "target_parent": target_parent_id,
                "source_arc": source_arc, "target_arc": target_arc,
                "source_child": source_p_id, "target_child": target_p_id,
                "binding": binding["probe_path_binding_id"],
                "state": state["state_id"], "classification": classification,
                "evidence": evidence,
            }) + b"\n")

            if classification not in ALLOWED_CHILD:
                require(not any(q["parent_probe_path_binding_id"] ==
                                binding["probe_path_binding_id"] for q in q_bindings),
                        "q_below_separated_p", path_index=path_index, p_flat=p_flat)
                continue

            allowed_indices.append(p_flat)
            source_q_arcs = admissible_internal_arcs(source_p)
            target_q_arcs = admissible_internal_arcs(target_p)
            expected_q_shapes.append([len(source_q_arcs), len(target_q_arcs)])
            q_group = [q for q in q_bindings
                       if q["parent_probe_path_binding_id"] ==
                       binding["probe_path_binding_id"]]
            q_by_arcs = {}
            for q_binding in q_group:
                key = (tuple(q_binding["source_insertion"]["subdivided_parent_arc"]),
                       tuple(q_binding["target_insertion"]["subdivided_parent_arc"]))
                require(key not in q_by_arcs, "duplicate_verbose_q_arc_pair",
                        path_index=path_index, p_flat=p_flat, key=key)
                q_by_arcs[key] = q_binding
            expected_q_keys = [(s, t) for s in source_q_arcs for t in target_q_arcs]
            require(set(q_by_arcs) == set(expected_q_keys), "q_arc_pair_bijection",
                    path_index=path_index, p_flat=p_flat,
                    expected=len(expected_q_keys), actual=len(q_by_arcs))

            for q_local, (source_q_arc, target_q_arc) in enumerate(expected_q_keys):
                require(q_cursor < len(q_words), "truncated_q_block",
                        path_index=path_index, p_flat=p_flat)
                q_binding = q_by_arcs[(source_q_arc, target_q_arc)]
                source_q, source_q_meta = insert_port(source_p, source_q_arc, q_label)
                target_q, target_q_meta = insert_port(target_p, target_q_arc, q_label)
                source_q_id, target_q_id = graph_id(source_q), graph_id(target_q)
                q_state = verbose["states"][q_binding["state_id"]]
                compare_binding_common(
                    q_binding, q_state, stage="A_plus_p_plus_q", row=row,
                    source_parent_id=source_p_id, target_parent_id=target_p_id,
                    source_child_id=source_q_id, target_child_id=target_q_id,
                    source_insertion=source_q_meta, target_insertion=target_q_meta,
                    selected_count=p0 + 2,
                )
                require(q_binding["parent_transport"] == state["transport"],
                        "q_parent_transport", path_index=path_index,
                        p_flat=p_flat, q_local=q_local)
                verify_graph_library_entry(verbose, source_q_id, source_q,
                                           admissible_internal_arcs(source_q))
                verify_graph_library_entry(verbose, target_q_id, target_q,
                                           admissible_internal_arcs(target_q))
                q_classification, q_evidence = word_relation(
                    q_words[q_cursor], compact, q_state,
                    (path_index, "q", p_flat, q_local), used)
                counts[q_classification] += 1; q_relation_count += 1
                used_bindings.add(q_binding["probe_path_binding_id"])
                relation_digest.update(stable_bytes({
                    "path_index": path_index, "stage": "A_plus_p_plus_q",
                    "parent_p_flat_index": p_flat, "local_flat_index": q_local,
                    "global_q_flat_index": q_cursor,
                    "source_parent": source_p_id, "target_parent": target_p_id,
                    "source_arc": source_q_arc, "target_arc": target_q_arc,
                    "source_child": source_q_id, "target_child": target_q_id,
                    "binding": q_binding["probe_path_binding_id"],
                    "state": q_state["state_id"],
                    "classification": q_classification, "evidence": q_evidence,
                }) + b"\n")
                q_cursor += 1

        require(row["allowed_p_flat_indices"] == allowed_indices,
                "allowed_p_flat_indices", path_index=path_index)
        require(row["q_shapes"] == expected_q_shapes, "q_shape_blocks",
                path_index=path_index)
        require(q_cursor == len(q_words), "q_trailing_words",
                path_index=path_index, decoded=len(q_words), used=q_cursor)
        require(len(path_bindings) == len(p_bindings) + len(q_bindings),
                "unknown_verbose_stage", path_index=path_index)
        require(set(b["probe_path_binding_id"] for b in path_bindings) <= used_bindings,
                "unconsumed_verbose_binding", path_index=path_index)

    relevant_ids = {b["probe_path_binding_id"] for b in verbose["bindings"]}
    require(used_bindings == relevant_ids, "verbose_binding_bijection",
            used=len(used_bindings), expected=len(relevant_ids))
    require(dict(sorted(counts.items())) == summary["counts"],
            "compact_classification_counts", actual=dict(sorted(counts.items())),
            expected=summary["counts"])
    require(used["witnesses"] == set(compact["witnesses"]), "orphan_witnesses",
            orphan=sorted(set(compact["witnesses"]) - used["witnesses"])[:5])
    require(used["transports"] == set(compact["transports"]), "orphan_transports",
            orphan=sorted(set(compact["transports"]) - used["transports"])[:5])

    referenced_polynomials = set()
    for witness in compact["witnesses"].values():
        body = witness["probe_witness"]
        for key, value in body.items():
            if key.endswith("_pullback_id") and value not in {None, "0"}:
                referenced_polynomials.add(str(value))
    require(referenced_polynomials == set(compact["polynomials"]),
            "compact_polynomial_reference_bijection",
            referenced=len(referenced_polynomials),
            stored=len(compact["polynomials"]))
    for identifier, row in compact["polynomials"].items():
        require(identifier in verbose["polynomials"],
                "compact_polynomial_missing_from_verbose", polynomial_id=identifier)
        require(row == verbose["polynomials"][identifier],
                "compact_verbose_polynomial_body", polynomial_id=identifier)
        used["polynomials"].add(identifier)

    return {
        "path_records": len(rows),
        "p_relations": p_relation_count,
        "conditional_q_relations": q_relation_count,
        "total_relations": p_relation_count + q_relation_count,
        "classification_counts": dict(sorted(counts.items())),
        "used_witnesses": len(used["witnesses"]),
        "used_transports": len(used["transports"]),
        "used_polynomials": len(used["polynomials"]),
        "normalized_relation_stream_sha256": relation_digest.hexdigest(),
    }


def refresh_path_id(row: dict) -> None:
    row["path_record_id"] = stable_hash({key: value for key, value in row.items()
                                         if key != "path_record_id"})


def mutation_cases(compact: dict, inventory: list[dict]):
    original = compact["paths"]

    def changed_row():
        rows = deepcopy(original)
        return rows, rows[0]

    cases = []

    rows, row = changed_row()
    words = decode_words(row["p_words_base64_le_u32"], int(row["p_word_count"]))
    words.pop()
    row["p_word_count"] = len(words); row["p_words_base64_le_u32"] = encode_words(words)
    refresh_path_id(row); cases.append(("delete_relation", rows))

    rows, row = changed_row()
    words = decode_words(row["p_words_base64_le_u32"], int(row["p_word_count"]))
    words.insert(0, words[0])
    row["p_word_count"] = len(words); row["p_words_base64_le_u32"] = encode_words(words)
    refresh_path_id(row); cases.append(("duplicate_relation", rows))

    rows, row = changed_row()
    raw = base64.b64decode(row["q_words_base64_le_u32"])
    row["q_words_base64_le_u32"] = base64.b64encode(raw[:-1]).decode()
    refresh_path_id(row); cases.append(("truncate_q_block", rows))

    rows, row = changed_row()
    row["source_p_arcs"][0], row["source_p_arcs"][1] = (
        row["source_p_arcs"][1], row["source_p_arcs"][0])
    refresh_path_id(row); cases.append(("alter_arc_order", rows))

    rows, row = changed_row()
    for left, right in (
        ("source_parent_graph_id", "target_parent_graph_id"),
        ("source_parent_normalized_graph_id", "target_parent_normalized_graph_id"),
        ("source_p_arcs", "target_p_arcs"),
    ):
        row[left], row[right] = row[right], row[left]
    refresh_path_id(row); cases.append(("reverse_source_target", rows))

    rows, row = changed_row()
    words = decode_words(row["p_words_base64_le_u32"], int(row["p_word_count"]))
    position = next(i for i, word in enumerate(words) if (word >> 29) in {0, 1})
    old = words[position] & INDEX_MASK
    alternatives = sorted(set(compact["witnesses"]) - {old})
    words[position] = (words[position] & ~INDEX_MASK) | alternatives[0]
    row["p_words_base64_le_u32"] = encode_words(words); refresh_path_id(row)
    cases.append(("wrong_witness_index", rows))

    rows, row = changed_row()
    words = decode_words(row["p_words_base64_le_u32"], int(row["p_word_count"]))
    position = next(i for i, word in enumerate(words) if (word >> 29) in {2, 3})
    old = words[position] & INDEX_MASK
    alternatives = sorted(set(compact["transports"]) - {old})
    words[position] = (words[position] & ~INDEX_MASK) | alternatives[0]
    row["p_words_base64_le_u32"] = encode_words(words); refresh_path_id(row)
    cases.append(("wrong_transport_index", rows))

    rows, row = changed_row()
    row["source_parent_normalized_graph_id"] = "0" * 64
    refresh_path_id(row); cases.append(("wrong_parent", rows))

    rows, row = changed_row()
    row["fixed_full_root_case_id"] = "f" * 64
    refresh_path_id(row); cases.append(("wrong_root", rows))

    rows, row = changed_row()
    require(len(inventory) > 1, "mutation_inventory_needs_two_paths")
    row["base_path_binding_id"] = inventory[1]["base_path_binding_id"]
    refresh_path_id(row); cases.append(("cross_path_merge", rows))

    rows = deepcopy(original); rows.append(deepcopy(rows[0]))
    cases.append(("duplicate_path_row", rows))
    return cases


def preserve_failure(output_dir: Path, compact_path: Path, verbose_path: Path,
                     exc: Exception) -> Path:
    history = output_dir / "history"
    history.mkdir(parents=True, exist_ok=True)
    target = history / "FIRST_SEMANTIC_FAILURE.json"
    if not target.exists():
        payload = {
            "schema": 1,
            "status": "FALSE",
            "compact_summary": normalized_path(compact_path),
            "compact_summary_sha256": file_sha256(compact_path),
            "verbose_summary": normalized_path(verbose_path),
            "verbose_summary_sha256": file_sha256(verbose_path),
            "failure": str(exc),
        }
        target.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compact", type=Path, default=DEFAULT_COMPACT)
    parser.add_argument("--verbose", type=Path, default=DEFAULT_VERBOSE)
    parser.add_argument("--output-dir", type=Path, default=HERE / "certificates")
    parser.add_argument("--skip-mutations", action="store_true")
    args = parser.parse_args()
    compact_path = args.compact.resolve(); verbose_path = args.verbose.resolve()
    output_dir = args.output_dir.resolve(); output_dir.mkdir(parents=True, exist_ok=True)

    try:
        compact = load_compact(compact_path)
        base_paths = [resolve_path(path, compact_path)
                      for path in compact["summary"]["base_summaries"]]
        inventory, commitment_rows, input_hashes = build_inventory(base_paths)
        require(len(inventory) == int(compact["summary"]["path_inventory_count"]),
                "path_inventory_count")
        require(inventory_commitment(commitment_rows) ==
                compact["summary"]["path_inventory_sha256"],
                "path_inventory_sha256")
        require(dict(sorted(input_hashes.items())) ==
                compact["summary"]["input_sha256"], "path_inventory_input_map")
        base_ids = {str(row["base_path_binding_id"]) for row in compact["paths"]}
        verbose = load_verbose(verbose_path, base_ids)
        semantic = compare_semantics(compact, verbose, inventory)
    except Exception as exc:
        failure = preserve_failure(output_dir.parent, compact_path, verbose_path, exc)
        print(json.dumps({"status": "FALSE", "failure": str(exc),
                          "preserved_at": str(failure)}, sort_keys=True))
        return 1

    mutations = []
    if not args.skip_mutations:
        for name, rows in mutation_cases(compact, inventory):
            try:
                compare_semantics(compact, verbose, inventory, path_rows=rows)
            except Exception as exc:
                mutations.append({"mutation": name, "rejected": True,
                                  "first_failure": str(exc)})
            else:
                mutations.append({"mutation": name, "rejected": False,
                                  "first_failure": None})
        require(all(row["rejected"] for row in mutations),
                "mutation_not_rejected",
                mutations=[row["mutation"] for row in mutations
                           if not row["rejected"]])

    audit = {
        "schema": "compact-probe-cleanroom-format-audit-v1",
        "status": "VERIFIED",
        "scope": "one-path compact smoke versus independently audited verbose theta2 schema3 p/q streams",
        "reviewer": normalized_path(Path(__file__)),
        "reviewer_sha256": file_sha256(Path(__file__)),
        "compact_summary": normalized_path(compact_path),
        "compact_summary_sha256": file_sha256(compact_path),
        "verbose_summary": normalized_path(verbose_path),
        "verbose_summary_sha256": file_sha256(verbose_path),
        "schema_specification": normalized_path(compact["schema_path"]),
        "schema_specification_sha256": file_sha256(compact["schema_path"]),
        "inventory_count": len(inventory),
        "inventory_sha256": inventory_commitment(commitment_rows),
        "semantic_comparison": semantic,
        "compact_stream_logical_sha256": compact["stream_sha"],
        "verbose_stream_logical_sha256": verbose["stream_sha"],
    }
    mutation_certificate = {
        "schema": "compact-probe-cleanroom-mutations-v1",
        "status": "VERIFIED" if all(row["rejected"] for row in mutations) else "FALSE",
        "reviewer": normalized_path(Path(__file__)),
        "reviewer_sha256": file_sha256(Path(__file__)),
        "mutations": mutations,
    }
    audit_path = output_dir / "compact_smoke_cleanroom_audit.json"
    mutation_path = output_dir / "compact_smoke_mutations.json"
    audit_path.write_text(json.dumps(audit, sort_keys=True, indent=2) + "\n")
    mutation_path.write_text(json.dumps(mutation_certificate, sort_keys=True,
                                        indent=2) + "\n")
    print(json.dumps({
        "status": audit["status"],
        "semantic_comparison": semantic,
        "mutations_rejected": sum(row["rejected"] for row in mutations),
        "mutations_total": len(mutations),
        "audit": normalized_path(audit_path),
        "audit_sha256": file_sha256(audit_path),
        "mutation_certificate": normalized_path(mutation_path),
        "mutation_certificate_sha256": file_sha256(mutation_path),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
