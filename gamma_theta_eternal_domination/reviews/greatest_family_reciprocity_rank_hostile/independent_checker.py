#!/usr/bin/env python3
"""Clean-room order-nine audit of complementary-exchange deletion ranks.

This program deliberately does not import either campaign evaluator or the
candidate rank probe.  Graphs are represented by Python adjacency sets and
guard configurations by sorted vertex tuples.  The eternal kernel is built
as an explicit attack-coloured configuration digraph and pruned
synchronously from the full set of dominating triples.

For coverage, the program asks the pinned nauty ``geng`` binary for *all*
unlabeled graphs of order nine, filters connectedness itself, and then checks
that the resulting byte stream is identical to a second ``geng -c`` stream.
The two generator modes exercise different connectedness paths while the
mathematical predicates and game computation remain entirely in this file.
"""

from __future__ import annotations

import collections
import hashlib
import itertools
import json
import math
import pathlib
import subprocess
import sys
from typing import Iterable


ORDER = 9
VERTICES = frozenset(range(ORDER))
PAIRS = tuple(itertools.combinations(range(ORDER), 2))
TRIPLES = tuple(itertools.combinations(range(ORDER), 3))
FOURS = tuple(itertools.combinations(range(ORDER), 4))

EXPECTED_ALL_COUNT = 274_668
EXPECTED_CONNECTED_COUNT = 261_080
EXPECTED_GENG_SHA256 = (
    "588052a87e5313f331aa145a0a641702b6c13b6e2387dd3c4807bf7f49fdaca1"
)
EXPECTED_LABELG_SHA256 = (
    "ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0"
)
EXPECTED_ALL_STREAM_SHA256 = (
    "ce9c5d4d27c8e55de5f0c6348ec781a650382e16bdff26b6c3418fa00a9cfcf9"
)
EXPECTED_CONNECTED_STREAM_SHA256 = (
    "fe73f2b8aad1a653b6f3bee799efff369cc486688df5aeade62ce0b3b5889eb5"
)
EXPECTED_CANONICAL_STREAM_SHA256 = (
    "b52cedd4697f689327e09df5d36de1ae9aab02737f6ccd8e8f8bb18faedc962a"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    """Decode a small graph6 record into adjacency sets.

    This parser supports only the one-byte order field, which is exactly the
    format used here.  It also rejects nonzero graph6 padding.
    """

    if not record:
        raise ValueError("empty graph6 record")
    values = [ord(char) - 63 for char in record]
    if any(value < 0 or value > 63 for value in values):
        raise ValueError(f"invalid graph6 byte in {record!r}")
    order = values[0]
    if order != ORDER:
        raise ValueError(f"expected order {ORDER}, got {order}")

    payload: list[int] = []
    for value in values[1:]:
        payload.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    if len(payload) < needed:
        raise ValueError("truncated graph6 payload")
    if any(payload[needed:]):
        raise ValueError("nonzero graph6 padding")

    adjacency = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if payload[cursor]:
                adjacency[low].add(high)
                adjacency[high].add(low)
            cursor += 1
    return tuple(frozenset(row) for row in adjacency)


def is_connected(adjacency: tuple[frozenset[int], ...]) -> bool:
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        new_vertices = adjacency[vertex].difference(reached)
        reached.update(new_vertices)
        frontier.extend(new_vertices)
    return len(reached) == len(adjacency)


def edge_count(adjacency: tuple[frozenset[int], ...]) -> int:
    return sum(len(row) for row in adjacency) // 2


def is_independent(
    adjacency: tuple[frozenset[int], ...], choice: tuple[int, ...]
) -> bool:
    return all(v not in adjacency[u] for u, v in itertools.combinations(choice, 2))


def dominates(
    closed_neighborhoods: tuple[frozenset[int], ...],
    choice: tuple[int, ...],
) -> bool:
    covered: set[int] = set()
    for vertex in choice:
        covered.update(closed_neighborhoods[vertex])
    return len(covered) == ORDER


def equality_static_filter(
    adjacency: tuple[frozenset[int], ...],
) -> tuple[tuple[int, int, int], ...] | None:
    """Return all maximum independent triples iff gamma=alpha=3."""

    independent_triples = tuple(
        triple for triple in TRIPLES if is_independent(adjacency, triple)
    )
    if not independent_triples:
        return None
    if any(is_independent(adjacency, four) for four in FOURS):
        return None

    closed = tuple(
        frozenset(set(adjacency[vertex]) | {vertex}) for vertex in range(ORDER)
    )
    if any(len(neighborhood) == ORDER for neighborhood in closed):
        return None
    if any(dominates(closed, pair) for pair in PAIRS):
        return None

    # Every independent triple is maximal because alpha=3, hence dominates.
    # Check this implication literally rather than relying on it in the audit.
    if not all(dominates(closed, triple) for triple in independent_triples):
        raise AssertionError("a maximum independent set failed to dominate")
    return independent_triples


def greatest_triple_kernel(
    adjacency: tuple[frozenset[int], ...],
) -> tuple[
    frozenset[tuple[int, int, int]],
    dict[tuple[int, int, int], int],
    frozenset[tuple[int, int, int]],
]:
    """Build the colored configuration digraph and synchronously prune it."""

    closed = tuple(
        frozenset(set(adjacency[vertex]) | {vertex}) for vertex in range(ORDER)
    )
    dominating = frozenset(
        triple for triple in TRIPLES if dominates(closed, triple)
    )

    # responses[(state, attacked_vertex)] is the explicit set of all legal
    # one-edge, one-guard successors that still dominate.
    responses: dict[
        tuple[tuple[int, int, int], int],
        frozenset[tuple[int, int, int]],
    ] = {}
    for state in dominating:
        occupied = frozenset(state)
        for attacked in VERTICES.difference(occupied):
            successors: set[tuple[int, int, int]] = set()
            for guard in state:
                if attacked not in adjacency[guard]:
                    continue
                successor = tuple(
                    sorted(occupied.difference({guard}) | {attacked})
                )
                if successor in dominating:
                    successors.add(successor)
            responses[(state, attacked)] = frozenset(successors)

    live = set(dominating)
    deletion_rank: dict[tuple[int, int, int], int] = {}
    round_number = 1
    while True:
        doomed: set[tuple[int, int, int]] = set()
        for state in live:
            occupied = frozenset(state)
            for attacked in VERTICES.difference(occupied):
                if responses[(state, attacked)].isdisjoint(live):
                    doomed.add(state)
                    break
        if not doomed:
            break
        for state in doomed:
            deletion_rank[state] = round_number
        live.difference_update(doomed)
        round_number += 1

    if len(deletion_rank) + len(live) != len(dominating):
        raise AssertionError("kernel rank partition is incomplete")
    return frozenset(live), deletion_rank, dominating


def rank_label(
    state: tuple[int, int, int],
    survivors: frozenset[tuple[int, int, int]],
    deletion_rank: dict[tuple[int, int, int], int],
    dominating: frozenset[tuple[int, int, int]],
) -> str:
    if state in survivors:
        return "S"
    if state not in dominating:
        return "0"
    return str(deletion_rank[state])


def normalized_stream(records: Iterable[str]) -> bytes:
    return "".join(f"{record}\n" for record in records).encode("ascii")


def integer_partitions(total: int, ceiling: int | None = None):
    """Yield nonincreasing integer partitions of ``total``."""

    if total == 0:
        yield ()
        return
    upper = total if ceiling is None else min(total, ceiling)
    for first in range(upper, 0, -1):
        for rest in integer_partitions(total - first, first):
            yield (first,) + rest


def burnside_unlabeled_graph_count(order: int) -> int:
    """Number of unlabeled simple graphs from the S_n edge action."""

    if order == 0:
        return 1
    numerator = 0
    factorial = math.factorial(order)
    for cycle_lengths in integer_partitions(order):
        multiplicities = collections.Counter(cycle_lengths)
        centralizer = 1
        for length, count in multiplicities.items():
            centralizer *= (length**count) * math.factorial(count)
        class_size = factorial // centralizer

        edge_orbits = sum(length // 2 for length in cycle_lengths)
        edge_orbits += sum(
            math.gcd(left, right)
            for index, left in enumerate(cycle_lengths)
            for right in cycle_lengths[index + 1 :]
        )
        numerator += class_size * (2**edge_orbits)
    quotient, remainder = divmod(numerator, factorial)
    if remainder:
        raise AssertionError("Burnside numerator is not divisible by n!")
    return quotient


def euler_connected_counts(
    all_graph_counts: tuple[int, ...],
) -> tuple[int, ...]:
    """Invert A(x)=product_m (1-x^m)^(-c_m)."""

    maximum = len(all_graph_counts) - 1
    logarithmic = [0] * (maximum + 1)
    connected = [0] * (maximum + 1)
    for order in range(1, maximum + 1):
        logarithmic[order] = order * all_graph_counts[order] - sum(
            logarithmic[index] * all_graph_counts[order - index]
            for index in range(1, order)
        )
        proper_divisor_sum = sum(
            divisor * connected[divisor]
            for divisor in range(1, order)
            if order % divisor == 0
        )
        numerator = logarithmic[order] - proper_divisor_sum
        connected[order], remainder = divmod(numerator, order)
        if remainder:
            raise AssertionError("Euler-transform inverse is not integral")
    return tuple(connected)


def generate_records(
    geng: pathlib.Path, *arguments: str
) -> tuple[list[str], bytes]:
    completed = subprocess.run(
        [str(geng), *arguments],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.stderr:
        raise RuntimeError(
            f"unexpected geng diagnostics: {completed.stderr.decode(errors='replace')}"
        )
    records = completed.stdout.decode("ascii").splitlines()
    if len(records) != len(set(records)):
        raise AssertionError("duplicate graph6 record in geng stream")
    return records, completed.stdout


def canonicalize_records(
    labelg: pathlib.Path, stream: bytes
) -> tuple[list[str], bytes]:
    completed = subprocess.run(
        [str(labelg), "-q"],
        input=stream,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.stderr:
        raise RuntimeError(
            "unexpected labelg diagnostics: "
            + completed.stderr.decode(errors="replace")
        )
    return completed.stdout.decode("ascii").splitlines(), completed.stdout


def control_certificate() -> dict[str, object]:
    """Return a literal certificate for the first static asymmetry."""

    record = "HCOceRy"
    adjacency = decode_graph6(record)
    if not is_connected(adjacency):
        raise AssertionError("control is disconnected")
    independent_triples = equality_static_filter(adjacency)
    if independent_triples is None:
        raise AssertionError("control does not have gamma=alpha=3")
    survivors, ranks, dominating = greatest_triple_kernel(adjacency)
    if not survivors:
        raise AssertionError("control has empty greatest triple-kernel")

    forward = (1, 2, 7)
    reverse = (0, 5, 8)
    closed = tuple(
        frozenset(set(adjacency[vertex]) | {vertex}) for vertex in range(ORDER)
    )
    forward_covered = set().union(*(closed[v] for v in forward))
    reverse_covered = set().union(*(closed[v] for v in reverse))
    if forward in dominating or reverse not in dominating or ranks[reverse] != 1:
        raise AssertionError("control exchange ranks changed")

    losing_attacks: dict[str, list[dict[str, object]]] = {}
    for attacked in VERTICES.difference(reverse):
        responses: list[dict[str, object]] = []
        for guard in reverse:
            if attacked not in adjacency[guard]:
                continue
            successor = tuple(
                sorted(frozenset(reverse).difference({guard}) | {attacked})
            )
            if successor in dominating:
                responses.append({"guard": guard, "successor": list(successor)})
        if not responses:
            losing_attacks[str(attacked)] = responses
    if set(losing_attacks) != {"3", "6"}:
        raise AssertionError("unexpected round-one control attacks")

    return {
        "graph6": record,
        "connected": True,
        "edges": [
            [left, right]
            for left in range(ORDER)
            for right in range(left + 1, ORDER)
            if right in adjacency[left]
        ],
        "gamma": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "independent_triples": len(independent_triples),
        "dominating_triples": len(dominating),
        "greatest_states": len(survivors),
        "S": [0, 1, 2],
        "T": [5, 7, 8],
        "u": 0,
        "x": 7,
        "forward": list(forward),
        "forward_rank": "0",
        "forward_undominated_vertices": sorted(VERTICES.difference(forward_covered)),
        "reverse": list(reverse),
        "reverse_rank": "1",
        "reverse_undominated_vertices": sorted(VERTICES.difference(reverse_covered)),
        "reverse_round_one_losing_attacks": losing_attacks,
    }


def census(geng: pathlib.Path, labelg: pathlib.Path) -> dict[str, object]:
    if sha256_bytes(geng.read_bytes()) != EXPECTED_GENG_SHA256:
        raise AssertionError("pinned geng executable hash mismatch")
    if sha256_bytes(labelg.read_bytes()) != EXPECTED_LABELG_SHA256:
        raise AssertionError("pinned labelg executable hash mismatch")

    version = subprocess.run(
        [str(geng), "-version"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ).stdout.strip()
    if version != "Nauty&Traces version 2.9300 (32 bits)":
        raise AssertionError(f"unexpected geng version: {version!r}")

    burnside_counts = tuple(
        burnside_unlabeled_graph_count(order) for order in range(ORDER + 1)
    )
    connected_theory = euler_connected_counts(burnside_counts)
    if burnside_counts[ORDER] != EXPECTED_ALL_COUNT:
        raise AssertionError("Burnside order-nine total changed")
    if connected_theory[ORDER] != EXPECTED_CONNECTED_COUNT:
        raise AssertionError("Euler-transform connected total changed")

    # Deliberately generate all unlabeled graphs, then filter connectedness
    # without trusting geng's -c filter.
    all_records, all_bytes = generate_records(geng, "-q", str(ORDER))
    if len(all_records) != EXPECTED_ALL_COUNT:
        raise AssertionError("unexpected all-unlabeled count")
    if sha256_bytes(all_bytes) != EXPECTED_ALL_STREAM_SHA256:
        raise AssertionError("unexpected all-unlabeled stream hash")
    canonical_records, canonical_bytes = canonicalize_records(labelg, all_bytes)
    if len(canonical_records) != EXPECTED_ALL_COUNT:
        raise AssertionError("labelg changed the record count")
    if len(set(canonical_records)) != EXPECTED_ALL_COUNT:
        raise AssertionError("two generated records are isomorphic")
    if sha256_bytes(canonical_bytes) != EXPECTED_CANONICAL_STREAM_SHA256:
        raise AssertionError("unexpected canonical-label stream hash")

    connected_records: list[str] = []
    all_edge_histogram: collections.Counter[int] = collections.Counter()
    connected_edge_histogram: collections.Counter[int] = collections.Counter()
    for record in all_records:
        adjacency = decode_graph6(record)
        edges = edge_count(adjacency)
        all_edge_histogram[edges] += 1
        if is_connected(adjacency):
            connected_records.append(record)
            connected_edge_histogram[edges] += 1

    if len(connected_records) != EXPECTED_CONNECTED_COUNT:
        raise AssertionError("independent connectedness count mismatch")
    connected_bytes = normalized_stream(connected_records)
    if sha256_bytes(connected_bytes) != EXPECTED_CONNECTED_STREAM_SHA256:
        raise AssertionError("independently filtered connected stream hash mismatch")

    # Cross-check the independent filter against geng's connected-generation
    # mode.  Exact byte equality is stronger than comparing only the count.
    direct_connected, direct_bytes = generate_records(
        geng, "-c", "-q", str(ORDER)
    )
    if direct_connected != connected_records:
        raise AssertionError("all-mode filter and connected-mode streams differ")
    if direct_bytes != connected_bytes:
        raise AssertionError("connected stream byte normalization mismatch")

    totals: collections.Counter[str] = collections.Counter()
    rank_pairs: collections.Counter[str] = collections.Counter()
    asymmetric_rank_pairs: collections.Counter[str] = collections.Counter()
    first_static_asymmetry: dict[str, object] | None = None
    first_unequal_positive_finite: dict[str, object] | None = None
    first_survival_violation: dict[str, object] | None = None

    totals["all_unlabeled_graphs"] = len(all_records)
    totals["connected_unlabeled_graphs"] = len(connected_records)
    for record in connected_records:
        adjacency = decode_graph6(record)
        independent_triples = equality_static_filter(adjacency)
        if independent_triples is None:
            continue
        totals["static_equality_graphs"] += 1

        survivors, deletion_rank, dominating = greatest_triple_kernel(adjacency)
        if not survivors:
            continue
        totals["eternal_equality_graphs"] += 1
        totals["greatest_states"] += len(survivors)

        if not set(independent_triples).issubset(survivors):
            raise AssertionError(
                "maximum-independent-state forcing failed in greatest kernel"
            )

        for pair_index, first in enumerate(independent_triples):
            first_set = frozenset(first)
            for second in independent_triples[pair_index + 1 :]:
                totals["independent_state_pairs"] += 1
                second_set = frozenset(second)
                left_only = sorted(first_set.difference(second_set))
                right_only = sorted(second_set.difference(first_set))
                if len(left_only) != len(right_only):
                    raise AssertionError("equal-size states have unequal differences")

                for removed_left in left_only:
                    for inserted_right in right_only:
                        forward = tuple(
                            sorted(
                                first_set.difference({removed_left})
                                | {inserted_right}
                            )
                        )
                        reverse = tuple(
                            sorted(
                                second_set.difference({inserted_right})
                                | {removed_left}
                            )
                        )
                        forward_label = rank_label(
                            forward, survivors, deletion_rank, dominating
                        )
                        reverse_label = rank_label(
                            reverse, survivors, deletion_rank, dominating
                        )
                        pair_key = f"{forward_label},{reverse_label}"
                        rank_pairs[pair_key] += 1
                        totals["exchange_instances"] += 1

                        if (forward_label == "0") != (reverse_label == "0"):
                            totals["static_asymmetries"] += 1
                            asymmetric_rank_pairs[pair_key] += 1
                            if first_static_asymmetry is None:
                                first_static_asymmetry = {
                                    "graph6": record,
                                    "S": list(first),
                                    "T": list(second),
                                    "u": removed_left,
                                    "x": inserted_right,
                                    "forward_rank": forward_label,
                                    "reverse_rank": reverse_label,
                                }

                        if (
                            forward_label.isdigit()
                            and reverse_label.isdigit()
                            and forward_label != "0"
                            and reverse_label != "0"
                            and forward_label != reverse_label
                            and first_unequal_positive_finite is None
                        ):
                            first_unequal_positive_finite = {
                                "graph6": record,
                                "S": list(first),
                                "T": list(second),
                                "u": removed_left,
                                "x": inserted_right,
                                "forward_rank": forward_label,
                                "reverse_rank": reverse_label,
                            }

                        if (forward_label == "S") != (reverse_label == "S"):
                            totals["survival_violations"] += 1
                            if first_survival_violation is None:
                                first_survival_violation = {
                                    "graph6": record,
                                    "S": list(first),
                                    "T": list(second),
                                    "u": removed_left,
                                    "x": inserted_right,
                                    "forward_rank": forward_label,
                                    "reverse_rank": reverse_label,
                                }

    totals.setdefault("survival_violations", 0)
    if sum(rank_pairs.values()) != totals["exchange_instances"]:
        raise AssertionError("rank-pair table does not cover every exchange")
    if sum(asymmetric_rank_pairs.values()) != totals["static_asymmetries"]:
        raise AssertionError("static-asymmetry table is incomplete")
    expected_first = {
        "graph6": "HCOceRy",
        "S": [0, 1, 2],
        "T": [5, 7, 8],
        "u": 0,
        "x": 7,
        "forward_rank": "0",
        "reverse_rank": "1",
    }
    if first_static_asymmetry != expected_first:
        raise AssertionError("first static-asymmetry control changed")

    return {
        "schema": "greatest-family-reciprocity-rank-hostile-v1",
        "classification": "CERTIFIED_FINITE_ORDER_9_K3",
        "generator": {
            "name": "nauty geng",
            "version": version,
            "binary_sha256": EXPECTED_GENG_SHA256,
            "labelg_binary_sha256": EXPECTED_LABELG_SHA256,
            "all_mode_command": "geng -q 9",
            "connected_mode_command": "geng -c -q 9",
            "all_stream_sha256": sha256_bytes(all_bytes),
            "connected_stream_sha256": sha256_bytes(connected_bytes),
            "canonical_label_stream_sha256": sha256_bytes(canonical_bytes),
            "canonical_labels_are_pairwise_distinct": True,
            "independent_connected_filter_equals_direct_mode": True,
        },
        "coverage": {
            "burnside_all_unlabeled_counts_n0_to_n9": list(burnside_counts),
            "euler_transform_connected_counts_n0_to_n9": list(connected_theory),
            "all_edge_histogram": {
                str(key): value for key, value in sorted(all_edge_histogram.items())
            },
            "connected_edge_histogram": {
                str(key): value
                for key, value in sorted(connected_edge_histogram.items())
            },
        },
        "totals": dict(sorted(totals.items())),
        "ordered_rank_pairs": dict(sorted(rank_pairs.items())),
        "static_asymmetry_rank_pairs": dict(
            sorted(asymmetric_rank_pairs.items())
        ),
        "first_static_asymmetry": first_static_asymmetry,
        "first_static_asymmetry_certificate": control_certificate(),
        "first_unequal_positive_finite_rank_pair": first_unequal_positive_finite,
        "first_survival_violation": first_survival_violation,
        "scope_guardrail": (
            "The no-one-sided-survivor result is exact only for connected "
            "unlabeled order-nine graphs with gamma=alpha=gamma_infinity=3. "
            "It proves no all-order reciprocity theorem and does not resolve "
            "the gamma-theta conjecture."
        ),
    }


def main() -> None:
    root = pathlib.Path(__file__).resolve().parents[2]
    geng = root / "tools" / "nauty2_9_3" / "geng"
    labelg = root / "tools" / "nauty2_9_3" / "labelg"
    result = census(geng, labelg)
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
