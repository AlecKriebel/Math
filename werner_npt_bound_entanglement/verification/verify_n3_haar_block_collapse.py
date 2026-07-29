#!/usr/bin/env python3
"""Exact checker for the Haar-equality block coefficient collapse.

The checker constructs the 81-by-81 rational linear system obtained
by comparing coefficients in

    h(A,B) = gamma <A, L(B)>

and verifies both that beta = gamma |vec(I)><vec(I)| solves it and
that the coefficient matrix has full rank.
"""

from fractions import Fraction as Q


D = 3


def pair(a: int, p: int) -> int:
    return D * a + p


def beta_index(a: int, p: int, b: int, q: int) -> int:
    return D * D * pair(a, p) + pair(b, q)


def equation_index(r: int, a: int, t: int, b: int) -> int:
    return D * D * pair(r, a) + pair(t, b)


def rational_rank(matrix: list[list[Q]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(
                    work[row], work[pivot_row]
                )
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def partial_trace(matrix: list[list[Q]], site: int) -> list[list[Q]]:
    """Partial trace of a two-qutrit matrix over one site."""
    output = [[Q(0) for _ in range(D)] for _ in range(D)]
    for row in range(D):
        for column in range(D):
            for traced in range(D):
                if site == 0:
                    full_row = D * traced + row
                    full_column = D * traced + column
                else:
                    full_row = D * row + traced
                    full_column = D * column + traced
                output[row][column] += matrix[full_row][full_column]
    return output


def inner(left: list[list[Q]], right: list[list[Q]]) -> Q:
    return sum(
        left[row][column] * right[row][column]
        for row in range(len(left))
        for column in range(len(left[0]))
    )


def two_copy_pairing(
    left: list[list[Q]], right: list[list[Q]]
) -> Q:
    trace_left = sum(left[index][index] for index in range(D * D))
    trace_right = sum(right[index][index] for index in range(D * D))
    return (
        inner(left, right)
        - Q(1, 2)
        * sum(
            inner(partial_trace(left, site), partial_trace(right, site))
            for site in range(2)
        )
        + Q(1, 4) * trace_left * trace_right
    )


def fixed_left_matrix(
    left_columns: tuple[int, int], right_basis_index: int
) -> list[list[Q]]:
    """Return X Y^T for a matrix-unit basis vector of Y."""
    physical_row = right_basis_index // 2
    auxiliary = right_basis_index % 2
    output = [[Q(0) for _ in range(D * D)] for _ in range(D * D)]
    output[left_columns[auxiliary]][physical_row] = Q(1)
    return output


def fixed_left_gram(left_columns: tuple[int, int]) -> list[list[Q]]:
    matrices = [
        fixed_left_matrix(left_columns, basis_index)
        for basis_index in range(2 * D * D)
    ]
    return [
        [two_copy_pairing(left, right) for right in matrices]
        for left in matrices
    ]


def main() -> None:
    size = D**4
    system = [[Q(0) for _ in range(size)] for _ in range(size)]
    right = [Q(0) for _ in range(size)]

    # Multiply the coefficient identity by two:
    #
    # 2 delta_rt sum_p beta_ap,bp - beta_ar,bt
    #   = 2 delta_rt delta_ab - delta_ra delta_tb.
    for r in range(D):
        for a in range(D):
            for t in range(D):
                for b in range(D):
                    row = equation_index(r, a, t, b)
                    if r == t:
                        for p in range(D):
                            column = beta_index(a, p, b, p)
                            system[row][column] += Q(2)
                    column = beta_index(a, r, b, t)
                    system[row][column] -= Q(1)
                    right[row] = (
                        Q(2) * (r == t) * (a == b)
                        - Q(1) * (r == a) * (t == b)
                    )

    expected = [Q(0) for _ in range(size)]
    for a in range(D):
        for p in range(D):
            for b in range(D):
                for q in range(D):
                    expected[beta_index(a, p, b, q)] = Q(
                        (a == p) * (b == q)
                    )

    image = [
        sum(coefficient * value for coefficient, value in zip(row, expected))
        for row in system
    ]
    assert image == right
    assert rational_rank(system) == size

    # Exact representatives of the two boundary kernel types.
    #
    # span{|00>,|11>} has minimal support (2,2) and nullity one.
    nonfactor = fixed_left_gram((0, 4))
    assert len(nonfactor) - rational_rank(nonfactor) == 1
    # span{|00>,|01>} has a fixed first-site factor and nullity three.
    factor = fixed_left_gram((0, 1))
    assert len(factor) - rational_rank(factor) == 3

    # Coefficientwise audit of the critical trace-excess identity
    #
    # Tr(G_i) + 8q = (15/2) g_i.
    # A Boolean sector is encoded by whether site i is traceless and by
    # the endpoint eigenvalue on the other two sites.
    for site_is_traceless in (False, True):
        for other_traceless_count in range(3):
            other_eigenvalue = (
                Q(-1, 2) ** (2 - other_traceless_count)
            )
            local_eigenvalue = Q(1) if site_is_traceless else Q(-1, 2)
            endpoint_eigenvalue = local_eigenvalue * other_eigenvalue
            trace_h_coefficient = Q(5, 2) * other_eigenvalue
            trace_g_plus_8q = (
                trace_h_coefficient
                - Q(3) * endpoint_eigenvalue
                + Q(8) * endpoint_eigenvalue
            )
            haar_bracket_coefficient = (
                other_eigenvalue if site_is_traceless else Q(0)
            )
            assert trace_g_plus_8q == (
                Q(15, 2) * haar_bracket_coefficient
            )

    # Exact inverse of the local-form/block-Gram coefficient map.
    sample_k = [Q(((17 * index + 5) % 23) - 11, 7) for index in range(size)]

    def k_entry(r, a, t, b):
        return sample_k[equation_index(r, a, t, b)]

    gram_trace = [
        [
            Q(2, 5) * sum(k_entry(s, a, s, b) for s in range(D))
            for b in range(D)
        ]
        for a in range(D)
    ]
    recovered_beta = [Q(0) for _ in range(size)]
    for a in range(D):
        for r in range(D):
            for b in range(D):
                for t in range(D):
                    recovered_beta[beta_index(a, r, b, t)] = (
                        Q(2) * (r == t) * gram_trace[a][b]
                        - Q(2) * k_entry(r, a, t, b)
                    )

    for r in range(D):
        for a in range(D):
            for t in range(D):
                for b in range(D):
                    forward = (
                        (r == t)
                        * sum(
                            recovered_beta[beta_index(a, p, b, p)]
                            for p in range(D)
                        )
                        - Q(1, 2)
                        * recovered_beta[beta_index(a, r, b, t)]
                    )
                    assert forward == k_entry(r, a, t, b)

    # Exact arithmetic behind the quantitative constants:
    # (360 sqrt(15))^2 and the extra ||I||_2^2=3 in the
    # critical marginal corollary.
    isotropy_constant_squared = 360 * 360 * 15
    assert isotropy_constant_squared == 1_944_000
    assert 3 * isotropy_constant_squared == 5_832_000
    # Frobenius coefficient inversion costs (22/5)*sqrt(9);
    # multiplying 360 by 66/5 gives 4752.
    assert Q(22, 5) * 3 * 360 == 4752

    print(
        "verified: the 81 block-coefficient equations are invertible and "
        "force beta = |vec(I_3)><vec(I_3)|; boundary kernel nullities "
        "are 1 for support (2,2) and 3 for a fixed-factor plane; "
        "the critical trace-excess identity holds coefficientwise; "
        "the general coefficient inverse reconstructs an exact sample; "
        "all quantitative stability constants agree exactly"
    )


if __name__ == "__main__":
    main()
