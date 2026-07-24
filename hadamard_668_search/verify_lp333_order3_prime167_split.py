#!/usr/bin/env python3
"""Verify the prime-167 split parameterization of the LP(333) profile gate.

On the energy-167 shell, exact Eisenstein complementarity on ``C_37`` is
equivalent to complementarity modulo 167.  The equality case in Cauchy's
inequality makes this stronger than an ordinary modular necessary condition.

Writing ``k=F_167(omega)=F_(167^2)`` and taking the order-three invariant
subalgebra, the finite group algebra has the split form

    k[C_37]^H = k x E x E,       E=F_(167^12).

In coordinates ``(F(1),F(zeta),F(zeta^167))``, its involution is

    (c,x,y)^* = (c^167, y^(167^5), x^(167^7)).

This module checks an explicit factorization of Phi_37 over k, proves both
degree-18 factors irreducible, replays the fixed-field dimensions and star
exponents, round-trips deterministic inverse-CRT fixtures, and verifies a
complete, branch-by-branch parameterization of the finite-field solution
cone.
"""

from __future__ import annotations

from hashlib import sha256
import json
from math import gcd
from typing import Sequence

from verify_lp333_order3_profile9 import profile_column_values
from verify_lp333_order3_profile9_shards import PROFILE9_SHARD_WITNESSES


P = 167
N = 37
Q = P * P
H = (1, 10, 26)
E_SIZE = P**12
L_SIZE = P**36

K = tuple[int, int]  # a+b*omega in F_167[omega], omega^2+omega+1=0.
L = tuple[K, ...]  # degree-18 extension over K, padded to length 18.

K_ZERO: K = (0, 0)
K_ONE: K = (1, 0)

# One of the two degree-18 factors of Phi_37 over K.  Coefficients are in
# ascending order.  The other factor is its coefficient-conjugate reciprocal.
FACTOR_PLUS: tuple[K, ...] = (
    (1, 0),
    (62, 123),
    (5, 0),
    (121, 79),
    (113, 44),
    (15, 35),
    (114, 44),
    (119, 79),
    (111, 44),
    (121, 79),
    (111, 44),
    (119, 79),
    (114, 44),
    (15, 35),
    (113, 44),
    (121, 79),
    (5, 0),
    (62, 123),
    (1, 0),
)

FACTOR_MINUS: tuple[K, ...] = (
    (1, 0),
    (106, 44),
    (5, 0),
    (42, 88),
    (69, 123),
    (147, 132),
    (70, 123),
    (40, 88),
    (67, 123),
    (42, 88),
    (67, 123),
    (40, 88),
    (70, 123),
    (147, 132),
    (69, 123),
    (42, 88),
    (5, 0),
    (106, 44),
    (1, 0),
)

EXPECTED_PROFILE_SIGNATURE_SHA256 = (
    "6a4bd5cd494346cc1a0396e51936fb2fafb34ee53032f84fb79caeb95a890900"
)
EXPECTED_EQUALITY_CASE_SHA256 = (
    "04435badfc26829c4b9bfdd51929c7ae6daa51868b138c335c383d99fa51cc3b"
)
EXPECTED_FIELD_SPLIT_SHA256 = (
    "445e8246071b8b84702e05d640cfbbf81ab7b09c7c82999d00d345d35afe6815"
)
EXPECTED_PARAMETER_FIXTURE_SHA256 = (
    "1492ae5cf79738a1721c4f5eb9046e1333eb7ac99dd0f305cebafd20d5850d9e"
)
EXPECTED_STAR_CRT_FIXTURE_SHA256 = (
    "6cd8b72030b431111bdece3260526a211775c71191e63380a907fa8e65a08268"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


# ---------------------------------------------------------------------------
# Arithmetic in k=F_167[omega].


def k_reduce(value: K) -> K:
    return value[0] % P, value[1] % P


def k_add(left: K, right: K) -> K:
    return (left[0] + right[0]) % P, (left[1] + right[1]) % P


def k_neg(value: K) -> K:
    return (-value[0]) % P, (-value[1]) % P


def k_sub(left: K, right: K) -> K:
    return k_add(left, k_neg(right))


def k_multiply(left: K, right: K) -> K:
    a, b = left
    c, d = right
    return (a * c - b * d) % P, (a * d + b * c - b * d) % P


def k_conjugate(value: K) -> K:
    return (value[0] - value[1]) % P, (-value[1]) % P


def k_norm(value: K) -> int:
    a, b = value
    return (a * a - a * b + b * b) % P


def k_inverse(value: K) -> K:
    norm = k_norm(value)
    if not norm:
        raise ZeroDivisionError("zero has no inverse in k")
    inverse_norm = pow(norm, -1, P)
    conjugate = k_conjugate(value)
    return (
        conjugate[0] * inverse_norm % P,
        conjugate[1] * inverse_norm % P,
    )


def k_power(value: K, exponent: int) -> K:
    if exponent < 0:
        return k_power(k_inverse(value), -exponent)
    result = K_ONE
    base = k_reduce(value)
    while exponent:
        if exponent & 1:
            result = k_multiply(result, base)
        base = k_multiply(base, base)
        exponent //= 2
    return result


# ---------------------------------------------------------------------------
# Generic K-polynomials, used for the exact factor/irreducibility checks.


def poly_trim(value: Sequence[K]) -> list[K]:
    result = [k_reduce(coefficient) for coefficient in value]
    while result and result[-1] == K_ZERO:
        result.pop()
    return result


def poly_add(left: Sequence[K], right: Sequence[K]) -> list[K]:
    return poly_trim(
        [
            k_add(
                left[index] if index < len(left) else K_ZERO,
                right[index] if index < len(right) else K_ZERO,
            )
            for index in range(max(len(left), len(right)))
        ]
    )


def poly_subtract(left: Sequence[K], right: Sequence[K]) -> list[K]:
    return poly_add(left, [k_neg(value) for value in right])


def poly_multiply(left: Sequence[K], right: Sequence[K]) -> list[K]:
    if not left or not right:
        return []
    result = [K_ZERO] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] = k_add(
                result[left_index + right_index],
                k_multiply(left_value, right_value),
            )
    return poly_trim(result)


