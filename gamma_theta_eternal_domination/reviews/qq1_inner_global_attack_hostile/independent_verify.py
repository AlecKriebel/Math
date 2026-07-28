#!/usr/bin/env python3
"""Clean-room bitmask audit of the two QQ1 cross-layer controls.

This program does not import any campaign evaluator, candidate verifier, or
search code.  Graphs and configurations are represented by integer bitmasks.
The one-guard kernel is recomputed directly from the definition, while theta
is certified by the independently recomputed alpha lower bound and an exact
clique-partition backtrack.
"""

from __future__ import annotations

from functools import lru_cache
import hashlib
import itertools
import json


RECORDS = {
    "two_witness": "OslallyN]z~r|^{~|^|~^",
    "repaired_pw": "OslallyN]fv|y~v^}n}{n",
}

LABEL = {
    "u": 0,
    "x": 1,
    "p": 2,
    "q": 3,
    "r": 4,
    "b": 5,
    "c": 6,
    "d": 7,
    "w": 8,
    "z": 9,
}


def decode_graph6(record: str) -> tuple[int, ...]:
    """Decode the short graph6 format directly from its published bit order."""

    if not record:
        raise AssertionError("empty graph6 record")
    order = ord(record[0]) - 63
    if not 0 <= order <= 62:
        raise AssertionError("this audit only supports short graph6 headers")
    payload = []
    for char in record[1:]:
        value = ord(char) - 63
        if not 0 <= value <= 63:
            raise AssertionError("invalid graph6 payload")
        payload.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = order * (order - 1) // 2
    if len(payload) < required or any(payload[required:]):
        raise AssertionError("truncated graph6 record or nonzero padding")

    neighbors = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if payload[cursor]:
                neighbors[low] |= 1 << high
                neighbors[high] |= 1 << low
            cursor += 1
    return tuple(neighbors)


def encode_graph6(neighbors: tuple[int, ...]) -> str:
    order = len(neighbors)
    bits = []
    for high in range(1, order):
        for low in range(high):
            bits.append((neighbors[low] >> high) & 1)
    while len(bits) % 6:
        bits.append(0)
    chars = [chr(order + 63)]
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        chars.append(chr(value + 63))
    return "".join(chars)


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def mask_of(items) -> int:
    answer = 0
    for item in items:
        answer |= 1 << item
    return answer


def tuple_of(mask: int) -> tuple[int, ...]:
    return tuple(vertices(mask))


def masks_of_size(order: int, size: int):
    for subset in itertools.combinations(range(order), size):
        yield mask_of(subset)


def covered(neighbors: tuple[int, ...], state: int) -> int:
    answer = state
    for vertex in vertices(state):
        answer |= neighbors[vertex]
    return answer


def dominates(neighbors: tuple[int, ...], state: int) -> bool:
    return covered(neighbors, state) == (1 << len(neighbors)) - 1


def independent(neighbors: tuple[int, ...], state: int) -> bool:
    for vertex in vertices(state):
        if neighbors[vertex] & (state ^ (1 << vertex)):
            return False
    return True


def clique(neighbors: tuple[int, ...], state: int) -> bool:
    for vertex in vertices(state):
        required = state ^ (1 << vertex)
        if required & ~neighbors[vertex]:
            return False
    return True


def static_parameters(neighbors: tuple[int, ...]):
    order = len(neighbors)
    domination = order + 1
    independent_domination = order + 1
    independence = 0
    for state in range(1, 1 << order):
        size = state.bit_count()
        is_independent = independent(neighbors, state)
        is_dominating = dominates(neighbors, state)
        if is_dominating and size < domination:
            domination = size
        if is_independent:
            independence = max(independence, size)
            if is_dominating and size < independent_domination:
                independent_domination = size
    return domination, independent_domination, independence


