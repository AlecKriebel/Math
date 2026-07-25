"""Independent bit-mask proofs for domination and one-guard non-eternality.

This module deliberately shares no transition or predicate implementation with
the edge-toggle search, verifier A, verifier B, or ``evaluation_checker``.
Only the frozen strict graph6 ``Graph`` container is reused.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations
import json
from typing import Iterable, Iterator

from coverage_checker.graph import Graph


Blocker = tuple[int, int]
Deletion = tuple[int, int]
DeletionRounds = tuple[tuple[Deletion, ...], ...]


@dataclass(frozen=True, slots=True)
class DominationProof:
    gamma: int
    dominating_witness_mask: int
    lower_blockers: tuple[Blocker, ...]


@dataclass(frozen=True, slots=True)
class FixedPointProof:
    guard_count: int
    initial_count: int
    deletion_rounds: DeletionRounds
    surviving_configurations: tuple[int, ...]
    trace_sha256: str


def combination_masks(order: int, size: int) -> Iterator[int]:
    if (
        type(order) is not int
        or type(size) is not int
        or order < 0
        or not 0 <= size <= order
    ):
        raise ValueError("invalid subset parameters")
    for vertices in combinations(range(order), size):
        mask = 0
        for vertex in vertices:
            mask |= 1 << vertex
        yield mask


def _universe(graph: Graph) -> int:
    return (1 << graph.order) - 1


def is_dominating_mask(graph: Graph, mask: int) -> bool:
    if (
        type(mask) is not int
        or mask < 0
        or mask & ~_universe(graph)
    ):
        return False
    covered = mask
    remaining = mask
    while remaining:
        guard_bit = remaining & -remaining
        remaining ^= guard_bit
        guard = guard_bit.bit_length() - 1
        covered |= graph.neighbors[guard]
    return covered == _universe(graph)


def first_undominated_vertex(graph: Graph, mask: int) -> int | None:
    for vertex in range(graph.order):
        if mask & (1 << vertex):
            continue
        if graph.neighbors[vertex] & mask:
            continue
        return vertex
    return None


def build_domination_proof(graph: Graph) -> DominationProof:
    """Prove gamma is two or three with a witness and exhaustive lower blockers."""

    gamma: int | None = None
    witness: int | None = None
    for size in (1, 2, 3):
        for mask in combination_masks(graph.order, size):
            if is_dominating_mask(graph, mask):
                gamma = size
                witness = mask
                break
        if gamma is not None:
            break
    if gamma not in (2, 3) or witness is None:
        raise ValueError("graph does not have domination number two or three")

    blockers: list[Blocker] = []
    for lower_mask in combination_masks(graph.order, gamma - 1):
        undominated = first_undominated_vertex(graph, lower_mask)
        if undominated is None:
            raise AssertionError("minimum domination scan is inconsistent")
        blockers.append((lower_mask, undominated))
    return DominationProof(gamma, witness, tuple(blockers))


def verify_domination_proof(
    graph: Graph,
    gamma: int,
    dominating_witness_mask: int,
    lower_blockers: Iterable[Blocker],
) -> bool:
    """Directly verify the explicit exhaustive domination certificate."""

    try:
        if (
            type(gamma) is not int
            or gamma not in (2, 3)
            or type(dominating_witness_mask) is not int
            or dominating_witness_mask.bit_count() != gamma
            or not is_dominating_mask(graph, dominating_witness_mask)
        ):
            return False
        records = tuple(lower_blockers)
        expected_masks = tuple(combination_masks(graph.order, gamma - 1))
        if len(records) != len(expected_masks):
            return False
        for expected_mask, record in zip(expected_masks, records, strict=True):
            if (
                type(record) is not tuple
                or len(record) != 2
                or type(record[0]) is not int
                or type(record[1]) is not int
            ):
                return False
            subset_mask, witness = record
            if (
                subset_mask != expected_mask
                or not 0 <= witness < graph.order
                or subset_mask & (1 << witness)
                or graph.neighbors[witness] & subset_mask
                or is_dominating_mask(graph, subset_mask)
            ):
                return False
        return True
    except (TypeError, ValueError, OverflowError):
        return False


def dominating_configurations(graph: Graph, guard_count: int) -> tuple[int, ...]:
    if (
        type(guard_count) is not int
        or not 0 <= guard_count <= graph.order
    ):
        raise ValueError("guard count outside graph")
    return tuple(
        mask
        for mask in combination_masks(graph.order, guard_count)
        if is_dominating_mask(graph, mask)
    )


def _generator_has_response(
    graph: Graph, configuration: int, attacked: int, active: set[int]
) -> bool:
    """Generator-side transition predicate; verifier uses a separate loop."""

    if configuration & (1 << attacked):
        raise ValueError("attacked vertex must be unoccupied")
    movable = configuration & graph.neighbors[attacked]
    while movable:
        guard_bit = movable & -movable
        movable ^= guard_bit
        successor = (configuration ^ guard_bit) | (1 << attacked)
        if (
            successor.bit_count() == configuration.bit_count()
            and successor in active
            and is_dominating_mask(graph, successor)
        ):
            return True
    return False


def trace_sha256(rounds: Iterable[Iterable[Deletion]]) -> str:
    digest = sha256()
    for round_index, records in enumerate(rounds):
        for configuration, attacked in records:
            digest.update(
                json.dumps(
                    [round_index, configuration, attacked],
                    separators=(",", ":"),
                ).encode("ascii")
                + b"\n"
            )
    return digest.hexdigest()


def build_fixed_point_proof(graph: Graph, guard_count: int) -> FixedPointProof:
    """Compute exact simultaneous greatest-fixed-point deletion rounds."""

    active = set(dominating_configurations(graph, guard_count))
    initial_count = len(active)
    rounds: list[tuple[Deletion, ...]] = []
    while active:
        doomed: list[Deletion] = []
        frozen = set(active)
        for configuration in sorted(frozen):
            for attacked in range(graph.order):
                if configuration & (1 << attacked):
                    continue
                if not _generator_has_response(
                    graph, configuration, attacked, frozen
                ):
                    doomed.append((configuration, attacked))
                    break
        if not doomed:
            break
        rounds.append(tuple(doomed))
        active.difference_update(configuration for configuration, _ in doomed)
    normalized = tuple(rounds)
    return FixedPointProof(
        guard_count=guard_count,
        initial_count=initial_count,
        deletion_rounds=normalized,
        surviving_configurations=tuple(sorted(active)),
        trace_sha256=trace_sha256(normalized),
    )


def verify_complete_empty_trace(
    graph: Graph,
    guard_count: int,
    rounds: DeletionRounds,
    expected_trace_sha256: str,
    expected_initial_count: int,
) -> bool:
    """Replay exact simultaneous rounds and require the fixed point to be empty.

    This verifier intentionally does not call the generator-side successor
    predicate.  It recomputes the complete doomed set in every round.
    """

    try:
        if (
            type(guard_count) is not int
            or guard_count not in (2, 3)
            or type(expected_initial_count) is not int
            or expected_initial_count < 1
            or not isinstance(expected_trace_sha256, str)
            or trace_sha256(rounds) != expected_trace_sha256
        ):
            return False
        active = set(dominating_configurations(graph, guard_count))
        if len(active) != expected_initial_count:
            return False
        for supplied_round in rounds:
            if type(supplied_round) is not tuple or not supplied_round:
                return False
            frozen = set(active)
            independently_doomed: list[Deletion] = []
            for configuration in sorted(frozen):
                first_failure: int | None = None
                for attacked in range(graph.order):
                    attack_bit = 1 << attacked
                    if configuration & attack_bit:
                        continue
                    response_exists = False
                    possible_guards = configuration & graph.neighbors[attacked]
                    while possible_guards:
                        moved_guard = possible_guards & -possible_guards
                        possible_guards ^= moved_guard
                        successor = (configuration & ~moved_guard) | attack_bit
                        if (
                            successor.bit_count() == guard_count
                            and successor in frozen
                            and is_dominating_mask(graph, successor)
                        ):
                            response_exists = True
                            break
                    if not response_exists:
                        first_failure = attacked
                        break
                if first_failure is not None:
                    independently_doomed.append(
                        (configuration, first_failure)
                    )
            if supplied_round != tuple(independently_doomed):
                return False
            active.difference_update(
                configuration for configuration, _ in independently_doomed
            )
        return not active
    except (TypeError, ValueError, OverflowError):
        return False


def serialize_blockers(blockers: Iterable[Blocker]) -> list[list[int]]:
    return [[mask, witness] for mask, witness in blockers]


def deserialize_blockers(value: object) -> tuple[Blocker, ...]:
    if not isinstance(value, list):
        raise ValueError("lower blockers must be an array")
    records: list[Blocker] = []
    for item in value:
        if (
            not isinstance(item, list)
            or len(item) != 2
            or type(item[0]) is not int
            or type(item[1]) is not int
        ):
            raise ValueError("malformed lower blocker")
        records.append((item[0], item[1]))
    return tuple(records)


def serialize_rounds(rounds: DeletionRounds) -> list[list[list[int]]]:
    return [
        [[configuration, attacked] for configuration, attacked in round_]
        for round_ in rounds
    ]


def deserialize_rounds(value: object) -> DeletionRounds:
    if not isinstance(value, list):
        raise ValueError("deletion rounds must be an array")
    rounds: list[tuple[Deletion, ...]] = []
    for round_value in value:
        if not isinstance(round_value, list) or not round_value:
            raise ValueError("deletion rounds must be nonempty arrays")
        records: list[Deletion] = []
        for item in round_value:
            if (
                not isinstance(item, list)
                or len(item) != 2
                or type(item[0]) is not int
                or type(item[1]) is not int
            ):
                raise ValueError("malformed deletion record")
            records.append((item[0], item[1]))
        rounds.append(tuple(records))
    return tuple(rounds)


__all__ = [
    "Blocker",
    "Deletion",
    "DeletionRounds",
    "DominationProof",
    "FixedPointProof",
    "build_domination_proof",
    "build_fixed_point_proof",
    "combination_masks",
    "deserialize_blockers",
    "deserialize_rounds",
    "dominating_configurations",
    "first_undominated_vertex",
    "is_dominating_mask",
    "serialize_blockers",
    "serialize_rounds",
    "trace_sha256",
    "verify_complete_empty_trace",
    "verify_domination_proof",
]
