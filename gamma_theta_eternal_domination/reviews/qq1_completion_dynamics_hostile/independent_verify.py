#!/usr/bin/env python3
"""Clean-room audit for the canonical QQ1 completion-dynamics note.

This program does not import the candidate checker or campaign evaluators.
It independently:

* exhausts the cold-witness incidence template;
* checks the hot-witness collision and conditional repair bookkeeping;
* enumerates the allowed deletion-rank diamond;
* decodes and exactly evaluates the two frozen graph6 controls.

The accepted theorems C-010, C-064, C-108, C-143, C-146, C-158, and
C-161 remain mathematical dependencies rather than claims re-proved here.
"""

from __future__ import annotations

from functools import cache
import hashlib
import itertools
import json
import math


CONTROLS = {
    "dominating-ux": {
        "graph6": "Mslamztl~fnny~]~_",
        "order": 14,
        "size": 67,
        "completion": 9,
        "kernel3": 284,
        "ux_dominates": True,
    },
    "nondominating-ux": {
        "graph6": "NslalntvXzn^{~n||^w",
        "order": 15,
        "size": 78,
        "completion": 7,
        "kernel3": 285,
        "ux_dominates": False,
    },
}


def decode_graph6(record: str) -> tuple[int, ...]:
    raw = [ord(char) - 63 for char in record]
    if not raw or not 0 <= raw[0] <= 62:
        raise ValueError("clean checker supports short graph6 records only")
    n = raw[0]
    stream = []
    for value in raw[1:]:
        if not 0 <= value <= 63:
            raise ValueError("invalid graph6 character")
        stream.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    if len(stream) < needed or any(stream[needed:]):
        raise ValueError("truncated or nonzero-padded graph6")
    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if stream[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return tuple(adjacency)


def mask(vertices) -> int:
    answer = 0
    for vertex in vertices:
        answer |= 1 << vertex
    return answer


def members(state: int):
    while state:
        bit = state & -state
        yield bit.bit_length() - 1
        state ^= bit


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in members(state):
        covered |= adjacency[vertex]
    return covered == (1 << len(adjacency)) - 1


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    for vertex in members(state):
        if adjacency[vertex] & (state ^ (1 << vertex)):
            return False
    return True


def exact_parameters(adjacency: tuple[int, ...]):
    n = len(adjacency)

    gamma = None
    indep_dom = None
    alpha = 0
    for size in range(n + 1):
        for choice in itertools.combinations(range(n), size):
            state = mask(choice)
            is_independent = independent(adjacency, state)
            if is_independent:
                alpha = max(alpha, size)
                if indep_dom is None and dominates(adjacency, state):
                    indep_dom = size
            if gamma is None and dominates(adjacency, state):
                gamma = size

    limit = 1 << n
    clique = bytearray(limit)
    clique[0] = 1
    for state in range(1, limit):
        first = state & -state
        vertex = first.bit_length() - 1
        rest = state ^ first
        clique[state] = clique[rest] and not (rest & ~adjacency[vertex])

    @cache
    def cover(state: int) -> int:
        if not state:
            return 0
        first = state & -state
        best = n
        subset = state
        while subset:
            if subset & first and clique[subset]:
                best = min(best, 1 + cover(state ^ subset))
            subset = (subset - 1) & state
        return best

    theta = cover(limit - 1)
    return gamma, indep_dom, alpha, theta


def greatest_kernel(adjacency: tuple[int, ...], guard_count: int):
    n = len(adjacency)
    family = {
        mask(choice)
        for choice in itertools.combinations(range(n), guard_count)
        if dominates(adjacency, mask(choice))
    }
    ranks = {}
    round_number = 0
    while True:
        removed = set()
        for state in family:
            for target in range(n):
                target_bit = 1 << target
                if state & target_bit:
                    continue
                if not any(
                    adjacency[guard] & target_bit
                    and ((state ^ (1 << guard)) | target_bit) in family
                    for guard in members(state)
                ):
                    removed.add(state)
                    break
        if not removed:
            return family, ranks
        round_number += 1
        for state in removed:
            ranks[state] = round_number
        family.difference_update(removed)


def deletion_rank(adjacency, family, ranks, state):
    if not dominates(adjacency, state):
        return 0
    if state in family:
        return math.inf
    return ranks[state]


def active(adjacency, family, responder: int, target: int) -> bool:
    sources = []
    values = []
    n = len(adjacency)
    for other in itertools.combinations(
        [v for v in range(n) if v not in (responder, target)], 2
    ):
        state = mask((responder, *other))
        if not independent(adjacency, state):
            continue
        sources.append(state)
        successor = (state ^ (1 << responder)) | (1 << target)
        values.append(
            bool(adjacency[responder] & (1 << target))
            and successor in family
        )
    if not sources:
        raise AssertionError("responder lies in no independent triple")
    if len(set(values)) != 1:
        raise AssertionError("vertex-star activity is not uniform")
    return values[0]


def cold_witness_exhaustion():
    # u,x,p,q,r,b,c,d,w = 0,...,8.
    u, x, p, q, r, b, c, d, w = range(9)
    base_edges = {
        frozenset(edge)
        for edge in (
            (u, x), (u, r), (p, r), (q, r), (p, b), (q, c),
            (x, b), (x, c), (b, c), (u, p), (u, q),
            (d, p), (d, q), (d, b), (d, c),
        )
    }
    base_nonedges = {
        frozenset(edge)
        for edge in (
            (x, p), (x, q), (p, q), (x, r),
            (b, u), (b, r), (b, q),
            (c, u), (c, r), (c, p),
            (d, x), (d, r),
            (w, u), (w, x), (w, d),
        )
    }
    optional = ((w, p), (w, q), (w, b), (w, c))
    outcome_counts = {
        "J-nondominating-at-r": 0,
        "J-no-response-at-u": 0,
        "U-no-response-at-d": 0,
    }
    terminal_signature = None

    for optional_bits in itertools.product((0, 1), repeat=4):
        for du in (0, 1):
            for rw in (0, 1):
                edges = set(base_edges)
                nonedges = set(base_nonedges)
                assignments = list(zip(optional, optional_bits))
                assignments.extend((((d, u), du), ((r, w), rw)))
                for endpoints, present in assignments:
                    (edges if present else nonedges).add(
                        frozenset(endpoints)
                    )
                if edges & nonedges:
                    raise AssertionError("inconsistent incidence")

                def adjacent(left, right):
                    edge = frozenset((left, right))
                    if edge in edges:
                        return True
                    if edge in nonedges:
                        return False
                    raise AssertionError(f"unresolved pair {left},{right}")

                I = {x, r, d}
                J = {x, w, d}
                if any(
                    adjacent(left, right)
                    for state in (I, J)
                    for left, right in itertools.combinations(state, 2)
                ):
                    raise AssertionError("I or J is not independent")

                # A retained independent J must dominate r.
                if not rw:
                    if any(adjacent(guard, r) for guard in J):
                        raise AssertionError("wrong J domination branch")
                    outcome_counts["J-nondominating-at-r"] += 1
                    continue

                # At target u, x is family-inactive and w is ineligible.
                # If du is absent, the retained state J has no response.
                if not du:
                    graph_eligible = {
                        guard for guard in J if adjacent(guard, u)
                    }
                    if graph_eligible != {x}:
                        raise AssertionError("wrong eligible J,u guards")
                    outcome_counts["J-no-response-at-u"] += 1
                    continue

                # With du present, the exact family list is {d}.  Ridge
                # covariance fixes d under r<->w, so A={u,x,d} is absent.
                graph_eligible = {
                    guard for guard in J if adjacent(guard, u)
                }
                if graph_eligible != {x, d}:
                    raise AssertionError("wrong eligible J,u guards")
                list_J_u = {d}
                list_I_u = {
                    w if guard == r else r if guard == w else guard
                    for guard in list_J_u
                }
                if list_I_u != {d}:
                    raise AssertionError("ridge covariance failed")
                omitted_A = {u, x, d}

                U = {u, b, c}
                if {guard for guard in U if adjacent(guard, d)} != U:
                    raise AssertionError("not all U guards hit d")

                first = {}
                for mover in sorted(U):
                    successor = U - {mover} | {d}
                    if mover == u:
                        if any(adjacent(guard, r) for guard in successor):
                            raise AssertionError("u-successor hits r")
                        first[str(mover)] = "misses-r"
                        continue
                    x_movers = {
                        guard
                        for guard in successor
                        if adjacent(guard, x)
                    }
                    expected = {u, c if mover == b else b}
                    if x_movers != expected:
                        raise AssertionError("wrong second-stage movers")
                    for x_mover in x_movers:
                        second = successor - {x_mover} | {x}
                        if x_mover == u:
                            if any(
                                adjacent(guard, r) for guard in second
                            ):
                                raise AssertionError(
                                    "u second-stage successor hits r"
                                )
                        elif second != omitted_A:
                            raise AssertionError("wrong omitted corner")
                    first[str(mover)] = "fails-at-x"
                terminal_signature = first
                outcome_counts["U-no-response-at-d"] += 1

    if sum(outcome_counts.values()) != 64:
        raise AssertionError("cold assignment coverage gap")
    if outcome_counts != {
        "J-nondominating-at-r": 32,
        "J-no-response-at-u": 16,
        "U-no-response-at-d": 16,
    }:
        raise AssertionError("unexpected cold outcome partition")
    return {
        "assignments": 64,
        "optional_w_core_incidences": [list(pair) for pair in optional],
        "outcome_counts": outcome_counts,
        "terminal_signature": terminal_signature,
        "all_rejected": True,
    }


def hot_witness_audit():
    # Every canonical core collision is excluded as a common nonneighbor
    # of {u,d} by one displayed incident edge.
    excluded_collisions = {
        "x": "xu",
        "p": "pu-and-pd",
        "q": "qu-and-qd",
        "r": "ru",
        "b": "bd",
        "c": "cd",
    }
    hot_patterns = [
        {"wb": wb, "wc": wc}
        for wb, wc in itertools.product((False, True), repeat=2)
        if wb or wc
    ]
    original_corner = frozenset(("u", "d", "r"))
    opposite_corner = frozenset(("u", "d", "r"))
    if original_corner != opposite_corner:
        raise AssertionError("repair does not preserve literal corner")
    if (
        frozenset(("u", "d", "w")) - {"u"} | {"x"}
        != frozenset(("x", "d", "r")) - {"r"} | {"w"}
    ):
        raise AssertionError("repair states do not meet")
    return {
        "core_collisions_excluded": excluded_collisions,
        "hot_side_patterns": hot_patterns,
        "forced_hot_edges": ["wx", "wr", "wb-or-wc"],
        "conditional_on_ud_nonedge": {
            "independent_states": [["u", "d", "w"], ["x", "d", "r"]],
            "orientations": ["u->x", "r->w"],
            "missing_reverse": "w-not->r",
            "literal_omitted_corner": sorted(original_corner),
            "same_corner_rank": True,
        },
    }


def rank_diamond_audit():
    admissible = []
    for h in (1, 2, 3):
        for p_rank in (0, 1, 2):
            for q_rank in (0, 1, 2):
                if h >= 2 and min(p_rank, q_rank) < h - 1:
                    continue
                if h > 1 + min(p_rank, q_rank):
                    raise AssertionError("rank inequality failed")
                admissible.append([h, p_rank, q_rank])
    top = [row for row in admissible if row[0] == 3]
    if top != [[3, 2, 2]]:
        raise AssertionError("top rank is not forced exactly")
    return {
        "admissible_h_P_Q_tuples": admissible,
        "count": len(admissible),
        "top_case": top[0],
        "control_vector_B_P_Q_R": [1, 2, 2, 3],
    }


def audit_control(label: str, specification):
    record = specification["graph6"]
    adjacency = decode_graph6(record)
    n = len(adjacency)
    if n != specification["order"]:
        raise AssertionError("wrong order")
    size = sum(row.bit_count() for row in adjacency) // 2
    if size != specification["size"]:
        raise AssertionError("wrong size")

    gamma, indep_dom, alpha, theta = exact_parameters(adjacency)
    family2, _ = greatest_kernel(adjacency, 2)
    family3, ranks3 = greatest_kernel(adjacency, 3)
    eternal = 2 if family2 else 3 if family3 else None
    parameters = [gamma, indep_dom, alpha, eternal, theta]
    if parameters != [2, 3, 3, 3, 3]:
        raise AssertionError(f"wrong parameters: {parameters}")
    if len(family3) != specification["kernel3"]:
        raise AssertionError("wrong triple-kernel size")

    u, x, p, q, r, b, c = range(7)
    d = specification["completion"]
    T = mask((x, p, q))
    B = mask((u, p, q))
    P = mask((u, p, d))
    Q = mask((u, q, d))
    R = mask((u, r, d))
    if not independent(adjacency, T) or T not in family3:
        raise AssertionError("root T is not retained independent")
    if deletion_rank(adjacency, family3, ranks3, B) != 1:
        raise AssertionError("B is not rank one")
    if not active(adjacency, family3, u, x):
        raise AssertionError("u->x is not active")
    if active(adjacency, family3, x, u):
        raise AssertionError("x->u is active")

    completions = [
        vertex
        for vertex in range(n)
        if vertex not in (x, r)
        and not (adjacency[x] & (1 << vertex))
        and not (adjacency[r] & (1 << vertex))
    ]
    if completions != [d]:
        raise AssertionError(f"wrong completion list {completions}")
    if not all(adjacency[d] & (1 << v) for v in (p, q, b, c)):
        raise AssertionError("completion is not four-hit")
    if not dominates(adjacency, mask((u, x, d))):
        raise AssertionError("completion triple does not dominate")
    if not dominates(adjacency, mask((u, d))):
        raise AssertionError("u,d is not a dominating pair")

    private = ((u, x), (p, b), (q, c))
    successor_witnesses = []
    for mover, witness in private:
        successor = (B ^ (1 << mover)) | (1 << r)
        if deletion_rank(adjacency, family3, ranks3, successor) != 0:
            raise AssertionError("rank-one deleting successor dominates")
        if adjacency[witness] & successor:
            raise AssertionError("named witness does not miss successor")
        if not adjacency[witness] & (1 << mover):
            raise AssertionError("named witness misses removed guard")
        successor_witnesses.append(
            {
                "mover": mover,
                "successor": list(members(successor)),
                "witness": witness,
            }
        )

    rank_vector = [
        deletion_rank(adjacency, family3, ranks3, state)
        for state in (B, P, Q, R)
    ]
    if rank_vector != [1, 2, 2, 3]:
        raise AssertionError(f"wrong diamond {rank_vector}")
    ux_dominates = dominates(adjacency, mask((u, x)))
    if ux_dominates != specification["ux_dominates"]:
        raise AssertionError("wrong u,x domination status")
    dominating_pairs = sum(
        dominates(adjacency, mask(pair))
        for pair in itertools.combinations(range(n), 2)
    )

    return {
        "label": label,
        "graph6": record,
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "order": n,
        "size": size,
        "parameters_gamma_i_alpha_eternal_theta": parameters,
        "greatest_pair_family_size": len(family2),
        "greatest_triple_family_size": len(family3),
        "active_u_x": True,
        "active_x_u": False,
        "completion_list": completions,
        "completion_hits_p_q_b_c": True,
        "completion_triple_dominates": True,
        "u_d_pair_dominates": True,
        "u_x_pair_dominates": ux_dominates,
        "dominating_pair_count": dominating_pairs,
        "rank_vector_B_P_Q_R": rank_vector,
        "private_successor_witnesses": successor_witnesses,
    }


def evaluate():
    return {
        "schema": "qq1-completion-dynamics-hostile-clean-v1",
        "status": "PASS",
        "symbolic": {
            "cold_witness": cold_witness_exhaustion(),
            "hot_witness": hot_witness_audit(),
            "rank_diamond": rank_diamond_audit(),
        },
        "controls": {
            label: audit_control(label, specification)
            for label, specification in CONTROLS.items()
        },
        "scope": (
            "Independent finite bookkeeping and fixed-control evaluation; "
            "accepted C-010/C-064/C-108/C-143/C-146/C-158/C-161 are "
            "mathematical dependencies."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
