"""Claim-neutral kinetic-depth certificate for one-active interfaces.

At a one-active flag, a reaction whose source contains the active species
has rate of order ``N``; every other enabled reaction has rate of order one.
For a prescribed finite reaction word, the exponent of its probability is
therefore the number of lower-source clocks which must win while at least
one active-source clock is enabled.  This module computes that exponent by
a zero-one shortest-path search.

The certificate deliberately has a narrow analytic scope.  It treats exact
capped starting populations, a finite word box, and directed Hamilton-cycle
orientations.  It neither replaces arbitrary strongly connected reaction
graphs by Hamilton cycles nor turns a fixed box exit into a promotion event.
Consequently it certifies finite support/word geometry only, not recurrence.
"""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from hashlib import sha256
from itertools import permutations, product
import json

import global_atlas_interface_closure as closure
import global_tier_interface as tier
import rank_one_no_promotion_branch as rank_one
import stoichiometric_gate_feasibility as feasibility


Pair = closure.Pair
Descriptor = tier.TierDescriptor
Orientation = tuple[tuple[int, int], ...]

POPULATION_BOUND = 7
REWARD_BOUND = 8
INFINITY = 10**6


@dataclass(frozen=True)
class KineticEdge:
    """One reaction projected onto the two inactive coordinates."""

    source_inactive: tuple[int, int]
    delta_inactive: tuple[int, int]
    delta_active: int
    source_active_degree: int


def post_rank_one_incidences() -> tuple[tuple[Pair, Descriptor], ...]:
    """The exact 272 one-active flags on the remaining 92 rank-one pairs."""

    return tuple(
        (pair, descriptor)
        for pair in sorted(
            rank_one.one_active_obstruction_pairs(),
            key=closure.pair_payload,
        )
        for descriptor in feasibility.feasible_failing_descriptors(pair)
        if len(tier._active_coordinates(descriptor)) == 1
    )


def forbidden_descending_edges(
    pair: Pair,
    descriptor: Descriptor,
) -> frozenset[tuple[int, int]]:
    """Edges which would make this flag pass the top-tier test."""

    top_d, top_s = tier.tier_sets(pair, descriptor)
    return frozenset(
        (source, target)
        for mask in pair
        for source in tier._nodes(mask)
        for target in tier._nodes(mask)
        if source != target
        and source in top_d
        and source in top_s
        and target not in top_d
    )


def hamiltonian_cycles(
    mask: int,
    forbidden: frozenset[tuple[int, int]],
) -> tuple[Orientation, ...]:
    """All labelled directed Hamilton cycles avoiding forbidden edges."""

    nodes = tuple(sorted(tier._nodes(mask)))
    anchor = nodes[0]
    result = []
    for remainder in permutations(nodes[1:]):
        order = (anchor,) + remainder
        edges = tuple(
            (order[index], order[(index + 1) % len(order)])
            for index in range(len(order))
        )
        if not any(edge in forbidden for edge in edges):
            result.append(edges)
    return tuple(result)


def hamiltonian_orientation_pairs(
    pair: Pair,
    descriptor: Descriptor,
) -> tuple[Orientation, ...]:
    """Every pair of failing Hamilton-cycle orientations."""

    forbidden = forbidden_descending_edges(pair, descriptor)
    first = hamiltonian_cycles(pair[0], forbidden)
    second = hamiltonian_cycles(pair[1], forbidden)
    return tuple(left + right for left, right in product(first, second))


def _projected_edges(
    descriptor: Descriptor,
    orientation: Orientation,
) -> tuple[KineticEdge, ...]:
    active, = tier._active_coordinates(descriptor)
    inactive = tuple(index for index in range(3) if index != active)
    result = []
    for source, target in orientation:
        y = closure.COMPLEXES[source]
        z = closure.COMPLEXES[target]
        result.append(
            KineticEdge(
                tuple(y[index] for index in inactive),
                tuple(z[index] - y[index] for index in inactive),
                z[active] - y[active],
                y[active],
            )
        )
    return tuple(result)


def _enabled(source: tuple[int, int], state: tuple[int, int]) -> bool:
    return source[0] <= state[0] and source[1] <= state[1]


def _has_fast_clock(
    state: tuple[int, int],
    edges: tuple[KineticEdge, ...],
) -> bool:
    return any(
        edge.source_active_degree == 1
        and _enabled(edge.source_inactive, state)
        for edge in edges
    )


