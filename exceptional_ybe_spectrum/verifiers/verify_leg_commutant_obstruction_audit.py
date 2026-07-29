#!/usr/bin/env python3
"""Exact audit of leg-commutant and endpoint-bimodule obstructions.

This verifier has four logically separate parts.

1. It enumerates every finite-dimensional C*-algebra representation on
   C^6 whose minimal projections all have even ordinary rank.
2. It verifies, through exact integer arithmetic, that every ordered pair
   of those endpoint algebras passes every H_n(3,6) central-rank,
   endpoint-bimodule, and one-sided branching constraint through level 14.
3. It constructs exact standard d=6 two-site reflections with respectively
   scalar leg commutants and an M_3 tensor I_2 leg commutant.  Exact nonzero
   cubic coefficients guard against mistaking either assumption-audit object
   for a Yang--Baxter witness.
4. It checks the scalar arithmetic in the Conti--Lechner ergodicity and
   index audit.

No floating-point arithmetic is used.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations_with_replacement

import sympy as sp


FUSION_BY_X = {
    (0, 0): ((1, 0),),
    (1, 0): ((2, 0), (0, 1)),
    (0, 1): ((1, 1), (0, 0)),
    (2, 0): ((3, 0), (1, 1)),
    (1, 1): ((2, 1), (0, 2), (1, 0)),
    (0, 2): ((1, 2), (0, 1)),
    (3, 0): ((2, 1),),
    (2, 1): ((1, 2), (2, 0)),
    (1, 2): ((0, 3), (1, 1)),
    (0, 3): ((0, 2),),
}

QUANTUM_DIMENSION = {
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


def next_paths(paths: dict[tuple[int, int], int]) -> dict[tuple[int, int], int]:
    following: dict[tuple[int, int], int] = defaultdict(int)
    for vertex, count in paths.items():
        for successor in FUSION_BY_X[vertex]:
            following[successor] += count
    return dict(following)


def algebra_types_for_s(s: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Enumerate sum M_m tensor I_(2a), with sum m*a=s.

    A summand is stored as (m,a); its minimal projections have ordinary
    rank 2a and its represented dimension is 2ma.
    """

    summands = tuple(
        (m, a)
        for m in range(1, s + 1)
        for a in range(1, s + 1)
        if m * a <= s
    )
    answers: set[tuple[tuple[int, int], ...]] = set()
    for length in range(1, s + 1):
        for choice in combinations_with_replacement(summands, length):
            if sum(m * a for m, a in choice) == s:
                answers.add(tuple(sorted(choice)))
    return tuple(sorted(answers))


