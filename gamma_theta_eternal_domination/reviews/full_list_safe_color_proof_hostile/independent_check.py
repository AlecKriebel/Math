#!/usr/bin/env python3
"""Clean-room checks for the full-list cumulative-kernel package.

No candidate transition or coloring code is imported.  Graphs and
configurations use packed integer masks, restricted kernels are rebuilt
from the one-guard definition, and list-coloring is checked both directly
and through a separately generated 2-CNF.
"""

from __future__ import annotations

import csv
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


def decode_graph6(record: str) -> tuple[int, ...]:
    values = [ord(character) - 63 for character in record.strip()]
    if not values or not 0 <= values[0] <= 62:
        raise ValueError("only short graph6 records are supported")
    order = values[0]
    bits: list[int] = []
    for value in values[1:]:
        if not 0 <= value <= 63:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = order * (order - 1) // 2
    if len(bits) < required:
        raise ValueError("truncated graph6 record")
    rows = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            cursor += 1
    return tuple(rows)


def masks_of_size(order: int, size: int) -> tuple[int, ...]:
    return tuple(
        sum(1 << vertex for vertex in state)
        for state in combinations(range(order), size)
    )


def vertices(mask: int) -> tuple[int, ...]:
    result = []
    while mask:
        bit = mask & -mask
        result.append(bit.bit_length() - 1)
        mask ^= bit
    return tuple(result)


def dominates(rows: tuple[int, ...], state: int) -> bool:
    covered = state
    for guard in vertices(state):
        covered |= rows[guard]
    return covered == (1 << len(rows)) - 1


def independent(rows: tuple[int, ...], state: int) -> bool:
    members = vertices(state)
    return all(not (rows[first] & (1 << second))
               for first, second in combinations(members, 2))


def greatest_kernel(
    rows: tuple[int, ...],
    size: int,
    banned: frozenset[int] = frozenset(),
) -> tuple[frozenset[int], dict[int, int], tuple[tuple[int, ...], ...]]:
    active = {
        state
        for state in masks_of_size(len(rows), size)
        if state not in banned and dominates(rows, state)
    }
    ranks: dict[int, int] = {}
    deletion_rounds: list[tuple[int, ...]] = []
    round_number = 0
    while True:
        doomed = []
        for state in sorted(active):
            for attacked in range(len(rows)):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                movable = state & rows[attacked]
                legal = False
                for guard in vertices(movable):
                    successor = state ^ (1 << guard) ^ attacked_bit
                    if successor in active:
                        legal = True
                        break
                if not legal:
                    doomed.append(state)
                    break
        if not doomed:
            return frozenset(active), ranks, tuple(deletion_rounds)
        deletion_rounds.append(tuple(doomed))
        for state in doomed:
            ranks[state] = round_number
        active.difference_update(doomed)
        round_number += 1


def complement_neighbors(rows: tuple[int, ...], target: int) -> int:
    full = (1 << len(rows)) - 1
    return full & ~(rows[target] | (1 << target))


def response_list(
    rows: tuple[int, ...],
    family: frozenset[int],
    root: int,
    target: int,
) -> int:
    result = 0
    for role in vertices(root):
        successor = root ^ (1 << role) ^ (1 << target)
        if rows[role] & (1 << target) and successor in family:
            result |= 1 << role
    return result


def exact_parameters(rows: tuple[int, ...]) -> dict[str, int]:
    order = len(rows)
    gamma = next(
        size
        for size in range(order + 1)
        if any(dominates(rows, state) for state in masks_of_size(order, size))
    )
    alpha = next(
        size
        for size in range(order, -1, -1)
        if any(independent(rows, state) for state in masks_of_size(order, size))
    )
    gamma_infinity = next(
        size
        for size in range(1, order + 1)
        if greatest_kernel(rows, size)[0]
    )

    cliques = []
    for size in range(1, order + 1):
        for state in masks_of_size(order, size):
            members = vertices(state)
            if all(rows[u] & (1 << v) for u, v in combinations(members, 2)):
                cliques.append(state)
    cover = {0: 0}
    full = (1 << order) - 1
    for remaining in range(1, full + 1):
        pivot = remaining & -remaining
        cover[remaining] = min(
            1 + cover[remaining ^ clique]
            for clique in cliques
            if clique & pivot and clique & remaining == clique
        )
    return {
        "gamma": gamma,
        "alpha": alpha,
        "gamma_infinity": gamma_infinity,
        "theta": cover[full],
    }


