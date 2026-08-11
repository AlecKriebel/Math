"""Relative-debt graph certificates for one-active orientations.

For a fixed support/cap profile, every orientation realizing a failed
one-active descriptor is a strongly connected subgraph of the maximal
allowed digraph.  This module searches *all* such subgraphs without
enumerating them explicitly.

At a no-fast base carrying old reflected debt, relative active displacement
starts at zero.  The two competing events are

* ``down``: the first transition to relative displacement ``r < 0``;
* ``up``: a return to a no-fast base with ``r > 0`` before ``down``.

If the maximal graph has ``down < up``, choose one shortest down word.
Every subgraph which retains that word still has

    down(subgraph) <= down(maximal) < up(maximal) <= up(subgraph).

Consequently a counterexample subgraph must delete at least one physical
reaction in that word.  Branching on those deletions is a complete CEGAR
search.  Strong connectivity and historical consistency of the displayed
positive-debt base are rechecked after every deletion.

The population/reward CEGAR automaton is deliberately finite.  Its output
is exact only *inside that automaton*.  Separately, the architecture
certificate freezes the support partition used by the analytic
orientation-independent proof in
``research_notes/one_active_arbitrary_orientation_graph_theorem.md``.
That proof does not rely on the bounded CEGAR.  Neither layer is a
stochastic resolvent estimate or a recurrence proof.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import one_active_debt_reduction_regression as relative
import one_active_kinetic_depth as kinetic
import one_active_phase_shape as phase_shape
import one_active_remaining_structure as structure


POPULATION_BOUND = 7
HISTORICAL_DEBT_BOUND = 10
RELATIVE_REWARD_BOUND = 8
INFINITY = 10**6

FAMILY_II_ROWS_SHA256 = (
    "3642fb37f7dde46a5e0204f39851d38c167516678b4a1aae92529ec211d29d25"
)
FAMILY_II_PAIRS_SHA256 = (
    "45a1df2a3462af42aed88753720c5b20b569238b08f7b6a2ba3d1811931e4a75"
)
ARCHITECTURE_ROWS_SHA256 = (
    "15fb66321d495bbe6fc63bbdf28c17a2975eea8bb23ca0dc08f22c868ec457c2"
)


def normalized_spectator_cap(value: int) -> int:
    """Availability category for a classwise conserved spectator value."""

    if value < 0:
        raise ValueError("spectator population must be nonnegative")
    return min(value, 2)


@dataclass(frozen=True)
class ReactionEdge:
    source_node: int
    target_node: int
    linkage: int
    source_inactive: tuple[int, int]
    delta_inactive: tuple[int, int]
    delta_active: int
    source_active_degree: int


def maximal_edges(pair, descriptor) -> tuple[ReactionEdge, ...]:
    """Every descriptor-allowed nonloop reaction, with stable edge ids."""

    active, = tier._active_coordinates(descriptor)
    inactive = tuple(index for index in range(3) if index != active)
    forbidden = kinetic.forbidden_descending_edges(pair, descriptor)
    result = []
    for linkage, mask in enumerate(pair):
        for source in sorted(tier._nodes(mask)):
            for target in sorted(tier._nodes(mask)):
                if source == target or (source, target) in forbidden:
                    continue
                y = closure.COMPLEXES[source]
                z = closure.COMPLEXES[target]
                result.append(
                    ReactionEdge(
                        source,
                        target,
                        linkage,
                        tuple(y[index] for index in inactive),
                        tuple(z[index] - y[index] for index in inactive),
                        z[active] - y[active],
                        y[active],
                    )
                )
    return tuple(result)


def full_mask(edges: tuple[ReactionEdge, ...]) -> int:
    return (1 << len(edges)) - 1


def selected_edges(edges: tuple[ReactionEdge, ...], mask: int):
    return tuple(edge for index, edge in enumerate(edges) if mask >> index & 1)


def is_strong(pair, edges: tuple[ReactionEdge, ...], mask: int) -> bool:
    """Strong connectivity in each labelled linkage support."""

    for linkage, support_mask in enumerate(pair):
        nodes = frozenset(tier._nodes(support_mask))
        adjacency = {node: [] for node in nodes}
        for index, edge in enumerate(edges):
            if mask >> index & 1 and edge.linkage == linkage:
                adjacency[edge.source_node].append(edge.target_node)
        for start in nodes:
            reached = {start}
            frontier = [start]
            while frontier:
                source = frontier.pop()
                for target in adjacency[source]:
                    if target not in reached:
                        reached.add(target)
                        frontier.append(target)
            if reached != nodes:
                return False
    return True


def enabled(source: tuple[int, int], state: tuple[int, int]) -> bool:
    return source[0] <= state[0] and source[1] <= state[1]


def has_fast_clock(
    state: tuple[int, int], edges: tuple[ReactionEdge, ...]
) -> bool:
    """Fast enabledness depends on support, not on a strong orientation."""

    return any(
        edge.source_active_degree == 1
        and enabled(edge.source_inactive, state)
        for edge in edges
    )


def transitions(
    edges: tuple[ReactionEdge, ...],
    mask: int,
    state: tuple[int, int],
    *,
    population_bound: int,
):
    fast = has_fast_clock(state, edges)
    for index, edge in enumerate(edges):
        if not (mask >> index & 1) or not enabled(edge.source_inactive, state):
            continue
        endpoint = tuple(
            state[coordinate] + edge.delta_inactive[coordinate]
            for coordinate in range(2)
        )
        if not all(0 <= value <= population_bound for value in endpoint):
            continue
        cost = int(edge.source_active_degree == 0 and fast)
        yield endpoint, edge.delta_active, cost, index


def _zero_one_path(starts, neighbors, is_target):
    """Return ``(distance, edge-id word, endpoint)`` or infinity."""

    queue = deque(starts)
    distance = {state: 0 for state in starts}
    predecessor = {}
    while queue:
        state = queue.popleft()
        old = distance[state]
        if is_target(state):
            word = []
            cursor = state
            while cursor not in starts:
                previous, edge_id = predecessor[cursor]
                word.append(edge_id)
                cursor = previous
            return old, tuple(reversed(word)), state
        for endpoint, cost, edge_id in neighbors(state):
            new = old + cost
            if new >= distance.get(endpoint, INFINITY):
                continue
            distance[endpoint] = new
            predecessor[endpoint] = state, edge_id
            (queue.append if cost else queue.appendleft)(endpoint)
    return INFINITY, (), None


def historical_base_is_consistent(
    descriptor,
    edges: tuple[ReactionEdge, ...],
    mask: int,
    base: tuple[int, int],
    *,
    population_bound: int = POPULATION_BOUND,
    debt_bound: int = HISTORICAL_DEBT_BOUND,
) -> bool:
    """Bounded reachability of ``base`` with some positive reflected debt."""

    active, = tier._active_coordinates(descriptor)
    inactive_coordinates = tuple(
        coordinate for coordinate in range(3) if coordinate != active
    )
    start = tuple(descriptor.caps[c] for c in inactive_coordinates), 0
    queue = deque((start,))
    reached = {start}
    while queue:
        inactive, debt = queue.popleft()
        if inactive == base and debt > 0 and not has_fast_clock(inactive, edges):
            return True
        for endpoint, active_delta, _cost, _edge_id in transitions(
            edges, mask, inactive, population_bound=population_bound
        ):
            new_debt = debt + active_delta
            if new_debt > debt_bound:
                continue
            target = endpoint, max(0, new_debt)
            if target not in reached:
                reached.add(target)
                queue.append(target)
    return False


def relative_depths(
    edges: tuple[ReactionEdge, ...],
    mask: int,
    base: tuple[int, int],
    *,
    population_bound: int = POPULATION_BOUND,
    reward_bound: int = RELATIVE_REWARD_BOUND,
):
    """Shortest future up-return and first-down words from one base."""

    start = base, 0

    def neighbors(state):
        inactive, reward = state
        for endpoint, active_delta, cost, edge_id in transitions(
            edges, mask, inactive, population_bound=population_bound
        ):
            new_reward = reward + active_delta
            if new_reward < 0:
                yield (endpoint, -1), cost, edge_id
            elif new_reward <= reward_bound:
                yield (endpoint, new_reward), cost, edge_id

    down = _zero_one_path(
        (start,),
        neighbors,
        lambda state: state[1] < 0,
    )
    up = _zero_one_path(
        (start,),
        neighbors,
        lambda state: (
            state[1] > 0 and not has_fast_clock(state[0], edges)
        ),
    )
    return {
        "up_depth": up[0],
        "up_word": up[1],
        "up_endpoint": up[2],
        "down_depth": down[0],
        "down_word": down[1],
        "down_endpoint": down[2],
    }


def maximal_consistent_bases(
    pair,
    descriptor,
    *,
    population_bound: int = POPULATION_BOUND,
    debt_bound: int = HISTORICAL_DEBT_BOUND,
):
    edges = maximal_edges(pair, descriptor)
    mask = full_mask(edges)
    result = []
    for first in range(population_bound + 1):
        for second in range(population_bound + 1):
            base = first, second
            if has_fast_clock(base, edges):
                continue
            if historical_base_is_consistent(
                descriptor,
                edges,
                mask,
                base,
                population_bound=population_bound,
                debt_bound=debt_bound,
            ):
                result.append(base)
    return tuple(result)


def cegar_base(
    pair,
    descriptor,
    base: tuple[int, int],
    *,
    population_bound: int = POPULATION_BOUND,
    debt_bound: int = HISTORICAL_DEBT_BOUND,
    reward_bound: int = RELATIVE_REWARD_BOUND,
    node_limit: int | None = None,
):
    """Exhaust every strong allowed subgraph relevant to one bounded base."""

    edges = maximal_edges(pair, descriptor)
    initial_mask = full_mask(edges)
    memo = set()
    counters = {
        "cegar_nodes": 0,
        "inconsistent_prunes": 0,
        "nonstrong_prunes": 0,
        "shortest_word_prunes": 0,
    }

    def visit(mask):
        if mask in memo:
            return None
        memo.add(mask)
        counters["cegar_nodes"] += 1
        if node_limit is not None and counters["cegar_nodes"] > node_limit:
            return {"kind": "node_limit", "mask": mask}
        if not is_strong(pair, edges, mask):
            counters["nonstrong_prunes"] += 1
            return None
        if not historical_base_is_consistent(
            descriptor,
            edges,
            mask,
            base,
            population_bound=population_bound,
            debt_bound=debt_bound,
        ):
            counters["inconsistent_prunes"] += 1
            return None
        row = relative_depths(
            edges,
            mask,
            base,
            population_bound=population_bound,
            reward_bound=reward_bound,
        )
        if row["down_depth"] >= INFINITY or row["up_depth"] <= row["down_depth"]:
            return {
                "kind": "counterexample",
                "mask": mask,
                "orientation": tuple(
                    (edge.source_node, edge.target_node)
                    for edge in selected_edges(edges, mask)
                ),
                **row,
            }

        # Every violating subgraph must delete at least one edge in this
        # retained shortest-down word.  Branch only on those deletions.
        branch_edges = tuple(sorted(set(row["down_word"])))
        assert branch_edges
        counters["shortest_word_prunes"] += 1
        for edge_id in branch_edges:
            result = visit(mask & ~(1 << edge_id))
            if result is not None:
                return result
        return None

    counterexample = visit(initial_mask)
    return {
        **counters,
        "base": base,
        "edges": len(edges),
        "counterexample": counterexample,
        "bounded_arbitrary_orientation_pass": counterexample is None,
    }


def excluded_equality_example():
    """The sharp equality graph outside the all-one-active selector."""

    return {
        "supports": [["0", "BC"], ["A", "B", "AB", "2B"]],
        "active": "C",
        "caps": [0, 0],
        "orientation": [
            "0->BC",
            "BC->0",
            "B->A",
            "A->AB",
            "AB->2B",
            "2B->B",
        ],
        "base": [0, 0],
        "future_up_depth": 2,
        "future_down_depth": 2,
        "feasible_active_dimensions": [1, 2],
        "inside_candidate_1227": False,
    }


def family_ii_axis_incidences():
    """The exact lower-only/single-top-cofactor incidence family.

    After relabelling the active coordinate to ``C``, its only fast source
    is ``BC``.  Thus the no-fast set is the apparent spectator axis
    ``B=0``.  The finite atlas in fact leaves only the five supports listed
    below; their linkage invariants fix the spectator classwise.  The
    stored cap is only the availability representative min(a_Gamma, 2),
    so representative 2 includes every fixed invariant a_Gamma >= 2.
    """

    rows = []
    pairs = set()
    for pair, descriptor in phase_shape.candidate_incidences():
        normalized = structure._normalized(pair, descriptor)
        supports = tuple(normalized["supports"])
        phases = tuple(
            structure._linkage_phase(support) for support in supports
        )
        if {kind for kind, _ in phases} != {"lower_only", "mixed_killed"}:
            continue
        mixed = tuple(
            stripped
            for kind, stripped in phases
            if kind == "mixed_killed"
        )
        if mixed != (("B",),):
            continue
        assert not kinetic.forbidden_descending_edges(pair, descriptor)
        rows.append(
            {
                "pair": closure.pair_payload(pair),
                "weight": descriptor.weight,
                "caps": descriptor.caps,
                "supports": supports,
                "normalized_caps": tuple(normalized["caps"]),
                "phase": phases,
            }
        )
        pairs.add(pair)
    return tuple(
        sorted(rows, key=lambda row: json.dumps(row, sort_keys=True))
    ), frozenset(pairs)


def family_ii_axis_certificate():
    """Finite support certificate for the analytic Family-II lemma."""

    rows, pairs = family_ii_axis_incidences()
    encoded = json.dumps(
        rows, sort_keys=True, separators=(",", ":")
    ).encode()
    profiles = tuple(
        sorted(
            {
                (row["supports"], row["normalized_caps"])
                for row in rows
            }
        )
    )
    support_types = tuple(sorted({row["supports"] for row in rows}))
    result = {
        "claim_scope": (
            "finite support classification plus the analytic arbitrary-"
            "strong-orientation relative-debt lemma; no stopped-kernel or "
            "recurrence conclusion"
        ),
        "incidences": len(rows),
        "physical_pairs": len(pairs),
        "normalized_profiles": len(profiles),
        "normalized_support_types": len(support_types),
        "rows_sha256": sha256(encoded).hexdigest(),
        "pairs_sha256": closure.pair_fingerprint(pairs),
        "profiles": profiles,
        "arbitrary_strong_orientation_relative_down_depth": 0,
        "arbitrary_strong_orientation_relative_up_depth_lower_bound": 1,
        "spectator_is_linkage_invariant": True,
        "normalized_cap_semantics": (
            "cap 0 means a_Gamma=0; cap 1 means a_Gamma=1; "
            "cap 2 means arbitrary fixed a_Gamma>=2"
        ),
        "graph_resistance_lemma_certified": True,
        "aggregate_kernel_certified": False,
        "pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    assert result["incidences"] == 30
    assert result["physical_pairs"] == 10
    assert result["normalized_profiles"] == 15
    assert result["normalized_support_types"] == 5
    assert result["rows_sha256"] == FAMILY_II_ROWS_SHA256
    assert result["pairs_sha256"] == FAMILY_II_PAIRS_SHA256
    return result


def _swap_inactive_name(name: str) -> str:
    vector = closure.COMPLEXES[closure.NAME_TO_INDEX[name]]
    swapped = (vector[1], vector[0], vector[2])
    return closure.NAMES[closure.COMPLEXES.index(swapped)]


def _family_i_category(supports, phases) -> str:
    mixed_side, = (
        side
        for side, (kind, stripped) in enumerate(phases)
        if kind == "mixed_killed" and set(stripped) == {"A", "B"}
    )
    lower_side = 1 - mixed_side
    mixed_lower = tuple(
        name for name in supports[mixed_side] if name not in structure.TOP_MENU
    )
    lower_support = supports[lower_side]
    if "0" in lower_support or (
        "0" in mixed_lower and len(mixed_lower) > 1
    ):
        return "family_i_origin_down_0"
    if "0" not in lower_support and "0" not in mixed_lower:
        return "family_i_origin_no_history"
    assert mixed_lower == ("0",) and "0" not in lower_support
    # The finite selector leaves exactly the nine unary/quadratic supports
    # used by the cut proof in the analytic note.
    degrees = {
        sum(closure.COMPLEXES[closure.NAME_TO_INDEX[name]])
        for name in lower_support
    }
    assert 1 in degrees and 2 in degrees
    return "family_i_origin_down_1"


def _family_ii_category(supports, normalized_caps) -> str:
    if supports[0] == ("A", "AB"):
        a = normalized_caps[0]
        if a > 0 or "0" in supports[1]:
            return "family_ii_axis_down_0"
        return "family_ii_axis_no_history"
    assert supports == (("A", "BC"), ("2A", "2B", "AB"))
    return (
        "family_ii_axis_down_0"
        if normalized_caps[0] == 2
        else "family_ii_axis_no_history"
    )


def _family_iii_category(supports, phases) -> str:
    lower = tuple(
        tuple(name for name in support if name not in structure.TOP_MENU)
        for support in supports
    )
    zero_sides = tuple(
        side for side, support in enumerate(lower) if "0" in support
    )
    if not zero_sides:
        return "family_iii_origin_no_history"
    if any(len(lower[side]) > 1 for side in zero_sides):
        return "family_iii_origin_down_0"
    if len(zero_sides) == 2:
        # This alternative is absent from the residual table, but its two
        # carrier pairs can only make neutral origin returns.
        return "family_iii_origin_no_history"

    zero_side, = zero_sides
    other_side = 1 - zero_side
    assert lower[zero_side] == ("0",)
    other_lower = lower[other_side]
    exact_cofactor, = phases[zero_side][1]
    if exact_cofactor == "B":
        other_lower = tuple(
            _swap_inactive_name(name) for name in other_lower
        )
    support = set(other_lower)
    assert "0" not in support
    if "A" in support:
        if len(support) == 1:
            return "family_iii_origin_no_history"
        return "family_iii_origin_down_1"
    if "2A" in support:
        return "family_iii_origin_down_2"
    return "family_iii_origin_no_history"


def _whole_top_category(supports, phases) -> str:
    """Route the neutral ``C<->AC`` phase without truncating its A-tail."""

    whole_side, = (
        side for side, (kind, _stripped) in enumerate(phases)
        if kind == "whole_top"
    )
    mixed_side = 1 - whole_side
    assert supports[whole_side] == ("C", "AC")
    mixed_support = supports[mixed_side]
    assert tuple(
        name for name in mixed_support if name in structure.TOP_MENU
    ) == ("BC",)
    pure_a = tuple(
        name for name in mixed_support if name in {"0", "A", "2A"}
    )
    b_lower = tuple(
        name for name in mixed_support if name in {"B", "AB", "2B"}
    )
    assert b_lower
    if pure_a:
        return "open_wholly_top_down_1"
    # At B=0 the whole-top linkage changes only A, while every source in
    # the mixed linkage requires B.  The face is closed and cannot acquire
    # historical positive C-debt.
    return "open_wholly_top_no_history"


def graph_architecture_rows():
    """Classify all 3,297 candidate incidences without an orientation box."""

    rows = []
    for pair, descriptor in phase_shape.candidate_incidences():
        normalized = structure._normalized(pair, descriptor)
        supports = tuple(normalized["supports"])
        caps = tuple(normalized["caps"])
        phases = tuple(
            structure._linkage_phase(support) for support in supports
        )
        kinds = tuple(kind for kind, _ in phases)
        if "whole_top" in kinds:
            category = _whole_top_category(supports, phases)
        elif any("0" in stripped for _kind, stripped in phases):
            category = "mixed_C_source_direct_down_0"
        elif set(kinds) == {"lower_only", "mixed_killed"}:
            mixed_stripped, = (
                stripped
                for kind, stripped in phases
                if kind == "mixed_killed"
            )
            if set(mixed_stripped) == {"A", "B"}:
                category = _family_i_category(supports, phases)
            else:
                assert len(mixed_stripped) == 1
                category = _family_ii_category(supports, caps)
        else:
            assert kinds == ("mixed_killed", "mixed_killed")
            assert {phases[0][1], phases[1][1]} == {("A",), ("B",)}
            category = _family_iii_category(supports, phases)
        rows.append(
            {
                "pair": closure.pair_payload(pair),
                "weight": descriptor.weight,
                "caps": descriptor.caps,
                "normalized_supports": supports,
                "normalized_caps": caps,
                "phase": phases,
                "graph_category": category,
            }
        )
    return tuple(
        sorted(rows, key=lambda row: json.dumps(row, sort_keys=True))
    )


def population_five_counterexample():
    """A shortest depth-two service which genuinely reaches ``B=5``."""

    state = [0, 0]
    reward = 0
    cost = 0
    trace = []
    word = (
        ("0", "AC"),
        ("0", "AC"),
        ("2A", "BC"),
        ("BC", "2B"),
        ("BC", "2B"),
        ("BC", "2B"),
        ("BC", "2B"),
    )
    for source_name, target_name in word:
        source = closure.COMPLEXES[closure.NAME_TO_INDEX[source_name]]
        target = closure.COMPLEXES[closure.NAME_TO_INDEX[target_name]]
        source_inactive = source[:2]
        assert all(source_inactive[i] <= state[i] for i in range(2))
        fast = state[0] + state[1] > 0
        if source[2] == 0 and fast:
            cost += 1
        state = [
            state[i] + target[i] - source[i] for i in range(2)
        ]
        reward += target[2] - source[2]
        trace.append(
            {
                "edge": f"{source_name}->{target_name}",
                "inactive": tuple(state),
                "relative_reward": reward,
                "cost": cost,
            }
        )
    assert state == [0, 5]
    assert reward == -1 and cost == 2
    return {
        "supports": (("0", "AC"), ("2A", "2B", "AB", "BC")),
        "strong_orientation": (
            "0->AC",
            "AC->0",
            "2A->BC",
            "BC->2B",
            "2B->AB",
            "AB->2A",
        ),
        "word": tuple(f"{source}->{target}" for source, target in word),
        "trace": tuple(trace),
        "maximum_inactive_population": 5,
        "population_bound_four_valid": False,
    }


def graph_architecture_certificate():
    """Exact finite routing table for the arbitrary-orientation proof."""

    rows = graph_architecture_rows()
    histogram = {}
    for row in rows:
        category = row["graph_category"]
        histogram[category] = histogram.get(category, 0) + 1
    histogram = dict(sorted(histogram.items()))
    expected = {
        "family_i_origin_down_0": 710,
        "family_i_origin_down_1": 75,
        "family_i_origin_no_history": 185,
        "family_ii_axis_down_0": 24,
        "family_ii_axis_no_history": 6,
        "family_iii_origin_down_0": 234,
        "family_iii_origin_down_1": 40,
        "family_iii_origin_down_2": 16,
        "family_iii_origin_no_history": 90,
        "mixed_C_source_direct_down_0": 1695,
        "open_wholly_top_down_1": 210,
        "open_wholly_top_no_history": 12,
    }
    assert histogram == expected
    direct_phase_histogram = {}
    for row in rows:
        if row["graph_category"] != "mixed_C_source_direct_down_0":
            continue
        kinds = tuple(kind for kind, _stripped in row["phase"])
        label = {
            ("lower_only", "mixed_killed"): "lower_only_plus_mixed",
            ("mixed_killed", "mixed_killed"): "two_mixed",
        }[kinds]
        direct_phase_histogram[label] = (
            direct_phase_histogram.get(label, 0) + 1
        )
    direct_phase_histogram = dict(sorted(direct_phase_histogram.items()))
    assert direct_phase_histogram == {
        "lower_only_plus_mixed": 1030,
        "two_mixed": 665,
    }
    open_rows = tuple(
        row for row in rows
        if row["graph_category"].startswith("open_wholly_top_")
    )
    open_supports = {
        row["normalized_supports"] for row in open_rows
    }
    open_down_supports = {
        row["normalized_supports"] for row in open_rows
        if row["graph_category"] == "open_wholly_top_down_1"
    }
    open_no_history_supports = open_supports - open_down_supports
    assert (len(open_supports), len(open_down_supports), len(open_no_history_supports)) == (
        37,
        35,
        2,
    )
    encoded = json.dumps(
        rows, sort_keys=True, separators=(",", ":")
    ).encode()
    digest = sha256(encoded).hexdigest()
    if ARCHITECTURE_ROWS_SHA256 != "TO_BE_FILLED":
        assert digest == ARCHITECTURE_ROWS_SHA256
    counterexample = population_five_counterexample()
    assert counterexample["supports"] in {
        row["normalized_supports"] for row in rows
    }
    return {
        "claim_scope": (
            "finite exact architecture routing plus analytic relative-"
            "resistance theorem; aggregate kernels and recurrence remain open"
        ),
        "candidate_pairs": len(phase_shape.candidate_pairs()),
        "candidate_incidences": len(rows),
        "category_histogram": histogram,
        "rows_sha256": digest,
        "relative_down_depth_upper_bound": 2,
        "same_base_up_depth_is_strictly_larger": True,
        "direct_C_phase_histogram": direct_phase_histogram,
        "wholly_top_phase_histogram": {
            "depth_one": 210,
            "no_history": 12,
        },
        "wholly_top_normalized_support_types": {
            "total": len(open_supports),
            "depth_one": len(open_down_supports),
            "no_history": len(open_no_history_supports),
        },
        "finite_mixed_carrier_bound": {
            "inactive_mass": "M_t <= M_0 + 3*K + 4",
            "family_ii_initial_mass": (
                "M_0=a_Gamma is arbitrary but fixed on the class"
            ),
            "active_overshoot": "r_plus <= K + 1",
            "boundary_above_M0_plus_10_requires_interruptions": 3,
            "weighted_green_bound_certified": False,
        },
        "arbitrary_strong_orientation_graph_theorem_certified": True,
        "population_five_counterexample": counterexample,
        "aggregate_kernel_certified": False,
        "promotion_contract_certified": False,
        "pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }


def scope_payload():
    """Fast metadata; the full CEGAR replay is intentionally separate."""

    candidates = phase_shape.candidate_pairs()
    incidences = phase_shape.candidate_incidences()
    payload = {
        "claim_scope": (
            "CEGAR algorithm exact for arbitrary strong allowed orientations "
            "inside a bounded population/reward automaton; no small-witness "
            "or stochastic recurrence theorem"
        ),
        "candidate_pairs": len(candidates),
        "candidate_incidences": len(incidences),
        "population_bound": POPULATION_BOUND,
        "historical_debt_bound": HISTORICAL_DEBT_BOUND,
        "relative_reward_bound": RELATIVE_REWARD_BOUND,
        "excluded_equality_example": excluded_equality_example(),
        "family_ii_axis": family_ii_axis_certificate(),
        "graph_architecture": graph_architecture_certificate(),
        "bounded_cegar_full_replay_frozen": False,
        "petri_net_small_witness_certified": False,
        "arbitrary_orientation_analytic_theorem_certified": False,
        "pair_recurrence_certified": False,
        "global_t3_2_certified": False,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return {**payload, "payload_sha256": sha256(encoded).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(scope_payload(), indent=2, sort_keys=True))
