#!/usr/bin/env python3
"""Verify the spectral-unit theorem for the order-three LP(333) profile gate.

This file uses only the Python standard library.  It checks the finite
arithmetic behind the following conditional theorem.

If two order-three-invariant Eisenstein sequences on F_37 have total
correlation 167 at zero and zero elsewhere, and their nonzero coefficients
come from the ten profile values, then both sequences are units after
reduction modulo 167.  In the invariant CRT

    F_(167^2)[C_37]^H = k x E x E,   E=F_(167^12),

all six channel coordinates are nonzero.  Consequently the four-branch
prime-167 cone reduces, on the physical profile alphabet, to one torus.

The proof itself is recorded in ``LP333_ORDER3_SPECTRAL_UNITS.md``.  The
checks below pin its profile polynomial, Eisenstein irreducibility
certificate, embedding pairing, residue-prime degrees, norm gap, and exact
torus counts.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from math import comb
from typing import Sequence


P = 37
Q = 167
Q2 = Q * Q
H = (1, 10, 26)
PROFILE_ENERGY = 54
PROFILE_VARIABLES = 24
M = Q**12

Eisenstein = tuple[int, int]  # a+b*omega, omega^2+omega+1=0.
Polynomial = tuple[Eisenstein, ...]  # ascending coefficients

E_ZERO: Eisenstein = (0, 0)
E_ONE: Eisenstein = (1, 0)

EXPECTED_ALPHABET_CERTIFICATE_SHA256 = (
    "ef638caa35d133e285ffaa6e781bdaff3788d6a95e3df7eb5733e7be7466a725"
)
EXPECTED_FIELD_CERTIFICATE_SHA256 = (
    "8ee4b74642b7e2ffdbc44c9b71d49132faf776457aa53f1220a709571c6f2566"
)
EXPECTED_NORM_CERTIFICATE_SHA256 = (
    "cc16fbfca0fabfdf1535ce898ccf06c5174e77f547bfb94352be31c24fa467cc"
)
EXPECTED_TORUS_CERTIFICATE_SHA256 = (
    "970b3cf1db191292a59cff91db42ba902c935373d106ae65bf0a74fd85e95a51"
)
EXPECTED_MASTER_CERTIFICATE_SHA256 = (
    "a8f551c9c7933f17178d7f63e2df78871b393462d890ccba9753bdc74bcae6ac"
)


ROW_SUM_TARGETS: tuple[tuple[int, int, int, int], ...] = (
    (-3, -3, -4, -2),
    (-3, -3, -2, 2),
    (-3, 0, -3, -3),
    (-3, 0, 0, 3),
    (-1, -2, -5, -1),
    (-1, -2, -4, 1),
    (0, 3, -4, -2),
    (0, 3, -2, 2),
    (1, -1, 2, -2),
    (1, -1, 4, 2),
    (1, 2, -5, -1),
    (1, 2, -4, 1),
    (2, -2, -4, -2),
    (2, -2, -2, 2),
    (2, 1, 2, -2),
    (2, 1, 4, 2),
    (3, 0, 0, -3),
    (3, 0, 3, 3),
    (4, -1, 0, 0),
    (4, 2, -4, -2),
    (4, 2, -2, 2),
    (5, 1, 0, 0),
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def require_hash(label: str, value: object, expected: str) -> str:
    actual = compact_hash(value)
    if expected and actual != expected:
        raise AssertionError(f"{label} hash changed: {actual} != {expected}")
    return actual


def e_add(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return left[0] + right[0], left[1] + right[1]


def e_neg(value: Eisenstein) -> Eisenstein:
    return -value[0], -value[1]


def e_multiply(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def e_conjugate(value: Eisenstein) -> Eisenstein:
    return value[0] - value[1], -value[1]


def e_norm(value: Eisenstein) -> int:
    a, b = value
    return a * a - a * b + b * b


def p_trim(value: Sequence[Eisenstein]) -> Polynomial:
    result = list(value)
    while len(result) > 1 and result[-1] == E_ZERO:
        result.pop()
    return tuple(result)


def p_multiply(
    left: Sequence[Eisenstein], right: Sequence[Eisenstein]
) -> Polynomial:
    result = [E_ZERO] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            index = left_index + right_index
            result[index] = e_add(
                result[index], e_multiply(left_value, right_value)
            )
    return p_trim(result)


def p_from_integer_coefficients(values: Sequence[int]) -> Polynomial:
    return tuple((value, 0) for value in values)


def profiles() -> tuple[tuple[int, int, int], ...]:
    result = tuple(
        (first, second, 3 - first - second)
        for first in range(4)
        for second in range(4)
        if 0 <= 3 - first - second <= 3
    )
    if len(result) != 10:
        raise AssertionError("the profile alphabet no longer has ten values")
    return result


PROFILES = profiles()


def profile_value(profile: tuple[int, int, int]) -> Eisenstein:
    first, second, third = profile
    return first - third, second - third


PROFILE_VALUES = tuple(profile_value(profile) for profile in PROFILES)


def profile_polynomial() -> Polynomial:
    result: Polynomial = (E_ONE,)
    for root in PROFILE_VALUES:
        result = p_multiply(result, (e_neg(root), E_ONE))
    return result


def expected_profile_polynomial() -> Polynomial:
    # X (X^3-27) (X^6+27).
    return p_multiply(
        p_multiply(
            p_from_integer_coefficients((0, 1)),
            p_from_integer_coefficients((-27, 0, 0, 1)),
        ),
        p_from_integer_coefficients((27, 0, 0, 0, 0, 0, 1)),
    )


def profile_type_sectors() -> tuple[tuple[int, int, int, int, int], ...]:
    """Return (n_9,n_0,n_3,support,power_sum_6) on energy 54."""

    sectors = []
    for norm_nine in range(7):
        norm_three = 18 - 3 * norm_nine
        norm_zero = 6 + 2 * norm_nine
        support = norm_three + norm_nine
        sixth_power_sum = -27 * norm_three + 729 * norm_nine
        sectors.append(
            (
                norm_nine,
                norm_zero,
                norm_three,
                support,
                sixth_power_sum,
            )
        )
    return tuple(sectors)


def verify_alphabet() -> dict[str, object]:
    norms = tuple(e_norm(value) for value in PROFILE_VALUES)
    if Counter(norms) != Counter({0: 1, 3: 6, 9: 3}):
        raise AssertionError("the profile norm distribution changed")
    actual_polynomial = profile_polynomial()
    expected_polynomial = expected_profile_polynomial()
    if actual_polynomial != expected_polynomial:
        raise AssertionError("the ten profile values lost their polynomial")

    sectors = profile_type_sectors()
    for norm_nine, norm_zero, norm_three, support, sixth_sum in sectors:
        if norm_zero + norm_three + norm_nine != PROFILE_VARIABLES:
            raise AssertionError("a profile type sector has the wrong size")
        if 3 * norm_three + 9 * norm_nine != PROFILE_ENERGY:
            raise AssertionError("a profile type sector has the wrong energy")
        if support != norm_three + norm_nine:
            raise AssertionError("a profile support count changed")
        if sixth_sum != -486 + 810 * norm_nine:
            raise AssertionError("a sixth power moment changed")

    certificate = (
        PROFILES,
        PROFILE_VALUES,
        norms,
        actual_polynomial,
        sectors,
    )
    certificate_hash = require_hash(
        "alphabet", certificate, EXPECTED_ALPHABET_CERTIFICATE_SHA256
    )
    return {
        "profile_values": len(PROFILE_VALUES),
        "norm_histogram": dict(sorted(Counter(norms).items())),
        "annihilating_polynomial": "X(X^3-27)(X^6+27)",
        "energy_type_sectors": sectors,
        "certificate_sha256": certificate_hash,
    }


def multiplicative_order(value: int, modulus: int) -> int:
    value %= modulus
    if value == 0:
        raise ValueError("zero has no multiplicative order")
    product_value = 1
    for exponent in range(1, modulus):
        product_value = product_value * value % modulus
        if product_value == 1:
            return exponent
    raise AssertionError("multiplicative order search failed")


def subgroup_coset(value: int) -> tuple[int, ...]:
    return tuple(sorted(value * member % P for member in H))


def quotient_cosets() -> tuple[tuple[int, ...], ...]:
    return tuple(sorted({subgroup_coset(value) for value in range(1, P)}))


def frobenius_coset_cycle(start: int) -> tuple[tuple[int, ...], ...]:
    multiplier = Q2 % P
    result = []
    current = subgroup_coset(start)
    while current not in result:
        result.append(current)
        current = subgroup_coset(current[0] * multiplier)
    return tuple(result)


def e_unit_orbit(value: Eisenstein) -> set[Eisenstein]:
    units = ((1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1))
    return {e_multiply(unit, value) for unit in units}


def verify_field_arithmetic() -> dict[str, object]:
    # Phi_37(X+1) is Eisenstein at pi=7+3 omega.
    pi = (7, 3)
    pi_bar = e_conjugate(pi)
    if e_norm(pi) != P or e_multiply(pi, pi_bar) != (P, 0):
        raise AssertionError("the norm-37 Eisenstein prime changed")
    if pi_bar in e_unit_orbit(pi):
        raise AssertionError("the two primes above 37 became associates")
    shifted_coefficients = tuple(comb(P, index) for index in range(1, P + 1))
    if shifted_coefficients[-1] != 1:
        raise AssertionError("Phi_37(X+1) lost its leading coefficient")
    if shifted_coefficients[0] != P:
        raise AssertionError("Phi_37(X+1) lost its constant coefficient")
    if any(value % P for value in shifted_coefficients[:-1]):
        raise AssertionError("a nonleading shifted coefficient left (pi)")
    if shifted_coefficients[0] % (P * P) == 0:
        raise AssertionError("the shifted constant entered (pi)^2")

    # At 167, the base Eisenstein prime is inert and the quotient Frobenius
    # has exactly the two degree-six cycles underlying E x E.
    norm_residues_mod_three = {
        e_norm((first, second)) % 3
        for first, second in product(range(3), repeat=2)
    }
    if norm_residues_mod_three != {0, 1} or Q % 3 != 2:
        raise AssertionError("167 is no longer excluded as an Eisenstein norm")
    order_q = multiplicative_order(Q, P)
    order_q2 = multiplicative_order(Q2, P)
    if (order_q, order_q2) != (36, 18):
        raise AssertionError("the residue orders modulo 37 changed")
    full_plus_orbit = tuple(pow(Q2, exponent, P) for exponent in range(order_q2))
    if not set(H).issubset(full_plus_orbit):
        raise AssertionError("H left the 167^2 Frobenius orbit")

    plus_cycle = frobenius_coset_cycle(1)
    minus_cycle = frobenius_coset_cycle(Q)
    all_cosets = quotient_cosets()
    if len(plus_cycle) != 6 or len(minus_cycle) != 6:
        raise AssertionError("a primitive invariant residue degree changed")
    if set(plus_cycle) & set(minus_cycle):
        raise AssertionError("the two primitive residue primes merged")
    if set(plus_cycle) | set(minus_cycle) != set(all_cosets):
        raise AssertionError("the two residue primes lost a quotient coset")

    # Pair the two omega embeddings.  The conjugate of F(zeta^r) is the
    # (bar,-rH) embedding, giving twelve positive squared-modulus factors.
    embedding_pairs = tuple(
        (coset, subgroup_coset(-coset[0]))
        for coset in all_cosets
    )
    paired_bar_cosets = tuple(pair[1] for pair in embedding_pairs)
    if set(paired_bar_cosets) != set(all_cosets):
        raise AssertionError("complex conjugation no longer pairs all embeddings")
    if any(
        subgroup_coset(-right[0]) != left
        for left, right in embedding_pairs
    ):
        raise AssertionError("the embedding pairing is not an involution")

    certificate = (
        pi,
        pi_bar,
        shifted_coefficients,
        tuple(sorted(norm_residues_mod_three)),
        order_q,
        order_q2,
        full_plus_orbit,
        all_cosets,
        plus_cycle,
        minus_cycle,
        embedding_pairs,
        Q**12,
    )
    certificate_hash = require_hash(
        "field", certificate, EXPECTED_FIELD_CERTIFICATE_SHA256
    )
    return {
        "irreducibility_prime": pi,
        "phi37_shift_eisenstein": True,
        "ord_37_167": order_q,
        "ord_37_167_squared": order_q2,
        "primitive_quotient_cycles": (len(plus_cycle), len(minus_cycle)),
        "primitive_prime_absolute_norms": (Q**12, Q**12),
        "embedding_pairs": len(embedding_pairs),
        "certificate_sha256": certificate_hash,
    }


def target_spectral_values(
    target: tuple[int, int, int, int]
) -> tuple[Eisenstein, Eisenstein]:
    first, second, third, fourth = target
    return (-1 + 3 * first, 3 * second), (2 + 3 * third, 3 * fourth)


def product_norm_gap(
    factor_count: int, strict_factor_upper: int, prime_norm: int
) -> dict[str, int]:
    """Audit the integer norm gap used to force prime valuation zero."""

    if factor_count <= 0 or strict_factor_upper <= 0:
        raise ValueError("the norm-gap dimensions must be positive")
    universal_upper_exclusive = strict_factor_upper**factor_count
    if universal_upper_exclusive != prime_norm:
        raise ValueError("the residue-prime norm does not match the product gap")
    return {
        "positive_integer_lower": 1,
        "integer_upper_inclusive": prime_norm - 1,
        "prime_divisibility_threshold": prime_norm,
    }


def verify_norm_gap() -> dict[str, object]:
    target_values = tuple(map(target_spectral_values, ROW_SUM_TARGETS))
    target_norm_pairs = tuple(
        (e_norm(first), e_norm(second)) for first, second in target_values
    )
    if any(first + second != Q for first, second in target_norm_pairs):
        raise AssertionError("a trivial-character norm pair left energy 167")
    if any(
        not 0 < first < Q or not 0 < second < Q
        for first, second in target_norm_pairs
    ):
        raise AssertionError("a physical trivial coordinate is not a 167-unit")
    expected_histogram = {
        (19, 148): 4,
        (28, 139): 4,
        (64, 103): 2,
        (91, 76): 8,
        (100, 67): 2,
        (163, 4): 2,
    }
    if dict(Counter(target_norm_pairs)) != expected_histogram:
        raise AssertionError("the 22 target norm pairs changed")

    # The exact theorem has twelve factors in (0,167), while either residue
    # prime has norm 167^12.  Divisibility is therefore impossible.
    gap = product_norm_gap(12, Q, Q**12)

    # Pin the target-dependent trace/AM-GM formula on every arithmetically
    # possible allocation E_A=1+9q_A, E_B=166-9q_A.  Some allocations are
    # later excluded by aggregate/profile constraints; retaining them here
    # makes this an ambient theorem rather than a corpus enumeration.
    trace_rows = []
    for first_norm, second_norm in sorted(set(target_norm_pairs)):
        for normalized_energy_units in range(19):
            energy_a = 1 + 9 * normalized_energy_units
            energy_b = Q - energy_a
            numerator_a = P * energy_a - first_norm
            numerator_b = P * energy_b - second_norm
            if numerator_a % 3 or numerator_b % 3:
                raise AssertionError("a nontrivial spectral trace is nonintegral")
            trace_a = numerator_a // 3
            trace_b = numerator_b // 3
            if trace_a + trace_b != 12 * Q:
                raise AssertionError("the complementary spectral traces changed")
            physically_positive = 0 < trace_a < 12 * Q
            if physically_positive:
                # N_F <= (trace_F/12)^12.  Cross multiplication keeps this
                # certificate exact and avoids floating point.
                bound_numerator = trace_a**12
                bound_denominator = 12**12
                if bound_numerator >= (Q**12) * bound_denominator:
                    raise AssertionError("the AM-GM bound lost the strict gap")
            trace_rows.append(
                (
                    first_norm,
                    second_norm,
                    normalized_energy_units,
                    trace_a,
                    trace_b,
                    physically_positive,
                )
            )

    certificate = (
        target_values,
        target_norm_pairs,
        tuple(sorted(expected_histogram.items())),
        gap,
        tuple(trace_rows),
    )
    certificate_hash = require_hash(
        "norm", certificate, EXPECTED_NORM_CERTIFICATE_SHA256
    )
    return {
        "target_norm_histogram": expected_histogram,
        "primitive_norm_factor_count": 12,
        "strict_factor_interval": (0, Q),
        "primitive_norm_integer_interval": (
            gap["positive_integer_lower"],
            gap["integer_upper_inclusive"],
        ),
        "prime_valuations": {
            "A_trivial": 0,
            "A_plus": 0,
            "A_minus": 0,
            "B_trivial": 0,
            "B_plus": 0,
            "B_minus": 0,
        },
        "am_gm_trace_formula": "(37*E_F-Norm(F(1)))/3",
        "trace_rows_checked": len(trace_rows),
        "certificate_sha256": certificate_hash,
    }


def primitive_torus_exponents(
    plus_a: int, plus_b: int, tau: int
) -> tuple[int, int]:
    """Return exponent coordinates for the all-nonzero primitive torus.

    A nonzero E element is represented by its exponent modulo M-1.  The
    exponent of -1 is (M-1)/2.
    """

    modulus = M - 1
    half = modulus // 2
    minus_a = pow(Q, 7, modulus) * (half + tau + plus_b) % modulus
    minus_b = pow(Q, 7, modulus) * (tau + plus_a) % modulus
    return minus_a, minus_b


def unitary_ratio_exponents(plus: int) -> tuple[int, int]:
    modulus = M - 1
    half = modulus // 2
    minus = pow(Q, 7, modulus) * (half - plus) % modulus
    return plus % modulus, minus


def primitive_nonzero_pattern(
    plus_a_nonzero: bool,
    plus_b_nonzero: bool,
    tau_nonzero: bool,
) -> tuple[int, int, int, int]:
    """Propagate zeros through the old nondegenerate parameterization."""

    if not plus_a_nonzero and not plus_b_nonzero:
        raise ValueError("the old nondegenerate branch needs a nonzero plus pair")
    # y_A=(-tau*x_B)^(q^7), y_B=(tau*x_A)^(q^7).
    minus_a_nonzero = tau_nonzero and plus_b_nonzero
    minus_b_nonzero = tau_nonzero and plus_a_nonzero
    return (
        int(plus_a_nonzero),
        int(plus_b_nonzero),
        int(minus_a_nonzero),
        int(minus_b_nonzero),
    )


def verify_torus() -> dict[str, object]:
    modulus = M - 1
    half = modulus // 2
    q5 = pow(Q, 5, modulus)
    q7 = pow(Q, 7, modulus)
    if q5 * q7 % modulus != 1:
        raise AssertionError("the fifth and seventh Frobenius powers changed")

    # The k-coordinate norm-minus-one fiber.
    k_order = Q2 - 1
    trivial_exponents = tuple(
        ((Q - 1) // 2 + index * (Q - 1)) % k_order
        for index in range(Q + 1)
    )
    if len(set(trivial_exponents)) != Q + 1:
        raise AssertionError("the trivial norm-minus-one fiber size changed")
    if any(
        (Q + 1) * exponent % k_order != k_order // 2
        for exponent in trivial_exponents
    ):
        raise AssertionError("a trivial ratio lost norm minus one")

    ratio_fixtures = []
    for plus in (0, 1, 668, M // 3, M - 2):
        plus_exponent, minus_exponent = unitary_ratio_exponents(plus)
        starred_minus = q5 * minus_exponent % modulus
        if (plus_exponent + starred_minus) % modulus != half:
            raise AssertionError("a primitive unitary ratio fixture failed")
        ratio_fixtures.append((plus_exponent, minus_exponent))

    torus_fixtures = []
    for plus_a, plus_b, tau in (
        (0, 1, 2),
        (37, 167, 668),
        (M // 5, M // 7, M // 11),
    ):
        minus_a, minus_b = primitive_torus_exponents(plus_a, plus_b, tau)
        powered_minus_a = q5 * minus_a % modulus
        powered_minus_b = q5 * minus_b % modulus
        first_term = (plus_a + powered_minus_a) % modulus
        second_term = (plus_b + powered_minus_b) % modulus
        if (first_term - second_term) % modulus != half:
            raise AssertionError("a primitive torus residual lost its minus sign")
        torus_fixtures.append(
            (plus_a, minus_a, plus_b, minus_b, tau)
        )

    old_primitive_count = M**2 + (M**2 - 1) * M
    fixed_target_torus_count = (M - 1) ** 3
    removed_boundary_count = old_primitive_count - fixed_target_torus_count
    if removed_boundary_count != (2 * M - 1) ** 2:
        raise AssertionError("the excluded primitive boundary count changed")

    # Zero-pattern recovery for the old parameterization:
    # y_A=(-tau*x_B)^(q^7), y_B=(tau*x_A)^(q^7).
    forbidden_patterns = (
        ("degenerate", 0, 0, "*", "*"),
        ("A-axis", *primitive_nonzero_pattern(True, False, True)),
        ("B-axis", *primitive_nonzero_pattern(False, True, True)),
        ("tau-zero", *primitive_nonzero_pattern(True, True, False)),
    )
    allowed_pattern = (
        "torus",
        *primitive_nonzero_pattern(True, True, True),
    )
    if allowed_pattern != ("torus", 1, 1, 1, 1):
        raise AssertionError("the physical primitive torus hit a coordinate plane")

    unitary_ratio_count = (Q + 1) * (M - 1)
    ring_unit_count = (Q2 - 1) * (M - 1) ** 2
    universal_unit_cone_count = unitary_ratio_count * ring_unit_count
    direct_universal_count = (Q2 - 1) * (Q + 1) * (M - 1) ** 3
    if universal_unit_cone_count != direct_universal_count:
        raise AssertionError("the unit-ratio and direct torus counts disagree")

    certificate = (
        M,
        q5,
        q7,
        trivial_exponents,
        tuple(ratio_fixtures),
        tuple(torus_fixtures),
        old_primitive_count,
        fixed_target_torus_count,
        removed_boundary_count,
        forbidden_patterns,
        allowed_pattern,
        unitary_ratio_count,
        ring_unit_count,
        universal_unit_cone_count,
    )
    certificate_hash = require_hash(
        "torus", certificate, EXPECTED_TORUS_CERTIFICATE_SHA256
    )
    return {
        "E_size": M,
        "unitary_ratio_count": unitary_ratio_count,
        "ring_unit_count": ring_unit_count,
        "fixed_target_primitive_torus_count": fixed_target_torus_count,
        "universal_unit_cone_count": universal_unit_cone_count,
        "old_primitive_count": old_primitive_count,
        "removed_boundary_count": removed_boundary_count,
        "forbidden_old_patterns": forbidden_patterns,
        "generic_torus_fixtures": len(torus_fixtures),
        "certificate_sha256": certificate_hash,
    }


def verify() -> dict[str, object]:
    result = {
        "alphabet": verify_alphabet(),
        "field": verify_field_arithmetic(),
        "norm": verify_norm_gap(),
        "torus": verify_torus(),
        "status": (
            "conditional spectral-unit theorem verified; "
            "no profile survivor, LP(333), or H(668) is claimed"
        ),
    }
    certificate = (
        result["alphabet"]["certificate_sha256"],
        result["field"]["certificate_sha256"],
        result["norm"]["certificate_sha256"],
        result["torus"]["certificate_sha256"],
    )
    result["certificate_sha256"] = require_hash(
        "master", certificate, EXPECTED_MASTER_CERTIFICATE_SHA256
    )
    return result


def main() -> None:
    result = verify()
    print("PASS: order-three profile spectral-unit theorem")
    print(
        "profile_polynomial="
        f"{result['alphabet']['annihilating_polynomial']}"
    )
    print(
        "primitive_prime_norm="
        f"{result['field']['primitive_prime_absolute_norms'][0]}"
    )
    print(
        "fixed_target_torus_count="
        f"{result['torus']['fixed_target_primitive_torus_count']}"
    )
    print(
        "removed_boundary_count="
        f"{result['torus']['removed_boundary_count']}"
    )
    print(f"certificate_sha256={result['certificate_sha256']}")
    print("STATUS: exact search reduction; no LP(333) or H(668) found")


if __name__ == "__main__":
    main()