def verify_endpoint_arithmetic() -> None:
    d = 6
    s = d // 2
    algebra_types = algebra_types_for_s(s)
    expected = {
        ((1, 3),),  # C I_6
        ((3, 1),),  # M_3 tensor I_2
        ((1, 1), (1, 2)),  # C I_2 plus C I_4
        ((1, 1), (2, 1)),  # C I_2 plus M_2 tensor I_2
        ((1, 1), (1, 1), (1, 1)),  # three rank-two scalar blocks
    }
    assert set(algebra_types) == expected
    for algebra in algebra_types:
        assert sum(2 * m * a for m, a in algebra) == d
        assert all((2 * a) % 2 == 0 for _, a in algebra)

    for vertex, successors in FUSION_BY_X.items():
        assert (
            sum(QUANTUM_DIMENSION[x] for x in successors)
            == 2 * QUANTUM_DIMENSION[vertex]
        )

    paths = {(0, 0): 1}
    maximum_strand = 14
    for strand in range(maximum_strand + 1):
        categorical_dimension = sum(
            path_count * QUANTUM_DIMENSION[vertex]
            for vertex, path_count in paths.items()
        )
        assert categorical_dimension == 2**strand

        if strand >= 2:
            for left in algebra_types:
                for right in algebra_types:
                    for vertex, simple_dimension in paths.items():
                        qdim = QUANTUM_DIMENSION[vertex]

                        # One-sided multiplicities forced by the endpoint
                        # conditional-trace identity.
                        for _, a in left:
                            ell = a * qdim * s ** (strand - 1)
                            assert isinstance(ell, int) and ell >= 0
                        assert (
                            sum(
                                m * (a * qdim * s ** (strand - 1))
                                for m, a in left
                            )
                            == qdim * s**strand
                        )

                        # Explicit integral solution of every two-ended
                        # transportation equation.
                        k = {
                            (alpha, beta): (
                                a * b * qdim * s ** (strand - 2)
                            )
                            for alpha, (_, a) in enumerate(left)
                            for beta, (_, b) in enumerate(right)
                        }
                        for alpha, (_, a) in enumerate(left):
                            assert (
                                sum(
                                    right[beta][0] * k[alpha, beta]
                                    for beta in range(len(right))
                                )
                                == a * qdim * s ** (strand - 1)
                            )
                        for beta, (_, b) in enumerate(right):
                            assert (
                                sum(
                                    left[alpha][0] * k[alpha, beta]
                                    for alpha in range(len(left))
                                )
                                == b * qdim * s ** (strand - 1)
                            )
                        assert (
                            sum(
                                left[alpha][0]
                                * right[beta][0]
                                * k[alpha, beta]
                                for alpha in range(len(left))
                                for beta in range(len(right))
                            )
                            == qdim * s**strand
                        )

                        # Central ranks close on every endpoint-minimal
                        # corner.  The ordinary simple dimension is the
                        # path count.
                        for alpha, (_, a) in enumerate(left):
                            for beta, (_, b) in enumerate(right):
                                corner_central_rank = (
                                    simple_dimension * k[alpha, beta]
                                )
                                assert corner_central_rank >= 0

                    # Sum of all central corners is the dimension of
                    # z V^(n-2) w for minimal endpoint projections of
                    # ranks 2a and 2b.
                    for _, a in left:
                        for _, b in right:
                            central_sum = sum(
                                path_count
                                * (
                                    a
                                    * b
                                    * QUANTUM_DIMENSION[vertex]
                                    * s ** (strand - 2)
                                )
                                for vertex, path_count in paths.items()
                            )
                            assert central_sum == 4 * a * b * d ** (
                                strand - 2
                            )

        paths = next_paths(paths)

    # The n=3 common-one, generic, common-zero multiplicities in one
    # endpoint-minimal corner are (ab*s, 3ab*s, ab*s).
    for left in algebra_types:
        for right in algebra_types:
            for _, a in left:
                for _, b in right:
                    common = a * b * s
                    generic_blocks = 3 * a * b * s
                    corner_dimension = (2 * a) * d * (2 * b)
                    assert 2 * common + 2 * generic_blocks == corner_dimension

    print("[ok] exhaustive d=6 even-minimal-rank leg-algebra list (5 types)")
    print(
        "[ok] all 25 ordered endpoint-algebra pairs pass exact central, "
        "bimodule, and branching arithmetic through n=14"
    )


def bell_sign(a: int, b: int) -> int:
    value = 1 if b < 3 else -1
    if (a, b) == (0, 0):
        value = -1
    if (a, b) == (1, 3):
        value = 1
    return value


def bell_pair_coeff(a: int, output_first: int, input_first: int) -> sp.Expr:
    """Matrix coefficient of the exact Bell-diagonal reflection."""

    zeta = sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    return sp.simplify(
        sum(
            bell_sign(a, b) * zeta ** (b * (output_first - input_first))
            for b in range(6)
        )
        / 6
    )


def apply_bell_pair(
    state: dict[tuple[int, int, int], sp.Expr], leg: int
) -> dict[tuple[int, int, int], sp.Expr]:
    output: dict[tuple[int, int, int], sp.Expr] = {}
    for (x, y, z), amplitude in state.items():
        if leg == 1:
            difference = (y - x) % 6
            for j in range(6):
                coefficient = bell_pair_coeff(difference, j, x)
                target = (j, (j + difference) % 6, z)
                output[target] = sp.simplify(
                    output.get(target, 0) + amplitude * coefficient
                )
        else:
            difference = (z - y) % 6
            for j in range(6):
                coefficient = bell_pair_coeff(difference, j, y)
                target = (x, j, (j + difference) % 6)
                output[target] = sp.simplify(
                    output.get(target, 0) + amplitude * coefficient
                )
    return {
        target: sp.simplify(value)
        for target, value in output.items()
        if sp.simplify(value) != 0
    }


def apply_word(
    state: dict[tuple[int, int, int], sp.Expr], word: tuple[int, ...]
) -> dict[tuple[int, int, int], sp.Expr]:
    for leg in reversed(word):
        state = apply_bell_pair(state, leg)
    return state


