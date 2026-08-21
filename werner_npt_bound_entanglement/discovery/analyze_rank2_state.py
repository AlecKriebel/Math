#!/usr/bin/env python3
"""Small dependency-free diagnostics for a saved rank-two search state."""

from __future__ import annotations

import cmath
import sys


def digits(index: int, d: int, n: int) -> tuple[int, ...]:
    out = []
    for _ in range(n):
        out.append(index % d)
        index //= d
    return tuple(out)


def inner(x: list[complex], y: list[complex]) -> complex:
    return sum(a.conjugate() * b for a, b in zip(x, y))


def local_cross(
    x: list[complex], y: list[complex], site: int, d: int, n: int
) -> list[list[complex]]:
    out = [[0j for _ in range(d)] for _ in range(d)]
    all_digits = [digits(k, d, n) for k in range(d**n)]
    for p, dp in enumerate(all_digits):
        for q, dq in enumerate(all_digits):
            if all(dp[k] == dq[k] for k in range(n) if k != site):
                out[dp[site]][dq[site]] += x[p] * y[q].conjugate()
    return out


def mat_inner(a: list[list[complex]], b: list[list[complex]]) -> complex:
    return sum(
        a[i][j].conjugate() * b[i][j]
        for i in range(len(a))
        for j in range(len(a[0]))
    )


def determinant3(a: list[list[complex]]) -> complex:
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def main() -> None:
    path = sys.argv[1]
    d = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    size = d**n
    left = [[0j] * size for _ in range(2)]
    right = [[0j] * size for _ in range(2)]
    singular = []
    with open(path, encoding="utf-8") as source:
        for line in source:
            fields = line.split()
            if fields[0] == "singular":
                singular = [float(fields[1]), float(fields[2])]
            elif fields[0] in ("left", "right"):
                row, column = int(fields[1]), int(fields[2])
                value = complex(float(fields[3]), float(fields[4]))
                (left if fields[0] == "left" else right)[column][row] = value

    print("singular", singular)
    print("global U*V")
    for a in range(2):
        print([inner(left[a], right[b]) for b in range(2)])
    for site in range(n):
        lu = [[0j] * d for _ in range(d)]
        rv = [[0j] * d for _ in range(d)]
        print("site", site)
        for a in range(2):
            ua = local_cross(left[a], left[a], site, d, n)
            va = local_cross(right[a], right[a], site, d, n)
            print(
                " vector", a,
                "purity U", mat_inner(ua, ua).real,
                "purity V", mat_inner(va, va).real,
            )
            for i in range(d):
                for j in range(d):
                    lu[i][j] += ua[i][j]
                    rv[i][j] += va[i][j]
        combined = [
            [lu[i][j] + rv[i][j] for j in range(d)] for i in range(d)
        ]
        print(
            " det support U,V,combined",
            determinant3(lu).real,
            determinant3(rv).real,
            determinant3(combined).real,
        )
        print(
            " cross local Gram",
            [
                [
                    mat_inner(
                        local_cross(left[a], left[b], site, d, n),
                        local_cross(right[a], right[b], site, d, n),
                    )
                    for b in range(2)
                ]
                for a in range(2)
            ],
        )


if __name__ == "__main__":
    main()
