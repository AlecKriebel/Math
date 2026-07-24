#!/usr/bin/env python3
"""Verify and expose the characteristic-two order-three profile quotient.

The public entry point for dense-shell code is ``check_profile_assignment``.
Class coefficients use the encoding

    0, 1, w, 1+w  <->  0, 1, 2, 3

for F_4=F_2[w]/(w^2+w+1).  The twelve class positions are the H-orbits
2^j H, 0 <= j < 12, where H={1,10,26} in F_37^*.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
from typing import Sequence


P = 37
H = (1, 10, 26)
CLASS_COUNT = 12
CERTIFICATE = Path(__file__).with_name("char2_profile_census.json")
EXACT_AGGREGATE_TARGETS = (
    (-3, -3, -4, -2), (-3, -3, -2, 2),
    (-3, 0, -3, -3), (-3, 0, 0, 3),
    (-1, -2, -5, -1), (-1, -2, -4, 1),
    (0, 3, -4, -2), (0, 3, -2, 2),
    (1, -1, 2, -2), (1, -1, 4, 2),
    (1, 2, -5, -1), (1, 2, -4, 1),
    (2, -2, -4, -2), (2, -2, -2, 2),
    (2, 1, 2, -2), (2, 1, 4, 2),
    (3, 0, 0, -3), (3, 0, 3, 3),
    (4, -1, 0, 0), (4, 2, -4, -2),
    (4, 2, -2, 2), (5, 1, 0, 0),
)
EXPECTED_MATCHES = {
    (3, 0): (1_591_338_552, 966_197_016, 286_163_712),
    (1, 3): (1_591_301_760, 966_296_568, 286_154_784),
    (1, 2): (1_591_301_760, 966_296_568, 286_154_784),
    (2, 0): (1_591_338_552, 966_197_016, 286_163_712),
    (0, 0): (1_591_802_496, 966_019_275, 286_244_568),
}


def f4_multiply(left: int, right: int) -> int:
    """Multiply two encoded elements of F_4."""

    if not 0 <= left < 4 or not 0 <= right < 4:
        raise ValueError("an F_4 element must lie in 0..3")
    a, b = left & 1, left >> 1
    c, d = right & 1, right >> 1
    return (a * c ^ b * d) | (
        (a * d ^ b * c ^ b * d) << 1
    )


def f4_square(value: int) -> int:
    return f4_multiply(value, value)


def f4_trace(value: int) -> int:
    """Return Tr_{F_4/F_2}(value), encoded as 0 or 1."""

    result = value ^ f4_square(value)
    if result not in (0, 1):
        raise AssertionError("the F_4 trace left F_2")
    return result


def cyclotomic_classes() -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...]]:
    classes = []
    class_of = [-1] * P
    power = 1
    for _ in range(CLASS_COUNT):
        orbit = tuple(sorted(power * member % P for member in H))
        classes.append(orbit)
        for value in orbit:
            if class_of[value] != -1:
                raise AssertionError("the H-orbits overlap")
            class_of[value] = len(classes) - 1
        power = 2 * power % P
    if set().union(*(set(orbit) for orbit in classes)) != set(range(1, P)):
        raise AssertionError("the H-orbits do not cover F_37^*")
    return tuple(classes), tuple(class_of)


CLASSES, CLASS_OF = cyclotomic_classes()


def reduce_eisenstein(value: Sequence[int]) -> int:
    """Reduce a+b*omega in Z[omega] modulo 2."""

    if len(value) != 2:
        raise ValueError("an Eisenstein coefficient needs two coordinates")
    return (int(value[0]) & 1) | ((int(value[1]) & 1) << 1)


def reduce_aggregate_target(
    target: Sequence[int],
) -> tuple[int, int]:
    """Reduce one exact four-coordinate aggregate target modulo two."""

    if len(target) != 4:
        raise ValueError("an aggregate target needs four integer coordinates")
    return reduce_eisenstein(target[:2]), reduce_eisenstein(target[2:])


def expand_class_word(origin: int, coefficients: Sequence[int]) -> tuple[int, ...]:
    if len(coefficients) != CLASS_COUNT:
        raise ValueError("a class word needs twelve coefficients")
    if not 0 <= origin < 4 or any(not 0 <= int(x) < 4 for x in coefficients):
        raise ValueError("all coefficients must lie in F_4")
    word = [0] * P
    word[0] = int(origin)
    for index, orbit in enumerate(CLASSES):
        for position in orbit:
            word[position] = int(coefficients[index])
    return tuple(word)


def channel_signature(
    origin: int, coefficients: Sequence[int]
) -> tuple[int, ...]:
    """Return the six reversal-independent nonzero coefficients of U U*."""

    word = expand_class_word(origin, coefficients)
    result = []
    for lag_class in range(6):
        lag = CLASSES[lag_class][0]
        value = 0
        for source in range(P):
            value ^= f4_multiply(
                word[(source + lag) % P],
                f4_square(word[source]),
            )
        result.append(value)
    return tuple(result)


def residual_signature(
    coefficients_a: Sequence[int],
    coefficients_b: Sequence[int],
) -> tuple[int, ...]:
    """Return the nonzero-lag residual for origins A(0)=1, B(0)=0."""

    left = channel_signature(1, coefficients_a)
    right = channel_signature(0, coefficients_b)
    return tuple(a ^ b for a, b in zip(left, right))


def class_aggregate(coefficients: Sequence[int]) -> int:
    result = 0
    for value in coefficients:
        result ^= int(value)
    return result


def support_size(coefficients: Sequence[int]) -> int:
    return sum(int(value) != 0 for value in coefficients)


def signature_trace_dependency(signature: Sequence[int]) -> int:
    """The forced one-bit dependency on the six F_4 residual coordinates."""

    if len(signature) != 6:
        raise ValueError("a residual signature needs six F_4 coordinates")
    result = 0
    for value in signature:
        result ^= f4_trace(int(value))
    return result


def check_profile_assignment(
    coefficients_a: Sequence[int],
    coefficients_b: Sequence[int],
    *,
    target_aggregate: tuple[int, int] | None = None,
    high_count: int | None = None,
) -> dict[str, object]:
    """Test one actual reduced profile assignment.

    ``target_aggregate`` is the pair of twelve-class coefficient sums, not
    the full augmentations.  ``high_count=h`` optionally pins total support
    ``18-2h`` for h=0,1,2.
    """

    if len(coefficients_a) != CLASS_COUNT or len(coefficients_b) != CLASS_COUNT:
        raise ValueError("each channel needs twelve class coefficients")
    a = tuple(map(int, coefficients_a))
    b = tuple(map(int, coefficients_b))
    if target_aggregate is not None and (
        len(target_aggregate) != 2
        or any(not 0 <= int(value) < 4 for value in target_aggregate)
    ):
        raise ValueError("a reduced aggregate target needs two F_4 elements")
    if high_count is not None and high_count not in (0, 1, 2):
        raise ValueError("the dense profile shell has high count 0, 1, or 2")
    signature = residual_signature(a, b)
    aggregate = (class_aggregate(a), class_aggregate(b))
    support = support_size(a) + support_size(b)
    nonzero_lags_hold = not any(signature)
    zero_lag_holds = support % 2 == 0
    full_aggregate_a = 1 ^ aggregate[0]
    full_aggregate_b = aggregate[1]
    trivial_factor_holds = (
        f4_multiply(full_aggregate_a, f4_square(full_aggregate_a))
        ^ f4_multiply(full_aggregate_b, f4_square(full_aggregate_b))
    ) == 1
    unitary_holds = (
        nonzero_lags_hold and zero_lag_holds and trivial_factor_holds
    )
    aggregate_ok = target_aggregate is None or aggregate == target_aggregate
    support_ok = high_count is None or support == 18 - 2 * high_count
    return {
        "passes_unitary_quotient": unitary_holds,
        "nonzero_lags_hold": nonzero_lags_hold,
        "zero_lag_holds": zero_lag_holds,
        "trivial_factor_holds": trivial_factor_holds,
        "target_aggregate_holds": aggregate_ok,
        "shell_support_holds": support_ok,
        "passes_all_requested_gates": (
            unitary_holds and aggregate_ok and support_ok
        ),
        "aggregate": aggregate,
        "total_support": support,
        "residual_signature": signature,
        "trace_dependency": signature_trace_dependency(signature),
    }


def check_eisenstein_profile(
    coefficients_a: Sequence[Sequence[int]],
    coefficients_b: Sequence[Sequence[int]],
    **kwargs: object,
) -> dict[str, object]:
    """Reduce two twelve-class Z[omega] words and apply the quotient gate."""

    return check_profile_assignment(
        tuple(reduce_eisenstein(value) for value in coefficients_a),
        tuple(reduce_eisenstein(value) for value in coefficients_b),
        **kwargs,
    )


def factor_audit() -> dict[str, object]:
    """Reconstruct the two Frobenius orbits and the star action on them."""

    # F_37^*/H is cyclic of order 12, labelled by exponents j modulo 12.
    # Fourth-power Frobenius adds two; the two cycles are parity classes.
    unseen = set(range(12))
    cycles = []
    while unseen:
        start = min(unseen)
        cycle = []
        value = start
        while value not in cycle:
            cycle.append(value)
            unseen.remove(value)
            value = (value + 2) % 12
        cycles.append(tuple(cycle))
    if cycles != [
        (0, 2, 4, 6, 8, 10),
        (1, 3, 5, 7, 9, 11),
    ]:
        raise AssertionError("the fourth-power character orbits changed")

    # Fourier star sends k to -k/2 before coefficient squaring.  Since
    # -1/2=2^17 modulo 37, it sends class j to j+5.  With coordinates at
    # j=0 and j=1 this yields (X,Y)^*=(Y^32,X^128).
    star_classes = tuple((index + 5) % 12 for index in range(12))
    if any((star_classes[index] - index) % 12 != 5 for index in range(12)):
        raise AssertionError("the Fourier star class shift changed")
    if any((star_classes[index] - index) % 2 != 1 for index in range(12)):
        raise AssertionError("Fourier star no longer exchanges the factors")
    field_order = 4**6
    if pow(2, 5) != 32 or pow(2, 7) != 128:
        raise AssertionError("the star exponents changed")
    if (32 * 128) % (field_order - 1) != 1:
        raise AssertionError("the two semilinear star exponents are not inverse")
    return {
        "algebra": "F_4 x F_(4^6) x F_(4^6)",
        "frobenius_cycles": tuple(cycles),
        "star_class_shift": 5,
        "star_coordinates": "(a,X,Y)^*=(a^2,Y^32,X^128)",
        "nontrivial_norm_equation": (
            "X_A*Y_A^32 + X_B*Y_B^32 = 1 in F_(4^6)"
        ),
    }


def unconstrained_pair_count(
    aggregate_a: int, aggregate_b: int, total_support: int
) -> int:
    """Count words with only the aggregate and total-support data pinned."""

    channel: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(CLASS_COUNT):
        updated: dict[tuple[int, int], int] = defaultdict(int)
        for (support, aggregate), count in channel.items():
            updated[support, aggregate] += count
            for value in (1, 2, 3):
                updated[support + 1, aggregate ^ value] += count
        channel = updated
    return sum(
        channel.get((left_support, aggregate_a), 0)
        * channel.get((total_support - left_support, aggregate_b), 0)
        for left_support in range(CLASS_COUNT + 1)
    )


def verify_certificate() -> dict[str, object]:
    stored = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if stored["schema"] != "lp333-order3-char2-profile-census-v1":
        raise AssertionError("the characteristic-two certificate schema changed")
    if stored["factorization"]["algebra"] != factor_audit()["algebra"]:
        raise AssertionError("the stored factorization changed")
    expected_multiplicities = Counter(
        reduce_aggregate_target(target) for target in EXACT_AGGREGATE_TARGETS
    )
    expected_shells = {(0, 18, 18), (1, 15, 16), (2, 12, 14)}
    actual_shells = {
        (
            int(shell["high_count"]),
            int(shell["medium_count"]),
            int(shell["total_support"]),
        )
        for shell in stored["shells"]
    }
    if len(stored["shells"]) != 3 or actual_shells != expected_shells:
        raise AssertionError("the three dense profile shells changed")
    actual_aggregates = {
        tuple(map(int, record["aggregate"]))
        for record in stored["target_residue_types"]
    }
    if (
        len(stored["target_residue_types"]) != len(EXPECTED_MATCHES)
        or actual_aggregates != set(EXPECTED_MATCHES)
    ):
        raise AssertionError("the five reduced aggregate types changed")
    target_total = 0
    for record in stored["target_residue_types"]:
        aggregate = tuple(map(int, record["aggregate"]))
        target_total += int(record["multiplicity"])
        if int(record["multiplicity"]) != expected_multiplicities[aggregate]:
            raise AssertionError("an exact target multiplicity changed")
        full_a = 1 ^ aggregate[0]
        full_b = aggregate[1]
        if f4_multiply(full_a, f4_square(full_a)) ^ f4_multiply(
            full_b, f4_square(full_b)
        ) != 1:
            raise AssertionError("a target violates the trivial-factor norm")
        for shell in stored["shells"]:
            high = int(shell["high_count"])
            census = int(record["matches"][f"h{high}"])
            if census != EXPECTED_MATCHES[aggregate][high]:
                raise AssertionError("a pinned quotient census changed")
            ambient = unconstrained_pair_count(
                aggregate[0], aggregate[1], 18 - 2 * high
            )
            if ambient != int(record["ambient"][f"h{high}"]):
                raise AssertionError("an ambient census changed")
            if not 0 < census < ambient:
                raise AssertionError("a quotient census is not a strict survivor")
    if target_total != len(EXACT_AGGREGATE_TARGETS):
        raise AssertionError("the 22 exact aggregate targets are not covered")
    measurement = stored["computation"]["reference_measurement"]
    if float(measurement["wall_seconds"]) >= 10 * 60:
        raise AssertionError("the reference census exceeds its time budget")
    if int(measurement["maximum_resident_bytes"]) >= 4 * 1024**3:
        raise AssertionError("the reference census exceeds its memory budget")
    return stored


def main() -> None:
    certificate = verify_certificate()
    factor = factor_audit()
    zero = (0,) * CLASS_COUNT
    trivial = check_profile_assignment(zero, zero)
    if not trivial["passes_unitary_quotient"]:
        raise AssertionError("the delta-origin fixture failed")
    print(f"factorization={factor['algebra']}")
    print(f"star={factor['star_coordinates']}")
    print(f"target_residue_types={len(certificate['target_residue_types'])}")
    print("exact_target_multiplicity=22")
    print("PASS: characteristic-two profile quotient and certificate verified")


if __name__ == "__main__":
    main()
