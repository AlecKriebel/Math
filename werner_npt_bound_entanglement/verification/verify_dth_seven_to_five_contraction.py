#!/usr/bin/env python3
"""Exact seven-to-five replica contraction used by the DTH extension test.

At one physical qutrit site, the commutant is represented by permutation
operators.  Tracing replica positions 4 and 5 deletes those symbols from the
cycle notation.  Every cycle lying wholly in the deleted set contributes one
factor of the local dimension.  The verifier checks the resulting map and its
Hilbert--Schmidt adjoint exhaustively on S_7 x S_5.

No third-party packages or floating-point arithmetic are used.
"""

from itertools import permutations


D = 3
N = 7
DELETED = frozenset((4, 5))
RETAINED = tuple(i for i in range(N) if i not in DELETED)
RETAINED_INDEX = {value: index for index, value in enumerate(RETAINED)}


def compose(left, right):
    """Return left o right for image-form permutations."""
    return tuple(left[right[i]] for i in range(len(left)))


def inverse(permutation):
    out = [None] * len(permutation)
    for source, target in enumerate(permutation):
        out[target] = source
    return tuple(out)


def cycles(permutation):
    seen = set()
    out = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        cycle = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = permutation[current]
        out.append(tuple(cycle))
    return tuple(out)


def cycle_count(permutation):
    return len(cycles(permutation))


def delete_from_cycles(permutation):
    """Return (closed_cycle_count, induced permutation on retained slots)."""
    induced = list(range(len(RETAINED)))
    closed = 0
    for cycle in cycles(permutation):
        remaining = [value for value in cycle if value not in DELETED]
        if not remaining:
            closed += 1
            continue
        for source, target in zip(remaining, remaining[1:] + remaining[:1]):
            induced[RETAINED_INDEX[source]] = RETAINED_INDEX[target]
    return closed, tuple(induced)


def embed_five(permutation):
    """Embed S_5 by fixing deleted slots and using retained-slot order."""
    out = list(range(N))
    for source, target in enumerate(permutation):
        out[RETAINED[source]] = RETAINED[target]
    return tuple(out)


def permutation_hs_inner(left, right, dimension=D):
    """Tr(P_left^* P_right) on (C^dimension)^{tensor n}."""
    relative = compose(inverse(left), right)
    return dimension ** cycle_count(relative)


def verify_local_contraction():
    five = tuple(permutations(range(5)))
    seven = tuple(permutations(range(7)))

    for pi in seven:
        closed, reduced = delete_from_cycles(pi)

        # Trace preservation is a first normalization audit.
        assert D ** cycle_count(pi) == (
            D ** closed * D ** cycle_count(reduced)
        )

        # Exhaustive adjoint audit:
        # <P_sigma, Tr_45 P_pi> = <P_sigma tensor I_45, P_pi>.
        for sigma in five:
            left = D ** closed * permutation_hs_inner(sigma, reduced)
            right = permutation_hs_inner(embed_five(sigma), pi)
            assert left == right


def verify_three_site_factors():
    identity7 = tuple(range(7))
    closed, identity5 = delete_from_cycles(identity7)
    assert closed == 2
    assert identity5 == tuple(range(5))

    # The two removed physical replicas have dimension 27^2.  Sitewise cycle
    # deletion gives the same factor 3^(2+2+2)=729.
    assert D ** (3 * closed) == 27 ** 2 == 729

    # A cycle meeting retained slots creates no closed-loop factor.  The other
    # removed singleton contributes exactly one qutrit factor.
    transposition = list(range(7))
    transposition[0], transposition[4] = 4, 0
    closed, reduced = delete_from_cycles(tuple(transposition))
    assert closed == 1
    assert reduced == tuple(range(5))


def main():
    verify_local_contraction()
    verify_three_site_factors()
    print("exact DTH seven-to-five contraction passed")


if __name__ == "__main__":
    main()
