#!/usr/bin/env python3
"""Verify prime-167 exactness for the full six-sequence phase frame.

The order-three phase factorization gives six sparse Eisenstein sequences
with total support 167.  Its two independent group-ring equations are

    E0 = sum_i U_i U_i^* = 167 e,
    E1 = sum_i (P U)_i U_i^* = 0,

where on each channel

    P(U0,U1,U2) = (U1,U2,omega^2 U0),   P^3=omega^2.

This module checks the equality-case orbit obstruction that makes reduction
modulo 167 exact for *both* equations.  It also checks the complete
``k x E x E`` coordinate equations and the three-plane annihilator form of
the primitive equations.  Arithmetic is exact and uses only the Python
standard library plus the repository's independently checked finite-field
module.
"""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Sequence

from verify_lp333_order3_labeled_jet import ZERO_A_PLUS, ZERO_B_PLUS
from verify_lp333_order3_phase_factor import fiber_phase
import verify_lp333_order3_prime167_split as split


Eisenstein = tuple[int, int]  # a+b*omega, omega^2+omega+1=0.
ExactWord = tuple[Eisenstein, ...]
ExactFrame = tuple[ExactWord, ...]

P = 167
N = 37
ENERGY = 167

E_ZERO: Eisenstein = (0, 0)
E_ONE: Eisenstein = (1, 0)
E_OMEGA: Eisenstein = (0, 1)
E_OMEGA2: Eisenstein = (-1, -1)
E_ROOTS = (E_ONE, E_OMEGA, E_OMEGA2)

K_OMEGA: split.K = (0, 1)
K_OMEGA2: split.K = split.k_multiply(K_OMEGA, K_OMEGA)