def greatest_kernel(neighbors: tuple[int, ...], guard_count: int):
    """Literal synchronous greatest-fixed-point deletion with round ranks."""

    order = len(neighbors)
    alive = {
        state
        for state in masks_of_size(order, guard_count)
        if dominates(neighbors, state)
    }
    initial_size = len(alive)
    rank: dict[int, int] = {}
    round_number = 1
    all_vertices = (1 << order) - 1
    while True:
        deleted = set()
        for state in alive:
            unoccupied = all_vertices ^ state
            for target in vertices(unoccupied):
                target_bit = 1 << target
                has_response = False
                for guard in vertices(state):
                    if neighbors[guard] & target_bit:
                        successor = (state ^ (1 << guard)) | target_bit
                        if successor in alive:
                            has_response = True
                            break
                if not has_response:
                    deleted.add(state)
                    break
        if not deleted:
            return alive, rank, initial_size
        for state in deleted:
            rank[state] = round_number
        alive.difference_update(deleted)
        round_number += 1


def find_clique_partition(
    neighbors: tuple[int, ...], part_count: int
) -> tuple[tuple[int, ...], ...] | None:
    """Exact symmetry-broken partition search, independent of DSATUR."""

    order = len(neighbors)
    complement_degree = [
        order - 1 - neighbors[vertex].bit_count() for vertex in range(order)
    ]
    order_vertices = tuple(
        sorted(range(order), key=lambda v: (-complement_degree[v], v))
    )
    blocks: list[int] = []

    def recurse(position: int) -> bool:
        if position == order:
            return True
        vertex = order_vertices[position]
        bit = 1 << vertex
        seen_block_masks = set()
        for index, block in enumerate(blocks):
            if block in seen_block_masks:
                continue
            seen_block_masks.add(block)
            if block & ~neighbors[vertex]:
                continue
            blocks[index] |= bit
            if recurse(position + 1):
                return True
            blocks[index] ^= bit
        if len(blocks) < part_count:
            blocks.append(bit)
            if recurse(position + 1):
                return True
            blocks.pop()
        return False

    if not recurse(0):
        return None
    return tuple(sorted((tuple_of(block) for block in blocks)))


def common_nonneighbors(
    neighbors: tuple[int, ...], left: int, right: int
) -> tuple[int, ...]:
    forbidden = (
        (1 << left)
        | (1 << right)
        | neighbors[left]
        | neighbors[right]
    )
    available = ((1 << len(neighbors)) - 1) & ~forbidden
    return tuple_of(available)


def all_dominating_pairs(neighbors: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        pair
        for pair in itertools.combinations(range(len(neighbors)), 2)
        if dominates(neighbors, mask_of(pair))
    )


def retained_activity(
    neighbors: tuple[int, ...],
    family: set[int],
    responder: int,
    target: int,
) -> dict:
    roots = []
    for state in masks_of_size(len(neighbors), 3):
        if not independent(neighbors, state):
            continue
        if not (state & (1 << responder)) or state & (1 << target):
            continue
        successor = (state ^ (1 << responder)) | (1 << target)
        roots.append(
            {
                "root": list(tuple_of(state)),
                "successor": list(tuple_of(successor)),
                "successor_retained": successor in family,
            }
        )
    if not roots:
        raise AssertionError("activity audit has no independent root")
    values = {entry["successor_retained"] for entry in roots}
    if len(values) != 1:
        raise AssertionError("activity is not uniform across independent roots")
    return {"active": values.pop(), "roots": roots}


def edge(neighbors: tuple[int, ...], left: int, right: int) -> bool:
    return bool(neighbors[left] & (1 << right))


