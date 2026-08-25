#!/usr/bin/env python3
"""Independent, standard-library finite-universe and frozen-ledger census.

This script deliberately imports no submitted K2P module.  It implements the
five primitive core incidence lists directly, enumerates all completion words,
checks binary/DAG/tree-child graph conditions, derives the closed-form counts,
then streams the submitted authoritative ledgers to check dense raw IDs,
partitions, hashes, and registry uniqueness.
"""

from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import itertools
import json
import math
import os
import resource
import time
from pathlib import Path
from typing import Any, Iterable, Iterator


CORES: dict[str, dict[str, Any]] = {
    "cycle": {
        "arcs": (("S", "X"), ("S", "X")),
        "retics": ("X",),
        "sinks": ("X",),
        # The target completion does not choose a repair.  The two source
        # supports put their one physical subdivision on opposite parallel arcs.
        "target_repairs": ((),),
        "source_repairs": ((0,), (1,)),
    },
    "theta0": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X"), ("V", "X"), ("U", "V")),
        "retics": ("V", "X"),
        "sinks": ("X",),
        "target_repairs": ((2, 3), (3, 4)),
        "source_repairs": ((2, 3), (3, 4)),
    },
    "theta1": {
        "arcs": (("S", "U"), ("S", "X"), ("V", "X"), ("U", "V"), ("U", "V")),
        "retics": ("V", "X"),
        "sinks": ("X",),
        "target_repairs": ((2, 3), (2, 4)),
        "source_repairs": ((2, 3), (2, 4)),
    },
    "theta2": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1")),
        "retics": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "target_repairs": ((2, 3), (2, 5), (3, 4), (4, 5)),
        "source_repairs": ((2, 3), (2, 5), (3, 4), (4, 5)),
    },
    "theta3": {
        "arcs": (("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V")),
        "retics": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "target_repairs": ((2,), (4,)),
        "source_repairs": ((2,), (4,)),
    },
}


EXPECTED = {
    "target_counts": {
        "k3_incoming": 289,
        "k3_marginal": 831,
        "k4_incoming": 831,
        "k4_marginal": 1983,
        "k5_incoming": 1983,
        "k5_marginal": 4155,
    },
    "raw4": {
        "rows": 405_216,
        "categories": {
            "displayed_quartet_exclusion": 360_408,
            "full_map_Ti_strict_sign": 16_974,
            "exact_rank_exclusion": 23_822,
            "direct_terminal_presentation": 1_472,
            "restoration_member_presentation": 2_540,
        },
    },
    "theta2": {
        "rows": 2_946_240,
        "categories": {
            "displayed_quartet_exclusion": 2_942_592,
            "full_map_Ti_strict_sign": 2_528,
            "exact_rank_exclusion": 800,
            "direct_quadratic_separator": 240,
            "labelled_isomorphism": 80,
        },
    },
    "cycle_base": {
        "rows": 13_440,
        "categories": {
            "full_map_Ti_strict_sign": 7_452,
            "fixed_full_restoration_obligation": 5_964,
            "labelled_isomorphism": 8,
            "ordinary_triangle_relation": 16,
        },
    },
    "cycle_full": {
        "rows": 536_364,
        "categories": {
            "displayed_quartet_strict_separator": 535_920,
            "full_map_Ti_strict_sign": 300,
            "exact_directional_quadratic": 132,
            "labelled_isomorphism": 12,
        },
    },
    "one_port": {
        "rows": 29_964,
        "categories": {
            "displayed_quartet_mismatch": 27_758,
            "full_map_Ti_strict_sign": 99,
            "isomorphic": 1_915,
            "triangle": 192,
        },
    },
    "two_port": {
        "rows": 544_571,
        "categories": {
            "displayed_quartet_mismatch": 511_266,
            "full_map_Ti_strict_sign": 576,
            "isomorphic": 30_969,
            "triangle": 1_760,
        },
    },
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def weak_compositions(total: int, bins: int) -> Iterator[tuple[int, ...]]:
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, bins - 1):
            yield (first,) + rest


