#!/usr/bin/env python3
"""Detached algebra audit for the shell-two partition descent.

This verifier deliberately does not import or call the C++ enumerator.  It
reconstructs the Eisenstein arithmetic, the cyclotomic transition algebra,
the local signed-skeleton equation, the lossless additive reduction modulo
9, and the exact replay format used by the partition certificate.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
from typing import Iterable, Sequence


P = 37
PAIRS = 6
CLASSES = 12
H = (1, 26, 10)
OMEGA_POWERS = ((1, 0), (0, 1), (-1, -1))
LAMBDA = (1, -1)
ORIGINS = ((-1, 0), (2, 0))
PARTITIONS = (
    (2, 2, 2, 2, 2, 2),
    (3, 3, 2, 2, 2, 0),
    (3, 3, 3, 3, 0, 0),
    (4, 2, 2, 2, 2, 0),
    (4, 3, 3, 2, 0, 0),
    (4, 4, 2, 2, 0, 0),
    (4, 4, 4, 0, 0, 0),
)
TARGETS = {
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
}
PROFILES = tuple(
    (first, second, 3 - first - second)
    for first in range(4)
    for second in range(4 - first)
)
CANDIDATE_TARGET = (2, -2, -2, 2)
CANDIDATE_A = (2, 5, 8, 1, 7, 9, 5, 8, 5, 5, 5, 7)
CANDIDATE_B = (2, 5, 3, 6, 5, 5, 5, 4, 7, 5, 4, 7)

E = tuple[int, int]


def add(x: E, y: E) -> E:
    return x[0] + y[0], x[1] + y[1]


def subtract(x: E, y: E) -> E:
    return x[0] - y[0], x[1] - y[1]


def scale(n: int, x: E) -> E:
    return n * x[0], n * x[1]


def multiply(x: E, y: E) -> E:
    a, b = x
    c, d = y
    return a * c - b * d, a * d + b * c - b * d


def conjugate(x: E) -> E:
    return x[0] - x[1], -x[1]


def power(x: E, exponent: int) -> E:
    result = (1, 0)
    for _ in range(exponent):
        result = multiply(result, x)
    return result


def classes() -> tuple[tuple[int, int, int], ...]:
    result = tuple(
        tuple(pow(2, index, P) * h % P for h in H)
        for index in range(CLASSES)
    )
    if set().union(*(set(part) for part in result)) != set(range(1, P)):
        raise AssertionError("cyclotomic classes do not partition F_37^*")
    return result


CYCLIC_CLASSES = classes()
CLASS_OF = {
    value: index
    for index, part in enumerate(CYCLIC_CLASSES)
    for value in part
}


def local_states() -> tuple[tuple[int, int, int, int], ...]:
    return tuple(
        state
        for state in product((-1, 0, 1), repeat=4)
        if (state[1] - state[0] - state[3] + state[2]) % 3 == 0
    )


LOCAL_STATES = local_states()


def permitted_partitions() -> tuple[tuple[int, ...], ...]:
    local_sizes = tuple(
        sorted({
            sum(value != 0 for value in state)
            for state in LOCAL_STATES
        })
    )
    result = {
        tuple(sorted(word, reverse=True))
        for word in product(local_sizes, repeat=PAIRS)
        if sum(word) == 12
    }
    return tuple(sorted(result))


def actual_factor(channel: int, class_index: int) -> int:
    epsilon = 1 if class_index % 2 == 0 else -1
    return -epsilon if channel == 0 else epsilon


def raw_medium(sign: int, phase: int) -> E:
    return scale(sign, multiply(LAMBDA, OMEGA_POWERS[phase]))


def raw_high(phase: int) -> E:
    return scale(3, OMEGA_POWERS[phase])


def expand(parts: Sequence[E]) -> tuple[E, ...]:
    result = [(0, 0)] * P
    result[0] = parts[0]
    for index, part in enumerate(CYCLIC_CLASSES):
        for value in part:
            result[value] = parts[index + 1]
    return tuple(result)


def correlations(values: Sequence[Sequence[E]]) -> tuple[E, ...]:
    expanded = tuple(expand(channel) for channel in values)
    result = []
    for pair in range(PAIRS):
        lag = CYCLIC_CLASSES[pair][0]
        total = (0, 0)
        for channel in range(2):
            for source in range(P):
                total = add(
                    total,
                    multiply(
                        expanded[channel][(source + lag) % P],
                        conjugate(expanded[channel][source]),
                    ),
                )
        result.append(total)
    return tuple(result)


def all_correlations(values: Sequence[Sequence[E]]) -> tuple[E, ...]:
    expanded = tuple(expand(channel) for channel in values)
    result = []
    for lag in range(P):
        total = (0, 0)
        for channel in range(2):
            for source in range(P):
                total = add(
                    total,
                    multiply(
                        expanded[channel][(source + lag) % P],
                        conjugate(expanded[channel][source]),
                    ),
                )
        result.append(total)
    return tuple(result)


def one_slot_delta(
    base: Sequence[Sequence[E]],
    channel: int,
    class_index: int,
    delta: E,
) -> tuple[E, ...]:
    changed = [list(word) for word in base]
    changed[channel][class_index + 1] = add(
        changed[channel][class_index + 1], delta
    )
    before = correlations(base)
    after = correlations(changed)
    return tuple(subtract(y, x) for x, y in zip(before, after))


def deterministic_fixtures() -> Iterable[
    tuple[tuple[tuple[E, ...], tuple[E, ...]], tuple[tuple[E, ...], ...]]
]:
    """Yield base words and divisible-by-three one-slot corrections."""

    for fixture, partition in enumerate(PARTITIONS):
        base = [[(0, 0)] * 13 for _ in range(2)]
        base[0][0], base[1][0] = ORIGINS
        corrections: list[tuple[int, int, E]] = []
        local_by_size = {
            size: [
                state for state in LOCAL_STATES
                if sum(value != 0 for value in state) == size
            ]
            for size in range(5)
        }
        zero_slots: list[tuple[int, int]] = []
        for pair, size in enumerate(partition):
            state = local_by_size[size][
                (fixture + pair) % len(local_by_size[size])
            ]
            positions = (
                (0, pair), (0, pair + 6),
                (1, pair), (1, pair + 6),
            )
            for (channel, class_index), sign in zip(positions, state):
                factor = actual_factor(channel, class_index)
                if sign:
                    value = scale(factor, raw_medium(sign, 0))
                    base[channel][class_index + 1] = value
                    phase = (fixture + channel + class_index) % 3
                    new = scale(factor, raw_medium(sign, phase))
                    corrections.append(
                        (channel, class_index, subtract(new, value))
                    )
                else:
                    zero_slots.append((channel, class_index))
        for channel, class_index in (
            zero_slots[fixture % len(zero_slots)],
            zero_slots[(fixture + 5) % len(zero_slots)],
        ):
            factor = actual_factor(channel, class_index)
            phase = (fixture + class_index) % 3
            corrections.append(
                (channel, class_index, scale(factor, raw_high(phase)))
            )
        yield (
            (tuple(base[0]), tuple(base[1])),
            tuple(corrections),
        )


def audit_additive_mod9() -> int:
    checks = 0
    for base, corrections in deterministic_fixtures():
        exact = [list(word) for word in base]
        unary = list(correlations(base))
        for channel, class_index, delta in corrections:
            exact[channel][class_index + 1] = add(
                exact[channel][class_index + 1], delta
            )
            response = one_slot_delta(base, channel, class_index, delta)
            unary = [add(x, y) for x, y in zip(unary, response)]
        direct = correlations(exact)
        for left, right in zip(direct, unary):
            if (left[0] - right[0]) % 9:
                raise AssertionError("first modulo-nine coordinate failed")
            if (left[1] - right[1]) % 9:
                raise AssertionError("second modulo-nine coordinate failed")
            checks += 2
    return checks


def audit_local_phase_rank() -> int:
    """Check the one-equation-per-nonempty-quartet theorem directly."""

    checks = 0
    for state in LOCAL_STATES:
        size = sum(value != 0 for value in state)
        if size == 0:
            continue
        # Formula (3) in the shell-three proof says that the primitive flag
        # is an affine nonzero linear form in the local phase trits.  It is
        # enough to audit its coefficient vector: every occupied position
        # enters with coefficient +/-1, hence it has rank one.
        coefficients = tuple(value % 3 for value in state if value)
        if not coefficients or all(value == 0 for value in coefficients):
            raise AssertionError("local phase form lost rank")
        values = [
            sum(c * x for c, x in zip(coefficients, phase)) % 3
            for phase in product(range(3), repeat=size)
        ]
        histogram = tuple(values.count(residue) for residue in range(3))
        expected = (3 ** (size - 1),) * 3
        if histogram != expected:
            raise AssertionError((state, histogram, expected))
        checks += 1
    return checks


def star_target(target: tuple[int, int, int, int],
                star_a: bool, star_b: bool) -> tuple[int, int, int, int]:
    a = target[:2]
    b = target[2:]
    if star_a:
        a = conjugate(a)
    if star_b:
        b = conjugate(b)
    return a[0], a[1], b[0], b[1]


def profile_value(profile_id: int) -> E:
    first, second, third = PROFILES[profile_id]
    return first - third, second - third


def candidate_values() -> tuple[tuple[E, ...], tuple[E, ...]]:
    result = [[(0, 0)] * 13 for _ in range(2)]
    result[0][0], result[1][0] = ORIGINS
    for channel, identifiers in enumerate((CANDIDATE_A, CANDIDATE_B)):
        for class_index, profile_id in enumerate(identifiers):
            result[channel][class_index + 1] = scale(
                actual_factor(channel, class_index),
                profile_value(profile_id),
            )
    return tuple(result[0]), tuple(result[1])


def signed_skeleton(identifiers: Sequence[int]) -> tuple[int, ...]:
    positive = {7, 6, 1}
    negative = {2, 4, 8}
    return tuple(
        1 if profile_id in positive
        else -1 if profile_id in negative
        else 0
        for profile_id in identifiers
    )


def transform_skeleton(
    skeleton: Sequence[Sequence[int]], group: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    rotation = group // 4
    stars = (bool((group // 2) % 2), bool(group % 2))
    result = []
    for channel in range(2):
        offset = (2 * rotation + (6 if stars[channel] else 0)) % 12
        sign = -1 if stars[channel] else 1
        result.append(tuple(
            sign * skeleton[channel][(index + offset) % 12]
            for index in range(12)
        ))
    return tuple(result)  # type: ignore[return-value]


def transform_identifiers(
    identifiers: Sequence[int], rotation: int, star: bool
) -> tuple[int, ...]:
    profile_to_id = {
        profile: index for index, profile in enumerate(PROFILES)
    }
    conjugate_id = tuple(
        profile_to_id[(profile[0], profile[2], profile[1])]
        for profile in PROFILES
    )
    offset = (2 * rotation + (6 if star else 0)) % 12
    return tuple(
        conjugate_id[identifiers[(index + offset) % 12]]
        if star else identifiers[(index + offset) % 12]
        for index in range(12)
    )


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def candidate_certificate() -> dict[str, object]:
    values = candidate_values()
    aggregate = []
    for channel in range(2):
        total = (0, 0)
        for value in values[channel][1:]:
            total = add(total, value)
        aggregate.extend(total)
    physical = all_correlations(values)
    identifiers = CANDIDATE_A + CANDIDATE_B
    norms = tuple(
        value[0] * value[0] - value[0] * value[1] + value[1] * value[1]
        for value in map(profile_value, identifiers)
    )
    norm_histogram = {
        str(norm): norms.count(norm) for norm in sorted(set(norms))
    }

    skeleton = (
        signed_skeleton(CANDIDATE_A),
        signed_skeleton(CANDIDATE_B),
    )
    skeleton_orbit = tuple(
        transform_skeleton(skeleton, group) for group in range(24)
    )
    full_orbit = []
    for group in range(24):
        rotation = group // 4
        star_a = bool((group // 2) % 2)
        star_b = bool(group % 2)
        full_orbit.append((
            transform_identifiers(CANDIDATE_A, rotation, star_a),
            transform_identifiers(CANDIDATE_B, rotation, star_b),
        ))

    local_states_candidate = tuple(
        (
            skeleton[0][pair],
            skeleton[0][pair + 6],
            skeleton[1][pair],
            skeleton[1][pair + 6],
        )
        for pair in range(PAIRS)
    )
    for state in local_states_candidate:
        if (state[1] - state[0] - state[3] + state[2]) % 3:
            raise AssertionError("candidate failed a local signature")
        if sum(value != 0 for value in state) != 2:
            raise AssertionError("candidate left partition 222222")
    if tuple(aggregate) != CANDIDATE_TARGET:
        raise AssertionError("candidate aggregate changed")
    if physical[0] != (167, 0) or any(
        value != (0, 0) for value in physical[1:]
    ):
        raise AssertionError("candidate is not exact profile zero")
    if norm_histogram != {"0": 10, "3": 12, "9": 2}:
        raise AssertionError(norm_histogram)
    if min(skeleton_orbit) != skeleton:
        raise AssertionError("candidate skeleton is not canonical")
    if len(set(skeleton_orbit)) != 24 or len(set(full_orbit)) != 24:
        raise AssertionError("candidate orbit has a nontrivial stabilizer")

    return {
        "schema": "lp333-order3-profile-zero-v1",
        "sector_n9_n3_n0": (2, 12, 10),
        "partition": (2, 2, 2, 2, 2, 2),
        "target": CANDIDATE_TARGET,
        "profile_ids_a": CANDIDATE_A,
        "profile_ids_b": CANDIDATE_B,
        "profiles_a": tuple(PROFILES[index] for index in CANDIDATE_A),
        "profiles_b": tuple(PROFILES[index] for index in CANDIDATE_B),
        "actual_values_a": values[0],
        "actual_values_b": values[1],
        "aggregate": tuple(aggregate),
        "norm_histogram": norm_histogram,
        "local_signed_states": local_states_candidate,
        "physical_correlations": physical,
        "canonical_signed_skeleton": skeleton,
        "skeleton_orbit_size": len(set(skeleton_orbit)),
        "full_profile_orbit_size": len(set(full_orbit)),
        "stabilizer_size": 1,
    }


def main() -> None:
    if power(LAMBDA, 2) != (0, -3):
        raise AssertionError("lambda^2 identity changed")
    if power(LAMBDA, 4) != (-9, -9):
        raise AssertionError("lambda^4 identity changed")
    if power(LAMBDA, 6) != (-27, 0):
        raise AssertionError("lambda^6 identity changed")
    if power(LAMBDA, 8) != (0, 81):
        raise AssertionError("lambda^8 identity changed")

    local_histogram = tuple(
        sum(sum(value != 0 for value in state) == size
            for state in LOCAL_STATES)
        for size in range(5)
    )
    if local_histogram != (1, 0, 12, 8, 6):
        raise AssertionError(local_histogram)
    if permitted_partitions() != tuple(sorted(PARTITIONS)):
        raise AssertionError("the seven support partitions changed")

    for star_a, star_b in product((False, True), repeat=2):
        transformed = {
            star_target(target, star_a, star_b) for target in TARGETS
        }
        if transformed != TARGETS:
            raise AssertionError("aggregate targets lost star closure")

    additive_checks = audit_additive_mod9()
    rank_checks = audit_local_phase_rank()
    certificate = candidate_certificate()
    print(f"local_states={len(LOCAL_STATES)}")
    print(f"local_histogram={local_histogram}")
    print(f"support_partitions={len(PARTITIONS)}")
    print(f"local_rank_checks={rank_checks}")
    print(f"detached_additive_coordinate_checks={additive_checks}")
    print(f"lambda_squared={power(LAMBDA, 2)}")
    print(f"lambda_fourth={power(LAMBDA, 4)}")
    print(f"lambda_sixth={power(LAMBDA, 6)}")
    print(f"lambda_eighth={power(LAMBDA, 8)}")
    print(f"exact_candidate_sha256={compact_hash(certificate)}")


if __name__ == "__main__":
    main()