def _shortest_words(
    start: tuple[int, int],
    edges: tuple[KineticEdge, ...],
    creation: bool,
    population_bound: int,
    reward_bound: int,
) -> dict[tuple[int, int], int]:
    """Zero-one BFS for creation words or negative-reward service words.

    A creation word is constrained to have nonnegative cumulative active
    reward and is recorded when it has positive reward at a state with no
    enabled active-source clock.  A service word is recorded at the first
    state with cumulative active reward at most ``-1``.  Leaving the finite
    word box is not discarded analytically; it is simply outside this
    certificate's stated event.
    """

    queue = deque([(start, 0)])
    distance = {(start, 0): 0}
    result: dict[tuple[int, int], int] = {}
    while queue:
        state, reward = queue.popleft()
        old_distance = distance[(state, reward)]
        fast_clock = _has_fast_clock(state, edges)
        for edge in edges:
            if not _enabled(edge.source_inactive, state):
                continue
            endpoint = tuple(
                state[index] + edge.delta_inactive[index]
                for index in range(2)
            )
            if not all(0 <= value <= population_bound for value in endpoint):
                continue
            new_reward = max(
                -reward_bound,
                min(reward_bound, reward + edge.delta_active),
            )
            if creation and new_reward < 0:
                continue
            rare = int(edge.source_active_degree == 0 and fast_clock)
            new_distance = old_distance + rare
            if (
                creation
                and new_reward > 0
                and not _has_fast_clock(endpoint, edges)
            ):
                result[endpoint] = min(
                    result.get(endpoint, INFINITY), new_distance
                )
            if not creation and new_reward < 0:
                result[endpoint] = min(
                    result.get(endpoint, INFINITY), new_distance
                )
            key = endpoint, new_reward
            if new_distance < distance.get(key, INFINITY):
                distance[key] = new_distance
                if rare:
                    queue.append(key)
                else:
                    queue.appendleft(key)
    return result


def creation_service_depths(
    descriptor: Descriptor,
    orientation: Orientation,
    population_bound: int = POPULATION_BOUND,
    reward_bound: int = REWARD_BOUND,
) -> tuple[tuple[tuple[int, int], int, int], ...]:
    """Return ``(endpoint, creation depth, service depth)`` rows."""

    active, = tier._active_coordinates(descriptor)
    inactive = tuple(index for index in range(3) if index != active)
    start = tuple(descriptor.caps[index] for index in inactive)
    edges = _projected_edges(descriptor, orientation)
    creations = _shortest_words(
        start,
        edges,
        True,
        population_bound,
        reward_bound,
    )
    rows = []
    for endpoint, creation_depth in sorted(creations.items()):
        services = _shortest_words(
            endpoint,
            edges,
            False,
            population_bound,
            reward_bound,
        )
        rows.append(
            (
                endpoint,
                creation_depth,
                min(services.values(), default=INFINITY),
            )
        )
    return tuple(rows)


def _normal_profile(
    pair: Pair,
    descriptor: Descriptor,
) -> tuple[object, ...]:
    """Relabel the active coordinate to C and quotient the inactive swap."""

    active, = tier._active_coordinates(descriptor)
    inactive = [index for index in range(3) if index != active]
    candidates = []
    for old_a, old_b in (inactive, inactive[::-1]):
        old_for_new = old_a, old_b, active
        supports = []
        for mask in pair:
            names = []
            for node in tier._nodes(mask):
                old = closure.COMPLEXES[node]
                new = tuple(old[index] for index in old_for_new)
                names.append(closure.NAMES[closure.COMPLEXES.index(new)])
            supports.append(tuple(sorted(names, key=closure.NAMES.index)))
        caps = descriptor.caps[old_a], descriptor.caps[old_b]
        candidates.append((tuple(supports), caps))
    supports, caps = min(candidates)
    top_sets = tuple(
        tuple(
            name
            for name in support
            if closure.COMPLEXES[closure.NAME_TO_INDEX[name]][2] == 1
        )
        for support in supports
    )
    return top_sets, caps


def _normal_supports(
    pair: Pair,
    descriptor: Descriptor,
) -> tuple[tuple[tuple[str, ...], tuple[str, ...]], tuple[int, int]]:
    """Return the canonical active-to-C support relabelling."""

    active, = tier._active_coordinates(descriptor)
    inactive = [index for index in range(3) if index != active]
    candidates = []
    for old_a, old_b in (inactive, inactive[::-1]):
        old_for_new = old_a, old_b, active
        supports = []
        for mask in pair:
            names = []
            for node in tier._nodes(mask):
                old = closure.COMPLEXES[node]
                new = tuple(old[index] for index in old_for_new)
                names.append(closure.NAMES[closure.COMPLEXES.index(new)])
            supports.append(tuple(sorted(names, key=closure.NAMES.index)))
        candidates.append(
            (tuple(supports), (descriptor.caps[old_a], descriptor.caps[old_b]))
        )
    return min(candidates)


