#!/usr/bin/env python3
"""Replay and independently audit the bounded cyclic-SDS window searches."""

from __future__ import annotations

import argparse
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import re
import subprocess
import tempfile

from verify_sds_167_neighborhood import (
    HALF,
    ORDER,
    individual_pafs,
    load_checkpoint,
    periodic_correlation,
)


WINDOW_PATTERN = re.compile(
    r"FOUR_WINDOW family=(\d+) sequence=(\d+) "
    r"positions=\(([^)]*)\) assignments=(\d+)"
)
MIXED_WINDOW_PATTERN = re.compile(
    r"MIXED_WINDOW family=(\d+) sequence=(\d+) "
    r"positions=\(([^)]*)\) assignments=(\d+)"
)


def replay(
    engine: Path,
    checkpoint: Path,
    half_size: int,
    families: int,
    output: Path,
) -> str:
    completed = subprocess.run(
        [
            str(engine),
            "--initial",
            str(checkpoint),
            "--profile",
            "5",
            "--four-window-mitm-half-size",
            str(half_size),
            "--window-family-count",
            str(families),
            "--output",
            str(output),
            "--seed",
            "668",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 1:
        raise AssertionError(
            f"H={half_size}, F={families} returned "
            f"{completed.returncode}: {completed.stderr}"
        )
    if completed.stderr:
        raise AssertionError(
            f"H={half_size}, F={families} wrote stderr: {completed.stderr}"
        )
    source_payload = json.loads(checkpoint.read_text(encoding="utf-8"))
    result_payload = json.loads(output.read_text(encoding="utf-8"))
    if result_payload.get("kind") != "cyclic_sds_167_checkpoint":
        raise AssertionError("window scan unexpectedly marked its output exact")
    if result_payload.get("sequences") != source_payload.get("sequences"):
        raise AssertionError("window scan changed the no-solution checkpoint")
    return completed.stdout


def replay_mixed(
    engine: Path,
    checkpoint: Path,
    half_size: int,
    families: int,
    output: Path,
) -> str:
    completed = subprocess.run(
        [
            str(engine),
            "--initial",
            str(checkpoint),
            "--profile",
            "5",
            "--mixed-window-mitm-half-size",
            str(half_size),
            "--window-family-count",
            str(families),
            "--mixed-window-batch-size",
            "8",
            "--output",
            str(output),
            "--seed",
            "668",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 1:
        raise AssertionError(
            f"mixed H={half_size}, F={families} returned "
            f"{completed.returncode}: {completed.stderr}"
        )
    if completed.stderr:
        raise AssertionError(
            f"mixed H={half_size}, F={families} wrote stderr: "
            f"{completed.stderr}"
        )
    source_payload = json.loads(checkpoint.read_text(encoding="utf-8"))
    result_payload = json.loads(output.read_text(encoding="utf-8"))
    if result_payload.get("kind") != "cyclic_sds_167_checkpoint":
        raise AssertionError("mixed scan unexpectedly marked its output exact")
    if result_payload.get("sequences") != source_payload.get("sequences"):
        raise AssertionError("mixed scan changed the no-solution checkpoint")
    return completed.stdout


def parsed_windows(
    stdout: str,
) -> dict[tuple[int, int], tuple[tuple[int, ...], int]]:
    result: dict[tuple[int, int], tuple[tuple[int, ...], int]] = {}
    for match in WINDOW_PATTERN.finditer(stdout):
        family, sequence, raw_positions, assignments = match.groups()
        positions = tuple(map(int, raw_positions.split(",")))
        key = (int(family), int(sequence))
        if key in result:
            raise AssertionError(f"duplicate window record: {key}")
        result[key] = (positions, int(assignments))
    return result


def parsed_mixed_windows(
    stdout: str,
) -> dict[tuple[int, int], tuple[tuple[int, ...], int]]:
    result: dict[tuple[int, int], tuple[tuple[int, ...], int]] = {}
    for match in MIXED_WINDOW_PATTERN.finditer(stdout):
        family, sequence, raw_positions, assignments = match.groups()
        positions = tuple(map(int, raw_positions.split(",")))
        key = (int(family), int(sequence))
        if key in result:
            raise AssertionError(f"duplicate mixed-window record: {key}")
        result[key] = (positions, int(assignments))
    return result


def assignment_deltas(
    sequence: tuple[int, ...],
    window: tuple[int, ...],
    half_size: int,
) -> tuple[tuple[int, ...], ...]:
    baseline = tuple(
        periodic_correlation(sequence, lag) for lag in range(1, HALF + 1)
    )
    result: list[tuple[int, ...]] = []
    for plus_indices in combinations(range(2 * half_size), half_size):
        plus = set(plus_indices)
        modified = list(sequence)
        for index, position in enumerate(window):
            modified[position] = 1 if index in plus else -1
        paf = tuple(
            periodic_correlation(tuple(modified), lag)
            for lag in range(1, HALF + 1)
        )
        result.append(tuple(value - old for value, old in zip(paf, baseline)))
    return tuple(result)


def independent_small_brute_force(
    sequences: tuple[tuple[int, ...], ...],
    windows: dict[tuple[int, int], tuple[tuple[int, ...], int]],
) -> int:
    half_size = 2
    expected_assignments = comb(2 * half_size, half_size)
    deltas: list[tuple[tuple[int, ...], ...]] = []
    for which in range(4):
        positions, assignments = windows[(0, which)]
        if len(positions) != 2 * half_size or len(set(positions)) != len(positions):
            raise AssertionError("small window has invalid positions")
        if assignments != expected_assignments:
            raise AssertionError("small window has the wrong assignment count")
        deltas.append(assignment_deltas(sequences[which], positions, half_size))
    paf = individual_pafs(sequences)
    baseline = tuple(
        sum(paf[which][lag] for which in range(4))
        for lag in range(1, HALF + 1)
    )
    exact = 0
    for first, second, third, fourth in product(*deltas):
        exact += all(
            baseline[index]
            + first[index]
            + second[index]
            + third[index]
            + fourth[index]
            == 0
            for index in range(HALF)
        )
    return exact


def verify_small_scan(
    sequences: tuple[tuple[int, ...], ...], stdout: str
) -> None:
    windows = parsed_windows(stdout)
    if set(windows) != {(0, which) for which in range(4)}:
        raise AssertionError("small scan emitted the wrong window set")
    brute = re.search(
        r"FOUR_WINDOW_BRUTE_FORCE family=0 cases=(\d+) exact_solutions=(\d+)",
        stdout,
    )
    if brute is None or tuple(map(int, brute.groups())) != (1_296, 0):
        raise AssertionError("engine small-domain brute-force summary is wrong")
    if independent_small_brute_force(sequences, windows) != 0:
        raise AssertionError("independent small-domain enumeration found a solution")
    print("PASS independent H=2 four-window enumeration cases=1296 exact=0")


def verify_large_scan(
    sequences: tuple[tuple[int, ...], ...], stdout: str
) -> None:
    half_size = 6
    families = 12
    assignments = comb(2 * half_size, half_size)
    pair_records = assignments**2
    conceptual_per_family = pair_records**2
    conceptual_exhausted = families * conceptual_per_family
    unique_exhausted = 1 + families * (conceptual_per_family - 1)
    windows = parsed_windows(stdout)
    if set(windows) != {
        (family, which)
        for family in range(families)
        for which in range(4)
    }:
        raise AssertionError("large scan emitted the wrong window set")
    for which in range(4):
        used: set[int] = set()
        for family in range(families):
            positions, count = windows[(family, which)]
            if count != assignments or len(positions) != 2 * half_size:
                raise AssertionError("large window has the wrong dimensions")
            if len(set(positions)) != len(positions) or used & set(positions):
                raise AssertionError("large windows are not support-disjoint")
            if any(sequences[which][position] != 1
                   for position in positions[:half_size]):
                raise AssertionError("large window plus support has a minus sign")
            if any(sequences[which][position] != -1
                   for position in positions[half_size:]):
                raise AssertionError("large window minus support has a plus sign")
            used.update(positions)
    family_summaries = re.findall(
        r"FOUR_WINDOW_FAMILY family=(\d+) pair_records=(\d+) "
        r"record_bytes=(\d+) cumulative_right_pair_probes=(\d+) "
        r"cumulative_exact_comparisons=(\d+) found=(\d+)",
        stdout,
    )
    if len(family_summaries) != families:
        raise AssertionError("large scan has the wrong number of family summaries")
    for family, summary in enumerate(family_summaries):
        values = tuple(map(int, summary))
        if values[0] != family or values[1] != pair_records:
            raise AssertionError("large scan family indexing/count is wrong")
        if values[3:] != ((family + 1) * pair_records, 0, 0):
            raise AssertionError("large scan family result is wrong")
    overall = re.search(
        r"FOUR_WINDOW_MITM half_size=(\d+) requested_families=(\d+) "
        r"fully_exhausted_families=(\d+) assignments_per_sequence=(\d+) "
        r"pair_records=(\d+) conceptual_per_family=(\d+) "
        r"conceptual_exhausted=(\d+) unique_exhausted=(\d+) "
        r"right_pair_probes=(\d+) exact_comparisons=(\d+)",
        stdout,
    )
    expected = (
        half_size,
        families,
        families,
        assignments,
        pair_records,
        conceptual_per_family,
        conceptual_exhausted,
        unique_exhausted,
        families * pair_records,
        0,
    )
    if overall is None or tuple(map(int, overall.groups())) != expected:
        raise AssertionError("large scan overall summary is wrong")
    print(
        "PASS exact aligned four-window union "
        f"families={families} unique_states={unique_exhausted} exact=0"
    )


def independent_small_mixed_brute_force(
    sequences: tuple[tuple[int, ...], ...],
    windows: dict[tuple[int, int], tuple[tuple[int, ...], int]],
) -> int:
    half_size = 2
    families = 2
    expected_assignments = comb(2 * half_size, half_size)
    zero = (0,) * HALF
    configurations: list[tuple[tuple[int, ...], ...]] = []
    for which in range(4):
        unique = [zero]
        for family in range(families):
            positions, assignments = windows[(family, which)]
            if len(positions) != 2 * half_size or assignments != expected_assignments:
                raise AssertionError("small mixed window has invalid dimensions")
            deltas = assignment_deltas(
                sequences[which], positions, half_size
            )
            if deltas[0] != zero:
                raise AssertionError("small mixed assignment zero is not identity")
            unique.extend(deltas[1:])
        if len(unique) != 1 + families * (expected_assignments - 1):
            raise AssertionError("small mixed canonical count is wrong")
        configurations.append(tuple(unique))
    paf = individual_pafs(sequences)
    baseline = tuple(
        sum(paf[which][lag] for which in range(4))
        for lag in range(1, HALF + 1)
    )
    exact = 0
    for first, second, third, fourth in product(*configurations):
        exact += all(
            baseline[index]
            + first[index]
            + second[index]
            + third[index]
            + fourth[index]
            == 0
            for index in range(HALF)
        )
    return exact


def verify_small_mixed_scan(
    sequences: tuple[tuple[int, ...], ...], stdout: str
) -> None:
    windows = parsed_mixed_windows(stdout)
    if set(windows) != {
        (family, which) for family in range(2) for which in range(4)
    }:
        raise AssertionError("small mixed scan emitted the wrong windows")
    for which in range(4):
        first = set(windows[(0, which)][0])
        second = set(windows[(1, which)][0])
        if first & second:
            raise AssertionError("small mixed supports are not disjoint")
    brute = re.search(
        r"MIXED_WINDOW_BRUTE_FORCE conceptual_cases=(\d+) "
        r"exact_representations=(\d+)",
        stdout,
    )
    if brute is None or tuple(map(int, brute.groups())) != (20_736, 0):
        raise AssertionError("engine mixed brute-force summary is wrong")
    overall = re.search(
        r"MIXED_WINDOW_MITM half_size=2 families=2 assignments_per_sequence=6 "
        r"batch_size=8 batch_begin=0 batch_end=1 total_batches=1 "
        r"fully_exhausted_left_family_pairs=4 conceptual_exhausted=20736 "
        r"unique_exhausted=14641 full_unique_domain=14641 "
        r"right_pair_probes=144 bloom_positive_probes=(\d+) "
        r"exact_comparisons=(\d+)",
        stdout,
    )
    if overall is None or tuple(map(int, overall.groups())) != (0, 0):
        raise AssertionError("small mixed MITM summary is wrong")
    if independent_small_mixed_brute_force(sequences, windows) != 0:
        raise AssertionError("independent small mixed enumeration found a solution")
    print("PASS independent mixed H=2,F=2 union unique_states=14641 exact=0")


def verify_large_mixed_scan(
    sequences: tuple[tuple[int, ...], ...], stdout: str
) -> None:
    half_size = 6
    families = 12
    assignments = comb(2 * half_size, half_size)
    pair_count = assignments**2
    left_records = 8 * pair_count
    right_records = families**2 * pair_count
    conceptual = (families * assignments) ** 4
    unique = (1 + families * (assignments - 1)) ** 4
    windows = parsed_mixed_windows(stdout)
    if set(windows) != {
        (family, which)
        for family in range(families)
        for which in range(4)
    }:
        raise AssertionError("large mixed scan emitted the wrong windows")
    for which in range(4):
        used: set[int] = set()
        for family in range(families):
            positions, count = windows[(family, which)]
            if count != assignments or len(positions) != 2 * half_size:
                raise AssertionError("large mixed window has wrong dimensions")
            if len(set(positions)) != len(positions) or used & set(positions):
                raise AssertionError("large mixed supports are not disjoint")
            if any(sequences[which][position] != 1
                   for position in positions[:half_size]):
                raise AssertionError("large mixed plus support has a minus")
            if any(sequences[which][position] != -1
                   for position in positions[half_size:]):
                raise AssertionError("large mixed minus support has a plus")
            used.update(positions)
    batches = re.findall(
        r"MIXED_WINDOW_BATCH batch=(\d+) first_left_pair=(\d+) "
        r"left_family_pairs=(\d+) left_records=(\d+) record_bytes=(\d+) "
        r"bloom_bytes=(\d+) cumulative_right_pair_probes=(\d+) "
        r"cumulative_bloom_positive_probes=(\d+) "
        r"cumulative_exact_comparisons=(\d+) found=(\d+)",
        stdout,
    )
    if len(batches) != 18:
        raise AssertionError("large mixed scan has the wrong batch count")
    previous_bloom = -1
    for batch, raw in enumerate(batches):
        values = tuple(map(int, raw))
        if values[:6] != (
            batch,
            8 * batch,
            8,
            left_records,
            left_records * 24,
            1 << 25,
        ):
            raise AssertionError("large mixed batch dimensions are wrong")
        if values[6] != (batch + 1) * right_records:
            raise AssertionError("large mixed cumulative probe count is wrong")
        if values[7] <= previous_bloom or values[8:] != (0, 0):
            raise AssertionError("large mixed batch result is wrong")
        previous_bloom = values[7]
    overall = re.search(
        r"MIXED_WINDOW_MITM half_size=6 families=12 "
        r"assignments_per_sequence=924 batch_size=8 batch_begin=0 "
        r"batch_end=18 total_batches=18 "
        r"fully_exhausted_left_family_pairs=144 "
        r"conceptual_exhausted=(\d+) unique_exhausted=(\d+) "
        r"full_unique_domain=(\d+) right_pair_probes=(\d+) "
        r"bloom_positive_probes=(\d+) exact_comparisons=(\d+)",
        stdout,
    )
    expected = (conceptual, unique, unique, 18 * right_records, 877_347, 0)
    if overall is None or tuple(map(int, overall.groups())) != expected:
        raise AssertionError("large mixed scan overall summary is wrong")
    print(
        "PASS exact mixed four-window union "
        f"families={families} unique_states={unique} exact=0"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path(__file__).resolve().parent
        / "output"
        / "sds_167_local_continued_600s.json",
    )
    parser.add_argument("--engine", required=True, type=Path)
    args = parser.parse_args()
    checkpoint = args.checkpoint.resolve()
    engine = args.engine.resolve()
    if not engine.is_file():
        parser.error(f"engine does not exist: {engine}")
    sequences = load_checkpoint(checkpoint)
    with tempfile.TemporaryDirectory(prefix="sds-167-windows-") as directory:
        temporary = Path(directory)
        small = replay(engine, checkpoint, 2, 1, temporary / "small.json")
        verify_small_scan(sequences, small)
        large = replay(engine, checkpoint, 6, 12, temporary / "large.json")
        verify_large_scan(sequences, large)
        mixed_small = replay_mixed(
            engine, checkpoint, 2, 2, temporary / "mixed-small.json"
        )
        verify_small_mixed_scan(sequences, mixed_small)
        mixed_large = replay_mixed(
            engine, checkpoint, 6, 12, temporary / "mixed-large.json"
        )
        verify_large_mixed_scan(sequences, mixed_large)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
