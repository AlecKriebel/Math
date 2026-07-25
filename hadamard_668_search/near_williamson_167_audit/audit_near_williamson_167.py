#!/usr/bin/env python3
"""Exact arithmetic audit of near-Williamson matrices at order 167.

The default run uses only Python integer arithmetic.  The optional PSD pilot
imports NumPy lazily and is deliberately single-process and bounded.
"""

from __future__ import annotations

import argparse
import random
from collections import Counter
from itertools import product
from math import comb, isqrt, log10
from typing import Iterable, Sequence


ORDER = 167
HALF = (ORDER - 1) // 2
TARGET = 4 * ORDER


def half_index(index: int, n: int = ORDER) -> int:
    """Return the representative in {0,...,(n-1)/2} of {index,-index}."""

    residue = index % n
    return min(residue, (-residue) % n)


def periodic_autocorrelation(row: Sequence[int], lag: int) -> int:
    """Exact periodic autocorrelation at ``lag``."""

    n = len(row)
    return sum(row[j] * row[(j + lag) % n] for j in range(n))


def row_sum_profiles(n: int = ORDER) -> tuple[tuple[int, int, int, int], ...]:
    """Canonical normalized near-Williamson row-sum profiles.

    A is distinguished.  The three symmetric rows B,C,D have their signs
    forced by normalization, and are ordered by decreasing absolute row sum.
    """

    bound = isqrt(4 * n)
    odd_values = range(-bound, bound + 1, 2)
    return tuple(
        (a, b, c, d)
        for a, b, c, d in product(odd_values, repeat=4)
        if a * a + b * b + c * c + d * d == 4 * n
        and b % 4 == n % 4
        and c % 4 == n % 4
        and d % 4 == n % 4
        and abs(b) >= abs(c) >= abs(d)
    )


def one_defect_profiles(
    n: int = ORDER,
) -> tuple[tuple[int, int, int, int], ...]:
    """Profiles in which normalized almost-symmetric A is nonsymmetric."""

    # With A[0]=1, A[1]=-A[-1], and the other pairs symmetric,
    # sum(A)=n-2 (mod 4).  For n=167 this is 1 (mod 4).
    return tuple(profile for profile in row_sum_profiles(n) if profile[0] % 4 == (n - 2) % 4)


def symmetric_a_profiles(
    n: int = ORDER,
) -> tuple[tuple[int, int, int, int], ...]:
    """Profiles in which the paper's almost-symmetric A is fully symmetric."""

    return tuple(profile for profile in row_sum_profiles(n) if profile[0] % 4 == n % 4)


def one_defect_core_weight(row_sum: int, n: int = ORDER) -> int:
    """Negative symmetric pairs in A outside its exceptional pair."""

    numerator = n - 2 - row_sum
    if numerator % 4:
        raise ValueError("row sum is incompatible with a normalized one-defect row")
    weight = numerator // 4
    if not 0 <= weight <= (n - 3) // 2:
        raise ValueError("one-defect core weight is out of range")
    return weight


def symmetric_half_weight(row_sum: int, n: int = ORDER) -> int:
    """Negative pairs in a normalized symmetric row."""

    numerator = n - row_sum
    if numerator % 4:
        raise ValueError("row sum is incompatible with a normalized symmetric row")
    weight = numerator // 4
    if not 0 <= weight <= (n - 1) // 2:
        raise ValueError("symmetric half weight is out of range")
    return weight


def unrestricted_a_count(row_sum: int, n: int = ORDER) -> int:
    """Normalized circulant A rows of a prescribed row sum."""

    plus_after_origin = (row_sum + n - 2) // 2
    if 2 * plus_after_origin != row_sum + n - 2:
        return 0
    return comb(n - 1, plus_after_origin)