def closed_completion_count(k: int, incoming_selected: bool) -> dict[str, int]:
    nout = k - int(incoming_selected)
    counts: dict[str, int] = {}
    for core, spec in CORES.items():
        m = len(spec["arcs"])
        ns = len(spec["sinks"])
        repair_count = len(spec["target_repairs"])
        counts[core] = repair_count * sum(
            math.comb(ns, j) * math.comb(nout - j + m - 1, m - 1)
            for j in range(min(ns, nout) + 1)
        )
    return counts


def validate_graph(core: str, words: tuple[tuple[str, ...], ...], sink_tokens: tuple[str, ...], incoming: str) -> dict[str, int]:
    """Build and validate the rooted binary graph with no graph library."""
    spec = CORES[core]
    nodes: dict[tuple[Any, ...], str] = {}
    edges: set[tuple[tuple[Any, ...], tuple[Any, ...]]] = set()

    def add_node(node: tuple[Any, ...], role: str) -> None:
        previous = nodes.setdefault(node, role)
        if previous != role:
            raise AssertionError((core, node, previous, role))

    def add_edge(tail: tuple[Any, ...], head: tuple[Any, ...]) -> None:
        edge = (tail, head)
        if edge in edges:
            # The mathematical encoding is a simple subdivided digraph.  A
            # surviving parallel core arc would make the claimed encoding ill-defined.
            raise AssertionError(("duplicate directed edge", core, edge, words))
        edges.add(edge)

    core_nodes = {x for edge in spec["arcs"] for x in edge}
    for name in core_nodes:
        add_node(("core", name), "retic" if name in spec["retics"] else "tree")
    root = ("root",)
    incoming_leaf = ("leaf", "incoming", incoming)
    add_node(root, "root")
    add_node(incoming_leaf, "leaf")
    add_edge(root, ("core", "S"))
    add_edge(root, incoming_leaf)
    for arc_index, ((tail, head), word) in enumerate(zip(spec["arcs"], words)):
        previous = ("core", tail)
        for position, token in enumerate(word):
            subdivision = ("sub", arc_index, position)
            leaf = ("leaf", "seg", arc_index, position, token)
            add_node(subdivision, "tree")
            add_node(leaf, "leaf")
            add_edge(previous, subdivision)
            add_edge(subdivision, leaf)
            previous = subdivision
        add_edge(previous, ("core", head))
    for sink_index, (sink, token) in enumerate(zip(spec["sinks"], sink_tokens)):
        leaf = ("leaf", "sink", sink_index, token)
        add_node(leaf, "leaf")
        add_edge(("core", sink), leaf)

    indegree = collections.Counter(head for _, head in edges)
    outdegree = collections.Counter(tail for tail, _ in edges)
    expected_degrees = {"root": (0, 2), "tree": (1, 2), "retic": (2, 1), "leaf": (1, 0)}
    for node, role in nodes.items():
        actual = (indegree[node], outdegree[node])
        if actual != expected_degrees[role]:
            raise AssertionError(("binary degree", core, node, role, actual, words))

    children: dict[tuple[Any, ...], list[tuple[Any, ...]]] = collections.defaultdict(list)
    for tail, head in edges:
        children[tail].append(head)
    queue = collections.deque(node for node in nodes if indegree[node] == 0)
    remaining = dict(indegree)
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for child in children[node]:
            remaining[child] -= 1
            if remaining[child] == 0:
                queue.append(child)
    if visited != len(nodes):
        raise AssertionError(("cycle", core, words))

    for node, role in nodes.items():
        if role != "leaf" and not any(nodes[child] in {"tree", "leaf"} for child in children[node]):
            raise AssertionError(("tree-child", core, node, words))
    return {"nodes": len(nodes), "edges": len(edges)}