def ban_for(
    rows: tuple[int, ...],
    root: int,
    target: int,
    color: int,
) -> frozenset[int]:
    base = root ^ (1 << color)
    return frozenset(
        base | (1 << vertex)
        for vertex in vertices(complement_neighbors(rows, target))
    )


def full_core(
    rows: tuple[int, ...],
    family: frozenset[int],
    root: int,
) -> tuple[int, ...]:
    return tuple(
        target
        for target in range(len(rows))
        if not root & (1 << target)
        and response_list(rows, family, root, target) == root
    )


def proper_full_assignment(
    rows: tuple[int, ...],
    assignment: dict[int, int],
) -> bool:
    return all(
        assignment[first] != assignment[second]
        or bool(rows[first] & (1 << second))
        for first, second in combinations(sorted(assignment), 2)
    )


def cumulative_ban(
    rows: tuple[int, ...],
    root: int,
    assignment: dict[int, int],
) -> frozenset[int]:
    result = set()
    for target, color in assignment.items():
        result.update(ban_for(rows, root, target, color))
    return frozenset(result)


def domains_for(
    rows: tuple[int, ...],
    family: frozenset[int],
    root: int,
    assignment: dict[int, int],
) -> dict[int, tuple[int, ...]]:
    domains: dict[int, tuple[int, ...]] = {
        anchor: (anchor,) for anchor in vertices(root)
    }
    for vertex in range(len(rows)):
        if root & (1 << vertex):
            continue
        if vertex in assignment:
            domains[vertex] = (assignment[vertex],)
        else:
            domains[vertex] = vertices(
                response_list(rows, family, root, vertex)
            )
    return domains


def direct_domain_colorings(
    rows: tuple[int, ...],
    domains: dict[int, tuple[int, ...]],
) -> tuple[tuple[int, ...], ...]:
    order = len(rows)
    answers = []
    for choices in product(*(domains[vertex] for vertex in range(order))):
        if all(
            choices[first] != choices[second]
            or bool(rows[first] & (1 << second))
            for first, second in combinations(range(order), 2)
        ):
            answers.append(tuple(choices))
    return tuple(answers)


def two_cnf_count(
    rows: tuple[int, ...],
    domains: dict[int, tuple[int, ...]],
) -> tuple[int, int, int]:
    """Return variable count, clause count, satisfying assignment count."""
    if any(len(domain) not in (1, 2) for domain in domains.values()):
        raise AssertionError("2-CNF received a non-binary domain")
    variables = tuple(
        vertex for vertex in range(len(rows)) if len(domains[vertex]) == 2
    )
    variable_index = {vertex: index for index, vertex in enumerate(variables)}
    clauses: list[tuple[tuple[int, int], ...]] = []

    for first, second in combinations(range(len(rows)), 2):
        if rows[first] & (1 << second):
            continue
        common = set(domains[first]) & set(domains[second])
        for color in sorted(common):
            clause: list[tuple[int, int]] = []
            for endpoint in (first, second):
                domain = domains[endpoint]
                if len(domain) == 1:
                    # The endpoint is fixed to the forbidden color, so it
                    # contributes a false literal.
                    if domain[0] != color:
                        raise AssertionError("common-color bookkeeping error")
                    continue
                forbidden_choice = domain.index(color)
                clause.append(
                    (variable_index[endpoint], 1 - forbidden_choice)
                )
            clauses.append(tuple(clause))

    satisfying = 0
    for values in product((0, 1), repeat=len(variables)):
        if all(any(values[var] == required for var, required in clause)
               for clause in clauses):
            satisfying += 1
    return len(variables), len(clauses), satisfying


