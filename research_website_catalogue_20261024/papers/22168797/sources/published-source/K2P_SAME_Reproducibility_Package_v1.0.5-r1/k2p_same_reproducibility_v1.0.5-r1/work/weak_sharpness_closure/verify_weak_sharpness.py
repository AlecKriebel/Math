#!/usr/bin/env python3
"""Exact proof replay for the weak-tree-child K2P sharpness family.

The verifier reconstructs the two three-port semi-directed networks from their
primitive theta cores.  It then certifies their rooting censuses, inequivalence
modulo the ordinary-triangle relation, a common strict continuous-time K2P
tensor at two submersive parameter points, and the four-dimensional cherry
extension used for every additional leaf.

No atlas pickle or precomputed rank table is read.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS_DIR = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas"
sys.path.insert(0, str(ATLAS_DIR))

import k2p_atlas_core as atlas  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_object(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def fraction_text(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def primitive_network(
    core_id: str,
    arcs: tuple[tuple[str, str], ...],
    reticulations: frozenset[str],
    words: tuple[tuple[int, ...], ...],
    sink_labels: tuple[tuple[str, int], ...],
) -> nx.DiGraph:
    """Build a rooted representative without assuming that rooting is tree-child."""
    graph = nx.DiGraph(core_id=core_id)
    core_nodes = sorted({node for edge in arcs for node in edge})
    for name in core_nodes:
        graph.add_node(
            ("core", name),
            role="retic" if name in reticulations else "tree",
            label=None,
            dummy=False,
        )
    root = ("root",)
    incoming_leaf = ("leaf", "INCOMING")
    graph.add_node(root, role="root", label=None, dummy=False)
    graph.add_node(incoming_leaf, role="leaf", label=0, dummy=False)
    graph.add_edge(root, ("core", "S"), edge_role="incoming_core")
    graph.add_edge(root, incoming_leaf, edge_role="incoming_arm")

    for arc_index, ((tail, head), word) in enumerate(zip(arcs, words)):
        previous = ("core", tail)
        for position, label in enumerate(word):
            subdivision = ("sub", arc_index, position)
            leaf = ("leaf", "seg", arc_index, position)
            graph.add_node(subdivision, role="tree", label=None, dummy=False)
            graph.add_node(leaf, role="leaf", label=label, dummy=False)
            graph.add_edge(previous, subdivision, edge_role=f"seg{arc_index}")
            graph.add_edge(subdivision, leaf, edge_role="arm")
            previous = subdivision
        graph.add_edge(previous, ("core", head), edge_role=f"seg{arc_index}")

    for sink_number, (sink, label) in enumerate(sink_labels):
        leaf = ("leaf", "sink", sink_number)
        graph.add_node(leaf, role="leaf", label=label, dummy=False)
        graph.add_edge(("core", sink), leaf, edge_role="sink_arm")

    require(nx.is_directed_acyclic_graph(graph), f"{core_id}: primitive graph is cyclic")
    require(
        sorted(data["label"] for _, data in graph.nodes(data=True) if isinstance(data.get("label"), int))
        == [0, 1, 2],
        f"{core_id}: wrong boundary labels",
    )
    return graph


def weak_pair() -> tuple[nx.DiGraph, nx.DiGraph]:
    # W: theta0 with the unique outgoing boundary subdivision on V -> X.
    theta0_arcs = (("S", "U"), ("S", "V"), ("U", "X"), ("V", "X"), ("U", "V"))
    first = primitive_network(
        "theta0_segment3",
        theta0_arcs,
        frozenset(("V", "X")),
        ((), (), (), (1,), ()),
        (("X", 2),),
    )

    # W': the bare theta3 core, with its two sink children selected.
    theta3_arcs = (
        ("S", "U"),
        ("S", "X0"),
        ("V", "X0"),
        ("U", "X1"),
        ("V", "X1"),
        ("U", "V"),
    )
    second = primitive_network(
        "theta3_bare",
        theta3_arcs,
        frozenset(("X0", "X1")),
        ((), (), (), (), (), ()),
        (("X0", 1), ("X1", 2)),
    )
    return first, second


def graph_payload(graph: nx.DiGraph) -> dict[str, object]:
    def node_key(node: object) -> str:
        return repr(node)

    return {
        "nodes": [
            {
                "id": node_key(node),
                "role": data.get("role"),
                "label": data.get("label"),
            }
            for node, data in sorted(graph.nodes(data=True), key=lambda row: node_key(row[0]))
        ],
        "edges": [
            [node_key(u), node_key(v)]
            for u, v in sorted(graph.edges(), key=lambda edge: (node_key(edge[0]), node_key(edge[1])))
        ],
    }


def semi_directed_data(graph: nx.DiGraph) -> tuple[nx.Graph, frozenset[tuple[object, object]]]:
    roots = [node for node in graph if graph.in_degree(node) == 0]
    require(len(roots) == 1, "rooted representative does not have one root")
    root = roots[0]
    children = tuple(graph.successors(root))
    require(len(children) == 2, "root does not have two children")

    underlying = nx.Graph()
    underlying.add_nodes_from((node, data.copy()) for node, data in graph.nodes(data=True) if node != root)
    underlying.add_edges_from((u, v) for u, v in graph.edges() if u != root)
    underlying.add_edge(children[0], children[1])
    arrowheads = frozenset(
        (u, v)
        for u, v in graph.edges()
        if u != root and graph.nodes[v].get("role") == "retic"
    )
    return underlying, arrowheads


def tree_child(graph: nx.DiGraph, root: object) -> bool:
    for node, data in graph.nodes(data=True):
        if node == root or data.get("role") != "leaf":
            if not any(
                graph.nodes[child].get("role") in ("tree", "leaf")
                for child in graph.successors(node)
            ):
                return False
    return True


def rooting_census(graph: nx.DiGraph) -> dict[str, object]:
    """Enumerate every edge-rooting and every compatible orientation exactly."""
    underlying, arrowheads = semi_directed_data(graph)
    edges = tuple(sorted(underlying.edges(), key=lambda edge: (repr(edge[0]), repr(edge[1]))))
    rows: list[dict[str, object]] = []

    for edge_index, root_edge in enumerate(edges):
        new_root = ("candidate_root", edge_index)
        base = nx.DiGraph()
        base.add_nodes_from((node, data.copy()) for node, data in underlying.nodes(data=True))
        base.add_node(new_root, role="root", label=None)
        base.add_edge(new_root, root_edge[0])
        base.add_edge(new_root, root_edge[1])

        free_edges: list[tuple[object, object]] = []
        for edge in edges:
            if edge == root_edge:
                continue
            if edge in arrowheads:
                base.add_edge(*edge)
            elif (edge[1], edge[0]) in arrowheads:
                base.add_edge(edge[1], edge[0])
            else:
                free_edges.append(edge)

        valid: list[bool] = []
        for choices in itertools.product((0, 1), repeat=len(free_edges)):
            rooted = base.copy()
            for edge, choice in zip(free_edges, choices):
                rooted.add_edge(edge[choice], edge[1 - choice])
            if not nx.is_directed_acyclic_graph(rooted):
                continue
            good = True
            for node, data in rooted.nodes(data=True):
                degree = (rooted.in_degree(node), rooted.out_degree(node))
                if node == new_root:
                    expected = (0, 2)
                elif data.get("role") == "leaf":
                    expected = (1, 0)
                elif data.get("role") == "retic":
                    expected = (2, 1)
                else:
                    expected = (1, 2)
                if degree != expected:
                    good = False
                    break
            if good:
                valid.append(tree_child(rooted, new_root))

        if valid:
            require(len(valid) == 1, "an edge admitted more than one binary orientation")
            rows.append(
                {
                    "edge": sorted((repr(root_edge[0]), repr(root_edge[1]))),
                    "tree_child": valid[0],
                }
            )

    return {
        "admissible_rootings": len(rows),
        "tree_child_rootings": sum(row["tree_child"] for row in rows),
        "rows": rows,
    }


def descriptor_payload(descriptor: atlas.MapDescriptor) -> dict[str, object]:
    return {
        "k": descriptor.k,
        "retic_count": descriptor.retic_count,
        "edge_class_count": descriptor.edge_class_count,
        "outputs": descriptor.outputs,
        "edge_signatures": descriptor.edge_signatures,
    }


def evaluate_case(
    graph: nx.DiGraph,
    internal_value: F,
    lambdas: tuple[F, F],
    arm_coefficients: tuple[F, F, F],
    delta: F,
) -> dict[str, object]:
    slow = atlas.model_descriptor(graph)
    fast = atlas.model_descriptor_fast2(graph)
    require(slow == fast, "the two exact descriptor canonicalizers disagree")
    descriptor = fast
    require(descriptor.k == 3, "descriptor is not a three-port map")
    require(descriptor.retic_count == 2, "descriptor does not have two reticulations")
    require(descriptor.edge_class_count == 7, "descriptor does not have seven internal edge classes")

    edge_pairs = tuple((internal_value, internal_value) for _ in range(descriptor.edge_class_count))
    normalized = atlas.eval_descriptor(descriptor, edge_pairs, lambdas)
    jacobian = atlas.descriptor_jacobian(descriptor, edge_pairs, lambdas)
    rank, rows, columns = atlas.exact_rank_pivots(jacobian)
    require(rank == 9, "three-port map is not submersive")
    minor = [[jacobian[row][column] for column in columns] for row in rows]
    determinant = atlas.determinant_square(minor)
    require(determinant != 0, "stored rank minor vanishes")

    assignments = atlas.orbit_assignments(3)
    arm_pairs = tuple((coefficient * delta, coefficient * delta) for coefficient in arm_coefficients)
    for s_value, g_value in (*edge_pairs, *arm_pairs):
        require(0 < s_value < 1 and 0 < g_value < 1, "edge is outside the positive box")
        require(g_value > 2 * s_value - 1, "edge is outside D_plus")
        require(g_value > s_value * s_value, "edge is outside the strict continuous-time cone")
    require(all(0 < value < 1 for value in lambdas), "inheritance parameter is not strict")

    full_tensor: list[F] = []
    for characters, core_value in zip(assignments, normalized):
        arm_factor = F(1)
        for label, character in enumerate(characters):
            if character in (1, 3):
                arm_factor *= arm_pairs[label][0]
            elif character == 2:
                arm_factor *= arm_pairs[label][1]
        full_tensor.append(core_value * arm_factor)

    expected = [F(1)]
    for characters in assignments[1:]:
        nonzero = sum(character != 0 for character in characters)
        expected.append(delta**2 if nonzero == 2 else F(4, 5) * delta**3)
    require(tuple(full_tensor) == tuple(expected), "physical tensors do not have the locked common form")

    return {
        "graph_sha256": sha_object(graph_payload(graph)),
        "descriptor_sha256": sha_object(descriptor_payload(descriptor)),
        "edge_class_count": descriptor.edge_class_count,
        "internal_edge_pair": [fraction_text(internal_value), fraction_text(internal_value)],
        "lambdas": [fraction_text(value) for value in lambdas],
        "arm_pairs": [[fraction_text(s), fraction_text(g)] for s, g in arm_pairs],
        "normalized_tensor": [fraction_text(value) for value in normalized],
        "full_tensor": [fraction_text(value) for value in full_tensor],
        "rank": rank,
        "minor_rows": list(rows),
        "minor_columns": list(columns),
        "minor_determinant": fraction_text(determinant),
    }


def cherry_certificate() -> dict[str, object]:
    # In each character sector use the local rational coordinates R=u/v, P=uv.
    # Their Jacobian has determinant 2u/v.  The s and g sectors are independent.
    u_s, v_s, u_g, v_g = F(2, 5), F(3, 7), F(4, 9), F(5, 11)
    det_s = F(2) * u_s / v_s
    det_g = F(2) * u_g / v_g
    determinant = det_s * det_g
    require(determinant == F(4) * u_s * u_g / (v_s * v_g), "cherry determinant identity failed")
    require(determinant != 0, "cherry rank block is singular")
    # The two physical cherry edges pair the s- and g-sector coordinates
    # crosswise; check those actual edge pairs, not four artificial diagonal
    # pairs in the separate sectors.
    for s_value, g_value in ((u_s, u_g), (v_s, v_g)):
        require(g_value > s_value * s_value, "locked cherry witness is not continuous-time")
    return {
        "local_coordinates": ["u_s/v_s", "u_s*v_s", "u_g/v_g", "u_g*v_g"],
        "block_determinants": [fraction_text(det_s), fraction_text(det_g)],
        "four_by_four_determinant": fraction_text(determinant),
        "dimension_formula": "9+4*(n-3)=4*n-3",
        "pruning_implications": {
            "weak_not_strong": "a tree-child and a non-tree-child base rooting both lift; pruning and suppressing the cherry returns them",
            "inequivalence": "a labelled isomorphism or ordinary-triangle relation after identical cherry attachment restricts to one on the base pair",
        },
    }


def main() -> None:
    if not __debug__:
        raise SystemExit("WEAK_SHARPNESS_OPTIMIZED_MODE_FORBIDDEN")

    first, second = weak_pair()
    first_census = rooting_census(first)
    second_census = rooting_census(second)
    require(
        (first_census["admissible_rootings"], first_census["tree_child_rootings"]) == (5, 2),
        "first rooting census changed",
    )
    require(
        (second_census["admissible_rootings"], second_census["tree_child_rootings"]) == (7, 2),
        "second rooting census changed",
    )
    relation = atlas.mixed_relation_exact(first, second)
    require(relation == "none", "base pair became isomorphic or an ordinary-triangle pair")

    delta = F(1, 2**30)
    first_case = evaluate_case(
        first,
        F(1, 7),
        (F(15996, 16339), F(1, 8)),
        (F(86779, 80), F(320, 253), F(114373, 20240)),
        delta,
    )
    second_case = evaluate_case(
        second,
        F(1, 4),
        (F(1, 2), F(1, 6)),
        (F(16, 3), F(32, 9), F(96, 5)),
        delta,
    )
    require(first_case["full_tensor"] == second_case["full_tensor"], "common tensor equality failed")

    payload = {
        "schema": "k2p-weak-tree-child-sharpness-v1",
        "domain": "strict continuous-time subset of D_plus",
        "coordinate_order": atlas.orbit_assignments(3),
        "delta": fraction_text(delta),
        "graph_relation": relation,
        "first": {"rooting_census": first_census, "parameter_certificate": first_case},
        "second": {"rooting_census": second_census, "parameter_certificate": second_case},
        "common_tensor": first_case["full_tensor"],
        "base_dimension": 9,
        "cherry_extension": cherry_certificate(),
        "conclusion": {
            "base": "distinct weakly-but-not-strongly tree-child level-2 networks share a 9-dimensional image germ",
            "all_n_at_least_3": "iterated identical labelled cherries give distinct weakly-but-not-strongly tree-child level-2 networks with a common (4*n-3)-dimensional germ",
        },
    }
    certificate = dict(payload)
    certificate["payload_sha256"] = sha_object(payload)
    output_path = HERE / "weak_sharpness_certificate.json"
    output_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print("K2P_WEAK_SHARPNESS_PASS")
    print(json.dumps({
        "payload_sha256": certificate["payload_sha256"],
        "certificate_sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(),
        "rooting_censuses": [[5, 2], [7, 2]],
        "base_rank": [first_case["rank"], second_case["rank"]],
        "dimension": "4*n-3",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