def enumerate_targets(k: int, incoming_selected: bool) -> dict[str, int]:
    counts: collections.Counter[str] = collections.Counter()
    keys: set[tuple[Any, ...]] = set()
    nout = k - int(incoming_selected)
    for core, spec in CORES.items():
        ns = len(spec["sinks"])
        for mask in range(1 << ns):
            selected_sink_count = mask.bit_count()
            ordinary = nout - selected_sink_count
            if ordinary < 0:
                continue
            for composition in weak_compositions(ordinary, len(spec["arcs"])):
                base_words = tuple(tuple(f"L{arc_index}_{j}" for j in range(count)) for arc_index, count in enumerate(composition))
                for repair_index, repair in enumerate(spec["target_repairs"]):
                    words = [list(word) for word in base_words]
                    for arc_index in repair:
                        if not words[arc_index]:
                            words[arc_index].append(f"D_REPAIR_{repair_index}_{arc_index}")
                    sink_tokens = tuple(
                        f"L_SINK_{j}" if (mask >> j) & 1 else f"D_SINK_{j}"
                        for j in range(ns)
                    )
                    key = (core, incoming_selected, mask, composition, repair_index)
                    if key in keys:
                        raise AssertionError(("duplicate target descriptor", key))
                    keys.add(key)
                    validate_graph(core, tuple(tuple(word) for word in words), sink_tokens, "L_IN" if incoming_selected else "D_IN")
                    counts[core] += 1
    closed = closed_completion_count(k, incoming_selected)
    if dict(counts) != closed:
        raise AssertionError(("closed/enumerated mismatch", k, incoming_selected, dict(counts), closed))
    return dict(counts)


def enumerate_sources(core_ids: tuple[str, ...]) -> dict[str, int]:
    counts: collections.Counter[str] = collections.Counter()
    for core in core_ids:
        spec = CORES[core]
        for repair_index, repair in enumerate(spec["source_repairs"]):
            words = [[] for _ in spec["arcs"]]
            for arc_index in repair:
                words[arc_index].append(f"L_REPAIR_{repair_index}_{arc_index}")
            sink_tokens = tuple(f"L_SINK_{j}" for j in range(len(spec["sinks"])))
            validate_graph(core, tuple(tuple(word) for word in words), sink_tokens, "L_IN")
            counts[core] += 1
    return dict(counts)


def scan_jsonl(
    path: Path,
    *,
    category_field: str | None = None,
    id_field: str | None = None,
    dense_id: bool = False,
    unique_id: bool = False,
) -> dict[str, Any]:
    started = time.monotonic()
    compressed_sha = sha_file(path)
    plain_sha = hashlib.sha256()
    plain_bytes = 0
    rows = 0
    categories: collections.Counter[str] = collections.Counter()
    ids: set[Any] | None = set() if unique_id else None
    canonical_samples = 0
    with gzip.open(path, "rb") as handle:
        for line in handle:
            if not line.endswith(b"\n"):
                raise AssertionError(("missing final newline", path, rows))
            plain_sha.update(line)
            plain_bytes += len(line)
            row = json.loads(line)
            # Sample canonical spelling regularly, while still parsing every row.
            if rows < 10 or rows % 10_000 == 0:
                if canonical(row) + b"\n" != line:
                    raise AssertionError(("noncanonical sampled row", path, rows))
                canonical_samples += 1
            if dense_id and row.get(id_field) != rows:
                raise AssertionError(("raw id order", path, rows, row.get(id_field)))
            if category_field is not None:
                value = row.get(category_field)
                if not isinstance(value, str):
                    raise AssertionError(("missing category", path, rows, category_field))
                categories[value] += 1
            if unique_id:
                value = row.get(id_field)
                if value in ids:
                    raise AssertionError(("duplicate record id", path, value))
                ids.add(value)
            rows += 1
    return {
        "path": str(path),
        "sha256": compressed_sha,
        "rows": rows,
        "uncompressed_bytes": plain_bytes,
        "uncompressed_sha256": plain_sha.hexdigest(),
        "categories": dict(sorted(categories.items())),
        "unique_ids": len(ids) if ids is not None else None,
        "canonical_rows_sampled": canonical_samples,
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }


def require_equal(name: str, observed: Any, expected: Any) -> None:
    if observed != expected:
        raise AssertionError((name, observed, expected))


