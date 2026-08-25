#!/usr/bin/env python3
"""Independent/adversarial audit of the repaired H21 clean-room gate.

Topology is reconstructed from the frozen literal records and checked with a
NetworkX incidence-graph encoding that is independent of the corrected
verifier's custom backtracker.  Fourier relabelling is checked a second time
by direct exact numerical switching evaluation on physical edges.  The final
section applies fail-closed mutations to the corrected verifier.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import permutations, product
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
CLEAN_ROOM = HERE.parent
PROJECT = CLEAN_ROOM.parent
ARTIFACTS = PROJECT / "input_frozen" / "k3p_cloud_artifacts"
LOCK_PATH = ARTIFACTS / "K3P_14_ORBIT_LOCK.json"
LOCK = json.loads(LOCK_PATH.read_text())
RECORDS = {record["orbit_id"]: record for record in LOCK["records"]}
IDENTITY = (0, 1, 2, 3)
S4 = tuple(permutations(range(4)))
CH4 = tuple(prefix + (prefix[0] ^ prefix[1] ^ prefix[2],)
            for prefix in product(range(4), repeat=3))
CH4_INDEX = {assignment: index for index, assignment in enumerate(CH4)}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compose(left, right):
    return tuple(left[right[index]] for index in range(4))


def inverse(perm):
    result = [None] * len(perm)
    for old, new in enumerate(perm):
        if not isinstance(new, int) or not 0 <= new < len(perm):
            raise ValueError(("not a permutation", perm))
        if result[new] is not None:
            raise ValueError(("not a permutation", perm))
        result[new] = old
    if any(value is None for value in result):
        raise ValueError(("not a permutation", perm))
    return tuple(result)


@dataclass(frozen=True)
class LiteralGraph:
    nodes: dict
    arcs: tuple

    @classmethod
    def from_json(cls, literal):
        nodes = {}
        for entry in literal["nodes"]:
            node = ast.literal_eval(entry["id"])
            data = dict(entry)
            data.pop("id")
            nodes[node] = data
        arcs = tuple(
            (ast.literal_eval(entry["tail"]), ast.literal_eval(entry["head"]))
            for entry in literal["arcs"]
        )
        if len(arcs) != len(set(arcs)):
            raise AssertionError("parallel rooted arcs")
        return cls(nodes, tuple(sorted(arcs, key=repr)))

    def relabel(self, perm):
        inverse(perm)
        nodes = {node: dict(data) for node, data in self.nodes.items()}
        for data in nodes.values():
            label = data.get("label")
            if isinstance(label, int):
                data["label"] = perm[label]
        return LiteralGraph(nodes, self.arcs)


@dataclass(frozen=True)
class MixedGraph:
    nodes: dict
    edges: dict


def rooted_adjacency(graph: LiteralGraph):
    incoming = defaultdict(list)
    outgoing = defaultdict(list)
    for tail, head in graph.arcs:
        outgoing[tail].append(head)
        incoming[head].append(tail)
    return incoming, outgoing


def root_suppress(graph: LiteralGraph) -> MixedGraph:
    """Independent implementation of the fixed sd_0 operation."""
    incoming, outgoing = rooted_adjacency(graph)
    roots = [node for node, data in graph.nodes.items()
             if data["role"] == "root"]
    if len(roots) != 1:
        raise AssertionError(("root count", roots))
    root = roots[0]
    expected_degree = {
        "root": (0, 2),
        "tree": (1, 2),
        "retic": (2, 1),
        "leaf": (1, 0),
    }
    for node, data in graph.nodes.items():
        actual = (len(incoming[node]), len(outgoing[node]))
        if actual != expected_degree[data["role"]]:
            raise AssertionError((node, data["role"], actual))
    directed = nx.DiGraph()
    directed.add_nodes_from(graph.nodes)
    directed.add_edges_from(graph.arcs)
    if not nx.is_directed_acyclic_graph(directed):
        raise AssertionError("rooted graph is cyclic")
    if set(nx.descendants(directed, root)) | {root} != set(graph.nodes):
        raise AssertionError("root does not reach every vertex")

    mixed_nodes = {node: dict(data) for node, data in graph.nodes.items()
                   if node != root}
    edges = {}

    def add_edge(first, second, heads):
        endpoints = frozenset((first, second))
        if len(endpoints) != 2 or endpoints in edges:
            raise AssertionError(("nonsimple sd0", first, second))
        heads = frozenset(heads)
        if not heads <= endpoints:
            raise AssertionError(("bad arrowhead incidence", endpoints, heads))
        edges[endpoints] = heads

    for tail, head in graph.arcs:
        if tail == root:
            continue
        heads = (head,) if graph.nodes[head]["role"] == "retic" else ()
        add_edge(tail, head, heads)
    children = tuple(outgoing[root])
    heads = tuple(child for child in children
                  if graph.nodes[child]["role"] == "retic")
    add_edge(children[0], children[1], heads)

    degree = defaultdict(int)
    head_count = defaultdict(int)
    for endpoints, heads in edges.items():
        for node in endpoints:
            degree[node] += 1
            if node in heads:
                head_count[node] += 1
    expected_mixed = {
        "leaf": (1, 0),
        "tree": (3, 0),
        "retic": (3, 2),
    }
    for node, data in mixed_nodes.items():
        actual = (degree[node], head_count[node])
        if actual != expected_mixed[data["role"]]:
            raise AssertionError(("role/incidence mismatch", node,
                                  data["role"], actual))
    return MixedGraph(mixed_nodes, edges)


def incidence_expansion(graph: MixedGraph, ignore_heads=False,
                        ignore_roles=False):
    """Encode endpoint arrowheads as colored incidence vertices."""
    expanded = nx.Graph()
    for node, data in graph.nodes.items():
        expanded.add_node(
            ("vertex", node),
            kind="vertex",
            role=None if ignore_roles else data["role"],
            label=data.get("label"),
        )
    for index, (endpoints, heads) in enumerate(
            sorted(graph.edges.items(), key=lambda item: repr(item[0]))):
        edge_node = ("edge", index)
        expanded.add_node(edge_node, kind="edge", role=None, label=None)
        for endpoint_index, endpoint in enumerate(sorted(endpoints, key=repr)):
            headed = endpoint in heads and not ignore_heads
            incidence = ("incidence", index, endpoint_index)
            expanded.add_node(
                incidence,
                kind="headed-incidence" if headed else "plain-incidence",
                role=None,
                label=None,
            )
            expanded.add_edge(("vertex", endpoint), incidence)
            expanded.add_edge(incidence, edge_node)
    return expanded


def mixed_isomorphic(first: MixedGraph, second: MixedGraph,
                     ignore_heads=False, ignore_roles=False):
    left = incidence_expansion(first, ignore_heads, ignore_roles)
    right = incidence_expansion(second, ignore_heads, ignore_roles)
    node_match = nx.algorithms.isomorphism.categorical_node_match(
        ["kind", "role", "label"], [None, None, None]
    )
    return nx.is_isomorphic(left, right, node_match=node_match)


def mixed_vertex_isomorphism(first: MixedGraph, second: MixedGraph):
    left = incidence_expansion(first)
    right = incidence_expansion(second)
    node_match = nx.algorithms.isomorphism.categorical_node_match(
        ["kind", "role", "label"], [None, None, None]
    )
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        left, right, node_match=node_match
    )
    if not matcher.is_isomorphic():
        return None
    return {
        old[1]: new[1]
        for old, new in matcher.mapping.items()
        if old[0] == "vertex"
    }


def rooted_isomorphic(first: LiteralGraph, second: LiteralGraph):
    left = nx.DiGraph()
    right = nx.DiGraph()
    for target, graph in ((left, first), (right, second)):
        for node, data in graph.nodes.items():
            target.add_node(node, role=data["role"], label=data.get("label"))
        target.add_edges_from(graph.arcs)
    node_match = nx.algorithms.isomorphism.categorical_node_match(
        ["role", "label"], [None, None]
    )
    matcher = nx.algorithms.isomorphism.DiGraphMatcher(
        left, right, node_match=node_match
    )
    return matcher.is_isomorphic()


def mixed_port_group(graph: LiteralGraph, ignore_heads=False,
                     ignore_roles=False):
    base = root_suppress(graph)
    return tuple(
        perm for perm in S4
        if mixed_isomorphic(base, root_suppress(graph.relabel(perm)),
                            ignore_heads=ignore_heads,
                            ignore_roles=ignore_roles)
    )


def rooted_port_group(graph: LiteralGraph):
    return tuple(perm for perm in S4
                 if rooted_isomorphic(graph, graph.relabel(perm)))


def double_coset(source_group, representative, target_group):
    return tuple(sorted({
        compose(source_auto, compose(representative, target_auto))
        for source_auto in source_group for target_auto in target_group
    }))


def descendant_masks(graph: LiteralGraph, kept_edges):
    children = defaultdict(list)
    for tail, head in kept_edges:
        children[tail].append(head)
    memo = {}

    def descend(node):
        if node in memo:
            return memo[node]
        label = graph.nodes[node].get("label")
        answer = (1 << label) if isinstance(label, int) else 0
        for child in children[node]:
            answer |= descend(child)
        memo[node] = answer
        return answer

    for node in graph.nodes:
        descend(node)
    return {edge: memo[edge[1]] for edge in kept_edges}


def sector(mask, assignment):
    answer = 0
    index = 0
    while mask:
        if mask & 1:
            answer ^= assignment[index]
        index += 1
        mask >>= 1
    return answer


def exact_switching_evaluation(graph: LiteralGraph, edge_values, lambdas):
    """Direct exact evaluator independent of the symbolic descriptor compiler."""
    incoming, _ = rooted_adjacency(graph)
    retics = tuple(sorted(
        (node for node, data in graph.nodes.items()
         if data["role"] == "retic"),
        key=repr,
    ))
    parents = tuple(tuple(sorted(incoming[node], key=repr)) for node in retics)
    if any(len(pair) != 2 for pair in parents):
        raise AssertionError("reticulation parent count")
    selected_arms = {
        edge for edge in graph.arcs
        if graph.nodes[edge[1]]["role"] == "leaf"
        and isinstance(graph.nodes[edge[1]].get("label"), int)
    }
    outputs = []
    for assignment in CH4:
        answer = Q(0)
        for bits in product((0, 1), repeat=len(retics)):
            removed = set()
            weight = Q(1)
            for index, (retic, pair, bit) in enumerate(zip(retics, parents, bits)):
                keep_parent = pair[bit]
                for parent in incoming[retic]:
                    if parent != keep_parent:
                        removed.add((parent, retic))
                weight *= lambdas[index] if bit else 1 - lambdas[index]
            kept = tuple(edge for edge in graph.arcs if edge not in removed)
            masks = descendant_masks(graph, kept)
            monomial = Q(1)
            for edge in kept:
                if edge in selected_arms:
                    continue
                character = sector(masks[edge], assignment)
                if character:
                    monomial *= edge_values[edge][character - 1]
            answer += weight * monomial
        outputs.append(answer)
    return tuple(outputs)


def independent_coordinate_transport(perm):
    inverse(perm)
    return tuple(
        CH4_INDEX[tuple(assignment[perm[old]] for old in range(4))]
        for assignment in CH4
    )


def load_corrected_verifier():
    path = CLEAN_ROOM / "verify_h21_transport_and_fourteen_orbits.py"
    spec = importlib.util.spec_from_file_location("audited_corrected_verifier", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def expect_assertion(name, function, mutations):
    try:
        function()
    except AssertionError as error:
        mutations.append({"name": name, "status": "REJECTED",
                          "exception": repr(error)[:240]})
        return
    raise AssertionError(("mutation unexpectedly accepted", name))


def run():
    if not __debug__:
        raise RuntimeError("adversarial audit itself refuses optimized Python")

    historical = CLEAN_ROOM / "HISTORICAL_cleanroom_verify_fourteen_orbits.py"
    frozen_historical = ARTIFACTS / "cleanroom_verify_fourteen_orbits.py"
    corrected_path = CLEAN_ROOM / "verify_h21_transport_and_fourteen_orbits.py"
    regression_path = CLEAN_ROOM / "test_h21_transport_regression.py"
    hashes = {
        "historical": digest(historical),
        "frozen_historical": digest(frozen_historical),
        "corrected": digest(corrected_path),
        "regression": digest(regression_path),
        "lock": digest(LOCK_PATH),
    }
    if hashes["historical"] != hashes["frozen_historical"]:
        raise AssertionError("historical verifier bytes differ")

    verifier = load_corrected_verifier()
    independent_records = {}
    reconstructions = {}
    for orbit_id, record in RECORDS.items():
        source = LiteralGraph.from_json(record["source_literal_graph"])
        target_displayed = LiteralGraph.from_json(record["target_literal_graph"])
        representative = tuple(record["representative_permutation"])
        if tuple(record["port_permutation"]) != representative:
            raise AssertionError((orbit_id, "two permutation fields disagree"))
        target_base = target_displayed.relabel(inverse(representative))
        source_group = mixed_port_group(source)
        target_group = mixed_port_group(target_base)
        displayed_group = mixed_port_group(target_displayed)
        if mixed_isomorphic(root_suppress(source), root_suppress(target_displayed)):
            raise AssertionError((orbit_id, "source and target are isomorphic"))
        reconstruction = verifier.reconstruct_record(record)
        if source_group != reconstruction["source_geometric_group"]:
            raise AssertionError((orbit_id, "source group disagreement"))
        if target_group != reconstruction["target_group"]:
            raise AssertionError((orbit_id, "target group disagreement"))
        if displayed_group != reconstruction["displayed_target_group"]:
            raise AssertionError((orbit_id, "displayed group disagreement"))
        action_source = (source_group if record["family"] ==
                         "rank21_nonautomorphic_relabelling" else (IDENTITY,))
        orbit = double_coset(action_source, representative, target_group)
        raw = tuple(sorted(tuple(member) for member in record["raw_members"]))
        if orbit != raw:
            raise AssertionError((orbit_id, orbit, raw))
        witnessed = set()
        for witness in record["raw_member_transports"]:
            source_auto = tuple(witness["source_automorphism"])
            target_auto = tuple(witness["target_automorphism"])
            member = tuple(witness["permutation"])
            if source_auto not in action_source or target_auto not in target_group:
                raise AssertionError((orbit_id, "invalid witness automorphism"))
            if member != compose(source_auto,
                                 compose(representative, target_auto)):
                raise AssertionError((orbit_id, "invalid witness equation"))
            witnessed.add(member)
        if witnessed != set(raw):
            raise AssertionError((orbit_id, "witness coverage"))
        independent_records[orbit_id] = {
            "source_group": source_group,
            "target_base_group": target_group,
            "target_displayed_group": displayed_group,
            "raw_members": raw,
        }
        reconstructions[orbit_id] = reconstruction

    # H21-01 category/arrowhead/root-suppression diagnosis.
    hrecord = RECORDS["H21-01"]
    hsource = LiteralGraph.from_json(hrecord["source_literal_graph"])
    hbase = LiteralGraph.from_json(hrecord["target_literal_graph"]).relabel(
        inverse(tuple(hrecord["representative_permutation"]))
    )
    exact_group = mixed_port_group(hsource)
    rooted_group = rooted_port_group(hsource)
    nohead_role_group = mixed_port_group(hsource, ignore_heads=True)
    nohead_untyped_group = mixed_port_group(
        hsource, ignore_heads=True, ignore_roles=True
    )
    base_auto = (2, 1, 0, 3)
    expected_exact = (IDENTITY, (2, 1, 0, 3))
    expected_nohead = (
        IDENTITY,
        (0, 3, 2, 1),
        (2, 1, 0, 3),
        (2, 3, 0, 1),
    )
    if exact_group != expected_exact or rooted_group != (IDENTITY,):
        raise AssertionError(("H21 category groups", exact_group, rooted_group))
    # In this valid binary graph the explicit vertex roles already distinguish
    # reticulations after arrowheads are forgotten.  The corrected verifier
    # omits roles because they are derivable from exact arrowhead incidence;
    # forgetting both enlarges the port group and is therefore unsafe.
    if nohead_role_group != expected_exact:
        raise AssertionError(("H21 role-preserving no-arrowhead group",
                              nohead_role_group))
    if nohead_untyped_group != expected_nohead:
        raise AssertionError(("H21 untyped no-arrowhead group",
                              nohead_untyped_group))
    hsource_mixed = root_suppress(hsource)
    nontrivial_vertex_map = mixed_vertex_isomorphism(
        hsource_mixed, root_suppress(hsource.relabel(base_auto))
    )
    expected_vertex_map = {node: node for node in hsource_mixed.nodes}
    expected_vertex_map[("core", "S")] = ("sub", 4, 0)
    expected_vertex_map[("sub", 4, 0)] = ("core", "S")
    expected_vertex_map[("leaf", "INCOMING")] = ("leaf", "seg", 4, 0)
    expected_vertex_map[("leaf", "seg", 4, 0)] = ("leaf", "INCOMING")
    if nontrivial_vertex_map != expected_vertex_map:
        raise AssertionError(("H21 vertex automorphism", nontrivial_vertex_map))
    headed_edges = {
        (endpoints, heads)
        for endpoints, heads in hsource_mixed.edges.items() if heads
    }
    expected_headed_edges = {
        (frozenset((("core", "S"), ("core", "V"))),
         frozenset((("core", "V"),))),
        (frozenset((("sub", 4, 0), ("core", "V"))),
         frozenset((("core", "V"),))),
        (frozenset((("core", "U"), ("core", "X"))),
         frozenset((("core", "X"),))),
        (frozenset((("sub", 3, 0), ("core", "X"))),
         frozenset((("core", "X"),))),
    }
    if headed_edges != expected_headed_edges:
        raise AssertionError(("H21 headed edges", headed_edges))

    # Enumerate the entire H21 S4 quotient, not merely stored witnesses.
    remaining = set(S4)
    all_cosets = []
    while remaining:
        representative = min(remaining)
        orbit = double_coset(exact_group, representative, exact_group)
        all_cosets.append(orbit)
        remaining -= set(orbit)
    recorded_cosets = {
        tuple(sorted(tuple(member) for member in RECORDS[orbit_id]["raw_members"]))
        for orbit_id in RECORDS if orbit_id.startswith("H21-")
    }
    omitted = set(all_cosets) - recorded_cosets
    if len(all_cosets) != 7 or len(recorded_cosets) != 6:
        raise AssertionError("H21 double-coset count")
    if omitted != {tuple(sorted(exact_group))}:
        raise AssertionError(("wrong omitted H21 class", omitted))
    h21_01_raw = tuple(sorted(tuple(member) for member in hrecord["raw_members"]))
    if h21_01_raw != double_coset(
            exact_group, tuple(hrecord["representative_permutation"]), exact_group):
        raise AssertionError("H21-01 raw coverage")

    # Conjugation is tested on non-involutive representatives H21-03/04, where
    # the two possible formula orders differ.
    conjugation_checks = []
    for orbit_id in ("H21-03", "H21-04"):
        record = RECORDS[orbit_id]
        representative = tuple(record["representative_permutation"])
        direct_group = independent_records[orbit_id]["target_displayed_group"]
        correct = compose(representative,
                          compose(base_auto, inverse(representative)))
        wrong = compose(inverse(representative),
                        compose(base_auto, representative))
        if correct == wrong or correct not in direct_group or wrong in direct_group:
            raise AssertionError((orbit_id, "conjugation did not discriminate"))
        conjugation_checks.append({"orbit_id": orbit_id,
                                   "correct": correct, "wrong": wrong})

    # Independent exact numeric physical-edge Fourier evaluation for every
    # element of S4, plus comparison with all corrected symbolic transports.
    edge_values = {}
    for index, edge in enumerate(hbase.arcs):
        edge_values[edge] = tuple(
            Q(155 + ((7 * index + 3 * character) % 31), 211)
            for character in range(1, 4)
        )
    retic_count = sum(data["role"] == "retic" for data in hbase.nodes.values())
    lambdas = tuple(Q(index + 2, index + 7) for index in range(retic_count))
    physical_margins = []
    for c_value, g_value, t_value in edge_values.values():
        physical_margins.extend((
            c_value, g_value, t_value,
            1 - c_value, 1 - g_value, 1 - t_value,
            1 + c_value - g_value - t_value,
            1 - c_value + g_value - t_value,
            1 - c_value - g_value + t_value,
        ))
    for value in lambdas:
        physical_margins.extend((value, 1 - value))
    physical_margin = min(physical_margins)
    if physical_margin <= 0:
        raise AssertionError(("nonphysical Fourier audit point", physical_margin))
    q_base = exact_switching_evaluation(hbase, edge_values, lambdas)
    corrected_base = reconstructions["H21-01"]["target_base"]
    fourier_transport_hashes = {}
    for perm in S4:
        q_displayed = exact_switching_evaluation(
            hbase.relabel(perm), edge_values, lambdas
        )
        coordinate_map = independent_coordinate_transport(perm)
        if any(q_displayed[index] != q_base[coordinate_map[index]]
               for index in range(64)):
            raise AssertionError(("numeric Fourier transport", perm))
        corrected_map = verifier.verify_fourier_transport(
            corrected_base, corrected_base.relabel(perm), perm
        )
        if tuple(corrected_map) != coordinate_map:
            raise AssertionError(("symbolic Fourier transport", perm))
        fourier_transport_hashes["".join(map(str, perm))] = hashlib.sha256(
            json.dumps(coordinate_map, separators=(",", ":")).encode()
        ).hexdigest()

    # Exact certificate replay and coverage accounting.  The rank upper-bound
    # omission is tested separately below and deliberately not hidden here.
    verifier.verify_certificate_replay(reconstructions)
    certificate_files = {
        "h14": "k3p_h14_marginal_orbit_certificates.json",
        "remaining": "k3p_remaining_quartic_separators.json",
        "rank": "k3p_directed_rank_obstructions.json",
        "sink": "k3p_prelock_source5_quartic.json",
    }
    ids = {
        name: [entry.get("orbit_id") for entry in
               json.loads((ARTIFACTS / filename).read_text())["records"]]
        for name, filename in certificate_files.items()
    }
    if (len(ids["h14"]), len(ids["remaining"]), len(ids["rank"])) != (5, 4, 5):
        raise AssertionError(("certificate counts", ids))
    if set(ids["h14"]) & set(ids["remaining"]) or \
            set(ids["h14"]) & set(ids["rank"]) or \
            set(ids["remaining"]) & set(ids["rank"]):
        raise AssertionError("certificate categories overlap")
    if set(ids["h14"] + ids["remaining"] + ids["rank"]) != set(RECORDS):
        raise AssertionError("fourteen-orbit certificate coverage")
    sink_certificates = json.loads(
        (ARTIFACTS / certificate_files["sink"]).read_text()
    )["records"]
    if not (len(sink_certificates) ==
            len(LOCK["prelock_exact_separations"]) == 2):
        raise AssertionError("sink-swap count")
    sink_permutations = []
    for certificate, lock_record in zip(
            sink_certificates, LOCK["prelock_exact_separations"]):
        if certificate["permutation"] != lock_record["permutation"]:
            raise AssertionError("sink-swap ordering/binding")
        source = LiteralGraph.from_json(lock_record["source_literal_graph"])
        target = LiteralGraph.from_json(lock_record["target_literal_graph"])
        if mixed_isomorphic(root_suppress(source), root_suppress(target)):
            raise AssertionError("sink-swap graph unexpectedly isomorphic")
        sink_permutations.append(tuple(certificate["permutation"]))
    if len(set(sink_permutations)) != 2:
        raise AssertionError("duplicate sink-swap presentations")

    mutations = []
    base_record = RECORDS["H21-01"]

    bad = copy.deepcopy(base_record)
    bad["raw_members"] = bad["raw_members"][:-1]
    bad["raw_member_transports"] = bad["raw_member_transports"][:-1]
    expect_assertion("omit_one_H21_01_raw_member",
                     lambda: verifier.reconstruct_record(bad), mutations)

    bad = copy.deepcopy(base_record)
    bad["raw_member_transports"][1]["source_automorphism"] = [0, 3, 2, 1]
    expect_assertion("use_arrowhead_violating_source_symmetry",
                     lambda: verifier.reconstruct_record(bad), mutations)

    bad = copy.deepcopy(base_record)
    bad["raw_member_transports"][2]["target_automorphism"] = [3, 1, 2, 0]
    expect_assertion("use_displayed_target_auto_in_base_frame",
                     lambda: verifier.reconstruct_record(bad), mutations)

    bad = copy.deepcopy(base_record)
    bad["representative_permutation"] = [0, 1, 2, 3]
    expect_assertion("wrong_representative_permutation",
                     lambda: verifier.reconstruct_record(bad), mutations)

    bad = copy.deepcopy(base_record)
    bad["raw_member_transports"][0]["permutation"] = [0, 1, 2, 3]
    expect_assertion("wrong_raw_witness_equation",
                     lambda: verifier.reconstruct_record(bad), mutations)

    original_coordinate_transport = verifier.coordinate_transport
    verifier.coordinate_transport = lambda perm: tuple(range(64))
    try:
        reconstruction = reconstructions["H21-01"]
        expect_assertion(
            "identity_coordinate_map_for_nonidentity_relabelling",
            lambda: verifier.verify_fourier_transport(
                reconstruction["target_base"],
                reconstruction["target_displayed"],
                tuple(base_record["representative_permutation"]),
            ),
            mutations,
        )
    finally:
        verifier.coordinate_transport = original_coordinate_transport

    # Replacing base-target by displayed-target coordinates in the H21-01
    # double coset misses exactly half the recorded raw members.
    representative = tuple(base_record["representative_permutation"])
    wrong_frame_orbit = double_coset(
        exact_group, representative,
        independent_records["H21-01"]["target_displayed_group"],
    )
    if wrong_frame_orbit == h21_01_raw or len(wrong_frame_orbit) != 2:
        raise AssertionError(("wrong-frame mutation not exposed", wrong_frame_orbit))
    mutations.append({
        "name": "displayed_target_group_used_in_double_coset",
        "status": "COUNTEREXAMPLE_EXPOSED",
        "claimed_raw_count": len(h21_01_raw),
        "wrong_frame_count": len(wrong_frame_orbit),
    })

    # The next two redundant lock fields are currently not bound by the
    # corrected verifier.  Record the acceptance transparently.
    bad = copy.deepcopy(base_record)
    bad["port_permutation"] = [0, 1, 2, 3]
    verifier.reconstruct_record(bad)
    mutations.append({"name": "inconsistent_redundant_port_permutation_field",
                      "status": "ACCEPTED_METADATA_MUTATION"})
    bad = copy.deepcopy(base_record)
    bad["target_incoming_role"] = "selected-port-3"
    verifier.reconstruct_record(bad)
    mutations.append({"name": "inconsistent_target_incoming_role_field",
                      "status": "ACCEPTED_METADATA_MUTATION"})

    # Demonstrate that the rank replay trusts rank labels/upper bounds and does
    # not bind them to minor sizes or independently replay factorization.
    rank_path = ARTIFACTS / certificate_files["rank"]
    rank_text = rank_path.read_text()
    mutated_rank = json.loads(rank_text)
    rank_entry = mutated_rank["records"][0]
    rank_entry["source_rank_certificate"]["rank"] = 101
    rank_entry["target_dimension_upper_bound"] = 100
    rank_entry["target_rank_certificate"]["rank"] = 100
    real_loads = verifier.json.loads

    def mutated_loads(payload, *args, **kwargs):
        if payload == rank_text:
            return copy.deepcopy(mutated_rank)
        return real_loads(payload, *args, **kwargs)

    verifier.json.loads = mutated_loads
    try:
        verifier.verify_certificate_replay(reconstructions)
    finally:
        verifier.json.loads = real_loads
    mutations.append({
        "name": "rank_labels_101_over_100_with_11x11_and_10x10_minors",
        "status": "ACCEPTED_CERTIFICATE_MUTATION",
        "source_minor_size": len(rank_entry["source_rank_certificate"]["output_rows"]),
        "claimed_source_rank": 101,
        "target_minor_size": len(rank_entry["target_rank_certificate"]["output_rows"]),
        "claimed_target_rank_and_upper_bound": 100,
    })

    optimized = subprocess.run(
        [sys.executable, "-O", str(HERE / "optimized_bypass_probe.py")],
        cwd=PROJECT,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
        check=True,
    )
    if "OPTIMIZED_ASSERT_BYPASS_CONFIRMED" not in optimized.stdout:
        raise AssertionError(("optimized bypass probe", optimized.stdout,
                              optimized.stderr))
    mutations.append({"name": "python_optimized_mode_assert_stripping",
                      "status": "INVALID_RAW_ORBIT_ACCEPTED",
                      "sentinel": optimized.stdout.strip()})

    # Current immutable-input hashes must match the narrative audit exactly.
    prior_audit = json.loads((CLEAN_ROOM / "H21_01_TRANSPORT_AUDIT.json").read_text())
    for filename, expected in prior_audit["immutable_inputs"].items():
        actual = digest(ARTIFACTS / filename)
        if actual != expected:
            raise AssertionError(("prior audit input hash mismatch", filename,
                                  expected, actual))

    result = {
        "status": "MATHEMATICAL_TRANSPORT_PASS_WITH_CERTIFICATION_GAPS",
        "hashes": hashes,
        "independent_engine": f"networkx {nx.__version__} incidence encoding",
        "rooted_H21_group": rooted_group,
        "mixed_H21_group": exact_group,
        "role_preserving_no_arrowhead_H21_group": nohead_role_group,
        "untyped_no_arrowhead_H21_group": nohead_untyped_group,
        "H21_double_cosets": len(all_cosets),
        "H21_nonisomorphic_cosets": len(recorded_cosets),
        "H21_01_raw_members": h21_01_raw,
        "conjugation_checks": conjugation_checks,
        "all_S4_Fourier_transports": len(fourier_transport_hashes),
        "Fourier_audit_point_physical_margin": str(physical_margin),
        "fourteen_orbit_records": len(RECORDS),
        "raw_members": sum(len(record["raw_members"])
                           for record in RECORDS.values()),
        "polynomial_certificates": len(ids["h14"]) + len(ids["remaining"]),
        "rank_certificates": len(ids["rank"]),
        "sink_swap_certificates": len(sink_certificates),
        "mutations": mutations,
    }
    print(json.dumps(result, indent=2, default=list))
    print("ADVERSARIAL_H21_AUDIT_EXECUTED")
    return result


if __name__ == "__main__":
    run()
