#!/usr/bin/env python3
"""Independent bounded countermodel search for the forced-C5 continuation.

This script deliberately does not import campaign graph or eternal-family
code.  For each graph through the requested order it searches for:

* gamma(G) = alpha(G) = 3;
* an independent ordered reference state S=(a,b,c);
* an induced complement path x0-x1-x2-x3; and
* some (possibly proper) eternal family whose exact direct-response lists
  on that path are

      {a}, {a,c}, {b,c}, {b}.

For fixed graph and labels, existence of such a family is decided exactly.
Delete the six forbidden direct-swap states from all dominating triples and
take the greatest one-guard-safe kernel.  Every admissible family is
contained in this kernel, while the kernel itself is an admissible family.
Thus all seven required states survive exactly when an arbitrary specified
family with the target lists exists.

The scan is a bounded diagnostic, not a coverage certificate for the
campaign or a substitute for the human proof.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GENG = ROOT / "tools" / "nauty2_9_3" / "geng"
TARGET = ROOT / "math" / "working" / "forced_c5_contradiction" / "NOTE.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> tuple[int, tuple[int, ...]]:
    """Decode ordinary graph6 records of order at most 62."""
    text = record.strip()
    if text.startswith(">>graph6<<"):
        text = text[10:]
    if not text:
        raise ValueError("empty graph6 record")
    n = ord(text[0]) - 63
    if not 0 <= n <= 62:
        raise ValueError("only short graph6 records are supported")
    bits: list[int] = []
    for char in text[1:]:
        value = ord(char) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = n * (n - 1) // 2
    if len(bits) < required:
        raise ValueError("truncated graph6 record")
    adjacency = [0] * n
    cursor = 0
    for upper in range(1, n):
        for lower in range(upper):
            if bits[cursor]:
                adjacency[lower] |= 1 << upper
                adjacency[upper] |= 1 << lower
            cursor += 1
    return n, tuple(adjacency)


def combinations_masks(n: int, size: int) -> tuple[int, ...]:
    return tuple(
        sum(1 << vertex for vertex in subset)
        for subset in itertools.combinations(range(n), size)
    )


def is_independent(mask: int, adjacency: tuple[int, ...]) -> bool:
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        remaining ^= bit
        if adjacency[vertex] & remaining:
            return False
    return True


def dominates(mask: int, adjacency: tuple[int, ...], universe: int) -> bool:
    covered = mask
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        remaining ^= bit
        covered |= adjacency[vertex]
    return covered == universe


def gamma_alpha_three(
    adjacency: tuple[int, ...],
    pairs: tuple[int, ...],
    triples: tuple[int, ...],
    quads: tuple[int, ...],
    universe: int,
) -> tuple[bool, tuple[int, ...], tuple[int, ...]]:
    if any(dominates(pair, adjacency, universe) for pair in pairs):
        return False, (), ()
    independent_triples = tuple(
        triple for triple in triples if is_independent(triple, adjacency)
    )
    if not independent_triples:
        return False, (), ()
    if any(is_independent(quad, adjacency) for quad in quads):
        return False, (), ()
    dominating_triples = tuple(
        triple for triple in triples if dominates(triple, adjacency, universe)
    )
    return True, independent_triples, dominating_triples


def induced_complement_paths(
    n: int, adjacency: tuple[int, ...]
) -> tuple[tuple[int, int, int, int], ...]:
    paths: list[tuple[int, int, int, int]] = []
    for vertices in itertools.combinations(range(n), 4):
        for ordering in itertools.permutations(vertices):
            x0, x1, x2, x3 = ordering
            consecutive = ((x0, x1), (x1, x2), (x2, x3))
            chords = ((x0, x2), (x0, x3), (x1, x3))
            if all(not (adjacency[u] >> v) & 1 for u, v in consecutive) and all(
                (adjacency[u] >> v) & 1 for u, v in chords
            ):
                paths.append(ordering)
    return tuple(paths)


def transition_table(
    n: int,
    adjacency: tuple[int, ...],
    dominating_triples: tuple[int, ...],
) -> dict[int, tuple[tuple[int, tuple[int, ...]], ...]]:
    dominating = set(dominating_triples)
    table: dict[int, tuple[tuple[int, tuple[int, ...]], ...]] = {}
    universe = (1 << n) - 1
    for state in dominating_triples:
        attacks: list[tuple[int, tuple[int, ...]]] = []
        outside = universe ^ state
        remaining_attacks = outside
        while remaining_attacks:
            attack_bit = remaining_attacks & -remaining_attacks
            attack = attack_bit.bit_length() - 1
            remaining_attacks ^= attack_bit
            successors: list[int] = []
            guards = state
            while guards:
                guard_bit = guards & -guards
                guard = guard_bit.bit_length() - 1
                guards ^= guard_bit
                if adjacency[guard] & attack_bit:
                    successor = (state ^ guard_bit) | attack_bit
                    if successor in dominating:
                        successors.append(successor)
            attacks.append((attack, tuple(successors)))
        table[state] = tuple(attacks)
    return table


def greatest_safe_kernel(
    dominating_triples: tuple[int, ...],
    transitions: dict[int, tuple[tuple[int, tuple[int, ...]], ...]],
    forbidden: frozenset[int],
) -> frozenset[int]:
    live = set(dominating_triples)
    live.difference_update(forbidden)
    while True:
        doomed = {
            state
            for state in live
            if any(
                not any(successor in live for successor in successors)
                for _attack, successors in transitions[state]
            )
        }
        if not doomed:
            return frozenset(live)
        live.difference_update(doomed)


def direct_state(reference: int, missing: int, outside: int) -> int:
    return (reference ^ (1 << missing)) | (1 << outside)


def search_record(
    record: str,
    n: int,
    masks_by_size: dict[int, tuple[int, ...]],
) -> tuple[int, int, dict[str, object] | None]:
    decoded_n, adjacency = decode_graph6(record)
    if decoded_n != n:
        raise AssertionError((decoded_n, n, record))
    universe = (1 << n) - 1
    eligible, independent_triples, dominating_triples = gamma_alpha_three(
        adjacency,
        masks_by_size[2],
        masks_by_size[3],
        masks_by_size[4],
        universe,
    )
    if not eligible:
        return 0, 0, None

    transitions = transition_table(n, adjacency, dominating_triples)
    independent_set = set(independent_triples)
    patterns_tested = 0
    for x0, x1, x2, x3 in induced_complement_paths(n, adjacency):
        path_mask = (1 << x0) | (1 << x1) | (1 << x2) | (1 << x3)
        available = tuple(v for v in range(n) if not (path_mask >> v) & 1)
        for reference_vertices in itertools.combinations(available, 3):
            reference = sum(1 << v for v in reference_vertices)
            if reference not in independent_set:
                continue
            for a, b, c in itertools.permutations(reference_vertices):
                positive_edges = (
                    (a, x0),
                    (a, x1),
                    (c, x1),
                    (c, x2),
                    (b, x2),
                    (b, x3),
                )
                if any(not ((adjacency[u] >> v) & 1) for u, v in positive_edges):
                    continue
                positive = frozenset(
                    (
                        direct_state(reference, a, x0),
                        direct_state(reference, a, x1),
                        direct_state(reference, c, x1),
                        direct_state(reference, c, x2),
                        direct_state(reference, b, x2),
                        direct_state(reference, b, x3),
                    )
                )
                required = positive | {reference}
                if not required.issubset(transitions):
                    continue
                forbidden = frozenset(
                    (
                        direct_state(reference, b, x0),
                        direct_state(reference, c, x0),
                        direct_state(reference, b, x1),
                        direct_state(reference, a, x2),
                        direct_state(reference, a, x3),
                        direct_state(reference, c, x3),
                    )
                )
                patterns_tested += 1
                kernel = greatest_safe_kernel(
                    dominating_triples, transitions, forbidden
                )
                if required.issubset(kernel):
                    labels = {
                        "a": a,
                        "b": b,
                        "c": c,
                        "x0": x0,
                        "x1": x1,
                        "x2": x2,
                        "x3": x3,
                    }
                    return 1, patterns_tested, {
                        "graph6": record.strip(),
                        "labels": labels,
                        "kernel_size": len(kernel),
                        "kernel_states": [
                            [v for v in range(n) if (state >> v) & 1]
                            for state in sorted(kernel)
                        ],
                    }
    return 1, patterns_tested, None


def graph6_records(order: int):
    with subprocess.Popen(
        [str(GENG), "-q", str(order)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as process:
        assert process.stdout is not None
        for line in process.stdout:
            record = line.strip()
            if record:
                yield record
        stderr = process.stderr.read() if process.stderr is not None else ""
        returncode = process.wait()
        if returncode:
            raise RuntimeError(f"geng failed with code {returncode}: {stderr}")


def fd_zro_positive_control() -> dict[str, object]:
    """Confirm that the proper-family kernel test detects the known near-model."""
    n, adjacency = decode_graph6("FDzro")
    expected_edges = {
        (0, 3),
        (0, 4),
        (0, 5),
        (1, 4),
        (1, 5),
        (1, 6),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 5),
        (3, 6),
        (4, 6),
    }
    decoded_edges = {
        (u, v)
        for u in range(n)
        for v in range(u + 1, n)
        if (adjacency[u] >> v) & 1
    }
    if decoded_edges != expected_edges:
        raise AssertionError("FDzro decoder control failed")
    triples = combinations_masks(n, 3)
    universe = (1 << n) - 1
    dominating_triples = tuple(
        state for state in triples if dominates(state, adjacency, universe)
    )
    transitions = transition_table(n, adjacency, dominating_triples)
    a, b, c, x0, x1, x2, x3 = range(7)
    reference = (1 << a) | (1 << b) | (1 << c)
    positive = {
        direct_state(reference, a, x0),
        direct_state(reference, a, x1),
        direct_state(reference, c, x1),
        direct_state(reference, c, x2),
        direct_state(reference, b, x2),
        direct_state(reference, b, x3),
    }
    forbidden = frozenset(
        {
            direct_state(reference, b, x0),
            direct_state(reference, c, x0),
            direct_state(reference, b, x1),
            direct_state(reference, a, x2),
            direct_state(reference, a, x3),
            direct_state(reference, c, x3),
        }
    )
    kernel = greatest_safe_kernel(dominating_triples, transitions, forbidden)
    if not ({reference} | positive).issubset(kernel) or len(kernel) != 21:
        raise AssertionError("FDzro proper-family kernel control failed")
    return {
        "graph6": "FDzro",
        "expected_gamma": 2,
        "restricted_kernel_size": len(kernel),
        "required_states_survive": True,
    }


def run(max_order: int) -> dict[str, object]:
    if not GENG.is_file():
        raise FileNotFoundError(GENG)
    started = time.monotonic()
    by_order: list[dict[str, object]] = []
    witness = None
    for n in range(7, max_order + 1):
        masks_by_size = {
            size: combinations_masks(n, size) for size in (2, 3, 4)
        }
        graphs = 0
        eligible_graphs = 0
        patterns = 0
        for record in graph6_records(n):
            graphs += 1
            eligible, tested, found = search_record(record, n, masks_by_size)
            eligible_graphs += eligible
            patterns += tested
            if found is not None:
                witness = found
                break
        by_order.append(
            {
                "order": n,
                "graphs_scanned": graphs,
                "gamma_alpha_3_graphs": eligible_graphs,
                "candidate_labelings_reaching_kernel_test": patterns,
                "countermodels": int(witness is not None),
            }
        )
        if witness is not None:
            break
    return {
        "claim_status": "BOUNDED_DIAGNOSTIC_ONLY",
        "scope": (
            "All unlabeled graphs emitted by pinned nauty geng through the "
            "reported order; arbitrary proper eternal triple families are "
            "covered for each tested labeled mixed-P4 pattern by the "
            "greatest restricted safe-kernel equivalence."
        ),
        "target_note_sha256": sha256(TARGET),
        "script_sha256": sha256(Path(__file__)),
        "geng_sha256": sha256(GENG),
        "max_order": max_order,
        "by_order": by_order,
        "countermodel": witness,
        "proper_family_positive_control": fd_zro_positive_control(),
        "elapsed_seconds": time.monotonic() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=8)
    args = parser.parse_args()
    if not 7 <= args.max_order <= 10:
        raise SystemExit("--max-order must lie between 7 and 10")
    print(json.dumps(run(args.max_order), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
