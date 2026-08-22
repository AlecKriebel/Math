#!/usr/bin/env python3
"""Independent algebraic reclassification of the revoked raw-four sign rows.

No rooted restriction or tree/sunlet label is consulted.  The program starts
from the raw graph encodings, canonicalizes exact ordered labelled mixed-graph
pairs, compiles full K2P Fourier descriptors, and partitions every row by an
exact graph terminal, rank obstruction, existing direct certificate, exact
quadratic, or an explicit unresolved restoration/direct obligation.
"""

from __future__ import annotations

import collections
import gzip
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS_PATH = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
RAW_LEDGER = PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
DIRECT_CLOSURE = PROJECT / "work/four_port_direct_residual_closure_certificate.json"
OUTPUT = HERE / "raw4_sign_reclassification.json"


class Failure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_atlas():
    spec = importlib.util.spec_from_file_location("raw4_sign_clean_atlas", ATLAS_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def ordinary_triangles(mixed):
    answer = []
    for a, b, c in itertools.combinations(sorted(mixed.nodes(), key=repr), 3):
        if not (mixed.has_edge(a, b) and mixed.has_edge(a, c) and mixed.has_edge(b, c)):
            continue
        edges = frozenset((frozenset((a, b)), frozenset((a, c)), frozenset((b, c))))
        headed = []
        valid = True
        for edge in edges:
            left, right = tuple(edge)
            heads = mixed.edges[left, right].get("heads", frozenset())
            if len(heads) > 1:
                valid = False
                break
            if heads:
                headed.append(next(iter(heads)))
        if valid and len(headed) == 2 and headed[0] == headed[1]:
            answer.append(edges)
    return answer


def incidence(atlas, mixed, triangle=None):
    triangle = frozenset() if triangle is None else triangle
    result = nx.Graph()
    for node, data in mixed.nodes(data=True):
        result.add_node(("v", node), kind="vertex", label=data.get("label"), triangle=False)
    for number, (left, right, data) in enumerate(sorted(mixed.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1])))):
        edge = frozenset((left, right))
        edge_node = ("e", number)
        result.add_node(edge_node, kind="edge", label=None, triangle=edge in triangle)
        heads = data.get("heads", frozenset())
        result.add_edge(edge_node, ("v", left), head=False if edge in triangle else left in heads)
        result.add_edge(edge_node, ("v", right), head=False if edge in triangle else right in heads)
    return result


def exact_relation(atlas, source_graph, target_graph):
    try:
        source_mixed, target_mixed = atlas.sd0_mixed(source_graph), atlas.sd0_mixed(target_graph)
    except ValueError:
        return "none", ()
    node_match = lambda left, right: (
        left.get("kind") == right.get("kind")
        and left.get("label") == right.get("label")
        and left.get("triangle") == right.get("triangle")
    )
    edge_match = lambda left, right: left.get("head") == right.get("head")

    def mappings(source_triangle=None, target_triangle=None):
        matcher = nx.algorithms.isomorphism.GraphMatcher(
            incidence(atlas, source_mixed, source_triangle),
            incidence(atlas, target_mixed, target_triangle),
            node_match=node_match,
            edge_match=edge_match,
        )
        records = set()
        for mapping in matcher.isomorphisms_iter():
            public = tuple(sorted(
                (repr(node), repr(mapping[("v", node)][1]))
                for node in source_mixed.nodes()
            ))
            records.add(sha(public))
        return records

    isomorphisms = mappings()
    if isomorphisms:
        return "isomorphic", tuple(sorted(isomorphisms))
    triangles = set()
    for source_triangle in ordinary_triangles(source_mixed):
        for target_triangle in ordinary_triangles(target_mixed):
            triangles.update(mappings(source_triangle, target_triangle))
    return ("triangle", tuple(sorted(triangles))) if triangles else ("none", ())


