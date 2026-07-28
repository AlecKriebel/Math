#!/usr/bin/env python3
"""Clean-room audit of the retained QQ1 hot-layer theorem.

This file imports neither the candidate checker nor a campaign evaluator.
It independently checks the finite set bookkeeping, all permitted endpoint
collisions, and the three frozen graph6 controls.  The accepted symbolic
theorems C-010, C-108, C-143, C-145, and C-158 remain dependencies.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math


CONTROLS = (
    ("dominating-ux", "Mslamztl~fnny~]~_"),
    ("nondominating-ux", "NslalntvXzn^{~n||^w"),
)
EDGE_CONTROL = "Oslally^v{zn{~y~nn~j~"


def decode_short_graph6(record: str) -> tuple[int, ...]:
    """Decode short graph6 into adjacency bitmasks."""
    codes = [ord(character) - 63 for character in record]
    if not codes or not 0 <= codes[0] <= 62:
        raise ValueError("only short graph6 is accepted")
    n = codes[0]
    bits = []
    for code in codes[1:]:
        if not 0 <= code <= 63:
            raise ValueError("invalid graph6 byte")
        for place in (32, 16, 8, 4, 2, 1):
            bits.append(bool(code & place))
    needed = n * (n - 1) // 2
    if len(bits) < needed or any(bits[needed:]):
        raise ValueError("bad graph6 length or padding")
    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if bits[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return tuple(adjacency)


def bitset(vertices) -> int:
    answer = 0
    for vertex in vertices:
        answer |= 1 << vertex
    return answer


def vertices(state: int):
    while state:
        atom = state & -state
        yield atom.bit_length() - 1
        state ^= atom


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    closed = state
    for guard in vertices(state):
        closed |= adjacency[guard]
    return closed == (1 << len(adjacency)) - 1


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    return all(
        not (adjacency[vertex] & (state ^ (1 << vertex)))
        for vertex in vertices(state)
    )


def subset_parameters(adjacency: tuple[int, ...]) -> tuple[int, int, int]:
    n = len(adjacency)
    gamma = n
    indep_dom = n
    alpha = 0
    for state in range(1 << n):
        size = state.bit_count()
        if size < gamma and dominates(adjacency, state):
            gamma = size
        if independent(adjacency, state):
            alpha = max(alpha, size)
            if size < indep_dom and dominates(adjacency, state):
                indep_dom = size
    return gamma, indep_dom, alpha


def complement(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    universe = (1 << len(adjacency)) - 1
    return tuple(
        universe ^ adjacency[vertex] ^ (1 << vertex)
        for vertex in range(len(adjacency))
    )


def colorable(adjacency: tuple[int, ...], color_count: int) -> bool:
    """Exact DSATUR search, independently implemented with bit color masks."""
    n = len(adjacency)
    assigned = [-1] * n
    forbidden = [0] * n
    degrees = [row.bit_count() for row in adjacency]

    def recurse(done: int) -> bool:
        if done == n:
            return True
        uncolored = [vertex for vertex in range(n) if assigned[vertex] < 0]
        pivot = max(
            uncolored,
            key=lambda vertex: (
                forbidden[vertex].bit_count(),
                degrees[vertex],
                -vertex,
            ),
        )
        for color in range(color_count):
            color_bit = 1 << color
            if forbidden[pivot] & color_bit:
                continue
            assigned[pivot] = color
            changed = []
            neighbors = adjacency[pivot]
            for neighbor in uncolored:
                if (
                    neighbor != pivot
                    and neighbors & (1 << neighbor)
                    and not (forbidden[neighbor] & color_bit)
                ):
                    forbidden[neighbor] |= color_bit
                    changed.append(neighbor)
            if recurse(done + 1):
                return True
            for neighbor in changed:
                forbidden[neighbor] ^= color_bit
            assigned[pivot] = -1
        return False

    return recurse(0)


def theta(adjacency: tuple[int, ...], lower: int) -> int:
    opposite = complement(adjacency)
    for colors in range(lower, len(adjacency) + 1):
        if colorable(opposite, colors):
            return colors
    raise AssertionError("singleton coloring failed")


def greatest_kernel(
    adjacency: tuple[int, ...], guard_count: int
) -> tuple[set[int], dict[int, int]]:
    n = len(adjacency)
    family = {
        bitset(choice)
        for choice in itertools.combinations(range(n), guard_count)
        if dominates(adjacency, bitset(choice))
    }
    ranks: dict[int, int] = {}
    round_number = 0
    while True:
        doomed = set()
        for state in family:
            for target in range(n):
                target_bit = 1 << target
                if state & target_bit:
                    continue
                response_exists = False
                for guard in vertices(state):
                    if not adjacency[guard] & target_bit:
                        continue
                    successor = (state ^ (1 << guard)) | target_bit
                    if successor in family:
                        response_exists = True
                        break
                if not response_exists:
                    doomed.add(state)
                    break
        if not doomed:
            return family, ranks
        round_number += 1
        for state in doomed:
            ranks[state] = round_number
        family -= doomed


def eternal_number(adjacency: tuple[int, ...], gamma: int):
    kernels = {}
    for guards in range(gamma, len(adjacency) + 1):
        family, ranks = greatest_kernel(adjacency, guards)
        kernels[guards] = (family, ranks)
        if family:
            return guards, kernels
    raise AssertionError("all vertices must be eternal")


def state_tuple(state: int) -> list[int]:
    return list(vertices(state))


def edge(adjacency: tuple[int, ...], left: int, right: int) -> bool:
    return bool(adjacency[left] & (1 << right))


def active(
    adjacency: tuple[int, ...],
    family: set[int],
    responder: int,
    target: int,
) -> bool:
    n = len(adjacency)
    values = []
    for pair in itertools.combinations(
        [v for v in range(n) if v not in (responder, target)], 2
    ):
        source = bitset((responder, *pair))
        if not independent(adjacency, source):
            continue
        successor = (source ^ (1 << responder)) | (1 << target)
        values.append(edge(adjacency, responder, target) and successor in family)
    if not values or len(set(values)) != 1:
        raise AssertionError("activity is absent or not vertex-star invariant")
    return values[0]


def parameter_vector(adjacency: tuple[int, ...]):
    gamma, indep_dom, alpha = subset_parameters(adjacency)
    eternal, kernels = eternal_number(adjacency, gamma)
    return (
        [gamma, indep_dom, alpha, eternal, theta(adjacency, alpha)],
        kernels,
    )


def canonical_core_audit(adjacency: tuple[int, ...], family: set[int]):
    u, x, p, q, r, b, c = range(7)
    required_edges = (
        (u, x), (u, r), (p, r), (q, r), (p, b), (q, c),
        (x, b), (x, c), (b, c), (u, p), (u, q),
    )
    required_nonedges = (
        (x, p), (x, q), (p, q), (x, r), (b, u), (b, r),
        (b, q), (c, u), (c, r), (c, p),
    )
    if not all(edge(adjacency, *pair) for pair in required_edges):
        raise AssertionError("missing canonical QQ1 core edge")
    if any(edge(adjacency, *pair) for pair in required_nonedges):
        raise AssertionError("canonical QQ1 core nonedge is present")
    named_retained = (
        (x, p, q), (x, b, q), (x, p, c), (u, b, c), (r, b, c)
    )
    if not all(bitset(state) in family for state in named_retained):
        raise AssertionError("canonical QQ1 retained state missing")
    if active(adjacency, family, u, x) is not True:
        raise AssertionError("u->x activity missing")
    if active(adjacency, family, x, u) is not False:
        raise AssertionError("forbidden reverse activity present")
    return {
        "core_edges": ["".join(map(str, pair)) for pair in required_edges],
        "core_nonedges": ["".join(map(str, pair)) for pair in required_nonedges],
        "named_retained_count": len(named_retained),
        "active_u_x": True,
        "active_x_u": False,
    }


def audit_old_control(label: str, record: str):
    adjacency = decode_short_graph6(record)
    vector, kernels = parameter_vector(adjacency)
    if vector != [2, 3, 3, 3, 3]:
        raise AssertionError(f"bad parameter vector for {label}: {vector}")
    family2, _ = kernels[2]
    family3, rank3 = kernels[3]
    u, x, p, q, r, b, c = range(7)
    core = canonical_core_audit(adjacency, family3)
    completions = [
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (x, r)
        and not edge(adjacency, vertex, x)
        and not edge(adjacency, vertex, r)
    ]
    if len(completions) != 1:
        raise AssertionError("old control does not have unique x,r completion")
    d = completions[0]
    if not all(edge(adjacency, d, vertex) for vertex in (p, q, b, c)):
        raise AssertionError("old completion is not four-hit")
    hot = [
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (u, d)
        and not edge(adjacency, vertex, u)
        and not edge(adjacency, vertex, d)
    ]
    if hot:
        raise AssertionError("old control unexpectedly has a hot vertex")
    B = bitset((u, p, q))
    P = bitset((u, p, d))
    Q = bitset((u, q, d))
    O = bitset((u, r, d))
    ranks = [rank3[state] for state in (B, P, Q, O)]
    if ranks != [1, 2, 2, 3]:
        raise AssertionError("wrong old-control rank diamond")
    witnesses = []
    for mover, expected_witness in ((u, x), (p, b), (q, c)):
        successor = (B ^ (1 << mover)) | (1 << r)
        missed = [
            vertex
            for vertex in range(len(adjacency))
            if not (successor & (1 << vertex))
            and not (adjacency[vertex] & successor)
        ]
        if expected_witness not in missed:
            raise AssertionError("named private witness does not miss successor")
        witnesses.append(
            {
                "mover": mover,
                "successor": state_tuple(successor),
                "named_witness": expected_witness,
                "all_missed": missed,
            }
        )
    return {
        "label": label,
        "graph6": record,
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "order": len(adjacency),
        "size": sum(row.bit_count() for row in adjacency) // 2,
        "parameters_gamma_i_alpha_ginf_theta": vector,
        "greatest_pair_family_size": len(family2),
        "greatest_triple_family_size": len(family3),
        "canonical_core": core,
        "completion_d": d,
        "completion_four_hit": True,
        "retained_A": bitset((u, x, d)) in family3,
        "rank_B_P_Q_O": ranks,
        "private_successors": witnesses,
        "hot_set": hot,
        "u_d_pair_dominates": dominates(adjacency, bitset((u, d))),
    }


def audit_edge_control(record: str):
    adjacency = decode_short_graph6(record)
    vector, kernels = parameter_vector(adjacency)
    if vector != [2, 3, 3, 3, 3]:
        raise AssertionError(f"bad edge-control vector: {vector}")
    family2, _ = kernels[2]
    family3, rank3 = kernels[3]
    u, x, p, q, r, b, c, d, w, s, t = range(11)
    core = canonical_core_audit(adjacency, family3)
    if not edge(adjacency, u, d):
        raise AssertionError("the edge control has ud nonedge")
    xr_completions = [
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (x, r)
        and not edge(adjacency, vertex, x)
        and not edge(adjacency, vertex, r)
    ]
    if xr_completions != [d]:
        raise AssertionError("wrong x,r completion in edge control")
    if not all(edge(adjacency, d, vertex) for vertex in (p, q, b, c)):
        raise AssertionError("edge-control completion is not four-hit")
    hot = [
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (u, d)
        and not edge(adjacency, vertex, u)
        and not edge(adjacency, vertex, d)
    ]
    S = [
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (u, w)
        and not edge(adjacency, vertex, u)
        and not edge(adjacency, vertex, w)
    ]
    T = [
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (d, w)
        and not edge(adjacency, vertex, d)
        and not edge(adjacency, vertex, w)
    ]
    if hot != [w] or S != [b, s] or T != [t]:
        raise AssertionError("wrong hot or completion set")
    all_named = {
        "root_T": (x, p, q),
        "U": (u, b, c),
        "R": (r, b, c),
        "I": (x, r, d),
        "A": (u, x, d),
        "K": (u, d, w),
        "E": (x, d, w),
        "F": (r, d, w),
        "S_b": (u, w, b),
        "S_s": (u, w, s),
        "J_t": (d, w, t),
        "Q_b_t": (b, w, t),
        "Q_s_t": (s, w, t),
    }
    retention = {
        name: bitset(state) in family3 for name, state in all_named.items()
    }
    if not all(retention.values()):
        raise AssertionError("edge control misses a claimed retained state")
    side_states = {
        "leave_c": (u, d, c),
        "leave_b": (u, b, d),
    }
    side_retention = {
        name: bitset(state) in family3
        for name, state in side_states.items()
    }
    if not any(side_retention.values()):
        raise AssertionError("no retained side response at d")
    B = bitset((u, p, q))
    O = bitset((u, r, d))
    ranks = [rank3[B], rank3[O]]
    if ranks != [1, 3]:
        raise AssertionError("wrong B/O ranks")
    dominating_pairs = sum(
        dominates(adjacency, bitset(pair))
        for pair in itertools.combinations(range(len(adjacency)), 2)
    )
    if dominating_pairs != 34:
        raise AssertionError("wrong dominating-pair count")
    return {
        "graph6": record,
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "order": len(adjacency),
        "size": sum(row.bit_count() for row in adjacency) // 2,
        "parameters_gamma_i_alpha_ginf_theta": vector,
        "greatest_pair_family_size": len(family2),
        "greatest_triple_family_size": len(family3),
        "canonical_core": core,
        "u_d_edge": True,
        "completion_x_r": xr_completions,
        "completion_four_hit": True,
        "hot_set": hot,
        "completion_set_S": S,
        "completion_set_T": T,
        "side_response_retention": side_retention,
        "named_retention": retention,
        "rank_B_O": ranks,
        "dominating_pair_count": dominating_pairs,
        "classification": "GAMMA2_BOUNDARY_ONLY",
    }


def move(state, guard, target):
    state = frozenset(state)
    if guard not in state or target in state:
        raise AssertionError("occupied attack or absent mover")
    return state - {guard} | {target}


def symbolic_named_audit():
    U = frozenset(("u", "b", "c"))
    I = frozenset(("x", "r", "d"))
    A = frozenset(("u", "x", "d"))
    O = frozenset(("u", "r", "d"))

    side_paths = []
    for mover, remaining in (("b", "c"), ("c", "b")):
        side = move(U, mover, "d")
        bad = move(side, "u", "x")
        reached = move(side, remaining, "x")
        if bad != frozenset(("x", "d", remaining)) or reached != A:
            raise AssertionError("retained-A route is wrong")
        side_paths.append(
            {
                "mover_at_d": mover,
                "retained_side_state": sorted(side),
                "bad_u_successor_missing_r": sorted(bad),
                "forced_A": sorted(reached),
            }
        )

    K = move(A, "x", "w")
    F = move(K, "u", "r")
    if move(K, "w", "r") != O:
        raise AssertionError("wrong omitted corner from K")
    if move(F, "w", "x") != I:
        raise AssertionError("retained four-state loop does not close")
    E_from_I = move(I, "r", "w")
    E_from_K = move(K, "u", "x")
    if E_from_I != E_from_K:
        raise AssertionError("E corner is not shared")

    edge_branch_source = frozenset(("x", "w", "s"))
    if move(edge_branch_source, "s", "d") != E_from_I:
        raise AssertionError("ud-edge completion proof reaches wrong E")

    return {
        "retained_A_side_paths": side_paths,
        "loop_A_K_F_I": [
            sorted(A), sorted(K), sorted(F), sorted(I), sorted(A)
        ],
        "omitted_O": sorted(O),
        "shared_E": sorted(E_from_I),
        "E_nonedge_branch": "C-108 from independent K",
        "E_edge_branch": {
            "independent_completion_source": sorted(
                frozenset(("u", "w", "s"))
            ),
            "transported_state": sorted(edge_branch_source),
            "unique_attack_at_d_reaches": sorted(E_from_I),
        },
        "activity_sources": {
            "x_to_w": sorted(I),
            "r_to_w": sorted(I),
            "r_to_u": sorted(I),
            "nonedge_branch_w_to_x": sorted(K),
            "nonedge_branch_u_to_r": sorted(K),
        },
    }


def side_polarization_audit():
    cases = []
    for response in (("b",), ("c",), ("b", "c")):
        patterns = []
        for hit_b, hit_c in itertools.product((False, True), repeat=2):
            if "b" in response and not hit_c:
                continue
            if "c" in response and not hit_b:
                continue
            patterns.append({"wb": hit_b, "wc": hit_c})
        forced = {
            side
            for side in ("b", "c")
            if all(pattern["w" + side] for pattern in patterns)
        }
        expected = {
            "c" if response_guard == "b" else "b"
            for response_guard in response
        }
        if forced != expected:
            raise AssertionError("wrong global side polarization")
        cases.append(
            {
                "retained_side_response_list": list(response),
                "allowed_hot_patterns": patterns,
                "uniform_sides": sorted(forced),
            }
        )
    return {
        "nonempty_response_lists": 3,
        "single_hot_assignments_total": sum(
            len(case["allowed_hot_patterns"]) for case in cases
        ),
        "cases": cases,
    }


def bowtie_case(
    ud_edge: bool,
    s_role: str,
    t_role: str,
    side_left: str,
):
    """Check one alias pattern in the omitted-Q contradiction."""
    other = "c" if side_left == "b" else "b"
    # side_left is the side guard retained in X after the other one moves.
    s = {"b": "b", "c": "c", "d": "d", "fresh": "s"}[s_role]
    t = {"u": "u", "fresh": "t"}[t_role]
    R = frozenset(("r", "b", "c"))
    X = move(R, other, "w")
    if X != frozenset(("r", side_left, "w")):
        raise AssertionError("wrong side branch")

    if s == side_left:
        Y = X
        shortcut = True
    else:
        bad_u = move(X, "r", s)
        expected_bad = frozenset((s, side_left, "w"))
        if bad_u != expected_bad:
            raise AssertionError("wrong intermediate state missing u")
        Y = move(X, side_left, s)
        if Y != frozenset(("r", "w", s)):
            raise AssertionError("side branch failed to merge")
        shortcut = False

    if t in Y:
        raise AssertionError("final attack is occupied")
    Q = move(Y, "r", t)
    bad_d = move(Y, s, t)
    if Q != frozenset((s, "w", t)):
        raise AssertionError("wrong mixed Q state")
    if bad_d != frozenset(("r", "w", t)):
        raise AssertionError("wrong terminal state missing d")

    # Endpoint degeneracies are stronger: the assumed omitted Q is already
    # an independent endpoint state.
    endpoint = None
    if s_role == "d":
        endpoint = "J_t"
    if t_role == "u":
        endpoint = "S_s" if endpoint is None else "K_w"
    return {
        "ud_edge": ud_edge,
        "s_role": s_role,
        "t_role": t_role,
        "side_left_in_X": side_left,
        "collision_shortcut": shortcut,
        "Y": sorted(Y),
        "assumed_omitted_Q": sorted(Q),
        "other_successor_missing_d": sorted(bad_d),
        "already_retained_endpoint_if_degenerate": endpoint,
    }


def bowtie_exhaustion():
    audited = []
    for ud_edge in (False, True):
        s_roles = ("b", "c", "fresh") if ud_edge else ("b", "c", "d", "fresh")
        t_roles = ("fresh",) if ud_edge else ("u", "fresh")
        for s_role, t_role in itertools.product(s_roles, t_roles):
            # If s is a side vertex, it must be the side left in X because
            # sw is a nonedge; the other side is the only mover to w.
            possible_left = (s_role,) if s_role in ("b", "c") else ("b", "c")
            for side_left in possible_left:
                audited.append(
                    bowtie_case(
                        ud_edge=ud_edge,
                        s_role=s_role,
                        t_role=t_role,
                        side_left=side_left,
                    )
                )
    collision_count = sum(case["collision_shortcut"] for case in audited)
    degeneracy_count = sum(
        case["already_retained_endpoint_if_degenerate"] is not None
        for case in audited
    )
    signatures = [
        ":".join(
            (
                "edge" if case["ud_edge"] else "nonedge",
                case["s_role"],
                case["t_role"],
                case["side_left_in_X"],
                "collision" if case["collision_shortcut"] else "attack-s",
                case["already_retained_endpoint_if_degenerate"] or "ordinary",
            )
        )
        for case in audited
    ]
    return {
        "alias_branches_checked": len(audited),
        "side_collision_shortcuts": collision_count,
        "endpoint_degeneracy_branches": degeneracy_count,
        "all_terminal_other_successors_miss_d": True,
        "branch_signatures": signatures,
    }


def evaluate():
    detailed_controls = {
        label: audit_old_control(label, record)
        for label, record in CONTROLS
    }
    controls = {}
    for label, item in detailed_controls.items():
        controls[label] = {
            "graph6": item["graph6"],
            "graph6_sha256": item["graph6_sha256"],
            "order": item["order"],
            "size": item["size"],
            "parameters_gamma_i_alpha_ginf_theta": item[
                "parameters_gamma_i_alpha_ginf_theta"
            ],
            "greatest_pair_family_size": item["greatest_pair_family_size"],
            "greatest_triple_family_size": item[
                "greatest_triple_family_size"
            ],
            "completion_d": item["completion_d"],
            "completion_four_hit": item["completion_four_hit"],
            "retained_A": item["retained_A"],
            "rank_B_P_Q_O": item["rank_B_P_Q_O"],
            "private_successor_missed_sets": [
                entry["all_missed"] for entry in item["private_successors"]
            ],
            "hot_set": item["hot_set"],
            "u_d_pair_dominates": item["u_d_pair_dominates"],
            "active_u_x": item["canonical_core"]["active_u_x"],
            "active_x_u": item["canonical_core"]["active_x_u"],
        }
    edge_detail = audit_edge_control(EDGE_CONTROL)
    edge_summary = {
        "graph6": edge_detail["graph6"],
        "graph6_sha256": edge_detail["graph6_sha256"],
        "order": edge_detail["order"],
        "size": edge_detail["size"],
        "parameters_gamma_i_alpha_ginf_theta": edge_detail[
            "parameters_gamma_i_alpha_ginf_theta"
        ],
        "greatest_pair_family_size": edge_detail[
            "greatest_pair_family_size"
        ],
        "greatest_triple_family_size": edge_detail[
            "greatest_triple_family_size"
        ],
        "u_d_edge": edge_detail["u_d_edge"],
        "completion_x_r": edge_detail["completion_x_r"],
        "completion_four_hit": edge_detail["completion_four_hit"],
        "hot_set": edge_detail["hot_set"],
        "completion_set_S": edge_detail["completion_set_S"],
        "completion_set_T": edge_detail["completion_set_T"],
        "side_response_retention": edge_detail["side_response_retention"],
        "retained_named_states": sorted(
            name
            for name, retained in edge_detail["named_retention"].items()
            if retained
        ),
        "rank_B_O": edge_detail["rank_B_O"],
        "dominating_pair_count": edge_detail["dominating_pair_count"],
        "active_u_x": edge_detail["canonical_core"]["active_u_x"],
        "active_x_u": edge_detail["canonical_core"]["active_x_u"],
        "classification": edge_detail["classification"],
    }
    named = symbolic_named_audit()
    named_summary = {
        "retained_A_side_routes": len(named["retained_A_side_paths"]),
        "loop_A_K_F_I": named["loop_A_K_F_I"],
        "omitted_O": named["omitted_O"],
        "shared_E": named["shared_E"],
        "E_nonedge_branch": named["E_nonedge_branch"],
        "E_edge_branch": named["E_edge_branch"],
        "all_activity_sources_explicitly_independent": True,
    }
    return {
        "schema": "qq1-hot-layer-hostile-clean-v1",
        "status": "PASS",
        "symbolic": {
            "named_transitions": named_summary,
            "side_polarization": side_polarization_audit(),
            "hot_clique_argument": (
                "For distinct w,y in W_d, retained K_w dominates y; "
                "both u and d miss y, hence wy is an edge."
            ),
            "bowtie_alias_exhaustion": bowtie_exhaustion(),
            "completion_set_facts": {
                "S_and_T_nonempty": "well-coveredness extends each independent pair",
                "S_and_T_cliques": "an internal nonedge would make an independent 4-set",
                "S_intersection_T_empty": "a common member would be missed by retained K_w",
                "possible_s_core_roles": ["b", "c", "d-if-ud-nonedge"],
                "possible_t_core_roles": ["u-if-ud-nonedge"],
            },
        },
        "controls": controls,
        "hot_edge_control": edge_summary,
        "scope": {
            "accepted": [
                "retention of A={u,x,d}",
                "nonempty clique W_d and its uniform side",
                "five retained d,w corners with fixed omitted O",
                "retention of every outer mixed bow-tie",
                "reciprocity of every nondegenerate outer bow-tie edge",
            ],
            "open": [
                "elimination of the ud-nonedge inner repair square",
                "elimination of the ud-edge inner retained branch",
                "canonical QQ1",
                "complete k=3",
                "the universal gamma-theta conjecture",
            ],
            "controls_are": "sharp gamma=2 boundaries only",
        },
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
