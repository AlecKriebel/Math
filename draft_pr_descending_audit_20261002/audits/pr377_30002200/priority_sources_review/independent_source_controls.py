#!/usr/bin/env python3
"""Source-first exact falsifiers; no candidate imports and no floating point."""
import itertools
import json
import math
from datetime import datetime, timezone


def invariant(lengths):
    r = len(lengths)
    total = sum(lengths)
    sums = [0] * (1 << r)
    for mask in range(1, 1 << r):
        bit = mask & -mask
        sums[mask] = sums[mask ^ bit] + lengths[bit.bit_length() - 1]
    ties = [mask for mask, value in enumerate(sums) if 2 * value == total]
    if ties:
        return {"generic": False, "tie_count": len(ties)}
    short = [2 * value < total for value in sums]
    positive = []
    long_count = 0
    for mask in range(1 << r):
        if not short[mask]:
            long_count += 1
            sigma = sum(short[mask ^ (1 << j)] for j in range(r) if mask >> j & 1)
            if sigma:
                positive.append(sigma)
    assert long_count == 1 << (r - 1)
    return {"generic": True, "mu": min(positive), "long_count": long_count}


def main():
    print(json.dumps({"started_utc": datetime.now(timezone.utc).isoformat(),
                      "method": "exact subset sums and independently derived grade identities"}))
    cases = 0
    for r in range(1, 16):
        for m in range((r - 1) // 2 + 1):
            lengths = [0] * (r - 2 * m - 1) + [1] * (2 * m + 1)
            got = invariant(lengths)
            assert got["generic"] and got["mu"] == m + 1
            assert m < r / 2
            print(json.dumps({"family": "padded_odd", "r": r, "m": m,
                              "lengths": lengths, "dimension_a1_b1": 3 * r - 2,
                              **got}, sort_keys=True))
            cases += 1
    for r in range(2, 15, 2):
        got = invariant([1] * r)
        assert not got["generic"] and got["tie_count"] == math.comb(r, r // 2)
        print(json.dumps({"negative_control": "even_equilateral", "r": r, **got}))
    for r in range(2, 13):
        lengths = [0] * (r - 1) + [1]
        assert invariant(lengths)["mu"] == 1
    for r in range(5, 13):
        maximal = (r - 1) // 2
        assert maximal == math.ceil(r / 2) - 1
        assert not invariant([0] * r)["generic"]
    perm = [2, 1, 1, 1, 2]
    expected = invariant(perm)
    assert expected["generic"]
    permutation_count = 0
    for ell in sorted(set(itertools.permutations(perm))):
        assert invariant(ell) == expected
        permutation_count += 1
    print(json.dumps({"permutation_control_count": permutation_count, "invariant": expected}))
    for m, a, b in itertools.product(range(1, 5), range(1, 4), range(1, 5)):
        r = 2 * m + 1
        d = 2 * a + 2 * b - 1
        dbar = 2 * a - 1
        from_kernel_and_duality = -(m - 1) * d - 2 * dbar + r * d - 1
        corrected = (m + 2) * d - 2 * dbar - 1
        old = (m + 1) * d - dbar + 1
        assert corrected == from_kernel_and_duality
        assert corrected - old == 2 * b - 2
    print(json.dumps({"grade_control_count": 48, "b1_masks_2023_error": True,
                      "b2_detects_old_shift_difference": 2,
                      "topological_proof_is_not_computation": True,
                      "padded_odd_case_count": cases,
                      "completed_utc": datetime.now(timezone.utc).isoformat(), "status": "PASS"}))


if __name__ == "__main__":
    main()