def verify_scalar_leg_standard_guard() -> None:
    zeta = sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    signs = [[bell_sign(a, b) for b in range(6)] for a in range(6)]
    assert sum(sum(row) for row in signs) == 0
    assert sum(value == 1 for row in signs for value in row) == 18
    assert sp.simplify(zeta**6 - 1) == 0

    # Symplectic Fourier support contains both Weyl generators.  Therefore
    # the left slices contain X and Z, while the right slices contain X
    # and Z^{-1}; both leg commutants are scalar.
    frequency_a = sp.simplify(
        sum(signs[a][b] * zeta**a for a in range(6) for b in range(6))
    )
    frequency_b = sp.simplify(
        sum(signs[a][b] * zeta**b for a in range(6) for b in range(6))
    )
    assert frequency_a == -1 + sp.I * sp.sqrt(3)
    assert frequency_b == 8 + 12 * sp.I * sp.sqrt(3)
    assert frequency_a != 0 and frequency_b != 0
    assert all(
        sp.simplify(zeta**j - zeta**k) != 0
        for j in range(6)
        for k in range(j)
    )

    # Each Bell projector has both marginals I/6, so the balanced sign
    # sum gives zero partial traces.  Orthogonality of the Bell basis gives
    # a Hermitian involution with trace zero.
    assert sum(sum(row) for row in signs) / 6 == 0

    # Exact guard: this standard scalar-leg object is not a YBE witness.
    basis = (0, 0, 1)
    state = {basis: sp.Integer(1)}
    h1h2h1 = apply_word(state, (1, 2, 1))
    h2h1h2 = apply_word(state, (2, 1, 2))
    h1 = apply_bell_pair(state, 1)
    h2 = apply_bell_pair(state, 2)
    target = (3, 5, 3)
    residual_coefficient = sp.simplify(
        h1h2h1.get(target, 0)
        - h2h1h2.get(target, 0)
        - (h1.get(target, 0) - h2.get(target, 0)) / 3
    )
    assert residual_coefficient == (-1 + sp.I * sp.sqrt(3)) / 27

    # The abstract two-projection relation can nevertheless be completed
    # relative to any rank-half p by the canonical generic block.  It is
    # the shifted-copy constraint q=I tensor P that fails above.
    p = sp.diag(1, 0)
    q = sp.Matrix(
        [
            [sp.Rational(1, 3), sp.sqrt(2) / 3],
            [sp.sqrt(2) / 3, sp.Rational(2, 3)],
        ]
    )
    assert q * q == q
    assert p * q * p - q * p * q == (p - q) / 3
    dimension = 6**3
    common = dimension // 8
    generic_blocks = 3 * dimension // 8
    assert common == 27 and generic_blocks == 81
    assert 2 * common + 2 * generic_blocks == dimension

    print("[ok] exact standard d=6 Bell reflection has scalar commutants")
    print(
        "[ok] exact cubic guard is nonzero: "
        f"{sp.sstr(residual_coefficient)}"
    )
    print(
        "[ok] canonical abstract H_3 completion has multiplicities "
        "(27, 81, 27), but is not the spatial second shift"
    )


def factor_pair_transitions(
    first: int, second: int
) -> list[tuple[int, int, sp.Expr]]:
    """Sparse action of the M_3 tensor I_2 standard guard."""

    x = sp.Matrix([[0, 1], [1, 0]])
    y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    z = sp.diag(1, -1)
    diagonal_reflections = (
        (1, 1, 1, -1, -1, -1),
        (1, 1, -1, 1, -1, -1),
        (1, -1, 1, -1, 1, -1),
    )
    transitions: list[tuple[int, int, sp.Expr]] = []
    spectator, qubit = divmod(first, 2)
    for pauli, diagonal in zip((x, y, z), diagonal_reflections):
        for output_qubit in range(2):
            coefficient = (
                pauli[output_qubit, qubit]
                * diagonal[second]
                / sp.sqrt(3)
            )
            if coefficient != 0:
                transitions.append(
                    (2 * spectator + output_qubit, second, coefficient)
                )
    return transitions


def apply_factor_pair(
    state: dict[tuple[int, int, int], sp.Expr], leg: int
) -> dict[tuple[int, int, int], sp.Expr]:
    output: dict[tuple[int, int, int], sp.Expr] = {}
    for (first, second, third), amplitude in state.items():
        if leg == 1:
            for new_first, new_second, coefficient in factor_pair_transitions(
                first, second
            ):
                target = (new_first, new_second, third)
                output[target] = sp.simplify(
                    output.get(target, 0) + amplitude * coefficient
                )
        else:
            for new_second, new_third, coefficient in factor_pair_transitions(
                second, third
            ):
                target = (first, new_second, new_third)
                output[target] = sp.simplify(
                    output.get(target, 0) + amplitude * coefficient
                )
    return {
        target: sp.simplify(value)
        for target, value in output.items()
        if sp.simplify(value) != 0
    }