def symmetric_row_count(row_sum: int, n: int = ORDER) -> int:
    """Normalized symmetric rows of a prescribed row sum."""

    return comb((n - 1) // 2, symmetric_half_weight(row_sum, n))


def one_defect_ab_gauge_count(
    profile: tuple[int, int, int, int], n: int = ORDER
) -> int:
    """Gauge-fixed (A,B) inputs for the genuine one-defect family.

    A common multiplier puts the exceptional pair of A at {+1,-1}; the
    residual multiplier -1 identifies its two orientations.  No multiplier
    freedom remains to quotient B.  The count is therefore

        C((n-3)/2, h_A) C((n-1)/2, h_B).
    """

    a, b, _c, _d = profile
    return comb((n - 3) // 2, one_defect_core_weight(a, n)) * symmetric_row_count(
        b, n
    )


def unique_ab_workload(
    profiles: Iterable[tuple[int, int, int, int]],
    count,
) -> int:
    """Sum a candidate-count function once per distinct (a,b) shard."""

    representatives = {}
    for profile in profiles:
        representatives.setdefault(profile[:2], profile)
    return sum(count(profile) for profile in representatives.values())


def negative_support_bits(row: Sequence[int]) -> tuple[int, ...]:
    return tuple(int(value == -1) for value in row)


def generic_cd_xor_from_ab(
    a_row: Sequence[int], b_row: Sequence[int]
) -> tuple[int, ...]:
    """The paper's mod-8 relation, made explicit for every half-index.

    The returned bit e[t] says D[t] = (-1)^e[t] C[t].  It is determined
    before either C or D is searched.
    """

    n = len(a_row)
    half = (n - 1) // 2
    result = [0]
    for t in range(1, half + 1):
        numerator = (
            periodic_autocorrelation(a_row, 2 * t)
            + periodic_autocorrelation(b_row, 2 * t)
            + 2 * n
        )
        if numerator % 4:
            raise AssertionError("autocorrelation parity invariant failed")
        result.append((numerator // 4) & 1)
    return tuple(result)


def modified_product_xor(
    core_bits: Sequence[int],
    b_bits: Sequence[int],
    delta: int,
    n: int,
) -> tuple[int, ...]:
    """Closed form of the C/D relation for a one-defect A.

    ``delta`` is the index of the unique negative entry in the exceptional
    pair.  ``core_bits`` is symmetric, with zero at 0 and at the exceptional
    pair.  For t=1,...,(n-1)/2,

      C_t xor D_t =
          B_t xor X_t xor X_{2t-delta} xor X_{2t+delta}.
    """

    half = (n - 1) // 2
    return (0,) + tuple(
        b_bits[t]
        ^ core_bits[t]
        ^ core_bits[half_index(2 * t - delta, n)]
        ^ core_bits[half_index(2 * t + delta, n)]
        for t in range(1, half + 1)
    )


def build_one_defect_row(
    n: int,
    delta: int,
    negative_core_pairs: Iterable[int],
) -> tuple[int, ...]:
    """Build normalized A with one antisymmetric pair."""

    row = [1] * n
    row[delta % n] = -1
    row[-delta % n] = 1
    for index in negative_core_pairs:
        if half_index(index, n) in (0, half_index(delta, n)):
            raise ValueError("core overlaps the origin or exceptional pair")
        row[index % n] = -1
        row[-index % n] = -1
    return tuple(row)


def build_symmetric_row(n: int, negative_pairs: Iterable[int]) -> tuple[int, ...]:
    row = [1] * n
    for index in negative_pairs:
        if half_index(index, n) == 0:
            raise ValueError("symmetric negative pair cannot contain the origin")
        row[index % n] = -1
        row[-index % n] = -1
    return tuple(row)


def assert_modified_product_law() -> None:
    """Exhaustive small checks and deterministic order-167 checks."""

    rng = random.Random(0x668)
    for n in (7, 11):
        half = (n - 1) // 2
        for delta in (1, -1):
            exceptional = half_index(delta, n)
            core_indices = tuple(i for i in range(1, half + 1) if i != exceptional)
            for core_mask in range(1 << len(core_indices)):
                negative_core = {
                    index
                    for bit, index in enumerate(core_indices)
                    if core_mask >> bit & 1
                }
                a_row = build_one_defect_row(n, delta, negative_core)
                core_bits = [0] * (half + 1)
                for index in negative_core:
                    core_bits[index] = 1
                for b_mask in range(1 << half):
                    negative_b = {
                        index for index in range(1, half + 1) if b_mask >> (index - 1) & 1
                    }
                    b_row = build_symmetric_row(n, negative_b)
                    b_bits = (0,) + tuple(
                        int(index in negative_b) for index in range(1, half + 1)
                    )
                    assert generic_cd_xor_from_ab(
                        a_row, b_row
                    ) == modified_product_xor(core_bits, b_bits, delta, n)

    # A few larger tests ensure that the prime-167 indexing is exercised.
    for delta in (1, -1):
        for _ in range(8):
            negative_core = set(rng.sample(range(2, HALF + 1), rng.randrange(HALF)))
            negative_b = set(rng.sample(range(1, HALF + 1), rng.randrange(HALF + 1)))
            a_row = build_one_defect_row(ORDER, delta, negative_core)
            b_row = build_symmetric_row(ORDER, negative_b)
            core_bits = (0, 0) + tuple(
                int(index in negative_core) for index in range(2, HALF + 1)
            )
            b_bits = (0,) + tuple(
                int(index in negative_b) for index in range(1, HALF + 1)
            )
            assert generic_cd_xor_from_ab(
                a_row, b_row
            ) == modified_product_xor(core_bits, b_bits, delta, ORDER)


def c_d_weight_gate(
    xor_bits: Sequence[int], c_row_sum: int, d_row_sum: int, n: int = ORDER
) -> bool:
    """Exact feasibility of the two prescribed symmetric row sums."""

    e_weight = sum(xor_bits[1:])
    c_weight = symmetric_half_weight(c_row_sum, n)
    d_weight = symmetric_half_weight(d_row_sum, n)
    numerator = c_weight + e_weight - d_weight
    if numerator % 2:
        return False
    intersection = numerator // 2
    return (
        0 <= intersection <= min(c_weight, e_weight)
        and 0 <= c_weight - intersection <= (n - 1) // 2 - e_weight
    )


def reduced_c_system(
    a_row: Sequence[int],
    b_row: Sequence[int],
    xor_bits: Sequence[int],
) -> tuple[tuple[int, int], ...]:
    """Return the paper's second linearization as a GF(2) system.

    Each pair is ``(coefficient_mask, right_hand_side_bit)`` in the negative
    half-support bits of C.  Satisfying this system is necessary; the original
    integer autocorrelations must still be checked afterward.
    """

    n = len(a_row)
    half = (n - 1) // 2
    inverse_two = pow(2, -1, n)
    equations = []

    for lag in range(1, half + 1):
        # Reflection j -> -j-lag pairs all directed autocorrelation edges
        # except the fixed edge from -lag/2 to lag/2.  That edge contributes
        # exactly 2 to P_C(lag)+P_D(lag).
        fixed = (-lag * inverse_two) % n
        seen = set()
        eligible_orbits = 0
        coefficient_mask = 0
        for start in range(n):
            if start == fixed or start in seen:
                continue
            reflected_start = (-start - lag) % n
            seen.add(start)
            seen.add(reflected_start)
            end = (start + lag) % n
            left = half_index(start, n)
            right = half_index(end, n)
            if xor_bits[left] != xor_bits[right]:
                continue
            eligible_orbits += 1
            if left:
                coefficient_mask ^= 1 << (left - 1)
            if right:
                coefficient_mask ^= 1 << (right - 1)

        required = (
            -periodic_autocorrelation(a_row, lag)
            - periodic_autocorrelation(b_row, lag)
            - 2
        )
        if required % 4:
            raise AssertionError("fixed-edge divisibility invariant failed")
        required //= 4
        if (eligible_orbits - required) % 2:
            raise AssertionError("second linearization parity invariant failed")
        right_hand_side = ((eligible_orbits - required) // 2) & 1
        equations.append((coefficient_mask, right_hand_side))

    return tuple(equations)


def gf2_rank_and_consistency(
    equations: Iterable[tuple[int, int]],
) -> tuple[int, bool]:
    """Exact row reduction of a bit-packed GF(2) system."""

    pivots: dict[int, tuple[int, int]] = {}
    consistent = True
    for coefficient_mask, right_hand_side in equations:
        while coefficient_mask:
            pivot = coefficient_mask.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (coefficient_mask, right_hand_side)
                break
            old_mask, old_rhs = pivots[pivot]
            coefficient_mask ^= old_mask
            right_hand_side ^= old_rhs
        else:
            if right_hand_side:
                consistent = False
    return len(pivots), consistent


def assert_second_linearization() -> None:
    """Regression on an exact genuinely near-Williamson order-7 quadruple."""

    a_row = (1, 1, 1, 1, 1, 1, -1)
    b_row = (1, 1, -1, -1, -1, -1, 1)
    c_row = (1, -1, 1, -1, -1, 1, -1)
    d_row = (1, -1, -1, 1, 1, -1, -1)
    assert all(
        sum(
            periodic_autocorrelation(row, lag)
            for row in (a_row, b_row, c_row, d_row)
        )
        == 0
        for lag in range(1, 4)
    )
    xor_bits = generic_cd_xor_from_ab(a_row, b_row)
    assert xor_bits == (0,) + tuple(
        int(c_row[index] != d_row[index]) for index in range(1, 4)
    )
    equations = reduced_c_system(a_row, b_row, xor_bits)
    assignment = sum(
        int(c_row[index] == -1) << (index - 1) for index in range(1, 4)
    )
    assert all(
        ((coefficient_mask & assignment).bit_count() & 1) == right_hand_side
        for coefficient_mask, right_hand_side in equations
    )
    assert gf2_rank_and_consistency(equations) == (2, True)


def exact_linear_pilot(samples_per_profile: int, seed: int) -> None:
    """Bounded exact rank/consistency pilot for the second linearization."""

    if samples_per_profile <= 0:
        return
    rng = random.Random(seed)
    ranks: Counter[int] = Counter()
    totals: Counter[str] = Counter()
    for a, b, c, d in one_defect_profiles():
        h_a = one_defect_core_weight(a)
        h_b = symmetric_half_weight(b)
        for _ in range(samples_per_profile):
            negative_core = set(rng.sample(range(2, HALF + 1), h_a))
            negative_b = set(rng.sample(range(1, HALF + 1), h_b))
            a_row = build_one_defect_row(ORDER, 1, negative_core)
            b_row = build_symmetric_row(ORDER, negative_b)
            core_bits = (0, 0) + tuple(
                int(index in negative_core) for index in range(2, HALF + 1)
            )
            b_bits = (0,) + tuple(
                int(index in negative_b) for index in range(1, HALF + 1)
            )
            xor_bits = modified_product_xor(core_bits, b_bits, 1, ORDER)
            rank, consistent = gf2_rank_and_consistency(
                reduced_c_system(a_row, b_row, xor_bits)
            )
            totals["sample"] += 1
            totals["nonzero_xor"] += any(xor_bits)
            totals["weight_gate"] += c_d_weight_gate(xor_bits, c, d)
            totals["consistent"] += consistent
            ranks[rank] += 1

    print("second_linearization_exact_pilot_not_exhaustive")
    print(f"  sample={totals['sample']}")
    print(f"  nonzero_CD_xor={totals['nonzero_xor']}")
    print(f"  CD_weight_gate={totals['weight_gate']}")
    print(f"  consistent={totals['consistent']}")
    print(
        "  rank_histogram="
        + ",".join(f"{rank}:{count}" for rank, count in sorted(ranks.items()))
    )


def psd_pilot(samples_per_profile: int, seed: int) -> None:
    """Small numerical pilot; this is not a proof or a search for a matrix."""

    if samples_per_profile <= 0:
        return
    try:
        import numpy as np
    except ModuleNotFoundError as error:
        raise SystemExit(
            "The optional PSD pilot needs NumPy; run it in the repository's "
            "Hadamard Python environment."
        ) from error

    rng = random.Random(seed)
    totals: Counter[str] = Counter()
    limit = TARGET + 1e-7

    for a, b, c, d in one_defect_profiles():
        h_a = one_defect_core_weight(a)
        h_b = symmetric_half_weight(b)
        for _ in range(samples_per_profile):
            negative_core = set(rng.sample(range(2, HALF + 1), h_a))
            negative_b = set(rng.sample(range(1, HALF + 1), h_b))
            a_row = build_one_defect_row(ORDER, 1, negative_core)
            b_row = build_symmetric_row(ORDER, negative_b)
            psd_a = abs(np.fft.fft(a_row)) ** 2
            psd_b = abs(np.fft.fft(b_row)) ** 2
            a_ok = float(max(psd_a[1 : HALF + 1])) <= limit
            b_ok = float(max(psd_b[1 : HALF + 1])) <= limit
            ab_ok = float(max(psd_a[1 : HALF + 1] + psd_b[1 : HALF + 1])) <= limit

            core_bits = (0, 0) + tuple(
                int(index in negative_core) for index in range(2, HALF + 1)
            )
            b_bits = (0,) + tuple(
                int(index in negative_b) for index in range(1, HALF + 1)
            )
            xor_bits = modified_product_xor(core_bits, b_bits, 1, ORDER)
            totals["sample"] += 1
            totals["A_PSD"] += a_ok
            totals["B_PSD"] += b_ok
            totals["A_and_B_PSD"] += a_ok and b_ok
            totals["AB_sum_PSD"] += ab_ok
            totals["CD_weight_gate"] += c_d_weight_gate(xor_bits, c, d)

    print("PSD_pilot_numerical_not_proof")
    for key in (
        "sample",
        "A_PSD",
        "B_PSD",
        "A_and_B_PSD",
        "AB_sum_PSD",
        "CD_weight_gate",
    ):
        print(f"  {key}={totals[key]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--samples-per-profile",
        type=int,
        default=0,
        help="run an optional bounded numerical PSD pilot",
    )
    parser.add_argument(
        "--rank-samples-per-profile",
        type=int,
        default=0,
        help="run an optional bounded exact linear-system pilot",
    )
    parser.add_argument("--seed", type=int, default=260724)
    args = parser.parse_args()

    profiles = row_sum_profiles()
    defect_profiles = one_defect_profiles()
    williamson_overlap = symmetric_a_profiles()
    assert len(profiles) == 68
    assert len(defect_profiles) == 34
    assert len(williamson_overlap) == 34
    assert set(defect_profiles).isdisjoint(williamson_overlap)
    assert set(defect_profiles) | set(williamson_overlap) == set(profiles)
    assert_modified_product_law()
    assert_second_linearization()

    unique_defect_pairs = unique_ab_workload(
        defect_profiles, one_defect_ab_gauge_count
    )
    assert (
        unique_defect_pairs
        == 5_389_321_893_816_717_644_217_498_408_040_941_405_747_563_982_000
    )

    def unrestricted_ab_count(profile: tuple[int, int, int, int]) -> int:
        a, b, _c, _d = profile
        return unrestricted_a_count(a) * symmetric_row_count(b)

    unrestricted_pairs = unique_ab_workload(profiles, unrestricted_ab_count)

    print(f"order={ORDER}")
    print(f"near_row_sum_profiles={len(profiles)}")
    print(f"almost_symmetric_A_Williamson_overlap={len(williamson_overlap)}")
    print(f"almost_symmetric_A_genuine_one_defect={len(defect_profiles)}")
    print(f"one_defect_unique_AB_shards={len(set(p[:2] for p in defect_profiles))}")
    print(f"one_defect_gauge_fixed_AB_inputs={unique_defect_pairs}")
    print(f"one_defect_gauge_fixed_AB_log10={log10(unique_defect_pairs):.6f}")
    print(f"unrestricted_normalized_AB_inputs={unrestricted_pairs}")
    print(f"unrestricted_normalized_AB_log10={log10(unrestricted_pairs):.6f}")
    print("modified_product_law_regression=PASS")
    print("second_linearization_regression=PASS")
    exact_linear_pilot(args.rank_samples_per_profile, args.seed)
    psd_pilot(args.samples_per_profile, args.seed)


if __name__ == "__main__":
    main()
