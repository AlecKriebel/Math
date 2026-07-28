#!/usr/bin/env python3
"""Clean-room review of the QQ1 anchor-auxiliary boundary control.

This verifier deliberately uses nauty ``showg`` as an external graph6
decoder, adjacency sets, frozenset guard configurations, and a separately
written fixed-point loop.  It imports neither the candidate verifier nor any
campaign evaluator or SAT encoder.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from collections import Counter
from pathlib import Path


LABELED_GRAPH6 = r"QslallyN\~Y^v^|^z~~V|ve~^}G"
CANONICAL_GRAPH6 = "QpMu]qnvvJb~Tz]mnx~nnZ~|~~W"

EXPECTED_DOMINATING_PAIRS = (
    (0, 14),
    (0, 17),
    (4, 14),
    (5, 10),
    (5, 12),
    (5, 14),
    (7, 12),
    (7, 14),
    (7, 15),
    (7, 17),
    (8, 10),
    (8, 12),
    (8, 13),
    (8, 14),
    (8, 17),
    (9, 11),
    (9, 14),
    (9, 15),
    (9, 16),
    (9, 17),
    (10, 11),
    (10, 12),
    (10, 13),
    (10, 14),
    (10, 15),
    (10, 16),
    (10, 17),
    (12, 15),
    (13, 16),
    (15, 16),
)

EXPECTED_PQ_AUXILIARY_WITNESSES = {
    "2,10": (1,),
    "2,11": (16,),
    "2,12": (6,),
    "2,13": (6, 17),
    "2,14": (17,),
    "2,15": (3, 17),
    "2,16": (11,),
    "2,17": (14,),
    "3,10": (1,),
    "3,11": (2, 5),
    "3,12": (2,),
    "3,13": (15,),
    "3,14": (2,),
    "3,15": (5,),
    "3,16": (2,),
    "3,17": (2, 15),
}


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_tool(executable: Path, arguments: tuple[str, ...], input_text: str) -> str:
    completed = subprocess.run(
        [str(executable.resolve()), *arguments],
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    demand(not completed.stderr, f"{executable.name} wrote stderr")
    return completed.stdout


def decode_with_showg(showg: Path, record: str) -> tuple[frozenset[int], ...]:
    """Decode through an independently pinned nauty executable."""

    words = run_tool(showg, ("-e", "-q", "-l0"), record + "\n").split()
    demand(len(words) >= 2, "showg emitted no graph")
    order, size = map(int, words[:2])
    payload = tuple(map(int, words[2:]))
    demand(len(payload) == 2 * size, "showg edge count disagrees with payload")
    neighborhoods = [set() for _ in range(order)]
    for left, right in zip(payload[::2], payload[1::2]):
        demand(0 <= left < right < order, "showg emitted a malformed edge")
        demand(right not in neighborhoods[left], "showg emitted a duplicate edge")
        neighborhoods[left].add(right)
        neighborhoods[right].add(left)
    demand(sum(map(len, neighborhoods)) == 2 * size, "degree sum mismatch")
    return tuple(frozenset(row) for row in neighborhoods)


def edge_rows(graph: tuple[frozenset[int], ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (left, right)
        for left in range(len(graph))
        for right in range(left + 1, len(graph))
        if right in graph[left]
    )


def joint_refinement(
    left_graph: tuple[frozenset[int], ...],
    right_graph: tuple[frozenset[int], ...],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Produce comparable 1-WL colors for two graphs."""

    demand(len(left_graph) == len(right_graph), "orders differ")
    left = tuple(len(row) for row in left_graph)
    right = tuple(len(row) for row in right_graph)
    while True:
        left_features = tuple(
            (left[vertex], tuple(sorted(left[neighbor] for neighbor in left_graph[vertex])))
            for vertex in range(len(left_graph))
        )
        right_features = tuple(
            (right[vertex], tuple(sorted(right[neighbor] for neighbor in right_graph[vertex])))
            for vertex in range(len(right_graph))
        )
        palette = {
            feature: color
            for color, feature in enumerate(sorted(set(left_features + right_features)))
        }
        refined_left = tuple(palette[item] for item in left_features)
        refined_right = tuple(palette[item] for item in right_features)
        if refined_left == left and refined_right == right:
            return left, right
        left, right = refined_left, refined_right


