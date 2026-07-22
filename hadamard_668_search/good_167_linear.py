#!/usr/bin/env python3
"""Two-stage GF(2) reducer for circulant good matrices of order 167.

Fix normalized skew ``A`` and normalized symmetric ``B``.  The good-matrix
product theorem forces ``D = S*C`` with

``S[0]=1`` and ``S[i]=-A[i]*A[2*i]*B[i]`` for nonzero ``i``.

For every lag, complementarity of ``C,D`` has a mod-four shadow that is a
sparse linear equation over GF(2) in the 83 independent signs of ``C``.  This
module solves those equations and then checks the few surviving vectors in the
original integer PAF equations.  The linear system is a necessary filter; only
the final exact check is a construction certificate.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
import random
import sys

from good_167 import (
    ORDER,
    is_skew,
    is_symmetric,
    periodic_autocorrelation,
    validate_good_quadruple,
)


@dataclass(frozen=True)
class LinearSystem:
    rows: tuple[tuple[int, int], ...]
    variables: int
    early_rejection: str | None = None


@dataclass(frozen=True)
class LinearSolution:
    rank: int
    inconsistent: bool
    particular: int = 0
    nullspace: tuple[int, ...] = ()


@dataclass(frozen=True)
class Recovery:
    system: LinearSystem
    solution: LinearSolution | None
    weight_survivors: int
    candidates: tuple[tuple[tuple[int, ...], ...], ...]


def symmetric_from_negative_mask(mask: int, n: int = ORDER) -> tuple[int, ...]:
    half = (n - 1) // 2
    signs = tuple(-1 if (mask >> index) & 1 else 1 for index in range(half))
    return (1, *signs, *reversed(signs))


def skew_from_negative_mask(mask: int, n: int = ORDER) -> tuple[int, ...]:
    half = (n - 1) // 2
    signs = tuple(-1 if (mask >> index) & 1 else 1 for index in range(half))
    return (1, *signs, *(-value for value in reversed(signs)))


def pair_variable(index: int, n: int) -> int | None:
    """Map a nonzero index to its ``{i,-i}`` half-variable number."""

    index %= n
    if index == 0:
        return None
    representative = min(index, n - index)
    return representative - 1


def derive_s(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    """Derive the symmetric quotient ``S=D/C`` from fixed ``A,B``."""

    if len(a) != len(b):
        raise ValueError("A and B must have equal length")
    if not is_skew(a):
        raise ValueError("A must be normalized skew")
    if not is_symmetric(b):
        raise ValueError("B must be normalized symmetric")
    n = len(a)
    s = (1,) + tuple(-a[index] * a[2 * index % n] * b[index] for index in range(1, n))
    if not is_symmetric(s):
        raise AssertionError("the product-theorem quotient should be symmetric")
    return s


def c_linear_system(
    a: tuple[int, ...], b: tuple[int, ...]
) -> tuple[LinearSystem, tuple[int, ...]]:
    """Build the exact mod-four linear filter for the unknown symmetric C."""

    s = derive_s(a, b)
    n = len(a)
    half = (n - 1) // 2
    inverse_two = pow(2, -1, n)
    rows: list[tuple[int, int]] = []

    for lag in range(1, half + 1):
        q_numerator = -(
            periodic_autocorrelation(a, lag) + periodic_autocorrelation(b, lag)
        )
        if q_numerator % 2:
            return LinearSystem(tuple(rows), half, f"lag {lag}: q is nonintegral"), s
        q = q_numerator // 2

        # The involution i -> -i-lag reverses the directed correlation edge.
        # It has the unique fixed point i=-lag/2, whose C-product is one and
        # whose S endpoint signs agree by symmetry.
        fixed = (-lag * inverse_two) % n
        if s[fixed] != s[(fixed + lag) % n]:
            raise AssertionError("the reflection-fixed edge must be selected")
        selected = {
            index
            for index in range(n)
            if s[index] == s[(index + lag) % n]
        }
        selected.remove(fixed)
        representatives: list[int] = []
        while selected:
            index = min(selected)
            mate = (-index - lag) % n
            if mate == index or mate not in selected:
                raise AssertionError("edge-reflection orbit mismatch")
            selected.remove(index)
            selected.remove(mate)
            representatives.append(index)

        # PAF_C+PAF_D=2*(1+2*sum_E c_i*c_(i+lag)).  Therefore
        # sum_E c_i*c_(i+lag)=(q-1)/2, where q=-(PAF_A+PAF_B)/2.
        if (q - 1) % 2:
            return LinearSystem(tuple(rows), half, f"lag {lag}: fixed-edge parity"), s
        sign_sum_target = (q - 1) // 2
        negative_edge_numerator = len(representatives) - sign_sum_target
        if negative_edge_numerator % 2:
            return LinearSystem(tuple(rows), half, f"lag {lag}: edge parity"), s
        negative_edges = negative_edge_numerator // 2
        if not 0 <= negative_edges <= len(representatives):
            return LinearSystem(tuple(rows), half, f"lag {lag}: edge count bound"), s

        mask = 0
        for index in representatives:
            for endpoint in (index, (index + lag) % n):
                variable = pair_variable(endpoint, n)
                if variable is not None:
                    mask ^= 1 << variable
        rows.append((mask, negative_edges & 1))

    # Replacing C by D=S*C swaps the two unknown symmetric sequences and must
    # leave the homogeneous coefficient system invariant.  In negative-entry
    # bits this says that the half-mask of S is a null vector.  Check it
    # mechanically.  Whenever that mask is nonzero it gives rank <= half-1,
    # as it does in the order-167 search lane; generic small fixtures can have
    # S identically +1 and therefore do not inherit that rank bound.
    s_mask = sum(1 << (index - 1) for index in range(1, half + 1) if s[index] == -1)
    if any((mask & s_mask).bit_count() % 2 for mask, _rhs in rows):
        raise AssertionError("C/D swap mask is not in the GF(2) nullspace")
    return LinearSystem(tuple(rows), half), s


def solve_linear_system(system: LinearSystem) -> LinearSolution | None:
    """RREF solve a bit-packed GF(2) system and return a nullspace basis."""

    if system.early_rejection is not None:
        return None
    rows = [list(row) for row in system.rows]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(system.variables):
        found = next(
            (index for index in range(pivot_row, len(rows)) if (rows[index][0] >> column) & 1),
            None,
        )
        if found is None:
            continue
        rows[pivot_row], rows[found] = rows[found], rows[pivot_row]
        pivot_mask, pivot_rhs = rows[pivot_row]
        for index, (mask, rhs) in enumerate(rows):
            if index != pivot_row and ((mask >> column) & 1):
                rows[index] = [mask ^ pivot_mask, rhs ^ pivot_rhs]
        pivot_columns.append(column)
        pivot_row += 1

    if any(mask == 0 and rhs for mask, rhs in rows):
        return LinearSolution(len(pivot_columns), True)

    particular = 0
    for index, column in enumerate(pivot_columns):
        if rows[index][1]:
            particular |= 1 << column
    pivot_set = set(pivot_columns)
    free_columns = [column for column in range(system.variables) if column not in pivot_set]
    nullspace = []
    for free in free_columns:
        vector = 1 << free
        for index, pivot in enumerate(pivot_columns):
            if (rows[index][0] >> free) & 1:
                vector |= 1 << pivot
        nullspace.append(vector)
    return LinearSolution(
        rank=len(pivot_columns),
        inconsistent=False,
        particular=particular,
        nullspace=tuple(nullspace),
    )


def affine_vectors(solution: LinearSolution, maximum_nullity: int = 20):
    if solution.inconsistent:
        return
    if len(solution.nullspace) > maximum_nullity:
        raise ValueError(
            f"nullity {len(solution.nullspace)} exceeds enumeration cap {maximum_nullity}"
        )
    for selector in range(1 << len(solution.nullspace)):
        vector = solution.particular
        for index, basis in enumerate(solution.nullspace):
            if (selector >> index) & 1:
                vector ^= basis
        yield vector


def recover_c_d(
    a: tuple[int, ...],
    b: tuple[int, ...],
    c_sum: int,
    d_sum: int,
) -> Recovery:
    """Recover and exactly check all C,D allowed by the GF(2) filter."""

    n = len(a)
    system, s = c_linear_system(a, b)
    solution = solve_linear_system(system)
    if solution is None or solution.inconsistent:
        return Recovery(system, solution, 0, ())
    expected_c_weight = (n - c_sum) // 4
    expected_d_weight = (n - d_sum) // 4
    weight_survivors = 0
    candidates = []
    for vector in affine_vectors(solution):
        if vector.bit_count() != expected_c_weight:
            continue
        c = symmetric_from_negative_mask(vector, n)
        d = tuple(left * right for left, right in zip(s, c, strict=True))
        if sum(1 for index in range(1, (n + 1) // 2) if d[index] == -1) != expected_d_weight:
            continue
        weight_survivors += 1
        try:
            candidate = validate_good_quadruple((a, b, c, d), n)
        except ValueError:
            continue
        candidates.append(candidate)
    return Recovery(system, solution, weight_survivors, tuple(candidates))


def random_mask_with_weight(rng: random.Random, length: int, weight: int) -> int:
    mask = 0
    for index in rng.sample(range(length), weight):
        mask |= 1 << index
    return mask


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=int, choices=(0, 1), default=0)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--random-seed", type=int, default=668)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    # B is the uniquely normalized symmetric sequence with row sum 15 in
    # either profile.  Swapping C,D makes the displayed orientations safe.
    c_sum, d_sum = ((-1, -21), (-9, 19))[args.profile]
    n = ORDER
    half = (n - 1) // 2
    b_weight = (n - 15) // 4
    rng = random.Random(args.random_seed)
    counters: Counter[str] = Counter()
    ranks: Counter[int] = Counter()

    for trial in range(args.trials):
        # a_1=+1 is the safe i -> -i decimation symmetry break.
        a_mask = rng.getrandbits(half) & ~1
        b_mask = random_mask_with_weight(rng, half, b_weight)
        a = skew_from_negative_mask(a_mask)
        b = symmetric_from_negative_mask(b_mask)
        recovery = recover_c_d(a, b, c_sum, d_sum)
        if recovery.system.early_rejection:
            counters["early_rejection"] += 1
            continue
        if recovery.solution is None or recovery.solution.inconsistent:
            counters["linear_inconsistent"] += 1
            if recovery.solution is not None:
                ranks[recovery.solution.rank] += 1
            continue
        ranks[recovery.solution.rank] += 1
        if not recovery.weight_survivors:
            counters["weight_rejection"] += 1
            continue
        if not recovery.candidates:
            counters["exact_paf_rejection"] += 1
            continue
        candidate = recovery.candidates[0]
        payload = {
            "kind": "circulant_good_matrices",
            "order": n,
            "hadamard_order": 4 * n,
            "profile": args.profile,
            "row_sums": [sum(sequence) for sequence in candidate[1:]],
            "sequences": [list(sequence) for sequence in candidate],
            "trial": trial,
            "random_seed": args.random_seed,
        }
        rendered = json.dumps(payload, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered)
            print(f"wrote={args.output}")
        else:
            print(rendered, end="")
        print(f"FOUND trial={trial}")
        return 0

    print(f"trials={args.trials}")
    print(f"profile={args.profile} B,C,D_sums={(15, c_sum, d_sum)}")
    print(f"outcomes={dict(sorted(counters.items()))}")
    print(f"rank_histogram={dict(sorted(ranks.items()))}")
    print("FOUND=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
