#!/usr/bin/env python3
"""Independently replay the cyclic-SDS decimation and radius-four audit."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from math import comb
from pathlib import Path
import re
import subprocess
import tempfile


ORDER = 167
HALF = 83
EXPECTED_CHECKPOINT_SHA256 = (
    "3c4a23d1190ed74e464dc66e852dd0730c97cfd4f1d12aa4946de05aff5a8edd"
)
EXPECTED_ROW_SUMS = (3, 7, 9, 23)
EXPECTED_METRICS = (64, 136, 46, 2)


@dataclass(frozen=True)
class Metrics:
    energy: int
    quartic: int
    bad_lags: int
    maximum: int

    @property
    def energy_key(self) -> tuple[int, int, int, int]:
        return (self.energy, self.quartic, self.maximum, self.bad_lags)

    @property
    def quartic_key(self) -> tuple[int, int, int, int]:
        return (self.quartic, self.energy, self.maximum, self.bad_lags)

    @property
    def maximum_key(self) -> tuple[int, int, int, int]:
        return (self.maximum, self.quartic, self.energy, self.bad_lags)


def periodic_correlation(sequence: tuple[int, ...], lag: int) -> int:
    return sum(
        sequence[index] * sequence[(index + lag) % ORDER]
        for index in range(ORDER)
    )


def individual_pafs(
    sequences: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(periodic_correlation(sequence, lag) for lag in range(ORDER))
        for sequence in sequences
    )


def metrics_from_raw_residuals(residuals: tuple[int, ...]) -> Metrics:
    if len(residuals) != HALF:
        raise ValueError("expected 83 independent residuals")
    quarter: list[int] = []
    for value in residuals:
        if value % 4:
            raise ValueError("a periodic residual is not divisible by four")
        quarter.append(value // 4)
    return Metrics(
        energy=sum(value * value for value in quarter),
        quartic=sum(value**4 for value in quarter),
        bad_lags=sum(value != 0 for value in quarter),
        maximum=max(map(abs, quarter), default=0),
    )


def load_checkpoint(path: Path) -> tuple[tuple[int, ...], ...]:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_CHECKPOINT_SHA256:
        raise ValueError(f"unexpected checkpoint SHA-256: {digest}")
    payload = json.loads(raw)
    if payload.get("kind") != "cyclic_sds_167_checkpoint":
        raise ValueError("expected a nonexact cyclic-SDS checkpoint")
    if payload.get("order") != ORDER or payload.get("hadamard_order") != 668:
        raise ValueError("checkpoint order metadata is wrong")
    raw_sequences = payload.get("sequences")
    if not isinstance(raw_sequences, list) or len(raw_sequences) != 4:
        raise ValueError("checkpoint must contain four sequences")
    sequences: list[tuple[int, ...]] = []
    for raw_sequence in raw_sequences:
        if (
            not isinstance(raw_sequence, list)
            or len(raw_sequence) != ORDER
            or any(type(value) is not int or value not in (-1, 1)
                   for value in raw_sequence)
        ):
            raise ValueError("checkpoint contains an invalid sign sequence")
        sequences.append(tuple(raw_sequence))
    result = tuple(sequences)
    row_sums = tuple(map(sum, result))
    if row_sums != EXPECTED_ROW_SUMS:
        raise ValueError(f"unexpected row sums: {row_sums}")
    paf = individual_pafs(result)
    correlations = tuple(sum(paf[which][lag] for which in range(4))
                         for lag in range(ORDER))
    if tuple(payload.get("periodic_correlation_sums", ())) != correlations:
        raise ValueError("stored correlations do not match the sequences")
    metrics = metrics_from_raw_residuals(correlations[1 : HALF + 1])
    if (
        metrics.energy,
        metrics.quartic,
        metrics.bad_lags,
        metrics.maximum,
    ) != EXPECTED_METRICS:
        raise ValueError(f"unexpected checkpoint metrics: {metrics}")
    return result


def neighborhood_counts(
    sequences: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], tuple[int, ...], int, int]:
    plus = tuple(sum(value == 1 for value in sequence) for sequence in sequences)
    minus = tuple(ORDER - value for value in plus)
    exchanges = tuple(p * m for p, m in zip(plus, minus, strict=True))
    same = tuple(
        comb(p, 2) * comb(m, 2) for p, m in zip(plus, minus, strict=True)
    )
    cross = sum(
        exchanges[first] * exchanges[second]
        for first in range(4)
        for second in range(first + 1, 4)
    )
    total = 1 + sum(exchanges) + sum(same) + cross
    return exchanges, same, cross, total


def independent_decimation_scan(
    sequences: tuple[tuple[int, ...], ...],
) -> None:
    paf = individual_pafs(sequences)
    permuted = tuple(
        ((),) + tuple(
            tuple(paf[which][(multiplier * lag) % ORDER]
                  for lag in range(1, HALF + 1))
            for multiplier in range(1, HALF + 1)
        )
        for which in range(4)
    )
    base = permuted[0][1]
    best_keys: list[tuple[int, int, int, int] | None] = [None, None, None]
    best_tuples: list[tuple[int, int, int, int] | None] = [None, None, None]
    tie_counts = [0, 0, 0]
    cases = 0
    for second in range(1, HALF + 1):
        first_pair = tuple(
            base[index] + permuted[1][second][index]
            for index in range(HALF)
        )
        for third in range(1, HALF + 1):
            first_three = tuple(
                first_pair[index] + permuted[2][third][index]
                for index in range(HALF)
            )
            for fourth in range(1, HALF + 1):
                residuals = tuple(
                    first_three[index] + permuted[3][fourth][index]
                    for index in range(HALF)
                )
                metrics = metrics_from_raw_residuals(residuals)
                keys = (
                    metrics.energy_key,
                    metrics.quartic_key,
                    metrics.maximum_key,
                )
                multipliers = (1, second, third, fourth)
                for index, key in enumerate(keys):
                    if best_keys[index] is None or key < best_keys[index]:
                        best_keys[index] = key
                        best_tuples[index] = multipliers
                        tie_counts[index] = 1
                    elif key == best_keys[index]:
                        tie_counts[index] += 1
                cases += 1
    expected_keys = (
        (64, 136, 2, 46),
        (136, 64, 2, 46),
        (2, 136, 64, 46),
    )
    if cases != HALF**3:
        raise AssertionError(f"decimation case count is {cases}")
    if tuple(best_keys) != expected_keys:
        raise AssertionError(f"unexpected decimation minima: {best_keys}")
    if tuple(best_tuples) != ((1, 1, 1, 1),) * 3:
        raise AssertionError(f"unexpected decimation winners: {best_tuples}")
    if tuple(tie_counts) != (1, 1, 1):
        raise AssertionError(f"unexpected decimation tie counts: {tie_counts}")
    print(f"PASS independent relative decimation orbit cases={cases}")


def require_pattern(text: str, pattern: str, label: str) -> re.Match[str]:
    match = re.search(pattern, text)
    if match is None:
        raise AssertionError(f"missing {label} in scan output")
    return match


def replay_engine_scan(
    engine: Path,
    checkpoint: Path,
    mode: str,
    output: Path,
) -> str:
    completed = subprocess.run(
        [
            str(engine),
            mode,
            "--scan-objective",
            "energy",
            "--initial",
            str(checkpoint),
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
            f"{mode} returned {completed.returncode}: {completed.stderr}"
        )
    if completed.stderr:
        raise AssertionError(f"{mode} wrote stderr: {completed.stderr}")
    payload = json.loads(output.read_text(encoding="utf-8"))
    if payload.get("kind") != "cyclic_sds_167_checkpoint":
        raise AssertionError(f"{mode} unexpectedly produced an exact output")
    source_payload = json.loads(checkpoint.read_text(encoding="utf-8"))
    if payload.get("sequences") != source_payload.get("sequences"):
        raise AssertionError(f"{mode} did not preserve the unique champion")
    return completed.stdout


def verify_radius_four_scans(engine: Path, checkpoint: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="sds-167-neighborhood-") as directory:
        temporary = Path(directory)
        same = replay_engine_scan(
            engine,
            checkpoint,
            "--same-sequence-pair-scan",
            temporary / "same.json",
        )
        cross = replay_engine_scan(
            engine,
            checkpoint,
            "--cross-sequence-pair-scan",
            temporary / "cross.json",
        )
    same_cases = int(require_pattern(
        same, r"SAME_SEQUENCE_PAIR_SCAN cases=(\d+)", "same case count"
    ).group(1))
    cross_counts = require_pattern(
        cross,
        r"CROSS_SEQUENCE_PAIR_SCAN singles=(\d+) pairs=(\d+)",
        "cross case counts",
    )
    singles, cross_cases = map(int, cross_counts.groups())
    champion = (
        r"BEST_(?:ENERGY|QUARTIC|MAXIMUM) energy=64 quartic=136 "
        r"bad_lags=46 maximum_quarter_residual=2 "
        r"lexicographic_ties_including_incumbent=1"
    )
    if len(re.findall(champion, same)) != 3:
        raise AssertionError("same-sequence champion summaries do not match")
    if len(re.findall(champion, cross)) != 3:
        raise AssertionError("cross-sequence champion summaries do not match")
    same_ties = require_pattern(
        same,
        r"PRIMARY_TIES_INCLUDING_INCUMBENT energy=(\d+) quartic=(\d+) "
        r"maximum=(\d+)",
        "same primary ties",
    )
    cross_ties = require_pattern(
        cross,
        r"PRIMARY_TIES_INCLUDING_INCUMBENT energy=(\d+) quartic=(\d+) "
        r"maximum=(\d+)",
        "cross primary ties",
    )
    same_energy, same_quartic, same_maximum = map(int, same_ties.groups())
    cross_energy, cross_quartic, cross_maximum = map(int, cross_ties.groups())
    total = 1 + singles + same_cases + cross_cases
    combined_energy_ties = same_energy + cross_energy - 1
    combined_quartic_ties = same_quartic + cross_quartic - 1
    combined_maximum_ties = same_maximum + cross_maximum - 1
    if (singles, same_cases, cross_cases, total) != (
        27_722,
        46_884_138,
        288_185_440,
        335_097_301,
    ):
        raise AssertionError("radius-four scan counts do not match")
    if (combined_energy_ties, combined_quartic_ties, combined_maximum_ties) != (
        1,
        1,
        5_442,
    ):
        raise AssertionError("combined primary tie counts do not match")
    print(
        "PASS complete fixed-profile Hamming-radius-four audit "
        f"states={total} energy_ties={combined_energy_ties} "
        f"quartic_ties={combined_quartic_ties} "
        f"maximum_ties={combined_maximum_ties}"
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
    exchanges, same, cross, total = neighborhood_counts(sequences)
    if exchanges != (6_970, 6_960, 6_952, 6_840):
        raise AssertionError(f"unexpected exchange counts: {exchanges}")
    if sum(same) != 46_884_138 or cross != 288_185_440:
        raise AssertionError("independent neighborhood class counts do not match")
    if total != 335_097_301:
        raise AssertionError(f"unexpected radius-four total: {total}")
    print(f"PASS checkpoint SHA-256={EXPECTED_CHECKPOINT_SHA256}")
    print(
        "PASS independent combinatorial counts "
        f"singles={sum(exchanges)} same={sum(same)} cross={cross} total={total}"
    )
    independent_decimation_scan(sequences)
    verify_radius_four_scans(engine, checkpoint)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
