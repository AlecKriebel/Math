#!/usr/bin/env python3
"""Clean-room finite audit of general target-response propagation.

The checker uses only the Python standard library.  It enumerates every
labeled graph through order five, every guard number, and every nonempty
eternal subfamily of the dominating configurations.  It checks the
vertex-star theorem without assuming the greatest eternal family.  In the
equality cases it also checks the global active set, ridge-component color
invariance, complement-neighbor exclusion, and the common-color extension
criterion.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[2]
TARGET = CAMPAIGN / "math/lemmas/general_target_response_propagation.md"
TARGET_LOG = (
    CAMPAIGN / "math/working/general_target_response_propagation/RESEARCH_LOG.md"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bits(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def graph_from_mask(n: int, edge_mask: int) -> list[int]:
    adj = [0] * n
    pos = 0
    for u in range(n):
        for v in range(u + 1, n):
            if (edge_mask >> pos) & 1:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
            pos += 1
    return adj


def independent(adj: list[int], state: int) -> bool:
    for u in bits(state):
        if adj[u] & state:
            return False
    return True


def dominates(adj: list[int], state: int) -> bool:
    covered = state
    for u in bits(state):
        covered |= adj[u]
    return covered == (1 << len(adj)) - 1


def fixed_size_states(n: int, k: int) -> list[int]:
    return [
        sum(1 << u for u in comb)
        for comb in itertools.combinations(range(n), k)
    ]


def response_tables(adj: list[int], k: int):
    configs = [s for s in fixed_size_states(len(adj), k) if dominates(adj, s)]
    index = {s: i for i, s in enumerate(configs)}
    response = [[0] * len(adj) for _ in configs]
    all_vertices = (1 << len(adj)) - 1
    for i, state in enumerate(configs):
        for r in bits(all_vertices ^ state):
            choices = 0
            for u in bits(state & adj[r]):
                nxt = (state ^ (1 << u)) | (1 << r)
                j = index.get(nxt)
                if j is not None:
                    choices |= 1 << j
            response[i][r] = choices
    return configs, index, response


def eternal_family_masks(adj: list[int], k: int):
    configs, index, response = response_tables(adj, k)
    all_vertices = (1 << len(adj)) - 1
    for family in range(1, 1 << len(configs)):
        valid = True
        pending = family
        while pending and valid:
            bit = pending & -pending
            i = bit.bit_length() - 1
            pending ^= bit
            for r in bits(all_vertices ^ configs[i]):
                if not (response[i][r] & family):
                    valid = False
                    break
        if valid:
            yield family, configs, index, response


def greatest_kernel(adj: list[int], k: int) -> set[int]:
    configs, _index, response = response_tables(adj, k)
    alive = (1 << len(configs)) - 1
    all_vertices = (1 << len(adj)) - 1
    changed = True
    while changed:
        changed = False
        delete = 0
        for i, state in enumerate(configs):
            if not ((alive >> i) & 1):
                continue
            if any(
                not (response[i][r] & alive)
                for r in bits(all_vertices ^ state)
            ):
                delete |= 1 << i
        if delete:
            alive &= ~delete
            changed = True
    return {configs[i] for i in range(len(configs)) if (alive >> i) & 1}


def alpha(adj: list[int]) -> int:
    n = len(adj)
    return max(s.bit_count() for s in range(1 << n) if independent(adj, s))


def gamma(adj: list[int]) -> int:
    n = len(adj)
    if n == 0:
        return 0
    return min(s.bit_count() for s in range(1 << n) if dominates(adj, s))


def gamma_infinity(adj: list[int]) -> int:
    n = len(adj)
    if n == 0:
        return 0
    return next(k for k in range(1, n + 1) if greatest_kernel(adj, k))


def deletion(adj: list[int], x: int) -> list[int]:
    old = [u for u in range(len(adj)) if u != x]
    pos = {u: i for i, u in enumerate(old)}
    out = [0] * len(old)
    for u in old:
        for v in bits(adj[u]):
            if v != x:
                out[pos[u]] |= 1 << pos[v]
    return out


def complement_edges_without(adj: list[int], x: int) -> list[tuple[int, int]]:
    vertices = [u for u in range(len(adj)) if u != x]
    return [
        (u, v)
        for i, u in enumerate(vertices)
        for v in vertices[i + 1 :]
        if not ((adj[u] >> v) & 1)
    ]


def proper_deletion_colorings(adj: list[int], x: int, k: int):
    vertices = [u for u in range(len(adj)) if u != x]
    edges = complement_edges_without(adj, x)
    for values in itertools.product(range(k), repeat=len(vertices)):
        color = dict(zip(vertices, values))
        if all(color[u] != color[v] for u, v in edges):
            yield color


def theta(adj: list[int]) -> int:
    n = len(adj)
    if n == 0:
        return 0
    for k in range(1, n + 1):
        # A k-coloring of the complement is a clique partition with at
        # most k parts; unused colors are harmless here.
        edges = [
            (u, v)
            for u in range(n)
            for v in range(u + 1, n)
            if not ((adj[u] >> v) & 1)
        ]
        for values in itertools.product(range(k), repeat=n):
            if all(values[u] != values[v] for u, v in edges):
                return k
    raise AssertionError("chromatic search exhausted")


def ridge_components(facets: list[int], k: int) -> list[list[int]]:
    remaining = set(facets)
    components = []
    while remaining:
        start = min(remaining)
        remaining.remove(start)
        component = [start]
        queue = [start]
        while queue:
            state = queue.pop()
            neighbors = [
                other
                for other in remaining
                if (state & other).bit_count() == k - 1
            ]
            for other in neighbors:
                remaining.remove(other)
                component.append(other)
                queue.append(other)
        components.append(component)
    return components


def active_from(
    adj: list[int],
    family: int,
    index: dict[int, int],
    state: int,
    v: int,
    x: int,
) -> bool:
    if not ((adj[v] >> x) & 1):
        return False
    nxt = (state ^ (1 << v)) | (1 << x)
    j = index.get(nxt)
    return j is not None and ((family >> j) & 1) == 1


def audit_transport_path(
    adj: list[int],
    family_states: set[int],
    state: int,
    destination: int,
    v: int,
    x: int,
    stats: dict,
):
    """Replay the proof's forced attacks for one ordered active pair."""
    bit_v = 1 << v
    bit_x = 1 << x
    current = (state ^ bit_v) | bit_x
    assert current in family_states
    common = (state & destination) ^ bit_v
    old = state & ~destination
    new = destination & ~state
    assert old.bit_count() == new.bit_count()
    remaining_old = old
    installed_new = 0

    for b in bits(new):
        bit_b = 1 << b
        assert not (current & bit_b)  # the attack is unoccupied

        # Shared and previously installed destination guards have no move
        # edge because they lie with b in the independent destination.
        frozen = common | installed_new
        assert all(not ((adj[u] >> b) & 1) for u in bits(frozen))

        # Even when x-b is an edge, moving x leaves v undominated.
        x_successor = (current ^ bit_x) | bit_b
        assert not dominates(adj, x_successor)
        assert x_successor not in family_states

        retained = []
        for u in bits(current & adj[b]):
            successor = (current ^ (1 << u)) | bit_b
            if successor in family_states:
                retained.append((u, successor))
        assert retained  # literal eternal closure at the current state
        assert all((remaining_old >> u) & 1 for u, _ in retained)

        mover, current = min(retained)
        remaining_old ^= 1 << mover
        installed_new |= bit_b
        assert current == bit_x | common | installed_new | remaining_old
        assert current.bit_count() == state.bit_count()
        assert dominates(adj, current)
        stats["forced_transport_steps"] += 1

    assert current == (destination ^ bit_v) | bit_x
    assert current in family_states
    stats["forced_transport_paths"] += 1


