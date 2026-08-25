#!/usr/bin/env python3
"""Independent brute-force check of the cycle/theta event universe.

This file deliberately imports no code or data from the submitted package.
It starts from three abstract pole-to-pole paths, places one incoming source
and two reticulation events, orients every resulting segment, enforces the
binary local degrees and acyclicity, and quotients only by literal directed
multigraph isomorphism.  It then tests every occupied-segment subset directly
against simplicity and the fixed-mixed-graph no-omnian incidence condition.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter, defaultdict


POLES = ("P0", "P1")
EVENTS = ("S", "R0", "R1")


def permutations_by_role(nodes, roles):
    groups = defaultdict(list)
    for node in nodes:
        groups[roles[node]].append(node)
    ordered_roles = sorted(groups)
    slots = {
        role: tuple(f"{role}{i}" for i in range(len(groups[role])))
        for role in ordered_roles
    }
    for products in itertools.product(
        *(itertools.permutations(slots[role]) for role in ordered_roles)
    ):
        mapping = {}
        for role, perm in zip(ordered_roles, products):
            for old, new in zip(groups[role], perm):
                mapping[old] = new
        yield mapping


def canonical_key(nodes, roles, arcs, external_children):
    """Canonical directed-multigraph key, preserving vertex roles."""
    best = None
    role_order = {r: i for i, r in enumerate(sorted(set(roles.values())))}
    for mapping in permutations_by_role(nodes, roles):
        relabelled = sorted((mapping[u], mapping[v]) for u, v in arcs)
        children = sorted(mapping[u] for u in external_children)
        role_rows = sorted((mapping[u], role_order[roles[u]]) for u in nodes)
        row = (tuple(role_rows), tuple(relabelled), tuple(children))
        if best is None or row < best:
            best = row
    return best


def all_event_allocations():
    """Place S internally and each R either at a distinct pole or on a path."""
    # A location is a path 0,1,2 or a pole.  S is always internal.
    for s_path in range(3):
        for r0_loc in (0, 1, 2, "P0", "P1"):
            for r1_loc in (0, 1, 2, "P0", "P1"):
                if r0_loc == r1_loc and r0_loc in POLES:
                    continue
                if {r0_loc, r1_loc} == set(POLES):
                    # Reticulate poles are allowed into the orientation test;
                    # the claim is that acyclicity eliminates this case.
                    pass
                assignments = {0: [], 1: [], 2: []}
                assignments[s_path].append("S")
                pole_roles = {"P0": "T", "P1": "T"}
                valid = True
                for event, loc in (("R0", r0_loc), ("R1", r1_loc)):
                    if loc in POLES:
                        if pole_roles[loc] == "R":
                            valid = False
                        pole_roles[loc] = "R"
                    else:
                        assignments[loc].append(event)
                if not valid:
                    continue
                # Enumerate the order of multiple events along each path.
                for orders in itertools.product(
                    *(set(itertools.permutations(assignments[i])) for i in range(3))
                ):
                    yield pole_roles, tuple(tuple(x) for x in orders), s_path


def path_segments(path_orders):
    edges = []
    for p, order in enumerate(path_orders):
        chain = ("P0",) + order + ("P1",)
        for j, (u, v) in enumerate(zip(chain, chain[1:])):
            edges.append((p, j, u, v))
    return edges


def valid_orientation(pole_roles, path_orders, bits):
    segments = path_segments(path_orders)
    arcs = []
    for (_, _, u, v), bit in zip(segments, bits):
        arcs.append((u, v) if bit == 0 else (v, u))
    nodes = sorted(set(itertools.chain.from_iterable(arcs)))
    indeg = Counter(v for _, v in arcs)
    outdeg = Counter(u for u, _ in arcs)
    for node in nodes:
        if node == "S":
            need = (0, 2)
        elif node.startswith("R"):
            need = (2, 0)  # path-sink; its unique child is an external port
        elif node in POLES and pole_roles[node] == "R":
            need = (2, 1)
        else:
            need = (1, 2)
        if (indeg[node], outdeg[node]) != need:
            return None

    # Kahn acyclicity and reachability from the unique local source.
    remaining = Counter(indeg)
    queue = [u for u in nodes if remaining[u] == 0]
    seen = []
    while queue:
        u = queue.pop()
        seen.append(u)
        for a, v in arcs:
            if a == u:
                remaining[v] -= 1
                if remaining[v] == 0:
                    queue.append(v)
    if len(seen) != len(nodes):
        return None
    reachable = {"S"}
    changed = True
    while changed:
        changed = False
        for u, v in arcs:
            if u in reachable and v not in reachable:
                reachable.add(v)
                changed = True
    if reachable != set(nodes):
        return None
    return arcs, segments


def class_label(pole_roles, path_orders):
    pole_retics = sum(role == "R" for role in pole_roles.values())
    positions = {}
    for p, order in enumerate(path_orders):
        for event in order:
            positions[event] = p
    if pole_retics == 1:
        internal_r = next(r for r in ("R0", "R1") if r in positions)
        return "theta1" if positions[internal_r] == positions["S"] else "theta0"
    if pole_retics == 0:
        shares = any(positions[r] == positions["S"] for r in ("R0", "R1"))
        return "theta3" if shares else "theta2"
    return "two_reticulate_poles"


def mixed_graph_after_occupancy(pole_roles, arcs, occupied):
    """Build literal mixed incidences after inserting one port on each chosen arc."""
    ordinary = []
    retained = []
    node_roles = {"S": "tree", "P0": pole_roles["P0"], "P1": pole_roles["P1"]}
    for u, v in arcs:
        node_roles.setdefault(u, "R" if u.startswith("R") else "tree")
        node_roles.setdefault(v, "R" if v.startswith("R") else "tree")
    # Incoming physical arm and path-sink child arms.
    ordinary.append(("IN", "S"))
    node_roles["IN"] = "leaf"
    for r in ("R0", "R1"):
        if r in node_roles and not any(u == r for u, _ in arcs):
            leaf = "OUT_" + r
            ordinary.append((r, leaf))
            node_roles[leaf] = "leaf"

    for i, (u, v) in enumerate(arcs):
        if i in occupied:
            x = f"X{i}"
            leaf = f"L{i}"
            node_roles[x] = "tree"
            node_roles[leaf] = "leaf"
            ordinary.extend(((u, x), (x, leaf)))
            if node_roles[v] == "R":
                retained.append((x, v))
            else:
                ordinary.append((x, v))
        else:
            if node_roles[v] == "R":
                retained.append((u, v))
            else:
                ordinary.append((u, v))
    return node_roles, ordinary, retained


def valid_occupancy(pole_roles, arcs, occupied):
    roles, ordinary, retained = mixed_graph_after_occupancy(pole_roles, arcs, occupied)
    underlying = Counter(tuple(sorted(e)) for e in ordinary + retained)
    if any(n > 1 for n in underlying.values()):
        return False
    ordinary_incidence = Counter(itertools.chain.from_iterable(ordinary))
    for tail, _head in retained:
        if ordinary_incidence[tail] != 2:
            return False
    return True


def minimal_repairs(pole_roles, arcs):
    valid = []
    m = len(arcs)
    for k in range(m + 1):
        for subset in itertools.combinations(range(m), k):
            chosen = frozenset(subset)
            if valid_occupancy(pole_roles, arcs, chosen):
                valid.append(chosen)
    return [s for s in valid if not any(t < s for t in valid)]


def k4_minus_edge_rootings():
    """Literal all-edge rooting census, including the lowest-stable-ancestor test."""
    internal = (0, 1, 2, 3)
    leaves = (4, 5)
    root = 6
    nodes = set(range(7))
    edges = [(0, 1), (0, 2), (2, 1), (0, 3), (3, 1), (2, 4), (3, 5)]
    admitted = []

    def directed_paths(children, start, target):
        if start == target:
            return [(start,)]
        rows = []
        for child in children[start]:
            rows.extend(
                (start,) + suffix
                for suffix in directed_paths(children, child, target)
            )
        return rows

    for root_edge_index, root_edge in enumerate(edges):
        split = (
            edges[:root_edge_index] + edges[root_edge_index + 1:]
            + [(root_edge[0], root), (root, root_edge[1])]
        )
        for retics in itertools.combinations(internal, 2):
            roles = {
                node: ("R" if node in retics else "T") for node in internal
            }
            roles.update({4: "L", 5: "L", root: "root"})
            for bits in itertools.product((0, 1), repeat=len(split)):
                arcs = [
                    (v, u) if bit else (u, v)
                    for (u, v), bit in zip(split, bits)
                ]
                indegree = Counter(v for _, v in arcs)
                outdegree = Counter(u for u, _ in arcs)
                if (indegree[root], outdegree[root]) != (0, 2):
                    continue
                if any(
                    (indegree[node], outdegree[node])
                    != ((2, 1) if roles[node] == "R" else (1, 2))
                    for node in internal
                ):
                    continue
                if any((indegree[node], outdegree[node]) != (1, 0) for node in leaves):
                    continue
                children = {node: [] for node in nodes}
                remaining = dict.fromkeys(nodes, 0)
                for u, v in arcs:
                    children[u].append(v)
                    remaining[v] += 1
                queue = [node for node in nodes if remaining[node] == 0]
                seen = []
                while queue:
                    u = queue.pop()
                    seen.append(u)
                    for v in children[u]:
                        remaining[v] -= 1
                        if remaining[v] == 0:
                            queue.append(v)
                if len(seen) != len(nodes):
                    continue
                stable = None
                for leaf in leaves:
                    paths = directed_paths(children, root, leaf)
                    common = set.intersection(*(set(path) for path in paths))
                    stable = common if stable is None else stable & common
                if (stable or set()) - {root}:
                    continue
                tree_child = all(
                    roles[node] == "L"
                    or any(roles[child] in {"T", "L"} for child in children[node])
                    for node in nodes
                )
                admitted.append((root_edge_index, tuple(retics), tree_child))
    return {
        "admissible_lowest_stable_ancestor_rootings": len(admitted),
        "tree_child_rootings": sum(row[2] for row in admitted),
        "root_edge_census": dict(sorted(Counter(row[0] for row in admitted).items())),
    }


def main():
    canonical = {}
    raw_valid = 0
    two_pole_valid = 0
    for pole_roles, orders, _s_path in all_event_allocations():
        segments = path_segments(orders)
        for bits in itertools.product((0, 1), repeat=len(segments)):
            oriented = valid_orientation(pole_roles, orders, bits)
            if oriented is None:
                continue
            raw_valid += 1
            arcs, _segments = oriented
            nodes = sorted(set(itertools.chain.from_iterable(arcs)))
            roles = {
                node: (
                    "S" if node == "S" else
                    "R" if node.startswith("R") or pole_roles.get(node) == "R" else
                    "T"
                )
                for node in nodes
            }
            external = [r for r in ("R0", "R1") if r in nodes]
            key = canonical_key(nodes, roles, arcs, external)
            label = class_label(pole_roles, orders)
            if label == "two_reticulate_poles":
                two_pole_valid += 1
            canonical.setdefault(key, (label, pole_roles.copy(), orders, arcs))

    by_label = Counter(row[0] for row in canonical.values())
    repair_summary = {}
    for _key, (label, pole_roles, orders, arcs) in canonical.items():
        repairs = minimal_repairs(pole_roles, arcs)
        repair_summary.setdefault(label, []).append(
            {
                "segment_count": len(arcs),
                "repair_count": len(repairs),
                "repair_sizes": sorted(map(len, repairs)),
                "repairs": [sorted(x) for x in repairs],
                "orders": orders,
                "arcs": arcs,
            }
        )
    payload = {
        "cycle": {
            "segment_count": 2,
            "repairs": [
                sorted(x)
                for x in minimal_repairs(
                    {"P0": "T", "P1": "T"},
                    [("S", "R0"), ("S", "R0")],
                )
            ],
        },
        "K4_minus_edge": k4_minus_edge_rootings(),
        "raw_valid_oriented_placements": raw_valid,
        "canonical_class_count": len(canonical),
        "canonical_classes_by_type": dict(sorted(by_label.items())),
        "valid_two_reticulate_pole_placements": two_pole_valid,
        "repair_summary": repair_summary,
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    print(encoded, end="")
    print("payload_sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