def poly_divmod(
    dividend: Sequence[K], divisor: Sequence[K]
) -> tuple[list[K], list[K]]:
    remainder = poly_trim(dividend)
    normalized_divisor = poly_trim(divisor)
    if not normalized_divisor:
        raise ZeroDivisionError("polynomial division by zero")
    quotient = [K_ZERO] * max(
        0, len(remainder) - len(normalized_divisor) + 1
    )
    inverse_lead = k_inverse(normalized_divisor[-1])
    while len(remainder) >= len(normalized_divisor):
        offset = len(remainder) - len(normalized_divisor)
        factor = k_multiply(remainder[-1], inverse_lead)
        quotient[offset] = factor
        for index, coefficient in enumerate(normalized_divisor):
            remainder[index + offset] = k_sub(
                remainder[index + offset],
                k_multiply(factor, coefficient),
            )
        remainder = poly_trim(remainder)
    return poly_trim(quotient), remainder


def poly_mod(value: Sequence[K], modulus: Sequence[K]) -> list[K]:
    return poly_divmod(value, modulus)[1]


def poly_gcd(left: Sequence[K], right: Sequence[K]) -> list[K]:
    first = poly_trim(left)
    second = poly_trim(right)
    while second:
        first, second = second, poly_mod(first, second)
    if not first:
        return []
    inverse_lead = k_inverse(first[-1])
    return [k_multiply(value, inverse_lead) for value in first]


def poly_power_mod(
    value: Sequence[K], exponent: int, modulus: Sequence[K]
) -> list[K]:
    result = [K_ONE]
    base = poly_mod(value, modulus)
    while exponent:
        if exponent & 1:
            result = poly_mod(poly_multiply(result, base), modulus)
        base = poly_mod(poly_multiply(base, base), modulus)
        exponent //= 2
    return result