def check_core_incidence(neighbors: tuple[int, ...]):
    u, x, p, q, r, b, c, d, w, z = range(10)
    required_edges = {
        (u, x),
        (u, r),
        (p, r),
        (q, r),
        (p, b),
        (q, c),
        (x, b),
        (x, c),
        (b, c),
        (u, p),
        (u, q),
        (d, p),
        (d, q),
        (d, b),
        (d, c),
        (w, x),
        (d, z),
        (w, z),
        (u, d),
    }
    required_nonedges = {
        (x, p),
        (x, q),
        (p, q),
        (x, r),
        (b, u),
        (b, r),
        (b, q),
        (c, u),
        (c, r),
        (c, p),
        (x, d),
        (r, d),
        (u, w),
        (d, w),
        (u, z),
        (x, z),
    }
    missing = sorted(pair for pair in required_edges if not edge(neighbors, *pair))
    extra = sorted(pair for pair in required_nonedges if edge(neighbors, *pair))
    if missing or extra:
        raise AssertionError(f"named incidence failure: missing={missing}, extra={extra}")
    return {
        "required_edge_count": len(required_edges),
        "required_nonedge_count": len(required_nonedges),
        "all_match": True,
    }


def induced_cycle_check(neighbors: tuple[int, ...]):
    u, x, _, _, _, _, _, d, w, z = range(10)
    cycle = (u, d, z, w, x)
    cycle_edges = {
        tuple(sorted((cycle[index], cycle[(index + 1) % 5])))
        for index in range(5)
    }
    actual = {
        tuple(sorted(pair))
        for pair in itertools.combinations(cycle, 2)
        if edge(neighbors, *pair)
    }
    if actual != cycle_edges:
        raise AssertionError(
            f"named five-set is not the claimed induced C5: {sorted(actual)}"
        )
    return {
        "vertices_in_cycle_order": list(cycle),
        "induced_edges": [list(pair) for pair in sorted(actual)],
    }


def qq1_deleting_attack(neighbors: tuple[int, ...]):
    u, x, p, q, r, b, c = range(7)
    B = mask_of((u, p, q))
    ledger = []
    for guard, missed in ((u, x), (p, b), (q, c)):
        if not edge(neighbors, guard, r):
            raise AssertionError("named QQ1 mover edge is absent")
        successor = (B ^ (1 << guard)) | (1 << r)
        if dominates(neighbors, successor):
            raise AssertionError("rank-one named successor unexpectedly dominates")
        if covered(neighbors, successor) & (1 << missed):
            raise AssertionError("private witness is not missed")
        ledger.append(
            {
                "guard": guard,
                "successor": list(tuple_of(successor)),
                "missed_private_witness": missed,
            }
        )
    return ledger