def scan_restoration(project: Path) -> dict[str, Any]:
    path = project / "work/restoration_sign_reclassification/corrected_restoration_forest.json"
    started = time.monotonic()
    data = json.loads(path.read_bytes())
    first = data["first_coverage"]
    second = data["second_coverage"]
    census = data["census"]
    require_equal("restoration first hashes", [row["row_sha256"] for row in first], data["first_row_hashes"])
    require_equal("restoration second hashes", [row["row_sha256"] for row in second], data["second_row_hashes"])
    require_equal("restoration first children", len(first), 36_568)
    require_equal("restoration second children", len(second), 256)
    require_equal("restoration parent references", all(0 <= row["parent_first_coverage_index"] < len(first) for row in second), True)
    for row in second:
        parent = first[row["parent_first_coverage_index"]]
        require_equal("restoration second parent hash", row["parent_first_row_sha256"], parent["row_sha256"])
        require_equal("restoration second root", row["root_id"], parent["root_id"])
    roots = {row["root_id"] for row in first}
    require_equal("restoration roots", len(roots), 2_540)
    continuation = [row for row in first if row["status"] == "continuation"]
    require_equal("restoration continuation", len(continuation), 32)
    referenced_parents = {row["parent_first_coverage_index"] for row in second}
    require_equal("restoration referenced continuation parents", len(referenced_parents), 32)
    require_equal("restoration parent statuses", {first[i]["status"] for i in referenced_parents}, {"continuation"})
    derived = {
        "canonical_parents": census["canonical_restoration_parents"],
        "member_roots": len(roots),
        "first_children": len(first),
        "second_children": len(second),
        "forest_edges": len(first) + len(second),
        "final_leaves": (len(first) - len(continuation)) + len(second),
        "max_depth": 2 if second else 1,
        "first_proof_counts": dict(sorted(collections.Counter(row["proof"] for row in first).items())),
        "second_proof_counts": dict(sorted(collections.Counter(row["proof"] for row in second).items())),
    }
    expected = {
        "canonical_parents": 997,
        "member_roots": 2_540,
        "first_children": 36_568,
        "second_children": 256,
        "forest_edges": 36_824,
        "final_leaves": 36_792,
        "max_depth": 2,
        "first_proof_counts": census["first_proof_counts"],
        "second_proof_counts": census["second_proof_counts"],
    }
    require_equal("restoration derived census", derived, expected)
    return {
        "path": str(path),
        "sha256": sha_file(path),
        "derived": derived,
        "cycles": census["cycles"],
        "missing_children": census["missing_children"],
        "unresolved": census["unresolved"],
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }


def scan_terminal_registry(project: Path) -> dict[str, Any]:
    path = project / "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz"
    with gzip.open(path, "rt") as handle:
        data = json.load(handle)
    kinds = collections.Counter()
    degrees = collections.Counter()
    ids = set()
    for row in data["rows"]:
        class_id = (row["source_index"], row["class_id"])
        if class_id in ids:
            raise AssertionError(("duplicate terminal class", class_id))
        ids.add(class_id)
        terminal = row["terminal_certificate"]
        kinds[terminal["kind"]] += 1
        if terminal["kind"] == "exact_direct_polynomial_separator":
            degrees[int(terminal["degree"])] += 1
    require_equal("terminal class count", len(ids), 934)
    require_equal(
        "terminal kinds",
        dict(kinds),
        {
            "exact_multihomogeneous_quadratic": 839,
            "exact_direct_polynomial_separator": 36,
            "direct_hard_case_F2_F3_F4": 4,
            "exact_mixed_graph_isomorphism": 20,
            "ordinary_triangle_quotient": 35,
        },
    )
    require_equal("higher degree split", dict(degrees), {3: 2, 4: 12, 5: 22})
    return {
        "path": str(path),
        "sha256": sha_file(path),
        "class_count": len(ids),
        "kind_counts": dict(sorted(kinds.items())),
        "direct_degree_counts": {str(k): v for k, v in sorted(degrees.items())},
    }