def ordered_pair_graph(atlas, source_graph, target_graph):
    result = nx.Graph()
    for side, graph in (("S", source_graph), ("T", target_graph)):
        try:
            mixed = atlas.sd0_mixed(graph)
            expanded = atlas.mixed_incidence_graph(mixed)
        except ValueError:
            expanded = nx.Graph()
            for node, data in graph.nodes(data=True):
                expanded.add_node(
                    ("v", node), kind=f"rooted_vertex:{data.get('role')}",
                    label=data.get("label"),
                )
            for number, (tail, head) in enumerate(sorted(graph.edges(), key=lambda edge: (repr(edge[0]), repr(edge[1])))):
                edge_node = ("a", number)
                expanded.add_node(edge_node, kind="rooted_arc", label=None)
                expanded.add_edge(edge_node, ("v", tail), head=False)
                expanded.add_edge(edge_node, ("v", head), head=True)
        for node, data in expanded.nodes(data=True):
            result.add_node(
                (side, node),
                color=f"{side}|{data.get('kind')}|{data.get('label')!r}",
            )
        for left, right, data in expanded.edges(data=True):
            result.add_edge((side, left), (side, right), head=bool(data.get("head")))
    return result


class PairRegistry:
    def __init__(self):
        self.representatives = []
        self.buckets = collections.defaultdict(list)

    def add(self, graph):
        bucket = nx.weisfeiler_lehman_graph_hash(graph, node_attr="color", edge_attr="head", iterations=8)
        node_match = lambda left, right: left.get("color") == right.get("color")
        edge_match = lambda left, right: left.get("head") == right.get("head")
        for class_id in self.buckets[bucket]:
            if nx.is_isomorphic(graph, self.representatives[class_id], node_match=node_match, edge_match=edge_match):
                return class_id
        class_id = len(self.representatives)
        self.representatives.append(graph)
        self.buckets[bucket].append(class_id)
        return class_id


def sparse_public(polynomial):
    return [[list(exponent), str(coefficient)] for exponent, coefficient in sorted(polynomial.items())]


def evaluate_sparse(polynomial, point):
    total = 0
    for exponent, coefficient in polynomial.items():
        term = coefficient
        for value, power in zip(point, exponent):
            if power:
                term *= value ** power
        total += term
    return total


def quadratic_certificate(atlas, source, target):
    separator = atlas.quadratic_separator_fast(source, target, max_block_size=16)
    if separator is None:
        return None
    target_outputs = atlas.output_sparse_polynomials(target)
    target_columns = [
        atlas.sparse_mul(target_outputs[left], target_outputs[right])
        for left, right in separator["coordinate_pairs"]
    ]
    require(not atlas.sparse_lincomb(target_columns, separator["coefficients"]), "quadratic nonzero on target")
    source_pullback = separator["source_pullback"]
    require(bool(source_pullback), "quadratic zero on source")
    witness = None
    for salt in range(32):
        edge_pairs, lambdas = atlas.default_exact_point(source, salt)
        point = tuple(value for pair in edge_pairs for value in pair) + tuple(lambdas)
        value = evaluate_sparse(source_pullback, point)
        if value:
            witness = {
                "salt": salt,
                "edge_pairs": [[str(s), str(g)] for s, g in edge_pairs],
                "lambdas": [str(item) for item in lambdas],
                "source_value": str(value),
            }
            break
    require(witness is not None, "quadratic lacks exact source witness")
    return {
        "degree": 2,
        "weight": list(separator["weight"]),
        "coordinate_pairs": [list(pair) for pair in separator["coordinate_pairs"]],
        "coefficients": [str(value) for value in separator["coefficients"]],
        "source_pullback_sha256": sha(sparse_public(source_pullback)),
        "source_pullback_terms": len(source_pullback),
        "strict_source_witness": witness,
    }


