"""Definition-level graph predicates and the one-guard greatest fixed point.

This module imports no campaign search or evaluator implementation.  Graph
parsing is reused from the separately frozen ``coverage_checker.graph`` layer;
all domination, independence, transition, and deletion logic here is new.
Configurations are ordinary ``frozenset[int]`` objects, deliberately unlike
the bitset transition core used by verifier A.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations
import json
from typing import Iterable, Iterator

from coverage_checker.graph import Graph


Configuration = frozenset[int]
DeletionWitness = tuple[Configuration, int]
PrivateObstruction = tuple[int, int, tuple[tuple[int, int], ...]]


@dataclass(frozen=True, slots=True)
class FixedPointResult:
    guard_count: int
    initial_count: int
    family: frozenset[Configuration]
    deletion_rounds: tuple[tuple[DeletionWitness, ...], ...]
    trace_sha256: str


def vertices(graph: Graph) -> frozenset[int]:
    return frozenset(range(graph.order))


def is_dominating(graph: Graph, configuration: Iterable[int]) -> bool:
    state = frozenset(configuration)
    if any(type(vertex) is not int or not 0 <= vertex < graph.order for vertex in state):
        return False
    return all(
        vertex in state
        or any(graph.neighbors[vertex] & (1 << guard) for guard in state)
        for vertex in range(graph.order)
    )


def is_independent(graph: Graph, configuration: Iterable[int]) -> bool:
    state = frozenset(configuration)
    if any(type(vertex) is not int or not 0 <= vertex < graph.order for vertex in state):
        return False
    return all(
        not graph.has_edge(first, second)
        for first, second in combinations(sorted(state), 2)
    )


def mask_of(configuration: Iterable[int]) -> int:
    mask = 0
    for vertex in configuration:
        if type(vertex) is not int or vertex < 0:
            raise ValueError("configuration contains an invalid vertex")
        mask |= 1 << vertex
    return mask


def configuration_from_mask(graph: Graph, mask: int) -> Configuration:
    if (
        type(mask) is not int
        or mask < 0
        or mask & ~((1 << graph.order) - 1)
    ):
        raise ValueError("configuration mask is outside graph")
    return frozenset(
        vertex for vertex in range(graph.order) if mask & (1 << vertex)
    )


def subsets_of_size(graph: Graph, size: int) -> Iterator[Configuration]:
    if type(size) is not int or not 0 <= size <= graph.order:
        return
    for subset in combinations(range(graph.order), size):
        yield frozenset(subset)


def first_dominating_set(
    graph: Graph, minimum_size: int, maximum_size: int
) -> Configuration | None:
    if (
        type(minimum_size) is not int
        or type(maximum_size) is not int
        or minimum_size < 0
        or maximum_size < minimum_size
    ):
        raise ValueError("invalid domination witness size interval")
    for size in range(minimum_size, min(maximum_size, graph.order) + 1):
        for state in subsets_of_size(graph, size):
            if is_dominating(graph, state):
                return state
    return None


def first_independent_set(graph: Graph, size: int) -> Configuration | None:
    for state in subsets_of_size(graph, size):
        if is_independent(graph, state):
            return state
    return None


def failed_dominating_pair_witnesses(
    graph: Graph,
) -> tuple[tuple[int, int], ...] | None:
    """Return one undominated vertex for every pair, or ``None`` if one dominates."""

    witnesses: list[tuple[int, int]] = []
    for pair in subsets_of_size(graph, 2):
        if is_dominating(graph, pair):
            return None
        witness = next(
            vertex
            for vertex in range(graph.order)
            if vertex not in pair
            and not any(
                graph.neighbors[vertex] & (1 << guard) for guard in pair
            )
        )
        witnesses.append((mask_of(pair), witness))
    return tuple(witnesses)


def nonindependent_subset_witnesses(
    graph: Graph, size: int
) -> tuple[tuple[int, int, int], ...] | None:
    """Give an internal edge for every ``size``-set, or ``None`` if one is independent."""

    witnesses: list[tuple[int, int, int]] = []
    for subset in subsets_of_size(graph, size):
        edge = next(
            (
                (first, second)
                for first, second in combinations(sorted(subset), 2)
                if graph.has_edge(first, second)
            ),
            None,
        )
        if edge is None:
            return None
        witnesses.append((mask_of(subset), edge[0], edge[1]))
    return tuple(witnesses)


def witness_digest(records: Iterable[tuple[int, ...]]) -> str:
    digest = sha256()
    for record in records:
        digest.update(
            (",".join(str(value) for value in record) + "\n").encode("ascii")
        )
    return digest.hexdigest()


def find_private_obstruction(
    graph: Graph, independent_size: int
) -> PrivateObstruction | None:
    """Find the first maximum-independent-state first-attack obstruction.

    The caller proves separately that ``independent_size`` is ``alpha``.
    The returned failed-guard records give, for each guard adjacent to the
    attacked vertex, a vertex that becomes undominated after that guard moves.
    """

    for state in subsets_of_size(graph, independent_size):
        if not is_independent(graph, state):
            continue
        state_mask = mask_of(state)
        for attacked in range(graph.order):
            if attacked in state:
                continue
            failed: list[tuple[int, int]] = []
            for guard in sorted(state):
                if not graph.has_edge(guard, attacked):
                    continue
                successor = frozenset((state - {guard}) | {attacked})
                if is_dominating(graph, successor):
                    break
                undominated = next(
                    vertex
                    for vertex in range(graph.order)
                    if vertex not in successor
                    and not any(
                        graph.has_edge(vertex, occupant)
                        for occupant in successor
                    )
                )
                failed.append((guard, undominated))
            else:
                # A maximum independent set is maximal and thus dominating,
                # so at least one guard is adjacent to each unoccupied attack.
                if failed:
                    return state_mask, attacked, tuple(failed)
    return None


def verify_private_obstruction(
    graph: Graph,
    independent_size: int,
    obstruction: PrivateObstruction,
) -> bool:
    """Verify an explicit private-neighborhood obstruction directly."""

    try:
        state_mask, attacked, failed_records = obstruction
        state = configuration_from_mask(graph, state_mask)
        if (
            len(state) != independent_size
            or not is_independent(graph, state)
            or type(attacked) is not int
            or not 0 <= attacked < graph.order
            or attacked in state
        ):
            return False
        possible = {
            guard
            for guard in state
            if graph.has_edge(guard, attacked)
        }
        records = dict(failed_records)
        if (
            not possible
            or len(records) != len(failed_records)
            or set(records) != possible
        ):
            return False
        for guard, witness in records.items():
            if (
                type(guard) is not int
                or type(witness) is not int
                or not 0 <= witness < graph.order
            ):
                return False
            successor = frozenset((state - {guard}) | {attacked})
            if witness in successor or any(
                graph.has_edge(witness, occupant)
                for occupant in successor
            ):
                return False
            if is_dominating(graph, successor):
                return False
        return True
    except (TypeError, ValueError, OverflowError):
        return False


def dominating_configurations(
    graph: Graph, guard_count: int
) -> frozenset[Configuration]:
    if type(guard_count) is not int or not 0 <= guard_count <= graph.order:
        raise ValueError("guard count outside graph")
    return frozenset(
        state
        for state in subsets_of_size(graph, guard_count)
        if is_dominating(graph, state)
    )


def legal_successors(
    graph: Graph,
    state: Configuration,
    attacked: int,
    active: frozenset[Configuration] | set[Configuration],
) -> tuple[Configuration, ...]:
    """Successors under exactly one edge move to an unoccupied attack."""

    if (
        type(attacked) is not int
        or not 0 <= attacked < graph.order
        or attacked in state
    ):
        return ()
    successors: list[Configuration] = []
    for guard in sorted(state):
        if not graph.has_edge(guard, attacked):
            continue
        successor = frozenset((state - {guard}) | {attacked})
        if successor in active and is_dominating(graph, successor):
            successors.append(successor)
    return tuple(successors)


def _trace_digest(
    rounds: Iterable[Iterable[DeletionWitness]],
) -> str:
    digest = sha256()
    for round_index, round_records in enumerate(rounds):
        for state, attack in round_records:
            payload = [round_index, mask_of(state), attack]
            digest.update(
                json.dumps(payload, separators=(",", ":")).encode("ascii")
                + b"\n"
            )
    return digest.hexdigest()


def greatest_fixed_point(graph: Graph, guard_count: int) -> FixedPointResult:
    """Compute the greatest closed family by simultaneous deletion rounds."""

    active: set[Configuration] = set(
        dominating_configurations(graph, guard_count)
    )
    initial_count = len(active)
    rounds: list[tuple[DeletionWitness, ...]] = []
    all_vertices = vertices(graph)
    while active:
        frozen_active = frozenset(active)
        doomed: list[DeletionWitness] = []
        for state in sorted(active, key=mask_of):
            for attacked in sorted(all_vertices - state):
                if not legal_successors(
                    graph, state, attacked, frozen_active
                ):
                    doomed.append((state, attacked))
                    break
        if not doomed:
            break
        round_record = tuple(doomed)
        rounds.append(round_record)
        active.difference_update(state for state, _attack in round_record)
    frozen_rounds = tuple(rounds)
    return FixedPointResult(
        guard_count=guard_count,
        initial_count=initial_count,
        family=frozenset(active),
        deletion_rounds=frozen_rounds,
        trace_sha256=_trace_digest(frozen_rounds),
    )


def serialize_deletion_rounds(
    rounds: Iterable[Iterable[DeletionWitness]],
) -> list[list[list[int]]]:
    return [
        [[mask_of(state), attacked] for state, attacked in round_records]
        for round_records in rounds
    ]


def deserialize_deletion_rounds(
    graph: Graph, payload: object
) -> tuple[tuple[DeletionWitness, ...], ...]:
    if not isinstance(payload, list):
        raise ValueError("deletion rounds must be an array")
    rounds: list[tuple[DeletionWitness, ...]] = []
    for round_payload in payload:
        if not isinstance(round_payload, list) or not round_payload:
            raise ValueError("each deletion round must be a nonempty array")
        records: list[DeletionWitness] = []
        for record in round_payload:
            if (
                not isinstance(record, list)
                or len(record) != 2
                or type(record[0]) is not int
                or type(record[1]) is not int
            ):
                raise ValueError("malformed deletion record")
            state = configuration_from_mask(graph, record[0])
            records.append((state, record[1]))
        rounds.append(tuple(records))
    return tuple(rounds)


def verify_empty_fixed_point_trace(
    graph: Graph,
    guard_count: int,
    rounds: Iterable[Iterable[DeletionWitness]],
    expected_trace_sha256: str | None = None,
) -> bool:
    """Replay a complete simultaneous deletion trace and require emptiness."""

    try:
        active: set[Configuration] = set(
            dominating_configurations(graph, guard_count)
        )
        normalized_rounds = tuple(tuple(record for record in round_) for round_ in rounds)
        if expected_trace_sha256 is not None and (
            not isinstance(expected_trace_sha256, str)
            or _trace_digest(normalized_rounds) != expected_trace_sha256
        ):
            return False
        all_vertices = vertices(graph)
        for round_records in normalized_rounds:
            if not round_records:
                return False
            frozen_active = frozenset(active)
            removed: set[Configuration] = set()
            for state, attack in round_records:
                if (
                    state not in active
                    or state in removed
                    or type(attack) is not int
                    or attack not in all_vertices - state
                    or legal_successors(
                        graph, state, attack, frozen_active
                    )
                ):
                    return False
                removed.add(state)
            active.difference_update(removed)
        return not active
    except (TypeError, ValueError, OverflowError):
        return False