def verify_fiber_family(
    rows: tuple[int, ...],
    coloring: tuple[int, ...],
    root_colors: tuple[int, ...],
    banned: frozenset[int],
    kernel: frozenset[int],
) -> dict[str, int]:
    fibers = {
        color: tuple(
            vertex for vertex, assigned in enumerate(coloring)
            if assigned == color
        )
        for color in root_colors
    }
    if any(not fiber for fiber in fibers.values()):
        raise AssertionError("empty color fiber")
    family = frozenset(
        sum(1 << vertex for vertex in selected)
        for selected in product(*(fibers[color] for color in root_colors))
    )
    if family & banned:
        raise AssertionError("clique-fiber family enters cumulative ban")
    if not family <= kernel:
        raise AssertionError("clique-fiber family is not in greatest kernel")
    for state in family:
        if not dominates(rows, state):
            raise AssertionError("fiber transversal does not dominate")
        for attacked in range(len(rows)):
            attacked_bit = 1 << attacked
            if state & attacked_bit:
                continue
            attacked_color = coloring[attacked]
            guard = next(
                member
                for member in vertices(state)
                if coloring[member] == attacked_color
            )
            if not rows[guard] & attacked_bit:
                raise AssertionError("same-fiber move is not a G-edge")
            successor = state ^ (1 << guard) ^ attacked_bit
            if successor not in family:
                raise AssertionError("fiber family is not closed")
    return {
        "color_class_sizes_product": len(family),
        "family_states": len(family),
    }


def cumulative_profile(
    record: str,
    root_vertices: tuple[int, int, int],
) -> dict[str, object]:
    rows = decode_graph6(record)
    root = sum(1 << vertex for vertex in root_vertices)
    greatest = greatest_kernel(rows, 3)[0]
    if root not in greatest or not independent(rows, root):
        raise AssertionError("control root is not an independent retained triple")
    core = full_core(rows, greatest, root)
    profiles = []
    for colors in product(vertices(root), repeat=len(core)):
        assignment = dict(zip(core, colors))
        if not proper_full_assignment(rows, assignment):
            continue
        banned = cumulative_ban(rows, root, assignment)
        kernel = greatest_kernel(rows, 3, banned)[0]
        direct_count = 0
        cnf_count = 0
        variables = 0
        clauses = 0
        fiber_check = None
        if kernel:
            # Proposition 4.1, checked for every full target at once.
            for target, color in assignment.items():
                if not response_list(rows, kernel, root, target) & (1 << color):
                    raise AssertionError("selected full response was not forced")
                for neighbor in vertices(complement_neighbors(rows, target)):
                    if response_list(rows, kernel, root, neighbor) & (1 << color):
                        raise AssertionError("banned color reappeared on link")

            domains = domains_for(rows, kernel, root, assignment)
            if any(not domain for domain in domains.values()):
                raise AssertionError("nonempty kernel gave an empty root list")
            if any(len(domain) > 2 for vertex, domain in domains.items()
                   if vertex not in core and not root & (1 << vertex)):
                raise AssertionError("non-full residual domain exceeds two")
            colorings = direct_domain_colorings(rows, domains)
            direct_count = len(colorings)
            variables, clauses, cnf_count = two_cnf_count(rows, domains)
            if cnf_count != direct_count:
                raise AssertionError("direct list coloring and 2-CNF disagree")
            if colorings:
                fiber_check = verify_fiber_family(
                    rows,
                    colorings[0],
                    vertices(root),
                    banned,
                    kernel,
                )
        profiles.append(
            {
                "assignment": {
                    str(target): color
                    for target, color in sorted(assignment.items())
                },
                "kernel_states": len(kernel),
                "compatible_colorings": direct_count,
                "two_cnf_satisfying_assignments": cnf_count,
                "two_cnf_variables": variables,
                "two_cnf_clauses": clauses,
                "fiber_check": fiber_check,
            }
        )
    return {
        "graph6": record,
        "parameters": exact_parameters(rows),
        "root": list(root_vertices),
        "full_core": list(core),
        "proper_assignment_profiles": profiles,
    }


