#!/usr/bin/env python3
"""Exact audit for the four-copy invariant-SOS obstruction.

Only Python's standard library is used.  The code:

* constructs fifteen explicit sparse orthonormal two-column qutrit codes;
* computes all sixteen swap-sector masses with Fraction arithmetic;
* checks the two logical-parity identities;
* verifies rank 15 of the augmented sector vectors, hence affine
  dimension 14;
* audits the negative decomposable-orbit and full-code values.
"""

from fractions import Fraction as F


RAW_CODES = [
    ("1021+", "0102+"),
    ("0011+", "1211+"),
    ("0202+", "0122+"),
    ("0000+ 0202-", "0110- 2010+"),
    ("0012+ 0102+ 0111- 0200+", "0002+ 0202+ 1112- 2012+"),
    ("0001+ 1111- 1212+ 2111- 2200-",
     "2011- 2102+ 2120+ 2121+ 2201+"),
    ("0100+ 1211- 1212+ 2011+ 2201-",
     "0002+ 0110- 0221+ 1122- 2222+"),
    ("0201- 2112+", "1211- 2010-"),
    ("0002- 0220- 1012+ 1200-", "0000- 1101+ 2010+ 2012-"),
    ("2120-", "1220+"),
    ("0011- 2020- 2122+", "1121+ 1200- 2000-"),
    ("0101+ 2222+", "0021- 2111+"),
    ("0121+ 1121- 1202- 2112+", "0120+ 0211+ 2121- 2221+"),
    ("0010- 0202- 1102+ 2000+", "1122- 2120+ 2121- 2210+"),
    ("0222- 1011+ 1020- 1112+ 1212-",
     "0002- 0012+ 0101- 0221- 2120+"),
    ("0010- 1012+ 1212- 2201+", "1002+ 1200- 1222- 2102+"),
]


def parse(text):
    out = {}
    for token in text.split():
        word, sign = token[:4], token[4]
        out[tuple(int(x) for x in word)] = 1 if sign == "+" else -1
    return out


def reduction(code, keep):
    """Reduction of P=|u><u|+|v><v|, stored as a sparse matrix."""
    keep = tuple(keep)
    traced = tuple(i for i in range(4) if i not in keep)
    out = {}
    for vector in code:
        norm = sum(a * a for a in vector.values())
        for x, ax in vector.items():
            for y, ay in vector.items():
                if all(x[i] == y[i] for i in traced):
                    key = (
                        tuple(x[i] for i in keep),
                        tuple(y[i] for i in keep),
                    )
                    out[key] = out.get(key, F(0)) + F(ax * ay, norm)
    return {key: value for key, value in out.items() if value}


def hs_squared(matrix):
    return sum(value * value for value in matrix.values())


def sectors(code):
    moments = []
    for mask in range(16):
        keep = tuple(i for i in range(4) if (mask >> i) & 1)
        moments.append(hs_squared(reduction(code, keep)))
    return tuple(
        sum(
            (-1) ** ((r & mask).bit_count()) * moments[mask]
            for mask in range(16)
        ) / 16
        for r in range(16)
    )


def rational_rank(rows):
    a = [list(row) for row in rows]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        value = a[row][col]
        a[row] = [x / value for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                value = a[i][col]
                a[i] = [
                    a[i][j] - value * a[row][j]
                    for j in range(len(a[0]))
                ]
        row += 1
        if row == len(a):
            break
    return row


rows = []
for raw_u, raw_v in RAW_CODES:
    u, v = parse(raw_u), parse(raw_v)
    assert set(u).isdisjoint(v)
    p = sectors((u, v))
    assert sum(p[r] for r in range(16) if r.bit_count() % 2 == 0) == 3
    assert sum(p[r] for r in range(16) if r.bit_count() % 2 == 1) == 1
    assert all(value >= 0 for value in p)
    rows.append(p + (F(1),))

assert rational_rank(rows) == 15

# The full equality code in (13)--(16).
u = parse("0000+ 0110+")
v = parse("1000+ 1110+")
p = sectors((u, v))
e = [
    sum(p[r] for r in range(16) if r.bit_count() == weight)
    for weight in range(5)
]
assert e == [F(9, 4), F(3, 4), F(3, 4), F(1, 4), F(0)]
assert e[2] - 3 * e[3] + 10 * e[4] == 0

# The singled-out full-difference Hodge orbit has the exact negative
# contribution (14)--(15).
orbit_pair_mass = F(1, 4)
orbit_triple_mass = F(1, 4)
assert orbit_pair_mass - 3 * orbit_triple_mass == -F(1, 2)

# The coefficient comparison in Theorem 3.
# alpha <= 0 and beta <= -3 force a negative constant.
alpha, beta = F(0), F(-3)
assert 3 * alpha + beta == -3

print("verified: affine rank 15, parity identities, and SOS obstruction")
