#!/usr/bin/env python3
"""Independent integer-only audit of the C(sl_3,6) fusion arithmetic.

This does not construct a local Yang--Baxter matrix.  It verifies that every
low- and high-strand central-multiplicity/inclusion constraint obtained from
the Jones--Wenzl tower is compatible with every even local dimension.
"""

from collections import defaultdict
from fractions import Fraction


LEVEL = 3
WEIGHTS = tuple(
    (a, b)
    for a in range(LEVEL + 1)
    for b in range(LEVEL + 1 - a)
)

# Exact quantum dimensions at SU(3) level 3.  The quantum Weyl formula is
# [a+1][b+1][a+b+2]/[2], with [1..5] = 1,sqrt(3),2,sqrt(3),1.
QDIM = {
    (0, 0): 1,
    (1, 0): 2,
    (0, 1): 2,
    (2, 0): 2,
    (1, 1): 3,
    (0, 2): 2,
    (3, 0): 1,
    (2, 1): 2,
    (1, 2): 2,
    (0, 3): 1,
}
assert set(QDIM) == set(WEIGHTS)
assert sum(value * value for value in QDIM.values()) == 36


def tensor_x(weight):
    """Fusion with X=(1,0) in SU(3)_3, with multiplicity one."""

    a, b = weight
    candidates = ((a + 1, b), (a - 1, b + 1), (a, b - 1))
    return tuple(candidate for candidate in candidates if candidate in QDIM)


# Perron--Frobenius dimension equation N_X D = 2 D.
for source in WEIGHTS:
    assert sum(QDIM[target] for target in tensor_x(source)) == 2 * QDIM[source]

# f[n][lambda] is the number of admissible paths from 1 to lambda, equivalently
# the simple-matrix-block size in End(X^tensor n).
paths = {(0, 0): 1}
records = []
for n in range(0, 41):
    assert sum(paths.get(weight, 0) * QDIM[weight] for weight in WEIGHTS) == 2**n
    records.append(dict(paths))
    next_paths = defaultdict(int)
    for source, count in paths.items():
        for target in tensor_x(source):
            next_paths[target] += count
    paths = dict(next_paths)

# For local dimension d=2r, trace equality forces the multiplicity of the
# lambda block to be D_lambda r^n.  Check total dimension and compatibility
# under restriction for several independent integer values of r.
for r in (1, 2, 3, 5, 11):
    d = 2 * r
    for n, path_counts in enumerate(records):
        multiplicity = {
            weight: QDIM[weight] * r**n
            for weight in path_counts
        }
        total = sum(
            path_counts[weight] * multiplicity[weight]
            for weight in path_counts
        )
        assert total == d**n

        # The central trace weight is f_lambda D_lambda / 2^n.
        for weight, block_size in path_counts.items():
            central_weight = Fraction(
                block_size * QDIM[weight],
                2**n,
            )
            central_rank = block_size * multiplicity[weight]
            assert central_rank == central_weight * d**n

        if n + 1 < len(records):
            reached_next = records[n + 1]
            for source in path_counts:
                restricted_multiplicity = sum(
                    QDIM[target] * r ** (n + 1)
                    for target in tensor_x(source)
                    if target in reached_next
                )
                assert restricted_multiplicity == d * multiplicity[source]

# At d=6 (r=3), print representative exact multiplicities.
for n in range(0, 7):
    entries = [
        f"{weight}:{QDIM[weight] * 3**n}"
        for weight in sorted(records[n])
    ]
    print(f"n={n}: " + ", ".join(entries))

print("[ok] ten quantum dimensions are integral and square-sum to 36")
print("[ok] fusion by X has Perron--Frobenius eigenvalue 2")
print("[ok] path and central-weight identities hold through n=40")
print("[ok] all inclusion multiplicities hold for d=2r, including d=6")
print("[conclusion] tower arithmetic forces only 2 | d, not 4 | d")