def individual_profile(
    record: str,
    root_vertices: tuple[int, int, int],
    target: int,
    color: int,
) -> dict[str, object]:
    rows = decode_graph6(record)
    root = sum(1 << vertex for vertex in root_vertices)
    banned = ban_for(rows, root, target, color)
    kernel = greatest_kernel(rows, 3, banned)[0]
    assignment = {target: color}
    domains = domains_for(rows, kernel, root, assignment) if kernel else {}
    colorings = direct_domain_colorings(rows, domains) if kernel else ()
    successor = root ^ (1 << color) ^ (1 << target)
    return {
        "graph6": record,
        "root": list(root_vertices),
        "target": target,
        "color": color,
        "kernel_states": len(kernel),
        "forced_successor_survives": successor in kernel,
        "compatible_colorings_with_target_fixed": len(colorings),
    }


def audit_named_controls() -> dict[str, object]:
    equality = cumulative_profile(r"Ksv`f\knJVis", (1, 2, 3))
    mmv001 = cumulative_profile("IEhbtj{ro", (0, 1, 2))
    mmv021 = cumulative_profile("JEhbtj{rv~?", (0, 1, 2))
    individual = individual_profile(
        "JEhbtj{rv~?", (0, 1, 2), 10, 2
    )

    compact_equality = [
        (
            row["assignment"],
            row["kernel_states"],
            row["compatible_colorings"],
        )
        for row in equality["proper_assignment_profiles"]
    ]
    if equality["parameters"] != {
        "gamma": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    } or equality["full_core"] != [0] or compact_equality != [
        ({"0": 1}, 0, 0),
        ({"0": 2}, 0, 0),
        ({"0": 3}, 64, 1),
    ]:
        raise AssertionError(("equality control mismatch", equality))

    if mmv001["parameters"] != {
        "gamma": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 4,
    } or mmv001["full_core"] != [8] or any(
        row["kernel_states"] for row in mmv001["proper_assignment_profiles"]
    ):
        raise AssertionError(("MMV-001 mismatch", mmv001))

    if mmv021["parameters"] != {
        "gamma": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 4,
    } or mmv021["full_core"] != [8, 10] or len(
        mmv021["proper_assignment_profiles"]
    ) != 9 or any(
        row["kernel_states"] for row in mmv021["proper_assignment_profiles"]
    ):
        raise AssertionError(("MMV-021 cumulative mismatch", mmv021))

    if individual != {
        "graph6": "JEhbtj{rv~?",
        "root": [0, 1, 2],
        "target": 10,
        "color": 2,
        "kernel_states": 128,
        "forced_successor_survives": True,
        "compatible_colorings_with_target_fixed": 0,
    }:
        raise AssertionError(("MMV-021 individual mismatch", individual))

    return {
        "equality_control": equality,
        "mmv001_all_empty": mmv001,
        "mmv021_joint_core": mmv021,
        "mmv021_individual_safe_target": individual,
    }


def audit_two_cnf_exactness() -> dict[str, int]:
    """Exhaust all three-vertex graphs and all one/two-color domains."""
    possible_domains = (
        (0,), (1,), (2,),
        (0, 1), (0, 2), (1, 2),
    )
    checked = 0
    satisfiable = 0
    for edge_mask in range(1 << 3):
        rows = [0, 0, 0]
        for bit, (first, second) in enumerate(combinations(range(3), 2)):
            if edge_mask & (1 << bit):
                rows[first] |= 1 << second
                rows[second] |= 1 << first
        packed_rows = tuple(rows)
        for selected in product(possible_domains, repeat=3):
            domains = {vertex: selected[vertex] for vertex in range(3)}
            direct = direct_domain_colorings(packed_rows, domains)
            _, _, cnf_count = two_cnf_count(packed_rows, domains)
            if len(direct) != cnf_count:
                raise AssertionError(
                    ("2-CNF is not exact", edge_mask, domains, len(direct), cnf_count)
                )
            checked += 1
            satisfiable += bool(direct)
    if checked != 8 * 6 ** 3:
        raise AssertionError(checked)
    return {
        "graph_domain_instances": checked,
        "satisfiable_instances": satisfiable,
        "mismatches": 0,
    }