def check_family(
    adj: list[int],
    k: int,
    family: int,
    configs: list[int],
    index: dict[int, int],
    stats: dict,
):
    n = len(adj)
    family_states = [
        configs[i] for i in range(len(configs)) if (family >> i) & 1
    ]
    independent_states = [s for s in family_states if independent(adj, s)]

    # General theorem: for each (x,v), active status is constant across all
    # retained independent k-states avoiding x and containing v.
    signature: dict[tuple[int, int], bool] = {}
    star_states: dict[tuple[int, int], list[int]] = {}
    for state in independent_states:
        for x in range(n):
            if (state >> x) & 1:
                continue
            for v in bits(state):
                status = active_from(adj, family, index, state, v, x)
                key = (x, v)
                if key in signature:
                    assert signature[key] == status
                    stats["vertex_star_comparisons"] += 1
                else:
                    signature[key] = status
                star_states.setdefault(key, []).append(state)
                stats["active_incidences"] += 1

    family_set = set(family_states)
    for key, states in star_states.items():
        x, v = key
        if not signature[key]:
            continue
        for state in states:
            for destination in states:
                audit_transport_path(
                    adj,
                    family_set,
                    state,
                    destination,
                    v,
                    x,
                    stats,
                )

    if alpha(adj) != k:
        return

    stats["equality_families"] += 1
    all_independent = [
        s for s in fixed_size_states(n, k) if independent(adj, s)
    ]
    assert all(s in family_set for s in all_independent)

    full_gamma = gamma(adj)
    full_ginf = gamma_infinity(adj)
    full_theta = theta(adj)

    for x in range(n):
        facets = [s for s in all_independent if not ((s >> x) & 1)]
        if not facets:
            continue

        # Equation (12), including the edge forced by domination.
        physical_active: dict[int, bool] = {}
        for state in facets:
            responders = []
            for v in bits(state):
                nxt = (state ^ (1 << v)) | (1 << x)
                in_family = nxt in family_set
                is_active = active_from(adj, family, index, state, v, x)
                assert in_family == is_active
                physical_active.setdefault(v, is_active)
                assert physical_active[v] == is_active
                if is_active:
                    responders.append(v)
            assert responders
            stats["equality_target_facets"] += 1

        components = ridge_components(facets, k)
        support_union = 0
        for component in components:
            for state in component:
                support_union |= state
        deletion_vertices = ((1 << n) - 1) ^ (1 << x)
        inactive_mask = sum(
            1 << v
            for v in bits(deletion_vertices)
            if not physical_active.get(v, False)
        )

        # Equation (17d): no complement k-clique is supported entirely on
        # inactive vertices.  Equivalently, no independent k-set of G-x
        # lies inside R_x.
        assert all((state & ~inactive_mask) != 0 for state in facets)
        inactive_omega = max(
            (
                state.bit_count()
                for state in range(1 << n)
                if not (state & (1 << x))
                and not (state & ~inactive_mask)
                and independent(adj, state)
            ),
            default=0,
        )
        assert inactive_omega <= k - 1
        stats["inactive_clique_bound_checks"] += 1

        colorings = list(proper_deletion_colorings(adj, x, k))
        del_adj = deletion(adj, x)
        del_equal = (
            gamma(del_adj) == k
            and alpha(del_adj) == k
            and gamma_infinity(del_adj) == k
        )

        for color in colorings:
            # Every facet is a k-clique in the complement and must be
            # rainbow in a proper k-coloring.
            for state in facets:
                assert {color[v] for v in bits(state)} == set(range(k))
                stats["rainbow_facet_checks"] += 1

            component_sets = []
            for component in components:
                first = component[0]
                active_colors = {
                    color[v]
                    for v in bits(first)
                    if physical_active.get(v, False)
                }
                assert active_colors
                for state in component[1:]:
                    other = {
                        color[v]
                        for v in bits(state)
                        if physical_active.get(v, False)
                    }
                    assert other == active_colors
                    stats["component_invariance_checks"] += 1

                support = 0
                for state in component:
                    support |= state
                for r in bits(support):
                    if not ((adj[r] >> x) & 1):
                        assert color[r] not in active_colors
                        stats["complement_neighbor_checks"] += 1

                inactive_support_colors = {
                    color[v] for v in bits(support & inactive_mask)
                }
                assert active_colors == set(range(k)) - inactive_support_colors
                stats["inactive_component_identity_checks"] += 1
                component_sets.append(active_colors)

            # Audit the exchanged-vertex equivalence literally on every
            # ridge edge, independently of component traversal.
            for i, state in enumerate(facets):
                for other in facets[i + 1 :]:
                    if (state & other).bit_count() != k - 1:
                        continue
                    shared = state & other
                    p = next(bits(state ^ shared))
                    q = next(bits(other ^ shared))
                    successor_p = (state ^ (1 << p)) | (1 << x)
                    successor_q = (other ^ (1 << q)) | (1 << x)
                    assert successor_p == successor_q
                    p_active = active_from(adj, family, index, state, p, x)
                    q_active = active_from(adj, family, index, other, q, x)
                    assert p_active == q_active
                    if successor_p in family_set:
                        assert (adj[p] >> x) & 1
                        assert (adj[q] >> x) & 1
                    assert color[p] == color[q]
                    stats["ridge_exchange_checks"] += 1

            if support_union == deletion_vertices:
                common = set(range(k))
                for active_colors in component_sets:
                    common &= active_colors
                inactive_colors = {color[v] for v in bits(inactive_mask)}
                assert common == set(range(k)) - inactive_colors
                assert bool(common) == (len(inactive_colors) <= k - 1)
                stats["inactive_global_identity_checks"] += 1

            stats["coloring_instances"] += 1

            if del_equal:
                common = set(range(k))
                for active_colors in component_sets:
                    common &= active_colors
                for w in common:
                    for v, c in color.items():
                        if c == w:
                            assert (adj[v] >> x) & 1
                    # Explicitly check that assigning x color w is proper.
                    for v in range(n):
                        if v != x and not ((adj[v] >> x) & 1):
                            assert color[v] != w
                    assert full_theta == k
                    stats["extension_witnesses"] += 1

        # Check the full-target component corollary whenever all literal
        # hypotheses happen to occur in the finite universe.
        critical = (
            full_gamma == k
            and full_ginf == k
            and full_theta > k
            and gamma(del_adj) == k
            and alpha(del_adj) == k
            and gamma_infinity(del_adj) == k
            and theta(del_adj) == k
        )
        if critical:
            for state in facets:
                if all(
                    active_from(adj, family, index, state, v, x)
                    for v in bits(state)
                ):
                    stats["critical_full_targets"] += 1
                    components = ridge_components(facets, k)
                    assert len(components) >= 3


