#!/usr/bin/env python3
"""Independent exact replay of the maximal 3^15 x 3^15 zero-sum case.

The main audit sorts the full 36-byte F_167 coordinate keys.  This replay
uses a different necessary representation: a pinned linear hash into
Z/(2^64).  Exact key equality implies hash equality.  Therefore disjoint
left and target hash sets prove that the full exact sets are disjoint,
without any probabilistic assumption about hash collisions.

The pinned instance is h2-422220-1, channel A, primitive factor zero.  It is
the unique 30-trit channel among the five canonical shell-two profiles.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import sys
import time

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
if str(SEARCH_ROOT) not in sys.path:
    sys.path.insert(0, str(SEARCH_ROOT))

from audit_primitive_degenerate import (  # noqa: E402
    COORDINATES,
    P,
    balanced_partition,
    class_options,
    enumerate_sums,
    l_to_u8,
    phase167,
    split,
    zero_column_value,
)


LABEL = "h2-422220-1"
CHANNEL = 0
FACTOR = 0
PROFILE_IDS = (2, 8, 8, 5, 5, 5, 2, 8, 8, 5, 5, 5)
MASK64 = (1 << 64) - 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def hash_coefficients() -> np.ndarray:
    """Pinned SplitMix64-derived nonzero coefficients."""

    state = 0x6A09E667F3BCC909
    result = []
    for _ in range(COORDINATES):
        state = (state + 0x9E3779B97F4A7C15) & MASK64
        value = state
        value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
        value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & MASK64
        value ^= value >> 31
        result.append(value or 1)
    return np.asarray(result, dtype=np.uint64)


def linear_hashes(
    values: np.ndarray,
    coefficients: np.ndarray,
    chunk_size: int = 250_000,
) -> np.ndarray:
    """Return sum_i coefficient_i*value_i modulo 2^64."""

    result = np.empty(len(values), dtype=np.uint64)
    for start in range(0, len(values), chunk_size):
        stop = min(start + chunk_size, len(values))
        # Unsigned NumPy arithmetic is exactly arithmetic modulo 2^64.
        result[start:stop] = (
            values[start:stop].astype(np.uint64, copy=False) @ coefficients
        )
    return result


def target_hashes(
    right: np.ndarray,
    constant: np.ndarray,
    coefficients: np.ndarray,
    chunk_size: int = 250_000,
) -> np.ndarray:
    result = np.empty(len(right), dtype=np.uint64)
    constant16 = constant.astype(np.uint16)
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
        result[start:stop] = target.astype(np.uint64) @ coefficients
    return result


def intersection_count(sorted_left: np.ndarray, right: np.ndarray) -> int:
    locations = np.searchsorted(sorted_left, right)
    valid = locations < len(sorted_left)
    return int(
        np.count_nonzero(
            valid
            & (
                sorted_left[
                    np.minimum(locations, len(sorted_left) - 1)
                ]
                == right
            )
        )
    )


def main() -> None:
    args = parse_args()
    started = time.monotonic()
    alpha = phase167.ninth_root_of_unity()
    options = class_options(PROFILE_IDS, alpha, FACTOR, CHANNEL)
    left_options, right_options = balanced_partition(options)
    left_weight = sum(item[0] for item in left_options)
    right_weight = sum(item[0] for item in right_options)
    if (left_weight, right_weight) != (15, 15):
        raise AssertionError("the maximal replay lost its balanced 15+15 split")
    left = enumerate_sums(left_options)
    right = enumerate_sums(right_options)
    constant = l_to_u8(zero_column_value(CHANNEL, alpha))
    coefficients = hash_coefficients()

    left_hash = linear_hashes(left, coefficients)
    target_hash = target_hashes(right, constant, coefficients)
    left_hash.sort()
    physical_hash_intersections = intersection_count(left_hash, target_hash)
    if physical_hash_intersections:
        raise AssertionError(
            "the necessary 64-bit hash filter did not certify disjointness"
        )

    # Positive control: make the first left/right pair solve the synthetic
    # target, then derive its target hash directly.  This checks sign and
    # search orientation independently of the physical constant.
    synthetic_constant = (
        P
        - (
            left[0].astype(np.uint16)
            + right[0].astype(np.uint16)
        )
        % P
    ) % P
    synthetic_target = (
        P
        - (
            right[:1].astype(np.uint16)
            + synthetic_constant.astype(np.uint16)
        )
        % P
    ) % P
    synthetic_hash = (
        synthetic_target.astype(np.uint64) @ coefficients
    ).reshape(-1)
    if intersection_count(left_hash, synthetic_hash) == 0:
        raise AssertionError("the positive hash-filter control failed")

    semantic = {
        "schema": "lp333-prime167-maximal-hash-replay-v1",
        "label": LABEL,
        "channel": "A",
        "primitive_factor": FACTOR,
        "profile_ids": PROFILE_IDS,
        "half_trits": (left_weight, right_weight),
        "half_assignments": (len(left), len(right)),
        "hash_ring": "Z/(2^64)",
        "hash_coefficients": tuple(int(value) for value in coefficients),
        "physical_hash_intersections": physical_hash_intersections,
        "positive_control": True,
    }
    semantic_hash = sha256(
        json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    result = {
        **semantic,
        "semantic_sha256": semantic_hash,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    if args.output is not None:
        args.output.write_text(
            json.dumps(
                {
                    key: value
                    for key, value in result.items()
                    if key not in ("elapsed_seconds", "peak_rss_bytes")
                },
                sort_keys=True,
                indent=2,
            )
            + "\n"
        )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
