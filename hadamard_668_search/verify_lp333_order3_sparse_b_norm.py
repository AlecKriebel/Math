#!/usr/bin/env python3
"""Verify the sparse-B relative-norm screen for the LP(333) profile gate.

For either aggregate target ``(5,1,0,0)`` or ``(4,-1,0,0)``, normalized
B-profile energy six and B-aggregate zero force

    B = 2 + z (eta_i - eta_j),       Norm(z) = 3.

This dependency-free verifier checks the resulting finite classification,
the lift-safe and field-automorphism orbit counts, a uniform total-positivity
bound, and exact local norm obstructions.  The local certificates are
evaluated in unramified degree-six rings modulo p^2 for p=11 and p=101.

Four field-automorphism types pass the relative field-norm test.  Their
positive norm witnesses are replayed separately by
``verify_lp333_order3_sparse_b_norm.gp``.  Passing this necessary field-norm
test is not a profile construction.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations
import json
from typing import Iterable, Sequence


Eisenstein = tuple[int, int]
Word = tuple[Eisenstein, ...]
ZERO: Eisenstein = (0, 0)
CLASS_COUNT = 12
H = (1, 10, 26)

Z1: Eisenstein = (-2, -1)  # -2-omega
Z2: Eisenstein = (-1, -2)  # -1-2*omega
Z3: Eisenstein = (1, -1)   # 1-omega

NORM_THREE: tuple[Eisenstein, ...] = tuple(
    (a, b)
    for a in range(-3, 4)
    for b in range(-3, 4)
    if a * a - a * b + b * b == 3
)

EXPECTED_CERTIFICATE_SHA256 = (
    "6920db3a6912ad854e0af57562a0e61cd1a1966cb1ed91f8954bd520d4722f5d"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return sha256(payload.encode("ascii")).hexdigest()


def e_neg(value: Eisenstein) -> Eisenstein:
    return -value[0], -value[1]


def e_conjugate(value: Eisenstein) -> Eisenstein:
    """Conjugate a+b*omega in the same basis."""

    a, b = value
    return a - b, -b


def e_norm(value: Eisenstein) -> int:
    a, b = value
    return a * a - a * b + b * b


def sparse_word(first: int, second: int, value: Eisenstein) -> Word:
    if not (0 <= first < CLASS_COUNT and 0 <= second < CLASS_COUNT):
        raise ValueError("class indices must lie in 0,...,11")
    if first == second:
        raise ValueError("the two nonzero classes must be distinct")
    if value not in NORM_THREE:
        raise ValueError("the sparse coefficient must have Eisenstein norm 3")
    word = [ZERO] * CLASS_COUNT
    word[first] = value
    word[second] = e_neg(value)
    return tuple(word)


def even_rotation(word: Word, rotation: int) -> Word:
    """The certified common C6 source action."""

    offset = 2 * (rotation % 6)
    return tuple(word[(index + offset) % CLASS_COUNT] for index in range(12))


def b_star(word: Word) -> Word:
    """The certified B-star: opposite class followed by conjugation."""

    return tuple(
        e_conjugate(word[(index + 6) % CLASS_COUNT])
        for index in range(CLASS_COUNT)
    )


def lift_safe_orbit(word: Word) -> frozenset[Word]:
    return frozenset(
        b_star(even_rotation(word, rotation))
        if use_star
        else even_rotation(word, rotation)
        for rotation in range(6)
        for use_star in (False, True)
    )


def class_rotation(word: Word, rotation: int) -> Word:
    """A C12 Galois action used only to classify relative norms."""

    offset = rotation % CLASS_COUNT
    return tuple(word[(index + offset) % CLASS_COUNT] for index in range(12))


def coefficient_conjugation(word: Word) -> Word:
    return tuple(map(e_conjugate, word))


def field_orbit(word: Word) -> frozenset[Word]:
    """Orbit under C12 x Gal(Q(omega)/Q), not a labelled-lift symmetry."""

    return frozenset(
        coefficient_conjugation(class_rotation(word, rotation))
        if conjugate
        else class_rotation(word, rotation)
        for rotation in range(12)
        for conjugate in (False, True)
    )


def orbit_partition(
    words: Iterable[Word],
    orbit_function,
) -> tuple[frozenset[Word], ...]:
    universe = set(words)
    unseen = set(universe)
    result: list[frozenset[Word]] = []
    while unseen:
        representative = min(unseen)
        orbit = orbit_function(representative)
        if not orbit <= universe:
            raise AssertionError("an orbit left the sparse-B universe")
        result.append(orbit)
        unseen.difference_update(orbit)
    return tuple(sorted(result, key=lambda orbit: min(orbit)))


def all_sparse_words() -> frozenset[Word]:
    return frozenset(
        sparse_word(first, second, value)
        for first, second in combinations(range(CLASS_COUNT), 2)
        for value in NORM_THREE
    )


def _trim(poly: Sequence[int], modulus: int) -> list[int]:
    result = [int(value) % modulus for value in poly]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def _poly_divmod(
    numerator: Sequence[int],
    denominator: Sequence[int],
    modulus: int,
) -> tuple[list[int], list[int]]:
    left = _trim(numerator, modulus)
    right = _trim(denominator, modulus)
    if right == [0]:
        raise ZeroDivisionError("polynomial division by zero")
    quotient = [0] * max(1, len(left) - len(right) + 1)
    inverse_lead = pow(right[-1], -1, modulus)
    while len(left) >= len(right) and left != [0]:
        shift = len(left) - len(right)
        scale = left[-1] * inverse_lead % modulus
        quotient[shift] = scale
        for index, value in enumerate(right):
            left[index + shift] = (
                left[index + shift] - scale * value
            ) % modulus
        left = _trim(left, modulus)
    return _trim(quotient, modulus), left


def _poly_gcd(
    first: Sequence[int], second: Sequence[int], modulus: int
) -> tuple[int, ...]:
    left = _trim(first, modulus)
    right = _trim(second, modulus)
    while right != [0]:
        _, remainder = _poly_divmod(left, right, modulus)
        left, right = right, remainder
    inverse_lead = pow(left[-1], -1, modulus)
    return tuple(value * inverse_lead % modulus for value in left)


class QuotientRing:
    """(Z/nZ)[x]/(f), with f monic and stored in ascending order."""

    def __init__(self, modulus: int, polynomial: Sequence[int]) -> None:
        if modulus <= 1:
            raise ValueError("the coefficient modulus must exceed one")
        if len(polynomial) < 2 or int(polynomial[-1]) % modulus != 1:
            raise ValueError("the quotient polynomial must be monic")
        self.modulus = int(modulus)
        self.polynomial = tuple(
            int(value) % self.modulus for value in polynomial
        )
        self.degree = len(self.polynomial) - 1

    def element(self, value: int | Sequence[int] = 0) -> tuple[int, ...]:
        if isinstance(value, int):
            return (value % self.modulus,) + (0,) * (self.degree - 1)
        if len(value) > self.degree:
            raise ValueError("an element has too many coefficients")
        return tuple(int(entry) % self.modulus for entry in value) + (
            0,
        ) * (self.degree - len(value))

    def add(
        self, left: Sequence[int], right: Sequence[int]
    ) -> tuple[int, ...]:
        return tuple(
            (int(a) + int(b)) % self.modulus
            for a, b in zip(left, right)
        )

    def neg(self, value: Sequence[int]) -> tuple[int, ...]:
        return tuple(-int(entry) % self.modulus for entry in value)

    def subtract(
        self, left: Sequence[int], right: Sequence[int]
    ) -> tuple[int, ...]:
        return self.add(left, self.neg(right))

    def multiply(
        self, left: Sequence[int], right: Sequence[int]
    ) -> tuple[int, ...]:
        coefficients = [0] * (2 * self.degree - 1)
        for left_index, left_value in enumerate(left):
            for right_index, right_value in enumerate(right):
                index = left_index + right_index
                coefficients[index] = (
                    coefficients[index]
                    + int(left_value) * int(right_value)
                ) % self.modulus
        for power in range(2 * self.degree - 2, self.degree - 1, -1):
            scale = coefficients[power]
            if not scale:
                continue
            for index in range(self.degree):
                destination = power - self.degree + index
                coefficients[destination] = (
                    coefficients[destination]
                    - scale * self.polynomial[index]
                ) % self.modulus
        return tuple(coefficients[: self.degree])

    def power(self, value: Sequence[int], exponent: int) -> tuple[int, ...]:
        if exponent < 0:
            raise ValueError("power expects a nonnegative exponent")
        result = self.element(1)
        factor = tuple(map(int, value))
        remaining = int(exponent)
        while remaining:
            if remaining & 1:
                result = self.multiply(result, factor)
            factor = self.multiply(factor, factor)
            remaining >>= 1
        return result

    def inverse_unit(
        self, value: Sequence[int], residue_prime: int
    ) -> tuple[int, ...]:
        """Invert a unit modulo p^2 by finite-field inversion and Newton."""

        p = int(residue_prime)
        if self.modulus != p * p:
            raise ValueError("unit lifting is implemented only modulo p^2")
        residue_ring = QuotientRing(
            p, tuple(entry % p for entry in self.polynomial)
        )
        residue_value = tuple(int(entry) % p for entry in value)
        inverse_residue = residue_ring.power(
            residue_value, p**self.degree - 2
        )
        lifted = tuple(map(int, inverse_residue))
        return self.multiply(
            lifted,
            self.subtract(
                self.element(2), self.multiply(value, lifted)
            ),
        )


LOCAL_FACTORS: dict[int, tuple[int, ...]] = {
    11: (1, 1, 3, 5, 3, 1, 1),
    101: (1, 4, 50, 90, 50, 4, 1),
}


def verify_irreducible_factor(
    prime: int, polynomial: Sequence[int]
) -> dict[str, object]:
    """Certify that f is an irreducible degree-six factor of Phi_37 mod p."""

    p = int(prime)
    ring = QuotientRing(p, polynomial)
    if ring.degree != 6:
        raise AssertionError("the local factor must have degree six")
    x = ring.element((0, 1))
    if ring.power(x, 37) != ring.element(1) or x == ring.element(1):
        raise AssertionError("the pinned polynomial is not a Phi_37 factor")
    if ring.power(x, p**6) != x:
        raise AssertionError("the local factor did not split over F_(p^6)")
    gcd_degrees = []
    for divisor in (2, 3):
        exponent = p ** (6 // divisor)
        residue = ring.subtract(ring.power(x, exponent), x)
        gcd_value = _poly_gcd(residue, polynomial, p)
        gcd_degrees.append(len(gcd_value) - 1)
        if gcd_value != (1,):
            raise AssertionError("the pinned degree-six factor is reducible")
    powers = tuple(pow(p, exponent, 37) for exponent in range(6))
    if powers[3] != 36 or set(powers[::2]) != set(H):
        raise AssertionError("the Frobenius/H alignment changed")
    return {
        "prime": p,
        "factor": tuple(map(int, polynomial)),
        "irreducibility_gcd_degrees": tuple(gcd_degrees),
        "frobenius_powers_mod_37": powers,
    }


def hensel_local_generators(
    prime: int, polynomial: Sequence[int]
) -> tuple[QuotientRing, tuple[int, ...], tuple[int, ...]]:
    """Return compatible 37th and third roots modulo p^2."""

    p = int(prime)
    ring = QuotientRing(p * p, polynomial)
    alpha = ring.element((0, 1))
    error = ring.subtract(ring.power(alpha, 37), ring.element(1))
    derivative = ring.multiply(ring.element(37), ring.power(alpha, 36))
    alpha = ring.subtract(
        alpha,
        ring.multiply(error, ring.inverse_unit(derivative, p)),
    )
    if ring.power(alpha, 37) != ring.element(1):
        raise AssertionError("the primitive 37th root did not Hensel lift")

    residue_ring = QuotientRing(p, polynomial)
    residue_x = residue_ring.element((0, 1))
    omega_residue = None
    for constant in range(p):
        candidate = residue_ring.add(
            residue_x, residue_ring.element(constant)
        )
        value = residue_ring.power(candidate, (p**6 - 1) // 3)
        if value != residue_ring.element(1):
            omega_residue = value
            break
    if omega_residue is None:
        raise AssertionError("failed to locate a nontrivial cube root")
    omega = tuple(map(int, omega_residue))
    omega_error = ring.add(
        ring.add(ring.multiply(omega, omega), omega),
        ring.element(1),
    )
    omega_derivative = ring.add(
        ring.multiply(ring.element(2), omega), ring.element(1)
    )
    omega = ring.subtract(
        omega,
        ring.multiply(
            omega_error, ring.inverse_unit(omega_derivative, p)
        ),
    )
    if ring.add(
        ring.add(ring.multiply(omega, omega), omega),
        ring.element(1),
    ) != ring.element(0):
        raise AssertionError("the primitive cube root did not Hensel lift")
    return ring, alpha, omega


def ring_sum(
    ring: QuotientRing, values: Iterable[Sequence[int]]
) -> tuple[int, ...]:
    result = ring.element(0)
    for value in values:
        result = ring.add(result, value)
    return result


def local_valuation_signature(
    prime: int, separation: int, value: Eisenstein
) -> tuple[int, ...]:
    """Evaluate gamma at all 12 degree-one M-primes modulo p^2.

    Output category 0 means valuation zero, 1 means valuation exactly one,
    and 2 means valuation at least two.  Category 1 is therefore an exact
    odd-valuation local norm obstruction.
    """

    if not 1 <= separation <= 6:
        raise ValueError("the normalized class separation must lie in 1,...,6")
    if value not in (Z1, Z2, Z3):
        raise ValueError("use one of the normalized norm-type representatives")
    p = int(prime)
    polynomial = LOCAL_FACTORS[p]
    ring, alpha, omega = hensel_local_generators(p, polynomial)

    z = ring.add(
        ring.element(value[0]),
        ring.multiply(ring.element(value[1]), omega),
    )
    conjugate = e_conjugate(value)
    z_star = ring.add(
        ring.element(conjugate[0]),
        ring.multiply(ring.element(conjugate[1]), omega),
    )

    def eta(class_index: int, exponent: int) -> tuple[int, ...]:
        return ring_sum(
            ring,
            (
                ring.power(
                    alpha,
                    (
                        exponent
                        * pow(2, class_index, 37)
                        * subgroup_value
                    )
                    % 37,
                )
                for subgroup_value in H
            ),
        )

    result = []
    for embedding_index in range(12):
        exponent = pow(2, embedding_index, 37)
        negative_exponent = (-exponent) % 37
        difference = ring.subtract(
            eta(0, exponent), eta(separation, exponent)
        )
        star_difference = ring.subtract(
            eta(0, negative_exponent),
            eta(separation, negative_exponent),
        )
        b_value = ring.add(ring.element(2), ring.multiply(z, difference))
        b_star_value = ring.add(
            ring.element(2), ring.multiply(z_star, star_difference)
        )
        gamma = ring.subtract(
            ring.element(167), ring.multiply(b_value, b_star_value)
        )
        if any(gamma[index] for index in range(1, ring.degree)):
            raise AssertionError("a fixed-field gamma residue was not scalar")
        scalar = gamma[0]
        if scalar % p:
            result.append(0)
        elif scalar % (p * p):
            result.append(1)
        else:
            result.append(2)
    return tuple(result)


@dataclass(frozen=True)
class NormType:
    separation: int
    value: Eisenstein
    status: str
    p11_signature: tuple[int, ...]
    p101_signature: tuple[int, ...] = ()

    @property
    def representative(self) -> Word:
        return sparse_word(0, self.separation, self.value)

    @property
    def field_orbit_size(self) -> int:
        return len(field_orbit(self.representative))


ZERO_SIGNATURE = (0,) * 12

NORM_TYPES: tuple[NormType, ...] = (
    NormType(1, Z1, "inert_11", (0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0)),
    NormType(1, Z2, "relative_norm", (0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0)),
    NormType(1, Z3, "inert_11", (0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0)),
    NormType(2, Z1, "inert_11", (0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0)),
    NormType(2, Z2, "inert_11", (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)),
    NormType(2, Z3, "inert_11", (1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1)),
    NormType(3, Z1, "relative_norm", ZERO_SIGNATURE),
    NormType(3, Z2, "inert_11", (0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
    NormType(3, Z3, "inert_11", (0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 0, 0)),
    NormType(
        4,
        Z1,
        "inert_101",
        ZERO_SIGNATURE,
        (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0),
    ),
    NormType(4, Z2, "inert_11", (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1)),
    NormType(4, Z3, "inert_11", (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0)),
    NormType(
        5,
        Z1,
        "inert_11",
        (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0),
    ),
    NormType(5, Z2, "inert_11", (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0)),
    NormType(5, Z3, "inert_11", (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1)),
    NormType(6, Z1, "relative_norm", ZERO_SIGNATURE),
    NormType(6, Z2, "relative_norm", ZERO_SIGNATURE),
)


def verify() -> dict[str, object]:
    if NORM_THREE != (
        (-2, -1),
        (-1, -2),
        (-1, 1),
        (1, -1),
        (1, 2),
        (2, 1),
    ):
        raise AssertionError("the norm-three Eisenstein alphabet changed")
    if any(e_norm(value) != 3 for value in NORM_THREE):
        raise AssertionError("a pinned sparse coefficient lost norm three")

    words = all_sparse_words()
    if len(words) != 396:
        raise AssertionError("the raw sparse-B count changed")
    safe_orbits = orbit_partition(words, lift_safe_orbit)
    safe_sizes = tuple(sorted(map(len, safe_orbits)))
    if safe_sizes != (6, 6) + (12,) * 32:
        raise AssertionError("the lift-safe orbit census changed")
    algebraic_orbits = orbit_partition(words, field_orbit)
    algebraic_sizes = tuple(sorted(map(len, algebraic_orbits)))
    if algebraic_sizes != (12,) + (24,) * 16:
        raise AssertionError("the relative-norm orbit census changed")

    representative_orbits = tuple(
        field_orbit(norm_type.representative) for norm_type in NORM_TYPES
    )
    if len(set(representative_orbits)) != 17:
        raise AssertionError("two normalized norm types became equivalent")
    if frozenset().union(*representative_orbits) != words:
        raise AssertionError("the 17 normalized norm types do not cover")

    local_factor_certificates = tuple(
        verify_irreducible_factor(prime, LOCAL_FACTORS[prime])
        for prime in (11, 101)
    )
    rows = []
    for norm_type in NORM_TYPES:
        observed_11 = local_valuation_signature(
            11, norm_type.separation, norm_type.value
        )
        if observed_11 != norm_type.p11_signature:
            raise AssertionError("a pinned p=11 local signature changed")
        observed_101 = local_valuation_signature(
            101, norm_type.separation, norm_type.value
        )
        expected_101 = norm_type.p101_signature or ZERO_SIGNATURE
        if observed_101 != expected_101:
            raise AssertionError("a pinned p=101 local signature changed")

        simple_11 = observed_11.count(1)
        simple_101 = observed_101.count(1)
        if norm_type.status == "inert_11" and simple_11 == 0:
            raise AssertionError("a claimed p=11 obstruction is not simple")
        if norm_type.status == "inert_101" and simple_101 == 0:
            raise AssertionError("the claimed p=101 obstruction is not simple")
        if norm_type.status == "relative_norm" and (
            simple_11 or simple_101
        ):
            raise AssertionError("a norm-soluble row has a pinned obstruction")
        rows.append(
            {
                "separation": norm_type.separation,
                "value": norm_type.value,
                "field_orbit_size": norm_type.field_orbit_size,
                "status": norm_type.status,
                "p11_signature": observed_11,
                "p11_simple_primes": simple_11,
                "p101_signature": observed_101,
                "p101_simple_primes": simple_101,
            }
        )

    obstructed_orbits = tuple(
        orbit
        for norm_type, orbit in zip(NORM_TYPES, representative_orbits)
        if norm_type.status != "relative_norm"
    )
    surviving_orbits = tuple(
        orbit
        for norm_type, orbit in zip(NORM_TYPES, representative_orbits)
        if norm_type.status == "relative_norm"
    )
    obstructed_words = frozenset().union(*obstructed_orbits)
    surviving_words = frozenset().union(*surviving_orbits)
    if len(obstructed_words) != 312 or len(surviving_words) != 84:
        raise AssertionError("the raw obstruction census changed")
    if obstructed_words | surviving_words != words:
        raise AssertionError("the norm classification does not partition")

    obstructed_safe = tuple(
        orbit for orbit in safe_orbits if orbit <= obstructed_words
    )
    surviving_safe = tuple(
        orbit for orbit in safe_orbits if orbit <= surviving_words
    )
    if len(obstructed_safe) != 26 or len(surviving_safe) != 8:
        raise AssertionError("the lift-safe obstruction census changed")
    if tuple(sorted(map(len, surviving_safe))) != (
        6,
        6,
        12,
        12,
        12,
        12,
        12,
        12,
    ):
        raise AssertionError("the surviving lift-safe orbit sizes changed")

    # |B_sigma| <= 2 + sqrt(3)*(3+3) at every primitive embedding.
    # Squaring gives 112+24*sqrt(3), and the exact comparison with 167 is
    # 24*sqrt(3)<55, certified by 24^2*3 < 55^2.
    positivity_certificate = {
        "rational_part_of_squared_bound": 112,
        "sqrt3_coefficient": 24,
        "target": 167,
        "squared_comparison": (24 * 24 * 3, 55 * 55),
    }
    if positivity_certificate["squared_comparison"] != (1728, 3025):
        raise AssertionError("the total-positivity inequality changed")

    targets = ((5, 1, 0, 0), (4, -1, 0, 0))
    target_values = tuple(
        ((-1 + 3 * target[0], 3 * target[1]), (2, 0))
        for target in targets
    )
    if tuple((e_norm(a), e_norm(b)) for a, b in target_values) != (
        (163, 4),
        (163, 4),
    ):
        raise AssertionError("the two extreme target norm pairs changed")
    if e_conjugate(target_values[0][0]) != target_values[1][0]:
        raise AssertionError("the two A aggregates are no longer conjugate")

    certificate = {
        "alphabet": NORM_THREE,
        "raw_words": len(words),
        "lift_safe_orbit_sizes": safe_sizes,
        "field_orbit_sizes": algebraic_sizes,
        "local_factors": local_factor_certificates,
        "rows": tuple(rows),
        "obstructed_field_types": len(obstructed_orbits),
        "surviving_field_types": len(surviving_orbits),
        "obstructed_raw_words": len(obstructed_words),
        "surviving_raw_words": len(surviving_words),
        "obstructed_lift_safe_orbits": len(obstructed_safe),
        "surviving_lift_safe_orbits": len(surviving_safe),
        "surviving_lift_safe_sizes": tuple(
            sorted(map(len, surviving_safe))
        ),
        "positivity": positivity_certificate,
        "target_values": target_values,
        "normalized_energies": {"A": 48, "B": 6},
        "physical_energies": {"A": 145, "B": 22},
    }
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_CERTIFICATE_SHA256
    ):
        raise AssertionError(
            "the sparse-B norm certificate changed: "
            f"{certificate_hash} != {EXPECTED_CERTIFICATE_SHA256}"
        )
    return {
        **certificate,
        "certificate_sha256": certificate_hash,
    }


def main() -> None:
    result = verify()
    print(f"raw_sparse_B_words={result['raw_words']}")
    print(
        "lift_safe_orbits="
        f"{len(result['lift_safe_orbit_sizes'])} "
        "(32x12,2x6)"
    )
    print(
        "field_norm_types="
        f"{len(result['field_orbit_sizes'])} "
        "(16x24,1x12)"
    )
    print(
        "locally_obstructed="
        f"{result['obstructed_field_types']}/17 "
        f"raw={result['obstructed_raw_words']} "
        f"lift_safe={result['obstructed_lift_safe_orbits']}"
    )
    print(
        "relative_norm_soluble="
        f"{result['surviving_field_types']}/17 "
        f"raw={result['surviving_raw_words']} "
        f"lift_safe={result['surviving_lift_safe_orbits']}"
    )
    for row in result["rows"]:
        print(
            "row="
            f"d{row['separation']} z{tuple(row['value'])} "
            f"orbit{row['field_orbit_size']} "
            f"{row['status']} "
            f"simple11={row['p11_simple_primes']} "
            f"simple101={row['p101_simple_primes']}"
        )
    print("sector_closed=false")
    print(f"certificate_sha256={result['certificate_sha256']}")


if __name__ == "__main__":
    main()