def scan_probe_input(project: Path) -> dict[str, Any]:
    path = project / "work/adversarial_proof_review/probe_input_contract.json"
    data = json.loads(path.read_bytes())
    anchors = data["anchors"]
    require_equal("anchor count", len(anchors), 176)
    anchor_ids = {row["anchor_id"] for row in anchors}
    require_equal("anchor unique ids", len(anchor_ids), 176)
    source_sites = 0
    target_sites = 0
    site_types: collections.Counter[str] = collections.Counter()
    for row in anchors:
        for side in ("source", "target"):
            profile = row[f"{side}_candidate_profile"]
            expected_site_count = 2 * profile["port_count"] + 3 * profile["reticulation_count"] - 3
            actual_site_count = len(row["site_transport"])
            require_equal(f"{side} site formula", actual_site_count, expected_site_count)
            if side == "source":
                source_sites += actual_site_count
            else:
                target_sites += actual_site_count
        for transport in row["site_transport"]:
            site_types[f"source:{transport['source_site_type']}"] += 1
            site_types[f"target:{transport['target_site_type']}"] += 1
    require_equal("source site total", source_sites, 2_206)
    require_equal("target site total", target_sites, 2_206)
    require_equal("site type census", dict(site_types), data["candidate_census"]["site_types"])
    return {
        "path": str(path),
        "sha256": sha_file(path),
        "anchors": len(anchors),
        "source_sites": source_sites,
        "target_sites": target_sites,
        "site_types": dict(sorted(site_types.items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    started = time.monotonic()

    target_enumerations = {}
    for k in (3, 4, 5):
        for incoming in (True, False):
            key = f"k{k}_{'incoming' if incoming else 'marginal'}"
            counts = enumerate_targets(k, incoming)
            target_enumerations[key] = {"by_core": counts, "total": sum(counts.values())}
    observed_targets = {key: value["total"] for key, value in target_enumerations.items()}
    require_equal("target universe counts", observed_targets, EXPECTED["target_counts"])

    sources = {
        "raw4": enumerate_sources(("theta0", "theta1", "theta3")),
        "theta2": enumerate_sources(("theta2",)),
        "cycle": enumerate_sources(("cycle",)),
    }
    source_totals = {name: sum(values.values()) for name, values in sources.items()}
    require_equal("source supports", source_totals, {"raw4": 6, "theta2": 4, "cycle": 2})
    raw_universes = {
        "raw4": source_totals["raw4"] * observed_targets["k4_incoming"] + source_totals["raw4"] * observed_targets["k4_marginal"],
        "theta2": source_totals["theta2"] * (observed_targets["k5_incoming"] + observed_targets["k5_marginal"]),
        "cycle": source_totals["cycle"] * (observed_targets["k3_incoming"] + observed_targets["k3_marginal"]),
    }
    # Restore the explicit port-labelling permutation factors.
    raw_universes = {
        "raw4": raw_universes["raw4"] * math.factorial(4),
        "theta2": raw_universes["theta2"] * math.factorial(5),
        "cycle": raw_universes["cycle"] * math.factorial(3),
    }
    require_equal("raw universe counts", raw_universes, {"raw4": 405_216, "theta2": 2_946_240, "cycle": 13_440})
    primitive_archetypes = (
        source_totals["raw4"] + observed_targets["k4_incoming"] + observed_targets["k4_marginal"]
        + source_totals["theta2"] + observed_targets["k5_incoming"] + observed_targets["k5_marginal"]
        + source_totals["cycle"] + observed_targets["k3_incoming"] + observed_targets["k3_marginal"]
    )
    require_equal("primitive archetype count", primitive_archetypes, 10_084)

    artifact = project / "work/corrected_composite_ledgers/artifacts"
    raw4_summary = json.loads((artifact / "raw4_corrected_composite_summary.json").read_bytes())
    theta2_summary = json.loads((artifact / "theta2_corrected_composite_summary.json").read_bytes())
    scans: dict[str, Any] = {}
    scans["raw4"] = scan_jsonl(
        artifact / "raw4_corrected_composite_ledger.jsonl.gz",
        category_field="corrected_category", id_field="raw_id", dense_id=True,
    )
    scans["theta2"] = scan_jsonl(
        artifact / "theta2_corrected_composite_ledger.jsonl.gz",
        category_field="corrected_category", id_field="raw_id", dense_id=True,
    )
    cycle_promotion = json.loads((project / "work/cycle_three_port_closure/promotion/cycle_promotion_certificate.json").read_bytes())
    scans["cycle_base"] = scan_jsonl(
        project / "work/cycle_three_port_closure/promotion/cycle_base_authoritative.jsonl.gz",
        category_field="terminal_kind", id_field="raw_id", dense_id=True,
    )
    scans["cycle_full"] = scan_jsonl(
        project / "work/cycle_three_port_closure/promotion/cycle_full_authoritative.jsonl.gz",
        category_field="terminal_kind", id_field="raw_id", dense_id=True,
    )
    scans["one_port"] = scan_jsonl(
        project / "work/probe_coherence_corrected/one_port_ledger.jsonl.gz",
        category_field="status",
    )
    scans["two_port"] = scan_jsonl(
        project / "work/probe_coherence_corrected/two_port_ledger.jsonl.gz",
        category_field="status",
    )
    scans["exact_transports"] = scan_jsonl(
        project / "work/probe_coherence_corrected/exact_transport_ledger.jsonl.gz",
        id_field="record_id", unique_id=True,
    )
    scans["parent_restrictions"] = scan_jsonl(
        project / "work/probe_coherence_corrected/parent_restriction_ledger.jsonl.gz",
        id_field="record_id", unique_id=True,
    )

    for name in ("raw4", "theta2", "cycle_base", "cycle_full", "one_port", "two_port"):
        require_equal(f"{name} rows", scans[name]["rows"], EXPECTED[name]["rows"])
        require_equal(f"{name} partition", scans[name]["categories"], EXPECTED[name]["categories"])
    for name, summary in (("raw4", raw4_summary), ("theta2", theta2_summary)):
        require_equal(f"{name} compressed hash", scans[name]["sha256"], summary["ledger_sha256"])
        require_equal(f"{name} plain hash", scans[name]["uncompressed_sha256"], summary["uncompressed_stream_sha256"])
        require_equal(f"{name} plain bytes", scans[name]["uncompressed_bytes"], summary["uncompressed_bytes"])
    require_equal("cycle base hash", scans["cycle_base"]["sha256"], cycle_promotion["outputs"]["cycle_base_authoritative.jsonl.gz"]["sha256"])
    require_equal("cycle full hash", scans["cycle_full"]["sha256"], cycle_promotion["outputs"]["cycle_full_authoritative.jsonl.gz"]["sha256"])
    require_equal("exact transport rows", scans["exact_transports"]["rows"], 67_741)
    require_equal("exact transport unique", scans["exact_transports"]["unique_ids"], 67_741)
    require_equal("restriction rows", scans["parent_restrictions"]["rows"], 4_379)
    require_equal("restriction unique", scans["parent_restrictions"]["unique_ids"], 4_379)

    report = {
        "schema": "independent-k2p-primitive-and-ledger-census-v1",
        "status": "PASS",
        "method_independence": {
            "imports_submitted_code": False,
            "graph_library": None,
            "primitive_enumerator": "direct incidence lists + weak compositions + explicit repair words",
            "ledger_check": "stdlib gzip/json streaming; every row parsed; dense IDs and partitions recomputed",
            "canonical_serialization_check": "first ten and each 10,000th row",
        },
        "primitive_universe": {
            "target_enumerations": target_enumerations,
            "source_supports": sources,
            "source_totals": source_totals,
            "raw_direction_counts": raw_universes,
            "primitive_archetypes": primitive_archetypes,
        },
        "ledger_scans": scans,
        "terminal_registry": scan_terminal_registry(project),
        "restoration": scan_restoration(project),
        "probe_input": scan_probe_input(project),
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "max_rss_raw": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "platform": os.uname().sysname + " " + os.uname().release + " " + os.uname().machine,
    }
    payload = dict(report)
    report["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(json.dumps(report, sort_keys=True, indent=2).encode() + b"\n")
    print(json.dumps({"status": "PASS", "output": str(args.output), "payload_sha256": report["payload_sha256"], "elapsed_seconds": report["elapsed_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
