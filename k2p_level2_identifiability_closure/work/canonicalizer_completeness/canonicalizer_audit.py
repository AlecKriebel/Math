#!/usr/bin/env python3
"""Independent completeness audit for the finite K2P canonicalizers.

The graph relation below does not call the atlas triangle enumerator or its
incidence expansion.  The descriptor comparison deliberately compares the
slow, direct B_r orbit enumeration with the optimized implementation on every
primitive completion archetype.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import dataclasses
import gzip
import hashlib
import importlib.util
import inspect
import itertools
import json
import multiprocessing
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEFAULT_ATLAS = (
    PROJECT
    / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
)
DEFAULT_RAW_LEDGER = (
    PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
)
DEFAULT_OUTPUT = HERE / "canonicalizer_completeness_certificate.json"
SCHEMA = "k2p-canonicalizer-completeness-v1"

FAMILIES = (
    ("raw4_sources", "source", ("theta0", "theta1", "theta3"), 4, None, 6),
    ("raw4_targets", "target", None, 4, None, 2_814),
    ("theta2_sources", "source", ("theta2",), 5, None, 4),
    ("theta2_targets", "target", None, 5, None, 6_138),
    ("cycle_sources", "source", ("cycle",), 3, None, 2),
    ("cycle_targets", "target", None, 3, None, 1_120),
)
EXPECTED_ARCHETYPES = 10_084
EXPECTED_RELATIONS = Counter(
    {
        ("none", "none", "none"): 3_932,
        ("triangle", "triangle", "triangle"): 54,
        ("isomorphic", "isomorphic", "isomorphic"): 26,
    }
)


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise AuditFailure(code if detail is None else f"{code}: {detail}")


def canonical_data(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {
            field.name: canonical_data(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, dict):
        return {
            str(key): canonical_data(item)
            for key, item in sorted(value.items(), key=lambda row: repr(row[0]))
        }
    if isinstance(value, (tuple, list, set, frozenset)):
        rows = [canonical_data(item) for item in value]
        return sorted(rows, key=lambda item: json.dumps(item, sort_keys=True)) if isinstance(value, (set, frozenset)) else rows
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        canonical_data(value), sort_keys=True, separators=(",", ":")
    ).encode()


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def load_atlas(path: Path, suffix: str = "main"):
    name = f"k2p_canonicalizer_audit_atlas_{suffix}_{os.getpid()}"
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "ATLAS_IMPORT_SPEC", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def records_for_family(atlas, name: str):
    if name == "raw4_sources":
        return tuple(atlas.source_supports())
    if name == "raw4_targets":
        return tuple(atlas.target_completions(4, True) + atlas.target_completions(4, False))
    if name == "theta2_sources":
        return tuple(atlas.source_supports(core_ids=("theta2",)))
    if name == "theta2_targets":
        return tuple(atlas.target_completions(5, True) + atlas.target_completions(5, False))
    if name == "cycle_sources":
        return tuple(atlas.source_supports(core_ids=("cycle",)))
    if name == "cycle_targets":
        return tuple(atlas.target_completions(3, True) + atlas.target_completions(3, False))
    raise AuditFailure(f"UNKNOWN_FAMILY:{name}")


def descriptor_chunk(task):
    atlas_path_text, family, start, end = task
    atlas = load_atlas(Path(atlas_path_text), f"worker_{family}_{start}")
    records = records_for_family(atlas, family)
    require(end <= len(records), "DESCRIPTOR_CHUNK_RANGE", task)
    mismatches = []
    digest_root = hashlib.sha256()
    for index in range(start, end):
        graph = records[index].graph
        slow = atlas.model_descriptor(graph)
        fast = atlas.model_descriptor_fast2(graph)
        if slow != fast:
            mismatches.append(
                {
                    "family": family,
                    "index": index,
                    "slow_sha256": sha(slow),
                    "fast_sha256": sha(fast),
                }
            )
        digest_root.update(canonical_bytes([index, sha(slow), sha(fast)]))
    return {
        "family": family,
        "start": start,
        "end": end,
        "comparisons": end - start,
        "mismatches": mismatches,
        "ordered_comparison_sha256": digest_root.hexdigest(),
    }


def descriptor_audit(atlas_path: Path, jobs: int) -> dict[str, Any]:
    atlas = load_atlas(atlas_path, "family_census")
    family_counts = {name: len(records_for_family(atlas, name)) for name, *_ in FAMILIES}
    expected = {name: count for name, *_, count in FAMILIES}
    require(family_counts == expected, "DESCRIPTOR_FAMILY_CENSUS", family_counts)

    tasks = []
    chunk_size = 256
    for family, count in family_counts.items():
        for start in range(0, count, chunk_size):
            tasks.append((str(atlas_path), family, start, min(start + chunk_size, count)))
    if jobs == 1:
        results = [descriptor_chunk(task) for task in tasks]
    else:
        try:
            context = multiprocessing.get_context("fork")
        except ValueError:  # pragma: no cover - Windows fallback for referees
            context = multiprocessing.get_context("spawn")
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=jobs, mp_context=context
        ) as executor:
            results = list(executor.map(descriptor_chunk, tasks))
    results.sort(key=lambda row: (row["family"], row["start"]))
    mismatches = [item for row in results for item in row["mismatches"]]
    comparisons = sum(row["comparisons"] for row in results)
    require(comparisons == EXPECTED_ARCHETYPES, "DESCRIPTOR_TOTAL", comparisons)
    require(not mismatches, "DESCRIPTOR_SLOW_FAST_MISMATCH", mismatches[:10])
    return {
        "primitive_archetype_families": family_counts,
        "primitive_archetypes_compared": comparisons,
        "slow_fast_disagreements": 0,
        "chunk_size": chunk_size,
        "chunk_count": len(results),
        "ordered_chunk_roots_sha256": sha(
            [
                [row["family"], row["start"], row["end"], row["ordered_comparison_sha256"]]
                for row in results
            ]
        ),
    }


# ------------------- independent strict mixed-graph semantics ----------------

def selected_restriction(graph: nx.DiGraph) -> nx.DiGraph:
    keep = {
        data["label"]
        for _, data in graph.nodes(data=True)
        if isinstance(data.get("label"), int)
    }
    result = graph.copy()
    for node, data in list(result.nodes(data=True)):
        if data["role"] == "leaf" and data.get("label") not in keep:
            result.remove_node(node)
    changed = True
    while changed:
        changed = False
        for node, data in list(result.nodes(data=True)):
            if result.out_degree(node) == 0 and not (
                data["role"] == "leaf" and data.get("label") in keep
            ):
                result.remove_node(node)
                changed = True
                break
        if changed:
            continue
        for node, data in list(result.nodes(data=True)):
            if (
                data["role"] != "leaf"
                and result.in_degree(node) == 1
                and result.out_degree(node) == 1
            ):
                parent = next(result.predecessors(node))
                child = next(result.successors(node))
                result.remove_node(node)
                if parent != child and not result.has_edge(parent, child):
                    result.add_edge(parent, child)
                changed = True
                break
        if changed:
            continue
        roots = [node for node in result if result.in_degree(node) == 0]
        if (
            len(roots) == 1
            and result.nodes[roots[0]]["role"] != "leaf"
            and result.out_degree(roots[0]) == 1
        ):
            result.remove_node(roots[0])
            changed = True
    for node, data in result.nodes(data=True):
        if data.get("label") in keep:
            data["role"] = "leaf"
        elif result.in_degree(node) == 0:
            data["role"] = "root"
        elif result.in_degree(node) == 2:
            data["role"] = "retic"
        else:
            data["role"] = "tree"
    return result


def semi_directed(graph: nx.DiGraph) -> nx.Graph:
    roots = [node for node, data in graph.nodes(data=True) if data["role"] == "root"]
    require(len(roots) == 1, "INDEPENDENT_ROOT_CENSUS", len(roots))
    root = roots[0]
    children = tuple(graph.successors(root))
    require(len(children) == 2, "INDEPENDENT_ROOT_CHILDREN", len(children))
    mixed = nx.Graph()
    for node, data in graph.nodes(data=True):
        if node != root:
            mixed.add_node(
                node,
                label=data.get("label"),
                role=data.get("role"),
            )
    for tail, head in graph.edges():
        if tail == root:
            continue
        require(not mixed.has_edge(tail, head), "INDEPENDENT_PARALLEL")
        mixed.add_edge(
            tail,
            head,
            heads=frozenset((head,))
            if graph.nodes[head]["role"] == "retic"
            else frozenset(),
        )
    require(children[0] != children[1], "INDEPENDENT_ROOT_LOOP")
    require(not mixed.has_edge(*children), "INDEPENDENT_ROOT_PARALLEL")
    mixed.add_edge(
        children[0],
        children[1],
        heads=frozenset(
            child for child in children if graph.nodes[child]["role"] == "retic"
        ),
    )
    return mixed


def edge_key(edge) -> tuple[str, str]:
    return tuple(sorted((repr(item) for item in edge)))


def ordinary_triangles(mixed: nx.Graph):
    rows = []
    for vertices in itertools.combinations(sorted(mixed.nodes(), key=repr), 3):
        edges = frozenset(
            frozenset(pair) for pair in itertools.combinations(vertices, 2)
        )
        if not all(mixed.has_edge(*tuple(edge)) for edge in edges):
            continue
        headed = []
        valid = True
        for edge in edges:
            heads = mixed.edges[tuple(edge)].get("heads", frozenset())
            if len(heads) > 1 or any(head not in edge for head in heads):
                valid = False
                break
            headed.extend(heads)
        if not valid or len(headed) != 2 or headed[0] != headed[1]:
            continue
        reticulation = headed[0]
        if mixed.nodes[reticulation].get("role") != "retic":
            continue
        rows.append((edges, reticulation))
    return tuple(rows)


def incidence(mixed: nx.Graph, erased=frozenset(), mark_erased: bool = True):
    graph = nx.Graph()
    for node, data in mixed.nodes(data=True):
        graph.add_node(("v", node), kind="vertex", label=data.get("label"))
    for number, (left, right, data) in enumerate(
        sorted(mixed.edges(data=True), key=lambda row: edge_key((row[0], row[1])))
    ):
        edge = frozenset((left, right))
        is_erased = edge in erased
        kind = "forgotten_triangle_edge" if is_erased and mark_erased else "edge"
        edge_node = ("e", number)
        graph.add_node(edge_node, kind=kind, label=None)
        heads = data.get("heads", frozenset())
        graph.add_edge(
            edge_node,
            ("v", left),
            head=False if is_erased else left in heads,
        )
        graph.add_edge(
            edge_node,
            ("v", right),
            head=False if is_erased else right in heads,
        )
    return graph


def incidence_isomorphic(left: nx.Graph, right: nx.Graph) -> bool:
    node_match = lambda first, second: (
        first.get("kind") == second.get("kind")
        and first.get("label") == second.get("label")
    )
    edge_match = lambda first, second: first.get("head") == second.get("head")
    return nx.algorithms.isomorphism.GraphMatcher(
        left, right, node_match=node_match, edge_match=edge_match
    ).is_isomorphic()


def mixed_relation(mixed_source: nx.Graph, mixed_target: nx.Graph, mark_erased=True):
    if incidence_isomorphic(incidence(mixed_source), incidence(mixed_target)):
        return "isomorphic", None
    for source_edges, source_reticulation in ordinary_triangles(mixed_source):
        for target_edges, target_reticulation in ordinary_triangles(mixed_target):
            if incidence_isomorphic(
                incidence(mixed_source, source_edges, mark_erased),
                incidence(mixed_target, target_edges, mark_erased),
            ):
                return "triangle", {
                    "source_triangle": sorted(edge_key(edge) for edge in source_edges),
                    "target_triangle": sorted(edge_key(edge) for edge in target_edges),
                    "source_reticulation": repr(source_reticulation),
                    "target_reticulation": repr(target_reticulation),
                }
    return "none", None


def strict_relation(source: nx.DiGraph, target: nx.DiGraph):
    return mixed_relation(semi_directed(source), semi_directed(target), True)


def relation_audit(atlas, raw_ledger: Path) -> dict[str, Any]:
    sources = tuple(atlas.source_supports())
    targets = tuple(
        atlas.target_completions(4, True) + atlas.target_completions(4, False)
    )
    pair_counts: Counter[tuple[str, str, str]] = Counter()
    triangle_witnesses = []
    checked = 0
    with gzip.open(raw_ledger, "rt", newline="") as handle:
        for line_number, line in enumerate(handle):
            row = json.loads(line)
            if row["category"] not in {
                "retained_terminal",
                "restoration_obligation",
            }:
                continue
            source = sources[row["source_index"]].graph
            target_record = atlas.relabel_record(
                targets[row["target_index"]], tuple(row["port_permutation"])
            )
            target = selected_restriction(target_record.graph)
            independent, witness = strict_relation(source, target)
            exact = atlas.mixed_relation_exact(source, target)
            prepared = atlas.mixed_relation_exact_prepared(
                atlas.prepare_mixed_source(source), target
            )
            pair_counts[(exact, prepared, independent)] += 1
            require(
                exact == prepared == independent,
                "RELATION_SEMANTIC_MISMATCH",
                {
                    "raw_id": row["raw_id"],
                    "exact": exact,
                    "prepared": prepared,
                    "independent": independent,
                },
            )
            if independent == "triangle":
                require(witness is not None, "TRIANGLE_WITNESS_ABSENT", row["raw_id"])
                triangle_witnesses.append([row["raw_id"], witness])
            checked += 1
    require(checked == 4_012, "RELATION_CANDIDATE_CENSUS", checked)
    require(pair_counts == EXPECTED_RELATIONS, "RELATION_STATUS_CENSUS", pair_counts)
    require(len(triangle_witnesses) == 54, "RELATION_TRIANGLE_CENSUS")
    return {
        "rank_and_topology_eligible_presentations": checked,
        "strict_relation_status_triples": {
            "/".join(key): value for key, value in sorted(pair_counts.items())
        },
        "strict_triangle_presentations": len(triangle_witnesses),
        "strict_triangle_witness_root_sha256": sha(triangle_witnesses),
        "disagreements": 0,
        "independence": (
            "the replay implements its own dummy restriction, root suppression, "
            "ordinary-triangle predicate, marked incidence expansion, and exact "
            "labelled graph-isomorphism test"
        ),
    }


def mutation_graphs():
    # Nonordinary triangle: the two heads land at different endpoints.  The
    # first headed edge is incident with vertex 0 on both headed edges so that
    # deleting only the common-head test revives this invalid candidate.
    nonordinary = nx.Graph()
    nonordinary.add_nodes_from(
        (node, {"label": f"n{node}", "role": "retic" if node == 0 else "tree"})
        for node in range(3)
    )
    nonordinary.add_edge(0, 1, heads=frozenset((0,)))
    nonordinary.add_edge(0, 2, heads=frozenset((2,)))
    nonordinary.add_edge(1, 2, heads=frozenset())

    # Two labelled triangles joined by a bridge.  A has only the left
    # ordinary triangle and B only the right one.  Erasing without marking
    # makes them identical; marking the chosen triangles correctly rejects.
    left = nx.Graph()
    right = nx.Graph()
    for graph in (left, right):
        graph.add_nodes_from(
            (node, {"label": f"v{node}", "role": "tree"}) for node in range(6)
        )
        graph.add_edges_from(
            (
                (0, 1, {"heads": frozenset()}),
                (0, 2, {"heads": frozenset()}),
                (1, 2, {"heads": frozenset()}),
                (2, 3, {"heads": frozenset()}),
                (3, 4, {"heads": frozenset()}),
                (3, 5, {"heads": frozenset()}),
                (4, 5, {"heads": frozenset()}),
            )
        )
    left.nodes[0]["role"] = "retic"
    left.edges[0, 1]["heads"] = frozenset((0,))
    left.edges[0, 2]["heads"] = frozenset((0,))
    right.nodes[3]["role"] = "retic"
    right.edges[3, 4]["heads"] = frozenset((3,))
    right.edges[3, 5]["heads"] = frozenset((3,))
    return nonordinary, left, right


def atlas_mixed_relation(atlas, source: nx.Graph, target: nx.Graph) -> str:
    node_match = lambda first, second: (
        first.get("kind") == second.get("kind")
        and first.get("label") == second.get("label")
    )
    edge_match = lambda first, second: first.get("head") == second.get("head")
    if nx.is_isomorphic(
        atlas.mixed_incidence_graph(source),
        atlas.mixed_incidence_graph(target),
        node_match=node_match,
        edge_match=edge_match,
    ):
        return "isomorphic"
    for first in atlas._mixed_triangle_edges(source):
        for second in atlas._mixed_triangle_edges(target):
            if nx.is_isomorphic(
                atlas.mixed_incidence_graph(source, first),
                atlas.mixed_incidence_graph(target, second),
                node_match=node_match,
                edge_match=edge_match,
            ):
                return "triangle"
    return "none"


def semantic_mutation_contract(atlas) -> dict[str, Any]:
    nonordinary, first, second = mutation_graphs()
    independent_nonordinary = ordinary_triangles(nonordinary)
    atlas_nonordinary = tuple(atlas._mixed_triangle_edges(nonordinary))
    require(not independent_nonordinary, "NONORDINARY_INDEPENDENT_ACCEPTED")
    require(not atlas_nonordinary, "NONORDINARY_ATLAS_ACCEPTED")
    strict, _ = mixed_relation(first, second, True)
    unmarked, _ = mixed_relation(first, second, False)
    atlas_strict = atlas_mixed_relation(atlas, first, second)
    require(unmarked == "triangle", "SELECTED_TRIANGLE_ATTACK_NOT_LIVE", unmarked)
    require(strict == "none", "SELECTED_TRIANGLE_INDEPENDENT_ACCEPTED", strict)
    require(atlas_strict == "none", "SELECTED_TRIANGLE_ATLAS_ACCEPTED", atlas_strict)
    return {
        "nonordinary_triangle": {
            "legacy_all_three_cycles_would_accept": True,
            "independent_ordinary_candidates": 0,
            "atlas_ordinary_candidates": 0,
            "conclusion": "rejected",
        },
        "selected_triangle_mismatch": {
            "unmarked_head_erasure_relation": unmarked,
            "independent_marked_relation": strict,
            "atlas_marked_relation": atlas_strict,
            "conclusion": "rejected",
        },
    }


def action_proof(atlas) -> dict[str, Any]:
    functions = (
        "retic_variants",
        "descriptor_variant",
        "model_descriptor",
        "model_descriptor_fast2",
    )
    source_hash = hashlib.sha256(
        "\n".join(inspect.getsource(getattr(atlas, name)) for name in functions).encode()
    ).hexdigest()
    return {
        "licensed_group": "B_r = S_r semidirect_product (Z/2Z)^r",
        "group_order": "r!*2^r",
        "direct_enumeration": (
            "retic_variants enumerates every reticulation order and every "
            "independent order of its two incoming parents"
        ),
        "optimized_enumeration": (
            "(p,f) ranges over permutations(range(r)) x {0,1}^r and "
            "ob[p[j]]=nb[j]^f[j], bijectively the same switching action"
        ),
        "parent_flip_semantics": (
            "a parent-order flip exchanges bit 0/1 and therefore applies "
            "lambda_j -> 1-lambda_j on the open physical inheritance interval"
        ),
        "edge_class_canonicalization": (
            "equal complete switching-by-character sector signatures are one "
            "serial product class; sorting the signatures removes only class names"
        ),
        "canonical_representative": (
            "the lexicographic minimum of the exact integer pullbacks over all "
            "r!*2^r actions is a complete orbit representative"
        ),
        "port_equivariance": {
            "statement": (
                "a physical port permutation permutes descendant masks and the "
                "conservation-supported character rows by the same bijection"
            ),
            "commutes_with_switching": True,
            "commutes_with_sector_for_mask": True,
            "consequence": (
                "slow-fast equality on every primitive archetype implies equality "
                "on every physical port relabelling; no port action is quotiented"
            ),
        },
        "safety_of_partition": {
            "false_split": "can only duplicate a certified raw presentation",
            "false_merge_excluded_by": (
                "literal equality of the exact effective pullback after serial "
                "products, variable permutation, and licensed parent flips"
            ),
        },
        "audited_function_source_sha256": source_hash,
    }


def build(atlas_path: Path, raw_ledger: Path, jobs: int) -> dict[str, Any]:
    atlas = load_atlas(atlas_path, "main")
    result = {
        "schema": SCHEMA,
        "status": "PASS",
        "claim_boundary": (
            "complete licensed descriptor action and strict mixed-graph relation "
            "semantics for every relation-reachable four-port raw presentation"
        ),
        "inputs": {
            "auditor": str(Path(__file__).resolve().relative_to(PROJECT)),
            "auditor_sha256": sha_file(Path(__file__).resolve()),
            "atlas": str(atlas_path.relative_to(PROJECT)),
            "atlas_sha256": sha_file(atlas_path),
            "raw_ledger": str(raw_ledger.relative_to(PROJECT)),
            "raw_ledger_sha256": sha_file(raw_ledger),
        },
        "licensed_action_proof": action_proof(atlas),
        "descriptor_audit": descriptor_audit(atlas_path, jobs),
        "relation_audit": relation_audit(atlas, raw_ledger),
        "semantic_mutation_contract": semantic_mutation_contract(atlas),
        "conclusion": (
            "zero slow/fast descriptor disagreements, zero strict relation "
            "disagreements, and both formerly unguarded triangle attacks rejected"
        ),
    }
    result["payload_sha256"] = sha(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--atlas", type=Path, default=DEFAULT_ATLAS)
    parser.add_argument("--raw-ledger", type=Path, default=DEFAULT_RAW_LEDGER)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--jobs", type=int, default=max(1, min(8, os.cpu_count() or 1)))
    parser.add_argument("--semantic-only", action="store_true")
    args = parser.parse_args()
    if not __debug__:
        raise AuditFailure("OPTIMIZED_MODE_FORBIDDEN")
    require(args.jobs >= 1, "JOBS_POSITIVE")
    atlas_path = args.atlas.resolve()
    raw_ledger = args.raw_ledger.resolve()
    atlas = load_atlas(atlas_path, "semantic")
    if args.semantic_only:
        contract = semantic_mutation_contract(atlas)
        print(json.dumps({"status": "PASS", "semantic_mutation_contract": contract}, sort_keys=True))
        return 0
    result = build(atlas_path, raw_ledger, args.jobs)
    atomic_json(args.output.resolve(), result)
    print(
        json.dumps(
            {
                "status": result["status"],
                "descriptors": result["descriptor_audit"]["primitive_archetypes_compared"],
                "relations": result["relation_audit"]["rank_and_topology_eligible_presentations"],
                "payload_sha256": result["payload_sha256"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditFailure as error:
        print(f"CANONICALIZER_COMPLETENESS_FAIL:{error}", file=sys.stderr)
        raise SystemExit(1)
