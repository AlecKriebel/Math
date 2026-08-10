#!/usr/bin/env python3
"""Compile path-bound ``A+p`` and ``A+p+q`` local relation probes.

The fixed-full hard cover ends at a common rigid anchor ``A=Q_s union Q_t``.
Every further boundary is an ordinary port on an internal blob arc.  This
compiler extends *each raw terminal path* on both sides, verifies exact
deletion to its parent, regenerates JC quartet descriptors and pullbacks from
the child graphs, and requires every surviving child transport to restrict to
the parent's fixed ordinary-T quotient transport.

Canonical graph/algebra records are content-addressed and may be shared.
Path bindings are emitted separately and are never deduplicated by target
topology or polynomial hash.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

from atlas_compiler import load_bit_cache, stable_hash
from graph_model import (
    MixedEdge,
    RootedGraph,
    canonical_mixed,
    mixed_automorphisms,
    mixed_local_strong,
    rooted_validation,
    sd0,
    t_quotient,
)
from hard_cover_compiler import (
    exact_poly_hash,
    full_deck,
    load_invariants,
    relation_witness,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent

ALLOWED_BASE = {
    "support_prefix_labelled_isomorphism",
    "support_prefix_ordinary_T",
}
SEPARATED = {
    "generic_polynomial_separation",
    "strict_open_cube_separation",
}
ALLOWED_CHILD = {
    "labelled_isomorphism",
    "ordinary_T",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path, key: str) -> dict[str, dict]:
    rows = {}
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            identifier = row[key]
            if identifier in rows:
                raise AssertionError((path, "duplicate", identifier))
            rows[identifier] = row
    return rows


def graph_from_row(row: dict) -> RootedGraph:
    payload = row["rooted_graph"]
    return RootedGraph(
        int(payload["root"]),
        tuple(sorted(
            (int(vertex), str(label)) for vertex, label in payload["labels"]
        )),
        tuple(sorted((int(u), int(v)) for u, v in payload["arcs"])),
    )


def graph_payload(graph: RootedGraph) -> dict:
    return {
        "root": int(graph.root),
        "labels": tuple(sorted(
            (int(vertex), str(label)) for vertex, label in graph.labels
        )),
        "arcs": tuple(sorted((int(u), int(v)) for u, v in graph.arcs)),
    }


def write_jsonl(path: Path, rows: dict[str, dict], key_order=None) -> str:
    digest = hashlib.sha256()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as out:
            keys = sorted(rows) if key_order is None else key_order
            for key in keys:
                line = (
                    json.dumps(rows[key], sort_keys=True, separators=(",", ":"))
                    + "\n"
                ).encode()
                out.write(line)
                digest.update(line)
    return digest.hexdigest()


def underlying_bridges(graph) -> set[tuple[int, int]]:
    """Return bridges of the simple underlying graph by exact edge deletion."""
    adjacency = {vertex: set() for vertex in graph.vertices}
    for edge in graph.edges:
        adjacency[edge.u].add(edge.v)
        adjacency[edge.v].add(edge.u)
    answer = set()
    for edge in graph.edges:
        start, goal = edge.u, edge.v
        seen = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbour in adjacency[vertex]:
                if {vertex, neighbour} == {start, goal}:
                    continue
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        if goal not in seen:
            answer.add(tuple(sorted((start, goal))))
    return answer


def admissible_internal_arcs(graph: RootedGraph) -> tuple[tuple[int, int], ...]:
    """Every directed arc carried by the nontrivial mixed-graph blob."""
    mixed = sd0(graph)
    bridges = underlying_bridges(mixed)
    mixed_pairs = {
        tuple(sorted(edge.endpoints())) for edge in mixed.edges
        if tuple(sorted(edge.endpoints())) not in bridges
    }
    leaves = set(graph.label_map)
    answer = tuple(sorted(
        (u, v) for u, v in graph.arcs
        if u != graph.root and v not in leaves
        and tuple(sorted((u, v))) in mixed_pairs
    ))
    if not answer:
        raise AssertionError("core-retaining terminal has no internal blob arc")
    return answer


def insert_port(
    graph: RootedGraph, arc: tuple[int, int], label: str
) -> tuple[RootedGraph, dict]:
    if label in graph.label_map.values():
        raise AssertionError((label, "already present"))
    if graph.arcs.count(arc) != 1:
        raise AssertionError((arc, "not a unique parent arc"))
    new_tree = max(graph.vertices) + 1
    new_leaf = new_tree + 1
    u, v = arc
    arcs = list(graph.arcs)
    arcs.remove(arc)
    arcs.extend(((u, new_tree), (new_tree, v), (new_tree, new_leaf)))
    child = RootedGraph(
        graph.root,
        tuple(sorted((*graph.labels, (new_leaf, label)))),
        tuple(sorted(arcs)),
    )
    valid, problems = rooted_validation(child)
    if not valid:
        raise AssertionError((arc, label, problems))
    if not mixed_local_strong(sd0(child)):
        raise AssertionError((arc, label, "lost standard strong local class"))
    deletion = {
        "subdivided_parent_arc": arc,
        "inserted_tree_vertex": new_tree,
        "inserted_leaf_vertex": new_leaf,
        "inserted_label": label,
    }
    if delete_port(child, deletion) != graph:
        raise AssertionError((arc, label, "deletion failed"))
    return child, deletion


def delete_port(graph: RootedGraph, deletion: dict) -> RootedGraph:
    u, v = (int(x) for x in deletion["subdivided_parent_arc"])
    tree = int(deletion["inserted_tree_vertex"])
    leaf = int(deletion["inserted_leaf_vertex"])
    label = str(deletion["inserted_label"])
    required = {(u, tree), (tree, v), (tree, leaf)}
    if not required <= set(graph.arcs):
        raise AssertionError(("bad deletion arcs", deletion))
    arcs = [arc for arc in graph.arcs if arc not in required]
    arcs.append((u, v))
    labels = [row for row in graph.labels if row != (leaf, label)]
    return RootedGraph(graph.root, tuple(sorted(labels)), tuple(sorted(arcs)))


def quotient_transport(
    source: RootedGraph, target: RootedGraph
) -> tuple[str, tuple[tuple[int, int], ...], dict]:
    source_q = t_quotient(sd0(source))
    target_q = t_quotient(sd0(target))
    source_code, source_to_canonical = canonical_mixed(source_q)
    target_code, target_to_canonical = canonical_mixed(target_q)
    if source_code != target_code:
        raise ValueError("T quotient codes differ")
    if len(mixed_automorphisms(source_q)) != 1:
        raise AssertionError("anchor is not pointwise rigid on the source")
    if len(mixed_automorphisms(target_q)) != 1:
        raise AssertionError("anchor is not pointwise rigid on the target")
    canonical_to_target = {
        canonical: raw for raw, canonical in target_to_canonical.items()
    }
    transport = tuple(sorted(
        (raw, canonical_to_target[canonical])
        for raw, canonical in source_to_canonical.items()
    ))
    return source_code, transport, {
        "source_raw_to_canonical": tuple(sorted(source_to_canonical.items())),
        "target_raw_to_canonical": tuple(sorted(target_to_canonical.items())),
    }


def transport_metadata(
    source: RootedGraph,
    target: RootedGraph,
    transport: tuple[tuple[int, int], ...],
) -> dict:
    mapping = dict(transport)
    source_q = t_quotient(sd0(source))
    target_q = t_quotient(sd0(target))
    target_edges = {edge: index for index, edge in enumerate(target_q.edges)}
    edge_permutation = []
    for index, edge in enumerate(source_q.edges):
        moved = MixedEdge.make(
            mapping[edge.u], mapping[edge.v],
            (mapping[head] for head in edge.heads()),
        )
        edge_permutation.append((index, target_edges[moved]))
    source_labels = source_q.label_map
    target_labels = target_q.label_map
    port_transport = tuple(sorted(
        (label, target_labels[mapping[vertex]])
        for vertex, label in source_labels.items()
    ))
    if any(left != right for left, right in port_transport):
        raise AssertionError(("nonidentity physical port transport", port_transport))
    source_retics = set(sd0(source).reticulations())
    target_retics = set(sd0(target).reticulations())
    nontriangle_retics = tuple(sorted(
        (vertex, mapping[vertex]) for vertex in source_retics
        if mapping[vertex] in target_retics
    ))
    return {
        "vertex_transport": transport,
        "t_quotient_edge_permutation": tuple(edge_permutation),
        "port_transport": port_transport,
        "reticulation_vertices_source": tuple(sorted(source_retics)),
        "reticulation_vertices_target": tuple(sorted(target_retics)),
        "reticulation_transport_outside_redirected_triangle": nontriangle_retics,
    }


def restricts_to(
    child_transport: tuple[tuple[int, int], ...],
    parent_transport: tuple[tuple[int, int], ...],
) -> bool:
    child = dict(child_transport)
    return all(child.get(source) == target for source, target in parent_transport)


class Compiler:
    def __init__(self, invariants, bit_cache):
        self.invariants = invariants
        self.bit_cache = bit_cache
        self.sign_cache = {}
        self.deck_cache = {}
        self.graphs: dict[str, dict] = {}
        self.polynomials: dict[str, dict] = {}
        self.states: dict[str, dict] = {}
        self.bindings: dict[str, dict] = {}
        self.insertion_cache = {}
        self.relation_cache = {}
        self.counts = Counter()

    def register_graph(self, graph: RootedGraph) -> str:
        rooted = graph_payload(graph)
        graph_id = stable_hash(rooted)
        if graph_id not in self.graphs:
            valid, problems = rooted_validation(graph)
            mixed = sd0(graph)
            code, raw_map = canonical_mixed(mixed)
            t_code, t_map = canonical_mixed(t_quotient(mixed))
            self.graphs[graph_id] = {
                "schema": 1,
                "graph_id": graph_id,
                "rooted_graph": rooted,
                "rooted_valid": valid,
                "rooted_validation_problems": problems,
                "standard_strong_local": mixed_local_strong(mixed),
                "standard_mixed_code": code,
                "t_quotient_code": t_code,
                "raw_mixed_vertex_to_canonical": tuple(sorted(raw_map.items())),
                "raw_t_quotient_vertex_to_canonical": tuple(sorted(t_map.items())),
                "admissible_internal_arcs": admissible_internal_arcs(graph),
            }
        return graph_id

    def register_polynomial(self, poly) -> str:
        terms = tuple(
            (tuple(int(value) for value in exponents), int(coefficient))
            for exponents, coefficient in sorted(poly.items())
        )
        payload = {
            "schema": 1,
            "variable_count": len(terms[0][0]) if terms else 0,
            "terms": terms,
        }
        identifier = stable_hash(payload)
        row = {**payload, "polynomial_id": identifier}
        prior = self.polynomials.setdefault(identifier, row)
        if prior != row:
            raise AssertionError("polynomial content-address collision")
        return identifier

    def deck(self, graph_id: str, graph: RootedGraph, p: int):
        key = graph_id, p
        if key not in self.deck_cache:
            self.deck_cache[key] = full_deck(graph, p)
        return self.deck_cache[key]

    def inserted(self, graph_id: str, graph: RootedGraph, arc, label):
        key = graph_id, tuple(arc), label
        if key not in self.insertion_cache:
            child, deletion = insert_port(graph, tuple(arc), label)
            child_id = self.register_graph(child)
            self.insertion_cache[key] = child_id, child, deletion
        return self.insertion_cache[key]

    def classify(
        self,
        source_id: str,
        source: RootedGraph,
        target_id: str,
        target: RootedGraph,
        p: int,
        parent_transport: tuple[tuple[int, int], ...],
    ) -> dict:
        key = source_id, target_id, p, parent_transport
        if key in self.relation_cache:
            return self.relation_cache[key]
        source_deck = self.deck(source_id, source, p)
        target_deck = self.deck(target_id, target, p)
        probe, witness = relation_witness(
            source_deck,
            target_deck,
            self.invariants,
            self.bit_cache,
            self.sign_cache,
            register_polynomial=self.register_polynomial,
            exact_sign=True,
        )
        row = {"probe_classification": probe, "probe_witness": witness}
        if probe in SEPARATED:
            row["classification"] = probe
        elif probe == "equal_invariant_signature":
            source_code = canonical_mixed(sd0(source))[0]
            target_code = canonical_mixed(sd0(target))[0]
            try:
                _t_code, child_transport, canonical = quotient_transport(
                    source, target
                )
            except ValueError:
                row["classification"] = "unresolved_equal_non_T"
            else:
                if not restricts_to(child_transport, parent_transport):
                    row["classification"] = "incoherent_isomorphism_or_T"
                else:
                    row["classification"] = (
                        "labelled_isomorphism"
                        if source_code == target_code else "ordinary_T"
                    )
                    row["transport"] = transport_metadata(
                        source, target, child_transport
                    )
                    row["canonicalization"] = canonical
        else:
            row["classification"] = probe
        self.relation_cache[key] = row
        return row

    def add_state(
        self,
        *,
        stage: str,
        p: int,
        source_id: str,
        target_id: str,
        relation: dict,
    ) -> str:
        payload = {
            "stage": stage,
            "selected_port_count": p,
            "source_graph_id": source_id,
            "target_graph_id": target_id,
            "classification": relation["classification"],
            "probe_classification": relation["probe_classification"],
            "probe_witness": relation["probe_witness"],
            "transport": relation.get("transport"),
            "canonicalization": relation.get("canonicalization"),
        }
        state_id = stable_hash(payload)
        row = {"schema": 1, "state_id": state_id, **payload}
        prior = self.states.setdefault(state_id, row)
        if prior != row:
            raise AssertionError("extension state collision")
        return state_id

    def add_binding(self, payload: dict) -> str:
        binding_id = stable_hash(payload)
        row = {"schema": 1, "probe_path_binding_id": binding_id, **payload}
        prior = self.bindings.setdefault(binding_id, row)
        if prior != row:
            raise AssertionError("probe path binding collision")
        return binding_id


def base_inputs(summary_paths: list[Path]):
    for summary_path in summary_paths:
        summary = json.loads(summary_path.read_text())
        for run in summary["runs"]:
            cover = run["hard_cover"]
            state_path = PROJECT / cover["relation_path"]
            graph_path = PROJECT / cover["graph_library_path"]
            yield summary_path, cover, state_path, graph_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-summary", action="append", type=Path, required=True)
    parser.add_argument("--bit-cache", type=Path, required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    compiler = Compiler(load_invariants(), load_bit_cache(args.bit_cache))
    input_hashes = {}
    base_terminal_paths = 0
    base_terminal_states = 0

    for summary_path, cover, state_path, graph_path in base_inputs(args.base_summary):
        input_hashes[str(summary_path)] = sha256(summary_path)
        input_hashes[str(state_path)] = sha256(state_path)
        input_hashes[str(graph_path)] = sha256(graph_path)
        states = load_jsonl(state_path, "state_id")
        graph_rows = load_jsonl(graph_path, "graph_id")
        for state_id in sorted(states):
            state = states[state_id]
            if state["terminal_classification"] not in ALLOWED_BASE:
                continue
            base_terminal_states += 1
            for coverage in state["raw_coverage"]:
                base_terminal_paths += 1
                source_parent = graph_from_row(graph_rows[coverage["source_graph_id"]])
                target_parent = graph_from_row(graph_rows[coverage["target_graph_id"]])
                source_parent_id = compiler.register_graph(source_parent)
                target_parent_id = compiler.register_graph(target_parent)
                _code, base_transport, base_canonical = quotient_transport(
                    source_parent, target_parent
                )
                base_transport_meta = transport_metadata(
                    source_parent, target_parent, base_transport
                )
                p0 = int(state["selected_port_count"])
                p_label = f"L_{p0}"
                for source_arc in admissible_internal_arcs(source_parent):
                    source_p_id, source_p, source_delete = compiler.inserted(
                        source_parent_id, source_parent, source_arc, p_label
                    )
                    for target_arc in admissible_internal_arcs(target_parent):
                        target_p_id, target_p, target_delete = compiler.inserted(
                            target_parent_id, target_parent, target_arc, p_label
                        )
                        relation_p = compiler.classify(
                            source_p_id, source_p, target_p_id, target_p,
                            p0 + 1, base_transport,
                        )
                        state_p = compiler.add_state(
                            stage="A_plus_p", p=p0 + 1,
                            source_id=source_p_id, target_id=target_p_id,
                            relation=relation_p,
                        )
                        binding_p_payload = {
                            "stage": "A_plus_p",
                            "base_summary": str(summary_path),
                            "base_state_id": state_id,
                            "base_path_binding_id": coverage["path_binding_id"],
                            "restoration_root_id": coverage["root_case_id"],
                            "parent_probe_path_binding_id": None,
                            "state_id": state_p,
                            "source_parent_graph_id": source_parent_id,
                            "target_parent_graph_id": target_parent_id,
                            "source_child_graph_id": source_p_id,
                            "target_child_graph_id": target_p_id,
                            "source_insertion": source_delete,
                            "target_insertion": target_delete,
                            "source_deletion_exact_parent": delete_port(source_p, source_delete) == source_parent,
                            "target_deletion_exact_parent": delete_port(target_p, target_delete) == target_parent,
                            "base_dummy_order": coverage["dummy_order"],
                            "base_restored_role_to_label": coverage["restored_role_to_label"],
                            "base_transport": base_transport_meta,
                            "base_canonicalization": base_canonical,
                        }
                        binding_p = compiler.add_binding(binding_p_payload)
                        compiler.counts[f"A_plus_p::{relation_p['classification']}"] += 1
                        if relation_p["classification"] not in ALLOWED_CHILD:
                            continue
                        child_transport = tuple(
                            tuple(pair)
                            for pair in relation_p["transport"]["vertex_transport"]
                        )
                        q_label = f"L_{p0 + 1}"
                        for source_q_arc in admissible_internal_arcs(source_p):
                            source_q_id, source_q, source_q_delete = compiler.inserted(
                                source_p_id, source_p, source_q_arc, q_label
                            )
                            for target_q_arc in admissible_internal_arcs(target_p):
                                target_q_id, target_q, target_q_delete = compiler.inserted(
                                    target_p_id, target_p, target_q_arc, q_label
                                )
                                relation_q = compiler.classify(
                                    source_q_id, source_q, target_q_id, target_q,
                                    p0 + 2, child_transport,
                                )
                                state_q = compiler.add_state(
                                    stage="A_plus_p_plus_q", p=p0 + 2,
                                    source_id=source_q_id, target_id=target_q_id,
                                    relation=relation_q,
                                )
                                compiler.add_binding({
                                    "stage": "A_plus_p_plus_q",
                                    "base_summary": str(summary_path),
                                    "base_state_id": state_id,
                                    "base_path_binding_id": coverage["path_binding_id"],
                                    "restoration_root_id": coverage["root_case_id"],
                                    "parent_probe_path_binding_id": binding_p,
                                    "state_id": state_q,
                                    "source_parent_graph_id": source_p_id,
                                    "target_parent_graph_id": target_p_id,
                                    "source_child_graph_id": source_q_id,
                                    "target_child_graph_id": target_q_id,
                                    "source_insertion": source_q_delete,
                                    "target_insertion": target_q_delete,
                                    "source_deletion_exact_parent": delete_port(source_q, source_q_delete) == source_p,
                                    "target_deletion_exact_parent": delete_port(target_q, target_q_delete) == target_p,
                                    "base_dummy_order": coverage["dummy_order"],
                                    "base_restored_role_to_label": coverage["restored_role_to_label"],
                                    "parent_transport": relation_p["transport"],
                                })
                                compiler.counts[
                                    f"A_plus_p_plus_q::{relation_q['classification']}"
                                ] += 1

    unresolved = {
        row["classification"] for row in compiler.states.values()
    } - SEPARATED - ALLOWED_CHILD
    tag = args.tag
    cert = HERE / "certificates"
    state_path = cert / f"probe_extension_states_{tag}.jsonl.gz"
    binding_path = cert / f"probe_extension_bindings_{tag}.jsonl.gz"
    graph_path = cert / f"probe_extension_graphs_{tag}.jsonl.gz"
    polynomial_path = cert / f"probe_extension_polynomials_{tag}.jsonl.gz"
    streams = {
        "states": {
            "path": str(state_path.relative_to(PROJECT)),
            "records": len(compiler.states),
            "sha256": write_jsonl(state_path, compiler.states),
        },
        "bindings": {
            "path": str(binding_path.relative_to(PROJECT)),
            "records": len(compiler.bindings),
            "sha256": write_jsonl(binding_path, compiler.bindings),
        },
        "graphs": {
            "path": str(graph_path.relative_to(PROJECT)),
            "records": len(compiler.graphs),
            "sha256": write_jsonl(graph_path, compiler.graphs),
        },
        "polynomials": {
            "path": str(polynomial_path.relative_to(PROJECT)),
            "records": len(compiler.polynomials),
            "sha256": write_jsonl(polynomial_path, compiler.polynomials),
        },
    }
    payload = {
        "schema": "path-bound-common-anchor-probe-extension-v1",
        "status": "UNRESOLVED" if unresolved else "EXACTLY_COMPUTED",
        "input_sha256": input_hashes,
        "base_terminal_states": base_terminal_states,
        "base_terminal_paths": base_terminal_paths,
        "counts": dict(sorted(compiler.counts.items())),
        "unresolved_classifications": sorted(unresolved),
        "descriptor_cache_size": len(compiler.deck_cache),
        "sign_cache_size": len(compiler.sign_cache),
        "streams": streams,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "counts": payload["counts"],
        "base_terminal_paths": base_terminal_paths,
        "states": len(compiler.states),
        "bindings": len(compiler.bindings),
        "output": str(args.output),
        "sha256": sha256(args.output),
    }, sort_keys=True))
    if unresolved:
        raise SystemExit("unresolved probe-extension relation")


if __name__ == "__main__":
    main()