def exact_isomorphism(
    left_graph: tuple[frozenset[int], ...],
    right_graph: tuple[frozenset[int], ...],
) -> tuple[int, ...]:
    """Find and verify an exact isomorphism by color-guided backtracking."""

    left_colors, right_colors = joint_refinement(left_graph, right_graph)
    demand(Counter(left_colors) == Counter(right_colors), "refined color counts differ")
    order = len(left_graph)
    candidates = {
        vertex: tuple(
            image
            for image in range(order)
            if right_colors[image] == left_colors[vertex]
        )
        for vertex in range(order)
    }
    mapping: dict[int, int] = {}
    used: set[int] = set()

    def compatible(vertex: int, image: int) -> bool:
        return all(
            ((other in left_graph[vertex]) == (mapped in right_graph[image]))
            for other, mapped in mapping.items()
        )

    def search() -> bool:
        if len(mapping) == order:
            return True
        options = []
        for vertex in range(order):
            if vertex in mapping:
                continue
            available = tuple(
                image
                for image in candidates[vertex]
                if image not in used and compatible(vertex, image)
            )
            if not available:
                return False
            options.append((len(available), vertex, available))
        _, vertex, available = min(options)
        for image in available:
            mapping[vertex] = image
            used.add(image)
            if search():
                return True
            used.remove(image)
            del mapping[vertex]
        return False

    demand(search(), "decoded graph6 records are not isomorphic")
    result = tuple(mapping[vertex] for vertex in range(order))
    demand(len(set(result)) == order, "isomorphism is not bijective")
    demand(
        all(
            ((right in left_graph[left]) == (result[right] in right_graph[result[left]]))
            for left in range(order)
            for right in range(left + 1, order)
        ),
        "isomorphism fails an adjacency check",
    )
    return result


def configurations(order: int, size: int):
    for choice in itertools.combinations(range(order), size):
        yield frozenset(choice)


def is_independent(graph: tuple[frozenset[int], ...], state: frozenset[int]) -> bool:
    return all(right not in graph[left] for left, right in itertools.combinations(sorted(state), 2))


def is_dominating(graph: tuple[frozenset[int], ...], state: frozenset[int]) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(graph[guard])
    return len(covered) == len(graph)


def minimum_witness_size(order: int, predicate) -> int:
    for size in range(1, order + 1):
        for state in configurations(order, size):
            if predicate(state):
                return size
    raise AssertionError("no finite witness")


def maximum_independent_size(graph: tuple[frozenset[int], ...]) -> int:
    for size in range(len(graph), 0, -1):
        if any(is_independent(graph, state) for state in configurations(len(graph), size)):
            return size
    return 0


def eternal_kernel(
    graph: tuple[frozenset[int], ...], guard_count: int
) -> tuple[set[frozenset[int]], dict[frozenset[int], int], tuple[int, ...], int]:
    """Literal synchronous greatest-fixed-point deletion using frozensets."""

    order = len(graph)
    all_vertices = frozenset(range(order))
    surviving = {
        state
        for state in configurations(order, guard_count)
        if is_dominating(graph, state)
    }
    initial_size = len(surviving)
    deletion_rank: dict[frozenset[int], int] = {}
    wave_sizes: list[int] = []
    next_rank = 1
    while True:
        doomed: set[frozenset[int]] = set()
        for state in surviving:
            for attacked in all_vertices.difference(state):
                has_response = False
                for guard in state:
                    if attacked not in graph[guard]:
                        continue
                    successor = state.difference({guard}).union({attacked})
                    if successor in surviving:
                        has_response = True
                        break
                if not has_response:
                    doomed.add(state)
                    break
        if not doomed:
            return surviving, deletion_rank, tuple(wave_sizes), initial_size
        for state in doomed:
            deletion_rank[state] = next_rank
        surviving.difference_update(doomed)
        wave_sizes.append(len(doomed))
        next_rank += 1


def common_nonneighbors(
    graph: tuple[frozenset[int], ...], left: int, right: int
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(graph))
        if vertex not in (left, right)
        and vertex not in graph[left]
        and vertex not in graph[right]
    )


def missed_vertices(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(graph))
        if vertex not in state and all(vertex not in graph[guard] for guard in state)
    )


def activity_profile(
    graph: tuple[frozenset[int], ...],
    family: set[frozenset[int]],
    responder: int,
    attacked: int,
) -> tuple[dict[str, object], ...]:
    demand(attacked in graph[responder], "activity endpoints are not adjacent")
    profile = []
    for source in configurations(len(graph), 3):
        if responder not in source or attacked in source or not is_independent(graph, source):
            continue
        successor = source.difference({responder}).union({attacked})
        profile.append(
            {
                "source": tuple(sorted(source)),
                "source_retained": source in family,
                "successor": tuple(sorted(successor)),
                "successor_retained": successor in family,
            }
        )
    return tuple(profile)


