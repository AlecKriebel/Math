"""Fast certificates obstructing equality alpha = gamma-infinity."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from verifier_a.core import BitGraph, alpha


def _mask(vertices: tuple[int, ...]) -> int:
    result = 0
    for vertex in vertices:
        result |= 1 << vertex
    return result


def _vertex(bit: int) -> int:
    return bit.bit_length() - 1


@dataclass(frozen=True, slots=True)
class FailedGuard:
    guard: int
    newly_undominated: int


@dataclass(frozen=True, slots=True)
class PrivateObstruction:
    independent_set: int
    attack: int
    failed_guards: tuple[FailedGuard, ...]


def maximum_independent_masks(graph: BitGraph) -> tuple[int, ...]:
    cardinality = alpha(graph)
    return tuple(
        candidate
        for vertices in combinations(range(graph.n), cardinality)
        if graph.is_independent(candidate := _mask(vertices))
    )


def private_region(graph: BitGraph, dominating: int, guard: int) -> int:
    """Vertices whose unique dominator in ``dominating`` is ``guard``."""

    guard_bit = 1 << guard
    result = 0
    for vertex, closed in enumerate(graph.closed):
        if closed & dominating == guard_bit:
            result |= 1 << vertex
    return result


def find_private_obstruction(graph: BitGraph) -> PrivateObstruction | None:
    """Find a maximum independent state with an undefendable first attack."""

    for independent in maximum_independent_masks(graph):
        unoccupied = graph.full ^ independent
        while unoccupied:
            attacked_bit = unoccupied & -unoccupied
            attacked = _vertex(attacked_bit)
            failed: list[FailedGuard] = []
            possible = independent & graph.adj[attacked]
            scanning = possible
            while scanning:
                guard_bit = scanning & -scanning
                guard = _vertex(guard_bit)
                uncovered = private_region(graph, independent, guard) & ~graph.closed[
                    attacked
                ]
                if not uncovered:
                    break
                failed.append(
                    FailedGuard(guard, _vertex(uncovered & -uncovered))
                )
                scanning ^= guard_bit
            else:
                # A maximum independent set is maximal and hence dominating,
                # so ``possible`` is nonempty. Every possible guard has now
                # received an explicit newly-undominated witness.
                return PrivateObstruction(
                    independent, attacked, tuple(failed)
                )
            unoccupied ^= attacked_bit
    return None


def verify_private_obstruction(
    graph: BitGraph, obstruction: PrivateObstruction
) -> bool:
    """Directly verify a lower-bound certificate without eternal search."""

    if not isinstance(obstruction, PrivateObstruction):
        return False
    independent = obstruction.independent_set
    if (
        type(independent) is not int
        or independent < 0
        or independent & ~graph.full
    ):
        return False
    if independent.bit_count() != alpha(graph):
        return False
    if not graph.is_independent(independent):
        return False
    attack = obstruction.attack
    if type(attack) is not int or not 0 <= attack < graph.n:
        return False
    if independent >> attack & 1:
        return False
    possible = {
        vertex
        for vertex in range(graph.n)
        if independent >> vertex & 1
        and graph.adj[attack] >> vertex & 1
    }
    if not isinstance(obstruction.failed_guards, tuple):
        return False
    if len(obstruction.failed_guards) != len(possible):
        return False
    records: dict[int, FailedGuard] = {}
    for record in obstruction.failed_guards:
        if not isinstance(record, FailedGuard):
            return False
        guard = record.guard
        if type(guard) is not int or not 0 <= guard < graph.n:
            return False
        if guard in records:
            return False
        records[guard] = record
    if set(records) != possible:
        return False
    for guard, record in records.items():
        witness = record.newly_undominated
        if type(witness) is not int or not 0 <= witness < graph.n:
            return False
        if graph.closed[witness] & independent != 1 << guard:
            return False
        if graph.closed[attack] >> witness & 1:
            return False
        successor = (
            independent ^ (1 << guard) ^ (1 << attack)
        )
        if graph.is_dominating(successor):
            return False
    return True
