#!/usr/bin/env python3
"""Exact verifier for the canonical three-channel boundary/current block.

This is a theorem-side replay over ``fractions.Fraction``.  It constructs
the dB chain directly from a rational undirected weighted graph, solves its
Green system independently, and checks the state and rank identities for
the two noncomplete pair-flow directions

    alpha E1 - E3,        E2 - beta E1.

It does not import a discovery LP or a stored numerical certificate.
"""

from __future__ import annotations

from fractions import Fraction as Q


WEIGHTS = (
    (0, 2, 0, 1),
    (2, 0, 3, 0),
    (0, 3, 0, 4),
    (1, 0, 4, 0),
)


def solve_linear(matrix: list[list[Q]], rhs: list[Q]) -> list[Q]:
    """Solve a nonsingular rational system by Gauss--Jordan elimination."""

    n = len(rhs)
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale:
                augmented[row] = [
                    a - scale * b
                    for a, b in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(n)]


def determinant(matrix: list[list[Q]]) -> Q:
    """Exact determinant, used only for the small PSD replay."""

    work = [row[:] for row in matrix]
    answer = Q(1)
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        diagonal = work[column][column]
        answer *= diagonal
        for row in range(column + 1, len(work)):
            scale = work[row][column] / diagonal
            for j in range(column + 1, len(work)):
                work[row][j] -= scale * work[column][j]
    return answer


def inverse_matrix(matrix: tuple[tuple[Q, ...], ...]) -> tuple[tuple[Q, ...], ...]:
    columns = []
    for column in range(len(matrix)):
        rhs = [Q(int(row == column)) for row in range(len(matrix))]
        columns.append(solve_linear([list(row) for row in matrix], rhs))
    return tuple(
        tuple(columns[column][row] for column in range(len(matrix)))
        for row in range(len(matrix))
    )


