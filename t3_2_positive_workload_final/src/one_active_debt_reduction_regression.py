"""Claim-neutral one-active reflected-debt resistance regressions.

The numerical reflected debt is used only to certify that a no-fast base
with positive debt is physically reachable from the descriptor cap.  Once
an episode starts with old debt ``d>0``, its first strict reduction is
equivalently the first time the *relative* active displacement is negative:
reflection cannot act before that event.  A fresh entry followed by one
exit therefore has relative reward zero and does not service old debt.

For every reached base this module separately computes the resistance of

* a future unresolved arrival: relative reward ``r>0`` at a no-fast base;
* old-debt reduction: the first relative reward ``r<0``.

The scoped certificate treats the canonical obstruction cycles and the
maximal descriptor-allowed failing digraph.  It is bounded finite evidence,
not an arbitrary-strong-orientation theorem or a recurrence proof.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import one_active_kinetic_depth as kinetic
import one_active_phase_shape as phase_shape
import one_active_remaining_structure as structure


POPULATION_BOUND = 7
CREATION_DEBT_BOUND = 10
RELATIVE_REWARD_BOUND = 10
INFINITY = 10**6
EXPECTED_PAYLOAD_SHA256 = (
    "a1e3cd234586f850c3fae0ba11a6827b8e6d8af81c7549e9f27cf7e02e3d4a28"
)


def canonical_orientation(pair, descriptor):
    first, second = tier.obstruction_cycles(pair, descriptor)
    return first + second


def maximal_orientation(pair, descriptor):
    """Return every descriptor-allowed nonloop edge in each linkage."""

    forbidden = kinetic.forbidden_descending_edges(pair, descriptor)
    return tuple(
        (source, target)
        for mask in pair
        for source in tier._nodes(mask)
        for target in tier._nodes(mask)
        if source != target and (source, target) not in forbidden
    )


def orientation_is_allowed_and_strong(pair, descriptor, orientation):
    orientation = frozenset(orientation)
    forbidden = kinetic.forbidden_descending_edges(pair, descriptor)
    if orientation & forbidden:
        return False
    for mask in pair:
        nodes = frozenset(tier._nodes(mask))
        for start in nodes:
            reached = {start}
            frontier = [start]
            while frontier:
                source = frontier.pop()
                for left, right in orientation:
                    if (
                        left == source
                        and right in nodes
                        and right not in reached
                    ):
                        reached.add(right)
                        frontier.append(right)
            if reached != nodes:
                return False
    return True


def bounded_reflected_debt(
    debt, active_delta, *, debt_bound=CREATION_DEBT_BOUND
):
    """Reflect at zero and kill, rather than clamp, at the finite cap."""

    raw = debt + active_delta
    if raw > debt_bound:
        return None
    return max(0, raw)


def _zero_one_distances(starts, adjacency):
    queue = deque(starts)
    distance = {state: 0 for state in starts}
    while queue:
        state = queue.popleft()
        old = distance[state]
        for endpoint, cost in adjacency[state]:
            new = old + cost
            if new >= distance.get(endpoint, INFINITY):
                continue
            distance[endpoint] = new
            (queue.append if cost else queue.appendleft)(endpoint)
    return distance


def _transition_table(
    descriptor, orientation, *, population_bound=POPULATION_BOUND
):
    edges = structure._projected_edges(descriptor, orientation)
    table = {}
    for first in range(population_bound + 1):
        for second in range(population_bound + 1):
            inactive = first, second
            fast = structure._has_fast_clock(inactive, edges)
            transitions = []
            for edge in edges:
                if not structure._enabled(edge.source, inactive):
                    continue
                endpoint = tuple(
                    inactive[index] + edge.delta[index]
                    for index in range(2)
                )
                if not all(
                    0 <= value <= population_bound for value in endpoint
                ):
                    continue
                cost = int(edge.active_source_degree == 0 and fast)
                transitions.append((endpoint, edge.active_delta, cost))
            table[inactive] = tuple(transitions)
    return edges, table


def consistent_positive_bases(
    descriptor,
    orientation,
    *,
    population_bound=POPULATION_BOUND,
    debt_bound=CREATION_DEBT_BOUND,
):
    """Reachable no-fast inactive bases with some positive reflected debt."""

    active, = tier._active_coordinates(descriptor)
    inactive_coordinates = tuple(
        index for index in range(3) if index != active
    )
    start_inactive = tuple(
        descriptor.caps[index] for index in inactive_coordinates
    )
    edges, table = _transition_table(
        descriptor, orientation, population_bound=population_bound
    )
    states = tuple(
        (inactive, debt)
        for inactive in table
        for debt in range(debt_bound + 1)
    )
    adjacency = {state: [] for state in states}
    for state in states:
        inactive, debt = state
        for endpoint, active_delta, cost in table[inactive]:
            new_debt = bounded_reflected_debt(
                debt, active_delta, debt_bound=debt_bound
            )
            if new_debt is None:
                continue
            adjacency[state].append(((endpoint, new_debt), cost))
    distance = _zero_one_distances(((start_inactive, 0),), adjacency)
    grouped = defaultdict(list)
    for (inactive, debt), creation_depth in distance.items():
        if debt > 0 and not structure._has_fast_clock(inactive, edges):
            grouped[inactive].append((debt, creation_depth))
    return {
        inactive: {
            "reachable_debts": tuple(sorted(debt for debt, _ in rows)),
            "minimum_historical_creation_depth": min(
                depth for _, depth in rows
            ),
        }
        for inactive, rows in sorted(grouped.items())
    }


def relative_up_down_depths(
    descriptor,
    orientation,
    *,
    population_bound=POPULATION_BOUND,
    reward_bound=RELATIVE_REWARD_BOUND,
):
    """Future upward-return and first strict-reduction resistances.

    Relative reward starts at zero.  A transition to negative reward is a
    terminal old-debt reduction.  Positive reward is retained only up to the
    displayed finite word cap; there is no upper saturation.
    """

    edges, table = _transition_table(
        descriptor, orientation, population_bound=population_bound
    )
    states = tuple(
        (inactive, reward)
        for inactive in table
        for reward in range(reward_bound + 1)
    )
    adjacency = {state: [] for state in states}
    reverse = {state: [] for state in states}
    down_sources = []
    for state in states:
        inactive, reward = state
        for endpoint, active_delta, cost in table[inactive]:
            new_reward = reward + active_delta
            if new_reward < 0:
                # Negative active increments have active-degree-one sources,
                # so the terminal edge is a zero-resistance fast edge.
                assert cost == 0
                down_sources.append(state)
                continue
            if new_reward > reward_bound:
                continue
            target = endpoint, new_reward
            adjacency[state].append((target, cost))
            reverse[target].append((state, cost))

    down_distance = _zero_one_distances(tuple(set(down_sources)), reverse)
    up_targets = tuple(
        state
        for state in states
        if state[1] > 0
        and not structure._has_fast_clock(state[0], edges)
    )
    up_distance = _zero_one_distances(up_targets, reverse)
    return {
        inactive: {
            "future_unresolved_arrival_depth": up_distance.get(
                (inactive, 0), INFINITY
            ),
            "strict_old_debt_reduction_depth": down_distance.get(
                (inactive, 0), INFINITY
            ),
        }
        for inactive in table
        if not structure._has_fast_clock(inactive, edges)
    }


def incidence_rows(
    pair,
    descriptor,
    orientation,
    *,
    population_bound=POPULATION_BOUND,
    creation_debt_bound=CREATION_DEBT_BOUND,
    relative_reward_bound=RELATIVE_REWARD_BOUND,
):
    bases = consistent_positive_bases(
        descriptor,
        orientation,
        population_bound=population_bound,
        debt_bound=creation_debt_bound,
    )
    relative = relative_up_down_depths(
        descriptor,
        orientation,
        population_bound=population_bound,
        reward_bound=relative_reward_bound,
    )
    return tuple(
        {
            "inactive": inactive,
            **base,
            **relative[inactive],
        }
        for inactive, base in bases.items()
    )


def _phase_key(pair, descriptor):
    normalized = structure._normalized(pair, descriptor)
    return tuple(
        structure._linkage_phase(support)
        for support in normalized["supports"]
    )


def _row_payload(pair, descriptor, row):
    return {
        "pair": closure.pair_payload(pair),
        "weight": descriptor.weight,
        "caps": descriptor.caps,
        **row,
    }


def _family_payload(label, orient, *, relative_reward_bound):
    future_histogram = Counter()
    historical_histogram = Counter()
    phase_counter = Counter()
    depth_two_rows = []
    nonstrict = []
    missing_reduction = []
    rows_count = 0
    for pair, descriptor in phase_shape.candidate_incidences():
        orientation = orient(pair, descriptor)
        assert orientation_is_allowed_and_strong(
            pair, descriptor, orientation
        )
        phase_key = _phase_key(pair, descriptor)
        rows = incidence_rows(
            pair,
            descriptor,
            orientation,
            relative_reward_bound=relative_reward_bound,
        )
        rows_count += len(rows)
        for row in rows:
            creation = row["minimum_historical_creation_depth"]
            upward = row["future_unresolved_arrival_depth"]
            downward = row["strict_old_debt_reduction_depth"]
            historical_histogram[f"{creation},{downward}"] += 1
            future_histogram[f"{upward},{downward}"] += 1
            if downward == 2:
                phase_counter[str(phase_key)] += 1
                normalized = structure._normalized(pair, descriptor)
                depth_two_rows.append(
                    {
                        "pair": closure.pair_payload(pair),
                        "weight": descriptor.weight,
                        "caps": descriptor.caps,
                        "normalized_supports": normalized["supports"],
                        "normalized_caps": normalized["caps"],
                        **row,
                    }
                )
            if downward >= INFINITY:
                missing_reduction.append(_row_payload(pair, descriptor, row))
            elif upward <= downward:
                nonstrict.append(_row_payload(pair, descriptor, row))
    depth_two_rows = tuple(
        sorted(
            depth_two_rows,
            key=lambda row: json.dumps(row, sort_keys=True),
        )
    )
    depth_two_encoded = json.dumps(
        depth_two_rows, sort_keys=True, separators=(",", ":")
    ).encode()
    return {
        "label": label,
        "consistent_inactive_bases": rows_count,
        "future_upward_reduction_histogram": dict(
            sorted(future_histogram.items())
        ),
        "historical_creation_reduction_histogram": dict(
            sorted(historical_histogram.items())
        ),
        "reduction_depth_two_phase_histogram": dict(
            sorted(phase_counter.items())
        ),
        "reduction_depth_two_payload": depth_two_rows,
        "reduction_depth_two_payload_sha256": sha256(
            depth_two_encoded
        ).hexdigest(),
        "future_arrival_not_strictly_deeper": nonstrict,
        "missing_strict_reduction": missing_reduction,
    }


def _relative_boundary_sensitivity():
    """Replay the hardest two-singleton mixed phase at two word caps."""

    result = {}
    for label, orient in (
        ("canonical", canonical_orientation),
        ("maximal", maximal_orientation),
    ):
        mismatches = []
        rows_checked = 0
        for pair, descriptor in phase_shape.candidate_incidences():
            if _phase_key(pair, descriptor) != (
                ("mixed_killed", ("A",)),
                ("mixed_killed", ("B",)),
            ):
                continue
            orientation = orient(pair, descriptor)
            bases = consistent_positive_bases(descriptor, orientation)
            low = relative_up_down_depths(
                descriptor, orientation, reward_bound=6
            )
            high = relative_up_down_depths(
                descriptor, orientation, reward_bound=10
            )
            for inactive in bases:
                rows_checked += 1
                if low[inactive] != high[inactive]:
                    mismatches.append(
                        {
                            "pair": closure.pair_payload(pair),
                            "weight": descriptor.weight,
                            "caps": descriptor.caps,
                            "inactive": inactive,
                            "bound_6": low[inactive],
                            "bound_10": high[inactive],
                        }
                    )
        result[label] = {
            "rows_checked": rows_checked,
            "bound_6_vs_10_mismatches": mismatches,
        }
    return result


def certificate():
    families = {
        "canonical": _family_payload(
            "canonical",
            canonical_orientation,
            relative_reward_bound=RELATIVE_REWARD_BOUND,
        ),
        "maximal": _family_payload(
            "maximal",
            maximal_orientation,
            relative_reward_bound=RELATIVE_REWARD_BOUND,
        ),
    }
    payload = {
        "claim_scope": (
            "bounded claim-neutral canonical/maximal allowed-failing "
            "orientation regression; not an arbitrary-orientation theorem"
        ),
        "candidate_pairs": len(phase_shape.candidate_pairs()),
        "candidate_incidences": len(phase_shape.candidate_incidences()),
        "population_bound": POPULATION_BOUND,
        "creation_debt_bound": CREATION_DEBT_BOUND,
        "relative_reward_bound": RELATIVE_REWARD_BOUND,
        "service_semantics": (
            "from each current positive-debt base, relative reward r=0; "
            "first r<0 is strict old-debt reduction"
        ),
        "arrival_semantics": (
            "from the same base, future r>0 at a no-fast base"
        ),
        "orientation_families": families,
        "relative_boundary_sensitivity": _relative_boundary_sensitivity(),
        "arbitrary_strong_orientation_certified": False,
        "analytic_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert digest == EXPECTED_PAYLOAD_SHA256
    payload["payload_sha256"] = digest
    return payload


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
