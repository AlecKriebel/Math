#!/usr/bin/env python3
"""Clean-room replay for the full-list terminal-completion candidate.

This implementation imports no campaign code.  Graphs are adjacency sets,
guard configurations are frozensets, and all parameters and eternal kernels
are recomputed directly from the one-guard definition.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json


State = frozenset[int]
Graph = tuple[frozenset[int], ...]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def decode_graph6(record: str) -> Graph:
    """Decode the short (n <= 62) graph6 format without a library."""
    require(record and record[0] != "~", ("not short graph6", record))
    order = ord(record[0]) - 63
    require(0 <= order <= 62, ("bad order", order))
    needed = (order * (order - 1) // 2 + 5) // 6
    require(len(record) == 1 + needed, ("bad graph6 length", record))
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        require(0 <= value <= 63, ("bad graph6 character", character))
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    neighbors = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                neighbors[low].add(high)
                neighbors[high].add(low)
            cursor += 1
    require(not any(bits[cursor:]), ("nonzero graph6 padding", record))
    return tuple(frozenset(row) for row in neighbors)


def encode_graph6(graph: Graph) -> str:
    order = len(graph)
    require(order <= 62, "short graph6 only")
    bits = [
        int(high in graph[low])
        for high in range(1, order)
        for low in range(high)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = []
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = (value << 1) | bit
        payload.append(chr(63 + value))
    return chr(63 + order) + "".join(payload)


def edge_list(graph: Graph) -> list[list[int]]:
    return [
        [left, right]
        for left in range(len(graph))
        for right in range(left + 1, len(graph))
        if right in graph[left]
    ]


def edge_list_hash(graph: Graph) -> str:
    encoded = json.dumps(edge_list(graph), separators=(",", ":")).encode("ascii")
    return sha256(encoded).hexdigest()


def dominates(graph: Graph, state: State) -> bool:
    return all(vertex in state or bool(graph[vertex] & state) for vertex in range(len(graph)))


def independent(graph: Graph, state: State) -> bool:
    return all(not (graph[vertex] & (state - {vertex})) for vertex in state)


def all_states(order: int, size: int) -> tuple[State, ...]:
    return tuple(frozenset(group) for group in combinations(range(order), size))


def exact_gamma(graph: Graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, state) for state in all_states(len(graph), size)):
            return size
    raise AssertionError("gamma not found")


def exact_alpha(graph: Graph) -> int:
    for size in range(len(graph), 0, -1):
        if any(independent(graph, state) for state in all_states(len(graph), size)):
            return size
    return 0


def exact_independent_domination(graph: Graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(
            independent(graph, state) and dominates(graph, state)
            for state in all_states(len(graph), size)
        ):
            return size
    raise AssertionError("independent domination number not found")


def complement(graph: Graph) -> Graph:
    vertices = frozenset(range(len(graph)))
    return tuple(vertices - {vertex} - graph[vertex] for vertex in range(len(graph)))


def colorable(graph: Graph, number_of_colors: int) -> bool:
    """Exact DSATUR-style backtracking, with color-name symmetry breaking."""
    order = len(graph)
    colors = [-1] * order

    def search(colored: int, maximum_used: int) -> bool:
        if colored == order:
            return True
        uncolored = [vertex for vertex in range(order) if colors[vertex] < 0]
        vertex = max(
            uncolored,
            key=lambda item: (
                len({colors[nbr] for nbr in graph[item] if colors[nbr] >= 0}),
                len(graph[item]),
                -item,
            ),
        )
        forbidden = {colors[nbr] for nbr in graph[vertex] if colors[nbr] >= 0}
        upper = min(number_of_colors - 1, maximum_used + 1)
        for color in range(upper + 1):
            if color in forbidden:
                continue
            colors[vertex] = color
            if search(colored + 1, max(maximum_used, color)):
                return True
            colors[vertex] = -1
        return False

    return search(0, -1)


def exact_theta(graph: Graph) -> int:
    graph_complement = complement(graph)
    for colors in range(1, len(graph) + 1):
        if colorable(graph_complement, colors):
            return colors
    raise AssertionError("theta not found")


def one_guard_successors(graph: Graph, state: State, attacked: int) -> tuple[State, ...]:
    require(attacked not in state, ("occupied attack", state, attacked))
    return tuple(
        frozenset((state - {guard}) | {attacked})
        for guard in sorted(state)
        if attacked in graph[guard]
    )


def greatest_family(
    graph: Graph,
    guards: int,
    forbidden: frozenset[State] = frozenset(),
) -> tuple[frozenset[State], dict[State, int], tuple[int, ...]]:
    """Literal synchronous greatest-fixed-point deletion."""
    current = {
        state
        for state in all_states(len(graph), guards)
        if state not in forbidden and dominates(graph, state)
    }
    ranks: dict[State, int] = {}
    rounds: list[int] = []
    rank = 0
    while True:
        deleted = set()
        for state in current:
            for attacked in range(len(graph)):
                if attacked in state:
                    continue
                if not any(
                    successor in current
                    for successor in one_guard_successors(graph, state, attacked)
                ):
                    deleted.add(state)
                    break
        if not deleted:
            return frozenset(current), ranks, tuple(rounds)
        for state in deleted:
            ranks[state] = rank
        rounds.append(len(deleted))
        current.difference_update(deleted)
        rank += 1


def exact_eternal_number(graph: Graph) -> int:
    for guards in range(1, len(graph) + 1):
        family, _, _ = greatest_family(graph, guards)
        if family:
            return guards
    raise AssertionError("eternal domination number not found")


def exact_parameters(graph: Graph) -> dict[str, int]:
    return {
        "alpha": exact_alpha(graph),
        "gamma": exact_gamma(graph),
        "gamma_infinity": exact_eternal_number(graph),
        "i": exact_independent_domination(graph),
        "theta": exact_theta(graph),
    }


def dominating_pairs(graph: Graph) -> list[list[int]]:
    return [
        list(pair)
        for pair in combinations(range(len(graph)), 2)
        if dominates(graph, frozenset(pair))
    ]


def root_palette(graph: Graph, family: frozenset[State], root: State, vertex: int) -> tuple[int, ...]:
    return tuple(
        color
        for color in sorted(root)
        if vertex in graph[color] and frozenset((root - {color}) | {vertex}) in family
    )


def physical_link(graph: Graph, target: int) -> frozenset[int]:
    return frozenset(
        vertex
        for vertex in range(len(graph))
        if vertex != target and vertex not in graph[target]
    )


def color_ban(graph: Graph, root: State, target: int, color: int) -> frozenset[State]:
    return frozenset(
        frozenset((root - {color}) | {vertex})
        for vertex in physical_link(graph, target)
    )


def missed_vertices(graph: Graph, state: State) -> tuple[int, ...]:
    return tuple(vertex for vertex in range(len(graph)) if not dominates_vertex(graph, state, vertex))


def dominates_vertex(graph: Graph, state: State, vertex: int) -> bool:
    return vertex in state or bool(graph[vertex] & state)


def completion_set(graph: Graph, target: int, terminal: int) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(graph))
        if vertex not in (target, terminal)
        and vertex not in graph[target]
        and vertex not in graph[terminal]
    )


def retained_responses(
    graph: Graph,
    family: frozenset[State],
    state: State,
    attacked: int,
) -> tuple[tuple[int, State], ...]:
    return tuple(
        (guard, frozenset((state - {guard}) | {attacked}))
        for guard in sorted(state)
        if attacked in graph[guard]
        and frozenset((state - {guard}) | {attacked}) in family
    )


def deletion_witness(
    graph: Graph,
    allowed_initial: frozenset[State],
    attacked: int,
    state: State,
) -> bool:
    """Rank-zero witness: no physical successor remains in the initial universe."""
    return attacked not in state and not any(
        successor in allowed_initial
        for successor in one_guard_successors(graph, state, attacked)
    )


def audit_row(
    graph: Graph,
    greatest: frozenset[State],
    root: State,
    target: int,
    *,
    u: int,
    v: int,
    t: int,
    q: int,
    r: int,
    w: int,
    expected_completions: tuple[int, ...],
) -> dict[str, object]:
    require(root == frozenset((u, v, t)), ("bad root labels", u))
    require(independent(graph, root), ("root not independent", u))
    require(root in greatest, ("root absent", u))
    require(root_palette(graph, greatest, root, target) == tuple(sorted(root)), ("target not full", u))

    link = physical_link(graph, target)
    require(r in link and q not in link, ("bad corridor sides", u))
    require(len({u, v, t, q, r, target}) == 6, ("corridor collision", u))

    predecessor = frozenset((v, t, q))
    terminal = frozenset((v, t, r))
    secondary_root = frozenset((u, t, r))
    alternate = frozenset((t, q, r))
    witness_q = frozenset((w, t, q))
    witness_r = frozenset((w, t, r))
    require(predecessor in greatest and terminal in greatest, ("corridor states absent", u))
    require(secondary_root in greatest, ("secondary root state absent", u))
    require(r in graph[q], ("corridor move edge absent", u))
    require((q, terminal) in retained_responses(graph, greatest, predecessor, r), ("corridor response absent", u))
    require(v in root_palette(graph, greatest, root, r), ("secondary color absent", u))

    ban = color_ban(graph, root, target, u)
    restricted, ranks, rounds = greatest_family(graph, 3, ban)
    initial = frozenset(
        state
        for state in all_states(len(graph), 3)
        if state not in ban and dominates(graph, state)
    )
    require(ranks.get(predecessor) == 0, ("predecessor not rank zero", u, ranks.get(predecessor)))
    require(deletion_witness(graph, initial, r, predecessor), ("r not rank-zero witness", u))
    require(not dominates(graph, alternate), ("alternate dominates", u))
    require(missed_vertices(graph, alternate) == (w,), ("wrong missed witness", u))
    require(w not in root | {target, q, r}, ("witness collision", u))
    require(u in graph[w] and v in graph[w], ("positive witness edge absent", u))
    require(all(w not in graph[missed] for missed in (t, q, r)), ("witness nonedge absent", u))
    require(witness_q in greatest and witness_r in greatest, ("C168 witness state absent", u))
    require(
        retained_responses(graph, greatest, predecessor, w) == ((v, witness_q),),
        ("first witness response not unique", u),
    )
    require(
        retained_responses(graph, greatest, secondary_root, w) == ((u, witness_r),),
        ("second witness response not unique", u),
    )

    completions = completion_set(graph, target, r)
    require(completions == expected_completions, ("completion set mismatch", u, completions))
    require(completions, ("empty completion set", u))
    require(
        all(
            left == right or right in graph[left]
            for left in completions
            for right in completions
        ),
        ("completion set not a clique", u),
    )

    rows = []
    for d in completions:
        require(d not in root | {target, q, r}, ("completion collision", u, d))
        independent_completion = frozenset((target, r, d))
        first_branch = frozenset((d, t, r))
        second_branch = frozenset((v, d, r))
        require(independent(graph, independent_completion), ("completion not independent", u, d))
        require(independent_completion in greatest, ("independent completion absent", u, d))

        responses = retained_responses(graph, greatest, terminal, d)
        require(responses, ("empty completion split", u, d))
        require(all(guard in (v, t) for guard, _ in responses), ("illegal split guard", u, d))
        require(all(r not in graph[d] for _ in (0,)), ("terminal-completion edge present", u, d))
        first_retained = first_branch in greatest
        second_retained = second_branch in greatest
        require(first_retained or second_retained, ("no retained branch state", u, d))

        closed_hit = d == w or d in graph[w]
        if first_retained:
            require(closed_hit, ("first branch misses witness", u, d))
            physical = tuple(guard for guard in sorted(first_branch) if target in graph[guard])
            require(physical == (t,), ("first return not uniquely physical", u, d, physical))
            require(
                retained_responses(graph, greatest, first_branch, target)
                == ((t, independent_completion),),
                ("first return not uniquely retained", u, d),
            )

        rows.append(
            {
                "closed_witness_hit": closed_hit,
                "completion": d,
                "first_branch_edge": d in graph[v],
                "first_branch_retained": first_retained,
                "first_branch_rank": ranks.get(first_branch),
                "independent_completion_rank": ranks.get(independent_completion),
                "retained_completion_responses": [
                    [guard, sorted(successor)] for guard, successor in responses
                ],
                "second_branch_edge": d in graph[t],
                "second_branch_retained": second_retained,
                "unique_return_guard": t if first_retained else None,
            }
        )

    return {
        "completion_rows": rows,
        "completions": list(completions),
        "deletion_rounds": list(rounds),
        "predecessor_rank": ranks[predecessor],
        "q": q,
        "r": r,
        "restricted_kernel_size": len(restricted),
        "t": t,
        "terminal_palette": list(root_palette(graph, greatest, root, r)),
        "u": u,
        "v": v,
        "w": w,
    }


def graph_summary(record: str) -> tuple[Graph, frozenset[State], dict[str, object]]:
    graph = decode_graph6(record)
    require(encode_graph6(graph) == record, ("graph6 round trip", record))
    family, ranks, rounds = greatest_family(graph, 3)
    require(not ranks.keys() & family, ("ranked survivor", record))
    return graph, family, {
        "dominating_pairs": dominating_pairs(graph),
        "edge_list_sha256": edge_list_hash(graph),
        "greatest_family_size": len(family),
        "order": len(graph),
        "parameters": exact_parameters(graph),
        "size": len(edge_list(graph)),
        "unrestricted_deletion_rounds": list(rounds),
    }


def equality_control() -> dict[str, object]:
    record = "OYifur}UO]}iTij]tpo]v"
    graph, greatest, result = graph_summary(record)
    root = frozenset((0, 1, 10))
    target = 6
    rows = [
        audit_row(
            graph,
            greatest,
            root,
            target,
            u=0,
            v=1,
            t=10,
            q=14,
            r=11,
            w=8,
            expected_completions=(13,),
        ),
        audit_row(
            graph,
            greatest,
            root,
            target,
            u=10,
            v=0,
            t=1,
            q=12,
            r=5,
            w=4,
            expected_completions=(7, 9),
        ),
    ]
    require(result["parameters"] == {"alpha": 3, "gamma": 3, "gamma_infinity": 3, "i": 3, "theta": 3}, result)
    require(result["dominating_pairs"] == [], result["dominating_pairs"])
    require(
        {row["u"]: row["restricted_kernel_size"] for row in rows} == {0: 0, 10: 0},
        "empty equality kernels mismatch",
    )
    color_one, _, color_one_rounds = greatest_family(graph, 3, color_ban(graph, root, target, 1))
    require(len(color_one) == 150, ("safe equality kernel", len(color_one)))
    for row in rows:
        for completion in row["completion_rows"]:
            require(completion["first_branch_retained"], ("equality first branch", row["u"]))
            require(completion["second_branch_retained"], ("equality second branch", row["u"]))
            require(completion["first_branch_rank"] == 0, ("equality branch rank", row["u"]))
            require(completion["independent_completion_rank"] == 3, ("equality completion rank", row["u"]))
    result.update(
        {
            "graph6": record,
            "restricted_kernel_sizes": {"0": 0, "1": 150, "10": 0},
            "safe_color_deletion_rounds": list(color_one_rounds),
            "rows": rows,
        }
    )
    return result


def all_empty_gamma_two_control() -> dict[str, object]:
    record = "JEhbtj{rvu?"
    graph, greatest, result = graph_summary(record)
    base = decode_graph6("IEhbtj{ro")
    require(
        tuple(frozenset(neighbor for neighbor in graph[vertex] if neighbor < 10) for vertex in range(10))
        == base,
        "not the stated MMV-001 induced extension",
    )
    require(tuple(sorted(graph[10])) == (0, 1, 2, 3, 4, 6, 7), "wrong extension neighborhood")
    root = frozenset((0, 1, 2))
    target = 8
    specifications = (
        dict(u=0, v=1, t=2, q=4, r=9, w=3, expected_completions=(10,)),
        dict(u=1, v=2, t=0, q=3, r=6, w=5, expected_completions=(7,)),
        dict(u=2, v=0, t=1, q=5, r=7, w=4, expected_completions=(6,)),
    )
    rows = [audit_row(graph, greatest, root, target, **specification) for specification in specifications]
    require(result["parameters"] == {"alpha": 3, "gamma": 2, "gamma_infinity": 3, "i": 2, "theta": 4}, result)
    require(result["dominating_pairs"] == [[1, 10], [5, 10]], result["dominating_pairs"])
    require(all(row["restricted_kernel_size"] == 0 for row in rows), "kernel survives in all-empty control")
    for row in rows:
        completion = row["completion_rows"][0]
        require(completion["first_branch_retained"] and completion["second_branch_retained"], ("missing gamma-two branch", row["u"]))
        require(completion["first_branch_rank"] == 0, ("gamma-two branch rank", row["u"]))
        require(completion["independent_completion_rank"] == 3, ("gamma-two completion rank", row["u"]))
    result.update(
        {
            "graph6": record,
            "new_vertex_neighbors": sorted(graph[10]),
            "restricted_kernel_sizes": {"0": 0, "1": 0, "2": 0},
            "rows": rows,
        }
    )
    return result


def full_terminal_gamma_two_control() -> dict[str, object]:
    record = "HF~mdfj"
    graph, greatest, result = graph_summary(record)
    root = frozenset((0, 1, 2))
    target = 3
    require(root_palette(graph, greatest, root, target) == (0, 1, 2), "target not full")
    require(root_palette(graph, greatest, root, 5) == (0, 1, 2), "terminal not full")
    first = audit_row(
        graph,
        greatest,
        root,
        target,
        u=0,
        v=1,
        t=2,
        q=4,
        r=5,
        w=6,
        expected_completions=(8,),
    )
    second = audit_row(
        graph,
        greatest,
        root,
        target,
        u=0,
        v=2,
        t=1,
        q=4,
        r=5,
        w=7,
        expected_completions=(8,),
    )
    require(first["w"] != second["w"], "two witnesses collide")
    require(8 in graph[6] and 8 in graph[7], "completion does not meet both witnesses")
    for row in (first, second):
        completion = row["completion_rows"][0]
        require(completion["first_branch_retained"] and completion["second_branch_retained"], "overlap branch absent")
        require(completion["first_branch_rank"] == 0, "overlap branch rank")
        require(completion["independent_completion_rank"] is None, "completion should survive restricted kernel")
    kernels = {
        str(color): len(greatest_family(graph, 3, color_ban(graph, root, target, color))[0])
        for color in sorted(root)
    }
    require(kernels == {"0": 68, "1": 65, "2": 65}, kernels)
    require(result["parameters"] == {"alpha": 3, "gamma": 2, "gamma_infinity": 3, "i": 2, "theta": 3}, result)
    require(
        set(first["completions"]) <= (
            ({first["w"]} | graph[first["w"]]) | ({second["w"]} | graph[second["w"]])
        ),
        "two-witness cover absent",
    )
    result.update(
        {
            "first_secondary_row": first,
            "graph6": record,
            "restricted_kernel_sizes": kernels,
            "second_secondary_row": second,
            "terminal_palette": list(root_palette(graph, greatest, root, 5)),
        }
    )
    return result


def abstract_collision_audit() -> dict[str, object]:
    """Finite logic table for the only unresolved d=w collision."""
    rows = []
    failures = 0
    for collision in (False, True):
        for edge in (False, True):
            branch_dominates_witness = collision or edge
            conclusion_closed_hit = collision or edge
            if branch_dominates_witness and not conclusion_closed_hit:
                failures += 1
            rows.append(
                {
                    "branch_dominates_witness": branch_dominates_witness,
                    "d_equals_witness": collision,
                    "d_witness_edge": edge,
                    "closed_neighborhood_conclusion": conclusion_closed_hit,
                }
            )
    return {"failures": failures, "rows": rows}


def main() -> None:
    result = {
        "collision_truth_table": abstract_collision_audit(),
        "equality_rank_reversal": equality_control(),
        "gamma_two_all_completed": all_empty_gamma_two_control(),
        "gamma_two_full_terminal": full_terminal_gamma_two_control(),
        "model": "unoccupied attacks; one occupied guard moves along one G-edge; retained successors stay in the same family",
        "schema": "full-list-terminal-completion-hostile-replay-v1",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
