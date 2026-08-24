#!/usr/bin/env python3
"""Standalone exact regressions for the K2P two-sector analytic layer."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path


def fail(message: str) -> None:
    raise RuntimeError(message)


def rank(matrix):
    work = [[F(value) for value in row] for row in matrix]
    if not work:
        return 0
    m, n = len(work), len(work[0])
    r = 0
    for column in range(n):
        pivot = next((i for i in range(r, m) if work[i][column]), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        value = work[r][column]
        work[r] = [entry / value for entry in work[r]]
        for i in range(m):
            if i == r or not work[i][column]:
                continue
            value = work[i][column]
            work[i] = [a - value * b for a, b in zip(work[i], work[r])]
        r += 1
        if r == m:
            break
    return r


def pair_anchor_matrix(degree: int):
    pairs = [(0, 1), (0, 2), (1, 2)] + [(0, k) for k in range(3, degree)]
    return [[int(column in pair) for column in range(degree)] for pair in pairs]


def check_anchors():
    rows = []
    for degree in range(3, 10):
        one = pair_anchor_matrix(degree)
        if rank(one) != degree:
            fail(f"pair-anchor rank failure at degree {degree}")
        two = [row + [0] * degree for row in one] + [
            [0] * degree + row for row in one
        ]
        if rank(two) != 2 * degree:
            fail(f"two-sector anchor rank failure at degree {degree}")
        leading = [row[:3] for row in one[:3]]
        determinant = (
            leading[0][0] * (leading[1][1] * leading[2][2] - leading[1][2] * leading[2][1])
            - leading[0][1] * (leading[1][0] * leading[2][2] - leading[1][2] * leading[2][0])
            + leading[0][2] * (leading[1][0] * leading[2][1] - leading[1][1] * leading[2][0])
        )
        if determinant != -2:
            fail(f"leading determinant drift at degree {degree}: {determinant}")
        rows.append({"degree": degree, "one_sector_rank": degree, "two_sector_rank": 2 * degree})
    scales = tuple(F(value) for value in (2, 3, 5, 7, 11))
    pair_values = {(i, j): 1 / (scales[i] * scales[j]) for i, j in itertools.combinations(range(5), 2)}
    first_squared = pair_values[(0, 1)] * pair_values[(0, 2)] / pair_values[(1, 2)]
    recovered = [F(1, 2)]
    if recovered[0] * recovered[0] != first_squared:
        fail("positive square-root normalizer failed")
    recovered.extend(pair_values[(0, i)] / recovered[0] for i in range(1, 5))
    if tuple(recovered) != tuple(1 / value for value in scales):
        fail("positive normalizer reconstruction failed")
    return {"rank_rows": rows, "recovered": [str(value) for value in recovered]}


def in_dplus(s: F, g: F) -> bool:
    return 0 < s < 1 and 0 < g < 1 and g > 2 * s - 1


def in_ct(s: F, g: F) -> bool:
    return 0 < s < 1 and s * s < g < 1


def check_serial_sections():
    effective = (
        (F(1, 4), F(2, 5)),
        (F(3, 5), F(1, 3)),
        (F(4, 5), F(7, 10)),
    )
    rows = []
    for S, G in effective:
        if not in_dplus(S, G):
            fail("test effective pair outside D_plus")
        for length in range(2, 6):
            power = length - 1
            M = max(S, G, 2 * S - G, F(0))
            # Deterministic rational search for M < r^power < 1.
            r = next(
                (F(n, 1000) for n in range(999, 0, -1) if F(n, 1000) ** power > M),
                None,
            )
            if r is None:
                fail("no serial section r found")
            factors = [(r, r)] * power + [(S / r**power, G / r**power)]
            if not all(in_dplus(s, g) for s, g in factors):
                fail("serial D_plus factor outside domain")
            ps = F(1)
            pg = F(1)
            for s, g in factors:
                ps *= s
                pg *= g
            if (ps, pg) != (S, G):
                fail("serial product mismatch")
            rows.append({"effective": [str(S), str(G)], "length": length, "r": str(r)})
    # Exact CT divisibility examples using perfect-power rational points.
    for length in range(2, 6):
        s0, g0 = F(1, 3), F(1, 2)
        S, G = s0**length, g0**length
        if not in_ct(S, G) or not in_ct(s0, g0):
            fail("continuous-time divisibility regression failed")
    return rows


def check_gluing():
    rows = []
    products = ((F(2, 3), F(7, 5)), (F(5, 4), F(3, 7)), (F(11, 9), F(13, 8)))
    for A, B in products:
        s = min(F(1, 4), A / 4)
        g = min(F(1, 3), B / 3)
        if not in_dplus(s, g) or not in_dplus(s / A, g / B):
            fail("D_plus simultaneous gluing failed")
        # Choose a CT pair by the constructive small-s inequality.
        sct = min(F(1, 10), A / 10)
        lower = max(F(1), B / (A * A)) * sct * sct
        upper = min(F(1), B)
        if not lower < upper:
            fail("CT gluing interval unexpectedly empty")
        gct = (lower + upper) / 2
        if not in_ct(sct, gct) or not in_ct(sct / A, gct / B):
            fail("CT simultaneous gluing failed")
        rows.append({"A": str(A), "B": str(B), "D_plus": [str(s), str(g)], "CT": [str(sct), str(gct)]})
    return rows


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def main():
    if not __debug__:
        fail("optimized mode forbidden")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = {
        "schema": "k2p-bridge-marginal-regression-v1",
        "scope": "principal D_plus and strict continuous-time domains; no mixed-sign claim",
        "anchors": check_anchors(),
        "serial_sections": check_serial_sections(),
        "simultaneous_gluing": check_gluing(),
    }
    payload["payload_sha256"] = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
