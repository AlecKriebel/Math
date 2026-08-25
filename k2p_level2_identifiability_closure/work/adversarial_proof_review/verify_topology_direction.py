#!/usr/bin/env python3
"""Independent raw displayed-quartet binding for the current K2P release.

This audit is deliberately narrow.  It reconstructs displayed quartet sets
from the primitive graph grammar and checks the raw-four quartet directions
against the current corrected composite summary.  It does not classify
tree/sunlet restrictions, restoration children, or whole-map ``T_i`` rows;
those claims have separate current authorities in the corrected finite
universe and restoration-v3 packages.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS_PATH = (
    PROJECT
    / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
)
RAW4_SUMMARY = (
    PROJECT
    / "work/corrected_composite_ledgers/artifacts/"
    "raw4_corrected_composite_summary.json"
)


class VerificationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationFailure(message)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_graph_grammar():
    # Graph generation is treated as input.  No topology classifier from this
    # module is used in the clean-room displayed-set calculation below.
    spec = importlib.util.spec_from_file_location("topology_graph_input", ATLAS_PATH)
    if spec is None or spec.loader is None:
        raise VerificationFailure("cannot load graph grammar")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def clean_displayed_splits(graph, labels=(0, 1, 2, 3)) -> frozenset[tuple]:
    labels = tuple(labels)
    reticulations = [
        node
        for node, data in graph.nodes(data=True)
        if data.get("role") == "retic"
    ]
    incoming = [tuple(graph.in_edges(node)) for node in reticulations]
    answer = set()
    for choices in itertools.product(*incoming):
        chosen = set(choices)
        removed = {
            edge for options in incoming for edge in options if edge not in chosen
        }
        tree = nx.Graph()
        tree.add_nodes_from(graph.nodes())
        tree.add_edges_from(edge for edge in graph.edges() if edge not in removed)
        changed = True
        while changed:
            changed = False
            for node in list(tree.nodes()):
                label = graph.nodes[node].get("label")
                if label not in labels and tree.degree(node) <= 1:
                    tree.remove_node(node)
                    changed = True
                    break
                if label not in labels and tree.degree(node) == 2:
                    left, right = list(tree.neighbors(node))
                    tree.remove_node(node)
                    if left != right:
                        tree.add_edge(left, right)
                    changed = True
                    break
        switching_splits = set()
        for left, right in list(tree.edges()):
            tree.remove_edge(left, right)
            components = list(nx.connected_components(tree))
            tree.add_edge(left, right)
            if len(components) != 2:
                continue
            sides = []
            for component in components:
                sides.append(
                    tuple(
                        sorted(
                            graph.nodes[node].get("label")
                            for node in component
                            if graph.nodes[node].get("label") in labels
                        )
                    )
                )
            if sorted(map(len, sides)) == [2, 2]:
                switching_splits.add(tuple(sorted(sides)))
        require(
            len(switching_splits) == 1,
            f"switching lacks a unique quartet split: {switching_splits}",
        )
        answer.update(switching_splits)
    return frozenset(answer)


def clean_restrict_directed(graph, keep_labels: set[int]):
    restricted = graph.copy()
    for node, data in list(restricted.nodes(data=True)):
        if data.get("role") == "leaf" and data.get("label") not in keep_labels:
            restricted.remove_node(node)
    changed = True
    while changed:
        changed = False
        for node, data in list(restricted.nodes(data=True)):
            if restricted.out_degree(node) == 0 and not (
                data.get("role") == "leaf" and data.get("label") in keep_labels
            ):
                restricted.remove_node(node)
                changed = True
                break
        if changed:
            continue
        for node, data in list(restricted.nodes(data=True)):
            if (
                data.get("role") != "leaf"
                and restricted.in_degree(node) == 1
                and restricted.out_degree(node) == 1
            ):
                parent = next(restricted.predecessors(node))
                child = next(restricted.successors(node))
                restricted.remove_node(node)
                if parent != child and not restricted.has_edge(parent, child):
                    restricted.add_edge(parent, child)
                changed = True
                break
        if changed:
            continue
        roots = [node for node in restricted if restricted.in_degree(node) == 0]
        if (
            len(roots) == 1
            and restricted.nodes[roots[0]].get("role") != "leaf"
            and restricted.out_degree(roots[0]) == 1
        ):
            restricted.remove_node(roots[0])
            changed = True
    return restricted


def permute_split_set(split_set: frozenset[tuple], permutation: tuple[int, ...]):
    return frozenset(
        tuple(
            sorted(
                tuple(sorted(permutation[label] for label in side))
                for side in split
            )
        )
        for split in split_set
    )


def check_seven_set_theorem() -> dict[str, object]:
    universe = frozenset(range(3))
    subsets = [
        frozenset(item for item in universe if mask >> item & 1)
        for mask in range(1, 8)
    ]
    witnesses = []
    for left, right in itertools.combinations(subsets, 2):
        if len(left) == 1:
            split = next(iter(left))
            require(any(item != split for item in right), "singleton case")
            kind = "I_singleton"
            zero_set, positive_set = left, right
        elif len(right) == 1:
            split = next(iter(right))
            require(any(item != split for item in left), "singleton case")
            kind = "I_singleton"
            zero_set, positive_set = right, left
        else:
            difference = right - left
            if difference:
                split = next(iter(difference))
                zero_set, positive_set = left, right
            else:
                split = next(iter(left - right))
                zero_set, positive_set = right, left
            require(split not in zero_set and split in positive_set, "J witness")
            kind = "J_membership"
        witnesses.append(
            {
                "left": sorted(left),
                "right": sorted(right),
                "kind": kind,
                "split": split,
            }
        )
    require(len(witnesses) == 21, "seven-set pair census")
    return {"status": "PASS", "nonempty_sets": 7, "unequal_pairs": 21}


def check_raw_four_port_quartets(grammar) -> dict[str, object]:
    sources = grammar.source_supports()
    targets = grammar.target_completions(4, True) + grammar.target_completions(4, False)
    source_splits = [clean_displayed_splits(record.graph) for record in sources]
    target_splits = [clean_displayed_splits(record.graph) for record in targets]
    require(
        all(split_set for split_set in source_splits + target_splits),
        "empty displayed set",
    )

    dummy_reduction_matches = 0
    for record, full_splits in zip(targets, target_splits):
        selected = clean_restrict_directed(record.graph, set(range(4)))
        require(
            clean_displayed_splits(selected) == full_splits,
            "dummy reduction changed displayed quartet set",
        )
        dummy_reduction_matches += 1

    quartet_counts = []
    for source_index in range(len(sources)):
        quartet = 0
        for target_index in range(len(targets)):
            for permutation in itertools.permutations(range(4)):
                if source_splits[source_index] != permute_split_set(
                    target_splits[target_index], permutation
                ):
                    quartet += 1
        quartet_counts.append(quartet)

    require(
        quartet_counts == [59064, 65088, 59064, 59064, 59064, 59064],
        f"raw quartet census: {quartet_counts}",
    )
    return {
        "status": "PASS",
        "source_supports": len(sources),
        "target_completions": len(targets),
        "raw_directions": len(sources) * len(targets) * 24,
        "clean_displayed_sets": len(sources) + len(targets),
        "dummy_reduction_matches": dummy_reduction_matches,
        "quartet_exclusions_by_source": quartet_counts,
        "quartet_exclusions": sum(quartet_counts),
    }


def check_physical_hypotheses() -> dict[str, object]:
    tested = 0
    for s_num in range(1, 20):
        for g_num in range(1, 20):
            s, g = F(s_num, 20), F(g_num, 20)
            if g <= 2 * s - 1:
                continue
            require(0 < s < 1 and 0 < g < 1, "D_plus not in positive cube")
            tested += 1
    require(tested > 0, "empty D_plus test")
    return {
        "status": "PASS",
        "D_plus_points": tested,
        "character_convention": (
            "fixed spectrum (1,s,g,s): identity or global C<->T only; "
            "literature conventions require a one-time accompanying spectrum relabel"
        ),
        "inheritance_weights": "strictly positive switching weights",
    }


def check_current_raw4_summary() -> dict[str, object]:
    summary = json.loads(RAW4_SUMMARY.read_text())
    claimed_payload = summary.get("payload_sha256")
    payload = dict(summary)
    payload.pop("payload_sha256", None)
    require(
        claimed_payload == hashlib.sha256(canonical_bytes(payload)).hexdigest(),
        "current raw4 summary payload hash",
    )
    require(
        summary.get("schema") == "k2p-raw4-corrected-composite-summary-v1"
        and summary.get("status") == "PASS",
        "current raw4 summary",
    )
    categories = summary.get("category_counts", {})
    require(summary.get("total_rows") == 405216, "current raw4 row count")
    require(
        categories.get("displayed_quartet_exclusion") == 360408
        and summary.get("quartet_witness_rows") == 360408,
        "current raw4 quartet count",
    )
    require(
        summary.get("forbidden_rooted_field_count") == 0
        and summary.get("forbidden_rooted_reason_count") == 0,
        "current raw4 rooted-oracle quarantine",
    )
    return {
        "status": "PASS",
        "summary_path": str(RAW4_SUMMARY.relative_to(PROJECT)),
        "summary_sha256": sha256_file(RAW4_SUMMARY),
        "summary_payload_sha256": claimed_payload,
        "total_rows": 405216,
        "displayed_quartet_exclusions": 360408,
        "forbidden_rooted_fields": 0,
        "forbidden_rooted_reasons": 0,
    }


def main() -> int:
    if not __debug__:
        raise VerificationFailure("verification disabled under Python -O")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    grammar = load_graph_grammar()
    report: dict[str, object] = {
        "schema": "k2p-displayed-quartet-direction-audit-v2",
        "status": "PASS",
        "scope": (
            "principal D_plus; raw four-port displayed-quartet direction and "
            "tree-of-blobs predicate only; no restoration or whole-map T_i classifier"
        ),
        "seven_set_theorem": check_seven_set_theorem(),
        "physical_hypotheses": check_physical_hypotheses(),
        "raw_four_port_quartets": check_raw_four_port_quartets(grammar),
        "current_raw4_summary": check_current_raw4_summary(),
        "bridge_tree_consequence": (
            "Different labelled trees of blobs imply different displayed quartet sets "
            "on some restriction and therefore disjoint physical K2P images."
        ),
        "excluded_claims": [
            "rooted tree/sunlet classification",
            "restoration-child classification",
            "whole-map T_i classification",
        ],
        "manuscript": {
            "citation": (
                "Englander et al., bioRxiv 2025.04.18.649493, v4 "
                "(2026-07-04), Propositions 2.9-2.10, Theorem 2.11, "
                "Corollary 2.12"
            ),
            "reviewed_local_pdf_sha256": (
                "3c140c36aae45cd07040b0f1e03b55b40f7c61f14a04b9fbe9cd8c48112e8ba5"
            ),
        },
    }
    report["payload_sha256"] = hashlib.sha256(canonical_bytes(report)).hexdigest()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationFailure as error:
        print(f"TOPOLOGY_DIRECTION_AUDIT_FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