def polynomial_is_irreducible(
    polynomial: Sequence[K], field_size: int
) -> bool:
    """Apply the standard finite-field irreducibility criterion."""

    normalized = poly_trim(polynomial)
    degree = len(normalized) - 1
    if degree <= 0 or normalized[-1] != K_ONE:
        return False
    x = [K_ZERO, K_ONE]
    if poly_subtract(
        poly_power_mod(x, field_size**degree, normalized), x
    ):
        return False
    prime_divisors = tuple(
        prime
        for prime in range(2, degree + 1)
        if degree % prime == 0
        and all(prime % divisor for divisor in range(2, int(prime**0.5) + 1))
    )
    for prime in prime_divisors:
        probe = poly_subtract(
            poly_power_mod(x, field_size ** (degree // prime), normalized),
            x,
        )
        if len(poly_gcd(normalized, probe)) > 1:
            return False
    return True


# ---------------------------------------------------------------------------
# Arithmetic in L=k[zeta], with zeta a root of FACTOR_PLUS.


L_DEGREE = len(FACTOR_PLUS) - 1
L_ZERO: L = (K_ZERO,) * L_DEGREE
L_ONE: L = (K_ONE,) + (K_ZERO,) * (L_DEGREE - 1)
ZETA: L = (K_ZERO, K_ONE) + (K_ZERO,) * (L_DEGREE - 2)


def l_normalize(value: Sequence[K]) -> L:
    work = [k_reduce(coefficient) for coefficient in value]
    if len(work) < L_DEGREE:
        work.extend([K_ZERO] * (L_DEGREE - len(work)))
    if len(work) > L_DEGREE:
        for degree in range(len(work) - 1, L_DEGREE - 1, -1):
            factor = work[degree]
            if factor != K_ZERO:
                offset = degree - L_DEGREE
                for index in range(L_DEGREE):
                    work[offset + index] = k_sub(
                        work[offset + index],
                        k_multiply(factor, FACTOR_PLUS[index]),
                    )
        work = work[:L_DEGREE]
    return tuple(work)


def l_embed(value: K) -> L:
    return (k_reduce(value),) + (K_ZERO,) * (L_DEGREE - 1)


def l_add(left: L, right: L) -> L:
    return tuple(k_add(a, b) for a, b in zip(left, right))


def l_neg(value: L) -> L:
    return tuple(k_neg(coefficient) for coefficient in value)


def l_subtract(left: L, right: L) -> L:
    return l_add(left, l_neg(right))


def l_multiply(left: L, right: L) -> L:
    work = [K_ZERO] * (2 * L_DEGREE - 1)
    for left_index, left_value in enumerate(left):
        if left_value == K_ZERO:
            continue
        for right_index, right_value in enumerate(right):
            if right_value == K_ZERO:
                continue
            work[left_index + right_index] = k_add(
                work[left_index + right_index],
                k_multiply(left_value, right_value),
            )
    return l_normalize(work)


def l_power(value: L, exponent: int) -> L:
    if exponent < 0:
        if value == L_ZERO:
            raise ZeroDivisionError("zero has no negative field power")
        return l_power(value, L_SIZE - 1 + exponent)
    result = L_ONE
    base = value
    while exponent:
        if exponent & 1:
            result = l_multiply(result, base)
        base = l_multiply(base, base)
        exponent //= 2
    return result


def l_scale(value: L, scalar: K) -> L:
    return tuple(k_multiply(coefficient, scalar) for coefficient in value)


def l_inverse(value: L) -> L:
    if value == L_ZERO:
        raise ZeroDivisionError("zero has no inverse in L")
    return l_power(value, L_SIZE - 2)


def l_evaluate(coefficients: Sequence[K], point: L) -> L:
    result = L_ZERO
    for coefficient in reversed(coefficients):
        result = l_add(l_multiply(result, point), l_embed(coefficient))
    return result


def l_is_in_k(value: L) -> bool:
    return all(coefficient == K_ZERO for coefficient in value[1:])


def l_constant(value: L) -> K:
    if not l_is_in_k(value):
        raise ValueError("extension value is not in the coefficient field")
    return value[0]


def k_matrix_rank(rows: Sequence[Sequence[K]]) -> int:
    work = [list(map(k_reduce, row)) for row in rows]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(rank, row_count)
                if work[row][column] != K_ZERO
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = k_inverse(work[rank][column])
        work[rank] = [
            k_multiply(value, inverse) for value in work[rank]
        ]
        for row in range(row_count):
            if row == rank:
                continue
            factor = work[row][column]
            if factor != K_ZERO:
                work[row] = [
                    k_sub(left, k_multiply(factor, right))
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


# ---------------------------------------------------------------------------
# H-invariant group-ring CRT and involution.


def multiplicative_classes() -> tuple[tuple[int, ...], ...]:
    classes = tuple(
        tuple(pow(2, index, N) * h % N for h in H) for index in range(12)
    )
    if set().union(*(set(part) for part in classes)) != set(range(1, N)):
        raise AssertionError("the H-classes do not partition F_37^*")
    return classes


CLASSES = multiplicative_classes()
CLASS_OF = {
    member: class_index
    for class_index, part in enumerate(CLASSES)
    for member in part
}


def is_h_invariant(coefficients: Sequence[K]) -> bool:
    if len(coefficients) != N:
        return False
    return all(
        len({k_reduce(coefficients[index]) for index in part}) == 1
        for part in CLASSES
    )


def group_star(coefficients: Sequence[K]) -> tuple[K, ...]:
    if len(coefficients) != N:
        raise ValueError("expected a C_37 group-ring word")
    return tuple(k_conjugate(coefficients[-index % N]) for index in range(N))


def group_multiply(
    left: Sequence[K], right: Sequence[K]
) -> tuple[K, ...]:
    if len(left) != N or len(right) != N:
        raise ValueError("expected two C_37 group-ring words")
    result = [K_ZERO] * N
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[(left_index + right_index) % N] = k_add(
                result[(left_index + right_index) % N],
                k_multiply(left_value, right_value),
            )
    return tuple(result)


def group_add(
    left: Sequence[K], right: Sequence[K]
) -> tuple[K, ...]:
    return tuple(k_add(a, b) for a, b in zip(left, right))


def crt_forward(coefficients: Sequence[K]) -> tuple[K, L, L]:
    """Return (F(1),F(zeta),F(zeta^167))."""

    if not is_h_invariant(coefficients):
        raise ValueError("the CRT input must be H-invariant")
    first = K_ZERO
    for coefficient in coefficients:
        first = k_add(first, coefficient)
    plus = l_evaluate(coefficients, ZETA)
    minus = l_evaluate(coefficients, l_power(ZETA, P))
    return first, plus, minus


def crt_inverse(first: K, plus: L, minus: L) -> tuple[K, ...]:
    """Invert the H-invariant CRT by an exact finite-field DFT."""

    if l_power(plus, P**12) != plus or l_power(minus, P**12) != minus:
        raise ValueError("primitive CRT coordinates must lie in F_(167^12)")
    plus_orbit = []
    minus_orbit = []
    current_plus = plus
    current_minus = minus
    for _ in range(18):
        plus_orbit.append(current_plus)
        minus_orbit.append(current_minus)
        current_plus = l_power(current_plus, Q)
        current_minus = l_power(current_minus, Q)
    if current_plus != plus or current_minus != minus:
        raise AssertionError("a primitive Frobenius orbit failed to close")

    zeta_powers = [L_ONE]
    for _ in range(1, N):
        zeta_powers.append(l_multiply(zeta_powers[-1], ZETA))
    inverse_n = (pow(N, -1, P), 0)
    coefficients = []
    for coefficient_index in range(N):
        value = l_embed(first)
        q_power = 1
        for orbit_index in range(18):
            plus_exponent = (
                -q_power * coefficient_index
            ) % N
            minus_exponent = (
                -P * q_power * coefficient_index
            ) % N
            value = l_add(
                value,
                l_multiply(
                    plus_orbit[orbit_index], zeta_powers[plus_exponent]
                ),
            )
            value = l_add(
                value,
                l_multiply(
                    minus_orbit[orbit_index], zeta_powers[minus_exponent]
                ),
            )
            q_power = q_power * Q % N
        coefficients.append(l_constant(l_scale(value, inverse_n)))
    result = tuple(coefficients)
    if not is_h_invariant(result):
        raise AssertionError("inverse CRT output lost H-invariance")
    return result


def deterministic_h_word(seed: int) -> tuple[K, ...]:
    values = [
        ((17 * seed + 23) % P, (31 * seed + 7) % P)
    ]
    class_values = tuple(
        (
            (seed * seed + 11 * class_index + 3) % P,
            (7 * seed + class_index * class_index + 5) % P,
        )
        for class_index in range(12)
    )
    for index in range(1, N):
        values.append(class_values[CLASS_OF[index]])
    result = tuple(values)
    if not is_h_invariant(result):
        raise AssertionError("deterministic word construction failed")
    return result


def period(class_index: int) -> L:
    value = L_ZERO
    for exponent in CLASSES[class_index]:
        value = l_add(value, l_power(ZETA, exponent))
    return value


def verify_field_split() -> dict[str, object]:
    """Check the finite-field factorization and invariant dimensions."""

    if P % 3 != 2:
        raise AssertionError("167 is no longer inert in Z[omega]")
    if not all(k_norm(value) for value in ((1, 0), (0, 1), (1, 1))):
        raise AssertionError("basic coefficient-field fixtures vanished")
    # x^2+x+1 has a root over F_p iff p=1 mod 3 (away from p=3).
    if any((value * value + value + 1) % P == 0 for value in range(P)):
        raise AssertionError("x^2+x+1 unexpectedly split over F_167")

    orders = {}
    for value in (P % N, Q % N):
        order = next(
            exponent
            for exponent in range(1, N)
            if pow(value, exponent, N) == 1
        )
        orders[value] = order
    if orders != {19: 36, 28: 18}:
        raise AssertionError("the residue orders modulo 37 changed")
    if tuple(pow(P, 12 * exponent, N) for exponent in range(3)) != H:
        raise AssertionError("H is no longer generated by 167^12 modulo 37")

    cyclotomic = [K_ONE] * N
    product = poly_multiply(FACTOR_PLUS, FACTOR_MINUS)
    if product != cyclotomic:
        raise AssertionError("the displayed factors do not multiply to Phi_37")
    conjugate_reciprocal = tuple(
        k_conjugate(value) for value in reversed(FACTOR_PLUS)
    )
    if conjugate_reciprocal != FACTOR_MINUS:
        raise AssertionError("the two factors are not star-conjugate")
    irreducible_plus = polynomial_is_irreducible(FACTOR_PLUS, Q)
    irreducible_minus = polynomial_is_irreducible(FACTOR_MINUS, Q)
    if not irreducible_plus or not irreducible_minus:
        raise AssertionError("a degree-18 factor failed irreducibility")

    if l_power(ZETA, N) != L_ONE or ZETA == L_ONE:
        raise AssertionError("zeta is not a primitive 37th root")
    even_periods = tuple(period(index) for index in range(0, 12, 2))
    odd_periods = tuple(period(index) for index in range(1, 12, 2))
    for value in even_periods + odd_periods:
        if l_power(value, P**12) != value:
            raise AssertionError("an H-period left the degree-six fixed field")
    even_rank = k_matrix_rank(
        tuple(tuple(value[index] for value in even_periods) for index in range(18))
    )
    odd_rank = k_matrix_rank(
        tuple(tuple(value[index] for value in odd_periods) for index in range(18))
    )
    if (even_rank, odd_rank) != (6, 6):
        raise AssertionError("the two period systems lost fixed-field rank six")

    certificate = (
        FACTOR_PLUS,
        FACTOR_MINUS,
        tuple(sorted(orders.items())),
        even_periods,
        odd_periods,
        even_rank,
        odd_rank,
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_FIELD_SPLIT_SHA256
        and certificate_hash != EXPECTED_FIELD_SPLIT_SHA256
    ):
        raise AssertionError("the field-split certificate changed")
    return {
        "p_mod_3": P % 3,
        "ord_37_p": orders[P % N],
        "ord_37_p_squared": orders[Q % N],
        "full_primitive_factor_degrees_over_k": (18, 18),
        "h_generator": pow(P, 12, N),
        "h_order": 3,
        "invariant_primitive_degrees_over_k": (6, 6),
        "invariant_primitive_field_size_exponents_over_f_p": (12, 12),
        "factor_irreducible": (irreducible_plus, irreducible_minus),
        "period_basis_ranks": (even_rank, odd_rank),
        "certificate_sha256": certificate_hash,
    }


def verify_star_and_roundtrip() -> dict[str, object]:
    """Replay the star exponents and inverse CRT on deterministic words."""

    if pow(P, 6, N) * pow(-1, -1, N) % N not in H:
        raise AssertionError("the plus star exponent is not H-equivalent")
    if pow(P, 7, N) * pow(-P, -1, N) % N not in H:
        raise AssertionError("the minus star exponent is not H-equivalent")
    if (5 + 7) % 12:
        raise AssertionError("the two fixed-field Frobenius powers are not inverse")

    certificates = []
    for seed in range(1, 7):
        word = deterministic_h_word(seed)
        first, plus, minus = crt_forward(word)
        if l_power(plus, P**12) != plus or l_power(minus, P**12) != minus:
            raise AssertionError("an invariant evaluation left E")
        recovered = crt_inverse(first, plus, minus)
        if recovered != word:
            raise AssertionError("the invariant CRT failed to round-trip")

        star_first, star_plus, star_minus = crt_forward(group_star(word))
        if star_first != k_conjugate(first):
            raise AssertionError("the trivial star coordinate changed")
        if star_plus != l_power(minus, P**5):
            raise AssertionError("the plus star exponent changed")
        if star_minus != l_power(plus, P**7):
            raise AssertionError("the minus star exponent changed")
        if crt_forward(group_star(group_star(word))) != (first, plus, minus):
            raise AssertionError("the CRT involution failed to square to one")
        certificates.append(
            (
                seed,
                first,
                plus,
                minus,
                compact_hash(recovered),
            )
        )
    certificate_hash = compact_hash(tuple(certificates))
    if certificate_hash != EXPECTED_STAR_CRT_FIXTURE_SHA256:
        raise AssertionError("the star/CRT fixture certificate changed")
    return {
        "roundtrip_fixtures": len(certificates),
        "plus_star_frobenius_exponent": 5,
        "minus_star_frobenius_exponent": 7,
        "star_exponent_sum_mod_12": (5 + 7) % 12,
        "certificate_sha256": certificate_hash,
    }


def field_fixture(seed: int) -> L:
    """Return a deterministic member of E=F_(167^12)."""

    source = deterministic_h_word(seed)
    return crt_forward(source)[1]


def primitive_parameterization(
    plus_a: L, plus_b: L, tau: L
) -> tuple[L, L]:
    """Return the two minus coordinates when ``(plus_a,plus_b) != 0``."""

    if plus_a == L_ZERO and plus_b == L_ZERO:
        raise ValueError("the nondegenerate branch needs a nonzero plus pair")
    for value in (plus_a, plus_b, tau):
        if l_power(value, P**12) != value:
            raise ValueError("a parameter lies outside E")
    minus_a = l_power(l_neg(l_multiply(tau, plus_b)), P**7)
    minus_b = l_power(l_multiply(tau, plus_a), P**7)
    return minus_a, minus_b


def primitive_degenerate_parameterization(
    minus_a: L, minus_b: L
) -> tuple[L, L]:
    """Parameterize ``plus_a=plus_b=0`` by two free minus coordinates."""

    for value in (minus_a, minus_b):
        if l_power(value, P**12) != value:
            raise ValueError("a degenerate parameter lies outside E")
    return minus_a, minus_b


def primitive_residual(
    plus_a: L, minus_a: L, plus_b: L, minus_b: L
) -> L:
    return l_add(
        l_multiply(plus_a, l_power(minus_a, P**5)),
        l_multiply(plus_b, l_power(minus_b, P**5)),
    )


def recover_primitive_parameters(
    plus_a: L, minus_a: L, plus_b: L, minus_b: L
) -> tuple[object, ...]:
    """Recover the unique parameters in either primitive branch."""

    for value in (plus_a, minus_a, plus_b, minus_b):
        if l_power(value, P**12) != value:
            raise ValueError("a primitive coordinate lies outside E")
    if primitive_residual(plus_a, minus_a, plus_b, minus_b) != L_ZERO:
        raise ValueError("the primitive coordinates do not solve the equation")
    if plus_a == L_ZERO and plus_b == L_ZERO:
        return "degenerate", minus_a, minus_b

    powered_minus_a = l_power(minus_a, P**5)
    powered_minus_b = l_power(minus_b, P**5)
    if plus_b != L_ZERO:
        tau = l_multiply(l_neg(powered_minus_a), l_inverse(plus_b))
    else:
        tau = l_multiply(powered_minus_b, l_inverse(plus_a))
    reconstructed = primitive_parameterization(plus_a, plus_b, tau)
    if reconstructed != (minus_a, minus_b):
        raise AssertionError("the recovered primitive parameter is not exact")
    return "nondegenerate", tau


TRIVIAL_NORM_MINUS_ONE_RATIO: K = (4, 36)


def trivial_residual(first: K, second: K) -> K:
    return k_add(
        k_multiply(first, k_conjugate(first)),
        k_multiply(second, k_conjugate(second)),
    )


def trivial_parameterization(scale: K, ratio: K) -> tuple[K, K]:
    """Return ``(scale,scale*ratio)`` for a norm-minus-one ratio."""

    normalized_scale = k_reduce(scale)
    normalized_ratio = k_reduce(ratio)
    if normalized_scale == K_ZERO:
        raise ValueError("the nonzero trivial branch needs a nonzero scale")
    if k_norm(normalized_ratio) != P - 1:
        raise ValueError("the trivial ratio must have norm minus one")
    return normalized_scale, k_multiply(normalized_scale, normalized_ratio)


def recover_trivial_parameters(first: K, second: K) -> tuple[object, ...]:
    """Recover the zero branch or the unique scale and ratio."""

    normalized_first = k_reduce(first)
    normalized_second = k_reduce(second)
    if trivial_residual(normalized_first, normalized_second) != K_ZERO:
        raise ValueError("the trivial coordinates do not solve the equation")
    if normalized_first == K_ZERO:
        if normalized_second != K_ZERO:
            raise AssertionError("the coefficient ring is not a field")
        return ("zero",)
    ratio = k_multiply(normalized_second, k_inverse(normalized_first))
    if k_norm(ratio) != P - 1:
        raise AssertionError("the recovered ratio lost norm minus one")
    return "nonzero", normalized_first, ratio


def audit_coordinate_solution(
    trivial_a: K,
    plus_a: L,
    minus_a: L,
    trivial_b: K,
    plus_b: L,
    minus_b: L,
) -> tuple[str, str]:
    """Inverse-CRT one spectral solution and verify it in the group ring."""

    if trivial_residual(trivial_a, trivial_b) != K_ZERO:
        raise ValueError("the trivial coordinates are not isotropic")
    if primitive_residual(plus_a, minus_a, plus_b, minus_b) != L_ZERO:
        raise ValueError("the primitive coordinates are not complementary")
    word_a = crt_inverse(trivial_a, plus_a, minus_a)
    word_b = crt_inverse(trivial_b, plus_b, minus_b)
    residual = group_add(
        group_multiply(word_a, group_star(word_a)),
        group_multiply(word_b, group_star(word_b)),
    )
    if any(value != K_ZERO for value in residual):
        raise AssertionError("an inverse-CRT solution is not complementary")
    if crt_forward(word_a) != (trivial_a, plus_a, minus_a):
        raise AssertionError("channel A failed the spectral round-trip")
    if crt_forward(word_b) != (trivial_b, plus_b, minus_b):
        raise AssertionError("channel B failed the spectral round-trip")
    return compact_hash(word_a), compact_hash(word_b)


def verify_parameterization() -> dict[str, object]:
    """Verify both trivial branches and both primitive branches."""

    norm_histogram = [0] * P
    norm_minus_one_ratios = []
    for first in range(P):
        for second in range(P):
            value = first, second
            norm = k_norm(value)
            norm_histogram[norm] += 1
            if norm == P - 1:
                norm_minus_one_ratios.append(value)
    if norm_histogram[0] != 1 or any(
        count != P + 1 for count in norm_histogram[1:]
    ):
        raise AssertionError("the coefficient-field norm fibers changed")
    if (
        len(norm_minus_one_ratios) != P + 1
        or TRIVIAL_NORM_MINUS_ONE_RATIO not in norm_minus_one_ratios
    ):
        raise AssertionError("the norm-minus-one ratio fiber changed")
    for ratio in norm_minus_one_ratios:
        coordinates = trivial_parameterization(K_ONE, ratio)
        if trivial_residual(*coordinates) != K_ZERO:
            raise AssertionError("a trivial-cone ratio failed")
        if recover_trivial_parameters(*coordinates) != (
            "nonzero",
            K_ONE,
            ratio,
        ):
            raise AssertionError("a trivial-cone ratio failed recovery")
    if recover_trivial_parameters(K_ZERO, K_ZERO) != ("zero",):
        raise AssertionError("the zero trivial branch failed recovery")

    nondegenerate_certificates = []
    for seed in range(1, 6):
        plus_a = field_fixture(10 + 3 * seed)
        plus_b = field_fixture(11 + 3 * seed)
        tau = field_fixture(12 + 3 * seed)
        if plus_a == L_ZERO and plus_b == L_ZERO:
            raise AssertionError("a parameter fixture hit the degenerate branch")
        minus_a, minus_b = primitive_parameterization(
            plus_a, plus_b, tau
        )
        if primitive_residual(plus_a, minus_a, plus_b, minus_b) != L_ZERO:
            raise AssertionError("the primitive parameterization failed")
        recovered = recover_primitive_parameters(
            plus_a, minus_a, plus_b, minus_b
        )
        if recovered != ("nondegenerate", tau):
            raise AssertionError("the kernel parameter was not recovered")
        nondegenerate_certificates.append(
            (
                "generic",
                seed,
                compact_hash(plus_a),
                compact_hash(plus_b),
                compact_hash(tau),
            )
        )

    axis_value = field_fixture(37)
    axis_tau = field_fixture(38)
    if axis_value == L_ZERO:
        raise AssertionError("the nondegenerate axis fixture vanished")
    for label, plus_a, plus_b in (
        ("A-axis", axis_value, L_ZERO),
        ("B-axis", L_ZERO, axis_value),
    ):
        minus_a, minus_b = primitive_parameterization(
            plus_a, plus_b, axis_tau
        )
        if recover_primitive_parameters(
            plus_a, minus_a, plus_b, minus_b
        ) != ("nondegenerate", axis_tau):
            raise AssertionError("a nondegenerate axis failed recovery")
        nondegenerate_certificates.append(
            (
                label,
                compact_hash(plus_a),
                compact_hash(plus_b),
                compact_hash(axis_tau),
            )
        )

    degenerate_certificates = []
    for seed in range(1, 4):
        minus_a, minus_b = primitive_degenerate_parameterization(
            field_fixture(40 + 2 * seed),
            field_fixture(41 + 2 * seed),
        )
        recovered = recover_primitive_parameters(
            L_ZERO, minus_a, L_ZERO, minus_b
        )
        if recovered != ("degenerate", minus_a, minus_b):
            raise AssertionError("the degenerate parameters were not recovered")
        degenerate_certificates.append(
            (seed, compact_hash(minus_a), compact_hash(minus_b))
        )

    nonzero_trivial = trivial_parameterization(
        (9, 14), TRIVIAL_NORM_MINUS_ONE_RATIO
    )
    nondegenerate_plus_a = field_fixture(61)
    nondegenerate_plus_b = field_fixture(62)
    nondegenerate_tau = field_fixture(63)
    nondegenerate_minus_a, nondegenerate_minus_b = (
        primitive_parameterization(
            nondegenerate_plus_a,
            nondegenerate_plus_b,
            nondegenerate_tau,
        )
    )
    degenerate_minus_a, degenerate_minus_b = (
        primitive_degenerate_parameterization(
            field_fixture(64),
            field_fixture(65),
        )
    )
    branch_fixtures = (
        (
            "trivial-zero/primitive-degenerate",
            K_ZERO,
            L_ZERO,
            degenerate_minus_a,
            K_ZERO,
            L_ZERO,
            degenerate_minus_b,
        ),
        (
            "trivial-zero/primitive-nondegenerate",
            K_ZERO,
            nondegenerate_plus_a,
            nondegenerate_minus_a,
            K_ZERO,
            nondegenerate_plus_b,
            nondegenerate_minus_b,
        ),
        (
            "trivial-nonzero/primitive-degenerate",
            nonzero_trivial[0],
            L_ZERO,
            degenerate_minus_a,
            nonzero_trivial[1],
            L_ZERO,
            degenerate_minus_b,
        ),
        (
            "trivial-nonzero/primitive-nondegenerate",
            nonzero_trivial[0],
            nondegenerate_plus_a,
            nondegenerate_minus_a,
            nonzero_trivial[1],
            nondegenerate_plus_b,
            nondegenerate_minus_b,
        ),
    )
    branch_certificates = tuple(
        (fixture[0],) + audit_coordinate_solution(*fixture[1:])
        for fixture in branch_fixtures
    )

    trivial_solution_count = 1 + (Q - 1) * (P + 1)
    primitive_degenerate_solution_count = E_SIZE**2
    primitive_nondegenerate_solution_count = (E_SIZE**2 - 1) * E_SIZE
    primitive_solution_count = (
        primitive_degenerate_solution_count
        + primitive_nondegenerate_solution_count
    )
    full_solution_count = trivial_solution_count * primitive_solution_count
    certificate = (
        tuple(norm_histogram),
        tuple(norm_minus_one_ratios),
        tuple(nondegenerate_certificates),
        tuple(degenerate_certificates),
        branch_certificates,
        trivial_solution_count,
        primitive_degenerate_solution_count,
        primitive_nondegenerate_solution_count,
        full_solution_count,
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_PARAMETER_FIXTURE_SHA256
        and certificate_hash != EXPECTED_PARAMETER_FIXTURE_SHA256
    ):
        raise AssertionError("the parameter fixture certificate changed")
    return {
        "trivial_zero_branch_solutions": 1,
        "trivial_nonzero_branch_solutions": (Q - 1) * (P + 1),
        "trivial_solution_count": trivial_solution_count,
        "norm_minus_one_ratio_count": len(norm_minus_one_ratios),
        "trivial_norm_minus_one_ratio": TRIVIAL_NORM_MINUS_ONE_RATIO,
        "nondegenerate_parameter_fixtures": len(
            nondegenerate_certificates
        ),
        "degenerate_parameter_fixtures": len(degenerate_certificates),
        "primitive_degenerate_solution_count": (
            primitive_degenerate_solution_count
        ),
        "primitive_nondegenerate_solution_count": (
            primitive_nondegenerate_solution_count
        ),
        "primitive_solution_count": primitive_solution_count,
        "full_solution_count": full_solution_count,
        "primitive_free_parameter_field_exponent_over_f_p": 12,
        "trivial_branches": ("zero", "nonzero"),
        "primitive_branches": ("degenerate", "nondegenerate"),
        "solution_branch_fixtures": len(branch_certificates),
        "inverse_crt_complementary_fixtures": len(branch_certificates),
        "parameterization_complete": True,
        "certificate_sha256": certificate_hash,
    }


# ---------------------------------------------------------------------------
# Exact energy-shell theorem and the existing profile fixtures.


def integer_e_norm(value: tuple[int, int]) -> int:
    first, second = value
    return first * first - first * second + second * second


def exact_energy(
    first: Sequence[tuple[int, int]], second: Sequence[tuple[int, int]]
) -> int:
    return sum(integer_e_norm(value) for value in tuple(first) + tuple(second))


def exact_correlations(
    first: Sequence[tuple[int, int]], second: Sequence[tuple[int, int]]
) -> tuple[tuple[int, int], ...]:
    if len(first) != N or len(second) != N:
        raise ValueError("expected two length-37 sequences")

    def multiply(
        left: tuple[int, int], right: tuple[int, int]
    ) -> tuple[int, int]:
        a, b = left
        c, d = right
        return a * c - b * d, a * d + b * c - b * d

    def conjugate(value: tuple[int, int]) -> tuple[int, int]:
        return value[0] - value[1], -value[1]

    result = []
    for lag in range(N):
        total = (0, 0)
        for sequence in (first, second):
            for index in range(N):
                product = multiply(
                    sequence[(index + lag) % N],
                    conjugate(sequence[index]),
                )
                total = total[0] + product[0], total[1] + product[1]
        result.append(total)
    return tuple(result)


def reduced_word(
    sequence: Sequence[tuple[int, int]]
) -> tuple[K, ...]:
    return tuple(k_reduce(value) for value in sequence)


def verify_profile_corpus() -> dict[str, object]:
    """Replay prime-167 exactness and split signatures on 22 fixed tuples."""

    certificate = []
    modular_survivors = 0
    exact_survivors = 0
    minimum_strict_gap = P * P
    for index, (target, identifiers_a, identifiers_b) in enumerate(
        PROFILE9_SHARD_WITNESSES
    ):
        first = profile_column_values(0, identifiers_a)
        second = profile_column_values(1, identifiers_b)
        energy = exact_energy(first, second)
        if energy != P:
            raise AssertionError("a profile fixture left the energy-167 shell")
        correlations = exact_correlations(first, second)
        if correlations[0] != (P, 0):
            raise AssertionError("the origin correlation changed")

        exact_pass = all(value == (0, 0) for value in correlations[1:])
        modular_pass = all(
            value[0] % P == 0 and value[1] % P == 0
            for value in correlations
        )
        if exact_pass != modular_pass:
            raise AssertionError("prime-167 exactness failed on a profile fixture")
        exact_survivors += int(exact_pass)
        modular_survivors += int(modular_pass)

        word_a = reduced_word(first)
        word_b = reduced_word(second)
        trivial_a, plus_a, minus_a = crt_forward(word_a)
        trivial_b, plus_b, minus_b = crt_forward(word_b)
        trivial_residual = k_add(
            k_multiply(trivial_a, k_conjugate(trivial_a)),
            k_multiply(trivial_b, k_conjugate(trivial_b)),
        )
        primitive = primitive_residual(
            plus_a, minus_a, plus_b, minus_b
        )
        split_pass = trivial_residual == K_ZERO and primitive == L_ZERO
        if split_pass != modular_pass:
            raise AssertionError("the split predicate disagrees with correlations")

        maximum_modulus_squared = max(
            integer_e_norm(value) for value in correlations[1:]
        )
        if maximum_modulus_squared > P * P:
            raise AssertionError("a fixture violates the Cauchy disk")
        # The theorem proves strictness abstractly.  The corpus is also a
        # useful deterministic negative control with a visible strict gap.
        minimum_strict_gap = min(
            minimum_strict_gap,
            P * P - maximum_modulus_squared,
        )
        certificate.append(
            (
                index,
                target,
                trivial_residual,
                compact_hash(primitive),
                modular_pass,
                maximum_modulus_squared,
            )
        )

    certificate_hash = compact_hash(tuple(certificate))
    if (
        EXPECTED_PROFILE_SIGNATURE_SHA256
        and certificate_hash != EXPECTED_PROFILE_SIGNATURE_SHA256
    ):
        raise AssertionError("the profile split-signature corpus changed")
    if modular_survivors or exact_survivors:
        raise AssertionError("a fixed profile tuple unexpectedly became complementary")
    return {
        "energy_shell_fixtures": len(certificate),
        "prime167_modular_survivors": modular_survivors,
        "exact_profile_survivors": exact_survivors,
        "aggregate_shard_exclusions": 0,
        "strict_cauchy_gap_on_fixed_corpus": minimum_strict_gap,
        "certificate_sha256": certificate_hash,
    }


def verify_equality_case_arithmetic() -> dict[str, object]:
    """Replay the numerical and root-of-unity facts in the exactness proof."""

    if gcd(6, N) != 1:
        raise AssertionError("mu_6 and mu_37 no longer intersect trivially")
    if P % N == 0:
        raise AssertionError("37 unexpectedly divides the target energy")
    # A nonzero Eisenstein integer has norm at least one, with equality
    # exactly at the six units.  Exhaust a box containing all norm-one points.
    units = tuple(
        (a, b)
        for a in range(-2, 3)
        for b in range(-2, 3)
        if integer_e_norm((a, b)) == 1
    )
    expected_units = ((-1, -1), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 1))
    if units != expected_units:
        raise AssertionError("the Eisenstein unit census changed")
    certificate = (
        P,
        N,
        gcd(6, N),
        P % N,
        units,
        P * P,
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_EQUALITY_CASE_SHA256
        and certificate_hash != EXPECTED_EQUALITY_CASE_SHA256
    ):
        raise AssertionError("the equality-case certificate changed")
    return {
        "correlation_modulus": P,
        "energy": P,
        "shift_order": N,
        "roots_of_unity_in_q_omega": 6,
        "root_of_unity_intersection_order": gcd(6, N),
        "energy_divisible_by_shift_order": P % N == 0,
        "eisenstein_units": units,
        "certificate_sha256": certificate_hash,
        "conclusion": (
            "a nonzero 167-divisible correlation would force Cauchy equality; "
            "translation eigenvalue lies in mu_6 intersect mu_37={1}, making "
            "both channels constant and their energy divisible by 37"
        ),
    }


def verify() -> dict[str, object]:
    return {
        "equality_case": verify_equality_case_arithmetic(),
        "field_split": verify_field_split(),
        "star_and_crt": verify_star_and_roundtrip(),
        "parameterization": verify_parameterization(),
        "profile_corpus": verify_profile_corpus(),
        "status": (
            "energy-167 exact complementarity is equivalent to the split "
            "prime-167 equations; the H-invariant finite-field solution cone "
            "is fully parameterized, but no physical profile tuple or "
            "LP(333) is asserted"
        ),
    }


def main() -> None:
    result = verify()
    split = result["field_split"]
    star = result["star_and_crt"]
    parameterization = result["parameterization"]
    corpus = result["profile_corpus"]
    print(
        "full_primitive_factor_degrees_over_k="
        f"{split['full_primitive_factor_degrees_over_k']}"
    )
    print(
        "invariant_primitive_degrees_over_k="
        f"{split['invariant_primitive_degrees_over_k']}"
    )
    print(
        "star_frobenius_exponents="
        f"({star['plus_star_frobenius_exponent']},"
        f"{star['minus_star_frobenius_exponent']})"
    )
    print(
        "inverse_crt_complementary_fixtures="
        f"{parameterization['inverse_crt_complementary_fixtures']}"
    )
    print(
        "finite_field_solution_count="
        f"{parameterization['full_solution_count']}"
    )
    print(
        "equality_case_certificate_sha256="
        f"{result['equality_case']['certificate_sha256']}"
    )
    print(
        "field_split_certificate_sha256="
        f"{split['certificate_sha256']}"
    )
    print(
        "star_crt_certificate_sha256="
        f"{star['certificate_sha256']}"
    )
    print(
        "parameterization_certificate_sha256="
        f"{parameterization['certificate_sha256']}"
    )
    print(
        "profile_signature_certificate_sha256="
        f"{corpus['certificate_sha256']}"
    )
    print("PASS: prime-167 split and parameterization replayed exactly")
    print("STATUS: constructive profile-search architecture; no LP(333) found")


if __name__ == "__main__":
    main()