def apply_factor_word(
    state: dict[tuple[int, int, int], sp.Expr], word: tuple[int, ...]
) -> dict[tuple[int, int, int], sp.Expr]:
    for leg in reversed(word):
        state = apply_factor_pair(state, leg)
    return state


def verify_matrix_factor_standard_guard() -> None:
    x = sp.Matrix([[0, 1], [1, 0]])
    y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    z = sp.diag(1, -1)
    ds = (
        sp.diag(1, 1, 1, -1, -1, -1),
        sp.diag(1, 1, -1, 1, -1, -1),
        sp.diag(1, -1, 1, -1, 1, -1),
    )
    assert all(sp.trace(matrix) == 0 and matrix**2 == sp.eye(6) for matrix in ds)
    assert all(ds[i] * ds[j] == ds[j] * ds[i] for i in range(3) for j in range(3))
    assert sp.Matrix([[matrix[j, j] for matrix in ds] for j in range(6)]).rank() == 3
    signatures = {
        tuple(matrix[j, j] for matrix in ds)
        for j in range(6)
    }
    assert len(signatures) == 6
    assert all(sp.trace(matrix) == 0 for matrix in (x, y, z))
    assert x * y + y * x == sp.zeros(2)
    assert x * z + z * x == sp.zeros(2)
    assert y * z + z * y == sp.zeros(2)

    # H=(I_3 tensor X tensor D_1 + ...)/sqrt(3) is therefore an exact
    # standard reflection.  Independent right coefficients force its left
    # commutant to be exactly M_3 tensor I_2.
    state = {(0, 0, 0): sp.Integer(1)}
    h1h2h1 = apply_factor_word(state, (1, 2, 1))
    h2h1h2 = apply_factor_word(state, (2, 1, 2))
    h1 = apply_factor_pair(state, 1)
    h2 = apply_factor_pair(state, 2)
    target = (1, 0, 0)
    residual_coefficient = sp.simplify(
        h1h2h1.get(target, 0)
        - h2h1h2.get(target, 0)
        - (h1.get(target, 0) - h2.get(target, 0)) / 3
    )
    assert residual_coefficient == 4 * sp.sqrt(3) * (-1 - sp.I) / 9

    print("[ok] exact standard d=6 guard has C_L = M_3 tensor I_2")
    print(
        "[ok] its right commutant is diagonal and its exact cubic guard "
        f"is nonzero: {sp.sstr(residual_coefficient)}"
    )


def verify_ergodicity_and_index_arithmetic() -> None:
    q = (1 + sp.I * sp.sqrt(3)) / 2
    normalized_trace_r = sp.simplify((q - 1) / 2)
    trace_norm_squared = sp.simplify(
        normalized_trace_r * sp.conjugate(normalized_trace_r)
    )
    assert trace_norm_squared == sp.Rational(1, 4)

    # Conti--Lechner: ergodicity forces ||phi_R(R)||_2^2=1/d^2.
    # Automatic standardness gives phi_R(R)=tau(R)I here.
    for d in (4, 6, 8, 10, 14):
        assert trace_norm_squared != sp.Rational(1, d**2)

    # The scalar-partial-trace upper bound is |tau(R)|^{-2}=4.  The
    # H_n(3,6) braid-subfactor PF eigenvalue is 2, hence its Jones index
    # is 4, which supplies the matching lower bound.
    upper_index = sp.simplify(1 / trace_norm_squared)
    braid_pf_eigenvalue = 2
    braid_index = braid_pf_eigenvalue**2
    assert upper_index == braid_index == 4

    print(
        "[ok] exceptional endomorphism trace norm is 1/4; "
        "Conti--Lechner ergodicity is impossible for every d>2"
    )
    print("[ok] braid and ambient Jones-index bounds meet at index 4")


def main() -> None:
    verify_endpoint_arithmetic()
    verify_scalar_leg_standard_guard()
    verify_matrix_factor_standard_guard()
    verify_ergodicity_and_index_arithmetic()
    print(
        "Conclusion: central ranks, endpoint bimodules, one-sided tower "
        "inclusions, scalar leg commutants, M_k tensor I_even leg "
        "commutants, and Yang--Baxter endomorphism index/ergodicity do "
        "not force an odd-rank leg projection at d=6."
    )


if __name__ == "__main__":
    main()
