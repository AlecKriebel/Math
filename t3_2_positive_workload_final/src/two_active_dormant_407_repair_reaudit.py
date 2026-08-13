"""Adversarial re-audit of the repaired hard-interface candidate.

The repaired start-weighted Green estimate is compatible with the finite
support geometry, but the bounded entropy-coboundary step is false when the
actual service endpoint is retained.  This module freezes an exact strong
orientation and physical history witnessing that failure.  It makes no
claim about recurrence of the network.
"""

from __future__ import annotations

from collections import Counter
import json
from math import log

import two_active_dormant_407_certificate as dormant


VECTOR = {
    "0": (0, 0, 0),
    "U": (1, 0, 0),
    "2U": (2, 0, 0),
    "I": (0, 1, 0),
    "2I": (0, 2, 0),
    "UI": (1, 1, 0),
    "VI": (0, 1, 1),
}


def _apply_word(
    initial: tuple[int, int, int],
    word: tuple[tuple[str, str], ...],
) -> tuple[tuple[int, int, int], ...]:
    """Apply a word in coordinates ``(U, I, relative V)``."""

    state = initial
    states = [state]
    for source, target in word:
        y = VECTOR[source]
        z = VECTOR[target]
        if y[0] > state[0] or y[1] > state[1]:
            raise AssertionError(f"disabled edge {source}->{target}")
        state = tuple(
            state[index] + z[index] - y[index] for index in range(3)
        )
        if state[0] < 0 or state[1] < 0:
            raise AssertionError("word left the population lattice")
        states.append(state)
    return tuple(states)


def _is_strong(
    support: tuple[str, ...], edges: tuple[tuple[str, str], ...]
) -> bool:
    adjacency = {node: [] for node in support}
    for source, target in edges:
        adjacency[source].append(target)
    for start in support:
        reached = {start}
        frontier = [start]
        while frontier:
            source = frontier.pop()
            for target in adjacency[source]:
                if target not in reached:
                    reached.add(target)
                    frontier.append(target)
        if reached != set(support):
            return False
    return True


def actual_service_endpoint_counterexample() -> dict[str, object]:
    """Disprove equations (7.12)--(7.14) on one exact template."""

    proper = ("2U", "VI")
    lower = ("0", "I", "2I", "UI")
    matching = tuple(
        row
        for row in dormant.generalized_normalized_rows()
        if tuple(row["proper"]) == proper
        and tuple(row["lower"]) == lower
    )
    assert len(matching) == 6
    assert Counter(row["spectator_cap"] for row in matching) == {
        0: 2,
        1: 2,
        2: 2,
    }

    proper_edges = (("2U", "VI"), ("VI", "2U"))
    lower_edges = (
        ("0", "I"),
        ("I", "2I"),
        ("2I", "UI"),
        ("UI", "0"),
    )
    assert _is_strong(proper, proper_edges)
    assert _is_strong(lower, lower_edges)

    # Starting from spectator w+2, this positive-probability physical word
    # creates old-V debt and returns to the no-fast base with spectator w.
    w = 10
    history_word = (
        ("2U", "VI"),
        ("I", "2I"),
        ("2I", "UI"),
        ("UI", "0"),
    )
    history_states = _apply_word((w + 2, 0, 0), history_word)
    assert history_states[-1] == (w, 0, 1)

    # Reset relative V displacement at that historical base.  Exact proper
    # excursions 2U->VI->2U are state self-loops and are contracted.  The
    # next nonself zero-order step is the displayed service endpoint.
    service_word = (("0", "I"), ("VI", "2U"))
    service_states = _apply_word((w, 0, 0), service_word)
    assert service_states[-1] == (w + 2, 0, -1)

    b_drift_at_w_for_zero_ell = log((w + 1) * (w + 2))
    assert b_drift_at_w_for_zero_ell > 0
    sample_drifts = {
        value: log((value + 1) * (value + 2))
        for value in (10, 100, 1000, 10000)
    }
    assert all(
        right > left
        for left, right in zip(
            sample_drifts.values(), tuple(sample_drifts.values())[1:]
        )
    )

    return {
        "normalized_support": {
            "proper": list(proper),
            "lower": list(lower),
            "exact_generalized_rows": len(matching),
            "spectator_cap_histogram": {
                str(cap): count
                for cap, count in sorted(
                    Counter(row["spectator_cap"] for row in matching).items()
                )
            },
        },
        "strong_orientation": {
            "proper": [list(edge) for edge in proper_edges],
            "lower": [list(edge) for edge in lower_edges],
        },
        "historical_positive_debt_word": {
            "word": [list(edge) for edge in history_word],
            "states_U_I_relativeV": [list(state) for state in history_states],
            "endpoint": list(history_states[-1]),
        },
        "zero_order_actual_service_endpoint": {
            "word": [list(edge) for edge in service_word],
            "states_U_I_relativeV": [list(state) for state in service_states],
            "endpoint": list(service_states[-1]),
            "spectator_change": 2,
            "old_V_change": -1,
        },
        "B_ell_drift": {
            "exact_formula": (
                "log((u+1)(u+2)) + 2 ell_U"
            ),
            "asymptotic": "2 log u + O(1)",
            "positive_for_every_fixed_ell_U_eventually": True,
            "d_plus_has_finite_support": False,
            "chi_is_uniformly_bounded": False,
            "sample_zero_ell_drifts": {
                str(value): drift for value, drift in sample_drifts.items()
            },
        },
    }


def reaudit() -> dict[str, object]:
    certificate = dormant.certificate()
    assert certificate["selected_incidences"]["total"] == 407
    assert certificate["selected_pairs"]["total"] == 333
    assert certificate["generalized_family_ii"]["incidences"] == 951
    assert certificate["one_to_two_active_promotion_handoff"][
        "distinct_target_incidences"
    ] == 317
    assert not certificate["analytic_theorem_independently_audited"]
    assert not certificate["pair_level_recurrence_certified"]
    assert not certificate["global_t3_2_certified"]

    counterexample = actual_service_endpoint_counterexample()
    return {
        "frozen_repaired_finite_suite": "PASS",
        "sections_6_boundary_bookkeeping": (
            "conditional PASS after separating the cumulative A-boundary "
            "from the per-raw-block three-insertion event"
        ),
        "start_weighted_polynomial_factorial_green": (
            "PASS at the killed-to-cemetery level; actual service endpoint "
            "requires the theta-prime/theta loss already present in (7.4)"
        ),
        "maximal_degree_and_historical_singleton_exclusion": "PASS",
        "actual_service_endpoint_counterexample": counterexample,
        "bounded_B_ell_plus_chi": "FAIL",
        "equation_7_17_q_moments": (
            "no exact counterexample found, but the arbitrary-interruption "
            "tail is only sketched rather than explicitly closed"
        ),
        "service_probability_1_minus_o_1": (
            "conditional PASS given the start-weighted killed Green lemma"
        ),
        "fourth_power_identity": (
            "algebra PASS, but its O(1) first-moment input fails; an "
            "O(log(u+e))=o(log n) replacement appears sufficient"
        ),
        "exact_951_to_317_telescope": "PASS",
        "descriptor_local_reaudit_verdict": "FAIL_AS_WRITTEN_REPAIR_OPEN",
        "network_recurrence_counterexample_found": False,
        "analytic_theorem_independently_audited": False,
        "pair_level_recurrence_certified": False,
        "global_t3_2_certified": False,
    }


if __name__ == "__main__":
    print(json.dumps(reaudit(), indent=2, sort_keys=True))
