#!/usr/bin/env python3
"""Independent binding of displayed-set disjointness to K2P topology rows."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS_PATH = (
    PROJECT
    / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
)
RAW_SUMMARY = PROJECT / "work/raw_ledger_audit/artifacts/raw_ledger_summary.json"
RESTORATION_CERTIFICATE = PROJECT / "work/restoration_forest/five_port_certificate.json"
RESULT_ROOT = (
    PROJECT
    / "package/referee/k2p_offline_sweep_portable/results/four_port_release_v4"
)
CONTINUATION_VERIFIER = (
    PROJECT
    / "package/original/checkpoint_2/continuation_2/verify_triangle_and_sunlet.py"
)


class VerificationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationFailure(message)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


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


def clean_triple_type(graph, triple: tuple[int, int, int]) -> str:
    restricted = clean_restrict_directed(graph, set(triple))
    reticulations = sum(
        restricted.in_degree(node) == 2 for node in restricted.nodes()
    )
    if reticulations == 0:
        return "tree"
    if reticulations == 1:
        return "sunlet"
    return f"r{reticulations}"


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


def permute_triples(types: dict[tuple[int, ...], str], permutation: tuple[int, ...]):
    return {
        tuple(sorted(permutation[label] for label in triple)): value
        for triple, value in types.items()
    }


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


def check_four_port_binding(grammar) -> dict[str, object]:
    sources = grammar.source_supports()
    targets = grammar.target_completions(4, True) + grammar.target_completions(4, False)
    source_splits = [clean_displayed_splits(record.graph) for record in sources]
    target_splits = [clean_displayed_splits(record.graph) for record in targets]
    require(all(split_set for split_set in source_splits + target_splits), "empty displayed set")

    dummy_reduction_matches = 0
    for record, full_splits in zip(targets, target_splits):
        selected = clean_restrict_directed(record.graph, set(range(4)))
        require(
            clean_displayed_splits(selected) == full_splits,
            "dummy reduction changed displayed quartet set",
        )
        dummy_reduction_matches += 1

    triples = tuple(itertools.combinations(range(4), 3))
    source_triples = [
        {triple: clean_triple_type(record.graph, triple) for triple in triples}
        for record in sources
    ]
    target_triples = [
        {triple: clean_triple_type(record.graph, triple) for triple in triples}
        for record in targets
    ]

    quartet_counts = []
    tree_sunlet_counts = []
    for source_index in range(len(sources)):
        quartet = 0
        tree_sunlet = 0
        for target_index in range(len(targets)):
            for permutation in itertools.permutations(range(4)):
                mapped_splits = permute_split_set(
                    target_splits[target_index], permutation
                )
                if source_splits[source_index] != mapped_splits:
                    quartet += 1
                    continue
                mapped_types = permute_triples(
                    target_triples[target_index], permutation
                )
                if any(
                    {
                        source_triples[source_index][triple],
                        mapped_types[triple],
                    }
                    == {"tree", "sunlet"}
                    for triple in triples
                ):
                    tree_sunlet += 1
        quartet_counts.append(quartet)
        tree_sunlet_counts.append(tree_sunlet)

    require(
        quartet_counts == [59064, 65088, 59064, 59064, 59064, 59064],
        f"raw quartet census: {quartet_counts}",
    )
    require(
        tree_sunlet_counts == [1878, 72, 3756, 3756, 3756, 3756],
        f"raw tree-sunlet census: {tree_sunlet_counts}",
    )
    return {
        "status": "PASS",
        "source_supports": len(sources),
        "target_completions": len(targets),
        "clean_displayed_sets": len(sources) + len(targets),
        "dummy_reduction_matches": dummy_reduction_matches,
        "quartet_exclusions_by_source": quartet_counts,
        "tree_sunlet_exclusions_by_source": tree_sunlet_counts,
        "quartet_exclusions": sum(quartet_counts),
        "tree_sunlet_exclusions": sum(tree_sunlet_counts),
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
    # Strict sign boundary: all listed factors are positive, including
    # (1-f_g)^2 because 0<f_g<1.
    delta, d_g, e_g, f_g = F(2, 5), F(3, 7), F(5, 11), F(7, 13)
    sign_factor = -delta * (1 - delta) * d_g * e_g * (1 - f_g) ** 2
    require(sign_factor < 0, "tree-sunlet strict sign")
    return {
        "status": "PASS",
        "D_plus_points": tested,
        "character_convention": "equal-pair relabel by Aut(Z2 x Z2)",
        "inheritance_weights": "strictly positive switching weights",
        "tree_sunlet_sign": str(sign_factor),
    }


def source_insertion_candidates(graph) -> list[dict[str, object]]:
    rows = []
    for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    ):
        if graph.nodes[head].get("role") == "leaf":
            continue
        if graph.nodes[tail].get("role") == "root":
            continue
        rows.append(
            {
                "tail": repr(tail),
                "head": repr(head),
                "edge_role": data.get("edge_role"),
            }
        )
    return rows


def clean_reconstruct_restoration_roots(sources, targets) -> list[dict[str, object]]:
    roots = []
    canonical_parents = 0
    for path in sorted(RESULT_ROOT.glob("source_*/residual_manifest.json")):
        manifest = json.loads(path.read_text())
        source_index = manifest["source_index"]
        expected_candidates = source_insertion_candidates(sources[source_index].graph)
        for record in manifest["records"]:
            if record["status"] != "restoration_parent":
                continue
            canonical_parents += 1
            attachments: dict[tuple, dict[str, dict]] = {}
            frozen_candidates = None
            for request in record["child_requests"]:
                candidates = request["source_insertion_edge_candidates"]
                require(candidates == expected_candidates, "restoration source candidates")
                if frozen_candidates is None:
                    frozen_candidates = candidates
                require(candidates == frozen_candidates, "candidate drift across roles")
                role = request["omitted_role"]
                for attachment in request["target_dummy_attachments"]:
                    key = (
                        attachment["target_index"],
                        tuple(attachment["port_match"]),
                    )
                    attachments.setdefault(key, {})[role] = attachment
            require(frozen_candidates is not None, "parent without child request")
            for (target_index, permutation), by_role in sorted(attachments.items()):
                roles = tuple(sorted(by_role))
                require(
                    roles == tuple(targets[target_index].dummy_labels),
                    "restoration role union",
                )
                roots.append(
                    {
                        "source_index": source_index,
                        "target_index": target_index,
                        "permutation": permutation,
                        "roles": roles,
                        "candidates": frozen_candidates,
                    }
                )
    require(canonical_parents == 997, "canonical restoration parent count")
    require(len(roots) == 2540, "restoration member-root count")
    return roots


def clean_insert_source_leaf(graph, candidate: dict[str, object], label: int = 4):
    result = graph.copy()
    tail = ast.literal_eval(candidate["tail"])
    head = ast.literal_eval(candidate["head"])
    require(result.has_edge(tail, head), "source insertion edge missing")
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = ("clean_restoration_subdivision", label, repr(tail), repr(head))
    leaf = ("leaf", "clean_restoration", label)
    result.add_node(subdivision, role="tree", label=None, dummy=False)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    return result


def clean_promote_target(record, permutation: tuple[int, ...], role: str, label: int = 4):
    result = record.graph.copy()
    for _, data in result.nodes(data=True):
        old_label = data.get("label")
        if isinstance(old_label, int):
            data["label"] = permutation[old_label]
    nodes = [
        node
        for node, data in result.nodes(data=True)
        if data.get("dummy_name") == role
    ]
    require(len(nodes) == 1, "target promoted role not unique")
    result.nodes[nodes[0]]["label"] = label
    result.nodes[nodes[0]]["dummy"] = False
    result.nodes[nodes[0]]["dummy_name"] = None
    return result


def five_port_signature(graph) -> tuple:
    return tuple(
        (quartet, clean_displayed_splits(graph, quartet))
        for quartet in itertools.combinations(range(5), 4)
    )


def five_port_triples(graph) -> dict[tuple[int, ...], str]:
    return {
        triple: clean_triple_type(graph, triple)
        for triple in itertools.combinations(range(5), 3)
    }


def check_restoration_topology_binding(grammar) -> dict[str, object]:
    sources = grammar.source_supports()
    targets = grammar.target_completions(4, True) + grammar.target_completions(4, False)
    roots = clean_reconstruct_restoration_roots(sources, targets)
    source_graphs = {}
    target_graphs = {}
    source_signatures = {}
    target_signatures = {}
    source_triples = {}
    target_triples = {}

    for root in roots:
        source_index = root["source_index"]
        for insertion_index, candidate in enumerate(root["candidates"]):
            key = (source_index, insertion_index)
            if key not in source_graphs:
                source_graphs[key] = clean_insert_source_leaf(
                    sources[source_index].graph, candidate
                )
                source_signatures[key] = five_port_signature(source_graphs[key])
        for role in root["roles"]:
            key = (root["target_index"], root["permutation"], role)
            if key not in target_graphs:
                target_graphs[key] = clean_promote_target(
                    targets[root["target_index"]], root["permutation"], role
                )
                target_signatures[key] = five_port_signature(target_graphs[key])

    quartet_mismatch = 0
    tree_sunlet = 0
    equal_deck = 0
    raw = 0
    for root in roots:
        for role in root["roles"]:
            target_key = (root["target_index"], root["permutation"], role)
            for insertion_index, _ in enumerate(root["candidates"]):
                source_key = (root["source_index"], insertion_index)
                raw += 1
                if source_signatures[source_key] != target_signatures[target_key]:
                    quartet_mismatch += 1
                    continue
                if source_key not in source_triples:
                    source_triples[source_key] = five_port_triples(
                        source_graphs[source_key]
                    )
                if target_key not in target_triples:
                    target_triples[target_key] = five_port_triples(
                        target_graphs[target_key]
                    )
                if any(
                    {source_triples[source_key][triple], target_triples[target_key][triple]}
                    == {"tree", "sunlet"}
                    for triple in source_triples[source_key]
                ):
                    tree_sunlet += 1
                else:
                    equal_deck += 1

    require(raw == 36568, f"restoration raw topology census: {raw}")
    require(quartet_mismatch == 35758, f"restoration quartet census: {quartet_mismatch}")
    require(tree_sunlet == 646, f"restoration sign census: {tree_sunlet}")
    require(equal_deck == 164, f"restoration equal-deck census: {equal_deck}")
    return {
        "status": "PASS",
        "member_roots": len(roots),
        "unique_source_children": len(source_graphs),
        "unique_target_promotions": len(target_graphs),
        "raw_children": raw,
        "displayed_quartet_mismatch": quartet_mismatch,
        "strict_tree_sunlet": tree_sunlet,
        "equal_topology_deck": equal_deck,
    }


def check_published_ledgers() -> dict[str, object]:
    raw = json.loads(RAW_SUMMARY.read_text())
    restoration = json.loads(RESTORATION_CERTIFICATE.read_text())
    require(raw["partition_counts"]["topology_excluded"] == 377382, "raw topology total")
    proof_counts = restoration["census"]["proof_counts"]
    require(proof_counts["displayed_quartet_mismatch"] == 35758, "restoration quartet total")
    require(proof_counts["strict_tree_sunlet_sign"] == 646, "restoration sign total")
    return {
        "status": "PASS",
        "raw_topology_excluded": 377382,
        "raw_quartet": 360408,
        "raw_tree_sunlet": 16974,
        "restoration_quartet": 35758,
        "restoration_tree_sunlet": 646,
    }


def main() -> int:
    if not __debug__:
        raise VerificationFailure("verification disabled under Python -O")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    grammar = load_graph_grammar()
    report: dict[str, object] = {
        "schema": "k2p-directional-topology-audit-v1",
        "status": "PASS",
        "scope": "principal D_plus; exact physical disjointness, not generic distinction",
        "seven_set_theorem": check_seven_set_theorem(),
        "physical_hypotheses": check_physical_hypotheses(),
        "four_port_binding": check_four_port_binding(grammar),
        "restoration_topology_binding": check_restoration_topology_binding(grammar),
        "published_ledgers": check_published_ledgers(),
        "bridge_tree_consequence": (
            "Different labelled trees of blobs imply different displayed quartet sets "
            "on some restriction and therefore disjoint physical K2P images."
        ),
        "manuscript": {
            "citation": "Englander et al., bioRxiv 2025.04.18.649493, v4 (2026-07-04), Propositions 2.9-2.10, Theorem 2.11, Corollary 2.12",
            "reviewed_local_pdf_sha256": "3c140c36aae45cd07040b0f1e03b55b40f7c61f14a04b9fbe9cd8c48112e8ba5",
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
