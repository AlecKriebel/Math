"""Exact data and elementary operations for Eliahou's order-668 seed.

All indexing in the code is zero-based.  The source paper uses one-based
coordinates, so its half-sign involution keeps entries 1,...,84 and negates
entries 85,...,167.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence


N = 167
HALF = 84

ELIAHOU_Q_RUNS = (83, 2, 81, 1)
ELIAHOU_S_RUNS = (
    (4,) * 5
    + (2, 1, 1) * 5
    + (1, 5)
    + (4,) * 4
    + (2, 1, 1) * 6
    + (4,) * 4
    + (3,)
    + (1, 2, 1) * 5
    + (3,)
    + (4,) * 4
    + (3,)
    + (1, 2, 1) * 5
)

ELIAHOU_RESIDUALS = {
    4: -512,
    8: 384,
    12: -256,
    16: 128,
    26: -64,
    30: 128,
    34: -192,
    38: 256,
    42: -320,
    46: 256,
    50: -192,
    54: 128,
    58: -64,
}


def decode_runs(runs: Iterable[int], first: int = 1) -> tuple[int, ...]:
    """Expand alternating run lengths into a tuple of +1/-1 entries."""

    if first not in (-1, 1):
        raise ValueError("first must be +1 or -1")
    result: list[int] = []
    sign = first
    for run in runs:
        if run <= 0:
            raise ValueError("run lengths must be positive")
        result.extend([sign] * run)
        sign = -sign
    return tuple(result)


ELIAHOU_Q = decode_runs(ELIAHOU_Q_RUNS)
ELIAHOU_S = decode_runs(ELIAHOU_S_RUNS)


def validate_sign_sequence(sequence: Sequence[int], length: int | None = None) -> None:
    if length is not None and len(sequence) != length:
        raise ValueError(f"expected length {length}, got {len(sequence)}")
    if any(value not in (-1, 1) for value in sequence):
        raise ValueError("sequence entries must all be +1 or -1")


def half_sign_involution(sequence: Sequence[int]) -> tuple[int, ...]:
    """Apply Eliahou's prime involution to a sign sequence."""

    validate_sign_sequence(sequence)
    h = (len(sequence) + 1) // 2
    return tuple(sequence[:h]) + tuple(-value for value in sequence[h:])


def pointwise(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    if len(left) != len(right):
        raise ValueError("pointwise factors must have equal length")
    validate_sign_sequence(left)
    validate_sign_sequence(right)
    return tuple(a * b for a, b in zip(left, right, strict=True))


def aperiodic_autocorrelation(sequence: Sequence[int], lag: int) -> int:
    validate_sign_sequence(sequence)
    if not 0 <= lag < len(sequence):
        raise ValueError("aperiodic lag is out of range")
    return sum(sequence[i] * sequence[i + lag] for i in range(len(sequence) - lag))


def periodic_autocorrelation(sequence: Sequence[int], lag: int) -> int:
    validate_sign_sequence(sequence)
    n = len(sequence)
    if not 0 <= lag < n:
        raise ValueError("periodic lag is out of range")
    return sum(sequence[i] * sequence[(i + lag) % n] for i in range(n))


def special_quadruple(
    s: Sequence[int], q: Sequence[int] = ELIAHOU_Q
) -> tuple[tuple[int, ...], ...]:
    """Return (s, s', sq, (sq)') in the notation of Eliahou's paper."""

    if len(s) != len(q):
        raise ValueError("s and q must have equal length")
    validate_sign_sequence(s)
    validate_sign_sequence(q)
    sq = pointwise(s, q)
    return tuple(s), half_sign_involution(s), sq, half_sign_involution(sq)


def summed_aperiodic_correlations(
    sequences: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    if not sequences:
        raise ValueError("at least one sequence is required")
    n = len(sequences[0])
    if any(len(sequence) != n for sequence in sequences):
        raise ValueError("all sequences must have equal length")
    return tuple(
        sum(aperiodic_autocorrelation(sequence, lag) for sequence in sequences)
        for lag in range(n)
    )


def summed_periodic_correlations(
    sequences: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    if not sequences:
        raise ValueError("at least one sequence is required")
    n = len(sequences[0])
    if any(len(sequence) != n for sequence in sequences):
        raise ValueError("all sequences must have equal length")
    return tuple(
        sum(periodic_autocorrelation(sequence, lag) for sequence in sequences)
        for lag in range(n)
    )


def fixed_q_edges(lag: int, q: Sequence[int] = ELIAHOU_Q) -> tuple[tuple[int, int], ...]:
    """Edges surviving the two involution filters in the fixed-q identity."""

    n = len(q)
    h = (n + 1) // 2
    if not 0 <= lag < n:
        raise ValueError("lag is out of range")
    edges = []
    for i in range(n - lag):
        j = i + lag
        same_half = (i < h) == (j < h)
        if same_half and q[i] == q[j]:
            edges.append((i, j))
    return tuple(edges)


def fixed_q_reduced_sums(
    s: Sequence[int], q: Sequence[int] = ELIAHOU_Q
) -> tuple[int, ...]:
    """Return F_k/4 from the fixed-q identity, including lag zero."""

    if len(s) != len(q):
        raise ValueError("s and q must have equal length")
    validate_sign_sequence(s)
    return tuple(
        sum(s[i] * s[j] for i, j in fixed_q_edges(lag, q))
        for lag in range(len(s))
    )


def reduced_blocks(s: Sequence[int]) -> tuple[tuple[int, ...], tuple[int, ...], int, int]:
    """Extract the active X(83), Y(81), and endpoint signs u,v.

    For Eliahou's q, the fixed-q equations become

        c_k(X) + c_k(Y) = 0,  1 <= k <= 80,
        c_81(X) = 0,
        x_0*x_82 + u*v = 0.

    Coordinates s[83] and q[83] form an isolated singleton and do not occur.
    """

    validate_sign_sequence(s, N)
    x = tuple(s[0:83])
    u = s[84]
    y = tuple(s[85:166])
    v = s[166]
    return x, y, u, v


def assemble_reduced_blocks(
    x: Sequence[int],
    y: Sequence[int],
    u: int = 1,
    v: int = 1,
    isolated: int = 1,
) -> tuple[int, ...]:
    """Assemble a length-167 sequence from the reduced fixed-q variables."""

    validate_sign_sequence(x, 83)
    validate_sign_sequence(y, 81)
    validate_sign_sequence((u, v, isolated), 3)
    return tuple(x) + (isolated, u) + tuple(y) + (v,)