def audit_control(name: str, record: str):
    neighbors = decode_graph6(record)
    if encode_graph6(neighbors) != record:
        raise AssertionError(f"{name}: graph6 roundtrip failed")
    order = len(neighbors)
    if order != 16:
        raise AssertionError(f"{name}: expected order 16")

    gamma, i_value, alpha = static_parameters(neighbors)
    kernels = {}
    ranks = {}
    initial_sizes = {}
    for guard_count in (1, 2, 3):
        kernels[guard_count], ranks[guard_count], initial_sizes[guard_count] = (
            greatest_kernel(neighbors, guard_count)
        )
    eternal = next(
        count for count in (1, 2, 3) if kernels[count]
    )

    lower_bound_theta = alpha
    clique_partition = None
    theta = None
    for count in range(lower_bound_theta, order + 1):
        clique_partition = find_clique_partition(neighbors, count)
        if clique_partition is not None:
            theta = count
            break
    if theta is None:
        raise AssertionError("singleton partition was not found")
    for block in clique_partition:
        if not clique(neighbors, mask_of(block)):
            raise AssertionError("reported theta block is not a graph clique")

    vector = [gamma, i_value, alpha, eternal, theta]
    if vector != [2, 3, 3, 3, 3]:
        raise AssertionError(f"{name}: parameter vector mismatch {vector}")

    u, x, p, q, r, b, c, d, w, z = range(10)
    family = kernels[3]
    rank = ranks[3]
    B = mask_of((u, p, q))
    O = mask_of((u, r, d))
    if rank.get(B) != 1 or rank.get(O) != 3:
        raise AssertionError(f"{name}: wrong B/O ranks")

    named = {
        "T": mask_of((x, p, q)),
        "U": mask_of((u, b, c)),
        "R": mask_of((r, b, c)),
        "I": mask_of((x, r, d)),
        "A": mask_of((u, x, d)),
        "K_w": mask_of((u, d, w)),
        "E_w": mask_of((x, d, w)),
        "F_w": mask_of((r, d, w)),
        "bridge": mask_of((u, w, z)),
        "ux_ridge": mask_of((u, x, z)),
    }
    missing_named = sorted(label for label, state in named.items() if state not in family)
    if missing_named:
        raise AssertionError(f"{name}: missing retained states {missing_named}")

    Wux = common_nonneighbors(neighbors, u, x)
    Wud = common_nonneighbors(neighbors, u, d)
    Wpw = common_nonneighbors(neighbors, p, w)
    if Wux != (z,) or Wud != (w,):
        raise AssertionError(f"{name}: wrong primary witness layers")

    Suw = common_nonneighbors(neighbors, u, w)
    Tdw = common_nonneighbors(neighbors, d, w)
    outer_states = []
    for left in Suw:
        for right in Tdw:
            state = mask_of((left, w, right))
            if state not in family:
                raise AssertionError(f"{name}: omitted outer completion")
            outer_states.append(list(tuple_of(state)))

    bridge = named["bridge"]
    for side in (b, c):
        if not (
            edge(neighbors, w, side) or edge(neighbors, z, side)
        ):
            raise AssertionError(f"{name}: bridge fails side coverage")
    if not dominates(neighbors, bridge):
        raise AssertionError(f"{name}: bridge state is not dominating")

    activity_ux = retained_activity(neighbors, family, u, x)
    activity_xu = retained_activity(neighbors, family, x, u)
    if not activity_ux["active"] or activity_xu["active"]:
        raise AssertionError(f"{name}: wrong asymmetric activity orientation")

    pairs = all_dominating_pairs(neighbors)
    if name == "two_witness":
        if Wpw:
            raise AssertionError("first control unexpectedly repairs {p,w}")
        displayed_pair = (p, w)
        expected_pair_count = 29
    else:
        if Wpw != (15,):
            raise AssertionError("second control has wrong {p,w} witness")
        displayed_pair = (q, 14)
        expected_pair_count = 21
    if displayed_pair not in pairs or len(pairs) != expected_pair_count:
        raise AssertionError(f"{name}: wrong dominating-pair boundary")

    return {
        "graph6": record,
        "graph6_roundtrip": encode_graph6(neighbors),
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "order": order,
        "size": sum(row.bit_count() for row in neighbors) // 2,
        "parameter_vector_gamma_i_alpha_ginf_theta": vector,
        "theta_lower_bound_source": "independence_number",
        "theta_clique_partition": [list(block) for block in clique_partition],
        "kernel_initial_sizes_k1_k2_k3": [
            initial_sizes[count] for count in (1, 2, 3)
        ],
        "greatest_kernel_sizes_k1_k2_k3": [
            len(kernels[count]) for count in (1, 2, 3)
        ],
        "rank_B_O": [rank[B], rank[O]],
        "core_incidence": check_core_incidence(neighbors),
        "qq1_rank_one_deleting_attack": qq1_deleting_attack(neighbors),
        "common_nonneighbors_ux": list(Wux),
        "common_nonneighbors_ud": list(Wud),
        "common_nonneighbors_pw": list(Wpw),
        "completion_set_u_w": list(Suw),
        "completion_set_d_w": list(Tdw),
        "retained_outer_completion_states": outer_states,
        "retained_named_states": {
            label: list(tuple_of(state)) for label, state in named.items()
        },
        "activity_u_to_x": activity_ux,
        "activity_x_to_u": activity_xu,
        "side_coverage": {
            "b": {"w_hits": edge(neighbors, w, b), "z_hits": edge(neighbors, z, b)},
            "c": {"w_hits": edge(neighbors, w, c), "z_hits": edge(neighbors, z, c)},
        },
        "induced_C5": induced_cycle_check(neighbors),
        "dominating_pair_count": len(pairs),
        "dominating_pairs": [list(pair) for pair in pairs],
        "displayed_boundary_pair": list(displayed_pair),
    }


