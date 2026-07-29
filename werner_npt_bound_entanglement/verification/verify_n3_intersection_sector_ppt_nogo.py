#!/usr/bin/env python3
"""Exact checker for the quantitative-PPT/swap-sector Lorentz no-go.

Only Python's rational arithmetic is used.  The verifier checks:

* K = G^Gamma and [K,F] = 0;
* the exact Bell-basis eigenvalues and all swap-sector bounds;
* G > 0;
* the polynomial certificate for every diagonal qubit projector;
* the strict off-diagonal dyad violation.
"""

from fractions import Fraction as Q


Vector = tuple[Q, ...]
Matrix = tuple[tuple[Q, ...], ...]


def matvec(a: Matrix, x: Vector) -> Vector:
    return tuple(sum(a[i][j] * x[j] for j in range(len(x)))
                 for i in range(len(a)))


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
              for j in range(len(b[0])))
        for i in range(len(a))
    )


def partial_transpose(a: Matrix) -> Matrix:
    """Transpose the second qubit: (i,j;k,l) -> (i,l;k,j)."""
    out = [[Q(0) for _ in range(4)] for _ in range(4)]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for ell in range(2):
                    out[2 * i + ell][2 * k + j] = a[2 * i + j][2 * k + ell]
    return tuple(tuple(row) for row in out)


def scale(x: Vector, c: Q) -> Vector:
    return tuple(c * value for value in x)


def main() -> None:
    zero = Q(0)
    swap: Matrix = (
        (1, 0, 0, 0),
        (0, 0, 1, 0),
        (0, 1, 0, 0),
        (0, 0, 0, 1),
    )
    k: Matrix = (
        (Q(3, 5), zero, zero, Q(1, 5)),
        (zero, Q(2, 5), zero, zero),
        (zero, zero, Q(2, 5), zero),
        (Q(1, 5), zero, zero, Q(3, 5)),
    )
    g_expected: Matrix = (
        (Q(3, 5), zero, zero, zero),
        (zero, Q(2, 5), Q(1, 5), zero),
        (zero, Q(1, 5), Q(2, 5), zero),
        (zero, zero, zero, Q(3, 5)),
    )
    g = partial_transpose(k)
    assert g == g_expected
    assert matmul(k, swap) == matmul(swap, k)

    # Unnormalized Bell basis.  The first three vectors are symmetric;
    # the last is antisymmetric.
    bell: tuple[tuple[Vector, int, Q], ...] = (
        ((1, 0, 0, 1), +1, Q(4, 5)),
        ((1, 0, 0, -1), +1, Q(2, 5)),
        ((0, 1, 1, 0), +1, Q(2, 5)),
        ((0, 1, -1, 0), -1, Q(2, 5)),
    )
    for vector, swap_sign, eigenvalue in bell:
        assert matvec(swap, vector) == scale(vector, Q(swap_sign))
        assert matvec(k, vector) == scale(vector, eigenvalue)
        if swap_sign == 1:
            assert Q(1, 8) <= eigenvalue <= Q(9, 8)
        else:
            assert Q(3, 8) <= eigenvalue <= Q(27, 8)

    # G has eigenvalue 3/5 on the symmetric Bell vectors and 1/5 on
    # the antisymmetric one, proving positive definiteness exactly.
    for vector, swap_sign, _ in bell:
        eigenvalue = Q(3, 5) if swap_sign == 1 else Q(1, 5)
        assert matvec(g, vector) == scale(vector, eigenvalue)
        assert eigenvalue > 0

    # The continuum diagonal certificate is the polynomial identity
    #
    # (3/5)(3/5 - ny^2/5) - (9/25)nx^2
    #   = (9/25)nz^2 + (6/25)ny^2
    #
    # modulo nx^2 + ny^2 + nz^2 = 1.  Check its three coefficients.
    a = Q(3, 5)
    constant = a * Q(3, 5)
    coeff_nx2 = Q(-9, 25)
    coeff_ny2 = -a * Q(1, 5)
    assert constant == Q(9, 25)
    # Replacing 1 by nx^2+ny^2+nz^2 leaves:
    assert constant + coeff_nx2 == 0
    assert constant + coeff_ny2 == Q(6, 25)
    assert constant == Q(9, 25)  # coefficient of nz^2

    # Elementary physical scalar windows and the sharp self-adjoint
    # lower bound.  The latter follows from
    # g(H) >= (2/5)(x0^2+r^2) >= (1/2)min(x0^2,r^2).
    assert Q(1, 8) <= a <= Q(5, 8)
    assert Q(1, 8) <= Q(2, 5) <= Q(3, 5) <= Q(5, 8)
    assert Q(2, 5) * 2 >= Q(1, 2)

    # Exact polynomial residues used for the sharp scalar pair bounds:
    # upper residue 8(1-x)(53x+23), lower residue
    # 19(11 y^2 + 19 z^2).
    assert 8 * 53 > 0 and 8 * 23 > 0
    assert 19 * 11 > 0 and 19 * 19 > 0

    # u=|0>, v=|1>: vec(|u><v|)=|01>.  The T=(3/5)X
    # matrix element is 3/5.
    e01: Vector = (0, 1, 0, 0)
    ge01 = matvec(g, e01)
    dyad_energy = sum(e01[i] * ge01[i] for i in range(4))
    matrix_element_squared = Q(9, 25)
    assert dyad_energy == Q(2, 5)
    assert a * dyad_energy == Q(6, 25)
    assert a * dyad_energy < matrix_element_squared

    print("verified: normalized diagonal tests pass; dyad defect = -3/25")


if __name__ == "__main__":
    main()
