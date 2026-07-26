#!/usr/bin/env python3
"""Clean-room falsification probe for independent-antineighborhood projection.

This file imports no campaign evaluator.  Nauty's ``geng`` is used only to
stream one graph6 representative of every unlabeled graph.  Graph6 decoding,
all static parameters, and the one-guard greatest-fixed-point calculation are
implemented below with integer masks.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import platform
import subprocess
import sys


UNLABELED_COUNTS = {
    1: 1,
    2: 2,
    3: 4,
    4: 11,
    5: 34,
    6: 156,
    7: 1044,
    8: 12346,
}


def require(condition: bool, label: str, **context: object) -> None:
    if not condition:
        raise AssertionError(
            json.dumps({"failed_check": label, **context}, sort_keys=True)
        )


def digest(path: Path) -> str:
    value = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def decode_graph6(encoded: str) -> tuple[int, ...]:
    raw = encoded.encode("ascii")
    require(bool(raw), "nonempty_graph6")
    require(raw[0] != 126, "small_graph6_only", graph6=encoded)
    order = raw[0] - 63
    require(0 <= order <= 62, "valid_graph6_order", graph6=encoded)

    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        require(0 <= value < 64, "valid_graph6_byte", graph6=encoded)
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))

    needed = order * (order - 1) // 2
    require(len(bits) >= needed, "enough_graph6_bits", graph6=encoded)
    require(not any(bits[needed:]), "zero_graph6_padding", graph6=encoded)

    adjacency = [0] * order
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1
    return tuple(adjacency)


def graph_stream(
    geng: Path, maximum_order: int
) -> Iterable[tuple[int, str, tuple[int, ...]]]:
    for order in range(1, maximum_order + 1):
        completed = subprocess.run(
            [str(geng), "-q", str(order)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        records = tuple(
            line.strip()
            for line in completed.stdout.splitlines()
            if line.strip()
        )
        require(
            len(records) == UNLABELED_COUNTS[order],
            "unlabeled_graph_count",
            order=order,
            expected=UNLABELED_COUNTS[order],
            observed=len(records),
        )
        require(
            len(records) == len(set(records)),
            "unique_graph6_records",
            order=order,
        )
        for encoded in records:
            adjacency = decode_graph6(encoded)
            require(len(adjacency) == order, "decoded_order", graph6=encoded)
            yield order, encoded, adjacency


def subsets_of_size(order: int, size: int) -> Iterable[int]:
    for vertices in combinations(range(order), size):
        mask = 0
        for vertex in vertices:
            mask |= 1 << vertex
        yield mask


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    remaining = state
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        if adjacency[vertex] & (state ^ bit):
            return False
        remaining ^= bit
    return True


def clique(adjacency: tuple[int, ...], state: int) -> bool:
    remaining = state
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        if (state ^ bit) & ~adjacency[vertex]:
            return False
        remaining ^= bit
    return True


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    remaining = state
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        covered |= adjacency[vertex]
        remaining ^= bit
    return covered == (1 << len(adjacency)) - 1


def gamma(adjacency: tuple[int, ...]) -> int:
    for size in range(len(adjacency) + 1):
        if any(
            dominates(adjacency, state)
            for state in subsets_of_size(len(adjacency), size)
        ):
            return size
    raise AssertionError("the full set must dominate")


def independent_sets(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        state
        for state in range(1 << len(adjacency))
        if independent(adjacency, state)
    )


def alpha(adjacency: tuple[int, ...]) -> int:
    return max(state.bit_count() for state in independent_sets(adjacency))


def maximal_independent_sizes(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sorted(
            state.bit_count()
            for state in independent_sets(adjacency)
            if dominates(adjacency, state)
        )
    )


def theta(adjacency: tuple[int, ...]) -> int:
    order = len(adjacency)
    full = (1 << order) - 1
    clique_table = tuple(
        clique(adjacency, state) for state in range(1 << order)
    )

    @lru_cache(maxsize=None)
    def cover(remaining: int) -> int:
        if not remaining:
            return 0
        anchor = remaining & -remaining
        best = order
        part = remaining
        while part:
            if part & anchor and clique_table[part]:
                best = min(best, 1 + cover(remaining ^ part))
            part = (part - 1) & remaining
        return best

    return cover(full)


def eternal_kernel(
    adjacency: tuple[int, ...], guard_count: int
) -> frozenset[int]:
    """Greatest family satisfying every unoccupied-attack obligation."""

    order = len(adjacency)
    full = (1 << order) - 1
    alive = {
        state
        for state in subsets_of_size(order, guard_count)
        if dominates(adjacency, state)
    }
    while True:
        keep: set[int] = set()
        for state in alive:
            valid = True
            attacks = full ^ state
            while attacks:
                attack_bit = attacks & -attacks
                attacked = attack_bit.bit_length() - 1
                responders = state & adjacency[attacked]
                defended = False
                while responders:
                    guard_bit = responders & -responders
                    successor = (state ^ guard_bit) | attack_bit
                    if successor in alive:
                        defended = True
                        break
                    responders ^= guard_bit
                if not defended:
                    valid = False
                    break
                attacks ^= attack_bit
            if valid:
                keep.add(state)
        if keep == alive:
            return frozenset(keep)
        alive = keep


def gamma_eternal(
    adjacency: tuple[int, ...], lower_bound: int
) -> tuple[int, frozenset[int]]:
    for guard_count in range(lower_bound, len(adjacency) + 1):
        family = eternal_kernel(adjacency, guard_count)
        if family:
            return guard_count, family
    raise AssertionError("the fully occupied state is eternally closed")


def induced_graph(
    adjacency: tuple[int, ...], kept: tuple[int, ...]
) -> tuple[int, ...]:
    old_to_new = {old: new for new, old in enumerate(kept)}
    answer: list[int] = []
    for old in kept:
        row = 0
        for neighbor in kept:
            if adjacency[old] & (1 << neighbor):
                row |= 1 << old_to_new[neighbor]
        answer.append(row)
    return tuple(answer)


def project(state: int, kept: tuple[int, ...]) -> int:
    answer = 0
    for new, old in enumerate(kept):
        if state & (1 << old):
            answer |= 1 << new
    return answer


def lift(state: int, kept: tuple[int, ...]) -> int:
    answer = 0
    for new, old in enumerate(kept):
        if state & (1 << new):
            answer |= 1 << old
    return answer


@lru_cache(maxsize=None)
def q_parameters(
    adjacency: tuple[int, ...],
) -> tuple[int, int, int, int, tuple[int, ...], frozenset[int]]:
    q_gamma = gamma(adjacency)
    q_alpha = alpha(adjacency)
    q_gamma_eternal, q_family = gamma_eternal(adjacency, q_gamma)
    q_theta = theta(adjacency)
    q_maximal_sizes = maximal_independent_sizes(adjacency)
    return (
        q_gamma,
        q_alpha,
        q_gamma_eternal,
        q_theta,
        q_maximal_sizes,
        q_family,
    )


def empty_count_row() -> dict[str, int]:
    return {
        "graphs": 0,
        "equality_graphs": 0,
        "independent_sets_A": 0,
        "distinct_projected_graph_checks": 0,
        "slice_states": 0,
        "slice_attack_obligations": 0,
        "forced_independent_targets": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-order", type=int, default=8)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    require(1 <= args.maximum_order <= 8, "supported_order")

    review = Path(__file__).resolve().parent
    campaign = review.parents[1]
    geng = campaign / "tools" / "nauty2_9_3" / "geng"
    target_path = (
        campaign
        / "math"
        / "lemmas"
        / "independent_antineighborhood_projection.md"
    )
    output = args.output or review / "probe_result.json"
    require(geng.is_file(), "geng_exists", path=str(geng))
    require(target_path.is_file(), "target_exists", path=str(target_path))
    require(
        output.resolve().parent == review,
        "output_confined_to_review_directory",
        output=str(output.resolve()),
    )

    by_order = {
        str(order): empty_count_row()
        for order in range(1, args.maximum_order + 1)
    }
    totals = empty_count_row()
    totals["counterexamples"] = 0
    checked_q: set[tuple[int, ...]] = set()

    for order, encoded, adjacency in graph_stream(geng, args.maximum_order):
        row = by_order[str(order)]
        row["graphs"] += 1
        totals["graphs"] += 1

        graph_gamma = gamma(adjacency)
        graph_gamma_eternal, family = gamma_eternal(adjacency, graph_gamma)
        if graph_gamma != graph_gamma_eternal:
            continue

        row["equality_graphs"] += 1
        totals["equality_graphs"] += 1
        graph_alpha = alpha(adjacency)
        graph_theta = theta(adjacency)
        require(
            graph_alpha == graph_gamma,
            "equality_collapse_alpha",
            graph6=encoded,
        )
        require(
            set(maximal_independent_sizes(adjacency)) == {graph_gamma},
            "equality_collapse_well_covered",
            graph6=encoded,
        )
        if graph_theta > graph_gamma:
            totals["counterexamples"] += 1

        for independent_target in independent_sets(adjacency):
            if independent_target.bit_count() == graph_gamma:
                require(
                    independent_target in family,
                    "maximum_independent_target_in_greatest_family",
                    graph6=encoded,
                    target=independent_target,
                )
                row["forced_independent_targets"] += 1
                totals["forced_independent_targets"] += 1

        full = (1 << order) - 1
        for set_a in independent_sets(adjacency):
            size_a = set_a.bit_count()
            if not (1 <= size_a < graph_gamma):
                continue

            row["independent_sets_A"] += 1
            totals["independent_sets_A"] += 1
            closed_a = set_a
            cursor = set_a
            while cursor:
                bit = cursor & -cursor
                vertex = bit.bit_length() - 1
                closed_a |= adjacency[vertex]
                cursor ^= bit
            outside = full ^ closed_a
            require(
                bool(outside),
                "projected_graph_nonempty",
                graph6=encoded,
                set_a=set_a,
            )
            kept = tuple(
                vertex
                for vertex in range(order)
                if outside & (1 << vertex)
            )
            q_adjacency = induced_graph(adjacency, kept)
            expected = graph_gamma - size_a
            (
                q_gamma,
                q_alpha,
                q_gamma_eternal,
                q_theta,
                q_maximal_sizes,
                q_greatest_family,
            ) = q_parameters(q_adjacency)

            require(
                q_gamma == expected,
                "projected_gamma",
                graph6=encoded,
                set_a=set_a,
                expected=expected,
                observed=q_gamma,
            )
            require(
                q_alpha == expected,
                "projected_alpha",
                graph6=encoded,
                set_a=set_a,
                expected=expected,
                observed=q_alpha,
            )
            require(
                q_gamma_eternal == expected,
                "projected_gamma_eternal",
                graph6=encoded,
                set_a=set_a,
                expected=expected,
                observed=q_gamma_eternal,
            )
            require(
                set(q_maximal_sizes) == {expected},
                "projected_well_covered",
                graph6=encoded,
                set_a=set_a,
                expected=expected,
                maximal_sizes=q_maximal_sizes,
            )

            # There is no counterexample through this finite range.  This is
            # a finite check of the minimal-counterexample theta consequence,
            # not an ingredient in the analytic projection theorem.
            require(
                q_theta == expected,
                "finite_projected_theta",
                graph6=encoded,
                set_a=set_a,
                expected=expected,
                observed=q_theta,
            )

            allowed = outside | set_a
            sliced_original_states = tuple(
                state
                for state in family
                if state & set_a == set_a and state & ~allowed == 0
            )
            require(
                bool(sliced_original_states),
                "restricted_slice_nonempty",
                graph6=encoded,
                set_a=set_a,
            )
            projected_family = {
                project(state ^ set_a, kept)
                for state in sliced_original_states
            }
            require(
                len(projected_family) == len(sliced_original_states),
                "slice_projection_injective",
                graph6=encoded,
                set_a=set_a,
            )

            full_q = (1 << len(q_adjacency)) - 1
            for q_state in projected_family:
                require(
                    q_state.bit_count() == expected,
                    "slice_state_size",
                    graph6=encoded,
                    set_a=set_a,
                    q_state=q_state,
                )
                require(
                    dominates(q_adjacency, q_state),
                    "slice_state_dominates_q",
                    graph6=encoded,
                    set_a=set_a,
                    q_state=q_state,
                )
                lifted = lift(q_state, kept) | set_a
                require(
                    lifted in family,
                    "slice_state_lifts_to_family",
                    graph6=encoded,
                    set_a=set_a,
                    q_state=q_state,
                )
                attacks = full_q ^ q_state
                while attacks:
                    attack_bit = attacks & -attacks
                    attacked = attack_bit.bit_length() - 1
                    responders = q_state & q_adjacency[attacked]
                    witnesses = []
                    while responders:
                        guard_bit = responders & -responders
                        successor = (q_state ^ guard_bit) | attack_bit
                        if successor in projected_family:
                            witnesses.append(guard_bit)
                        responders ^= guard_bit
                    require(
                        bool(witnesses),
                        "slice_forall_attack_exists_response",
                        graph6=encoded,
                        set_a=set_a,
                        q_state=q_state,
                        attacked=attacked,
                    )
                    old_attack = kept[attacked]
                    for guard_bit in witnesses:
                        new_guard = guard_bit.bit_length() - 1
                        old_guard = kept[new_guard]
                        old_successor = (
                            lifted ^ (1 << old_guard)
                        ) | (1 << old_attack)
                        require(
                            old_successor in family,
                            "response_is_original_one_guard_move",
                            graph6=encoded,
                            set_a=set_a,
                            q_state=q_state,
                            attacked=attacked,
                            guard=new_guard,
                        )
                    row["slice_attack_obligations"] += 1
                    totals["slice_attack_obligations"] += 1
                    attacks ^= attack_bit

            require(
                projected_family.issubset(q_greatest_family),
                "slice_inside_projected_greatest_kernel",
                graph6=encoded,
                set_a=set_a,
            )
            row["slice_states"] += len(projected_family)
            totals["slice_states"] += len(projected_family)
            if q_adjacency not in checked_q:
                checked_q.add(q_adjacency)
                row["distinct_projected_graph_checks"] += 1
                totals["distinct_projected_graph_checks"] += 1

    expected_graphs = sum(
        UNLABELED_COUNTS[order]
        for order in range(1, args.maximum_order + 1)
    )
    require(
        totals["graphs"] == expected_graphs,
        "complete_unlabeled_census",
        expected=expected_graphs,
        observed=totals["graphs"],
    )
    require(
        totals["counterexamples"] == 0,
        "no_small_counterexample",
        observed=totals["counterexamples"],
    )

    result = {
        "schema": "independent-antineighborhood-projection-probe-v1",
        "verdict": "PASS",
        "model": {
            "attacks": "unoccupied vertices only",
            "movement": "exactly one adjacent guard moves to the attack",
            "closure": (
                "for every family state and every unoccupied attack, "
                "some one-move successor remains in the family"
            ),
        },
        "scope": {
            "maximum_order": args.maximum_order,
            "unlabeled_universe": (
                "one representative of every unlabeled graph from nauty geng"
            ),
            "eligible_pair": (
                "gamma(G)=gamma_eternal(G)=k and every independent A "
                "with 1<=|A|<k"
            ),
            "family_tested": (
                "restricted slice of the independently computed greatest "
                "eternal k-family"
            ),
        },
        "implementation": {
            "campaign_evaluator_imports": False,
            "language": "Python standard library",
            "graph_representation": "integer adjacency masks",
            "eternal_algorithm": "greatest-fixed-point deletion",
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "hashes": {
            "target_sha256": digest(target_path),
            "probe_sha256": digest(Path(__file__).resolve()),
            "geng_sha256": digest(geng),
        },
        "counts_by_order": by_order,
        "totals": totals,
        "limitations": [
            (
                "The census is a falsification probe, not the proof for "
                "unbounded order."
            ),
            (
                "The computation tests the greatest eternal family.  The "
                "analytic forcing argument, not enumeration of exponentially "
                "many subfamilies, proves the statement for every eternal "
                "k-family."
            ),
            (
                "The projected theta equality is checked only in this finite "
                "counterexample-free range; analytically it follows only "
                "under minimum-counterexample minimality."
            ),
        ],
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