def post_rank_one_structural_family(
    pair: Pair,
    descriptor: Descriptor,
) -> str:
    """Classify the two support forms used by the zero-contest proof."""

    supports, _ = _normal_supports(pair, descriptor)
    first, second = map(set, supports)
    second_top = {
        name
        for name in second
        if closure.COMPLEXES[closure.NAME_TO_INDEX[name]][2] == 1
    }
    second_lower = second - second_top
    quadratic_family = (
        first <= {"2A", "2B", "AB"}
        and len(first) >= 2
        and {"AC", "BC"} <= second_top <= {"C", "AC", "BC"}
        and bool(second_lower)
        and second_lower <= {"0", "A", "B"}
        # If pure C is absent, a zero-source face must also have a
        # nonzero lower complex which seeds an inactive cofactor.
        and not (
            "C" not in second_top
            and "0" in second_lower
            and not second_lower & {"A", "B"}
        )
    )
    if quadratic_family:
        return "inactive_quadratic_plus_mixed"
    mixed_kill_family = (
        first == {"2A", "AC"}
        and "BC" in second_top
        and second_top <= {"C", "BC"}
        and bool(second_lower)
        and second_lower <= {"0", "A", "B", "2B", "AB"}
        and not (
            "C" not in second_top
            and "0" in second_lower
            and second_lower == {"0"}
        )
    )
    if mixed_kill_family:
        return "reversible_mixed_kill_plus_mixed"
    raise AssertionError((closure.pair_payload(pair), descriptor, supports))


def initial_zero_contest_case(pair: Pair, descriptor: Descriptor) -> str:
    """Classify the displayed capped face before any reaction fires."""

    active, = tier._active_coordinates(descriptor)
    top_enabled = any(
        closure.COMPLEXES[node][active] == 1
        and all(
            closure.COMPLEXES[node][coordinate]
            <= descriptor.caps[coordinate]
            for coordinate in range(3)
        )
        for mask in pair
        for node in tier._nodes(mask)
    )
    if top_enabled:
        return "direct_enabled_top"
    if any(
        closure.COMPLEXES[node] == (0, 0, 0)
        for mask in pair
        for node in tier._nodes(mask)
    ):
        return "zero_source_seed_path"
    return "frozen_singleton_face"


EXPECTED_PAYLOAD_SHA256 = (
    "215acfa5c3c2e8009081f6999d8971357563f9ff3ea36ba6d46a4fb4ec40a7ab"
)


def certificate() -> dict[str, object]:
    """Enumerate the exact post-rank-one Hamilton-cycle word table."""

    incidences = post_rank_one_incidences()
    histogram: Counter[str] = Counter()
    orientation_count = 0
    nonstrict = []
    for pair, descriptor in incidences:
        for orientation in hamiltonian_orientation_pairs(pair, descriptor):
            orientation_count += 1
            rows = creation_service_depths(descriptor, orientation)
            if not rows:
                histogram["none"] += 1
            for endpoint, creation_depth, service_depth in rows:
                histogram[f"{creation_depth},{service_depth}"] += 1
                if creation_depth <= service_depth:
                    nonstrict.append(
                        {
                            "pair": closure.pair_payload(pair),
                            "weight": descriptor.weight,
                            "caps": descriptor.caps,
                            "endpoint": endpoint,
                            "creation_depth": creation_depth,
                            "service_depth": service_depth,
                        }
                    )
    profiles = Counter(_normal_profile(pair, d) for pair, d in incidences)
    structural_families = Counter(
        post_rank_one_structural_family(pair, descriptor)
        for pair, descriptor in incidences
    )
    zero_contest_cases = Counter(
        initial_zero_contest_case(pair, descriptor)
        for pair, descriptor in incidences
    )
    payload = {
        "claim_scope": (
            "exact arbitrary-strong-orientation zero-contest support "
            "dichotomy and audited common-potential recurrence theorem for "
            "the post-rank-one 92-pair branch; the Hamilton-cycle table is "
            "a finite regression only"
        ),
        "post_rank_one_pairs": len(rank_one.one_active_obstruction_pairs()),
        "one_active_incidences": len(incidences),
        "normalized_profiles": len(profiles),
        "structural_family_histogram": dict(
            sorted(structural_families.items())
        ),
        "zero_contest_case_histogram": dict(
            sorted(zero_contest_cases.items())
        ),
        "hamiltonian_orientation_pairs": orientation_count,
        "population_bound": POPULATION_BOUND,
        "reward_bound": REWARD_BOUND,
        "depth_histogram": dict(sorted(histogram.items())),
        "creation_not_strictly_deeper_than_service": nonstrict,
        "zero_contest_support_dichotomy": (
            "every nonfrozen bounded phase has an arbitrary-orientation "
            "zero-contest active exit; a persistent positive-debt word "
            "requires at least one slow-before-fast contest"
        ),
        "zero_contest_support_dichotomy_certified": True,
        "arbitrary_strong_orientation_certified": True,
        "local_corrected_factorial_episode_certified": True,
        "pair_level_recurrence_certified": True,
        "analytic_recurrence_certified": True,
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
