#!/usr/bin/env python3
"""Exact MITM audit of primitive-zero branches in the LP333 phase cone.

For one fixed compressed profile and one channel, the recombined phase word

    W = U_0 + alpha U_1 + alpha^2 U_2

has one coefficient on each of the twelve H-orbits in C_37^*.  At the first
primitive factor its value is

    W(zeta) = W(0) + sum_j W_j * sum_(h in H_j) zeta^h
              in F_(167^12).

Every active residue fiber contributes one independent trit.  This script
enumerates the local alphabet class by class, balances the active trits
between two halves, and checks the exact zero-sum condition with a sorted
meet-in-the-middle over all 36 prime-field coordinates of the repository's
ambient F_(167^36) representation.

The test is deliberately stronger than needed for a degenerate norm-cone
branch: it asks whether either channel can vanish individually.  If both
single-channel zero sets are empty, all three primitive degenerate branches
are impossible for that fixed profile.  No stochastic search or timeout
inference is used.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import itertools
import json
from pathlib import Path
import resource
import sys
import time
from typing import Iterable, Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
if str(SEARCH_ROOT) not in sys.path:
    sys.path.insert(0, str(SEARCH_ROOT))

from verify_lp333_order3_char37_transfer import PROFILES  # noqa: E402
from verify_lp333_order3_labeled_jet import (  # noqa: E402
    ZERO_A_PLUS,
    ZERO_B_PLUS,
)
from verify_lp333_order3_phase_factor import (  # noqa: E402
    fiber_phase,
    phase_from_trit,
)
from verify_lp333_order3_profile9 import actual_profile_counts  # noqa: E402
import verify_lp333_order3_phase_prime167 as phase167  # noqa: E402
import verify_lp333_order3_prime167_split as split  # noqa: E402


P = 167
COORDINATES = 36
VOID_KEY = np.dtype((np.void, COORDINATES))


def l_to_u8(value: split.L) -> np.ndarray:
    """Expand the repository L element into its 36 F_167 coordinates."""

    flat = [coordinate for pair in value for coordinate in pair]
    if len(flat) != COORDINATES or any(not 0 <= value < P for value in flat):
        raise AssertionError("invalid ambient field coordinate")
    return np.asarray(flat, dtype=np.uint8)


def u8_to_semantic(value: np.ndarray) -> tuple[int, ...]:
    if value.shape != (COORDINATES,):
        raise ValueError("expected one ambient field coordinate")
    return tuple(int(entry) for entry in value)


def zero_column_value(channel: int, alpha: split.L) -> split.L:
    """Return W_X(0) from the fixed normalized zero column."""

    word = (ZERO_A_PLUS, ZERO_B_PLUS)[channel]
    phases = tuple(fiber_phase(word, residue) for residue in range(3))
    reduced = tuple((a % P, b % P) for a, b in phases)
    alpha_squared = split.l_multiply(alpha, alpha)
    return split.l_add(
        split.l_embed(reduced[0]),
        split.l_add(
            split.l_multiply(alpha, split.l_embed(reduced[1])),
            split.l_multiply(alpha_squared, split.l_embed(reduced[2])),
        ),
    )


def local_w_values(
    profile: Sequence[int], alpha: split.L
) -> tuple[split.L, ...]:
    """Return the complete distinct W alphabet for one residue profile."""

    if len(profile) != 3 or sum(int(value) for value in profile) not in (3, 6):
        raise ValueError("expected a physical weight-three or weight-six profile")
    active = tuple(index for index, count in enumerate(profile) if count in (1, 2))
    alpha_powers = (split.L_ONE, alpha, split.l_multiply(alpha, alpha))
    values = []
    for trits in itertools.product(range(3), repeat=len(active)):
        trit_by_residue = dict(zip(active, trits))
        total = split.L_ZERO
        for residue, count in enumerate(profile):
            if count not in (1, 2):
                continue
            exact = phase_from_trit(count, trit_by_residue[residue])
            reduced = (exact[0] % P, exact[1] % P)
            total = split.l_add(
                total,
                split.l_multiply(
                    alpha_powers[residue],
                    split.l_embed(reduced),
                ),
            )
        values.append(total)
    if len(set(values)) != 3 ** len(active):
        raise AssertionError("a local phase alphabet lost injectivity")
    return tuple(values)


def class_options(
    profile_ids: Sequence[int],
    alpha: split.L,
    factor_index: int,
    channel: int,
) -> tuple[tuple[int, np.ndarray], ...]:
    """Return (active trits, contribution options) for all twelve classes."""

    if len(profile_ids) != 12:
        raise ValueError("a channel profile must have twelve classes")
    if not 0 <= factor_index < 6:
        raise ValueError("the primitive factor index must lie in 0,...,5")
    class_of = {
        value: index
        for index, part in enumerate(split.CLASSES)
        for value in part
    }
    factor_multiplier = pow(P, factor_index, 37)
    result = []
    for class_index, profile_id in enumerate(profile_ids):
        profile = actual_profile_counts(
            channel,
            class_index,
            PROFILES[profile_id],
        )
        active = sum(count in (1, 2) for count in profile)
        period_index = class_of[
            split.CLASSES[class_index][0] * factor_multiplier % 37
        ]
        period = split.period(period_index)
        values = tuple(
            split.l_multiply(period, value)
            for value in local_w_values(profile, alpha)
        )
        options = np.stack(tuple(l_to_u8(value) for value in values))
        if options.shape != (3**active, COORDINATES):
            raise AssertionError("a class alphabet has the wrong size")
        result.append((active, options))
    return tuple(result)


def balanced_partition(
    options: Sequence[tuple[int, np.ndarray]],
) -> tuple[tuple[tuple[int, np.ndarray], ...], tuple[tuple[int, np.ndarray], ...]]:
    """Find the deterministically best of the 2^12 class partitions."""

    total = sum(option[0] for option in options)
    best_key: tuple[int, tuple[int, ...]] | None = None
    best_indices: tuple[int, ...] | None = None
    for mask in range(1 << len(options)):
        indices = tuple(
            index for index in range(len(options)) if mask & (1 << index)
        )
        weight = sum(options[index][0] for index in indices)
        # Complement symmetry: retain the lighter half, then lexicographic tie.
        if weight > total - weight:
            continue
        key = (total - 2 * weight, indices)
        if best_key is None or key < best_key:
            best_key = key
            best_indices = indices
    if best_indices is None:
        raise AssertionError("the phase partition search failed")
    selected = set(best_indices)
    return (
        tuple(options[index] for index in best_indices),
        tuple(
            option for index, option in enumerate(options) if index not in selected
        ),
    )


def enumerate_sums(
    options: Sequence[tuple[int, np.ndarray]],
) -> np.ndarray:
    """Enumerate exact componentwise sums in F_167."""

    sums = np.zeros((1, COORDINATES), dtype=np.uint8)
    for active, alphabet in options:
        if alphabet.shape != (3**active, COORDINATES):
            raise AssertionError("inconsistent alphabet metadata")
        old_count = sums.shape[0]
        new_count = old_count * alphabet.shape[0]
        expanded = np.empty((new_count, COORDINATES), dtype=np.uint8)
        base16 = sums.astype(np.uint16, copy=False)
        for index, value in enumerate(alphabet.astype(np.uint16, copy=False)):
            block = (base16 + value) % P
            expanded[index * old_count : (index + 1) * old_count] = block
        sums = expanded
    return sums


def sorted_void_keys(values: np.ndarray) -> np.ndarray:
    if values.dtype != np.uint8 or values.ndim != 2 or values.shape[1] != COORDINATES:
        raise ValueError("invalid key matrix")
    return np.sort(np.ascontiguousarray(values).view(VOID_KEY).reshape(-1))


def count_zero_sums(
    left: np.ndarray,
    right: np.ndarray,
    constant: np.ndarray,
    chunk_size: int = 500_000,
) -> int:
    """Count labelled pairs with left+right+constant=0 in F_167."""

    left_keys = sorted_void_keys(left)
    total = 0
    constant16 = constant.astype(np.uint16, copy=False)
    for start in range(0, len(right), chunk_size):
        stop = min(start + chunk_size, len(right))
        target = (
            P
            - (
                right[start:stop].astype(np.uint16, copy=False)
                + constant16
            )
            % P
        ) % P
        target8 = target.astype(np.uint8, copy=False)
        target_keys = np.ascontiguousarray(target8).view(VOID_KEY).reshape(-1)
        lower = np.searchsorted(left_keys, target_keys, side="left")
        upper = np.searchsorted(left_keys, target_keys, side="right")
        total += int(np.sum(upper - lower, dtype=np.int64))
    return total


def direct_small_audit(
    options: Sequence[tuple[int, np.ndarray]],
    constant: np.ndarray,
) -> None:
    """Cross-check MITM mechanics on deterministic prefixes."""

    reduced = []
    weight = 0
    for option in options:
        if weight + option[0] > 8:
            break
        reduced.append(option)
        weight += option[0]
    if not reduced:
        raise AssertionError("no small audit prefix was available")
    split_at = len(reduced) // 2
    left = enumerate_sums(reduced[:split_at])
    right = enumerate_sums(reduced[split_at:])
    synthetic = (
        P
        - (
            left[0].astype(np.uint16)
            + right[0].astype(np.uint16)
        )
        % P
    ) % P
    for index, audit_constant in enumerate(
        (constant, synthetic.astype(np.uint8))
    ):
        mitm = count_zero_sums(left, right, audit_constant)
        joined = (
            left[:, None, :].astype(np.uint16)
            + right[None, :, :].astype(np.uint16)
            + audit_constant.astype(np.uint16)
        ) % P
        brute = int(np.count_nonzero(np.all(joined == 0, axis=2)))
        if mitm != brute:
            raise AssertionError("MITM/direct prefix counts disagree")
        if index == 1 and brute == 0:
            raise AssertionError("the synthetic positive MITM control vanished")


def audit_factor_formula(
    channel: int,
    profile_ids: Sequence[int],
    alpha: split.L,
    factor_index: int,
    options: Sequence[tuple[int, np.ndarray]],
    constant: np.ndarray,
) -> None:
    """Compare the period sum with direct polynomial evaluation."""

    word = [split.L_ZERO] * 37
    word[0] = zero_column_value(channel, alpha)
    selected = constant.astype(np.uint16)
    for class_index, profile_id in enumerate(profile_ids):
        profile = actual_profile_counts(
            channel,
            class_index,
            PROFILES[profile_id],
        )
        values = local_w_values(profile, alpha)
        choice = (7 * class_index + 5 * factor_index + channel) % len(values)
        for column in split.CLASSES[class_index]:
            word[column] = values[choice]
        selected = (selected + options[class_index][1][choice]) % P
    _, primitive = phase167.recombined_coordinates(tuple(word))
    if u8_to_semantic(selected.astype(np.uint8)) != u8_to_semantic(
        l_to_u8(primitive[factor_index])
    ):
        raise AssertionError("period MITM formula disagrees with direct CRT evaluation")


def audit_channel(
    label: str,
    channel: int,
    profile_ids: Sequence[int],
    alpha: split.L,
    factor_index: int,
) -> dict[str, object]:
    started = time.monotonic()
    options = class_options(profile_ids, alpha, factor_index, channel)
    active = sum(value[0] for value in options)
    left_options, right_options = balanced_partition(options)
    left_weight = sum(value[0] for value in left_options)
    right_weight = sum(value[0] for value in right_options)
    constant = l_to_u8(zero_column_value(channel, alpha))

    audit_factor_formula(
        channel,
        profile_ids,
        alpha,
        factor_index,
        options,
        constant,
    )
    direct_small_audit(options, constant)
    left = enumerate_sums(left_options)
    right = enumerate_sums(right_options)
    if len(left) != 3**left_weight or len(right) != 3**right_weight:
        raise AssertionError("half enumeration lost an assignment")

    zero_count = count_zero_sums(left, right, constant)
    elapsed = time.monotonic() - started
    peak_rss_bytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    certificate = {
        "label": label,
        "channel": "AB"[channel],
        "primitive_factor": factor_index,
        "profile_ids": list(profile_ids),
        "physical_profile_counts": [
            list(
                actual_profile_counts(
                    channel,
                    class_index,
                    PROFILES[profile_id],
                )
            )
            for class_index, profile_id in enumerate(profile_ids)
        ],
        "active_trits": active,
        "half_trits": [left_weight, right_weight],
        "half_assignments": [len(left), len(right)],
        "primitive_zero_assignments": zero_count,
        "direct_crt_formula_checked": True,
        "direct_prefix_mitm_checked": True,
    }
    certificate["semantic_sha256"] = sha256(
        json.dumps(
            certificate,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("ascii")
    ).hexdigest()
    certificate["elapsed_seconds"] = round(elapsed, 3)
    certificate["peak_rss_bytes"] = peak_rss_bytes
    return certificate


def load_profiles(scope: str) -> tuple[dict[str, object], ...]:
    result: list[dict[str, object]] = []
    if scope in ("h2", "h2_astar", "all"):
        path = SEARCH_ROOT / "shell_two_exact" / "shell_two_exact_orbits_certificate.json"
        data = json.loads(path.read_text())
        for record in data["orbits"]:
            if scope == "h2_astar":
                profile_to_id = {
                    tuple(profile): index
                    for index, profile in enumerate(PROFILES)
                }
                conjugate_id = tuple(
                    profile_to_id[(profile[0], profile[2], profile[1])]
                    for profile in PROFILES
                )
                identifiers_a = tuple(
                    conjugate_id[
                        int(record["profile_ids_a"][(index + 6) % 12])
                    ]
                    for index in range(12)
                )
                result.append(
                    {
                        **record,
                        "label": f"{record['label']}-Astar",
                        "profile_ids_a": identifiers_a,
                    }
                )
            else:
                result.append(record)
    if scope in ("h0", "all"):
        path = (
            SEARCH_ROOT
            / "dense_shell_h0_complete_classification"
            / "certificate.json"
        )
        data = json.loads(path.read_text())
        for record in data["profiles"]:
            result.append(record)
    return tuple(result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scope",
        choices=("h2", "h2_astar", "h0", "all"),
        default="h2",
    )
    parser.add_argument("--label", action="append", default=[])
    parser.add_argument("--channel", choices=("A", "B", "both"), default="both")
    parser.add_argument(
        "--factor",
        action="append",
        type=int,
        choices=range(6),
        help="primitive factor index; defaults to the three independent plus factors 0,1,2",
    )
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    alpha = phase167.ninth_root_of_unity()
    records = load_profiles(args.scope)
    if args.label:
        labels = set(args.label)
        records = tuple(record for record in records if record["label"] in labels)
        missing = labels - {str(record["label"]) for record in records}
        if missing:
            raise SystemExit(f"unknown labels: {sorted(missing)}")
    channels = (0, 1) if args.channel == "both" else ("AB".index(args.channel),)
    factors = tuple(args.factor) if args.factor else (0, 1, 2)

    certificates = []
    for record in records:
        for channel in channels:
            for factor_index in factors:
                certificate = audit_channel(
                    str(record["label"]),
                    channel,
                    tuple(
                        int(value)
                        for value in record[f"profile_ids_{'ab'[channel]}"]
                    ),
                    alpha,
                    factor_index,
                )
                certificates.append(certificate)
                print(json.dumps(certificate, sort_keys=True), flush=True)

    semantic = tuple(
        {
            key: value
            for key, value in certificate.items()
            if key not in ("elapsed_seconds", "peak_rss_bytes")
        }
        for certificate in certificates
    )
    summary = {
        "schema": "lp333-prime167-primitive-degenerate-mitm-v2",
        "scope": args.scope,
        "profiles": len({entry["label"] for entry in certificates}),
        "channel_factor_audits": len(certificates),
        "total_primitive_zero_assignments": sum(
            int(entry["primitive_zero_assignments"]) for entry in certificates
        ),
        "semantic_sha256": sha256(
            json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode("ascii")
        ).hexdigest(),
        "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    if args.output is not None:
        payload = {
            "summary": {
                key: value
                for key, value in summary.items()
                if key != "peak_rss_bytes"
            },
            "audits": semantic,
        }
        args.output.write_text(
            json.dumps(payload, sort_keys=True, indent=2) + "\n"
        )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
