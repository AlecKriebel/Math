#!/usr/bin/env python3
"""Exact exhaustion of a qutrit graph-phase/global-flip ansatz.

The active space is C^2 tensor C^3 tensor C^2.  E flips both outer bits
and applies an involution to the middle trit.  M is any diagonal sign
reflection satisfying ME=-EM.  The script proves that no
H=xM+yE, x^2+y^2=1, satisfies the required cubic overlap relation.

Matrix products use exact int64 arithmetic (all entries stay small).
Polynomial gcds are computed exactly over QQ by SymPy.
"""

from __future__ import annotations

import itertools

import numpy as np
import sympy as sp


def main():
    states = [
        (left, middle, right)
        for left in range(2)
        for middle in range(3)
        for right in range(2)
    ]
    state_index = {state: index for index, state in enumerate(states)}

    # Every involution of a three-element set: identity and 3 transpositions.
    middle_involutions = [
        (0, 1, 2),
        (1, 0, 2),
        (2, 1, 0),
        (0, 2, 1),
    ]

    identity_six = np.eye(6, dtype=np.int64)
    variable = sp.symbols("t")
    checked = 0

    for middle_permutation in middle_involutions:
        flip = np.zeros((12, 12), dtype=np.int64)
        seen = set()
        orbits = []
        for state in states:
            image = (
                1 - state[0],
                middle_permutation[state[1]],
                1 - state[2],
            )
            flip[state_index[image], state_index[state]] = 1
            if state not in seen:
                orbits.append((state, image))
                seen.update((state, image))

        assert len(orbits) == 6
        assert np.array_equal(flip @ flip, np.eye(12, dtype=np.int64))
        flip_first = np.kron(flip, identity_six)
        flip_second = np.kron(identity_six, flip)

        # Anticommutation forces opposite M signs on each E orbit.
        for orbit_signs in itertools.product((1, -1), repeat=6):
            diagonal = np.zeros(12, dtype=np.int64)
            for sign, (state, image) in zip(orbit_signs, orbits):
                diagonal[state_index[state]] = sign
                diagonal[state_index[image]] = -sign
            phase = np.diag(diagonal)

            assert np.array_equal(phase @ phase, np.eye(12, dtype=np.int64))
            assert np.array_equal(phase @ flip, -(flip @ phase))
            assert np.trace(phase) == 0
            assert np.trace(flip) == 0

            phase_first = np.kron(phase, identity_six)
            phase_second = np.kron(identity_six, phase)

            # For H=xM+yE, write the cubic difference as
            # x^3 A + x^2 y B + x y^2 C + y^3 D.
            coefficient_x3 = (
                phase_first @ phase_second @ phase_first
                - phase_second @ phase_first @ phase_second
            )
            coefficient_x2y = (
                flip_first @ phase_second @ phase_first
                + phase_first @ flip_second @ phase_first
                + phase_first @ phase_second @ flip_first
                - flip_second @ phase_first @ phase_second
                - phase_second @ flip_first @ phase_second
                - phase_second @ phase_first @ flip_second
            )
            coefficient_xy2 = (
                phase_first @ flip_second @ flip_first
                + flip_first @ phase_second @ flip_first
                + flip_first @ flip_second @ phase_first
                - phase_second @ flip_first @ flip_second
                - flip_second @ phase_first @ flip_second
                - flip_second @ flip_first @ phase_second
            )
            coefficient_y3 = (
                flip_first @ flip_second @ flip_first
                - flip_second @ flip_first @ flip_second
            )
            linear_x = phase_first - phase_second
            linear_y = flip_first - flip_second

            # For x != 0, put t=y/x and use x^2=1/(1+t^2).
            # After clearing denominators, every matrix entry must satisfy
            #
            # 3(A+tB+t^2 C+t^3 D)
            #   -(1+t^2)(linear_x+t linear_y) = 0.
            polynomial_coefficients = (
                3 * coefficient_x3 - linear_x,
                3 * coefficient_x2y - linear_y,
                3 * coefficient_xy2 - linear_x,
                3 * coefficient_y3 - linear_y,
            )

            # The endpoints y=0 and x=0 would require respectively the
            # constant and cubic coefficient matrices to vanish.
            assert np.any(polynomial_coefficients[0])
            assert np.any(polynomial_coefficients[3])

            common_gcd = None
            nonzero_positions = np.nonzero(
                np.any(
                    np.stack(polynomial_coefficients, axis=-1) != 0,
                    axis=-1,
                )
            )
            for position in zip(*nonzero_positions):
                coefficients = [
                    int(matrix[position])
                    for matrix in polynomial_coefficients
                ]
                polynomial = sp.Poly(
                    sum(
                        coefficients[degree] * variable**degree
                        for degree in range(4)
                    ),
                    variable,
                    domain=sp.QQ,
                )
                if polynomial.is_zero:
                    continue
                common_gcd = (
                    polynomial
                    if common_gcd is None
                    else sp.gcd(common_gcd, polynomial)
                )
                if common_gcd.degree() == 0:
                    break

            assert common_gcd is not None
            assert common_gcd.monic() == sp.Poly(1, variable, domain=sp.QQ)
            checked += 1

    assert checked == 4 * 2**6
    print("middle involutions checked: 4")
    print("anticommuting diagonal phases per involution: 64")
    print("total exact cases checked:", checked)
    print("endpoint coefficient matrices were nonzero in every case")
    print("common residual-polynomial gcd was 1 in every case")
    print("No real or complex mixing angle solves this ansatz.")
    print("All assertions passed (exact integer and QQ polynomial arithmetic).")


if __name__ == "__main__":
    main()