EXPECTED_ORBIT_CERTIFICATE_SHA256 = (
    "c74bc225f3d350b8ca81f118a1ca1796b676dbb6a992c0f3b6bd7dd3cf506011"
)
EXPECTED_FRAME_CERTIFICATE_SHA256 = (
    "29bdb7ab3d7ba49e8be0e32df70592ea5d4314f27c49e3664efd1504ac30c630"
)
EXPECTED_CRT_CERTIFICATE_SHA256 = (
    "3705a0b73069eec04ca5a65fd00aa38f6f829f6d2d388d519312c3a7e6c99694"
)
EXPECTED_PLANE_CERTIFICATE_SHA256 = (
    "3294fad8192a163fefdcaaaee120601ebed3fda20c0ef4db4501d268b91c2257"
)
EXPECTED_RECOMBINED_CERTIFICATE_SHA256 = (
    "cc86f194497dd5b6bc9139d9a299e888596dc99d98cf4b768730a605af0dafac"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


# ---------------------------------------------------------------------------
# Exact Eisenstein and group-ring arithmetic.


def e_add(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return left[0] + right[0], left[1] + right[1]


def e_neg(value: Eisenstein) -> Eisenstein:
    return -value[0], -value[1]


def e_subtract(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return e_add(left, e_neg(right))


def e_multiply(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def e_conjugate(value: Eisenstein) -> Eisenstein:
    return value[0] - value[1], -value[1]


def e_norm(value: Eisenstein) -> int:
    a, b = value
    return a * a - a * b + b * b


def e_power(value: Eisenstein, exponent: int) -> Eisenstein:
    if exponent < 0:
        if e_norm(value) != 1:
            raise ValueError("negative powers are used only for units")
        return e_power(e_conjugate(value), -exponent)
    result = E_ONE
    base = value
    while exponent:
        if exponent & 1:
            result = e_multiply(result, base)
        base = e_multiply(base, base)
        exponent //= 2
    return result


def exact_group_star(word: Sequence[Eisenstein]) -> ExactWord:
    if len(word) != N:
        raise ValueError("expected a C_37 word")
    return tuple(e_conjugate(word[-index % N]) for index in range(N))


def exact_group_multiply(
    left: Sequence[Eisenstein], right: Sequence[Eisenstein]
) -> ExactWord:
    if len(left) != N or len(right) != N:
        raise ValueError("expected two C_37 words")
    result = [E_ZERO] * N
    for left_index, left_value in enumerate(left):
        if left_value == E_ZERO:
            continue
        for right_index, right_value in enumerate(right):
            if right_value == E_ZERO:
                continue
            target = (left_index + right_index) % N
            result[target] = e_add(
                result[target], e_multiply(left_value, right_value)
            )
    return tuple(result)


def exact_group_inner(
    left: Sequence[Sequence[Eisenstein]],
    right: Sequence[Sequence[Eisenstein]],
) -> ExactWord:
    if len(left) != 6 or len(right) != 6:
        raise ValueError("the phase frame has six sequences")
    result = [E_ZERO] * N
    for left_word, right_word in zip(left, right):
        product = exact_group_multiply(
            left_word, exact_group_star(right_word)
        )
        result = [e_add(a, b) for a, b in zip(result, product)]
    return tuple(result)


def scale_exact_word(
    scalar: Eisenstein, word: Sequence[Eisenstein]
) -> ExactWord:
    return tuple(e_multiply(scalar, value) for value in word)


def twist_exact_frame(frame: Sequence[Sequence[Eisenstein]]) -> ExactFrame:
    """Apply P=(0 1 0;0 0 1;omega^2 0 0) on each channel."""

    if len(frame) != 6:
        raise ValueError("the phase frame has six sequences")
    result: list[ExactWord] = []
    for channel_start in (0, 3):
        first, second, third = frame[channel_start : channel_start + 3]
        result.extend(
            (
                tuple(second),
                tuple(third),
                scale_exact_word(E_OMEGA2, first),
            )
        )
    return tuple(result)


def exact_equations(frame: ExactFrame) -> tuple[ExactWord, ExactWord]:
    return (
        exact_group_inner(frame, frame),
        exact_group_inner(twist_exact_frame(frame), frame),
    )


def reduce_word(word: Sequence[Eisenstein]) -> tuple[split.K, ...]:
    return tuple((value[0] % P, value[1] % P) for value in word)


def exact_word_is_zero(word: Sequence[Eisenstein]) -> bool:
    return all(value == E_ZERO for value in word)


def exact_diagonal_target(word: Sequence[Eisenstein]) -> bool:
    return (
        len(word) == N
        and word[0] == (ENERGY, 0)
        and exact_word_is_zero(word[1:])
    )


def word_is_zero_mod_167(word: Sequence[Eisenstein]) -> bool:
    return all(value[0] % P == 0 and value[1] % P == 0 for value in word)


# ---------------------------------------------------------------------------
# Twisted-cycle equality obstruction.


def permutation_cycle_lengths(lag: int, twisted: bool) -> tuple[int, ...]:
    """Cycle lengths on one channel's 3 x 37 coordinate set."""

    if not 0 <= lag < N:
        raise ValueError("lag must lie in C_37")
    coordinates = tuple((residue, column) for residue in range(3)
                        for column in range(N))
    unseen = set(coordinates)
    lengths = []
    while unseen:
        start = min(unseen)
        current = start
        length = 0
        while current in unseen:
            unseen.remove(current)
            residue, column = current
            if twisted:
                current = ((residue + 1) % 3, (column + lag) % N)
            else:
                current = (residue, (column + lag) % N)
            length += 1
        if current != start:
            raise AssertionError("the coordinate map failed to close a cycle")
        lengths.append(length)
    return tuple(sorted(lengths))


def verify_equality_orbits() -> dict[str, object]:
    """Check every numerical ingredient of both Cauchy equality cases."""

    units = tuple(
        (a, b)
        for a in range(-2, 3)
        for b in range(-2, 3)
        if e_norm((a, b)) == 1
    )
    expected_units = ((-1, -1), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 1))
    if units != expected_units:
        raise AssertionError("the Eisenstein unit census changed")

    # Check P^3=omega^2 on an algebraically independent coordinate fixture.
    triple_frame: ExactFrame = tuple(
        ((E_ONE,) + (E_ZERO,) * (N - 1))
        if index == 0
        else ((E_ZERO,) * N)
        for index in range(6)
    )
    twisted_three = triple_frame
    for _ in range(3):
        twisted_three = twist_exact_frame(twisted_three)
    expected_three = tuple(
        scale_exact_word(E_OMEGA2, word) for word in triple_frame
    )
    if twisted_three != expected_three:
        raise AssertionError("the phase twist no longer satisfies P^3=omega^2")

    diagonal_cycle_sets = tuple(
        tuple(sorted(set(permutation_cycle_lengths(lag, False))))
        for lag in range(1, N)
    )
    if set(diagonal_cycle_sets) != {(N,)}:
        raise AssertionError("a nonzero C_37 translation lost order 37")

    cross_zero = permutation_cycle_lengths(0, True)
    cross_nonzero = tuple(
        tuple(sorted(set(permutation_cycle_lengths(lag, True))))
        for lag in range(1, N)
    )
    if set(cross_zero) != {3} or set(cross_nonzero) != {(3 * N,)}:
        raise AssertionError("the twisted-cycle orbit lengths changed")

    # Over a complete twisted orbit, Q^ell is multiplication by omega^2:
    # ell=3 at lag zero and ell=111 at nonzero lag.
    twist_scalars = tuple(
        e_power(E_OMEGA2, orbit_length // 3)
        for orbit_length in (3, 3 * N)
    )
    if twist_scalars != (E_OMEGA2, E_OMEGA2):
        raise AssertionError("the complete twisted-orbit phase changed")
    if any(
        e_power(unit, orbit_length) == E_OMEGA2
        for unit in units
        for orbit_length in (3, 3 * N)
    ):
        raise AssertionError("an Eisenstein unit became a twisted eigenvalue")

    if (
        ENERGY % N == 0
        or ENERGY % 3 == 0
        or ENERGY % (3 * N) == 0
    ):
        raise AssertionError("support 167 became a union of equality orbits")

    certificate = (
        units,
        N,
        ENERGY,
        tuple(sorted(set(diagonal_cycle_sets))),
        tuple(sorted(set(cross_zero))),
        tuple(sorted(set(cross_nonzero))),
        twist_scalars,
        (ENERGY % N, ENERGY % 3, ENERGY % (3 * N)),
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_ORBIT_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_ORBIT_CERTIFICATE_SHA256
    ):
        raise AssertionError("the equality-orbit certificate changed")
    return {
        "eisenstein_units": units,
        "diagonal_nonzero_lag_orbit": N,
        "cross_zero_lag_orbit": 3,
        "cross_nonzero_lag_orbit": 3 * N,
        "twisted_orbit_scalar": E_OMEGA2,
        "support_remainders": (
            ENERGY % N,
            ENERGY % 3,
            ENERGY % (3 * N),
        ),
        "certificate_sha256": certificate_hash,
    }


# ---------------------------------------------------------------------------
# Deterministic locally valid support-167 phase fixtures.


def locally_valid_phase_frame(seed: int) -> ExactFrame:
    """Build an H-invariant unit/zero frame with support 5+3*54=167.

    Eighteen of the 24 nonzero channel/class profiles are ``(1,1,1)``
    (three active fibers), and six are ``(3,0,0)`` (no active fibers).
    This realizes profile norm 54 and exactly 54 active class fibers.
    """

    mutable = [[E_ZERO for _ in range(N)] for _ in range(6)]
    zero_words = (ZERO_A_PLUS, ZERO_B_PLUS)
    for channel in range(2):
        for residue in range(3):
            mutable[3 * channel + residue][0] = fiber_phase(
                zero_words[channel], residue
            )

    profile_slots = tuple(range(24))
    active_slots = set(
        sorted(
            profile_slots,
            key=lambda slot: (
                ((slot + 1) * (29 + 2 * seed) + 17 * seed * seed) % 101,
                slot,
            ),
        )[:18]
    )
    for slot in active_slots:
        channel, class_index = divmod(slot, 12)
        for residue in range(3):
            phase = E_ROOTS[
                (seed + 5 * channel + 7 * class_index + residue) % 3
            ]
            for column in split.CLASSES[class_index]:
                mutable[3 * channel + residue][column] = phase

    frame = tuple(tuple(word) for word in mutable)
    support = sum(value != E_ZERO for word in frame for value in word)
    if support != ENERGY:
        raise AssertionError("the deterministic phase frame lost support 167")
    if any(
        value != E_ZERO and e_norm(value) != 1
        for word in frame
        for value in word
    ):
        raise AssertionError("the phase alphabet left zero plus Eisenstein units")
    if not all(split.is_h_invariant(reduce_word(word)) for word in frame):
        raise AssertionError("the deterministic phase frame lost H-invariance")
    return frame


def verify_phase_fixtures() -> dict[str, object]:
    certificates = []
    for seed in (1, 2, 3):
        frame = locally_valid_phase_frame(seed)
        diagonal, cross = exact_equations(frame)
        support = sum(value != E_ZERO for word in frame for value in word)
        if diagonal[0] != (support, 0):
            raise AssertionError("the diagonal origin coefficient lost the energy")
        if max(map(e_norm, diagonal)) > ENERGY * ENERGY:
            raise AssertionError("a diagonal coefficient violated Cauchy's bound")
        if max(map(e_norm, cross)) > ENERGY * ENERGY:
            raise AssertionError("a cross coefficient violated Cauchy's bound")

        exact_diagonal = exact_diagonal_target(diagonal)
        modular_diagonal = word_is_zero_mod_167(diagonal)
        exact_cross = exact_word_is_zero(cross)
        modular_cross = word_is_zero_mod_167(cross)
        if exact_diagonal != modular_diagonal:
            raise AssertionError("diagonal exact/mod-167 predicates disagree")
        if exact_cross != modular_cross:
            raise AssertionError("cross exact/mod-167 predicates disagree")
        if any(e_norm(value) == ENERGY * ENERGY for value in diagonal[1:]):
            raise AssertionError("a nonzero-lag diagonal equality case survived")
        if any(e_norm(value) == ENERGY * ENERGY for value in cross):
            raise AssertionError("a twisted equality case survived")

        certificates.append(
            (
                seed,
                support,
                exact_diagonal,
                modular_diagonal,
                exact_cross,
                modular_cross,
                max(e_norm(value) for value in diagonal[1:]),
                max(map(e_norm, cross)),
                compact_hash((diagonal, cross)),
            )
        )
    certificate_hash = compact_hash(tuple(certificates))
    if (
        EXPECTED_FRAME_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_FRAME_CERTIFICATE_SHA256
    ):
        raise AssertionError("the support-167 frame certificate changed")
    return {
        "fixtures": len(certificates),
        "support_per_fixture": ENERGY,
        "active_nonzero_class_fibers": 54,
        "active_zero_column_fibers": 5,
        "exact_modular_predicates_agree": True,
        "certificate_sha256": certificate_hash,
    }


# ---------------------------------------------------------------------------
# Full k x E x E equations.


def k_dot(left: Sequence[split.K], right: Sequence[split.K]) -> split.K:
    result = split.K_ZERO
    for first, second in zip(left, right):
        result = split.k_add(result, split.k_multiply(first, second))
    return result


def l_dot(left: Sequence[split.L], right: Sequence[split.L]) -> split.L:
    result = split.L_ZERO
    for first, second in zip(left, right):
        result = split.l_add(result, split.l_multiply(first, second))
    return result


def twist_k_vector(
    vector: Sequence[split.K], scalar: split.K
) -> tuple[split.K, ...]:
    if len(vector) != 6:
        raise ValueError("expected two three-fiber channels")
    result = []
    for start in (0, 3):
        first, second, third = vector[start : start + 3]
        result.extend((second, third, split.k_multiply(scalar, first)))
    return tuple(result)


def twist_l_vector(
    vector: Sequence[split.L], scalar: split.K
) -> tuple[split.L, ...]:
    if len(vector) != 6:
        raise ValueError("expected two three-fiber channels")
    result = []
    for start in (0, 3):
        first, second, third = vector[start : start + 3]
        result.extend((second, third, split.l_scale(first, scalar)))
    return tuple(result)


def group_inner_mod(
    left: Sequence[Sequence[split.K]],
    right: Sequence[Sequence[split.K]],
) -> tuple[split.K, ...]:
    result = (split.K_ZERO,) * N
    for first, second in zip(left, right):
        result = split.group_add(
            result,
            split.group_multiply(first, split.group_star(second)),
        )
    return result


def twist_mod_frame(
    frame: Sequence[Sequence[split.K]],
) -> tuple[tuple[split.K, ...], ...]:
    result = []
    for start in (0, 3):
        first, second, third = frame[start : start + 3]
        result.extend(
            (
                tuple(second),
                tuple(third),
                tuple(
                    split.k_multiply(K_OMEGA2, value) for value in first
                ),
            )
        )
    return tuple(result)


def finite_coordinate_audit(frame: ExactFrame) -> dict[str, object]:
    """Compare direct group products with every displayed CRT equation."""

    reduced = tuple(reduce_word(word) for word in frame)
    twisted = twist_mod_frame(reduced)
    diagonal_word = group_inner_mod(reduced, reduced)
    cross_word = group_inner_mod(twisted, reduced)
    diagonal_crt = split.crt_forward(diagonal_word)
    cross_crt = split.crt_forward(cross_word)

    coordinates = tuple(split.crt_forward(word) for word in reduced)
    c = tuple(value[0] for value in coordinates)
    x = tuple(value[1] for value in coordinates)
    y = tuple(value[2] for value in coordinates)
    sigma_y = tuple(split.l_power(value, P**5) for value in y)
    rho_x = tuple(split.l_power(value, P**7) for value in x)

    diagonal_formula = (
        k_dot(c, tuple(split.k_conjugate(value) for value in c)),
        l_dot(x, sigma_y),
        l_dot(y, rho_x),
    )
    pc = twist_k_vector(c, K_OMEGA2)
    px = twist_l_vector(x, K_OMEGA2)
    py = twist_l_vector(y, K_OMEGA2)
    cross_formula = (
        k_dot(pc, tuple(split.k_conjugate(value) for value in c)),
        l_dot(px, sigma_y),
        l_dot(py, rho_x),
    )
    if diagonal_crt != diagonal_formula:
        raise AssertionError("the diagonal CRT formula changed")
    if cross_crt != cross_formula:
        raise AssertionError("the directed-cross CRT formula changed")
    if diagonal_formula[0][1] != 0:
        raise AssertionError("the trivial diagonal coordinate left F_167")
    if diagonal_formula[2] != split.l_power(diagonal_formula[1], P**7):
        raise AssertionError("the diagonal primitive coordinates lost adjointness")

    # Put Z=sigma(Y).  The three primitive equations become
    # X dot bar(P)^r Z=0 for r=0,1,2.
    z = sigma_y
    bar_p_z = twist_l_vector(z, K_OMEGA)
    bar_p_squared_z = twist_l_vector(bar_p_z, K_OMEGA)
    plane_residuals = (
        l_dot(x, z),
        l_dot(x, bar_p_z),
        l_dot(x, bar_p_squared_z),
    )
    if plane_residuals[0] != diagonal_formula[1]:
        raise AssertionError("the first plane equation changed")
    if plane_residuals[1] != split.l_power(cross_formula[2], P**5):
        raise AssertionError("the minus cross coordinate has the wrong exponent")
    if cross_formula[1] != split.l_scale(
        plane_residuals[2], K_OMEGA2
    ):
        raise AssertionError("the plus cross coordinate has the wrong twist")

    return {
        "diagonal_crt_hash": compact_hash(diagonal_crt),
        "cross_crt_hash": compact_hash(cross_crt),
        "coordinate_hash": compact_hash(coordinates),
        "plane_residual_hash": compact_hash(plane_residuals),
    }


def l_matrix_rank(rows: Sequence[Sequence[split.L]]) -> int:
    work = [list(row) for row in rows]
    if not work:
        return 0
    rank = 0
    column_count = len(work[0])
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column] != split.L_ZERO
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = split.l_inverse(work[rank][column])
        work[rank] = [
            split.l_multiply(value, inverse) for value in work[rank]
        ]
        for row in range(len(work)):
            if row == rank:
                continue
            factor = work[row][column]
            if factor != split.L_ZERO:
                work[row] = [
                    split.l_subtract(
                        left, split.l_multiply(factor, right)
                    )
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def verify_primitive_plane() -> dict[str, object]:
    """Check the dimension reduction behind the finite-field search."""

    # A generic deterministic Z has a three-dimensional Pbar-orbit plane.
    z = tuple(split.field_fixture(200 + index) for index in range(6))
    orbit_rows = [z]
    for _ in range(2):
        orbit_rows.append(
            twist_l_vector(orbit_rows[-1], K_OMEGA)
        )
    rank = l_matrix_rank(orbit_rows)
    if rank != 3:
        raise AssertionError("the generic twisted orbit plane lost rank three")

    # An explicit solution: Z is supported in channel A and X in channel B.
    z_axis = (
        split.L_ONE,
        split.field_fixture(211),
        split.field_fixture(212),
        split.L_ZERO,
        split.L_ZERO,
        split.L_ZERO,
    )
    x_axis = (
        split.L_ZERO,
        split.L_ZERO,
        split.L_ZERO,
        split.field_fixture(213),
        split.field_fixture(214),
        split.field_fixture(215),
    )
    axis_rows = [z_axis]
    for _ in range(2):
        axis_rows.append(
            twist_l_vector(axis_rows[-1], K_OMEGA)
        )
    if l_matrix_rank(axis_rows) != 3:
        raise AssertionError("the channel-axis orbit plane lost rank three")
    residuals = tuple(l_dot(x_axis, row) for row in axis_rows)
    if residuals != (split.L_ZERO,) * 3:
        raise AssertionError("the explicit three-plane annihilator failed")

    certificate = (
        rank,
        6 - rank,
        compact_hash(tuple(orbit_rows)),
        compact_hash(tuple(axis_rows)),
        compact_hash(residuals),
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_PLANE_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_PLANE_CERTIFICATE_SHA256
    ):
        raise AssertionError("the primitive-plane certificate changed")
    return {
        "generic_orbit_plane_rank": rank,
        "generic_annihilator_dimension": 6 - rank,
        "maximum_equation_rank": 3,
        "explicit_annihilator_fixture": True,
        "certificate_sha256": certificate_hash,
    }


# ---------------------------------------------------------------------------
# Stronger ninth-root recombination: F_(167^6) x F_(167^12)^6.


def ninth_root_of_unity() -> split.L:
    """Return the pinned alpha in E with alpha^3=omega and alpha^9=1."""

    candidate = split.l_power(
        split.field_fixture(2), (split.E_SIZE - 1) // 9
    )
    embedded_omega = split.l_embed(K_OMEGA)
    if split.l_power(candidate, 3) == split.l_embed(K_OMEGA2):
        candidate = split.l_inverse(candidate)
    if split.l_power(candidate, 3) != embedded_omega:
        raise AssertionError("the pinned ninth root no longer cubes to omega")
    if (
        split.l_power(candidate, 9) != split.L_ONE
        or split.l_power(candidate, P**6) != candidate
        or split.l_power(candidate, P**3) != split.l_inverse(candidate)
    ):
        raise AssertionError("the pinned ninth root left F_(167^6)")
    return candidate


def l_polynomial_evaluate(
    coefficients: Sequence[split.L], point: split.L
) -> split.L:
    result = split.L_ZERO
    for coefficient in reversed(coefficients):
        result = split.l_add(
            split.l_multiply(result, point), coefficient
        )
    return result


def l_group_star_ninth(word: Sequence[split.L]) -> tuple[split.L, ...]:
    """Cyclotomic star: coefficient p^3-Frobenius plus C_37 inversion."""

    if len(word) != N:
        raise ValueError("expected a C_37 word over F_(167^6)")
    return tuple(
        split.l_power(word[-index % N], P**3) for index in range(N)
    )


def integer_is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def recombined_word(
    three_words: Sequence[Sequence[split.K]], alpha: split.L
) -> tuple[split.L, ...]:
    """Return U0+alpha U1+alpha^2 U2 coefficientwise."""

    if len(three_words) != 3 or any(len(word) != N for word in three_words):
        raise ValueError("expected three length-37 fiber words")
    alpha_squared = split.l_multiply(alpha, alpha)
    result = []
    for column in range(N):
        value = split.l_embed(three_words[0][column])
        value = split.l_add(
            value,
            split.l_multiply(
                alpha, split.l_embed(three_words[1][column])
            ),
        )
        value = split.l_add(
            value,
            split.l_multiply(
                alpha_squared, split.l_embed(three_words[2][column])
            ),
        )
        result.append(value)
    return tuple(result)


def recombined_coordinates(
    word: Sequence[split.L],
) -> tuple[split.L, tuple[split.L, ...]]:
    """Return the F_(p^6) origin and six primitive F_(p^12) coordinates."""

    if len(word) != N:
        raise ValueError("expected a C_37 word")
    origin = split.L_ZERO
    for value in word:
        origin = split.l_add(origin, value)
    primitive = tuple(
        l_polynomial_evaluate(word, split.l_power(split.ZETA, P**index))
        for index in range(6)
    )
    if split.l_power(origin, P**6) != origin:
        raise AssertionError("the recombined origin left F_(167^6)")
    if any(split.l_power(value, P**12) != value for value in primitive):
        raise AssertionError("a recombined primitive coordinate left F_(167^12)")
    return origin, primitive


def decompose_e_over_k6(
    value: split.L, theta: split.L
) -> tuple[split.L, split.L]:
    """Write an F_(p^12) value uniquely as a+b*theta over F_(p^6)."""

    theta_conjugate = split.l_power(theta, P**6)
    denominator = split.l_subtract(theta, theta_conjugate)
    if denominator == split.L_ZERO:
        raise ValueError("theta must lie outside F_(167^6)")
    value_conjugate = split.l_power(value, P**6)
    second = split.l_multiply(
        split.l_subtract(value, value_conjugate),
        split.l_inverse(denominator),
    )
    first = split.l_subtract(value, split.l_multiply(second, theta))
    if (
        split.l_power(first, P**6) != first
        or split.l_power(second, P**6) != second
        or split.l_add(first, split.l_multiply(second, theta)) != value
    ):
        raise AssertionError("the E/K quadratic decomposition failed")
    return first, second


def verify_recombined_split() -> dict[str, object]:
    """Check the full two-channel norm split and its factor parameterization."""

    alpha = ninth_root_of_unity()
    if next(
        exponent
        for exponent in range(1, 10)
        if pow(P, exponent, 9) == 1
    ) != 6:
        raise AssertionError("Phi_9 is no longer irreducible modulo 167")
    q = pow(P, 6, N)
    q_order = next(
        exponent for exponent in range(1, N) if pow(q, exponent, N) == 1
    )
    if q_order != 6 or pow(q, 2, N) not in split.H:
        raise AssertionError("the six primitive C_37 factors changed")
    if tuple(pow(q, 2 * exponent, N) for exponent in range(3)) != split.H:
        raise AssertionError("q^2 no longer generates the multiplier H")

    # Explicitly partition the 36 primitive exponents into six q-orbits.
    unseen = set(range(1, N))
    q_orbits = []
    while unseen:
        start = min(unseen)
        orbit = tuple(start * pow(q, exponent, N) % N for exponent in range(6))
        if len(set(orbit)) != 6 or any(value not in unseen for value in orbit):
            raise AssertionError("the primitive q-orbits overlap")
        unseen.difference_update(orbit)
        q_orbits.append(orbit)
    if len(q_orbits) != 6 or unseen:
        raise AssertionError("the six primitive q-orbits do not partition C_37^*")
    h_classes = {frozenset(part) for part in split.CLASSES}
    for orbit in q_orbits:
        even_half = frozenset(orbit[0::2])
        odd_half = frozenset(orbit[1::2])
        if even_half not in h_classes or odd_half not in h_classes:
            raise AssertionError("a q-orbit did not split into two H-orbits")

    # Certify the full 1+6*2=13 invariant dimension.  Expand every primitive
    # E coordinate in a pinned quadratic basis over K=F_(p^6), then compute
    # the rank of the images of the origin indicator and twelve H-class
    # indicators.
    theta = split.field_fixture(401)
    if split.l_power(theta, P**6) == theta:
        raise AssertionError("the pinned E/K basis element entered K")
    invariant_basis = []
    origin_indicator = [split.L_ZERO] * N
    origin_indicator[0] = split.L_ONE
    invariant_basis.append(tuple(origin_indicator))
    for part in split.CLASSES:
        indicator = [split.L_ZERO] * N
        for column in part:
            indicator[column] = split.L_ONE
        invariant_basis.append(tuple(indicator))
    expanded_images = []
    invariant_basis_coordinates = []
    for basis_word in invariant_basis:
        origin, primitive = recombined_coordinates(basis_word)
        invariant_basis_coordinates.append((origin, primitive))
        expanded = [origin]
        for value in primitive:
            expanded.extend(decompose_e_over_k6(value, theta))
        if len(expanded) != 13 or any(
            split.l_power(value, P**6) != value for value in expanded
        ):
            raise AssertionError("an expanded invariant coordinate left K")
        expanded_images.append(tuple(expanded))
    invariant_rank = l_matrix_rank(expanded_images)
    if invariant_rank != 13:
        raise AssertionError("the recombined invariant CRT lost injectivity")

    # Check the star formula on the entire 13-word invariant basis.  Together
    # with rank 13 and linearity, this certifies the formula on the full
    # invariant algebra rather than only on selected phase fixtures.
    basis_star_certificates = []
    for basis_word, (origin, primitive) in zip(
        invariant_basis, invariant_basis_coordinates
    ):
        star_origin, star_primitive = recombined_coordinates(
            l_group_star_ninth(basis_word)
        )
        if star_origin != split.l_power(origin, P**3):
            raise AssertionError("the basis trivial star exponent changed")
        for index in range(3):
            if star_primitive[index] != split.l_power(
                primitive[index + 3], P**3
            ):
                raise AssertionError("a basis forward star exponent changed")
            if star_primitive[index + 3] != split.l_power(
                primitive[index], P**9
            ):
                raise AssertionError("a basis reverse star exponent changed")
        basis_star_certificates.append(
            (
                compact_hash((origin, primitive)),
                compact_hash((star_origin, star_primitive)),
            )
        )

    # Directly audit the star on all seven CRT coordinates.
    reduced = tuple(
        reduce_word(word) for word in locally_valid_phase_frame(1)
    )
    channel_words = tuple(
        recombined_word(reduced[3 * channel : 3 * channel + 3], alpha)
        for channel in range(2)
    )
    coordinate_pairs = tuple(
        recombined_coordinates(word) for word in channel_words
    )
    star_coordinate_pairs = tuple(
        recombined_coordinates(l_group_star_ninth(word))
        for word in channel_words
    )
    for (origin, primitive), (star_origin, star_primitive) in zip(
        coordinate_pairs, star_coordinate_pairs
    ):
        if star_origin != split.l_power(origin, P**3):
            raise AssertionError("the recombined trivial star exponent changed")
        for index in range(3):
            if star_primitive[index] != split.l_power(
                primitive[index + 3], P**3
            ):
                raise AssertionError("a forward primitive star exponent changed")
            if star_primitive[index + 3] != split.l_power(
                primitive[index], P**9
            ):
                raise AssertionError("a reverse primitive star exponent changed")

    origins = tuple(value[0] for value in coordinate_pairs)
    primitives = tuple(value[1] for value in coordinate_pairs)
    trivial_residual = split.l_add(
        split.l_multiply(origins[0], split.l_power(origins[0], P**3)),
        split.l_multiply(origins[1], split.l_power(origins[1], P**3)),
    )
    primitive_residuals = tuple(
        split.l_add(
            split.l_multiply(
                primitives[0][index],
                split.l_power(primitives[0][index + 3], P**3),
            ),
            split.l_multiply(
                primitives[1][index],
                split.l_power(primitives[1][index + 3], P**3),
            ),
        )
        for index in range(3)
    )

    # Check all six norm-product coordinates, including the redundant partners.
    for index in range(3):
        partner = split.l_add(
            split.l_multiply(
                primitives[0][index + 3],
                split.l_power(primitives[0][index], P**9),
            ),
            split.l_multiply(
                primitives[1][index + 3],
                split.l_power(primitives[1][index], P**9),
            ),
        )
        if partner != split.l_power(primitive_residuals[index], P**9):
            raise AssertionError("a paired norm coordinate lost adjointness")

    # Exhibit the two branches of every primitive factor equation.
    degenerate_y = (split.field_fixture(301), split.field_fixture(302))
    if split.L_ZERO != split.l_add(
        split.l_multiply(split.L_ZERO, split.l_power(degenerate_y[0], P**3)),
        split.l_multiply(split.L_ZERO, split.l_power(degenerate_y[1], P**3)),
    ):
        raise AssertionError("the degenerate primitive branch failed")
    x_a = split.field_fixture(303)
    x_b = split.field_fixture(304)
    tau = split.field_fixture(305)
    powered_y_a = split.l_neg(split.l_multiply(tau, x_b))
    powered_y_b = split.l_multiply(tau, x_a)
    y_a = split.l_power(powered_y_a, P**9)
    y_b = split.l_power(powered_y_b, P**9)
    nondegenerate_residual = split.l_add(
        split.l_multiply(x_a, split.l_power(y_a, P**3)),
        split.l_multiply(x_b, split.l_power(y_b, P**3)),
    )
    if nondegenerate_residual != split.L_ZERO:
        raise AssertionError("the nondegenerate primitive branch failed")
    recovered_tau = split.l_multiply(
        split.l_neg(split.l_power(y_a, P**3)),
        split.l_inverse(x_b),
    )
    if recovered_tau != tau:
        raise AssertionError("the nondegenerate primitive parameter is not unique")

    # Build and verify one norm-minus-one ratio for the trivial quadratic
    # extension F_(p^6)/F_(p^3).
    primitive_generator = split.l_add(
        alpha, split.l_embed((1, 3))
    )
    k6_order = P**6 - 1
    prime_divisors = (2, 3, 7, 83, 9241, 28057)
    k6_factorization = ((2, 4), (3, 2), (7, 1), (83, 1),
                        (9241, 1), (28057, 1))
    if (
        any(not integer_is_prime(value) for value in prime_divisors)
        or k6_order
        != 2**4 * 3**2 * 7 * 83 * 9241 * 28057
    ):
        raise AssertionError("the factorization of 167^6-1 changed")
    if any(
        split.l_power(primitive_generator, k6_order // divisor) == split.L_ONE
        for divisor in prime_divisors
    ):
        raise AssertionError("the pinned F_(167^6) generator lost primitivity")
    norm_minus_one_ratio = split.l_power(
        primitive_generator, (P**3 - 1) // 2
    )
    if split.l_multiply(
        norm_minus_one_ratio,
        split.l_power(norm_minus_one_ratio, P**3),
    ) != split.l_embed((P - 1, 0)):
        raise AssertionError("the trivial norm-minus-one ratio changed")
    scale = split.l_power(primitive_generator, 167)
    trivial_parameter_residual = split.l_add(
        split.l_multiply(scale, split.l_power(scale, P**3)),
        split.l_multiply(
            split.l_multiply(scale, norm_minus_one_ratio),
            split.l_power(
                split.l_multiply(scale, norm_minus_one_ratio), P**3
            ),
        ),
    )
    if trivial_parameter_residual != split.L_ZERO:
        raise AssertionError("the nonzero trivial branch failed")

    k6_size = P**6
    fixed_size = P**3
    primitive_size = P**12
    trivial_zero_branch_count = 1
    trivial_nonzero_branch_count = (k6_size - 1) * (fixed_size + 1)
    trivial_solution_count = (
        trivial_zero_branch_count + trivial_nonzero_branch_count
    )
    primitive_degenerate_branch_count = primitive_size**2
    primitive_nondegenerate_branch_count = (
        (primitive_size**2 - 1) * primitive_size
    )
    one_pair_solution_count = (
        primitive_degenerate_branch_count
        + primitive_nondegenerate_branch_count
    )
    full_solution_count = (
        trivial_solution_count * one_pair_solution_count**3
    )
    certificate = (
        6,
        q,
        q_order,
        tuple(q_orbits),
        split.H,
        compact_hash(theta),
        invariant_rank,
        compact_hash(tuple(basis_star_certificates)),
        compact_hash(alpha),
        compact_hash(tuple(coordinate_pairs)),
        compact_hash(tuple(star_coordinate_pairs)),
        compact_hash(trivial_residual),
        compact_hash(primitive_residuals),
        compact_hash(norm_minus_one_ratio),
        compact_hash((y_a, y_b, nondegenerate_residual)),
        k6_factorization,
        (
            trivial_zero_branch_count,
            trivial_nonzero_branch_count,
            primitive_degenerate_branch_count,
            primitive_nondegenerate_branch_count,
        ),
        trivial_solution_count,
        one_pair_solution_count,
        full_solution_count,
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_RECOMBINED_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_RECOMBINED_CERTIFICATE_SHA256
    ):
        raise AssertionError("the ninth-root recombination certificate changed")
    return {
        "phi9_degree": 6,
        "coefficient_field_size_exponent": 6,
        "primitive_factor_count": 6,
        "primitive_factor_degree_over_coefficient_field": 2,
        "invariant_algebra": "F_(167^6) x F_(167^12)^6",
        "primitive_q_orbit_sizes": tuple(map(len, q_orbits)),
        "invariant_dimension_over_coefficient_field": 13,
        "class_indicator_rank": invariant_rank,
        "star_basis_words": len(basis_star_certificates),
        "star_pair_count": 3,
        "star_frobenius_exponents": (3, 9),
        "scalar_equation_count_over_f_167": 3 + 3 * 12,
        "trivial_branches": ("zero", "nonzero"),
        "primitive_branches_per_pair": ("degenerate", "nondegenerate"),
        "trivial_branch_counts": (
            trivial_zero_branch_count,
            trivial_nonzero_branch_count,
        ),
        "primitive_branch_counts_per_pair": (
            primitive_degenerate_branch_count,
            primitive_nondegenerate_branch_count,
        ),
        "trivial_solution_count": trivial_solution_count,
        "one_pair_solution_count": one_pair_solution_count,
        "full_solution_count": full_solution_count,
        "certificate_sha256": certificate_hash,
    }


def verify_crt_equations() -> dict[str, object]:
    audits = tuple(
        finite_coordinate_audit(locally_valid_phase_frame(seed))
        for seed in (1, 2, 3)
    )
    certificate_hash = compact_hash(audits)
    if (
        EXPECTED_CRT_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_CRT_CERTIFICATE_SHA256
    ):
        raise AssertionError("the full CRT-equation certificate changed")
    return {
        "fixtures": len(audits),
        "trivial_equations": 2,
        "primitive_equations_over_E": 3,
        "star_frobenius_exponents": (5, 7),
        "certificate_sha256": certificate_hash,
    }


def verify() -> dict[str, object]:
    return {
        "equality_orbits": verify_equality_orbits(),
        "phase_fixtures": verify_phase_fixtures(),
        "crt_equations": verify_crt_equations(),
        "primitive_plane": verify_primitive_plane(),
        "recombined_split": verify_recombined_split(),
        "status": (
            "both full phase-frame equations are exactly equivalent to their "
            "reductions modulo 167 on the unit/zero support-167 shell; the "
            "finite primitive system is a three-plane annihilator and the "
            "ninth-root recombination is completely parameterized, but no "
            "physical phase solution or LP(333) is asserted"
        ),
    }


def main() -> None:
    result = verify()
    orbits = result["equality_orbits"]
    crt = result["crt_equations"]
    plane = result["primitive_plane"]
    recombined = result["recombined_split"]
    print(
        "equality_orbits="
        f"({orbits['diagonal_nonzero_lag_orbit']},"
        f"{orbits['cross_zero_lag_orbit']},"
        f"{orbits['cross_nonzero_lag_orbit']})"
    )
    print(
        "finite_equations="
        f"trivial:{crt['trivial_equations']},"
        f"primitive:{crt['primitive_equations_over_E']}"
    )
    print(
        "generic_primitive_plane="
        f"rank:{plane['generic_orbit_plane_rank']},"
        f"annihilator_dimension:{plane['generic_annihilator_dimension']}"
    )
    print(
        "recombined_invariant_algebra="
        f"{recombined['invariant_algebra']}"
    )
    print(
        "orbit_certificate_sha256="
        f"{orbits['certificate_sha256']}"
    )
    print(
        "frame_certificate_sha256="
        f"{result['phase_fixtures']['certificate_sha256']}"
    )
    print(
        "crt_certificate_sha256="
        f"{crt['certificate_sha256']}"
    )
    print(
        "plane_certificate_sha256="
        f"{plane['certificate_sha256']}"
    )
    print(
        "recombined_certificate_sha256="
        f"{recombined['certificate_sha256']}"
    )
    print("PASS: full phase frame is prime-167 exact")
    print("STATUS: finite-field search architecture; no LP(333) found")


if __name__ == "__main__":
    main()
