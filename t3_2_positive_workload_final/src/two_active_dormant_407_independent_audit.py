"""Independent adversarial audit of the frozen hard-interface candidate.

This module does not certify recurrence.  It independently replays two
bounded resistance regressions and records exact physical histories which
disprove Lemma 7.1 and equation (8.6) as they were stated in
``two_active_dormant_407_resolvent_theorem.md``.  The examples disprove the
candidate proof statements, not recurrence of the underlying network.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import permutations, product
import json

import two_active_dormant_407_certificate as dormant


VECTOR = {
    "0": (0, 0, 0),
    "U": (1, 0, 0),
    "2U": (2, 0, 0),
    "I": (0, 0, 1),
    "2I": (0, 0, 2),
    "UI": (1, 0, 1),
    "VI": (0, 1, 1),
}
INFINITY = 99


def _complete_edges(support: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
    return tuple(
        (source, target)
        for source in support
        for target in support
        if source != target
    )


def _directed_cycles(
    support: tuple[str, ...],
) -> tuple[tuple[tuple[str, str], ...], ...]:
    first = support[0]
    cycles = []
    for remainder in permutations(support[1:]):
        order = (first,) + remainder
        cycles.append(
            tuple(
                (order[index], order[(index + 1) % len(order)])
                for index in range(len(order))
            )
        )
    return tuple(cycles)


def _apply_word(
    word: tuple[tuple[str, str], ...],
) -> tuple[tuple[int, int, int], ...]:
    """Return states in ``(U, relative V, I)`` coordinates."""

    state = (0, 0, 0)
    states = [state]
    for source, target in word:
        source_vector = VECTOR[source]
        target_vector = VECTOR[target]
        if any(source_vector[index] > state[index] for index in (0, 2)):
            raise AssertionError(f"disabled audit edge {source}->{target}")
        state = tuple(
            state[index] + target_vector[index] - source_vector[index]
            for index in range(3)
        )
        if state[0] < 0 or state[2] < 0:
            raise AssertionError("audit word left the population lattice")
        states.append(state)
    return tuple(states)


def exact_counterexamples() -> dict[str, object]:
    """Freeze the exact strong-orientation histories found by the audit."""

    proper = ("U", "I", "VI")
    lower = ("0", "2U", "UI")
    matching_rows = tuple(
        row
        for row in dormant.generalized_normalized_rows()
        if tuple(row["proper"]) == proper
        and tuple(row["lower"]) == lower
        and row["spectator_cap"] == 0
    )
    assert len(matching_rows) == 2
    expected_row = {
        "pair": [["A", "B", "AC"], ["0", "2B", "AB"]],
        "weight": [0, 0, 1],
        "caps": [0, 0, 2],
        "spectator_cap": 0,
        "proper": ["U", "I", "VI"],
        "lower": ["0", "2U", "UI"],
    }
    assert expected_row in matching_rows
    row = expected_row

    complete_orientation = _complete_edges(proper) + _complete_edges(lower)
    assert all(
        edge in complete_orientation
        for edge in (
            ("0", "UI"),
            ("U", "VI"),
            ("I", "U"),
            ("0", "2U"),
            ("VI", "U"),
        )
    )

    history_word = (
        ("0", "UI"),
        ("U", "VI"),
        ("I", "U"),
        ("I", "U"),
    )
    history_states = _apply_word(history_word)
    assert history_states[-1] == (2, 1, 0)
    # Each additional 0->2U edge preserves I=0 and the old-V debt while
    # increasing U by two.  Hence historically consistent bases are
    # unbounded even inside the one-active (subpower-spectator) regime.

    service_word = (
        ("0", "2U"),
        ("0", "UI"),
        ("VI", "U"),
    )
    service_states = _apply_word(service_word)
    service_endpoint = service_states[-1]
    assert service_endpoint == (4, -1, 0)
    promoted_workload_change = service_endpoint[0] + 3 * service_endpoint[1]
    assert promoted_workload_change == 1

    return {
        "physical_row": row,
        "orientation": "complete digraph on each linkage (strong)",
        "lemma_7_1_history": {
            "word": [list(edge) for edge in history_word],
            "states_U_relativeV_I": [list(state) for state in history_states],
            "endpoint": list(history_states[-1]),
            "repeatable_neutral_edge": ["0", "2U"],
            "unbounded_historically_consistent_positive_debt_bases": True,
            "uniform_green_bound_as_stated": False,
        },
        "equation_8_6_history": {
            "word": [list(edge) for edge in service_word],
            "states_U_relativeV_I": [list(state) for state in service_states],
            "first_strict_old_V_service": True,
            "change_in_3V_plus_U": promoted_workload_change,
            "pathwise_promoted_workload_decrease": False,
        },
    }


def _minimum_resistances(
    nodes: frozenset[str],
    edges: tuple[tuple[str, str], ...],
    ratio: tuple[int, int],
    *,
    resistance_limit: int,
    population_box: int = 10,
) -> tuple[int, int]:
    """Bounded zero-one search for first down and positive base return."""

    p, q = ratio
    maximum = max(
        (name for name in nodes if name in {"0", "U", "2U"}),
        key=lambda name: VECTOR[name][0],
    )
    base_order = p * VECTOR[maximum][0]
    start = (0, 0, 0)
    queue = deque((start,))
    distance = {start: 0}
    down = INFINITY
    up = INFINITY

    while queue:
        state = queue.popleft()
        old = distance[state]
        delta_u, delta_v, cofactor = state
        for source, target in edges:
            source_u, source_v, source_i = VECTOR[source]
            target_u, target_v, target_i = VECTOR[target]
            if source_i > cofactor:
                continue
            source_order = p * source_u + q * source_v
            resistance = (
                base_order - source_order
                if cofactor == 0
                else q - source_order
            )
            if resistance < 0:
                raise AssertionError("negative source resistance")
            new_cost = old + resistance
            if new_cost > resistance_limit:
                continue
            endpoint = (
                delta_u + target_u - source_u,
                delta_v + target_v - source_v,
                cofactor + target_i - source_i,
            )
            if endpoint[2] < 0 or max(
                abs(endpoint[0]), abs(endpoint[1]), endpoint[2]
            ) > population_box:
                continue
            reward = p * endpoint[0] + q * endpoint[1]
            if reward < 0:
                down = min(down, new_cost)
                continue
            if endpoint[2] == 0 and reward > 0:
                up = min(up, new_cost)
                continue
            if new_cost < distance.get(endpoint, INFINITY):
                distance[endpoint] = new_cost
                if resistance:
                    queue.append(endpoint)
                else:
                    queue.appendleft(endpoint)
    return down, up


def resistance_regressions() -> dict[str, object]:
    """Replay maximal-edge and Hamilton-cycle resistance attacks."""

    maximal_histogram: Counter[tuple[int, int, int]] = Counter()
    for row in dormant.normalized_templates():
        proper = tuple(row["proper_support"])
        lower = tuple(row["other_support"])
        nodes = frozenset(proper) | frozenset(lower)
        edges = _complete_edges(proper) + _complete_edges(lower)
        claimed = dormant._resistance_class(row)
        down, up = _minimum_resistances(
            nodes,
            edges,
            tuple(row["normalized_ratio"]),
            resistance_limit=claimed + 1,
            population_box=16,
        )
        maximal_histogram[(claimed, down, up)] += 1
        assert down == claimed
        assert up > claimed

    cycle_histogram: Counter[tuple[int, int, int]] = Counter()
    orientation_pairs = 0
    for row in dormant.normalized_templates():
        proper = tuple(row["proper_support"])
        lower = tuple(row["other_support"])
        nodes = frozenset(proper) | frozenset(lower)
        claimed = dormant._resistance_class(row)
        for first, second in product(
            _directed_cycles(proper), _directed_cycles(lower)
        ):
            orientation_pairs += 1
            down, up = _minimum_resistances(
                nodes,
                first + second,
                tuple(row["normalized_ratio"]),
                resistance_limit=3,
                population_box=10,
            )
            cycle_histogram[(claimed, down, up)] += 1
            assert down == claimed
            assert up > claimed
    assert orientation_pairs == 1470

    def payload(counter: Counter[tuple[int, int, int]]) -> dict[str, int]:
        return {
            f"claimed={claimed},down={down},up={up}": count
            for (claimed, down, up), count in sorted(counter.items())
        }

    return {
        "maximal_complete_digraph_templates": 188,
        "maximal_complete_digraph_histogram": payload(maximal_histogram),
        "hamilton_cycle_orientation_pairs": orientation_pairs,
        "hamilton_cycle_histogram": payload(cycle_histogram),
        "bounded_counterexamples": 0,
        "scope": (
            "bounded path regression only; the arbitrary-orientation down "
            "existence still relies on the directed-cut proof"
        ),
    }


def audit() -> dict[str, object]:
    finite = dormant.certificate()
    assert finite["selected_incidences"]["total"] == 407
    assert finite["selected_pairs"]["total"] == 333
    assert finite["generalized_family_ii"]["incidences"] == 951
    assert finite["one_to_two_active_promotion_handoff"][
        "distinct_target_incidences"
    ] == 317
    assert not finite["analytic_theorem_independently_audited"]
    assert not finite["pair_level_recurrence_certified"]
    assert not finite["global_t3_2_certified"]

    return {
        "finite_selector_and_951_to_317_map_replay": "PASS",
        "graph_resistance_bounded_attack": resistance_regressions(),
        "exact_analytic_counterexamples": exact_counterexamples(),
        "ordered_remainder_finding": (
            "equation (6.3) claims endpoint-weighted control after only "
            "three insertions, but the displayed renewal identity controls "
            "only the unweighted mass of its unrestricted tail; use the "
            "unweighted boundary probability plus deterministic cutoff cost "
            "or prove a weighted tail kernel"
        ),
        "all_active_common_potential_scope": (
            "not overclaimed: the candidate explicitly leaves all-active "
            "and global composition open"
        ),
        "audit_verdict": "FAIL_AS_WRITTEN_REPAIR_OPEN",
        "network_recurrence_counterexample_found": False,
        "analytic_theorem_independently_audited": False,
        "pair_level_recurrence_certified": False,
        "global_t3_2_certified": False,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
