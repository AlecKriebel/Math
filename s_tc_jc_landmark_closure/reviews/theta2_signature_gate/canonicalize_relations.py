#!/usr/bin/env python3
"""Independent mixed-graph quotient for the theta-2 survivor crosswalk.

Input records are raw algebraic survivors.  This verifier reconstructs both
graphs from their primitive provenance, performs the locked standard root
suppression, and canonically labels the coloured disjoint relation.  It does
not import the signature-gate implementation or any project graph code.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import gzip
import hashlib
import itertools
import json
from pathlib import Path
from typing import Sequence


HERE = Path(__file__).resolve().parent
RAW_PATH = HERE / "presentation_crosswalk.jsonl"
FROZEN_PATH = HERE.parent.parent / "primary/certificates/hard_cover_root_cases_n4_schema3_theta2_full.jsonl.gz"

CORES = {
    "theta-2": (("S", "U"), ("S", "V"), ("U", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1")),
    "theta-3": (("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V")),
}


def stable_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def natural(label: str):
    prefix, _, suffix = label.rpartition("_")
    return prefix, int(suffix) if suffix.isdigit() else -1, label


@dataclass(frozen=True)
class Rooted:
    root: int
    labels: tuple[tuple[int, str], ...]
    arcs: tuple[tuple[int, int], ...]

    @property
    def vertices(self):
        return tuple(sorted({self.root, *(v for edge in self.arcs for v in edge), *(v for v, _ in self.labels)}))


@dataclass(frozen=True)
class Mixed:
    labels: tuple[tuple[int, str], ...]
    # edge=(min endpoint,max endpoint,heads); heads is empty for undirected
    edges: tuple[tuple[int, int, tuple[int, ...]], ...]

    @property
    def vertices(self):
        return tuple(sorted({*(v for edge in self.edges for v in edge[:2]), *(v for v, _ in self.labels)}))


def source_and_sinks(arcs: Sequence[tuple[str, str]]):
    indegree = Counter(v for _, v in arcs)
    outdegree = Counter(u for u, _ in arcs)
    vertices = {x for edge in arcs for x in edge}
    sources = [v for v in vertices if indegree[v] == 0]
    if len(sources) != 1:
        raise AssertionError((arcs, sources))
    sinks = tuple(sorted(v for v in vertices if indegree[v] == 2 and outdegree[v] == 0))
    return sources[0], sinks


def build_graph(core: str, words: Sequence[Sequence[str]], sink_labels: dict[str, str]):
    arcs = CORES[core]
    ids = {}

    def vertex(key):
        if key not in ids:
            ids[key] = len(ids)
        return ids[key]

    for name in sorted({x for edge in arcs for x in edge}):
        vertex(("core", name))
    source, _ = source_and_sinks(arcs)
    root = vertex(("root",))
    incoming = vertex(("leaf", "INCOMING"))
    labels = {incoming: "INCOMING"}
    directed = [(root, vertex(("core", source))), (root, incoming)]
    for edge_index, ((tail, head), word) in enumerate(zip(arcs, words)):
        prior = vertex(("core", tail))
        for position, label in enumerate(word):
            subdivision = vertex(("subdivision", edge_index, position))
            leaf = vertex(("leaf", edge_index, position))
            labels[leaf] = label
            directed.extend(((prior, subdivision), (subdivision, leaf)))
            prior = subdivision
        directed.append((prior, vertex(("core", head))))
    for sink, label in sorted(sink_labels.items()):
        leaf = vertex(("sink", sink))
        labels[leaf] = label
        directed.append((vertex(("core", sink)), leaf))
    return Rooted(root, tuple(sorted(labels.items())), tuple(directed))


def reconstruct_source(provenance):
    core, _repair_index, words = provenance
    if core != "theta-2":
        raise AssertionError(core)
    return build_graph(core, words, {"X0": "Q_SINK_0", "X1": "Q_SINK_1"})


def reconstruct_target(provenance):
    core, sink_mask, _repair_index, words, _dummy_roles, _incoming_selected = provenance
    if core not in CORES:
        raise AssertionError(core)
    _, sinks = source_and_sinks(CORES[core])
    sink_labels = {}
    for index, sink in enumerate(sinks):
        sink_labels[sink] = f"SINK_{index}" if sink_mask & (1 << index) else f"D_SINK_{index}"
    return build_graph(core, words, sink_labels)


def selected_target_labels(provenance):
    core, sink_mask, _repair_index, words, _dummy_roles, incoming_selected = provenance
    _, sinks = source_and_sinks(CORES[core])
    labels = [label for word in words for label in word if not label.startswith("D_")]
    labels.extend(f"SINK_{index}" for index, _sink in enumerate(sinks) if sink_mask & (1 << index))
    labels = sorted(labels, key=natural)
    if incoming_selected:
        labels.append("INCOMING")
    if len(labels) != 5:
        raise AssertionError((provenance, labels))
    return tuple(labels)


def relabel_boundaries(graph: Rooted, selected_labels: Sequence[str], assignment: Sequence[int]):
    if sorted(assignment) != list(range(5)) or len(selected_labels) != 5:
        raise AssertionError((selected_labels, assignment))
    mapping = {label: f"L_{actual}" for label, actual in zip(selected_labels, assignment)}
    # All unselected physical boundaries are existential restoration
    # placeholders.  Their sink/segment/incoming placement is encoded by the
    # graph itself; provenance names and restoration order are not topology.
    labels = tuple(sorted((vertex, mapping.get(label, "DUMMY")) for vertex, label in graph.labels))
    return Rooted(graph.root, labels, graph.arcs)


def sd0(graph: Rooted):
    indegree = Counter(v for _, v in graph.arcs)
    retics = {v for v in graph.vertices if indegree[v] == 2}
    root_edges = [(u, v) for u, v in graph.arcs if u == graph.root]
    if len(root_edges) != 2:
        raise AssertionError("root is not binary")
    root_children = [v for _u, v in root_edges]
    edge_map = {}

    def add(u: int, v: int, heads=()):
        if u == v:
            raise AssertionError("root suppression created loop")
        a, b = sorted((u, v))
        key = (a, b)
        value = tuple(sorted(heads))
        if key in edge_map:
            raise AssertionError("root suppression created parallel edge")
        edge_map[key] = value

    for u, v in graph.arcs:
        if u == graph.root:
            continue
        add(u, v, (v,) if v in retics else ())
    a, b = root_children
    heads = tuple(v for v in (a, b) if v in retics)
    add(a, b, heads)
    labels = tuple(sorted((v, label) for v, label in graph.labels if v != graph.root))
    return Mixed(labels, tuple(sorted((u, v, heads) for (u, v), heads in edge_map.items())))


def canonical_mixed(graph: Mixed):
    vertices = graph.vertices
    labels = dict(graph.labels)
    adjacency = {v: {} for v in vertices}
    retics = set()
    for u, v, heads in graph.edges:
        if not heads:
            adjacency[u][v] = "U"
            adjacency[v][u] = "U"
        elif heads == (v,):
            adjacency[u][v] = "OUT"
            adjacency[v][u] = "IN"
            retics.add(v)
        elif heads == (u,):
            adjacency[u][v] = "IN"
            adjacency[v][u] = "OUT"
            retics.add(u)
        else:
            raise AssertionError((u, v, heads))

    initial = {}
    for vertex in vertices:
        label = labels.get(vertex)
        if label is not None:
            initial[vertex] = ("leaf", label)
        elif vertex in retics:
            initial[vertex] = ("retic",)
        else:
            initial[vertex] = ("ordinary",)

    def normalize(features):
        palette = {value: index for index, value in enumerate(sorted(set(features.values()), key=repr))}
        return {vertex: palette[value] for vertex, value in features.items()}

    def refine(colours):
        while True:
            old_partition = {
                frozenset(vertex for vertex in vertices if colours[vertex] == colour)
                for colour in set(colours.values())
            }
            features = {
                vertex: (
                    colours[vertex],
                    tuple(sorted((relation, colours[neighbor]) for neighbor, relation in adjacency[vertex].items())),
                )
                for vertex in vertices
            }
            moved = normalize(features)
            new_partition = {
                frozenset(vertex for vertex in vertices if moved[vertex] == colour)
                for colour in set(moved.values())
            }
            if new_partition == old_partition:
                return moved
            colours = moved

    best = None
    best_map = None

    def serialize(colours):
        order = tuple(sorted(vertices, key=lambda v: colours[v]))
        position = {vertex: index for index, vertex in enumerate(order)}
        vertex_rows = tuple(initial[vertex] for vertex in order)
        edge_rows = []
        for u, v, heads in graph.edges:
            a, b = position[u], position[v]
            moved_heads = tuple(sorted(position[head] for head in heads))
            edge_rows.append((min(a, b), max(a, b), moved_heads))
        return (vertex_rows, tuple(sorted(edge_rows))), position

    def search(colours):
        nonlocal best, best_map
        colours = refine(colours)
        cells = defaultdict(list)
        for vertex, colour in colours.items():
            cells[colour].append(vertex)
        nonsingle = [values for _colour, values in sorted(cells.items()) if len(values) > 1]
        if not nonsingle:
            code, mapping = serialize(colours)
            if best is None or repr(code) < repr(best):
                best, best_map = code, mapping
            return
        cell = min(nonsingle, key=lambda values: (len(values), tuple(values)))
        next_colour = max(colours.values()) + 1
        for vertex in sorted(cell):
            moved = dict(colours)
            moved[vertex] = next_colour
            search(moved)

    search(normalize(initial))
    if best is None or best_map is None:
        raise AssertionError("canonicalization failed")
    return json.dumps(best, sort_keys=True, separators=(",", ":")), best_map


def relation_from_normalized(normalized):
    source_graph = reconstruct_source(normalized["source_provenance"])
    source_labels = ("Q_REPAIR_0", "Q_REPAIR_1", "Q_SINK_0", "Q_SINK_1", "INCOMING")
    source = relabel_boundaries(source_graph, source_labels, normalized["source_position_to_label"])
    target_graph = reconstruct_target(normalized["target_provenance"])
    target_labels = selected_target_labels(normalized["target_provenance"])
    target = relabel_boundaries(target_graph, target_labels, normalized["target_position_to_label"])
    source_code, source_map = canonical_mixed(sd0(source))
    target_code, target_map = canonical_mixed(sd0(target))
    # Unique matched L_i colours encode all five cross-side matching edges;
    # side order and direction are retained by the ordered pair.
    code = json.dumps({
        "direction": "source_precedes_target",
        "source": source_code,
        "target": target_code,
    }, sort_keys=True, separators=(",", ":"))
    return code, {
        "source_raw_to_canonical": sorted(source_map.items()),
        "target_raw_to_canonical": sorted(target_map.items()),
    }


def raw_records():
    rows = []
    with RAW_PATH.open() as handle:
        for line in handle:
            row = json.loads(line)
            rows.append(row["normalized_relation"])
    return rows


def frozen_records():
    rows = []
    with gzip.open(FROZEN_PATH, "rt", encoding="utf-8") as handle:
        for line in handle:
            root = json.loads(line)["root_case"]
            rows.append({
                "direction": "source_precedes_target",
                "selected_outgoing": root["selected_outgoing"],
                "selected_signature_sha256": root["selected_signature_sha256"],
                "source_position_to_label": root["source_position_to_label"],
                "source_provenance": root["source_provenance"],
                "target_provenance": root["target_provenance"],
                "target_dummy_roles": root["target_dummy_roles"],
                "target_position_to_label": root["target_position_to_label"],
            })
    return rows


def canonicalize(rows):
    multiset = Counter()
    transports = defaultdict(list)
    modes = Counter()
    for index, normalized in enumerate(rows):
        code, transport = relation_from_normalized(normalized)
        digest = hashlib.sha256(code.encode()).hexdigest()
        multiset[digest] += 1
        modes["selected" if normalized["target_provenance"][-1] else "marginalized"] += 1
        transports[digest].append({
            "record_index": index,
            "incoming_mode": "selected" if normalized["target_provenance"][-1] else "marginalized",
            "source_provenance": normalized["source_provenance"],
            "target_provenance": normalized["target_provenance"],
            "target_position_to_label": normalized["target_position_to_label"],
            **transport,
        })
    return multiset, transports, modes


def target_topology_code(normalized):
    graph = reconstruct_target(normalized["target_provenance"])
    selected = set(selected_target_labels(normalized["target_provenance"]))
    labels = tuple(sorted(
        (vertex, "SELECTED" if label in selected else "DUMMY")
        for vertex, label in graph.labels
    ))
    code, _mapping = canonical_mixed(sd0(Rooted(graph.root, labels, graph.arcs)))
    return hashlib.sha256(code.encode()).hexdigest()


def mixed_transport(left_normalized, right_normalized, *, side):
    if side == "source":
        left_rooted = relabel_boundaries(
            reconstruct_source(left_normalized["source_provenance"]),
            ("Q_REPAIR_0", "Q_REPAIR_1", "Q_SINK_0", "Q_SINK_1", "INCOMING"),
            left_normalized["source_position_to_label"],
        )
        right_rooted = relabel_boundaries(
            reconstruct_source(right_normalized["source_provenance"]),
            ("Q_REPAIR_0", "Q_REPAIR_1", "Q_SINK_0", "Q_SINK_1", "INCOMING"),
            right_normalized["source_position_to_label"],
        )
        left_physical = dict(reconstruct_source(left_normalized["source_provenance"]).labels)
        right_physical = dict(reconstruct_source(right_normalized["source_provenance"]).labels)
    elif side == "target":
        left_original = reconstruct_target(left_normalized["target_provenance"])
        right_original = reconstruct_target(right_normalized["target_provenance"])
        left_rooted = relabel_boundaries(
            left_original, selected_target_labels(left_normalized["target_provenance"]),
            left_normalized["target_position_to_label"],
        )
        right_rooted = relabel_boundaries(
            right_original, selected_target_labels(right_normalized["target_provenance"]),
            right_normalized["target_position_to_label"],
        )
        left_physical = dict(left_original.labels)
        right_physical = dict(right_original.labels)
    else:
        raise ValueError(side)
    left_mixed, right_mixed = sd0(left_rooted), sd0(right_rooted)
    left_code, left_map = canonical_mixed(left_mixed)
    right_code, right_map = canonical_mixed(right_mixed)
    if left_code != right_code:
        raise AssertionError("transport requested across nonisomorphic mixed graphs")
    inverse_right = {canonical: raw for raw, canonical in right_map.items()}
    transport = {raw: inverse_right[canonical] for raw, canonical in left_map.items()}
    left_labels = dict(left_mixed.labels)
    right_labels = dict(right_mixed.labels)
    if {left_labels[v] for v in left_labels} != {right_labels[v] for v in right_labels}:
        raise AssertionError("label-colour sets differ")
    for vertex, label in left_labels.items():
        if right_labels.get(transport[vertex]) != label:
            raise AssertionError((side, "label transport", vertex, label))
    def moved_edges(graph, mapping):
        answer = set()
        for u, v, heads in graph.edges:
            a, b = sorted((mapping[u], mapping[v]))
            answer.add((a, b, tuple(sorted(mapping[head] for head in heads))))
        return answer
    if moved_edges(left_mixed, transport) != set(right_mixed.edges):
        raise AssertionError((side, "edge transport"))
    dummy_transport = []
    for left_vertex, left_role in left_physical.items():
        if left_role.startswith("D_") or left_role == "INCOMING" and left_labels.get(left_vertex) == "DUMMY":
            right_vertex = transport[left_vertex]
            right_role = right_physical[right_vertex]
            if right_labels.get(right_vertex) != "DUMMY":
                raise AssertionError("omitted boundary mapped to selected boundary")
            dummy_transport.append((left_role, right_role))
    return {
        "vertex_transport": sorted(transport.items()),
        "omitted_physical_role_transport": sorted(dummy_transport),
    }


def main():
    raw = raw_records()
    frozen = frozen_records()
    direct = [row for row in raw if not row["target_dummy_roles"]]
    nonretaining = [row for row in raw if row["target_dummy_roles"]]
    nonretaining_marginalized = [row for row in nonretaining if not row["target_provenance"][-1]]
    nonretaining_selected = [row for row in nonretaining if row["target_provenance"][-1]]

    direct_multiset, direct_transports, direct_modes = canonicalize(direct)
    nonretaining_multiset, nonretaining_transports, nonretaining_modes = canonicalize(nonretaining)
    marginalized_multiset, marginalized_transports, marginalized_modes = canonicalize(nonretaining_marginalized)
    frozen_multiset, frozen_transports, frozen_modes = canonicalize(frozen)
    nonretaining_set = set(nonretaining_multiset)
    marginalized_set = set(marginalized_multiset)
    frozen_set = set(frozen_multiset)

    direct_classifications = []
    for index, row in enumerate(direct):
        relation_code, _ = relation_from_normalized(row)
        parts = json.loads(relation_code)
        direct_classifications.append({
            "record_index": index,
            "classification": "labelled_mixed_graph_isomorphism" if parts["source"] == parts["target"] else "UNRESOLVED",
            "canonical_relation_sha256": hashlib.sha256(relation_code.encode()).hexdigest(),
        })

    # Pair the independently generated 132 marginalized descriptions with
    # the frozen inventory inside each canonical decorated relation class.
    presentation_transports = []
    for digest in sorted(frozen_set & marginalized_set):
        left_rows = [nonretaining_marginalized[row["record_index"]]
                     for row in marginalized_transports[digest]]
        right_rows = [frozen[row["record_index"]] for row in frozen_transports[digest]]
        if len(left_rows) != len(right_rows):
            continue
        for left, right in zip(left_rows, right_rows):
            presentation_transports.append({
                "canonical_relation_sha256": digest,
                "source_transport": mixed_transport(left, right, side="source"),
                "target_transport": mixed_transport(left, right, side="target"),
                "generated_target_provenance": left["target_provenance"],
                "frozen_target_provenance": right["target_provenance"],
            })

    # Every selected-incoming nonretaining presentation must be an admissible
    # root-presentation duplicate of a frozen marginalized root.  Give the
    # explicit mixed-graph transport, including omitted physical roles.
    selected_duplicate_transports = []
    for selected in nonretaining_selected:
        code, _ = relation_from_normalized(selected)
        digest = hashlib.sha256(code.encode()).hexdigest()
        candidates = frozen_transports.get(digest, [])
        if not candidates:
            continue
        frozen_row = frozen[candidates[0]["record_index"]]
        selected_duplicate_transports.append({
            "canonical_relation_sha256": digest,
            "selected_target_provenance": selected["target_provenance"],
            "frozen_target_provenance": frozen_row["target_provenance"],
            "source_transport": mixed_transport(selected, frozen_row, side="source"),
            "target_transport": mixed_transport(selected, frozen_row, side="target"),
        })

    mutations = []
    def record(name, rejected, reason):
        mutations.append({"name": name, "rejected": bool(rejected), "reason": reason})

    same_target = defaultdict(set)
    for row in frozen:
        relation_code, _ = relation_from_normalized(row)
        digest = hashlib.sha256(relation_code.encode()).hexdigest()
        same_target[target_topology_code(row)].add(digest)
    distinct_pair = next((sorted(values)[:2] for values in same_target.values() if len(values) >= 2), None)
    if distinct_pair is None:
        record("collapse_distinct_relations_sharing_target", False, "no adversarial pair found")
    else:
        mutated = Counter(marginalized_multiset)
        mutated[distinct_pair[0]] += mutated[distinct_pair[1]]
        del mutated[distinct_pair[1]]
        record("collapse_distinct_relations_sharing_target", mutated != frozen_multiset,
               "canonical multiset loses one port-matched directed relation despite shared unlabelled target topology")

    omitted = Counter(marginalized_multiset)
    first = next(iter(omitted))
    omitted[first] -= 1
    if not omitted[first]:
        del omitted[first]
    record("delete_nonretaining_presentation", omitted != frozen_multiset,
           "canonical multiplicity comparison detects one omitted presentation")

    direct_ok = all(row["classification"] == "labelled_mixed_graph_isomorphism"
                    for row in direct_classifications)
    marginalized_exact = marginalized_multiset == frozen_multiset
    selected_duplicates_ok = len(selected_duplicate_transports) == len(nonretaining_selected)

    status = "VERIFIED" if (
        len(direct) == 18 and direct_ok
        and len(nonretaining_marginalized) == 132 and marginalized_exact
        and len(nonretaining_selected) == 42 and selected_duplicates_ok
        and nonretaining_set == frozen_set
        and len(presentation_transports) == 132
        and all(row["rejected"] for row in mutations)
    ) else "FALSE"
    certificate = {
        "schema": "theta2-decorated-mixed-relation-quotient-v1",
        "status": status,
        "raw_survivor_presentations": len(raw),
        "intrinsic_partition": {
            "direct_no_omitted_roles": len(direct),
            "nonretaining_selected_incoming": len(nonretaining_selected),
            "nonretaining_marginalized_incoming": len(nonretaining_marginalized),
        },
        "direct_canonical_relation_count": len(direct_multiset),
        "direct_all_labelled_isomorphism": direct_ok,
        "direct_classifications": direct_classifications,
        "nonretaining_canonical_relation_count": len(nonretaining_set),
        "nonretaining_mode_counts": dict(sorted(nonretaining_modes.items())),
        "nonretaining_canonical_multiplicity_distribution": dict(sorted(Counter(nonretaining_multiset.values()).items())),
        "frozen_presentations": len(frozen),
        "frozen_incoming_modes": dict(sorted(frozen_modes.items())),
        "frozen_canonical_relation_count": len(frozen_set),
        "frozen_canonical_multiplicity_distribution": dict(sorted(Counter(frozen_multiset.values()).items())),
        "marginalized_presentation_multiset_equals_frozen": marginalized_exact,
        "marginalized_only": sorted(marginalized_set - frozen_set),
        "frozen_only": sorted(frozen_set - marginalized_set),
        "nonretaining_set_equals_frozen": nonretaining_set == frozen_set,
        "selected_incoming_duplicate_transport_count": len(selected_duplicate_transports),
        "presentation_transport_count": len(presentation_transports),
        "canonical_set_sha256": stable_hash(sorted(frozen_set)),
        "mutations": mutations,
        "method": {
            "imports_other_code": False,
            "standard_reduction": "reticulation arrowheads retained; binary root suppressed once; no further cleanup",
            "canonicalizer": "independent individualization-refinement over mixed-edge incidence",
            "matched_ports": "L_0,...,L_4 fixed jointly on source and target",
            "dummy_policy": "omitted boundaries have one placeholder colour; structural attachment is retained and every quotient carries an explicit omitted-role vertex transport",
            "root_marker_policy": "forgotten in sd0; incoming role is recorded only as presentation provenance",
        },
    }
    (HERE / "canonical_quotient_certificate.json").write_text(json.dumps(certificate, sort_keys=True, indent=2) + "\n")
    with (HERE / "canonical_duplicate_transports.jsonl").open("w") as handle:
        for row in selected_duplicate_transports:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    with (HERE / "frozen_presentation_transports.jsonl").open("w") as handle:
        for row in presentation_transports:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({
        "status": status,
        "raw": len(raw),
        "direct": len(direct),
        "nonretaining_selected": len(nonretaining_selected),
        "nonretaining_marginalized": len(nonretaining_marginalized),
        "frozen": len(frozen),
        "frozen_classes": len(frozen_set),
        "selected_duplicate_transports": len(selected_duplicate_transports),
        "marginalized_multiset_equal": marginalized_exact,
    }, sort_keys=True))
    if status != "VERIFIED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
