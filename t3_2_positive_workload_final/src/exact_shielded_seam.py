"""Finite certificate for the exact shielded/available T3-2 seam.

This module certifies only a finite support reduction and a few algebraic
interfaces used in ``research_notes/certified_exact_shielded_seam.md``.  It
does not certify T3-2 or any stochastic recurrence theorem.

The displayed orientation takes A and B as the active coordinates and uses
the four workload representatives from the inherited two-active atlas.  The
exchange A <-> B is an external symmetry.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Iterable, Sequence


Vector = tuple[int, int, int]
Support = tuple[str, ...]

NAMES: tuple[str, ...] = (
    "0",
    "A",
    "B",
    "C",
    "2A",
    "2B",
    "2C",
    "AB",
    "AC",
    "BC",
)
COMPLEXES: tuple[Vector, ...] = (
    (0, 0, 0),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (2, 0, 0),
    (0, 2, 0),
    (0, 0, 2),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
)
WORKLOADS: tuple[Vector, ...] = (
    (1, 1, 0),
    (2, 3, 0),
    (1, 2, 0),
    (1, 3, 0),
)

AVAILABLE_SUPPORT = frozenset(("C", "AC", "BC"))

EXPECTED_EXACT_SEAM_SUPPORTS: frozenset[Support] = frozenset(
    {
        ("0", "2C"),
        ("A", "B"),
        ("B", "2A"),
        ("2A", "2B"),
        ("2A", "AB"),
        ("2B", "AB"),
        ("2A", "2B", "AB"),
    }
)

UNSUPPORTED_MULTI_VERTEX_SUPPORTS: frozenset[Support] = frozenset(
    {
        ("0", "AC", "BC"),
        ("0", "C", "2C"),
        ("A", "AC", "BC"),
        ("A", "B", "AC"),
        ("A", "B", "BC"),
        ("B", "2A", "BC"),
        ("B", "AC", "BC"),
        ("A", "B", "AC", "BC"),
    }
)

SIGNED_SUPPORTS: frozenset[Support] = frozenset(
    {
        ("0", "A", "BC"),
        ("0", "2A", "BC"),
        ("A", "2A", "BC"),
        ("0", "A", "2A", "BC"),
    }
)


def _dot(left: Sequence[Fraction | int], right: Sequence[Fraction | int]) -> Fraction:
    return sum((Fraction(a) * Fraction(b) for a, b in zip(left, right)), Fraction())


def _indices(mask: int) -> tuple[int, ...]:
    return tuple(index for index in range(len(NAMES)) if mask >> index & 1)


def _support(mask: int) -> Support:
    return tuple(NAMES[index] for index in _indices(mask))


def classify_shielded(mask: int, workload: Vector) -> bool:
    """Replay the inherited finite top-complex shielded classifier."""

    indices = _indices(mask)
    values = {index: _dot(workload, COMPLEXES[index]) for index in indices}
    top = {index for index in indices if values[index] == max(values.values())}
    if len(top) == len(indices):
        return True
    if any(COMPLEXES[index][0] + COMPLEXES[index][1] >= 2 for index in top):
        return False
    active_support = {
        coordinate
        for index in top
        for coordinate in (0, 1)
        if COMPLEXES[index][coordinate]
    }

    def active_count(index: int) -> int:
        return sum(COMPLEXES[index][coordinate] for coordinate in active_support)

    if all(active_count(index) == 1 for index in indices):
        return True
    if any(sum(COMPLEXES[index]) == 1 for index in top):
        return False
    inactive_support = {2 for index in top if COMPLEXES[index][2]}
    lower = set(indices) - top
    if inactive_support and any(COMPLEXES[index][2] for index in lower):
        return False
    return True


def _rref(rows: Iterable[Sequence[int]]) -> tuple[tuple[Fraction, ...], ...]:
    matrix = [list(map(Fraction, row)) for row in rows if any(row)]
    pivot_row = 0
    for column in range(3):
        pivot = next(
            (index for index in range(pivot_row, len(matrix)) if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
        for index in range(len(matrix)):
            if index == pivot_row or not matrix[index][column]:
                continue
            value = matrix[index][column]
            matrix[index] = [
                matrix[index][offset] - value * matrix[pivot_row][offset]
                for offset in range(3)
            ]
        pivot_row += 1
    return tuple(tuple(row) for row in matrix[:pivot_row])


def _difference_rows(mask: int) -> tuple[Vector, ...]:
    indices = _indices(mask)
    root = COMPLEXES[indices[0]]
    return tuple(
        tuple(COMPLEXES[index][coordinate] - root[coordinate] for coordinate in range(3))
        for index in indices[1:]
    )


def positive_active_invariant(mask: int) -> tuple[Fraction, Fraction, Fraction] | None:
    """Return one invariant with positive A and B coefficients, if present."""

    rows = _rref(_difference_rows(mask))
    rank = len(rows)
    if rank == 0:
        return Fraction(1), Fraction(1), Fraction(0)
    if rank == 3:
        return None
    if rank == 1:
        a_value, b_value, c_value = rows[0]
        if c_value:
            return Fraction(1), Fraction(1), -(a_value + b_value) / c_value
        if not a_value and not b_value:
            return Fraction(1), Fraction(1), Fraction(0)
        if a_value * b_value < 0:
            return abs(b_value), abs(a_value), Fraction(0)
        return None
    first, second = rows
    normal = (
        first[1] * second[2] - first[2] * second[1],
        first[2] * second[0] - first[0] * second[2],
        first[0] * second[1] - first[1] * second[0],
    )
    if normal[0] and normal[1] and normal[0] * normal[1] > 0:
        if normal[0] < 0:
            normal = tuple(-entry for entry in normal)
        return normal
    return None


def positive_invariant_shielded_supports() -> frozenset[Support]:
    supports: set[Support] = set()
    for workload, mask in product(WORKLOADS, range(1, 1 << len(NAMES))):
        if mask.bit_count() < 2 or not classify_shielded(mask, workload):
            continue
        if positive_active_invariant(mask) is not None:
            supports.add(_support(mask))
    return frozenset(supports)


def exact_seam_supports() -> frozenset[Support]:
    """Filter positive-invariant shielded supports disjoint from C+{0,A,B}."""

    return frozenset(
        support
        for support in positive_invariant_shielded_supports()
        if AVAILABLE_SUPPORT.isdisjoint(support)
    )


def single_linkage_deficiency(support: Support) -> int:
    mask = sum(1 << NAMES.index(name) for name in support)
    return len(support) - 1 - len(_rref(_difference_rows(mask)))


def falling(population: int, requirement: int) -> int:
    if population < requirement:
        return 0
    result = 1
    for offset in range(requirement):
        result *= population - offset
    return result


def monomial(state: Sequence[int], complex_vector: Sequence[int]) -> int:
    result = 1
    for population, requirement in zip(state, complex_vector):
        result *= falling(population, requirement)
    return result


def reversible_pair_divergence_bound(
    state: Vector,
    source: Vector,
    target: Vector,
    forward_rate: Fraction,
    reverse_rate: Fraction,
) -> Fraction:
    """Right side obtained by applying log(u) <= u-1 to both directions.

    In the interior this is

      reverse * [(x+z-y)_z - (x)_z]
        + forward * [(x+y-z)_y - (x)_y].

    Each bracket is a first finite difference of a degree-at-most-two
    falling-factorial polynomial and is therefore at most affine in x.
    """

    displacement = tuple(target[i] - source[i] for i in range(3))
    forward_target = tuple(state[i] + displacement[i] for i in range(3))
    reverse_target = tuple(state[i] - displacement[i] for i in range(3))
    reverse_after_forward = monomial(forward_target, target)
    reverse_here = monomial(state, target)
    forward_after_reverse = monomial(reverse_target, source)
    forward_here = monomial(state, source)
    return reverse_rate * (reverse_after_forward - reverse_here) + forward_rate * (
        forward_after_reverse - forward_here
    )


def triple_fluid_coefficients(
    edges: Iterable[tuple[int, int, Fraction]],
) -> tuple[Fraction, Fraction, Fraction]:
    """Bernstein coefficients for {2B,A+B,2A}, indexed by A-count 0,1,2."""

    coefficients = [Fraction(), Fraction(), Fraction()]
    for source, target, rate in edges:
        if source == target or source not in (0, 1, 2) or target not in (0, 1, 2):
            raise ValueError("triple edges require distinct indices in {0,1,2}")
        if rate <= 0:
            raise ValueError("rates must be positive")
        coefficients[source] += rate * (target - source)
    return tuple(coefficients)


def autonomous_c_weight(
    parity: int,
    population: int,
    birth_rate: Fraction,
    death_rate: Fraction,
) -> Fraction:
    """Unnormalised stationary weight for 0 <-> 2C on one parity class."""

    if parity not in (0, 1) or population < parity or population % 2 != parity:
        raise ValueError("population must belong to the selected parity class")
    if birth_rate <= 0 or death_rate <= 0:
        raise ValueError("rates must be positive")
    steps = (population - parity) // 2
    numerator = (birth_rate / death_rate) ** steps
    denominator = 1
    for value in range(parity + 1, population + 1):
        denominator *= value
    return numerator / denominator


def residual_busy_period_hazards(population: int) -> tuple[int, int, int]:
    """Return positive, negative, and flat hazards at the residual target.

    Use the unit-rate cycles

    ``B -> 2A -> B+C -> B`` and ``0 -> C -> A -> 0``.

    Starting at ``(A,B,C)=(n,0,0)``, the first ``2A -> B+C`` reaction
    produces ``(n-2,1,1)``.  At that state the three entries returned here
    are the aggregate hazards of reactions that respectively increase,
    decrease, or preserve ``H=A+2B+C``.
    """

    if population < 4:
        raise ValueError("population must be at least four")
    positive = (population - 2) * (population - 3) + 1
    negative = (population - 2) + 1
    flat = 2
    return positive, negative, flat


def certificate() -> dict[str, object]:
    positive = positive_invariant_shielded_supports()
    exact = exact_seam_supports()
    two_vertex = frozenset(support for support in positive if len(support) == 2)
    triple_active = ("2A", "2B", "AB")
    direct_fast = two_vertex | {triple_active}
    deficiency_one = frozenset(
        support for support in positive if single_linkage_deficiency(support) == 1
    )
    return {
        "positive_invariant_shielded_supports": len(positive),
        "two_vertex_supports": len(two_vertex),
        "direct_fast_bound_supports": len(direct_fast),
        "exact_seam_supports": sorted(exact, key=lambda item: (len(item), item)),
        "unsupported_multi_vertex_supports": sorted(
            positive - direct_fast,
            key=lambda item: (len(item), item),
        ),
        "deficiency_one_supports": sorted(deficiency_one),
        "signed_supports": sorted(SIGNED_SUPPORTS, key=lambda item: (len(item), item)),
        "residual_busy_period_regression": {
            "start": "(n,0,0)",
            "actual_target": "(n-2,1,1)",
            "workload": "A+2B+C",
            "interpretation": "next-change service margin tends to the wrong sign",
        },
        "claim_scope": "finite support and algebra interfaces only; not T3-2",
    }


if __name__ == "__main__":
    import json

    print(json.dumps(certificate(), indent=2))
