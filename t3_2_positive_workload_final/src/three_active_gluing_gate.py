"""Finite and exact obstructions for gluing the three-active local drifts.

This module certifies the finite support/tier geometry and records the exact
scope of the independently audited all-active physical-time generator
theorem.  The local analytic flag is deliberately separate from pair-level
recurrence and global T3-2 certification, which remain uncertified.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import stoichiometric_gate_feasibility as feasibility
import three_active_flat_phase as flat
import two_active_phase_gate as two_active


Pair = closure.Pair


def incidences_by_pair() -> dict[Pair, tuple[tier.TierDescriptor, ...]]:
    result: dict[Pair, list[tier.TierDescriptor]] = defaultdict(list)
    for pair, descriptor in flat.feasible_all_active_incidences():
        result[pair].append(descriptor)
    return {
        pair: tuple(sorted(items, key=tier.descriptor_sort_key))
        for pair, items in result.items()
    }


def fixed_whole_top(pair: Pair) -> tuple[int, int]:
    """The side and support common to every failed all-active descriptor."""

    descriptors = incidences_by_pair()[pair]
    values = {
        flat.whole_top_linkage(pair, descriptor)
        for descriptor in descriptors
    }
    assert len(values) == 1
    return next(iter(values))


SELECTOR_SEAM_PAIR: Pair = (
    closure.mask(("2A", "BC")),
    closure.mask(("0", "A", "B", "2C")),
)

SELECTOR_SEAM_WEIGHTS = (
    (2, 3, 1),
    (3, 4, 2),
    (3, 5, 1),
    (4, 5, 3),
    (7, 10, 4),
)


def selector_seam() -> dict[str, object]:
    """Five failed cones invisible to finite linear population selectors."""

    descriptors = incidences_by_pair()[SELECTOR_SEAM_PAIR]
    weights = tuple(sorted(descriptor.weight for descriptor in descriptors))
    assert weights == SELECTOR_SEAM_WEIGHTS
    assert all(weight[1] > weight[0] > weight[2] for weight in weights)
    side, top = fixed_whole_top(SELECTOR_SEAM_PAIR)
    return {
        "pair": [
            list(part) for part in closure.pair_payload(SELECTOR_SEAM_PAIR)
        ],
        "whole_top_side": side,
        "whole_top_support": list(closure.support(top)),
        "failed_weights": [list(weight) for weight in weights],
        "common_population_dominance": ["B", "A", "C"],
    }


def _workload(descriptor: tier.TierDescriptor, node: int) -> int:
    return sum(
        descriptor.weight[index] * closure.COMPLEXES[node][index]
        for index in range(3)
    )


def top_curvature_excess(
    pair: Pair,
    descriptor: tier.TierDescriptor,
) -> int:
    """Worst top curvature exponent minus the maximal lower-source exponent.

    At an exact entropy center, a top reaction y->z has second-order scale
    r_top/min_i x_i over coordinates changed by z-y.  This function records
    its exponent relative to the largest source monomial in the other
    linkage.
    """

    side, top = flat.whole_top_linkage(pair, descriptor)
    top_nodes = tier._nodes(top)
    lower_nodes = tier._nodes(pair[1 - side])
    top_level = {_workload(descriptor, node) for node in top_nodes}
    assert len(top_level) == 1
    alpha = next(iter(top_level))
    beta = max(_workload(descriptor, node) for node in lower_nodes)
    worst = max(
        alpha
        - min(
            descriptor.weight[index]
            for index in range(3)
            if closure.COMPLEXES[source][index]
            != closure.COMPLEXES[target][index]
        )
        for source in top_nodes
        for target in top_nodes
        if source != target
    )
    return worst - beta


def curvature_obstructions() -> tuple[tuple[Pair, tier.TierDescriptor, int], ...]:
    result = tuple(
        (pair, descriptor, excess)
        for pair, descriptor in flat.feasible_all_active_incidences()
        if (excess := top_curvature_excess(pair, descriptor)) > 0
    )
    assert all(
        closure.support(flat.whole_top_linkage(pair, descriptor)[1])
        == ("2A", "BC")
        for pair, descriptor, _ in result
    )
    return result


def _two_node_rank_one(
    pair: Pair,
    descriptor: tier.TierDescriptor,
) -> bool:
    _, top = flat.whole_top_linkage(pair, descriptor)
    return (
        top.bit_count() == 2
        and flat._support_rank(top) == 1
        and flat._support_deficiency(top) == 0
    )


def curvature_cofactors(
    pair: Pair,
    descriptor: tier.TierDescriptor,
) -> tuple[int, ...]:
    """All degree-lowered top monomials entering the entropy remainder."""

    _, top = flat.whole_top_linkage(pair, descriptor)
    nodes = tuple(tier._nodes(top))
    assert len(nodes) == 2
    first, second = (closure.COMPLEXES[node] for node in nodes)
    changed = tuple(
        index for index in range(3) if first[index] != second[index]
    )
    complex_index = {
        vector: index for index, vector in enumerate(closure.COMPLEXES)
    }
    result: set[int] = set()
    for coordinate in changed:
        for node in nodes:
            vector = closure.COMPLEXES[node]
            if vector[coordinate]:
                lowered = list(vector)
                lowered[coordinate] -= 1
                result.add(complex_index[tuple(lowered)])
    return tuple(sorted(result))


def direct_entropy_safe(
    pair: Pair,
    descriptor: tier.TierDescriptor,
) -> bool:
    """Whether every top curvature cofactor is below the lower top tier."""

    side, _ = flat.whole_top_linkage(pair, descriptor)
    lower_nodes = tier._nodes(pair[1 - side])
    level = {
        node: rank
        for rank, block in enumerate(descriptor.partition)
        for node in block
    }
    lower_rank = min(level[node] for node in lower_nodes)
    return all(
        level[node] >= lower_rank
        for node in curvature_cofactors(pair, descriptor)
    )


def direct_entropy_branch() -> dict[str, object]:
    """Exact premise count for the rate-adjusted entropy drift lemma."""

    incidences = tuple(
        (pair, descriptor)
        for pair, descriptor in flat.feasible_all_active_incidences()
        if _two_node_rank_one(pair, descriptor)
    )
    safe = tuple(
        (pair, descriptor)
        for pair, descriptor in incidences
        if direct_entropy_safe(pair, descriptor)
    )
    obstructed = tuple(
        (pair, descriptor)
        for pair, descriptor in incidences
        if not direct_entropy_safe(pair, descriptor)
    )
    obstructed_from_exponent = {
        (pair, descriptor)
        for pair, descriptor, _ in curvature_obstructions()
    }
    assert set(obstructed) == obstructed_from_exponent
    pairs = {pair for pair, _ in incidences}
    obstructed_pairs = {pair for pair, _ in obstructed}
    fully_safe_pairs = pairs - obstructed_pairs
    return {
        "two_node_rank_one_failed_incidences": len(incidences),
        "direct_entropy_safe_incidences": len(safe),
        "curvature_obstructed_incidences": len(obstructed),
        "two_node_rank_one_pairs": len(pairs),
        "fully_direct_entropy_safe_pairs": len(fully_safe_pairs),
        "pairs_requiring_a_shell_seam": len(obstructed_pairs),
        "safe_incidences_on_seam_pairs": sum(
            pair in obstructed_pairs for pair, _ in safe
        ),
        "premise_only": (
            "counts the exact cofactor-tier hypothesis of the analytic "
            "rate-adjusted entropy lemma; it is not a recurrence claim"
        ),
    }


def curvature_obstruction_workload(
    pair: Pair,
    descriptor: tier.TierDescriptor,
) -> tuple[int, int, int]:
    """A top-invariant linear workload strictly descending on the seam."""

    side, _ = flat.whole_top_linkage(pair, descriptor)
    lower_names = set(closure.support(pair[1 - side]))
    if lower_names <= {"0", "A", "B", "2B", "AB"}:
        return 2, 1, 3
    if lower_names <= {"0", "A", "C", "2C", "AC"}:
        return 2, 3, 1
    raise AssertionError(lower_names)


def obstruction_workload_branch() -> dict[str, object]:
    """Exact cut certificate for all 16 curvature-obstructed incidences."""

    rows: list[dict[str, object]] = []
    for pair, descriptor, _ in curvature_obstructions():
        side, top = flat.whole_top_linkage(pair, descriptor)
        lower = pair[1 - side]
        workload = curvature_obstruction_workload(pair, descriptor)
        top_nodes = tier._nodes(top)
        assert {
            sum(workload[i] * closure.COMPLEXES[node][i] for i in range(3))
            for node in top_nodes
        } == {4}

        lower_nodes = tier._nodes(lower)
        values = {
            node: sum(
                workload[i] * closure.COMPLEXES[node][i]
                for i in range(3)
            )
            for node in lower_nodes
        }
        maximum = max(values.values())
        high = {node for node, value in values.items() if value == maximum}
        low = lower_nodes - high
        assert high and low

        level = {
            node: rank
            for rank, block in enumerate(descriptor.partition)
            for node in block
        }
        # Every possible high-to-low edge is strictly workload negative.
        assert all(values[target] < values[source] for source in high for target in low)
        # Every high source strictly dominates every possible positive
        # low-to-high source in the exact D-order.  Strong connectivity
        # supplies at least one high-to-low edge for every orientation.
        assert all(level[source] < level[target] for source in high for target in low)
        rows.append(
            {
                "pair": [
                    list(part) for part in closure.pair_payload(pair)
                ],
                "weight": list(descriptor.weight),
                "workload": list(workload),
                "high_cut": sorted(closure.NAMES[node] for node in high),
                "low_cut": sorted(closure.NAMES[node] for node in low),
            }
        )
    return {
        "incidences": len(rows),
        "pairs": len(
            {
                tuple(tuple(part) for part in row["pair"])
                for row in rows
            }
        ),
        "workloads": sorted({tuple(row["workload"]) for row in rows}),
        "rows": rows,
        "scope": (
            "local all-active obstruction-cone drift only; "
            "does not glue to the direct-entropy cones"
        ),
    }


def global_linear_workload_branch() -> dict[str, object]:
    """Which seam pairs need no all-active glue for the linear workload."""

    obstruction_pairs = {
        pair for pair, _, _ in curvature_obstructions()
    }
    globally_closed: list[Pair] = []
    counterexamples: list[dict[str, object]] = []
    equal_weight_descriptor, = (
        descriptor
        for descriptor in tier.tier_descriptors()
        if descriptor.weight == (1, 1, 1)
        and descriptor.caps == (2, 2, 2)
    )

    for pair in sorted(obstruction_pairs, key=closure.pair_payload):
        sample_descriptor = incidences_by_pair()[pair][0]
        side, _ = flat.whole_top_linkage(pair, sample_descriptor)
        lower = pair[1 - side]
        lower_support = closure.support(lower)
        workload = curvature_obstruction_workload(pair, sample_descriptor)

        if lower_support in {
            ("0", "A", "B", "AB"),
            ("0", "A", "C", "AC"),
        }:
            # AB (or AC) is the unique workload maximum and its monomial
            # strictly dominates every unary/zero source on every
            # all-active sequence.
            globally_closed.append(pair)
            continue

        assert feasibility.descriptor_feasible(pair, equal_weight_descriptor)
        nodes = tuple(sorted(tier._nodes(lower)))
        values = {
            node: sum(
                workload[i] * closure.COMPLEXES[node][i]
                for i in range(3)
            )
            for node in nodes
        }
        levels = {
            node: rank
            for rank, block in enumerate(equal_weight_descriptor.partition)
            for node in block
        }
        first = nodes[0]
        witness = None
        for rest in permutations(nodes[1:]):
            cycle = (first,) + rest
            edges = tuple(
                (cycle[index], cycle[(index + 1) % len(cycle)])
                for index in range(len(cycle))
            )
            nonzero = tuple(
                (
                    levels[source],
                    values[target] - values[source],
                    source,
                    target,
                )
                for source, target in edges
                if values[target] != values[source]
            )
            leading_level = min(item[0] for item in nonzero)
            leading = tuple(
                item for item in nonzero if item[0] == leading_level
            )
            if any(increment > 0 for _, increment, _, _ in leading):
                witness = edges, leading
                break
        assert witness is not None
        edges, leading = witness
        counterexamples.append(
            {
                "pair": [
                    list(part) for part in closure.pair_payload(pair)
                ],
                "workload": list(workload),
                "descriptor_weight": [1, 1, 1],
                "strong_cycle": [
                    f"{closure.NAMES[source]}->{closure.NAMES[target]}"
                    for source, target in edges
                ],
                "leading_positive_edges": [
                    f"{closure.NAMES[source]}->{closure.NAMES[target]}"
                    for _, increment, source, target in leading
                    if increment > 0
                ],
                "rate_choice": (
                    "take the listed positive edge rate sufficiently large "
                    "relative to the other fixed positive cycle rates"
                ),
            }
        )

    closed_set = set(globally_closed)
    closed_obstruction_incidences = sum(
        pair in closed_set
        for pair, _, _ in curvature_obstructions()
    )
    return {
        "globally_closed_pairs": len(globally_closed),
        "globally_closed_obstruction_incidences": closed_obstruction_incidences,
        "globally_closed_supports": [
            [list(part) for part in closure.pair_payload(pair)]
            for pair in globally_closed
        ],
        "remaining_pairs": len(counterexamples),
        "remaining_obstruction_incidences": (
            len(curvature_obstructions()) - closed_obstruction_incidences
        ),
        "minimal_counterexamples": counterexamples,
        "scope": (
            "all-active linear Foster branch only; "
            "no boundary-interface or recurrence claim"
        ),
    }


def rate_dependent_linear_workload_branch() -> dict[str, object]:
    """Support certificate for the all-active q_b workload theorem."""

    rows: list[dict[str, object]] = []
    class_counts: Counter[str] = Counter()
    for pair in sorted(
        {pair for pair, _, _ in curvature_obstructions()},
        key=closure.pair_payload,
    ):
        sample_descriptor = incidences_by_pair()[pair][0]
        side, _ = flat.whole_top_linkage(pair, sample_descriptor)
        lower_support = set(closure.support(pair[1 - side]))
        b_side = lower_support <= {"0", "A", "B", "2B", "AB"}
        c_side = lower_support <= {"0", "A", "C", "2C", "AC"}
        assert b_side ^ c_side
        quadratic_double = "2B" if b_side else "2C"
        quadratic_mixed = "AB" if b_side else "AC"
        has_double = quadratic_double in lower_support
        has_mixed = quadratic_mixed in lower_support
        assert has_double or has_mixed
        if has_double and has_mixed:
            support_class = "double_and_mixed"
            selector = (
                "b=2 if the mixed-source total-degree drift is strict; "
                "otherwise b<2 sufficiently close to 2"
            )
        elif has_mixed:
            support_class = "mixed_only"
            selector = "b=2"
        else:
            support_class = "double_only"
            selector = (
                "choose r_double<b<r_A, where r_double<=1<=r_A "
                "and strong connectivity makes the inequality strict"
            )
        class_counts[support_class] += 1
        rows.append(
            {
                "pair": [
                    list(part) for part in closure.pair_payload(pair)
                ],
                "side": "B" if b_side else "C",
                "support_class": support_class,
                "workload_family": (
                    ["2", "b", "4-b"]
                    if b_side
                    else ["2", "4-b", "b"]
                ),
                "parameter_domain": "0<b<4",
                "rate_dependent_selector": selector,
            }
        )
    return {
        "all_seam_pairs": len(rows),
        "class_counts": dict(sorted(class_counts.items())),
        "all_have_a_positive_rate_dependent_linear_workload": True,
        "rows": rows,
        "scope": (
            "all-active physical-time generator theorem; "
            "does not cover lower-active-coordinate interfaces"
        ),
    }


def rank_one_triple_factorial_linear_branch() -> dict[str, object]:
    """Finite premises for the arbitrary-directed three-node top lemma.

    The analytic input is Lemma 4.1 of
    ``research_notes/certified_exact_shielded_seam.md``.  After relabelling,
    a top support ``{2X,X+Y,2Y}`` admits a rate-dependent linear correction
    ``d X`` for which its factorial-entropy drift is at most linear in
    ``X+Y``.  This routine checks the two facts needed to let the other
    linkage dominate on every failed all-active flat cone: exact flatness
    makes ``X`` and ``Y`` comparable, and the other linkage contains a
    source involving ``X`` or ``Y``.
    """

    rows: list[dict[str, object]] = []
    support_histogram: Counter[str] = Counter()
    for pair, descriptor in flat.feasible_all_active_incidences():
        side, top = flat.whole_top_linkage(pair, descriptor)
        if not (
            top.bit_count() == 3
            and flat._support_rank(top) == 1
            and flat._support_deficiency(top) == 1
        ):
            continue

        top_nodes = tier._nodes(top)
        used_coordinates = tuple(
            index
            for index in range(3)
            if any(closure.COMPLEXES[node][index] for node in top_nodes)
        )
        assert len(used_coordinates) == 2
        first, second = used_coordinates
        expected = {
            tuple(2 if index == first else 0 for index in range(3)),
            tuple(
                1 if index in {first, second} else 0
                for index in range(3)
            ),
            tuple(2 if index == second else 0 for index in range(3)),
        }
        assert {closure.COMPLEXES[node] for node in top_nodes} == expected
        assert descriptor.weight[first] == descriptor.weight[second] > 0

        lower = pair[1 - side]
        lower_nodes = tier._nodes(lower)
        active_lower_nodes = tuple(
            node
            for node in lower_nodes
            if (
                closure.COMPLEXES[node][first]
                + closure.COMPLEXES[node][second]
                > 0
            )
        )
        # Otherwise the top direction together with the lower linkage would
        # span at most two dimensions, contradicting the exact full-rank
        # feasibility check for these incidences.
        assert active_lower_nodes
        assert len(closure.full_rows(*pair)) == 3

        top_name = ",".join(closure.support(top))
        support_histogram[top_name] += 1
        rows.append(
            {
                "pair": [
                    list(part) for part in closure.pair_payload(pair)
                ],
                "weight": list(descriptor.weight),
                "top_support": list(closure.support(top)),
                "top_active_coordinates": [
                    ("A", "B", "C")[first],
                    ("A", "B", "C")[second],
                ],
                "lower_active_sources": [
                    closure.NAMES[node] for node in active_lower_nodes
                ],
            }
        )

    pairs = {
        tuple(tuple(part) for part in row["pair"])
        for row in rows
    }
    return {
        "failed_incidences": len(rows),
        "pairs": len(pairs),
        "top_support_histogram": dict(sorted(support_histogram.items())),
        "all_lower_linkages_have_a_top_species_source": True,
        "all_have_one_rate_dependent_factorial_linear_all_active_potential": True,
        "rows": rows,
        "scope": (
            "all-active physical-time generator theorem; the linear "
            "correction depends on the actual top orientation and rates; "
            "no lower-active-coordinate interface claim"
        ),
    }


def rank_two_linear_workload_branch() -> dict[str, object]:
    """Exact global linear workloads for every rank-two whole-top pair."""

    rows: list[dict[str, object]] = []
    size_histogram: Counter[int] = Counter()
    weight_histogram: Counter[str] = Counter()
    for pair, descriptor in flat.feasible_all_active_incidences():
        side, top = flat.whole_top_linkage(pair, descriptor)
        if flat._support_rank(top) != 2:
            continue

        lower = pair[1 - side]
        assert closure.support(lower) == ("0", "C")
        workload = descriptor.weight
        assert all(value > 0 for value in workload)
        assert {
            sum(
                workload[index] * closure.COMPLEXES[node][index]
                for index in range(3)
            )
            for node in tier._nodes(top)
        } == {2}
        assert workload[2] > 0

        size_histogram[top.bit_count()] += 1
        weight_histogram[",".join(map(str, workload))] += 1
        rows.append(
            {
                "pair": [
                    list(part) for part in closure.pair_payload(pair)
                ],
                "weight": list(workload),
                "top_support": list(closure.support(top)),
                "lower_support": ["0", "C"],
                "exact_generator": (
                    "w_C*(kappa_0C-kappa_C0*C)"
                ),
            }
        )

    pairs = {
        tuple(tuple(part) for part in row["pair"])
        for row in rows
    }
    return {
        "failed_incidences": len(rows),
        "pairs": len(pairs),
        "top_size_histogram": {
            str(size): count for size, count in sorted(size_histogram.items())
        },
        "workload_histogram": dict(sorted(weight_histogram.items())),
        "all_have_exact_global_positive_linear_workload": True,
        "rows": rows,
        "scope": (
            "all-active physical-time generator theorem; in fact the "
            "displayed workload descends whenever C tends to infinity"
        ),
    }


def two_active_rate_correction_compatibility() -> dict[str, object]:
    """Exact overlap on which the same rank-one top correction is used.

    This is a support identity, not an analytic assertion about either
    endpoint theorem.  A fixed orientation/rate vector on the common top
    mask therefore selects the same detailed-balance or directed-triple
    correction in both active-coordinate regimes.
    """

    two_active_tops: dict[Pair, set[int]] = defaultdict(set)
    for pair, descriptor, category in two_active.incidences():
        if category != "closed_rank_one_top_phase":
            continue
        top, = two_active._whole_top_linkages(pair, descriptor)
        two_active_tops[pair].add(top)

    overlap = sorted(
        set(incidences_by_pair()) & set(two_active_tops),
        key=closure.pair_payload,
    )
    curvature_seam_pairs = {
        pair for pair, _, _ in curvature_obstructions()
    }
    rows: list[dict[str, object]] = []
    support_histogram: Counter[str] = Counter()
    for pair in overlap:
        assert len(two_active_tops[pair]) == 1
        two_top = next(iter(two_active_tops[pair]))
        _, all_top = fixed_whole_top(pair)
        assert two_top == all_top
        support_name = ",".join(closure.support(all_top))
        support_histogram[support_name] += 1
        rows.append(
            {
                "pair": [
                    list(part) for part in closure.pair_payload(pair)
                ],
                "common_top_support": list(closure.support(all_top)),
                "correction_type": (
                    "directed-triple factorial-linear"
                    if all_top.bit_count() == 3
                    else (
                        "shared top mask, but all-active uses H_b seam workload"
                        if pair in curvature_seam_pairs
                        else "reversible two-node rate-adjusted"
                    )
                ),
            }
        )

    return {
        "all_active_pairs": len(incidences_by_pair()),
        "two_active_rank_one_pairs": len(two_active_tops),
        "overlap_pairs": len(overlap),
        "all_overlap_pairs_have_one_identical_top_mask": True,
        "curvature_seam_overlap_pairs": sum(
            pair in curvature_seam_pairs for pair in overlap
        ),
        "common_corrected_factorial_candidate_pairs": sum(
            pair not in curvature_seam_pairs for pair in overlap
        ),
        "top_size_histogram": {
            "2": sum(len(row["common_top_support"]) == 2 for row in rows),
            "3": sum(len(row["common_top_support"]) == 3 for row in rows),
        },
        "top_support_histogram": dict(sorted(support_histogram.items())),
        "rows": rows,
        "scope": (
            "finite support/rate-correction compatibility only; analytic "
            "two-active entropy endpoints must be certified separately, "
            "and the twelve H_b curvature seams still switch potential"
        ),
    }


FIXED_EPSILON_COUNTERPAIR: Pair = (
    closure.mask(("2A", "BC")),
    closure.mask(("0", "A", "2B", "AB")),
)
FIXED_EPSILON_WEIGHT = (3, 1, 5)
SHELL_POTENTIAL_PASS_WEIGHT = (3, 1, 1)
SHELL_POWER_PASS_WEIGHT = (6, 10, 11)
EXPECTED_CERTIFICATE_SHA256 = (
    "77c4853ce916f224fe23132f17e2236a81d319632c6e2f3892cf516ae76f4b5e"
)


def certificate() -> dict[str, object]:
    grouped = incidences_by_pair()
    fixed = {pair: fixed_whole_top(pair) for pair in grouped}
    full_rank_three = {
        pair for pair in grouped if len(closure.full_rows(*pair)) == 3
    }
    assert len(full_rank_three) == len(grouped)
    curvature = curvature_obstructions()
    counter_descriptors = {
        descriptor.weight: descriptor
        for descriptor in grouped[FIXED_EPSILON_COUNTERPAIR]
    }
    counter_descriptor = counter_descriptors[FIXED_EPSILON_WEIGHT]
    assert top_curvature_excess(
        FIXED_EPSILON_COUNTERPAIR,
        counter_descriptor,
    ) == 1
    pass_descriptor, = (
        descriptor
        for descriptor in tier.tier_descriptors()
        if descriptor.weight == SHELL_POTENTIAL_PASS_WEIGHT
        and descriptor.caps == (2, 2, 2)
    )
    assert feasibility.descriptor_feasible(SELECTOR_SEAM_PAIR, pass_descriptor)
    assert tier.universal_orientation_tier_condition(
        SELECTOR_SEAM_PAIR,
        pass_descriptor,
    )
    shell_power_descriptor, = (
        descriptor
        for descriptor in tier.tier_descriptors()
        if descriptor.weight == SHELL_POWER_PASS_WEIGHT
        and descriptor.caps == (2, 2, 2)
    )
    assert feasibility.descriptor_feasible(
        FIXED_EPSILON_COUNTERPAIR,
        shell_power_descriptor,
    )
    assert tier.universal_orientation_tier_condition(
        FIXED_EPSILON_COUNTERPAIR,
        shell_power_descriptor,
    )

    payload: dict[str, object] = {
        "claim_scope": (
            "finite fixed-top geometry plus the independently audited "
            "dimension-local all-active generator theorem; no pair-level "
            "recurrence or global T3-2 claim"
        ),
        "all_active_local_analytic_theorem_certified": True,
        "pair_level_recurrence_certified": False,
        "global_t3_2_certified": False,
        "all_active_failed_pairs": len(grouped),
        "pairs_with_one_fixed_top_side_and_support": len(fixed),
        "full_rank_three_pairs": len(full_rank_three),
        "direct_entropy_branch": direct_entropy_branch(),
        "obstruction_workload_branch": obstruction_workload_branch(),
        "global_linear_workload_branch": global_linear_workload_branch(),
        "rate_dependent_linear_workload_branch": (
            rate_dependent_linear_workload_branch()
        ),
        "rank_one_triple_factorial_linear_branch": (
            rank_one_triple_factorial_linear_branch()
        ),
        "rank_two_linear_workload_branch": rank_two_linear_workload_branch(),
        "two_active_rate_correction_compatibility": (
            two_active_rate_correction_compatibility()
        ),
        "distinct_fixed_top_supports": len({top for _, top in fixed.values()}),
        "selector_seam": selector_seam(),
        "curvature_obstruction_incidences": len(curvature),
        "curvature_obstruction_pairs": len(
            {pair for pair, _, _ in curvature}
        ),
        "curvature_excess_histogram": {
            str(value): count
            for value, count in sorted(
                Counter(excess for _, _, excess in curvature).items()
            )
        },
        "curvature_top_supports": [
            list(support)
            for support in sorted(
                {
                    closure.support(
                        flat.whole_top_linkage(pair, descriptor)[1]
                    )
                    for pair, descriptor, _ in curvature
                }
            )
        ],
        "fixed_epsilon_counterexample": {
            "pair": [
                list(part)
                for part in closure.pair_payload(FIXED_EPSILON_COUNTERPAIR)
            ],
            "weight": list(FIXED_EPSILON_WEIGHT),
            "integer_state_family": ["N^3", "N", "N^5"],
            "top_propensity_order": "N^6",
            "positive_top_curvature_order": "N^5",
            "maximal_lower_source": "AB",
            "maximal_lower_propensity_order": "N^4",
            "lower_drift_upper_order": "N^4 log N",
        },
        "shell_potential_pass_counterexample": {
            "pair": [
                list(part) for part in closure.pair_payload(SELECTOR_SEAM_PAIR)
            ],
            "weight": list(SHELL_POTENTIAL_PASS_WEIGHT),
            "integer_state_family": ["N^3", "N", "N"],
            "shell_center": [
                "(N^3+2N)/3",
                "(N^3+2N)/3",
                "(N^3+2N)/3",
            ],
            "strong_lower_cycle": ["A->2C", "2C->B", "B->0", "0->A"],
            "positive_shell_drift_order": "N^3 log N",
        },
        "shell_power_counterexample": {
            "pair": [
                list(part)
                for part in closure.pair_payload(FIXED_EPSILON_COUNTERPAIR)
            ],
            "strong_lower_cycle": [
                "2B->AB",
                "AB->A",
                "A->0",
                "0->2B",
            ],
            "failed_weight": list(FIXED_EPSILON_WEIGHT),
            "failed_state_family": ["N^3", "N", "N^5"],
            "failed_required_power": "p>=1/5",
            "pass_weight": list(SHELL_POWER_PASS_WEIGHT),
            "pass_state_family": ["N^6", "N^10", "N^11"],
            "pass_shell_center_exponents": [10, 9, 11],
            "pass_required_power": "p<1/11",
        },
        "fixed_gap_hinge_counterexample": {
            "pair": [
                list(part)
                for part in closure.pair_payload(FIXED_EPSILON_COUNTERPAIR)
            ],
            "strong_lower_cycle": [
                "2B->AB",
                "AB->A",
                "A->0",
                "0->2B",
            ],
            "pass_weight": list(SHELL_POWER_PASS_WEIGHT),
            "pass_state_family": ["N^6", "N^10", "N^11"],
            "pass_shell_center_exponents": [10, 9, 11],
            "entropy_gap_order": "N^10 log N",
            "positive_invariant_shell_order": "N^11",
            "gap_to_shell_ratio": "(log N)/N -> 0",
            "positive_shell_drift_order": "N^20 log N",
            "conclusion": (
                "every fixed c>0 leaves the pass family in the F core; "
                "c=0 is ordinary entropy and fails at the curvature center"
            ),
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = sha256(encoded).hexdigest()
    return payload


def self_test() -> None:
    result = certificate()
    assert result["all_active_failed_pairs"] == 403
    assert result["pairs_with_one_fixed_top_side_and_support"] == 403
    assert result["full_rank_three_pairs"] == 403
    assert result["distinct_fixed_top_supports"] == 35
    assert result["direct_entropy_branch"] == {
        "two_node_rank_one_failed_incidences": 966,
        "direct_entropy_safe_incidences": 950,
        "curvature_obstructed_incidences": 16,
        "two_node_rank_one_pairs": 288,
        "fully_direct_entropy_safe_pairs": 276,
        "pairs_requiring_a_shell_seam": 12,
        "safe_incidences_on_seam_pairs": 44,
        "premise_only": (
            "counts the exact cofactor-tier hypothesis of the analytic "
            "rate-adjusted entropy lemma; it is not a recurrence claim"
        ),
    }
    assert result["obstruction_workload_branch"]["incidences"] == 16
    assert result["obstruction_workload_branch"]["pairs"] == 12
    assert result["obstruction_workload_branch"]["workloads"] == [
        (2, 1, 3),
        (2, 3, 1),
    ]
    assert result["global_linear_workload_branch"]["globally_closed_pairs"] == 2
    assert (
        result["global_linear_workload_branch"][
            "globally_closed_obstruction_incidences"
        ]
        == 2
    )
    assert result["global_linear_workload_branch"]["remaining_pairs"] == 10
    assert (
        result["global_linear_workload_branch"][
            "remaining_obstruction_incidences"
        ]
        == 14
    )
    assert result["rate_dependent_linear_workload_branch"][
        "all_seam_pairs"
    ] == 12
    assert result["rate_dependent_linear_workload_branch"]["class_counts"] == {
        "double_and_mixed": 8,
        "double_only": 2,
        "mixed_only": 2,
    }
    assert result["rate_dependent_linear_workload_branch"][
        "all_have_a_positive_rate_dependent_linear_workload"
    ]
    assert result["rank_one_triple_factorial_linear_branch"][
        "failed_incidences"
    ] == 279
    assert result["rank_one_triple_factorial_linear_branch"]["pairs"] == 91
    assert result["rank_one_triple_factorial_linear_branch"][
        "all_have_one_rate_dependent_factorial_linear_all_active_potential"
    ]
    assert result["rank_two_linear_workload_branch"]["failed_incidences"] == 24
    assert result["rank_two_linear_workload_branch"]["pairs"] == 24
    assert result["rank_two_linear_workload_branch"][
        "all_have_exact_global_positive_linear_workload"
    ]
    compatibility = result["two_active_rate_correction_compatibility"]
    assert compatibility["all_active_pairs"] == 403
    assert compatibility["two_active_rank_one_pairs"] == 310
    assert compatibility["overlap_pairs"] == 298
    assert compatibility["all_overlap_pairs_have_one_identical_top_mask"]
    assert compatibility["top_size_histogram"] == {"2": 207, "3": 91}
    assert compatibility["curvature_seam_overlap_pairs"] == 12
    assert compatibility["common_corrected_factorial_candidate_pairs"] == 286
    assert result["curvature_obstruction_incidences"] == 16
    assert result["curvature_obstruction_pairs"] == 12
    assert result["curvature_excess_histogram"] == {"1": 12, "2": 4}
    assert result["certificate_sha256"] == EXPECTED_CERTIFICATE_SHA256


if __name__ == "__main__":
    self_test()
    print(json.dumps(certificate(), indent=2, sort_keys=True))