def symbolic_transition_audit():
    """Collision and transition ledger independent of either fixed control."""

    # The canonical incidences exclude every collision listed here.
    d_distinct_from = ["u", "x", "p", "q", "r", "b", "c"]
    w_distinct_from = ["u", "x", "p", "q", "r", "b", "c", "d"]
    z_distinct_from_if_not_d = [
        "u",
        "x",
        "p",
        "q",
        "r",
        "b",
        "c",
        "w",
        "d",
    ]

    U = {"u", "b", "c"}
    side_b = (U - {"b"}) | {"d"}
    side_c = (U - {"c"}) | {"d"}
    A_from_b = (side_b - {"c"}) | {"x"}
    A_from_c = (side_c - {"b"}) | {"x"}
    if A_from_b != {"u", "x", "d"} or A_from_c != {"u", "x", "d"}:
        raise AssertionError("completion-state transition collision")

    A = {"u", "x", "d"}
    K = (A - {"x"}) | {"w"}
    if K != {"u", "d", "w"}:
        raise AssertionError("hot-state transition collision")

    # The z=d branch is literal equality D_{w,d}=K_w.
    bridge_collision = {"u", "w", "d"}
    if bridge_collision != K:
        raise AssertionError("z=d branch is not the retained hot state")

    bridge = (K - {"d"}) | {"z"}
    alternate = (K - {"w"}) | {"z"}
    u_successor = (alternate - {"u"}) | {"r"}
    z_successor = (alternate - {"z"}) | {"r"}
    if bridge != {"u", "w", "z"}:
        raise AssertionError("wrong desired z-successor")
    if alternate != {"u", "d", "z"}:
        raise AssertionError("wrong alternate z-successor")
    if u_successor != {"r", "d", "z"}:
        raise AssertionError("wrong nondominating r-successor")
    if z_successor != {"u", "d", "r"}:
        raise AssertionError("wrong omitted r-successor")

    return {
        "d_distinct_from": d_distinct_from,
        "w_distinct_from": w_distinct_from,
        "z_distinct_from_in_noncollision_branch": z_distinct_from_if_not_d,
        "z_equals_d_branch": {
            "bridge_equals_hot_state": True,
            "state": sorted(K),
        },
        "lemma_1_1": {
            "attack_d_from": sorted(U),
            "retained_side_candidates": [sorted(side_b), sorted(side_c)],
            "attack_x_reaches": sorted(A),
        },
        "theorem_2_1_noncollision": {
            "attack_z_from": sorted(K),
            "desired_successor": sorted(bridge),
            "only_alternate_successor": sorted(alternate),
            "attack_r_from_alternate": {
                "u_successor_misses_x": sorted(u_successor),
                "optional_z_successor_is_omitted_O": sorted(z_successor),
                "d_is_graph_ineligible": True,
            },
            "O_omission_used_only_as_family_obstruction": True,
        },
        "all_attacked_vertices_unoccupied": True,
        "all_transitions_replace_exactly_one_guard": True,
    }


def main():
    result = {
        "schema": "qq1-inner-global-hostile-cleanroom-v1",
        "status": "PASS",
        "symbolic_transition_audit": symbolic_transition_audit(),
        "controls": {
            name: audit_control(name, record)
            for name, record in RECORDS.items()
        },
        "scope": (
            "Independent fixed-control and symbolic transition audit. "
            "No SAT/CEGAR UNSAT trace, finite exclusion, QQ1 elimination, "
            "complete k=3 theorem, or universal conjecture resolution is certified."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