def matmul(
    left: tuple[tuple[Q, ...], ...],
    right: tuple[tuple[Q, ...], ...],
) -> tuple[tuple[Q, ...], ...]:
    return tuple(
        tuple(
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


N = len(WEIGHTS)
FULL = (1 << N) - 1
DEGREE = tuple(sum(row) for row in WEIGHTS)
TOTAL_DEGREE = sum(DEGREE)
P = tuple(
    tuple(Q(WEIGHTS[v][i], DEGREE[v]) for i in range(N))
    for v in range(N)
)
PI = tuple(Q(DEGREE[v], TOTAL_DEGREE) for v in range(N))
ALPHA = Q(N - 1, N)
THETA = 1 / ALPHA
BETA = Q(N - 2, N - 1)


def bit(state: int, vertex: int) -> int:
    return (state >> vertex) & 1


def matvec(matrix: tuple[tuple[Q, ...], ...], vector: tuple[Q, ...]):
    return tuple(sum(a * b for a, b in zip(row, vector)) for row in matrix)


def x_vector(state: int) -> tuple[Q, ...]:
    s = tuple(Q(bit(state, i)) for i in range(N))
    return matvec(P, s)


def indicator(state: int) -> tuple[Q, ...]:
    return tuple(Q(bit(state, i)) for i in range(N))


def quadratic_form(matrix: tuple[tuple[Q, ...], ...], vector: tuple[Q, ...]) -> Q:
    image = matvec(matrix, vector)
    return sum(vector[i] * image[i] for i in range(N))


def p2_matrix() -> tuple[tuple[Q, ...], ...]:
    return tuple(
        tuple(sum(P[v][j] * P[j][i] for j in range(N)) for i in range(N))
        for v in range(N)
    )


P2 = p2_matrix()
R_DIAGONAL = tuple(P2[v][v] for v in range(N))
SIGMA = sum(value * value for value in PI)
CHI = sum(PI[v] * sum(value * value for value in P[v]) for v in range(N))
DELTA = SIGMA - Q(1, N)
EPSILON = CHI - Q(1, N - 1)
H1 = tuple(PI[v] - Q(1, N) for v in range(N))
H2 = tuple(Q(1, N - 1) - R_DIAGONAL[v] for v in range(N))
BOUNDARY_VECTOR = (DELTA, -EPSILON)


def kappa() -> Q:
    return Q(
        2 * ((N - 3) * 2 ** N + 4),
        (3 * N - 7) * 2 ** N + 8,
    )


L_PI = tuple(
    tuple(PI[i] * ((i == j) - P[i][j]) for j in range(N))
    for i in range(N)
)
K_F = tuple(
    tuple(
        THETA * (PI[i] * (i == j) - PI[i] * PI[j]) - L_PI[i][j] / 2
        for j in range(N)
    )
    for i in range(N)
)
TRACE_K_F = sum(K_F[v][v] for v in range(N))
K_E = tuple(
    tuple(
        L_PI[i][j]
        - THETA * (PI[i] * (i == j) - PI[i] * PI[j])
        for j in range(N)
    )
    for i in range(N)
)
# ``K_F`` has constant kernel.  Adding the all-ones matrix changes only that
# kernel, so its inverse is the exact quotient inverse on every zero-sum
# column.  This avoids square roots and keeps the Green--Schur matrix rational.
K_F_QUOTIENT_INVERSE = inverse_matrix(
    tuple(tuple(K_F[i][j] + 1 for j in range(N)) for i in range(N))
)
K_G = matmul(matmul(K_E, K_F_QUOTIENT_INVERSE), K_E)
TRACE_K_G = sum(K_G[v][v] for v in range(N))


def rates(state: int) -> list[tuple[int, Q]]:
    x = x_vector(state)
    result = []
    for v in range(N):
        rate = (1 - x[v]) / (1 + x[v]) if bit(state, v) else 2 * x[v] / (1 + x[v])
        if rate:
            result.append((state ^ (1 << v), rate))
    return result


def stationary_mass(state: int) -> Q:
    return sum(PI[v] for v in range(N) if bit(state, v))


def cut(state: int) -> Q:
    s = indicator(state)
    return quadratic_form(L_PI, s)


def variance(state: int) -> Q:
    mass = stationary_mass(state)
    return mass * (1 - mass)


def selection_gain(state: int) -> Q:
    return sum(
        PI[v] * value
        for v, value in enumerate(selection_vector(state))
    )


def affine_spectral_gauge(state: int) -> Q:
    """The mass-only coboundary hidden in the ``K_F`` remainder."""

    mass = stationary_mass(state)
    return THETA * mass * mass - (THETA - Q(1, 2)) * mass


def spectral_storage(state: int) -> Q:
    return quadratic_form(K_F, indicator(state))


def green_schur_storage(state: int) -> Q:
    return quadratic_form(K_G, indicator(state))


def green_schur_dissipation(state: int) -> Q:
    s = indicator(state)
    neutral_gradient = tuple(
        s[v] - x_vector(state)[v] for v in range(N)
    )
    return sum(
        s[i] * K_G[i][j] * neutral_gradient[j]
        for i in range(N)
        for j in range(N)
    )


def green_schur_cross(state: int) -> Q:
    return sum(
        indicator(state)[i] * K_G[i][j] * selection_vector(state)[j]
        for i in range(N)
        for j in range(N)
    )


def green_schur_diagonal(state: int) -> Q:
    activity = activity_vector(state)
    return sum(K_G[v][v] * activity[v] for v in range(N))


def selection_vector(state: int) -> tuple[Q, ...]:
    x = x_vector(state)
    return tuple(x[v] * (1 - x[v]) / (1 + x[v]) for v in range(N))


def activity_vector(state: int) -> tuple[Q, ...]:
    x = x_vector(state)
    return tuple(
        (1 - x[v]) / (1 + x[v]) if bit(state, v)
        else 2 * x[v] / (1 + x[v])
        for v in range(N)
    )


def prediction_error(state: int) -> Q:
    s = indicator(state)
    x = x_vector(state)
    return sum(PI[v] * (s[v] - x[v]) ** 2 for v in range(N))


def nonlinear_remainder(state: int) -> Q:
    x = x_vector(state)
    return sum(
        PI[v] * x[v] ** 2 * (1 - x[v]) / (1 + x[v])
        for v in range(N)
    )


def k_theta(state: int) -> Q:
    e, _ = error_vectors(state)
    return sum(PI[v] * e[v] ** 2 for v in range(N))


def spectral_cross(state: int) -> Q:
    return sum(
        indicator(state)[i] * K_F[i][j] * selection_vector(state)[j]
        for i in range(N)
        for j in range(N)
    )


def spectral_diagonal(state: int) -> Q:
    activity = activity_vector(state)
    return sum(K_F[v][v] * activity[v] for v in range(N))


def spectral_currents(state: int) -> tuple[Q, Q]:
    """Signed creation and debt currents of the positive spectral storage."""

    s = indicator(state)
    image = matvec(K_F, s)
    x = x_vector(state)
    creation = Q(0)
    debt = Q(0)
    for v in range(N):
        if bit(state, v):
            rate = (1 - x[v]) / (1 + x[v])
            debt += rate * (2 * image[v] - K_F[v][v])
        else:
            rate = 2 * x[v] / (1 + x[v])
            creation += rate * (2 * image[v] + K_F[v][v])
    return creation, debt


def spectral_remainder(state: int) -> Q:
    coefficient = kappa() + Q(2, N - 1)
    return (
        nonlinear_remainder(state)
        + coefficient * cut(state)
        - 2 * spectral_cross(state)
        - spectral_diagonal(state)
    )


def target_residual(state: int) -> Q:
    coefficient = kappa() + Q(2, N - 1)
    return (
        k_theta(state)
        + nonlinear_remainder(state)
        + coefficient * cut(state)
        - THETA ** 2 * variance(state)
    )


def e1(state: int) -> Q:
    return sum(
        PI[i] * P[i][j]
        for i in range(N)
        for j in range(i + 1, N)
        if bit(state, i) and bit(state, j)
    )


def q_entry(i: int, j: int) -> Q:
    return sum(PI[v] * P[v][i] * P[v][j] for v in range(N))


def e2(state: int) -> Q:
    return sum(
        q_entry(i, j)
        for i in range(N)
        for j in range(i + 1, N)
        if bit(state, i) and bit(state, j)
    )


def e3(state: int) -> Q:
    return sum(
        PI[i] * PI[j]
        for i in range(N)
        for j in range(i + 1, N)
        if bit(state, i) and bit(state, j)
    )


def pair_storage(state: int) -> tuple[Q, Q]:
    return (ALPHA * e1(state) - e3(state), e2(state) - BETA * e1(state))


def mark_storage(state: int) -> tuple[Q, Q]:
    return (
        sum((PI[v] * H1[v] for v in range(N) if bit(state, v)), Q(0)),
        sum((PI[v] * H2[v] for v in range(N) if bit(state, v)), Q(0)),
    )


def centered_storage(state: int) -> tuple[Q, Q]:
    g = pair_storage(state)
    h = mark_storage(state)
    return (g[0] - h[0] / Q(2), g[1] - h[1] / Q(2))


def phase_mark_storage(state: int) -> tuple[Q, Q, Q]:
    h = mark_storage(state)
    return (stationary_mass(state), h[0], h[1])


def phase_pair_storage(state: int) -> tuple[Q, Q, Q]:
    """The rank-centred pair coordinate used by the Bellman transfer."""

    rank = state.bit_count()
    centered = centered_storage(state)
    radial = e1(state) - Q(2 * rank - 1, 2 * (N - 1)) * stationary_mass(state)
    return (radial, centered[0], centered[1])


def error_vectors(state: int) -> tuple[tuple[Q, ...], tuple[Q, ...]]:
    s = tuple(Q(bit(state, v)) for v in range(N))
    x = matvec(P, s)
    mass = stationary_mass(state)
    e = tuple(s[v] - x[v] - THETA * (s[v] - mass) for v in range(N))
    pe = matvec(P, e)
    f = tuple(e[v] - pe[v] for v in range(N))
    return e, f


def oriented_currents(state: int):
    """Return pair currents, mark currents, and the two Schur error rows."""

    x = x_vector(state)
    y = matvec(P2, tuple(Q(bit(state, i)) for i in range(N)))
    e, f = error_vectors(state)
    pair_plus = [Q(0), Q(0)]
    pair_minus = [Q(0), Q(0)]
    mark_plus = [Q(0), Q(0)]
    mark_minus = [Q(0), Q(0)]
    error_plus = [Q(0), Q(0)]
    error_minus = [Q(0), Q(0)]
    p_mass = Q(0)
    n_mass = Q(0)
    for v in range(N):
        if bit(state, v):
            weight = PI[v] * (1 - x[v]) / (1 + x[v])
            n_mass += weight
            pair_minus[0] += weight * (ALPHA * x[v] - (stationary_mass(state) - PI[v]))
            pair_minus[1] += weight * ((y[v] - R_DIAGONAL[v]) - BETA * x[v])
            mark_minus[0] += weight * H1[v]
            mark_minus[1] += weight * H2[v]
            error_minus[0] += weight * (-ALPHA * e[v])
            error_minus[1] += weight * f[v]
        else:
            weight = PI[v] * 2 * x[v] / (1 + x[v])
            p_mass += weight
            pair_plus[0] += weight * (ALPHA * x[v] - stationary_mass(state))
            pair_plus[1] += weight * (y[v] - BETA * x[v])
            mark_plus[0] += weight * H1[v]
            mark_plus[1] += weight * H2[v]
            error_plus[0] += weight * (-ALPHA * e[v])
            error_plus[1] += weight * f[v]
    return tuple(pair_plus), tuple(pair_minus), tuple(mark_plus), tuple(mark_minus), tuple(error_plus), tuple(error_minus), p_mass, n_mass


def three_phase_currents(state: int):
    """Add the rank-centred mass/request phase to the two pair phases."""

    x = x_vector(state)
    e, f = error_vectors(state)
    mass = stationary_mass(state)
    rank = state.bit_count()
    m = mass - Q(rank, N)
    up_ratio = Q(rank, N - 1)
    down_ratio = Q(rank - 1, N - 1)
    plus = [Q(0), Q(0), Q(0)]
    minus = [Q(0), Q(0), Q(0)]
    p_mass = Q(0)
    n_mass = Q(0)
    for v in range(N):
        if bit(state, v):
            weight = PI[v] * (1 - x[v]) / (1 + x[v])
            n_mass += weight
            minus[0] += weight * (x[v] - down_ratio)
            minus[1] += weight * (-ALPHA * e[v])
            minus[2] += weight * f[v]
            assert x[v] - down_ratio == THETA * m - e[v]
        else:
            weight = PI[v] * 2 * x[v] / (1 + x[v])
            p_mass += weight
            plus[0] += weight * (x[v] - up_ratio)
            plus[1] += weight * (-ALPHA * e[v])
            plus[2] += weight * f[v]
            assert x[v] - up_ratio == THETA * m - e[v]
    return tuple(plus), tuple(minus), p_mass, n_mass, m


def generator(state: int, values: tuple[tuple[Q, Q], ...]) -> tuple[Q, Q]:
    answer = [Q(0), Q(0)]
    for target, rate in rates(state):
        for a in range(2):
            answer[a] += rate * (values[target][a] - values[state][a])
    return tuple(answer)


def scalar_generator(state: int, values: tuple[Q, ...]) -> Q:
    return sum(rate * (values[target] - values[state]) for target, rate in rates(state))


def exact_green():
    transient = list(range(1, FULL))
    index = {state: j for j, state in enumerate(transient)}
    matrix = [[Q(0) for _ in transient] for _ in transient]
    full_rate = [Q(0) for _ in transient]
    for state in transient:
        row = index[state]
        outgoing = rates(state)
        matrix[row][row] -= sum(rate for _, rate in outgoing)
        for target, rate in outgoing:
            if target in index:
                matrix[row][index[target]] += rate
            elif target == FULL:
                full_rate[row] += rate
    source = [Q(1, N) if state.bit_count() == 1 else Q(0) for state in transient]
    transpose = [[matrix[j][i] for j in range(len(transient))] for i in range(len(transient))]
    occupation = solve_linear(transpose, [-value for value in source])
    harmonic = solve_linear(matrix, [-value for value in full_rate])
    rho = sum(harmonic[index[1 << v]] for v in range(N)) / N
    return transient, dict(zip(transient, occupation)), rho


def verify_state_identities() -> None:
    assert all(sum(row) == 1 for row in P)
    assert all(P[v][v] == 0 for v in range(N))
    assert sum(PI) == 1
    assert all(PI[v] * P[v][i] == PI[i] * P[i][v] for v in range(N) for i in range(N))
    assert all(K_F[i][j] == K_F[j][i] for i in range(N) for j in range(N))
    assert all(sum(K_F[i]) == 0 for i in range(N))
    assert TRACE_K_F == THETA * (1 - SIGMA) - Q(1, 2)
    assert all(K_E[i][j] == K_E[j][i] for i in range(N) for j in range(N))
    assert all(sum(K_E[i]) == 0 for i in range(N))
    assert all(K_G[i][j] == K_G[j][i] for i in range(N) for j in range(N))
    assert all(sum(K_G[i]) == 0 for i in range(N))
    assert matmul(matmul(K_F, K_F_QUOTIENT_INVERSE), K_E) == K_E
    assert TRACE_K_G > 0
    for mask in range(1, 1 << N):
        vertices = [v for v in range(N) if bit(mask, v)]
        principal = [[K_F[i][j] for j in vertices] for i in vertices]
        assert determinant(principal) >= 0
        green_principal = [[K_G[i][j] for j in vertices] for i in vertices]
        assert determinant(green_principal) >= 0
    assert sum(PI[v] * H1[v] for v in range(N)) == DELTA
    assert sum(PI[v] * H2[v] for v in range(N)) == -EPSILON

    g_values = tuple(pair_storage(state) for state in range(FULL + 1))
    h_values = tuple(mark_storage(state) for state in range(FULL + 1))
    c_values = tuple(centered_storage(state) for state in range(FULL + 1))
    assert g_values[0] == (0, 0)
    assert g_values[FULL] == (DELTA / 2, -EPSILON / 2)
    assert h_values[FULL] == BOUNDARY_VECTOR
    assert c_values[FULL] == (0, 0)
    assert tuple(sum(g_values[1 << v][a] for v in range(N)) / N for a in range(2)) == (0, 0)
    assert tuple(sum(c_values[1 << v][a] for v in range(N)) / N for a in range(2)) == tuple(-value / (2 * N) for value in BOUNDARY_VECTOR)

    multiplier = (Q(3, 7), Q(-5, 11))
    multiplier3 = (Q(-2, 9), Q(3, 8), Q(5, 12))
    constants = tuple(Q((k + 2) * (k + 5), 3 * k + 7) for k in range(N + 1))
    p_profile = tuple(
        (Q(k + 1, k + 2), Q(2 * k - 3, 2 * k + 5), Q(5 - k, 3 * k + 4))
        for k in range(N + 1)
    )
    q_profile = tuple(
        (Q(3 - k, 2 * k + 3), Q(k + 4, 5 * k + 7), Q(2 * k - 1, 4 * k + 9))
        for k in range(N + 1)
    )
    profile_values = tuple(
        constants[state.bit_count()]
        + sum(
            p_profile[state.bit_count()][a] * phase_pair_storage(state)[a]
            + q_profile[state.bit_count()][a] * phase_mark_storage(state)[a]
            for a in range(3)
        )
        for state in range(FULL + 1)
    )
    spectral_values = tuple(spectral_storage(state) for state in range(FULL + 1))
    green_values = tuple(green_schur_storage(state) for state in range(FULL + 1))
    gauge_values = tuple(affine_spectral_gauge(state) for state in range(FULL + 1))
    assert spectral_values[0] == spectral_values[FULL] == 0
    assert green_values[0] == green_values[FULL] == 0
    assert all(value >= 0 for value in green_values)
    assert sum(spectral_values[1 << v] for v in range(N)) / N == TRACE_K_F / N
    assert sum(green_values[1 << v] for v in range(N)) / N == TRACE_K_G / N
    assert gauge_values[0] == 0
    assert gauge_values[FULL] == Q(1, 2)
    assert sum(gauge_values[1 << v] for v in range(N)) / N == -TRACE_K_F / N
    for state in range(1, FULL):
        assert spectral_values[state] == THETA * variance(state) - cut(state) / 2
        assert spectral_values[state] >= 0
        spectral_drift = scalar_generator(state, spectral_values)
        spectral_creation, spectral_debt = spectral_currents(state)
        assert spectral_drift == spectral_creation - spectral_debt
        assert spectral_drift == (
            k_theta(state)
            - THETA ** 2 * variance(state)
            + 2 * spectral_cross(state)
            + spectral_diagonal(state)
        )
        assert target_residual(state) == spectral_drift + spectral_remainder(state)
        # The apparently new spectral remainder is exactly an affine
        # mass-square gauge.  In particular, the fixed affine conjugate
        # contributes no independent coercive inequality.
        assert target_residual(state) == (
            kappa() * cut(state) - selection_gain(state)
        )
        assert spectral_remainder(state) == (
            scalar_generator(state, gauge_values)
            - (1 - kappa()) * cut(state)
        )
        green_dissipation = green_schur_dissipation(state)
        assert green_dissipation >= 0
        assert scalar_generator(state, green_values) == (
            -2 * green_dissipation
            + 2 * green_schur_cross(state)
            + green_schur_diagonal(state)
        )
        mass = stationary_mass(state)
        state_variance = variance(state)
        state_cut = cut(state)
        state_prediction_error = prediction_error(state)
        x = x_vector(state)
        selection = selection_vector(state)
        gain = selection_gain(state)
        inside_mean_x = sum(
            PI[v] * x[v] for v in range(N) if bit(state, v)
        ) / mass
        outside_mean_x = sum(
            PI[v] * x[v] for v in range(N) if not bit(state, v)
        ) / (1 - mass)
        inside_mean_a = sum(
            PI[v] * selection[v] for v in range(N) if bit(state, v)
        ) / mass
        outside_mean_a = sum(
            PI[v] * selection[v] for v in range(N) if not bit(state, v)
        ) / (1 - mass)
        assert inside_mean_x == 1 - state_cut / mass
        assert outside_mean_x == state_cut / (1 - mass)
        conditional_x_variance = sum(
            PI[v]
            * (x[v] - (inside_mean_x if bit(state, v) else outside_mean_x)) ** 2
            for v in range(N)
        )
        conditional_a_variance = sum(
            PI[v]
            * (
                selection[v]
                - (inside_mean_a if bit(state, v) else outside_mean_a)
            ) ** 2
            for v in range(N)
        )
        schur_variance = (
            state_prediction_error - state_cut * state_cut / state_variance
        )
        assert conditional_x_variance == schur_variance
        assert conditional_a_variance <= schur_variance
        two_level_gain = (
            (1 - mass)
            * outside_mean_x * (1 - outside_mean_x) / (1 + outside_mean_x)
            + mass
            * inside_mean_x * (1 - inside_mean_x) / (1 + inside_mean_x)
        )
        assert two_level_gain - gain >= schur_variance / 4
        assert kappa() * state_cut - gain >= (
            kappa() * state_cut - two_level_gain + schur_variance / 4
        )
        centered_selection_norm = sum(
            PI[v] * (selection[v] - gain) ** 2 for v in range(N)
        )
        assert centered_selection_norm <= nonlinear_remainder(state)
        quotient_source = tuple(
            PI[v] * (selection[v] - gain) for v in range(N)
        )
        quotient_image = matvec(K_F_QUOTIENT_INVERSE, quotient_source)
        quotient_metric = sum(
            quotient_source[v] * quotient_image[v] for v in range(N)
        )
        assert quotient_metric <= (N - 1) * nonlinear_remainder(state)

        pair_plus, pair_minus, mark_plus, mark_minus, error_plus, error_minus, p_mass, n_mass = oriented_currents(state)
        assert pair_plus == error_plus
        assert tuple(pair_minus[a] - mark_minus[a] for a in range(2)) == error_minus
        assert generator(state, g_values) == tuple(pair_plus[a] - pair_minus[a] for a in range(2))
        assert generator(state, h_values) == tuple(mark_plus[a] - mark_minus[a] for a in range(2))
        assert generator(state, c_values) == tuple(
            pair_plus[a] - mark_plus[a] / 2 - pair_minus[a] + mark_minus[a] / 2
            for a in range(2)
        )

        e, f = error_vectors(state)
        action = sum(
            PI[v] * (multiplier[0] * (-ALPHA * e[v]) + multiplier[1] * f[v]) ** 2
            for v in range(N)
        )
        up = sum(multiplier[a] * error_plus[a] for a in range(2))
        down = sum(multiplier[a] * error_minus[a] for a in range(2))
        assert up * up <= p_mass * action
        assert down * down <= n_mass * action

        k_theta_value = sum(PI[v] * e[v] * e[v] for v in range(N))
        endpoint_zero = (ALPHA * multiplier[0]) ** 2
        endpoint_two = (-ALPHA * multiplier[0] + 2 * multiplier[1]) ** 2
        assert action <= max(endpoint_zero, endpoint_two) * k_theta_value

        phase_plus, phase_minus, phase_p_mass, phase_n_mass, m = three_phase_currents(state)
        assert phase_plus[1:] == error_plus
        assert phase_minus[1:] == error_minus
        phase_action = sum(
            PI[v]
            * (
                multiplier3[0] * THETA * m
                - (multiplier3[0] + ALPHA * multiplier3[1]) * e[v]
                + multiplier3[2] * f[v]
            ) ** 2
            for v in range(N)
        )
        phase_up = sum(multiplier3[a] * phase_plus[a] for a in range(3))
        phase_down = sum(multiplier3[a] * phase_minus[a] for a in range(3))
        assert phase_up * phase_up <= phase_p_mass * phase_action
        assert phase_down * phase_down <= phase_n_mass * phase_action
        phase_endpoint_zero = (multiplier3[0] + ALPHA * multiplier3[1]) ** 2
        phase_endpoint_two = (
            -multiplier3[0] - ALPHA * multiplier3[1]
            + 2 * multiplier3[2]
        ) ** 2
        phase_bound = multiplier3[0] ** 2 * THETA ** 2 * m ** 2
        phase_bound += max(phase_endpoint_zero, phase_endpoint_two) * k_theta_value
        assert phase_action <= phase_bound

        rank = state.bit_count()
        # ``z`` depends on the target through ``e_v``; verify the vector
        # transition identities one target at a time.
        for target, _ in rates(state):
            vertex = (state ^ target).bit_length() - 1
            local_z = (
                THETA * (stationary_mass(state) - Q(rank, N)) - e[vertex],
                -ALPHA * e[vertex],
                f[vertex],
            )
            h_hat = (Q(1), H1[vertex], H2[vertex])
            h_tilde = (Q(1, N - 1), H1[vertex], H2[vertex])
            old_pair = phase_pair_storage(state)
            new_pair = phase_pair_storage(target)
            old_mark = phase_mark_storage(state)
            new_mark = phase_mark_storage(target)
            if target.bit_count() == rank + 1:
                assert tuple(new_mark[a] - old_mark[a] for a in range(3)) == tuple(
                    PI[vertex] * h_hat[a] for a in range(3)
                )
                assert tuple(new_pair[a] - old_pair[a] for a in range(3)) == tuple(
                    PI[vertex] * (local_z[a] - h_tilde[a] / 2)
                    - (stationary_mass(state) / (N - 1) if a == 0 else 0)
                    for a in range(3)
                )
            else:
                assert tuple(old_mark[a] - new_mark[a] for a in range(3)) == tuple(
                    PI[vertex] * h_hat[a] for a in range(3)
                )
                assert tuple(old_pair[a] - new_pair[a] for a in range(3)) == tuple(
                    PI[vertex] * (local_z[a] + h_tilde[a] / 2)
                    - (stationary_mass(state) / (N - 1) if a == 0 else 0)
                    for a in range(3)
                )

        pair = phase_pair_storage(state)
        mark = phase_mark_storage(state)
        up_rate = sum(rate for target, rate in rates(state) if target.bit_count() == rank + 1)
        down_rate = sum(rate for target, rate in rates(state) if target.bit_count() == rank - 1)
        transfer = (constants[rank + 1] - constants[rank]) * up_rate
        transfer += (constants[rank - 1] - constants[rank]) * down_rate
        transfer += sum(
            (p_profile[rank + 1][a] - p_profile[rank][a]) * pair[a] * up_rate
            + (p_profile[rank - 1][a] - p_profile[rank][a]) * pair[a] * down_rate
            + (q_profile[rank + 1][a] - q_profile[rank][a]) * mark[a] * up_rate
            + (q_profile[rank - 1][a] - q_profile[rank][a]) * mark[a] * down_rate
            for a in range(3)
        )
        transfer -= p_profile[rank + 1][0] * stationary_mass(state) * up_rate / (N - 1)
        transfer += p_profile[rank - 1][0] * stationary_mass(state) * down_rate / (N - 1)
        oriented = Q(0)
        for target, rate in rates(state):
            vertex = (state ^ target).bit_length() - 1
            local_z = (
                THETA * (stationary_mass(state) - Q(rank, N)) - e[vertex],
                -ALPHA * e[vertex],
                f[vertex],
            )
            h_hat = (Q(1), H1[vertex], H2[vertex])
            h_tilde = (Q(1, N - 1), H1[vertex], H2[vertex])
            if target.bit_count() == rank + 1:
                oriented += rate * PI[vertex] * sum(
                    p_profile[rank + 1][a] * (local_z[a] - h_tilde[a] / 2)
                    + q_profile[rank + 1][a] * h_hat[a]
                    for a in range(3)
                )
            else:
                oriented -= rate * PI[vertex] * sum(
                    p_profile[rank - 1][a] * (local_z[a] + h_tilde[a] / 2)
                    + q_profile[rank - 1][a] * h_hat[a]
                    for a in range(3)
                )
        assert scalar_generator(state, profile_values) == transfer + oriented


def verify_rank_recurrences() -> Q:
    transient, occupation, rho = exact_green()
    pair_values = tuple(pair_storage(state) for state in range(FULL + 1))
    mark_values = tuple(mark_storage(state) for state in range(FULL + 1))
    centered_values = tuple(centered_storage(state) for state in range(FULL + 1))

    x_pair = [[Q(0), Q(0)] for _ in range(N + 1)]
    y_pair = [[Q(0), Q(0)] for _ in range(N + 1)]
    x_mark = [[Q(0), Q(0)] for _ in range(N + 1)]
    y_mark = [[Q(0), Q(0)] for _ in range(N + 1)]
    x_centered = [[Q(0), Q(0)] for _ in range(N + 1)]
    y_centered = [[Q(0), Q(0)] for _ in range(N + 1)]
    pair_plus = [[Q(0), Q(0)] for _ in range(N + 1)]
    pair_minus = [[Q(0), Q(0)] for _ in range(N + 1)]
    mark_plus = [[Q(0), Q(0)] for _ in range(N + 1)]
    mark_minus = [[Q(0), Q(0)] for _ in range(N + 1)]
    error_plus = [[Q(0), Q(0)] for _ in range(N + 1)]
    error_minus = [[Q(0), Q(0)] for _ in range(N + 1)]
    p_mass = [Q(0) for _ in range(N + 1)]
    n_mass = [Q(0) for _ in range(N + 1)]
    action = [Q(0) for _ in range(N + 1)]
    multiplier = (Q(2, 5), Q(7, 13))
    phase_plus = [[Q(0), Q(0), Q(0)] for _ in range(N + 1)]
    phase_minus = [[Q(0), Q(0), Q(0)] for _ in range(N + 1)]
    phase_action = [Q(0) for _ in range(N + 1)]
    multiplier3 = (Q(4, 9), Q(-3, 10), Q(5, 17))
    spectral_generator_integral = Q(0)
    spectral_remainder_integral = Q(0)
    target_residual_integral = Q(0)
    gauge_generator_integral = Q(0)
    cut_integral = Q(0)
    gain_integral = Q(0)
    green_generator_integral = Q(0)
    green_dissipation_integral = Q(0)
    green_cross_integral = Q(0)
    green_diagonal_integral = Q(0)
    spectral_values = tuple(spectral_storage(value) for value in range(FULL + 1))
    green_values = tuple(green_schur_storage(value) for value in range(FULL + 1))
    gauge_values = tuple(affine_spectral_gauge(value) for value in range(FULL + 1))
    spectral_x = [Q(0) for _ in range(N + 1)]
    spectral_y = [Q(0) for _ in range(N + 1)]
    spectral_creation = [Q(0) for _ in range(N + 1)]
    spectral_debt = [Q(0) for _ in range(N + 1)]

    for state in transient:
        mu = occupation[state]
        k = state.bit_count()
        spectral_generator_integral += mu * scalar_generator(state, spectral_values)
        spectral_remainder_integral += mu * spectral_remainder(state)
        target_residual_integral += mu * target_residual(state)
        gauge_generator_integral += mu * scalar_generator(state, gauge_values)
        cut_integral += mu * cut(state)
        gain_integral += mu * selection_gain(state)
        green_generator_integral += mu * scalar_generator(state, green_values)
        green_dissipation_integral += mu * green_schur_dissipation(state)
        green_cross_integral += mu * green_schur_cross(state)
        green_diagonal_integral += mu * green_schur_diagonal(state)
        up_rate = sum(rate for target, rate in rates(state) if target.bit_count() == k + 1)
        down_rate = sum(rate for target, rate in rates(state) if target.bit_count() == k - 1)
        spectral_x[k] += mu * spectral_values[state] * up_rate
        spectral_y[k] += mu * spectral_values[state] * down_rate
        state_creation, state_debt = spectral_currents(state)
        spectral_creation[k] += mu * state_creation
        spectral_debt[k] += mu * state_debt
        currents = oriented_currents(state)
        for a in range(2):
            x_pair[k][a] += mu * pair_values[state][a] * up_rate
            y_pair[k][a] += mu * pair_values[state][a] * down_rate
            x_mark[k][a] += mu * mark_values[state][a] * up_rate
            y_mark[k][a] += mu * mark_values[state][a] * down_rate
            x_centered[k][a] += mu * centered_values[state][a] * up_rate
            y_centered[k][a] += mu * centered_values[state][a] * down_rate
            pair_plus[k][a] += mu * currents[0][a]
            pair_minus[k][a] += mu * currents[1][a]
            mark_plus[k][a] += mu * currents[2][a]
            mark_minus[k][a] += mu * currents[3][a]
            error_plus[k][a] += mu * currents[4][a]
            error_minus[k][a] += mu * currents[5][a]
        p_mass[k] += mu * currents[6]
        n_mass[k] += mu * currents[7]
        e, f = error_vectors(state)
        action[k] += mu * sum(
            PI[v] * (multiplier[0] * (-ALPHA * e[v]) + multiplier[1] * f[v]) ** 2
            for v in range(N)
        )
        phases = three_phase_currents(state)
        for a in range(3):
            phase_plus[k][a] += mu * phases[0][a]
            phase_minus[k][a] += mu * phases[1][a]
        phase_action[k] += mu * sum(
            PI[v]
            * (
                multiplier3[0] * THETA * phases[4]
                - (multiplier3[0] + ALPHA * multiplier3[1]) * e[v]
                + multiplier3[2] * f[v]
            ) ** 2
            for v in range(N)
        )

    for k in range(1, N + 1):
        for a in range(2):
            pair_residual = x_pair[k - 1][a] + pair_plus[k - 1][a]
            if k < N:
                pair_residual += y_pair[k + 1][a] - pair_minus[k + 1][a]
            pair_residual -= x_pair[k][a] + y_pair[k][a]
            pair_residual -= rho * BOUNDARY_VECTOR[a] / 2 * (k == N)
            assert pair_residual == 0

            mark_residual = BOUNDARY_VECTOR[a] / N * (k == 1)
            mark_residual += x_mark[k - 1][a] + mark_plus[k - 1][a]
            if k < N:
                mark_residual += y_mark[k + 1][a] - mark_minus[k + 1][a]
            mark_residual -= x_mark[k][a] + y_mark[k][a]
            mark_residual -= rho * BOUNDARY_VECTOR[a] * (k == N)
            assert mark_residual == 0

            centered_residual = -BOUNDARY_VECTOR[a] / (2 * N) * (k == 1)
            centered_residual += x_centered[k - 1][a]
            centered_residual += pair_plus[k - 1][a] - mark_plus[k - 1][a] / 2
            if k < N:
                centered_residual += y_centered[k + 1][a]
                centered_residual -= pair_minus[k + 1][a] - mark_minus[k + 1][a] / 2
            centered_residual -= x_centered[k][a] + y_centered[k][a]
            assert centered_residual == 0

        up = sum(multiplier[a] * error_plus[k][a] for a in range(2))
        down = sum(multiplier[a] * error_minus[k][a] for a in range(2))
        assert up * up <= p_mass[k] * action[k]
        assert down * down <= n_mass[k] * action[k]
        phase_up = sum(multiplier3[a] * phase_plus[k][a] for a in range(3))
        phase_down = sum(multiplier3[a] * phase_minus[k][a] for a in range(3))
        assert phase_up * phase_up <= p_mass[k] * phase_action[k]
        assert phase_down * phase_down <= n_mass[k] * phase_action[k]

        if k < N:
            spectral_residual = TRACE_K_F / N * (k == 1)
            spectral_residual += spectral_x[k - 1] + spectral_creation[k - 1]
            spectral_residual += spectral_y[k + 1] - spectral_debt[k + 1]
            spectral_residual -= spectral_x[k] + spectral_y[k]
            assert spectral_residual == 0

    for a in range(2):
        assert sum(pair_plus[k][a] - pair_minus[k][a] for k in range(1, N)) == rho * BOUNDARY_VECTOR[a] / 2
        assert sum(mark_plus[k][a] - mark_minus[k][a] for k in range(1, N)) == BOUNDARY_VECTOR[a] * (rho - Q(1, N))
        centered_total = sum(
            pair_plus[k][a] - mark_plus[k][a] / 2
            - pair_minus[k][a] + mark_minus[k][a] / 2
            for k in range(1, N)
        )
        assert centered_total == BOUNDARY_VECTOR[a] / (2 * N)
    assert spectral_generator_integral == -TRACE_K_F / N
    assert spectral_creation[N - 1] == -spectral_x[N - 1]
    assert spectral_debt[1] == spectral_y[1]
    assert sum(spectral_creation) - sum(spectral_debt) == -TRACE_K_F / N
    assert target_residual_integral == (
        spectral_remainder_integral - TRACE_K_F / N
    )
    assert gain_integral == rho - Q(1, N)
    assert cut_integral == Q(3, 2) * rho - Q(1, N)
    assert gauge_generator_integral == rho / 2 + TRACE_K_F / N
    assert spectral_remainder_integral == (
        gauge_generator_integral - (1 - kappa()) * cut_integral
    )
    assert target_residual_integral == kappa() * cut_integral - gain_integral
    assert green_generator_integral == -TRACE_K_G / N
    assert 2 * green_dissipation_integral == (
        2 * green_cross_integral
        + green_diagonal_integral
        + TRACE_K_G / N
    )
    complete = Q((N - 1) * 2 ** (N - 2), N * (2 ** (N - 1) - 1))
    assert (
        spectral_remainder_integral >= TRACE_K_F / N
    ) == (rho <= complete)
    return rho


def verify_complete_equality() -> None:
    complete = tuple(
        tuple(Q(0) if i == v else Q(1, N - 1) for i in range(N))
        for v in range(N)
    )
    pi = tuple(Q(1, N) for _ in range(N))
    complete_laplacian = tuple(
        tuple(pi[i] * ((i == j) - complete[i][j]) for j in range(N))
        for i in range(N)
    )
    complete_k_e = tuple(
        tuple(
            complete_laplacian[i][j]
            - THETA * (pi[i] * (i == j) - pi[i] * pi[j])
            for j in range(N)
        )
        for i in range(N)
    )
    assert all(value == 0 for row in complete_k_e for value in row)
    chi = sum(pi[v] * sum(value * value for value in complete[v]) for v in range(N))
    assert sum(value * value for value in pi) - Q(1, N) == 0
    assert chi - Q(1, N - 1) == 0
    for state in range(1, FULL):
        s = tuple(Q(bit(state, i)) for i in range(N))
        x = matvec(complete, s)
        mass = sum(pi[i] * s[i] for i in range(N))
        e = tuple(s[v] - x[v] - THETA * (s[v] - mass) for v in range(N))
        assert all(value == 0 for value in e)


def main() -> None:
    verify_state_identities()
    rho = verify_rank_recurrences()
    verify_complete_equality()
    print("three-channel boundary/current block: PASS")
    print(f"graph: n={N}, exact rational connected loopless weighted graph")
    print(f"delta={DELTA}, epsilon={EPSILON}")
    print(f"Tr(K_F)={TRACE_K_F}, singleton source={TRACE_K_F / N}")
    print(f"Tr(K_G)={TRACE_K_G}, Green-Schur source={TRACE_K_G / N}")
    print(f"exact fixation={rho}")
    print("state identities, spectral conjugate, rank recurrences, and vector SOC checked")


if __name__ == "__main__":
    main()
