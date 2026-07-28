#!/usr/bin/env python3
"""Exact stress test of the one-sided local-support/product-space identity.

This uses deliberately nonorthogonal local A vectors and arbitrary entangled
B vectors.  It compares two independent integer contractions of

    R = 2^n <psi|X_{-1/2,d}^{tensor n}|psi>.

The test illustrates the index ordering in the proof; the proof itself does
not depend on this finite example.
"""

from itertools import product

D = 3
N = 3

# a[r][i][x].  At every site the two vectors are nonorthogonal; no W_i below
# is assumed isometric.
a = [
    [(1, 0, 1), (1, 2, 0), (1, -1, 1)],
    [(1, 1, 0), (0, 1, 1), (2, 0, 1)],
]

words = list(product(range(D), repeat=N))

# Arbitrary, non-product B-side tensors.
b = [
    tuple(((2*j*j + 3*j + 1) % 7) - 3 for j in range(D**N)),
    tuple(((j*j*j + 2*j + 4) % 9) - 4 for j in range(D**N)),
]


def avec(r, aword):
    z = 1
    for i, x in enumerate(aword):
        z *= a[r][i][x]
    return z


# Coefficient matrix of psi, with A and B multi-indices in lexicographic
# order matching `words`.
C = [
    [
        sum(avec(r, aw) * b[r][bi] for r in range(2))
        for bi, _ in enumerate(words)
    ]
    for aw in words
]


def local_scaled_x(aa, bb, cc, ee):
    """Matrix element <aa,bb| 2 X_{-1/2,d} |cc,ee>."""
    return 2 * (aa == cc and bb == ee) - (aa == bb and cc == ee)


# First contraction: full coefficient matrix against (2 X)^tensor N.
direct = 0
for ai, aw in enumerate(words):
    for bi, bw in enumerate(words):
        cab = C[ai][bi]
        if not cab:
            continue
        for ci, cw in enumerate(words):
            for ei, ew in enumerate(words):
                cce = C[ci][ei]
                if not cce:
                    continue
                k = 1
                for site in range(N):
                    k *= local_scaled_x(
                        aw[site], bw[site], cw[site], ew[site]
                    )
                direct += cab * k * cce


# Second contraction: local 2-by-2 operator blocks
# K_i[r,b,s,e] = <a_{r,i},b|2X|a_{s,i},e>, followed by the diagonal
# label embedding r -> (r,...,r).
K = []
for site in range(N):
    Ki = {}
    for r, bb, s, ee in product(range(2), range(D), range(2), range(D)):
        Ki[r, bb, s, ee] = sum(
            a[r][site][aa]
            * local_scaled_x(aa, bb, cc, ee)
            * a[s][site][cc]
            for aa in range(D)
            for cc in range(D)
        )
    K.append(Ki)

compressed = 0
for r, s in product(range(2), repeat=2):
    for bi, bw in enumerate(words):
        for ei, ew in enumerate(words):
            k = 1
            for site in range(N):
                k *= K[site][r, bw[site], s, ew[site]]
            compressed += b[r][bi] * k * b[s][ei]

print("2^n Q direct      =", direct)
print("2^n Q compressed  =", compressed)
print("exact identity    =", direct == compressed)
assert direct == compressed
assert direct >= 0