def main():
    stats = {
        "active_incidences": 0,
        "coloring_instances": 0,
        "complement_neighbor_checks": 0,
        "component_invariance_checks": 0,
        "critical_full_targets": 0,
        "equality_families": 0,
        "equality_target_facets": 0,
        "eternal_families": 0,
        "extension_witnesses": 0,
        "forced_transport_paths": 0,
        "forced_transport_steps": 0,
        "graphs": 0,
        "inactive_clique_bound_checks": 0,
        "inactive_component_identity_checks": 0,
        "inactive_global_identity_checks": 0,
        "rainbow_facet_checks": 0,
        "ridge_exchange_checks": 0,
        "vertex_star_comparisons": 0,
    }
    by_k = {}
    for n in range(1, 6):
        edge_count = n * (n - 1) // 2
        for edge_mask in range(1 << edge_count):
            adj = graph_from_mask(n, edge_mask)
            stats["graphs"] += 1
            for k in range(1, n + 1):
                key = str(k)
                by_k.setdefault(
                    key,
                    {"eternal_families": 0, "equality_families": 0},
                )
                before_equal = stats["equality_families"]
                for family, configs, index, _response in eternal_family_masks(
                    adj, k
                ):
                    stats["eternal_families"] += 1
                    by_k[key]["eternal_families"] += 1
                    check_family(adj, k, family, configs, index, stats)
                by_k[key]["equality_families"] += (
                    stats["equality_families"] - before_equal
                )

    result = {
        "verdict": "PASS",
        "scope": "all labeled graphs n<=5, all 1<=k<=n, all eternal subfamilies",
        "target_sha256": sha256(TARGET),
        "target_log_sha256": sha256(TARGET_LOG),
        "stats": stats,
        "by_k": by_k,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
