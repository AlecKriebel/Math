#!/usr/bin/env python3
"""Exact physical-margin plus characteristic-37 T1/T2 convolution audit.

For a fixed physical row-margin target, all six sequence augmentations A_0
are fixed exactly.  The first two nonconstant coefficients of one sequence's
diagonal norm are then additive summaries

    t1 = A_1 conjugate(A_0) - A_0 conjugate(A_1) in F_37,
    t2 = A_2 conjugate(A_0) + A_0 conjugate(A_2)
         - A_1 conjugate(A_1)                    in F_37.

This script enumerates each one-sequence phase alphabet once, conditions on
its exact physical augmentation, and records a dense 37 x 37 distribution
of (t1,t2).  Six such distributions are convolved exactly over F_37^2.

The convolution uses five independent prime moduli containing 37th roots of
unity, followed by integer CRT.  Their product exceeds 3^54, so the recovered
count is the unique exact nonnegative count.  This is not a stochastic search
and no timeout status is interpreted as mathematics.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import sys
import time
from typing import Sequence

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
if str(SEARCH_ROOT) not in sys.path:
    sys.path.insert(0, str(SEARCH_ROOT))

from verify_lp333_order3_char37_transfer import (  # noqa: E402
    P,
    TRANSFER_FACTORS,
    e_conjugate,
    e_multiply,
    e_reduce,
)
from verify_lp333_order3_diagonal_frame_prefix import (  # noqa: E402
    ROOTS,
    SequenceSignature,
    decode_signature,
    sequence_signature,
)
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    catalog_phase_sum_intersection,
)


if P != 37:
    raise AssertionError("this audit requires the characteristic-37 transfer")

RAW_PHASE_SPACE = 3**54
NTT_DATA = (
    (1_000_037, 2),
    (1_000_333, 5),
    (1_000_777, 5),
    (1_000_999, 6),
    (1_001_369, 3),
)
NTT_PRODUCT = int(np.prod(np.asarray([item[0] for item in NTT_DATA], dtype=object)))
if NTT_PRODUCT <= RAW_PHASE_SPACE:
    raise AssertionError("the CRT modulus no longer determines the exact count")


Eisenstein = tuple[int, int]
MarginTarget = tuple[
    tuple[Eisenstein, Eisenstein, Eisenstein],
    tuple[Eisenstein, Eisenstein, Eisenstein],
]


def e_add_mod(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return (left[0] + right[0]) % P, (left[1] + right[1]) % P


def e_sub_mod(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return (left[0] - right[0]) % P, (left[1] - right[1]) % P


def norm_coefficients(
    exact_sum: Eisenstein,
    first: Eisenstein,
    second: Eisenstein,
) -> tuple[int, int]:
    """Return the scalar T1 and T2 contributions of one sequence."""

    constant = e_reduce(exact_sum)
    first_value = e_sub_mod(
        e_multiply(first, e_conjugate(constant)),
        e_multiply(constant, e_conjugate(first)),
    )
    if (first_value[1] - 2 * first_value[0]) % P:
        raise AssertionError("T1 left the anti-self-conjugate line")

    second_value = e_sub_mod(
        e_add_mod(
            e_multiply(second, e_conjugate(constant)),
            e_multiply(constant, e_conjugate(second)),
        ),
        e_multiply(first, e_conjugate(first)),
    )
    if second_value[1] % P:
        raise AssertionError("T2 left the self-conjugate line")
    return first_value[0] % P, second_value[0] % P


@lru_cache(maxsize=None)
def conditioned_t12(
    signature: SequenceSignature,
) -> tuple[tuple[Eisenstein, tuple[tuple[tuple[int, int], int], ...]], ...]:
    """Map each exact augmentation to its dense-summary sparse support."""

    zero, active = decode_signature(signature)
    by_sum: defaultdict[Eisenstein, Counter[tuple[int, int]]] = defaultdict(Counter)

    def visit(
        position: int,
        sum_real: int,
        sum_omega: int,
        first_real: int,
        first_omega: int,
        second_real: int,
        second_omega: int,
    ) -> None:
        if position == len(active):
            exact_sum = sum_real, sum_omega
            t12 = norm_coefficients(
                exact_sum,
                (first_real, first_omega),
                (second_real, second_omega),
            )
            by_sum[exact_sum][t12] += 1
            return

        class_index, sign = active[position]
        first_scale = (
            TRANSFER_FACTORS[1]
            * pow(8, class_index, P)
            * sign
        ) % P
        second_scale = (
            TRANSFER_FACTORS[2]
            * pow(8, 2 * class_index, P)
            * sign
        ) % P
        for root in ROOTS:
            visit(
                position + 1,
                sum_real + 3 * sign * root[0],
                sum_omega + 3 * sign * root[1],
                (first_real + first_scale * root[0]) % P,
                (first_omega + first_scale * root[1]) % P,
                (second_real + second_scale * root[0]) % P,
                (second_omega + second_scale * root[1]) % P,
            )

    visit(0, zero[0], zero[1], 0, 0, 0, 0)
    expected = 3 ** len(active)
    actual = sum(
        count
        for distribution in by_sum.values()
        for count in distribution.values()
    )
    if actual != expected:
        raise AssertionError("one-sequence enumeration lost multiplicity")
    return tuple(
        (
            exact_sum,
            tuple(sorted(distribution.items())),
        )
        for exact_sum, distribution in sorted(by_sum.items())
    )


def conditioned_lookup(
    signature: SequenceSignature,
    exact_sum: Eisenstein,
) -> dict[tuple[int, int], int]:
    for candidate, distribution in conditioned_t12(signature):
        if candidate == exact_sum:
            return dict(distribution)
    return {}


@lru_cache(maxsize=None)
def transform_matrix(modulus: int, primitive_root: int) -> np.ndarray:
    root = pow(primitive_root, (modulus - 1) // P, modulus)
    if pow(root, P, modulus) != 1 or root == 1:
        raise AssertionError("the NTT root does not have order 37")
    return np.asarray(
        [
            [pow(root, frequency * value, modulus) for value in range(P)]
            for frequency in range(P)
        ],
        dtype=np.uint64,
    )


@lru_cache(maxsize=None)
def transformed_distribution(
    signature: SequenceSignature,
    exact_sum: Eisenstein,
    modulus: int,
    primitive_root: int,
) -> np.ndarray:
    distribution = conditioned_lookup(signature, exact_sum)
    values = np.zeros((P, P), dtype=np.uint64)
    for (first, second), count in distribution.items():
        values[first, second] = count % modulus
    matrix = transform_matrix(modulus, primitive_root)
    # Every inner sum is < 37*modulus^2 < 2^64 for the pinned moduli.
    first_axis = (matrix @ values) % modulus
    return (first_axis @ matrix.T) % modulus


def convolution_zero_mod(
    signatures: Sequence[SequenceSignature],
    target: MarginTarget,
    modulus: int,
    primitive_root: int,
) -> int:
    transforms = []
    for index, signature in enumerate(signatures):
        channel, residue = divmod(index, 3)
        transforms.append(
            transformed_distribution(
                signature,
                target[channel][residue],
                modulus,
                primitive_root,
            )
        )
    product = np.ones((P, P), dtype=np.uint64)
    for transform in transforms:
        product = (product * transform) % modulus
    inverse_size = pow(P * P, -1, modulus)
    return int(int(np.sum(product, dtype=np.uint64)) % modulus * inverse_size % modulus)


def crt_reconstruct(residues: Sequence[int]) -> int:
    if len(residues) != len(NTT_DATA):
        raise ValueError("the CRT residue vector has the wrong length")
    value = 0
    modulus_product = 1
    for residue, (modulus, _) in zip(residues, NTT_DATA):
        correction = (
            (int(residue) - value)
            * pow(modulus_product % modulus, -1, modulus)
        ) % modulus
        value += modulus_product * correction
        modulus_product *= modulus
    if not 0 <= value < modulus_product:
        raise AssertionError("CRT reconstruction left its range")
    if any(value % modulus != residue for residue, (modulus, _) in zip(residues, NTT_DATA)):
        raise AssertionError("CRT reconstruction failed replay")
    if value > RAW_PHASE_SPACE:
        raise AssertionError("the reconstructed count exceeds 3^54")
    return value


def exact_convolution_zero(
    signatures: Sequence[SequenceSignature],
    target: MarginTarget,
) -> int:
    residues = tuple(
        convolution_zero_mod(
            signatures,
            target,
            modulus,
            primitive_root,
        )
        for modulus, primitive_root in NTT_DATA
    )
    return crt_reconstruct(residues)


def audit_ntt() -> None:
    """Check every modular transform against a direct tiny convolution."""

    left = {(0, 0): 2, (1, 3): 5, (36, 7): 11}
    right = {(0, 0): 13, (2, 4): 17, (5, 30): 19}
    direct = sum(
        a_count * b_count
        for (a0, a1), a_count in left.items()
        for (b0, b1), b_count in right.items()
        if (a0 + b0) % P == 0 and (a1 + b1) % P == 0
    )
    for modulus, primitive_root in NTT_DATA:
        matrix = transform_matrix(modulus, primitive_root)
        arrays = []
        for distribution in (left, right):
            values = np.zeros((P, P), dtype=np.uint64)
            for key, count in distribution.items():
                values[key] = count % modulus
            arrays.append(((matrix @ values) % modulus @ matrix.T) % modulus)
        product = arrays[0] * arrays[1] % modulus
        recovered = (
            int(np.sum(product, dtype=np.uint64))
            * pow(P * P, -1, modulus)
        ) % modulus
        if recovered != direct % modulus:
            raise AssertionError("the 2D NTT convolution disagrees with direct replay")


def normalize_target(value: object) -> MarginTarget:
    nested = tuple(
        tuple((int(pair[0]), int(pair[1])) for pair in channel)
        for channel in value  # type: ignore[union-attr]
    )
    if len(nested) != 2 or any(len(channel) != 3 for channel in nested):
        raise ValueError("invalid six-sum margin target")
    return nested  # type: ignore[return-value]


def audit_profile(record: dict[str, object]) -> dict[str, object]:
    label = str(record["label"])
    identifiers_a = tuple(int(value) for value in record["profile_ids_a"])  # type: ignore[arg-type]
    identifiers_b = tuple(int(value) for value in record["profile_ids_b"])  # type: ignore[arg-type]
    signatures = tuple(
        sequence_signature(channel, residue, identifiers)
        for channel, identifiers in enumerate((identifiers_a, identifiers_b))
        for residue in range(3)
    )
    catalog = catalog_phase_sum_intersection(identifiers_a, identifiers_b)
    target_records = []
    for target_index, (raw_target, multiplicity) in enumerate(
        catalog["phase_sum_corpus"]
    ):
        target = normalize_target(raw_target)
        marginal_counts = tuple(
            sum(conditioned_lookup(signature, target[index // 3][index % 3]).values())
            for index, signature in enumerate(signatures)
        )
        reconstructed_multiplicity = int(np.prod(np.asarray(marginal_counts, dtype=object)))
        if reconstructed_multiplicity != int(multiplicity):
            raise AssertionError("the six conditioned sequence counts lost the margin multiplicity")
        survivors = exact_convolution_zero(signatures, target)
        if survivors > int(multiplicity):
            raise AssertionError("T1/T2 survivors exceed the physical-margin population")
        target_records.append(
            {
                "target_index": target_index,
                "target": target,
                "margin_assignments": int(multiplicity),
                "t1_t2_survivors": survivors,
            }
        )
    return {
        "label": label,
        "targets": len(target_records),
        "targets_excluded": sum(
            int(record["t1_t2_survivors"]) == 0 for record in target_records
        ),
        "minimum_survivors": min(
            int(record["t1_t2_survivors"]) for record in target_records
        ),
        "maximum_survivors": max(
            int(record["t1_t2_survivors"]) for record in target_records
        ),
        "total_margin_assignments": sum(
            int(record["margin_assignments"]) for record in target_records
        ),
        "total_t1_t2_survivors": sum(
            int(record["t1_t2_survivors"]) for record in target_records
        ),
        "target_records": target_records,
    }


def compact_hash(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", action="append", default=[])
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audit_ntt()
    certificate_path = (
        SEARCH_ROOT
        / "shell_two_exact"
        / "shell_two_exact_orbits_certificate.json"
    )
    records = json.loads(certificate_path.read_text())["orbits"]
    if args.label:
        labels = set(args.label)
        records = [record for record in records if record["label"] in labels]
        missing = labels - {str(record["label"]) for record in records}
        if missing:
            raise SystemExit(f"unknown labels: {sorted(missing)}")

    started = time.monotonic()
    profiles = []
    for record in records:
        result = audit_profile(record)
        profiles.append(result)
        print(
            json.dumps(
                {
                    key: value
                    for key, value in result.items()
                    if key != "target_records"
                },
                sort_keys=True,
            ),
            flush=True,
        )
    semantic = {
        "schema": "lp333-shell-two-margin-t1-t2-v1",
        "ntt_moduli": [modulus for modulus, _ in NTT_DATA],
        "crt_modulus": NTT_PRODUCT,
        "raw_phase_bound": RAW_PHASE_SPACE,
        "profiles": profiles,
    }
    summary = {
        "profiles": len(profiles),
        "targets": sum(int(profile["targets"]) for profile in profiles),
        "targets_excluded": sum(
            int(profile["targets_excluded"]) for profile in profiles
        ),
        "total_margin_assignments": sum(
            int(profile["total_margin_assignments"]) for profile in profiles
        ),
        "total_t1_t2_survivors": sum(
            int(profile["total_t1_t2_survivors"]) for profile in profiles
        ),
        "semantic_sha256": compact_hash(semantic),
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    if args.output is not None:
        args.output.write_text(
            json.dumps(
                {
                    "summary": {
                        key: value
                        for key, value in summary.items()
                        if key != "elapsed_seconds"
                    },
                    "certificate": semantic,
                },
                sort_keys=True,
                indent=2,
            )
            + "\n"
        )
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