def verify_partition(
    graph: tuple[frozenset[int], ...], partition: tuple[tuple[int, ...], ...]
) -> None:
    flattened = tuple(vertex for part in partition for vertex in part)
    demand(sorted(flattened) == list(range(len(graph))), "clique partition is not a partition")
    for part in partition:
        demand(
            all(right in graph[left] for left, right in itertools.combinations(part, 2)),
            f"part {part} is not a clique",
        )


def evaluate(showg: Path, labelg: Path) -> dict[str, object]:
    labeled = decode_with_showg(showg, LABELED_GRAPH6)
    canonical = decode_with_showg(showg, CANONICAL_GRAPH6)
    demand((len(labeled), len(edge_rows(labeled))) == (18, 114), "wrong labeled order/size")
    demand((len(canonical), len(edge_rows(canonical))) == (18, 114), "wrong canonical order/size")

    canonical_outputs = run_tool(
        labelg,
        ("-q",),
        LABELED_GRAPH6 + "\n" + CANONICAL_GRAPH6 + "\n",
    ).splitlines()
    demand(
        canonical_outputs == [CANONICAL_GRAPH6, CANONICAL_GRAPH6],
        "labelg canonicalization or idempotence mismatch",
    )
    isomorphism = exact_isomorphism(labeled, canonical)

    order = len(labeled)
    gamma = minimum_witness_size(order, lambda state: is_dominating(labeled, state))
    independent_domination = minimum_witness_size(
        order,
        lambda state: is_independent(labeled, state) and is_dominating(labeled, state),
    )
    alpha = maximum_independent_size(labeled)
    kernels = {
        count: eternal_kernel(labeled, count)
        for count in (1, 2, 3)
    }
    gamma_infinity = next(count for count in (1, 2, 3) if kernels[count][0])

    clique_partition = (
        (0, 3, 7, 10, 11, 12, 13, 14),
        (2, 4, 8, 9, 15),
        (1, 5, 6, 16, 17),
    )
    verify_partition(labeled, clique_partition)
    theta = 3
    demand(
        (gamma, independent_domination, alpha, gamma_infinity, theta)
        == (2, 3, 3, 3, 3),
        "parameter vector mismatch",
    )
    demand(alpha == theta, "alpha lower bound and clique-partition upper bound do not meet")

    family, ranks, waves, initial_triples = kernels[3]
    demand(len(family) == 473, "wrong greatest triple kernel size")
    demand(initial_triples == 642, "wrong number of dominating triples")
    demand(waves == (2, 8, 11, 28, 33, 18, 17, 34, 18), "wrong deletion waves")
    demand(len(kernels[1][0]) == len(kernels[2][0]) == 0, "one/two guard kernel survives")
    demand(kernels[1][3] == 0, "unexpected dominating singleton")
    demand(kernels[2][3] == 30 and kernels[2][2] == (30,), "wrong pair kernel")

    all_independent_triples = tuple(
        tuple(sorted(state))
        for state in configurations(order, 3)
        if is_independent(labeled, state)
    )
    demand(len(all_independent_triples) == 13, "wrong independent-triple count")
    demand(
        all(frozenset(state) in family for state in all_independent_triples),
        "a maximum independent triple is absent from the greatest family",
    )

    u, x, p, q, r, b, c, d, w, z = range(10)
    required_edges = (
        (u, x),
        (u, p),
        (u, q),
        (u, r),
        (u, d),
        (p, r),
        (q, r),
        (p, b),
        (q, c),
        (x, b),
        (x, c),
        (b, c),
        (d, p),
        (d, q),
        (d, b),
        (d, c),
        (w, x),
        (w, r),
        (z, d),
        (z, w),
    )
    required_nonedges = (
        (x, p),
        (x, q),
        (p, q),
        (x, r),
        (u, b),
        (b, r),
        (b, q),
        (u, c),
        (c, r),
        (c, p),
        (x, d),
        (r, d),
        (u, w),
        (d, w),
        (u, z),
        (x, z),
    )
    demand(all(right in labeled[left] for left, right in required_edges), "named edge absent")
    demand(
        all(right not in labeled[left] for left, right in required_nonedges),
        "named nonedge present",
    )

    retained_named = {
        "T": (x, p, q),
        "U": (u, b, c),
        "R": (r, b, c),
        "I": (x, r, d),
        "A": (u, x, d),
        "K": (u, d, w),
        "E": (x, d, w),
        "F": (r, d, w),
        "ux_ridge": (u, x, z),
        "cross_layer_bridge": (u, w, z),
        "outer_u_w_completion": (u, w, b),
        "outer_d_w_completion": (d, w, 16),
        "outer_bow_tie": (b, w, 16),
    }
    demand(
        all(frozenset(state) in family for state in retained_named.values()),
        "a named C166/C167 state is not retained",
    )

    blocker = frozenset((u, p, q))
    omitted_corner = frozenset((u, r, d))
    demand(is_dominating(labeled, blocker), "B is not dominating")
    demand(is_dominating(labeled, omitted_corner), "O is not dominating")
    demand(ranks.get(blocker) == 1, "B does not have deletion rank one")
    demand(ranks.get(omitted_corner) == 3, "O does not have deletion rank three")
    demand(blocker not in family and omitted_corner not in family, "omitted corner survives")

    blocker_successors = []
    for guard, expected_miss in ((u, x), (p, b), (q, c)):
        successor = blocker.difference({guard}).union({r})
        demand(r in labeled[guard], "rank-one mover lacks an edge")
        demand(
            missed_vertices(labeled, successor) == (expected_miss,),
            "rank-one successor has the wrong private witness",
        )
        blocker_successors.append(
            {
                "guard": guard,
                "successor": tuple(sorted(successor)),
                "missed": (expected_miss,),
            }
        )

    ux_activity = activity_profile(labeled, family, u, x)
    xu_activity = activity_profile(labeled, family, x, u)
    demand(ux_activity and all(row["source_retained"] for row in ux_activity), "bad u->x source")
    demand(all(row["successor_retained"] for row in ux_activity), "u->x is not active")
    demand(xu_activity and all(row["source_retained"] for row in xu_activity), "bad x->u source")
    demand(not any(row["successor_retained"] for row in xu_activity), "x->u is active")
    demand(
        any(
            row["source"] == (u, b, w)
            and row["successor"] == (x, b, w)
            and row["successor_retained"]
            for row in ux_activity
        ),
        "displayed u->x activity root is absent",
    )
    demand(
        any(
            row["source"] == (x, p, q)
            and row["successor"] == (u, p, q)
            and not row["successor_retained"]
            for row in xu_activity
        ),
        "displayed reverse endpoint is absent",
    )

    completion_data = {
        "C_xr": common_nonneighbors(labeled, x, r),
        "W_ux": common_nonneighbors(labeled, u, x),
        "W_ud": common_nonneighbors(labeled, u, d),
        "W_pw": common_nonneighbors(labeled, p, w),
        "C_uw": common_nonneighbors(labeled, u, w),
        "C_dw": common_nonneighbors(labeled, d, w),
    }
    demand(
        completion_data
        == {
            "C_xr": (d,),
            "W_ux": (z,),
            "W_ud": (w,),
            "W_pw": (16,),
            "C_uw": (b,),
            "C_dw": (16,),
        },
        "completion/witness sets are not the claimed singletons",
    )

    bridge = frozenset((u, w, z))
    demand(is_dominating(labeled, bridge) and bridge in family, "bridge is not retained")
    side_coverage = {
        side: tuple(vertex for vertex in (w, z) if side in labeled[vertex])
        for side in (b, c)
    }
    demand(side_coverage == {b: (z,), c: (w,)}, "bridge side coverage mismatch")

    cycle = (u, d, z, w, x)
    cycle_edges = tuple(
        tuple(sorted((cycle[index], cycle[(index + 1) % len(cycle)])))
        for index in range(len(cycle))
    )
    cycle_pairs = set(itertools.combinations(sorted(cycle), 2))
    demand(all(right in labeled[left] for left, right in cycle_edges), "C5 edge absent")
    demand(
        all(right not in labeled[left] for left, right in cycle_pairs.difference(cycle_edges)),
        "C5 has a chord",
    )

    outer_activity = {
        "b_to_d": activity_profile(labeled, family, b, d),
        "d_to_b": activity_profile(labeled, family, d, b),
        "sixteen_to_u": activity_profile(labeled, family, 16, u),
        "u_to_sixteen": activity_profile(labeled, family, u, 16),
    }
    demand(
        all(profile and all(row["successor_retained"] for row in profile) for profile in outer_activity.values()),
        "a singleton outer edge is not reciprocal",
    )

    auxiliary_witnesses = {
        f"{anchor},{vertex}": common_nonneighbors(labeled, anchor, vertex)
        for anchor in (p, q)
        for vertex in range(10, order)
    }
    demand(
        auxiliary_witnesses == EXPECTED_PQ_AUXILIARY_WITNESSES,
        "p/q auxiliary witness list mismatch",
    )

    dominating_pairs = tuple(
        tuple(sorted(state))
        for state in configurations(order, 2)
        if is_dominating(labeled, state)
    )
    demand(dominating_pairs == EXPECTED_DOMINATING_PAIRS, "dominating pair list mismatch")
    endpoint = frozenset((x, p, q))
    demand(all(endpoint.isdisjoint(pair) for pair in dominating_pairs), "a pair touches T")
    demand(sum(left < 10 <= right for left, right in dominating_pairs) == 20, "core/aux count")
    demand(sum(left >= 10 for left, _ in dominating_pairs) == 10, "aux/aux count")
    demand(all(right in labeled[left] for left, right in dominating_pairs), "independent pair dominates")

    witness_cycles = {
        "p:11->16": common_nonneighbors(labeled, p, 11),
        "p:16->11": common_nonneighbors(labeled, p, 16),
        "p:14->17": common_nonneighbors(labeled, p, 14),
        "p:17->14": common_nonneighbors(labeled, p, 17),
        "q:5->15": common_nonneighbors(labeled, q, 5),
        "q:15->5": common_nonneighbors(labeled, q, 15),
    }
    demand(
        witness_cycles
        == {
            "p:11->16": (16,),
            "p:16->11": (11,),
            "p:14->17": (17,),
            "p:17->14": (14,),
            "q:5->15": (15,),
            "q:15->5": (5,),
        },
        "listed witness-recycling cycle is not literal",
    )

    labeled_edges = edge_rows(labeled)
    edge_text = "".join(f"{left} {right}\n" for left, right in labeled_edges)
    demand(
        digest(LABELED_GRAPH6.encode("ascii"))
        == "99ddf436936152440c778efb79270a89e10feb8dd95d7033052e571a1bc3142c",
        "labeled graph6 digest mismatch",
    )
    demand(
        digest(edge_text.encode("ascii"))
        == "6a6256204cff1a80d67e16be7efa67377f02b5c9d7c6a924cf6bbfc4ec7b738e",
        "labeled edge-list digest mismatch",
    )

    return {
        "schema": "qq1-anchor-auxiliary-hostile-cleanroom-v1",
        "status": "PASS",
        "classification": "EXACT_GAMMA2_BOUNDARY_CONTROL",
        "graph6": {
            "labeled": LABELED_GRAPH6,
            "canonical": CANONICAL_GRAPH6,
            "labeled_sha256": digest(LABELED_GRAPH6.encode("ascii")),
            "canonical_sha256": digest(CANONICAL_GRAPH6.encode("ascii")),
            "labeled_edge_list_sha256": digest(edge_text.encode("ascii")),
            "order": order,
            "size": len(labeled_edges),
            "labeled_to_canonical_isomorphism": isomorphism,
            "canonicalization": canonical_outputs,
        },
        "parameters": {
            "gamma": gamma,
            "i": independent_domination,
            "alpha": alpha,
            "gamma_infinity": gamma_infinity,
            "theta": theta,
            "clique_partition": clique_partition,
            "independent_triples": all_independent_triples,
        },
        "kernels": {
            "initial_dominating_configuration_counts": {
                str(count): kernels[count][3] for count in (1, 2, 3)
            },
            "greatest_family_sizes": {
                str(count): len(kernels[count][0]) for count in (1, 2, 3)
            },
            "k3_deletion_waves": waves,
            "k3_rank_histogram": dict(sorted(Counter(ranks.values()).items())),
            "B_rank": ranks[blocker],
            "O_rank": ranks[omitted_corner],
            "B_attack_r_successors": blocker_successors,
        },
        "qq1": {
            "retained_named_states": retained_named,
            "completion_and_witness_sets": completion_data,
            "u_to_x_independent_root_profile": ux_activity,
            "x_to_u_independent_root_profile": xu_activity,
            "bridge_side_coverage": side_coverage,
            "induced_C5": cycle,
            "outer_reciprocal_activity": outer_activity,
        },
        "anchor_protection": {
            "T": tuple(sorted(endpoint)),
            "p_q_auxiliary_witnesses": auxiliary_witnesses,
            "dominating_pair_count": len(dominating_pairs),
            "dominating_pairs": dominating_pairs,
            "core_auxiliary_count": 20,
            "auxiliary_auxiliary_count": 10,
            "witness_recycling_cycles": witness_cycles,
        },
        "scope": {
            "refuted": (
                "The displayed local QQ1/C166/C167 obligations plus "
                "non-domination of every pair touching T do not imply gamma=3."
            ),
            "not_refuted": (
                "No statement assuming gamma=3 or full equality is refuted; "
                "the graph has gamma=2 and is not a conjecture counterexample."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--showg", required=True, type=Path)
    parser.add_argument("--labelg", required=True, type=Path)
    arguments = parser.parse_args()
    print(json.dumps(evaluate(arguments.showg, arguments.labelg), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