def main():
    if not __debug__:
        raise Failure("RAW4_SIGN_OPTIMIZED_MODE_FORBIDDEN")
    atlas = load_atlas()
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    direct = json.loads(DIRECT_CLOSURE.read_text())
    direct_keys = {
        (row["source_index"], row["target_index"], tuple(row["port_match"])): row
        for row in direct["coverage"]
    }
    rows = []
    with gzip.open(RAW_LEDGER, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("topology_exclusion_reason") == "tree_sunlet":
                rows.append(row)
    require(len(rows) == 16974, f"revoked row census {len(rows)}")

    source_descriptors = [atlas.model_descriptor_fast2(record.graph) for record in sources]
    target_cache = {}
    descriptor_registry = {}
    descriptor_examples = {}
    descriptor_multiplicity = collections.Counter()
    pair_registry = PairRegistry()
    pair_examples = {}
    pair_multiplicity = collections.Counter()
    descriptor_graph_classes = collections.defaultdict(set)
    row_bindings = []
    for number, row in enumerate(rows):
        key = (row["target_index"], tuple(row["port_permutation"]))
        if key not in target_cache:
            record = atlas.relabel_record(targets[row["target_index"]], tuple(row["port_permutation"]))
            graph = atlas.selected_graph_from_completion(record)
            target_cache[key] = (record, graph, atlas.model_descriptor_fast2(graph))
        record, target_graph, target_descriptor = target_cache[key]
        source_graph = sources[row["source_index"]].graph
        source_descriptor = source_descriptors[row["source_index"]]
        descriptor_pair = (source_descriptor, target_descriptor)
        if descriptor_pair not in descriptor_registry:
            descriptor_registry[descriptor_pair] = len(descriptor_registry)
        descriptor_class_id = descriptor_registry[descriptor_pair]
        descriptor_multiplicity[descriptor_class_id] += 1
        descriptor_examples.setdefault(descriptor_class_id, (source_graph, target_graph, row, record))

        graph_pair_class_id = pair_registry.add(ordered_pair_graph(atlas, source_graph, target_graph))
        pair_multiplicity[graph_pair_class_id] += 1
        pair_examples.setdefault(graph_pair_class_id, (source_graph, target_graph, descriptor_class_id))
        descriptor_graph_classes[descriptor_class_id].add(graph_pair_class_id)
        row_bindings.append({
            "raw_id": row["raw_id"],
            "source_index": row["source_index"],
            "target_index": row["target_index"],
            "port_permutation": row["port_permutation"],
            "descriptor_pair_class_id": descriptor_class_id,
            "graph_pair_class_id": graph_pair_class_id,
            "target_dummy_roles": list(record.dummy_labels),
        })
        if number and number % 2500 == 0:
            print(f"raw4-sign: canonicalized {number}/{len(rows)}", file=sys.stderr, flush=True)

    require(len(pair_examples) == len(pair_registry.representatives), "pair registry coverage")
    pair_relations = {}
    for class_id, (source_graph, target_graph, descriptor_class_id) in sorted(pair_examples.items()):
        status, mappings = exact_relation(atlas, source_graph, target_graph)
        pair_relations[class_id] = {
            "status": status,
            "mapping_multiplicity": len(mappings),
            "mapping_hashes": list(mappings),
            "descriptor_pair_class_id": descriptor_class_id,
        }

    descriptor_classes = []
    class_categories = {}
    for descriptor_pair, class_id in sorted(descriptor_registry.items(), key=lambda item: item[1]):
        source_descriptor, target_descriptor = descriptor_pair
        source_graph, target_graph, example, record = descriptor_examples[class_id]
        source_rank = atlas.rank_certificate(source_descriptor)["rank"]
        target_rank = atlas.rank_certificate(target_descriptor)["rank"]
        graph_classes = sorted(descriptor_graph_classes[class_id])
        relation_statuses = collections.Counter(
            pair_relations[pair_id]["status"] for pair_id in graph_classes
        )
        direct_key = (example["source_index"], example["target_index"], tuple(example["port_permutation"]))
        direct_certificate = direct_keys.get(direct_key)
        quadratic = None
        if relation_statuses.get("none") and source_rank <= target_rank and direct_certificate is None:
            quadratic = quadratic_certificate(atlas, source_descriptor, target_descriptor)
        if not relation_statuses.get("none"):
            category = "labelled_graph_terminal"
        elif source_rank > target_rank:
            category = "rank_excluded"
        elif direct_certificate is not None:
            category = "existing_direct_separator"
        elif quadratic is not None:
            category = "new_quadratic_separator"
        elif source_descriptor == target_descriptor:
            category = "descriptor_equal_candidate"
        elif record.dummy_labels:
            category = "restoration_candidate"
        else:
            category = "direct_unresolved"
        class_categories[class_id] = category
        descriptor_classes.append({
            "descriptor_pair_class_id": class_id,
            "raw_multiplicity": descriptor_multiplicity[class_id],
            "source_descriptor_sha256": sha(source_descriptor.__dict__),
            "target_descriptor_sha256": sha(target_descriptor.__dict__),
            "source_rank": source_rank,
            "target_rank": target_rank,
            "graph_pair_class_ids": graph_classes,
            "graph_relation_class_counts": dict(sorted(relation_statuses.items())),
            "category": category,
            "quadratic_certificate": quadratic,
            "existing_direct_certificate": None if direct_certificate is None else {
                "family": direct_certificate["family"],
                "polynomial_sha256": direct_certificate["polynomial_sha256"],
                "semantic_record_sha256": direct_certificate["semantic_record_sha256"],
            },
            "example": {
                "raw_id": example["raw_id"],
                "source_index": example["source_index"],
                "target_index": example["target_index"],
                "port_permutation": example["port_permutation"],
                "dummy_roles": list(record.dummy_labels),
            },
        })

    raw_category_counts = collections.Counter()
    raw_relation_counts = collections.Counter()
    unresolved_rows = []
    for binding in row_bindings:
        relation = pair_relations[binding["graph_pair_class_id"]]["status"]
        raw_relation_counts[relation] += 1
        category = class_categories[binding["descriptor_pair_class_id"]]
        if relation in {"isomorphic", "triangle"}:
            category = f"labelled_{relation}"
        raw_category_counts[category] += 1
        binding["category"] = category
        binding["graph_relation"] = relation
        if category in {"descriptor_equal_candidate", "restoration_candidate", "direct_unresolved"}:
            unresolved_rows.append(binding)

    summary = {
        "schema": "k2p-raw4-revoked-sign-reclassification-v1",
        "status": "PASS" if not unresolved_rows else "INCOMPLETE",
        "claim_boundary": "algebraic reclassification of the 16,974 revoked rooted-triple exclusions only",
        "raw_rows": len(rows),
        "unique_relabelled_targets": len(target_cache),
        "exact_ordered_labelled_graph_pair_classes": len(pair_registry.representatives),
        "exact_descriptor_pair_classes": len(descriptor_registry),
        "raw_graph_relation_counts": dict(sorted(raw_relation_counts.items())),
        "raw_category_counts": dict(sorted(raw_category_counts.items())),
        "descriptor_class_category_counts": dict(sorted(collections.Counter(class_categories.values()).items())),
        "rows_not_handled_by_graph_rank_direct_or_quadratic": len(unresolved_rows),
        "unresolved_row_hashes": [sha(row) for row in unresolved_rows],
        "graph_pair_classes": [
            {
                "graph_pair_class_id": class_id,
                "raw_multiplicity": pair_multiplicity[class_id],
                **pair_relations[class_id],
            }
            for class_id in sorted(pair_relations)
        ],
        "descriptor_pair_classes": descriptor_classes,
        "raw_binding_hashes": [sha(row) for row in row_bindings],
        "raw_binding_hash_root": sha([sha(row) for row in row_bindings]),
        "inputs": {
            "atlas_sha256": sha_file(ATLAS_PATH),
            "raw_ledger_sha256": sha_file(RAW_LEDGER),
            "existing_direct_closure_sha256": sha_file(DIRECT_CLOSURE),
        },
    }
    summary["payload_sha256"] = sha(summary)
    OUTPUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": summary["status"],
        "raw": summary["raw_rows"],
        "graph_pair_classes": summary["exact_ordered_labelled_graph_pair_classes"],
        "descriptor_pair_classes": summary["exact_descriptor_pair_classes"],
        "raw_relations": summary["raw_graph_relation_counts"],
        "raw_categories": summary["raw_category_counts"],
        "unhandled": summary["rows_not_handled_by_graph_rank_direct_or_quadratic"],
        "payload_sha256": summary["payload_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print(f"RAW4_SIGN_RECLASSIFICATION_FAIL:{error}", file=sys.stderr)
        raise SystemExit(1)
