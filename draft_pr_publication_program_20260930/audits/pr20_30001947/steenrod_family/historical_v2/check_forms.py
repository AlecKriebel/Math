"""Exact F2 form probes. These test the algebra adapter, not the space theorem."""

import json
from itertools import combinations
from pathlib import Path


def pairing(rows, x, y):
    result = 0
    for i, row in enumerate(rows):
        if x >> i & 1:
            result ^= (row & y).bit_count() & 1
    return result


def rank(rows):
    work = list(rows)
    pivot = 0
    for column in range(len(rows)):
        found = next((i for i in range(pivot, len(work)) if work[i] >> column & 1), None)
        if found is None:
            continue
        work[pivot], work[found] = work[found], work[pivot]
        for i in range(len(work)):
            if i != pivot and work[i] >> column & 1:
                work[i] ^= work[pivot]
        pivot += 1
    return pivot


def symplectic_basis(rows):
    generators = [1 << i for i in range(len(rows))]
    planes = []
    while generators:
        e = generators[0]
        partner = next(i for i, f in enumerate(generators) if pairing(rows, e, f))
        f = generators[partner]
        planes.append((e, f))
        generators = [
            x ^ (e if pairing(rows, x, f) else 0) ^ (f if pairing(rows, x, e) else 0)
            for i, x in enumerate(generators)
            if i not in (0, partner)
        ]
    ordered = [v for plane in planes for v in plane]
    assert rank(ordered) == len(rows)
    for a, x in enumerate(ordered):
        for b, y in enumerate(ordered):
            assert pairing(rows, x, y) == int((a ^ 1) == b)
    lagrangian = [e for e, _ in planes]
    assert rank(lagrangian + [0] * (len(rows) - len(lagrangian))) == len(lagrangian)
    assert all(pairing(rows, x, y) == 0 for x in lagrangian for y in lagrangian)
    return planes


def exhaustive_alternating(n):
    coordinates = list(combinations(range(n), 2))
    total = 1 << len(coordinates)
    nonsingular = 0
    for encoded in range(total):
        rows = [0] * n
        for bit, (a, b) in enumerate(coordinates):
            if encoded >> bit & 1:
                rows[a] |= 1 << b
                rows[b] |= 1 << a
        assert all(pairing(rows, 1 << a, 1 << a) == 0 for a in range(n))
        if rank(rows) == n:
            nonsingular += 1
            symplectic_basis(rows)
    return {"dimension": n, "alternating_matrices": total,
            "nonsingular_matrices_with_checked_symplectic_basis": nonsingular}


def main():
    probes = [exhaustive_alternating(n) for n in (0, 2, 4, 6)]
    assert [p["nonsingular_matrices_with_checked_symplectic_basis"] for p in probes] == [1, 1, 28, 13888]
    rank_one_nonalt = [1]
    singular_alt = [2, 1, 0]
    assert rank(rank_one_nonalt) == 1 and pairing(rank_one_nonalt, 1, 1) == 1
    assert rank(singular_alt) == 2 and all(pairing(singular_alt, x, x) == 0 for x in range(8))
    result = {
        "arithmetic": "exact bit operations over F2; no floating point",
        "scope": "finite algebra supplement only; not universal geometric evidence",
        "alternating_probes": probes,
        "countercontrols": {
            "one_dimensional_identity": "nonsingular and nonalternating; no nonzero isotropic vector",
            "three_dimensional_hyperbolic_plus_zero": "alternating but singular; cannot be used as a Witt form"
        },
        "status": "passed"
    }
    Path(__file__).with_name("form_probe_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
