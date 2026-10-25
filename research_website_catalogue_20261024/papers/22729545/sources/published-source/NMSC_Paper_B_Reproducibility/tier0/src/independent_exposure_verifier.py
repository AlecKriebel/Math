#!/usr/bin/env python3
"""Independent exact verifier for the four exposure-loss repairs.

This executable deliberately does not import the Paper B implementation or the
handoff graph enumerator.  It starts from a small raw-arc manifest, derives the
minimum repairs from graph predicates, generates only total observable laws and
labelled typing cells, inverts those laws, and reconstructs the decorated graph
from the residual carrier plus the two recovered/stored records.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import networkx as nx
import sympy as sp

from record_schema import make_record, write_jsonl


MANIFEST_SCHEMA = "nmsc-independent-exposure-loss-manifest-v1"
JOB = "independent_exposure_loss"


def rational(value: object) -> sp.Expr:
    result = sp.Rational(str(value))
    if result.is_rational is not True:
        raise ValueError(f"manifest value is not rational: {value!r}")
    return result


def load_manifest(path: Path) -> dict:
    payload = json.loads(path.read_text())
    if payload.get("schema") != MANIFEST_SCHEMA:
        raise ValueError("unexpected independent exposure manifest schema")
    if set(payload.get("primitive_cores", {})) != {"branch", "parallel"}:
        raise ValueError("manifest must contain exactly the two exposure-loss cores")
    cases = payload.get("cases", [])
    if len(cases) != 4 or len({row.get("case_id") for row in cases}) != 4:
        raise ValueError("manifest must contain four uniquely named repair cases")
    return payload


def _core_graph(specification: Mapping) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    reticulations = set(specification["reticulations"])
    arcs = tuple(tuple(arc) for arc in specification["arcs"])
    nodes = {node for arc in arcs for node in arc}
    for node in sorted(nodes):
        graph.add_node(node, role="retic" if node in reticulations else "tree")
    for segment, (tail, head) in enumerate(arcs):
        graph.add_edge(
            tail,
            head,
            key=f"s{segment}",
            segment=segment,
            edge_role="primitive",
        )
    sources = [node for node in graph if graph.in_degree(node) == 0]
    if sources != ["S"]:
        raise ValueError(f"primitive core has unexpected sources: {sources!r}")
    graph.nodes["S"]["role"] = "source"
    return graph


def _ported_graph(
    specification: Mapping,
    repair_segments: Sequence[int],
) -> nx.MultiDiGraph:
    repair = set(map(int, repair_segments))
    arcs = tuple(tuple(arc) for arc in specification["arcs"])
    if not repair.issubset(range(len(arcs))):
        raise ValueError("repair names a nonexistent primitive segment")
    graph = nx.MultiDiGraph()
    reticulations = set(specification["reticulations"])
    nodes = {node for arc in arcs for node in arc}
    for node in sorted(nodes):
        role = "source" if node == "S" else "retic" if node in reticulations else "tree"
        graph.add_node(node, role=role)
    for segment, (tail, head) in enumerate(arcs):
        if segment not in repair:
            graph.add_edge(
                tail,
                head,
                key=f"s{segment}",
                segment=segment,
                edge_role="primitive",
            )
            continue
        port, sample = f"p{segment}", f"L{segment}"
        graph.add_node(port, role="tree")
        graph.add_node(sample, role="sample")
        graph.add_edge(
            tail,
            port,
            key=f"s{segment}:a",
            segment=segment,
            edge_role="ported-upper",
        )
        graph.add_edge(
            port,
            head,
            key=f"s{segment}:b",
            segment=segment,
            edge_role="ported-lower",
        )
        graph.add_edge(
            port,
            sample,
            key=f"s{segment}:sample",
            segment=f"port-{segment}",
            edge_role="sample-incidence",
        )
    for sink in specification["sinks"]:
        sample = f"C_{sink}"
        graph.add_node(sample, role="sample")
        graph.add_edge(
            sink,
            sample,
            key=f"child:{sink}",
            segment="sink-child",
            edge_role="compulsory-child",
        )
    return graph


def _tree_child(graph: nx.MultiDiGraph) -> bool:
    if not nx.is_directed_acyclic_graph(graph):
        return False
    for node, data in graph.nodes(data=True):
        role = data.get("role")
        indegree, outdegree = graph.in_degree(node), graph.out_degree(node)
        if role == "sample":
            if (indegree, outdegree) != (1, 0):
                return False
            continue
        expected = {
            "source": (0, 2),
            "tree": (1, 2),
            "retic": (2, 1),
        }.get(role)
        if expected is None or (indegree, outdegree) != expected:
            return False
        children = [head for _, head, _ in graph.out_edges(node, keys=True)]
        if not any(graph.nodes[child].get("role") != "retic" for child in children):
            return False
    return True


def _strong_tail(graph: nx.MultiDiGraph) -> bool:
    """Evaluate the local tail-incidence predicate directly on the ported graph."""
    for reticulation, data in graph.nodes(data=True):
        if data.get("role") != "retic":
            continue
        for tail in set(graph.predecessors(reticulation)):
            ordinary_incidence_count = graph.in_degree(tail)
            ordinary_incidence_count += sum(
                graph.nodes[head].get("role") != "retic"
                for _, head, _ in graph.out_edges(tail, keys=True)
            )
            if graph.nodes[tail].get("role") == "source":
                ordinary_incidence_count += 1
            if ordinary_incidence_count < 2:
                return False
    return True


def _minimal_repairs(specification: Mapping) -> tuple[tuple[int, ...], ...]:
    segment_count = len(specification["arcs"])
    valid = []
    for size in range(segment_count + 1):
        for repair in combinations(range(segment_count), size):
            graph = _ported_graph(specification, repair)
            if _tree_child(graph) and _strong_tail(graph):
                valid.append(repair)
    return tuple(
        repair
        for repair in valid
        if not any(set(other) < set(repair) for other in valid)
    )


def _canonical_role_code(graph: nx.MultiDiGraph) -> str:
    """Independent brute-force role-preserving multidigraph canonical form."""
    blocks: dict[str, list[str]] = {}
    for node, data in graph.nodes(data=True):
        blocks.setdefault(str(data.get("role")), []).append(str(node))
    role_names = sorted(blocks)
    block_orders = [tuple(permutations(sorted(blocks[role]))) for role in role_names]
    best = None
    for chosen in product(*block_orders):
        order = tuple(node for block in chosen for node in block)
        candidate = (
            tuple(str(graph.nodes[node].get("role")) for node in order),
            tuple(
                graph.number_of_edges(tail, head)
                for tail in order
                for head in order
            ),
        )
        if best is None or candidate < best:
            best = candidate
    if best is None:
        raise ValueError("empty graph has no canonical role code")
    return json.dumps(best, separators=(",", ":"))


def _edge_tuple(tail: str, head: str, key: str, data: Mapping) -> tuple:
    return (str(tail), str(head), str(key), data["segment"], data["edge_role"])


def _incoming(graph: nx.MultiDiGraph, node: str) -> tuple[tuple, ...]:
    return tuple(sorted(
        (_edge_tuple(tail, head, key, data) for tail, head, key, data in graph.in_edges(node, keys=True, data=True)),
        key=repr,
    ))


def _outgoing(graph: nx.MultiDiGraph, node: str) -> tuple[tuple, ...]:
    return tuple(sorted(
        (_edge_tuple(tail, head, key, data) for tail, head, key, data in graph.out_edges(node, keys=True, data=True)),
        key=repr,
    ))


def _sample_descendants(graph: nx.MultiDiGraph, node: str) -> tuple[str, ...]:
    descendants = set(nx.descendants(graph, node)).union({node})
    return tuple(sorted(
        sample
        for sample in descendants
        if graph.nodes[sample].get("role") == "sample"
    ))


def _topology_record(graph: nx.MultiDiGraph, case: Mapping) -> dict:
    child_segment = int(case["child_segment"])
    typing_segment = int(case["typing_segment"])
    parent_incidences = _incoming(graph, "V")
    child_incidence = _outgoing(graph, "V")
    x_incoming = _incoming(graph, "X")
    x_outgoing = _outgoing(graph, "X")
    if len(parent_incidences) != 2 or len(child_incidence) != 1:
        raise ValueError("V does not have binary exposed incidence")
    if len(x_incoming) != 2 or len(x_outgoing) != 1:
        raise ValueError("X does not have binary hidden incidence")
    child_samples = _sample_descendants(graph, "V")
    expected_child_samples = tuple(sorted(("C_X", f"L{child_segment}")))
    if child_samples != expected_child_samples:
        raise ValueError(
            f"V two-block support is {child_samples!r}, expected {expected_child_samples!r}"
        )
    if _sample_descendants(graph, "X") != ("C_X",):
        raise ValueError("X is not a unary sampled fan before first exposure")
    typing_port = f"p{typing_segment}"
    if graph.has_edge(typing_port, "X"):
        typing_kind = "bypass-sibling-at-upper-tail"
    elif graph.has_edge(typing_port, "V"):
        primitive_v_parents = tuple(sorted(set(graph.predecessors("V"))))
        typing_kind = (
            "nested-parent-arm"
            if "S" in primitive_v_parents
            else f"parallel-parent-arm-segment-{typing_segment}"
        )
    else:
        raise ValueError("typing repair is not incident to a routed parent arm")
    child_corridor = next(
        row for row in x_incoming if nx.has_path(graph, "V", row[0])
    )
    bypass = next(row for row in x_incoming if row != child_corridor)
    return {
        "parent_incidences": parent_incidences,
        "child_incidence": child_incidence,
        "child_component": child_samples,
        "x_incoming": x_incoming,
        "x_outgoing": x_outgoing,
        "x_child_corridor": child_corridor,
        "x_bypass": bypass,
        "typing_kind": typing_kind,
        "label_triple": ("C_X", f"L{child_segment}", f"L{typing_segment}"),
    }


def _fixture(manifest: Mapping) -> dict:
    raw = manifest["exact_fixture"]
    return {
        "entry_time": rational(raw["entry_time"]),
        "p_x": rational(raw["x_child_corridor_weight"]),
        "child_chambers": tuple(
            (rational(row["duration"]), rational(row["rate"]))
            for row in raw["child_chambers"]
        ),
        "parent_chambers": tuple({
            "duration": rational(row["duration"]),
            "rates": tuple(rational(rate) for rate in row["rates"]),
            "changed_parent": row["changed_parent"],
        } for row in raw["parent_chambers"]),
        "equal_parent_rate": rational(raw["equal_parent_rate"]),
        "equal_parent_q_values": tuple(rational(q) for q in raw["equal_parent_q_values"]),
        "equal_child_rate": rational(raw["equal_child_rate"]),
        "direction_rate": rational(raw["direction_rate"]),
        "direction_duration": rational(raw["direction_duration"]),
    }


def _observation(
    topology: Mapping,
    fixture: Mapping,
    physical_q: Sequence[sp.Expr],
) -> dict:
    """Generate total laws; marked anchor cells are stored separately."""
    u = sp.Symbol("u", nonnegative=True)
    p_x = fixture["p_x"]
    q_0, q_1 = map(sp.sympify, physical_q)
    if any(value.is_positive is not True for value in (p_x, 1 - p_x, q_0, q_1)):
        raise ValueError("strict positive-domain fixture violated")
    if sp.simplify(q_0 + q_1 - 1) != 0:
        raise ValueError("physical inheritance weights do not sum to one")
    current_time = fixture["entry_time"]
    child_prefix = sp.Integer(0)
    below = []
    for duration, rate in fixture["child_chambers"]:
        atom = sp.exp(-(child_prefix + rate * u))
        below.append({
            "start": current_time,
            "end": sp.simplify(current_time + duration),
            "total_survival": sp.simplify(1 - p_x + p_x * atom),
            "first_merger_density": sp.simplify(p_x * rate * atom),
        })
        current_time = sp.simplify(current_time + duration)
        child_prefix = sp.simplify(child_prefix + duration * rate)
    p_tilde = sp.simplify(p_x * sp.exp(-child_prefix))
    parent_prefix = [sp.Integer(0), sp.Integer(0)]
    parent_ids = tuple(row[0] + "|" + row[2] for row in topology["parent_incidences"])
    above = []
    for chamber in fixture["parent_chambers"]:
        components = tuple(
            sp.simplify(
                p_tilde * physical_q[index] ** 2
                * sp.exp(-(parent_prefix[index] + chamber["rates"][index] * u))
            )
            for index in range(2)
        )
        constant = sp.simplify(1 - p_x + 2 * p_tilde * q_0 * q_1)
        above.append({
            "start": current_time,
            "end": sp.simplify(current_time + chamber["duration"]),
            "total_survival": sp.simplify(constant + sum(components)),
            "anchor_cells": dict(zip(parent_ids, components)),
            "changed_parent": chamber["changed_parent"],
        })
        current_time = sp.simplify(current_time + chamber["duration"])
        for index in range(2):
            parent_prefix[index] = sp.simplify(
                parent_prefix[index]
                + chamber["duration"] * chamber["rates"][index]
            )
    equal_parent = []
    for q in fixture["equal_parent_q_values"]:
        rate = fixture["equal_parent_rate"]
        equal_parent.append({
            "q": q,
            "total_survival": sp.simplify(
                1 - p_x
                + 2 * p_tilde * q * (1 - q)
                + p_tilde * (q**2 + (1 - q) ** 2) * sp.exp(-rate * u)
            ),
        })
    direction_forward = sp.simplify(
        q_0 * sp.exp(-fixture["direction_rate"] * u)
        + q_1 * sp.exp(
            -fixture["direction_rate"] * (u + fixture["direction_duration"])
        )
    )
    direction_reversed = sp.simplify(
        q_1 * sp.exp(-fixture["direction_rate"] * u)
        + q_0 * sp.exp(
            -fixture["direction_rate"] * (u + fixture["direction_duration"])
        )
    )
    return {
        "u": u,
        "p_x": p_x,
        "p_tilde": p_tilde,
        "below": tuple(below),
        "above": tuple(above),
        "equal_parent": tuple(equal_parent),
        "direction_forward": direction_forward,
        "direction_reversed": direction_reversed,
    }


def _prony_total(total: sp.Expr, scale: sp.Expr, u: sp.Symbol) -> dict:
    constant = sp.simplify(sp.limit(total, u, sp.oo))
    germ = sp.simplify(total - constant)
    moments = tuple(
        sp.simplify((-1) ** order * sp.diff(germ, u, order).subs(u, 0) / scale)
        for order in range(4)
    )
    m0, m1, m2, m3 = moments
    determinant = sp.simplify(m0 * m2 - m1**2)
    if determinant == 0:
        rate = sp.simplify(m1 / m0)
        components = ((rate, m0),)
        branch = "equal-rate"
        recurrence = None
    else:
        sum_rates = sp.simplify((m0 * m3 - m1 * m2) / determinant)
        product_rates = sp.simplify((m1 * m3 - m2**2) / determinant)
        z = sp.Symbol("z")
        rates = tuple(sorted(
            sp.solve(sp.Eq(z**2 - sum_rates * z + product_rates, 0), z),
            key=sp.default_sort_key,
        ))
        if len(rates) != 2 or rates[0] == rates[1]:
            raise ValueError("two-atom Prony polynomial failed to separate rates")
        left, right = rates
        weights = (
            sp.simplify((right * m0 - m1) / (right - left)),
            sp.simplify((m1 - left * m0) / (right - left)),
        )
        components = tuple(zip(rates, weights))
        branch = "unequal-rate"
        recurrence = (sum_rates, product_rates)
    if any(rate.is_positive is not True or weight.is_positive is not True for rate, weight in components):
        raise ValueError("Prony inverse left the strict positive domain")
    rebuilt = sp.simplify(
        constant + scale * sum(
            weight * sp.exp(-rate * u) for rate, weight in components
        )
    )
    if sp.simplify(rebuilt - total) != 0:
        raise ValueError("Prony components do not rebuild the total observable law")
    return {
        "branch": branch,
        "constant": constant,
        "moments": moments,
        "determinant": determinant,
        "recurrence": recurrence,
        "components": components,
        "rebuilt": rebuilt,
    }


def _q_pair_from_sum_squares(sum_squares: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    root = sp.sqrt(sp.simplify(2 * sum_squares - 1))
    pair = tuple(sorted(
        (sp.simplify((1 - root) / 2), sp.simplify((1 + root) / 2)),
        key=sp.default_sort_key,
    ))
    if any(value.is_positive is not True for value in pair):
        raise ValueError("sum-of-squares inverse left the strict inheritance domain")
    if sp.simplify(sum(value**2 for value in pair) - sum_squares) != 0:
        raise ValueError("sum-of-squares inverse does not replay")
    return pair


def _typed_components(
    inverse: Mapping,
    anchors: Mapping[str, sp.Expr],
    scale: sp.Expr,
    u: sp.Symbol,
    q_pair: Sequence[sp.Expr] | None = None,
) -> dict[str, tuple[sp.Expr, sp.Expr]]:
    """Use marked cells only to type already recovered total-law atoms."""
    typed = {}
    for parent, cell in anchors.items():
        observed_rate = sp.simplify(-sp.diff(cell, u) / cell)
        observed_weight = sp.simplify(cell.subs(u, 0) / scale)
        if inverse["branch"] == "unequal-rate":
            matches = tuple(
                (recovered_rate, recovered_weight)
                for recovered_rate, recovered_weight in inverse["components"]
                if recovered_rate == observed_rate
                and sp.simplify(recovered_weight - observed_weight) == 0
            )
            if len(matches) != 1:
                raise ValueError("anchor does not type a recovered total-law atom")
            typed[parent] = matches[0]
        else:
            recovered_rate, recovered_weight = inverse["components"][0]
            if observed_rate != recovered_rate or q_pair is None:
                raise ValueError("equal-rate anchor does not type the recovered rate")
            candidate_weights = tuple(sp.simplify(q**2) for q in q_pair)
            matches = tuple(
                weight for weight in candidate_weights
                if sp.simplify(weight - observed_weight) == 0
            )
            if not matches:
                raise ValueError("equal-rate anchor does not type a recovered q branch")
            if sp.simplify(sum(
                sp.simplify(anchor.subs(u, 0) / scale) for anchor in anchors.values()
            ) - recovered_weight) != 0:
                raise ValueError("typed equal-rate cells do not partition the recovered atom")
            typed[parent] = (recovered_rate, matches[0])
    return typed


def _compress_word(durations: Sequence[sp.Expr], rates: Sequence[sp.Expr]) -> tuple:
    result: list[tuple[sp.Expr, sp.Expr]] = []
    for duration, rate in zip(durations, rates):
        if result and result[-1][1] == rate:
            result[-1] = (sp.simplify(result[-1][0] + duration), rate)
        else:
            result.append((duration, rate))
    return tuple(result)


def _recover_record(
    observation: Mapping,
    topology: Mapping,
) -> dict:
    u = observation["u"]
    below_constants = tuple(
        sp.simplify(sp.limit(row["total_survival"], u, sp.oo))
        for row in observation["below"]
    )
    if len(set(below_constants)) != 1:
        raise ValueError("below-breakpoint zero atom changes across a child chamber")
    bypass = below_constants[0]
    p_x = sp.simplify(1 - bypass)
    child_rates = []
    child_durations = []
    for row in observation["below"]:
        atom = sp.simplify(row["total_survival"] - bypass)
        rate = sp.simplify(-sp.diff(atom, u) / atom)
        if sp.simplify(row["first_merger_density"] - rate * atom) != 0:
            raise ValueError("first-merger density does not identify the child atom")
        child_rates.append(rate)
        child_durations.append(sp.simplify(row["end"] - row["start"]))
    h_v = observation["above"][0]["start"]
    if h_v != observation["below"][-1]["end"]:
        raise ValueError("observable chamber boundary does not define one V time")
    child_hazard = sp.simplify(sum(
        duration * rate for duration, rate in zip(child_durations, child_rates)
    ))
    p_tilde = sp.simplify(p_x * sp.exp(-child_hazard))
    inversions = tuple(
        _prony_total(row["total_survival"], p_tilde, u)
        for row in observation["above"]
    )
    first = inversions[0]
    if first["branch"] == "equal-rate":
        q_pair = _q_pair_from_sum_squares(first["moments"][0])
    else:
        q_pair = tuple(sorted(
            (sp.sqrt(weight) for _, weight in first["components"]),
            key=sp.default_sort_key,
        ))
        if sp.simplify(sum(q_pair) - 1) != 0:
            raise ValueError("unequal-rate total law does not recover a Bernoulli pair")
    typed_by_chamber = tuple(
        _typed_components(
            inversion,
            row["anchor_cells"],
            p_tilde,
            u,
            q_pair if inversion["branch"] == "equal-rate" else None,
        )
        for inversion, row in zip(inversions, observation["above"])
    )
    parent_ids = tuple(row[0] + "|" + row[2] for row in topology["parent_incidences"])
    physical_q = {}
    for parent in parent_ids:
        first_rate, first_weight = typed_by_chamber[0][parent]
        candidate = sp.sqrt(first_weight)
        if candidate not in q_pair:
            raise ValueError("typed first chamber does not select a recovered q value")
        physical_q[parent] = candidate
    if tuple(sorted(physical_q.values(), key=sp.default_sort_key)) != q_pair:
        raise ValueError("physical typing does not use the entire recovered q pair")
    parent_rates = {
        parent: tuple(chamber[parent][0] for chamber in typed_by_chamber)
        for parent in parent_ids
    }
    changes = tuple(
        sum(parent_rates[parent][index] != parent_rates[parent][index - 1] for parent in parent_ids)
        for index in range(1, len(observation["above"]))
    )
    parent_durations = tuple(
        sp.simplify(row["end"] - row["start"]) for row in observation["above"]
    )
    above_constant = first["constant"]
    zero_atom_jump = sp.simplify(above_constant - bypass)
    return {
        "h_v": h_v,
        "p_x": p_x,
        "p_tilde": p_tilde,
        "inheritance_pair": q_pair,
        "typed_inheritance": tuple((parent, physical_q[parent]) for parent in parent_ids),
        "child_chamber_rates": tuple(child_rates),
        "parent_chamber_rates": parent_rates,
        "rate_words": {
            "child": _compress_word(child_durations, child_rates),
            "parent_0": _compress_word(parent_durations, parent_rates[parent_ids[0]]),
            "parent_1": _compress_word(parent_durations, parent_rates[parent_ids[1]]),
        },
        "parent_incidences": topology["parent_incidences"],
        "child_incidence": topology["child_incidence"],
        "child_component": topology["child_component"],
        "typing_kind": topology["typing_kind"],
        "label_triple": topology["label_triple"],
        "direction_quotient": "forward-mod-parent-exchange",
        "zero_atom": {
            "below": bypass,
            "above": above_constant,
            "jump": zero_atom_jump,
        },
        "asynchronous_changes": changes,
        "prony": inversions,
    }


def _validate_record(record: Mapping) -> bool:
    pair = tuple(record["inheritance_pair"])
    typed = tuple(record["typed_inheritance"])
    return (
        record["h_v"].is_positive is True
        and len(pair) == 2
        and all(q.is_positive is True for q in pair)
        and sp.simplify(sum(pair) - 1) == 0
        and len(typed) == 2
        and len({parent for parent, _ in typed}) == 2
        and tuple(sorted((q for _, q in typed), key=sp.default_sort_key)) == pair
        and record["zero_atom"]["jump"].is_positive is True
        and record["asynchronous_changes"] == (1, 1)
        and all(record["rate_words"].values())
        and len(record["child_component"]) == 2
        and len(record["label_triple"]) == 3
    )


def _stored_x_macro(topology: Mapping, p_x: sp.Expr) -> dict:
    child_parent_id = topology["x_child_corridor"][0] + "|" + topology["x_child_corridor"][2]
    bypass_parent_id = topology["x_bypass"][0] + "|" + topology["x_bypass"][2]
    return {
        "focal": "C_X",
        "incoming": topology["x_incoming"],
        "outgoing": topology["x_outgoing"],
        "child_corridor_parent": child_parent_id,
        "bypass_parent": bypass_parent_id,
        "typed_weights": (
            (child_parent_id, p_x),
            (bypass_parent_id, sp.simplify(1 - p_x)),
        ),
    }


def _residual_q8(graph: nx.MultiDiGraph, topology: Mapping) -> tuple[nx.MultiDiGraph, dict]:
    restricted = graph.copy()
    restricted.remove_node("C_X")
    restricted.remove_node("X")
    remaining_samples = _sample_descendants(restricted, "V")
    if len(remaining_samples) != 1:
        raise ValueError("restriction does not turn V into a unary Q8 fan")
    residual = restricted.copy()
    residual.remove_node("V")
    residual.add_node("Q8:V", role="macro", macro_kind="unary-routing-response")
    for index, incidence in enumerate(topology["parent_incidences"]):
        residual.add_edge(
            incidence[0], "Q8:V", key=f"q8-in:{index}",
            segment="macro", edge_role="q8-incoming",
        )
    for index, incidence in enumerate(topology["child_incidence"]):
        residual.add_edge(
            "Q8:V", incidence[1], key=f"q8-out:{index}",
            segment="macro", edge_role="q8-outgoing",
        )
    return residual, {
        "remaining_sample": remaining_samples[0],
        "macro_parent_count": residual.in_degree("Q8:V"),
        "macro_child_count": residual.out_degree("Q8:V"),
    }


def _decorate_expected(
    graph: nx.MultiDiGraph,
    fixture: Mapping,
    topology: Mapping,
    physical_q: Sequence[sp.Expr],
) -> nx.MultiDiGraph:
    """Build the expected decorated graph from manifest data, not the inverse."""
    expected = graph.copy()
    child_durations = tuple(duration for duration, _ in fixture["child_chambers"])
    child_rates = tuple(rate for _, rate in fixture["child_chambers"])
    parent_durations = tuple(row["duration"] for row in fixture["parent_chambers"])
    parent_0_rates = tuple(row["rates"][0] for row in fixture["parent_chambers"])
    parent_1_rates = tuple(row["rates"][1] for row in fixture["parent_chambers"])
    h_v = sp.simplify(fixture["entry_time"] + sum(child_durations))
    rate_words = {
        "child": _compress_word(child_durations, child_rates),
        "parent_0": _compress_word(parent_durations, parent_0_rates),
        "parent_1": _compress_word(parent_durations, parent_1_rates),
    }
    expected.nodes["V"].update(
        h_v=h_v,
        inheritance_pair=tuple(sorted(physical_q, key=sp.default_sort_key)),
        rate_words=rate_words,
        direction_quotient="forward-mod-parent-exchange",
        typing_kind=topology["typing_kind"],
        label_triple=topology["label_triple"],
        child_component=topology["child_component"],
    )
    expected.nodes["X"].update(p_x=fixture["p_x"], typed_macro=True)
    for incidence, q in zip(topology["parent_incidences"], physical_q):
        expected[incidence[0]][incidence[1]][incidence[2]]["inheritance_probability"] = q
    for incidence in topology["x_incoming"]:
        weight = (
            fixture["p_x"]
            if incidence == topology["x_child_corridor"]
            else sp.simplify(1 - fixture["p_x"])
        )
        expected[incidence[0]][incidence[1]][incidence[2]]["inheritance_probability"] = weight
    return expected


def _restore(
    residual: nx.MultiDiGraph,
    record: Mapping,
    stored_x: Mapping,
) -> nx.MultiDiGraph:
    if not _validate_record(record):
        raise ValueError("recovered V record is incomplete")
    graph = residual.copy()
    graph.remove_node("Q8:V")
    graph.add_node(
        "V",
        role="retic",
        h_v=record["h_v"],
        inheritance_pair=record["inheritance_pair"],
        rate_words=record["rate_words"],
        direction_quotient=record["direction_quotient"],
        typing_kind=record["typing_kind"],
        label_triple=record["label_triple"],
        child_component=record["child_component"],
    )
    typed_q = dict(record["typed_inheritance"])
    for incidence in record["parent_incidences"]:
        parent_id = incidence[0] + "|" + incidence[2]
        graph.add_edge(
            incidence[0], incidence[1], key=incidence[2],
            segment=incidence[3], edge_role=incidence[4],
            inheritance_probability=typed_q[parent_id],
        )
    for incidence in record["child_incidence"]:
        graph.add_edge(
            incidence[0], incidence[1], key=incidence[2],
            segment=incidence[3], edge_role=incidence[4],
        )
    if stored_x["focal"] != "C_X" or len(stored_x["outgoing"]) != 1:
        raise ValueError("stored X macro has a malformed focal child")
    x_weights = dict(stored_x["typed_weights"])
    if set(x_weights) != {stored_x["child_corridor_parent"], stored_x["bypass_parent"]}:
        raise ValueError("stored X macro does not type its two parent routes")
    graph.add_node("X", role="retic", p_x=x_weights[stored_x["child_corridor_parent"]], typed_macro=True)
    graph.add_node("C_X", role="sample")
    for incidence in stored_x["incoming"]:
        parent_id = incidence[0] + "|" + incidence[2]
        graph.add_edge(
            incidence[0], incidence[1], key=incidence[2],
            segment=incidence[3], edge_role=incidence[4],
            inheritance_probability=x_weights[parent_id],
        )
    for incidence in stored_x["outgoing"]:
        graph.add_edge(
            incidence[0], incidence[1], key=incidence[2],
            segment=incidence[3], edge_role=incidence[4],
        )
    return graph


def _frozen_graph_fingerprint(graph: nx.MultiDiGraph) -> tuple:
    nodes = tuple(sorted(
        (str(node), tuple(sorted((str(key), repr(value)) for key, value in data.items())))
        for node, data in graph.nodes(data=True)
    ))
    edges = tuple(sorted(
        (
            str(tail), str(head), str(key),
            tuple(sorted((str(name), repr(value)) for name, value in data.items())),
        )
        for tail, head, key, data in graph.edges(keys=True, data=True)
    ))
    return nodes, edges


def _bundle_matches(
    residual: nx.MultiDiGraph,
    record: Mapping,
    stored_x: Mapping,
    expected: nx.MultiDiGraph,
) -> bool:
    try:
        restored = _restore(residual, record, stored_x)
    except (KeyError, TypeError, ValueError, nx.NetworkXError):
        return False
    return _frozen_graph_fingerprint(restored) == _frozen_graph_fingerprint(expected)


def _field_consumption(
    residual: nx.MultiDiGraph,
    record: Mapping,
    stored_x: Mapping,
    expected: nx.MultiDiGraph,
) -> dict[str, bool]:
    mutations = {}
    changed = deepcopy(record)
    changed["h_v"] += 1
    mutations["V-time"] = changed
    changed = deepcopy(record)
    changed["inheritance_pair"] = (sp.Rational(1, 4), sp.Rational(3, 4))
    mutations["V-inheritance-pair"] = changed
    changed = deepcopy(record)
    typed = list(changed["typed_inheritance"])
    typed[0] = (typed[0][0], record["typed_inheritance"][1][1])
    typed[1] = (typed[1][0], record["typed_inheritance"][0][1])
    changed["typed_inheritance"] = tuple(typed)
    mutations["V-typed-inheritance"] = changed
    for key in ("child", "parent_0", "parent_1"):
        changed = deepcopy(record)
        word = list(changed["rate_words"][key])
        word[0] = (word[0][0], word[0][1] + 1)
        changed["rate_words"][key] = tuple(word)
        mutations[f"V-rate-word-{key}"] = changed
    changed = deepcopy(record)
    changed["parent_incidences"] = changed["parent_incidences"][:-1]
    mutations["V-parent-incidence"] = changed
    changed = deepcopy(record)
    changed["child_incidence"] = ()
    mutations["V-child-incidence"] = changed
    changed = deepcopy(record)
    changed["direction_quotient"] = "reverse"
    mutations["V-direction"] = changed
    changed = deepcopy(record)
    changed["typing_kind"] = "wrong-typing"
    mutations["V-repair-typing"] = changed
    changed = deepcopy(record)
    changed["label_triple"] = ("wrong-child",) + tuple(changed["label_triple"][1:])
    mutations["V-label-triple"] = changed
    changed = deepcopy(record)
    changed["child_component"] = ()
    mutations["V-child-component"] = changed
    killed = {
        name: not _bundle_matches(residual, mutant, stored_x, expected)
        for name, mutant in mutations.items()
    }
    changed_x = deepcopy(stored_x)
    weights = list(changed_x["typed_weights"])
    weights[0] = (weights[0][0], weights[0][1] + sp.Rational(1, 7))
    changed_x["typed_weights"] = tuple(weights)
    killed["X-typed-weight"] = not _bundle_matches(residual, record, changed_x, expected)
    changed_x = deepcopy(stored_x)
    changed_x["incoming"] = changed_x["incoming"][:-1]
    killed["X-parent-incidence"] = not _bundle_matches(residual, record, changed_x, expected)
    changed_x = deepcopy(stored_x)
    changed_x["focal"] = "wrong-focal"
    killed["X-focal"] = not _bundle_matches(residual, record, changed_x, expected)
    changed_x = deepcopy(stored_x)
    changed_x["outgoing"] = ()
    killed["X-outgoing-incidence"] = not _bundle_matches(
        residual, record, changed_x, expected
    )
    changed_x = deepcopy(stored_x)
    changed_x["child_corridor_parent"] = stored_x["bypass_parent"]
    killed["X-child-corridor-parent"] = not _bundle_matches(
        residual, record, changed_x, expected
    )
    changed_x = deepcopy(stored_x)
    changed_x["bypass_parent"] = stored_x["child_corridor_parent"]
    killed["X-bypass-parent"] = not _bundle_matches(
        residual, record, changed_x, expected
    )
    return killed


def _serialize(value):
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, nx.MultiDiGraph):
        return _graph_payload(value)
    if isinstance(value, Mapping):
        return {str(key): _serialize(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_serialize(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _graph_payload(graph: nx.MultiDiGraph) -> dict:
    return {
        "nodes": [
            {"id": str(node), "attributes": _serialize(dict(data))}
            for node, data in sorted(graph.nodes(data=True), key=lambda row: str(row[0]))
        ],
        "edges": [
            {
                "tail": str(tail),
                "head": str(head),
                "key": str(key),
                "attributes": _serialize(dict(data)),
            }
            for tail, head, key, data in sorted(
                graph.edges(keys=True, data=True), key=lambda row: (str(row[0]), str(row[1]), str(row[2]))
            )
        ],
    }


def _analytic_formula_checks() -> dict:
    a, b, left, right = sp.symbols("a b left right", positive=True)
    moments = tuple(sp.expand(a * left**order + b * right**order) for order in range(4))
    determinant = sp.factor(moments[0] * moments[2] - moments[1] ** 2)
    sum_rates = sp.factor(
        (moments[0] * moments[3] - moments[1] * moments[2]) / determinant
    )
    product_rates = sp.factor(
        (moments[1] * moments[3] - moments[2] ** 2) / determinant
    )
    expected_determinant = a * b * (left - right) ** 2
    return {
        "hankel_determinant_identity": sp.simplify(determinant - expected_determinant) == 0,
        "rate_sum_identity": sp.simplify(sum_rates - left - right) == 0,
        "rate_product_identity": sp.simplify(product_rates - left * right) == 0,
        "equal_rate_rank_drop": sp.simplify(determinant.subs(right, left)) == 0,
        "determinant_formula": str(expected_determinant),
    }


def _equal_first_parent_fixture(fixture: Mapping) -> dict:
    """Return a full strict asynchronous schedule with one equal first chamber."""
    changed = deepcopy(fixture)
    chambers = [dict(row) for row in fixture["parent_chambers"]]
    shared_rate = chambers[0]["rates"][0]
    chambers[0]["rates"] = (shared_rate, shared_rate)
    chambers[1]["rates"] = (chambers[1]["rates"][0], shared_rate)
    changed["parent_chambers"] = tuple(chambers)
    return changed


def _equal_child_fixture(fixture: Mapping) -> dict:
    """Return the full fixture with two adjacent equal child-rate chambers."""
    changed = deepcopy(fixture)
    changed["child_chambers"] = tuple(
        (duration, fixture["equal_child_rate"])
        for duration, _ in fixture["child_chambers"]
    )
    return changed


def _case_record(manifest: Mapping, case: Mapping, manifest_hash: str) -> tuple[dict, list[str]]:
    failures = []
    specification = manifest["primitive_cores"][case["core"]]
    repair = tuple(map(int, case["repair_segments"]))
    minima = _minimal_repairs(specification)
    if repair not in minima:
        failures.append(f"manifest repair {repair!r} is not predicate-minimal")
    graph = _ported_graph(specification, repair)
    if not (_tree_child(graph) and _strong_tail(graph)):
        failures.append("ported graph is outside the declared graph domain")
    topology = _topology_record(graph, case)
    fixture = _fixture(manifest)
    physical_q = tuple(rational(value) for value in case["physical_q"])
    observation = _observation(topology, fixture, physical_q)
    recovered = _recover_record(observation, topology)
    if not _validate_record(recovered):
        failures.append("recovered V record is incomplete")
    expected_q = tuple(sorted(physical_q, key=sp.default_sort_key))
    if recovered["inheritance_pair"] != expected_q:
        failures.append("total-law inverse failed to recover the unordered q pair")
    parent_ids = tuple(row[0] + "|" + row[2] for row in topology["parent_incidences"])
    expected_typed_q = tuple(zip(parent_ids, physical_q))
    if recovered["typed_inheritance"] != expected_typed_q:
        failures.append("anchor typing failed to recover the physical q assignment")
    residual, q8_witness = _residual_q8(graph, topology)
    equal_parent_checks = []
    for q in fixture["equal_parent_q_values"]:
        equal_fixture = _equal_first_parent_fixture(fixture)
        equal_physical_q = (q, sp.simplify(1 - q))
        equal_observation = _observation(topology, equal_fixture, equal_physical_q)
        equal_recovered = _recover_record(equal_observation, topology)
        equal_stored_x = _stored_x_macro(topology, equal_observation["p_x"])
        equal_expected = _decorate_expected(
            graph, equal_fixture, topology, equal_physical_q
        )
        equal_expected_pair = tuple(sorted(equal_physical_q, key=sp.default_sort_key))
        equal_expected_typed = tuple(zip(parent_ids, equal_physical_q))
        equal_joint = _bundle_matches(
            residual, equal_recovered, equal_stored_x, equal_expected
        )
        equal_parent_checks.append({
            "q": q,
            "branch": equal_recovered["prony"][0]["branch"],
            "q_pair": equal_recovered["inheritance_pair"],
            "typed_q": equal_recovered["typed_inheritance"],
            "joint_reattachment_exact": equal_joint,
            "exact": (
                _validate_record(equal_recovered)
                and equal_recovered["prony"][0]["branch"] == "equal-rate"
                and equal_recovered["inheritance_pair"] == equal_expected_pair
                and equal_recovered["typed_inheritance"] == equal_expected_typed
                and equal_joint
            ),
        })
    if not all(row["exact"] for row in equal_parent_checks):
        failures.append("full equal-first-parent-rate or q=1/2 joint lift failed")
    equal_child_fixture = _equal_child_fixture(fixture)
    equal_child_observation = _observation(topology, equal_child_fixture, physical_q)
    equal_child_recovered = _recover_record(equal_child_observation, topology)
    equal_child_stored_x = _stored_x_macro(
        topology, equal_child_observation["p_x"]
    )
    equal_child_expected = _decorate_expected(
        graph, equal_child_fixture, topology, physical_q
    )
    equal_child_joint = _bundle_matches(
        residual,
        equal_child_recovered,
        equal_child_stored_x,
        equal_child_expected,
    )
    equal_child_check = {
        "word": equal_child_recovered["rate_words"]["child"],
        "one_compressed_epoch": len(equal_child_recovered["rate_words"]["child"]) == 1,
        "joint_reattachment_exact": equal_child_joint,
        "exact": _validate_record(equal_child_recovered) and equal_child_joint,
    }
    if not equal_child_check["exact"] or not equal_child_check["one_compressed_epoch"]:
        failures.append("full equal-child-epoch compression/joint lift failed")
    if sp.simplify(observation["direction_forward"] - observation["direction_reversed"]) == 0:
        failures.append("directional marked cell collapsed outside q=1/2")
    stored_x = _stored_x_macro(topology, observation["p_x"])
    expected = _decorate_expected(graph, fixture, topology, physical_q)
    exact_joint = _bundle_matches(residual, recovered, stored_x, expected)
    if not exact_joint:
        failures.append("residual + recovered V + stored X did not restore the decorated graph")
    field_consumption = _field_consumption(residual, recovered, stored_x, expected)
    if not all(field_consumption.values()):
        failures.append("a stored V/X field is not semantically consumed")
    formula_checks = _analytic_formula_checks()
    if not all(value for key, value in formula_checks.items() if key != "determinant_formula"):
        failures.append("independent Prony identities failed")
    core_code = _canonical_role_code(_core_graph(specification))
    expected_v_attributes = expected.nodes["V"]
    independent_expected_record_match = (
        recovered["h_v"] == expected_v_attributes["h_v"]
        and recovered["inheritance_pair"] == expected_v_attributes["inheritance_pair"]
        and recovered["rate_words"] == expected_v_attributes["rate_words"]
        and recovered["direction_quotient"] == expected_v_attributes["direction_quotient"]
        and recovered["typing_kind"] == expected_v_attributes["typing_kind"]
        and recovered["label_triple"] == expected_v_attributes["label_triple"]
        and recovered["p_x"] == fixture["p_x"]
    )
    if not independent_expected_record_match:
        failures.append("recovered V record differs from manifest-derived expected record")
    witness = {
        "manifest_schema": manifest["schema"],
        "manifest_sha256": manifest_hash,
        "case_id": case["case_id"],
        "core_key": case["core"],
        "core_code": core_code,
        "primitive_segment_count": len(specification["arcs"]),
        "repair_subset_count_checked": 2 ** len(specification["arcs"]),
        "predicate_minimal_repairs": minima,
        "selected_repair": repair,
        "zero_atom_breakpoint": recovered["zero_atom"],
        "recovered_v_record": recovered,
        "stored_x_macro": stored_x,
        "residual_q8": q8_witness,
        "prony_formula_checks": formula_checks,
        "equal_parent_rate_checks": equal_parent_checks,
        "equal_child_epoch_check": equal_child_check,
        "physical_q_assignment": expected_typed_q,
        "swapped_physical_q_fixture": physical_q == (sp.Rational(2, 3), sp.Rational(1, 3)),
        "strict_asynchronous_parent_changes": recovered["asynchronous_changes"],
        "typing_kind": topology["typing_kind"],
        "label_triple": topology["label_triple"],
        "joint_reattachment_order": ("restore-recovered-V", "reattach-stored-X-macro"),
        "joint_reattachment_exact": exact_joint,
        "independent_expected_record_match": independent_expected_record_match,
        "field_consumption_mutants_killed": field_consumption,
        "failures": failures,
    }
    record = make_record(
        job=JOB,
        case_input={
            "manifest_sha256": manifest_hash,
            "case": case,
        },
        status="BLOCKING" if failures else "PASS",
        graph=_graph_payload(graph),
        exact_witness=_serialize(witness),
        declared_quotient_orbit={
            "core_code": core_code,
            "repair": list(repair),
            "residual": "unary-Q8-V",
        },
        notes=(
            "Raw arcs and rational fixtures come only from the handoff manifest; "
            "the inverse receives total laws and separately marked typing cells, "
            "never latent Paper B state."
        ),
        extra={"case_name": case["case_id"], "core_key": case["core"]},
    )
    return record, failures


def enumerate_records(manifest_path: Path) -> list[dict]:
    manifest = load_manifest(manifest_path)
    manifest_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    records = []
    all_failures = []
    for case in manifest["cases"]:
        record, failures = _case_record(manifest, case, manifest_hash)
        records.append(record)
        all_failures.extend((case["case_id"], failure) for failure in failures)
    if len(records) != 4:
        raise AssertionError("exposure verifier must emit exactly four repair records")
    swapped_count = sum(
        record["exact_witness"]["swapped_physical_q_fixture"] for record in records
    )
    if swapped_count != 1:
        raise AssertionError("exactly one physical-q swap fixture is required")
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    manifest_path = Path(args.manifest)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    records = enumerate_records(manifest_path)
    write_jsonl(output, records)
    blocking = [record["case_name"] for record in records if record["status"] != "PASS"]
    if blocking:
        print(f"INDEPENDENT_EXPOSURE_LOSS_BLOCKING cases={blocking!r}")
        raise SystemExit(1)
    print(
        "INDEPENDENT_EXPOSURE_LOSS_OK "
        "records=4 unequal=4 equal_parent=8 q_half=4 swapped_physical_q=1"
    )


if __name__ == "__main__":
    main()