def audit_catalog(campaign: Path) -> dict[str, int]:
    with (campaign / "instances/mmv2022_table9.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        records = list(csv.DictReader(stream))
    totals = {
        "graphs": 0,
        "full_incidences": 0,
        "color_tests": 0,
        "unsafe_colors": 0,
        "nonempty_kernel_without_forced_start": 0,
    }
    for record in records:
        rows = decode_graph6(record["graph6"])
        if exact_parameters(rows)["alpha"] != 3:
            continue
        totals["graphs"] += 1
        greatest = greatest_kernel(rows, 3)[0]
        for root in masks_of_size(len(rows), 3):
            if not independent(rows, root):
                continue
            for target in range(len(rows)):
                if root & (1 << target):
                    continue
                if response_list(rows, greatest, root, target) != root:
                    continue
                totals["full_incidences"] += 1
                for color in vertices(root):
                    totals["color_tests"] += 1
                    banned = ban_for(rows, root, target, color)
                    kernel = greatest_kernel(rows, 3, banned)[0]
                    start = root ^ (1 << color) ^ (1 << target)
                    if start in kernel:
                        continue
                    totals["unsafe_colors"] += 1
                    if kernel:
                        totals["nonempty_kernel_without_forced_start"] += 1
    if totals != {
        "graphs": 55,
        "full_incidences": 581,
        "color_tests": 1743,
        "unsafe_colors": 1688,
        "nonempty_kernel_without_forced_start": 0,
    }:
        raise AssertionError(("catalog totals mismatch", totals))
    return totals


def retained_successors(
    rows: tuple[int, ...],
    family: frozenset[int],
    state: int,
    attacked: int,
) -> tuple[int, ...]:
    attacked_bit = 1 << attacked
    if state & attacked_bit:
        return ()
    result = []
    for guard in vertices(state & rows[attacked]):
        successor = state ^ (1 << guard) ^ attacked_bit
        if successor in family:
            result.append(successor)
    return tuple(sorted(result))


def deletion_witness_attacks(
    rows: tuple[int, ...],
    state: int,
    banned: frozenset[int],
    ranks: dict[int, int],
) -> tuple[int, ...]:
    current = ranks[state]
    result = []
    for attacked in range(len(rows)):
        if state & (1 << attacked):
            continue
        allowed_successors = []
        for guard in vertices(state & rows[attacked]):
            successor = state ^ (1 << guard) ^ (1 << attacked)
            if successor in banned or not dominates(rows, successor):
                continue
            allowed_successors.append(successor)
        if all(
            successor in ranks and ranks[successor] < current
            for successor in allowed_successors
        ):
            result.append(attacked)
    return tuple(result)


def descent_trace(
    rows: tuple[int, ...],
    greatest: frozenset[int],
    start: int,
    banned: frozenset[int],
    ranks: dict[int, int],
) -> tuple[int, ...]:
    trace = [start]
    current = start
    while current not in banned:
        if current not in ranks:
            raise AssertionError("nonbanned trace state has no finite rank")
        progressed = False
        for attacked in deletion_witness_attacks(rows, current, banned, ranks):
            successors = retained_successors(rows, greatest, current, attacked)
            if not successors:
                raise AssertionError("greatest family failed closure")
            for successor in successors:
                if successor in banned or (
                    successor in ranks
                    and ranks[successor] < ranks[current]
                ):
                    trace.append(successor)
                    current = successor
                    progressed = True
                    break
            if progressed:
                break
        if not progressed:
            raise AssertionError("rank descent could not progress")
    return tuple(trace)


def audit_rank_descent_and_gates() -> dict[str, object]:
    rows = decode_graph6(r"Ksv`f\knJVis")
    root = sum(1 << vertex for vertex in (1, 2, 3))
    x = 0
    greatest = greatest_kernel(rows, 3)[0]
    by_color = {}
    for color in (1, 2):
        base = root ^ (1 << color)
        banned = ban_for(rows, root, x, color)
        kernel, ranks, rounds = greatest_kernel(rows, 3, banned)
        if kernel:
            raise AssertionError("expected annihilated equality-control kernel")

        traces = {
            state: descent_trace(rows, greatest, state, banned, ranks)
            for state in greatest - banned
        }
        for trace in traces.values():
            nonterminal = trace[:-1]
            if any(state not in greatest - banned for state in nonterminal):
                raise AssertionError("descent leaves retained allowed states")
            if trace[-1] not in greatest & banned:
                raise AssertionError("descent does not terminate in retained ban")
            trace_ranks = [ranks[state] for state in nonterminal]
            if any(left <= right
                   for left, right in zip(trace_ranks, trace_ranks[1:])):
                raise AssertionError("descent ranks do not strictly decrease")

        entries = []
        root_entry_non_singletons = []
        for predecessor in greatest - banned:
            for attacked in range(len(rows)):
                for successor in retained_successors(
                    rows, greatest, predecessor, attacked
                ):
                    if successor not in banned:
                        continue
                    added = successor & ~predecessor
                    removed = predecessor & ~successor
                    if added.bit_count() != 1 or removed.bit_count() != 1:
                        raise AssertionError("not a one-guard transition")
                    if added != 1 << attacked:
                        raise AssertionError("attacked vertex not inserted")
                    b_mask = successor & ~base
                    if b_mask.bit_count() != 1:
                        raise AssertionError("banned state has wrong shape")
                    b = b_mask.bit_length() - 1
                    q = removed.bit_length() - 1

                    if attacked == b:
                        gate = "corridor"
                        if predecessor != base | (1 << q):
                            raise AssertionError("corridor predecessor shape")
                        if complement_neighbors(rows, x) & (1 << q):
                            raise AssertionError("corridor mover lies in Bx")
                        if q == color:
                            gate = "direct_root"
                            full_list = vertices(
                                response_list(rows, greatest, root, b)
                            )
                            if len(full_list) > 1:
                                root_entry_non_singletons.append(
                                    {
                                        "b": b,
                                        "response_list": list(full_list),
                                    }
                                )
                        else:
                            if q in vertices(root) or q == x:
                                raise AssertionError("nonroot corridor collision")
                            quartet = (x, color, q, b)
                            missing = []
                            for first, second in combinations(quartet, 2):
                                if not rows[first] & (1 << second):
                                    missing.append(tuple(sorted((first, second))))
                            if missing != [tuple(sorted((x, b)))]:
                                raise AssertionError(("diamond failure", quartet, missing))
                    elif base & (1 << attacked):
                        gate = "anchor_restoration"
                        remaining_anchor = base ^ (1 << attacked)
                        if predecessor != remaining_anchor | (1 << b) | (1 << q):
                            raise AssertionError("anchor-restoration shape")
                    else:
                        raise AssertionError("unclassified terminal gate")
                    entries.append(
                        {
                            "predecessor": list(vertices(predecessor)),
                            "attack": attacked,
                            "mover": q,
                            "successor": list(vertices(successor)),
                            "gate": gate,
                        }
                    )
        if not entries:
            raise AssertionError("no terminal entries found")
        by_color[str(color)] = {
            "restricted_initial_states": sum(len(row) for row in rounds),
            "deletion_round_sizes": [len(row) for row in rounds],
            "descent_start_count": len(traces),
            "terminal_entry_count": len(entries),
            "gate_counts": {
                gate: sum(entry["gate"] == gate for entry in entries)
                for gate in ("direct_root", "corridor", "anchor_restoration")
            },
            "root_entries_with_nonsingleton_lists": root_entry_non_singletons,
        }
    return by_color


def audit_anchor_in_link_clarification() -> dict[str, object]:
    rows = decode_graph6(r"Ksv`f\knJVis")
    root = sum(1 << vertex for vertex in (1, 2, 3))
    for target in range(len(rows)):
        if root & (1 << target):
            continue
        link = complement_neighbors(rows, target)
        for color in vertices(root):
            kernel = greatest_kernel(
                rows, 3, ban_for(rows, root, target, color)
            )[0]
            other_anchor_link = link & root & ~(1 << color)
            if kernel and other_anchor_link:
                if link & (1 << color):
                    raise AssertionError("nonempty kernel while root itself is banned")
                if not response_list(rows, kernel, root, target) & (1 << color):
                    raise AssertionError("ban-avoidance forcing failed")
                return {
                    "target": target,
                    "color": color,
                    "anchor_vertices_in_Bx": list(vertices(other_anchor_link)),
                    "kernel_states": len(kernel),
                    "forced_response_list": list(
                        vertices(response_list(rows, kernel, root, target))
                    ),
                    "interpretation": (
                        "Bx may contain anchors in S-u; revised proof puts "
                        "them directly in the projection base."
                    ),
                }
    raise AssertionError("no anchor-in-link control found")


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_hashes(campaign: Path) -> dict[str, str]:
    pinned = {
        "candidate_NOTE.md": (
            campaign / "math/working/full_list_safe_color_proof/NOTE.md",
            "a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d",
        ),
        "candidate_MANIFEST.json": (
            campaign / "math/working/full_list_safe_color_proof/MANIFEST.json",
            "8a09e4c9c932caeebea257f7ac8c3e9ece51d1a4dbd444cfa562a55dc86de3f4",
        ),
        "candidate_verify_controls.py": (
            campaign / "math/working/full_list_safe_color_proof/verify_controls.py",
            "34f3d2cfe9026af493d943773ea8c0c5f729c20d90c0214555e330d8cea54811",
        ),
        "candidate_expected_result.json": (
            campaign / "math/working/full_list_safe_color_proof/expected_result.json",
            "2e413f103f73d5da4afcf0960b15a384bff6ae2e3c1699d2df1be1f2e41e0b0b",
        ),
        "C010_maximum_independent_states.md": (
            campaign / "math/lemmas/maximum_independent_states.md",
            "08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e",
        ),
        "C006_reductions.md": (
            campaign / "math/reductions.md",
            "d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13",
        ),
        "C063_k3_cross_state_attack.md": (
            campaign / "math/working/k3_cross_state_attack.md",
            "3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68",
        ),
        "C063_hostile_REVIEW.md": (
            campaign / "reviews/frozen_color_projection_hostile/REVIEW.md",
            "cc8273ea5737562502af4991a5933e38b4eeb15de29c811bd1a3c4bb4fd7580e",
        ),
    }
    result = {name: hash_file(path) for name, (path, _) in pinned.items()}
    for name, (_, expected) in pinned.items():
        if result[name] != expected:
            raise AssertionError(("pinned input changed", name, result[name], expected))
    return result


def main() -> None:
    campaign = Path(__file__).resolve().parents[2]
    controls = audit_named_controls()
    two_cnf = audit_two_cnf_exactness()
    catalog = audit_catalog(campaign)
    ranks = audit_rank_descent_and_gates()
    anchor_case = audit_anchor_in_link_clarification()
    result = {
        "schema": "full-list-safe-color-hostile-clean-room-v1",
        "model": (
            "unoccupied attacks; exactly one occupied guard moves along "
            "one G-edge; successor remains in the same family"
        ),
        "named_controls": controls,
        "two_cnf_exactness": two_cnf,
        "catalog": catalog,
        "rank_descent_and_terminal_gates": ranks,
        "anchor_in_link_control": anchor_case,
        "candidate_replay_relation": (
            "verify_controls output is semantically equal after JSON "
            "normalization to expected_result.json; byte formatting differs"
        ),
        "hashes": audit_hashes(campaign),
        "scope": (
            "reductions only; no safe-color existence, no guaranteed "
            "satisfiable residual 2-CNF, no complete k=3 theorem"
        ),
        "verdict": "PASS_REVISED_BYTES",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
