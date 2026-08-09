#!/usr/bin/env python3
"""Independent exact verifier for the rank-pair dual conductance laws.

This script deliberately does not import the floating discovery programs.
All transition rates, Green occupations, optional-current conjugacies,
two-mark matrix balances, and identities are evaluated over
``fractions.Fraction``.
"""

from __future__ import annotations

from fractions import Fraction as F


WEIGHTS = (
    (0, 2, 0, 1),
    (2, 0, 3, 0),
    (0, 3, 0, 4),
    (1, 0, 4, 0),
)


def solve_linear(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Solve a nonsingular square rational system by Gauss-Jordan."""

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


def bit(state: int, vertex: int) -> bool:
    return bool(state >> vertex & 1)


def build_kernel():
    n = len(WEIGHTS)
    degree = [sum(row) for row in WEIGHTS]
    kernel = [
        [F(WEIGHTS[v][i], degree[v]) for i in range(n)] for v in range(n)
    ]
    total_degree = sum(degree)
    stationary = [F(value, total_degree) for value in degree]
    conductance = [
        [stationary[v] * kernel[v][i] for i in range(n)] for v in range(n)
    ]
    assert all(sum(row) == 1 for row in kernel)
    assert sum(stationary) == 1
    assert all(
        conductance[v][i] == conductance[i][v]
        for v in range(n)
        for i in range(n)
    )
    return kernel, stationary, conductance


P, PI, CONDUCTANCE = build_kernel()
N = len(P)
FULL = (1 << N) - 1


def x_value(state: int, vertex: int) -> F:
    return sum(P[vertex][i] for i in range(N) if bit(state, i))


def rates(state: int) -> list[tuple[int, F]]:
    result = []
    for vertex in range(N):
        x = x_value(state, vertex)
        if bit(state, vertex):
            rate = (1 - x) / (1 + x)
        else:
            rate = 2 * x / (1 + x)
        if rate:
            result.append((state ^ (1 << vertex), rate))
    return result


def mass(state: int) -> F:
    return sum(PI[i] for i in range(N) if bit(state, i))


def internal(state: int) -> F:
    return sum(
        CONDUCTANCE[i][j]
        for i in range(N)
        for j in range(i + 1, N)
        if bit(state, i) and bit(state, j)
    )


def storage(state: int) -> F:
    return mass(state) + internal(state)


def cut(state: int) -> F:
    return sum(
        CONDUCTANCE[i][j]
        for i in range(N)
        for j in range(N)
        if bit(state, i) and not bit(state, j)
    )


def selection_gain(state: int) -> F:
    """Drift of stationary mutant mass at fitness two."""

    return sum(
        PI[v] * x_value(state, v) * (1 - x_value(state, v))
        / (1 + x_value(state, v))
        for v in range(N)
    )


def generator(state: int, values: list[F]) -> F:
    return sum(rate * (values[target] - values[state]) for target, rate in rates(state))


def exact_green_occupation():
    transient = list(range(1, FULL))
    index = {state: j for j, state in enumerate(transient)}
    size = len(transient)
    q = [[F(0) for _ in transient] for _ in transient]
    for state in transient:
        row = index[state]
        outgoing = rates(state)
        q[row][row] -= sum(rate for _, rate in outgoing)
        for target, rate in outgoing:
            if target in index:
                q[row][index[target]] += rate

    initial = [F(1, N) if state.bit_count() == 1 else F(0) for state in transient]
    transpose = [[q[column][row] for column in range(size)] for row in range(size)]
    occupation = solve_linear(transpose, [-value for value in initial])

    # Independently solve the harmonic fixation equations.
    rhs = []
    harmonic_matrix = []
    for state in transient:
        row = [F(0) for _ in transient]
        outgoing = rates(state)
        row[index[state]] -= sum(rate for _, rate in outgoing)
        full_rate = F(0)
        for target, rate in outgoing:
            if target in index:
                row[index[target]] += rate
            elif target == FULL:
                full_rate += rate
        harmonic_matrix.append(row)
        rhs.append(-full_rate)
    fixation = solve_linear(harmonic_matrix, rhs)
    rho = sum(
        fixation[index[1 << vertex]] / N for vertex in range(N)
    )
    return transient, occupation, rho


def verify_storage_identities() -> None:
    h_values = [storage(state) for state in range(FULL + 1)]
    c_values = [cut(state) for state in range(FULL + 1)]
    assert storage(0) == 0
    assert storage(FULL) == F(3, 2)
    assert sum(storage(1 << i) for i in range(N)) / N == F(1, N)
    for state in range(1, FULL):
        for vertex in range(N):
            target = state ^ (1 << vertex)
            if bit(state, vertex):
                expected = -PI[vertex] * (1 + x_value(state, vertex))
            else:
                expected = PI[vertex] * (1 + x_value(state, vertex))
            assert h_values[target] - h_values[state] == expected
        assert generator(state, h_values) == c_values[state]

    # Check the full rank-weighted drift identity for a nontrivial sequence.
    q = [F((k + 2) * (k + 3), 2 * k + 3) for k in range(N + 1)]
    weighted = [q[state.bit_count()] * h_values[state] for state in range(FULL + 1)]
    for state in range(1, FULL):
        k = state.bit_count()
        u = sum(rate for target, rate in rates(state) if target.bit_count() == k + 1)
        d = sum(rate for target, rate in rates(state) if target.bit_count() == k - 1)
        right = h_values[state] * ((q[k + 1] - q[k]) * u + (q[k - 1] - q[k]) * d)
        right += c_values[state] * (2 * q[k + 1] - q[k - 1])
        assert generator(state, weighted) == right

    # In optional coordinates, the geometric rank profile turns the cut
    # reward into an exact drift on every (not necessarily complete) graph.
    geometric = [F(1, 2 ** (N - k)) for k in range(N + 1)]
    optional_values = [
        geometric[state.bit_count()] * h_values[state]
        for state in range(FULL + 1)
    ]
    for state in range(1, FULL):
        k = state.bit_count()
        optional_drift = F(0)
        for target, rate in rates(state):
            if target.bit_count() == k + 1:
                optional_drift += rate * (optional_values[target] - 2 * optional_values[state])
            else:
                optional_drift += rate * (4 * optional_values[target] - 2 * optional_values[state])
        assert optional_drift == 2 * geometric[k] * c_values[state]


def verify_dual_and_rank_recurrences() -> F:
    transient, occupation, rho = exact_green_occupation()
    y = {state: occupation[j] for j, state in enumerate(transient)}
    # The chosen sparse support has two transient configurations which are
    # not reached from a singleton, so nonnegativity (rather than strict
    # positivity) is the correct Green-law check.
    assert all(value >= 0 for value in occupation)

    # Full statewise dual conservation is stronger than rank-pair balance.
    for target in range(1, FULL + 1):
        residual = F(1, N) if target.bit_count() == 1 else F(0)
        for state in transient:
            outgoing = rates(state)
            residual -= y[state] * sum(rate for _, rate in outgoing) * (state == target)
            residual += y[state] * sum(
                rate for destination, rate in outgoing if destination == target
            )
        residual -= rho * (target == FULL)
        assert residual == 0

    a = [F(0) for _ in range(N + 1)]
    r = [F(0) for _ in range(N + 1)]
    xh = [F(0) for _ in range(N + 1)]
    yh = [F(0) for _ in range(N + 1)]
    cuts = [F(0) for _ in range(N + 1)]
    for state in transient:
        k = state.bit_count()
        up = sum(rate for target, rate in rates(state) if target.bit_count() == k + 1)
        down = sum(rate for target, rate in rates(state) if target.bit_count() == k - 1)
        a[k] += y[state] * up
        r[k] += y[state] * down
        xh[k] += y[state] * storage(state) * up
        yh[k] += y[state] * storage(state) * down
        cuts[k] += y[state] * cut(state)

    for k in range(1, N + 1):
        mass_residual = (k == 1) + a[k - 1]
        mass_residual += r[k + 1] if k < N else 0
        mass_residual -= a[k] + r[k] + rho * (k == N)
        assert mass_residual == 0

        storage_residual = F(1, N) * (k == 1)
        storage_residual += xh[k - 1] + 2 * cuts[k - 1]
        if k < N:
            storage_residual += yh[k + 1] - cuts[k + 1]
        storage_residual -= xh[k] + yh[k] + F(3, 2) * rho * (k == N)
        assert storage_residual == 0

    assert rho == a[N - 1] == 1 - r[1]
    assert F(1, N) + sum(cuts) == F(3, 2) * rho
    return rho


def bridge_test_function(state: int) -> F:
    """A deterministic slice-quadratic function with nontrivial boundary."""

    if state == 0:
        return F(0)
    occupied = [i for i in range(N) if bit(state, i)]
    k = len(occupied)
    value = F(2 * k + 1, 7)
    value += sum(F((k + 1) * (i + 2), 11) for i in occupied)
    value += sum(
        F((k + 2) * (i + j + 1), 13)
        for i in occupied
        for j in occupied
        if i < j
    )
    return value


def verify_geometric_green_bridge() -> None:
    """Check optional/Green conjugacy and the two-mark matrix identity."""

    transient, occupation, rho = exact_green_occupation()
    mu = {state: occupation[j] for j, state in enumerate(transient)}
    q = [F(1, 2 ** (N - k)) for k in range(N + 1)]
    eta = {state: mu[state] / (2 * q[state.bit_count()]) for state in transient}

    optional_top = sum(
        eta[state] for state in transient if state.bit_count() == N - 1
    )
    optional_bottom = sum(
        eta[state] for state in transient if state.bit_count() == 1
    )
    injection = optional_top + F(1, 2 ** (N - 2)) * optional_bottom
    assert optional_top == rho
    assert optional_bottom == 2 ** (N - 2) * (1 - rho)
    assert injection == 1
    theta = -(2 * optional_bottom + 2 ** (N - 1) * optional_top) / N
    assert -N * theta * q[1] == injection

    values = [bridge_test_function(state) for state in range(FULL + 1)]
    optional_values = [
        q[state.bit_count()] * values[state] for state in range(FULL + 1)
    ]
    optional_integral = F(0)
    green_integral = F(0)
    for state in transient:
        k = state.bit_count()
        optional_drift = F(0)
        for target, rate in rates(state):
            if target.bit_count() == k + 1:
                optional_drift += rate * (
                    optional_values[target] - 2 * optional_values[state]
                )
            else:
                optional_drift += rate * (
                    4 * optional_values[target] - 2 * optional_values[state]
                )
        ordinary_drift = generator(state, values)
        assert optional_drift == 2 * q[k] * ordinary_drift
        optional_integral += eta[state] * optional_drift
        green_integral += mu[state] * ordinary_drift

    boundary = optional_top * values[FULL]
    boundary += theta * q[1] * sum(values[1 << i] for i in range(N))
    assert optional_integral == green_integral == boundary
    assert (
        sum(values[1 << i] for i in range(N)) / N
        + green_integral
        - rho * values[FULL]
        == 0
    )

    # Matrix form of every one- and two-mark balance.
    matrix = [[F(0) for _ in range(N)] for _ in range(N)]
    for state in transient:
        indicator = [F(int(bit(state, i))) for i in range(N)]
        drift = []
        activity = []
        for i in range(N):
            x = x_value(state, i)
            if bit(state, i):
                drift.append(-(1 - x) / (1 + x))
                activity.append((1 - x) / (1 + x))
            else:
                drift.append(2 * x / (1 + x))
                activity.append(2 * x / (1 + x))
        for i in range(N):
            for j in range(N):
                entry = indicator[i] * drift[j] + drift[i] * indicator[j]
                if i == j:
                    entry += activity[i]
                    assert activity[i] == (1 - 2 * indicator[i]) * drift[i]
                matrix[i][j] += mu[state] * entry
    for i in range(N):
        for j in range(N):
            expected = rho - (F(1, N) if i == j else 0)
            assert matrix[i][j] == expected

    centered_mark = [F(3), F(-2), F(4), F(-5)]
    assert sum(centered_mark) == 0
    quadratic_balance = sum(
        centered_mark[i] * matrix[i][j] * centered_mark[j]
        for i in range(N)
        for j in range(N)
    )
    assert quadratic_balance == -sum(x * x for x in centered_mark) / N

    # Exact selection drift, collision occupation, and sharp conditional
    # Jensen inequality.  The latter is checked statewise on a non-equitable
    # rational graph and at equality on every complete-graph rank.
    gain_integral = F(0)
    cut_integral = F(0)
    mass_values = [mass(state) for state in range(FULL + 1)]
    for state in transient:
        gain = selection_gain(state)
        assert generator(state, mass_values) == gain
        mutant_mass = mass(state)
        collision_cut = cut(state)
        bound_ratio = (
            (1 - mutant_mass - collision_cut)
            / (1 - mutant_mass + collision_cut)
            + (mutant_mass - collision_cut)
            / (2 * mutant_mass - collision_cut)
        )
        assert gain <= collision_cut * bound_ratio
        gain_integral += mu[state] * gain
        cut_integral += mu[state] * collision_cut
    assert gain_integral == rho - F(1, N)
    assert cut_integral == F(3, 2) * rho - F(1, N)

    for k in range(1, N):
        mutant_mass = F(k, N)
        collision_cut = F(k * (N - k), N * (N - 1))
        x_out = F(k, N - 1)
        x_in = F(k - 1, N - 1)
        complete_gain = (
            F(N - k, N) * x_out * (1 - x_out) / (1 + x_out)
            + F(k, N) * x_in * (1 - x_in) / (1 + x_in)
        )
        bound_ratio = (
            (1 - mutant_mass - collision_cut)
            / (1 - mutant_mass + collision_cut)
            + (mutant_mass - collision_cut)
            / (2 * mutant_mass - collision_cut)
        )
        assert complete_gain == collision_cut * bound_ratio

    # The selection gain is a state-dependent mixture of categorical
    # covariance matrices.  Check the exact matrix identities and the
    # reversible square 2 L_pi-K_0=(I-P)^T Pi (I-P).
    covariance = []
    for v in range(N):
        matrix_v = [
            [
                (P[v][i] if i == j else F(0)) - P[v][i] * P[v][j]
                for j in range(N)
            ]
            for i in range(N)
        ]
        covariance.append(matrix_v)
        for test in (
            [F(1), F(-2), F(4), F(3)],
            [F(0), F(5), F(-1), F(2)],
        ):
            quadratic = sum(
                test[i] * matrix_v[i][j] * test[j]
                for i in range(N)
                for j in range(N)
            )
            variance = sum(P[v][i] * test[i] ** 2 for i in range(N))
            variance -= sum(P[v][i] * test[i] for i in range(N)) ** 2
            assert quadratic == variance >= 0

    k_zero = [
        [sum(PI[v] * covariance[v][i][j] for v in range(N)) for j in range(N)]
        for i in range(N)
    ]
    laplacian = [
        [(PI[i] if i == j else F(0)) - CONDUCTANCE[i][j] for j in range(N)]
        for i in range(N)
    ]
    assert all(
        k_zero[i][j]
        == (PI[i] if i == j else F(0))
        - sum(P[v][i] * PI[v] * P[v][j] for v in range(N))
        for i in range(N)
        for j in range(N)
    )
    reversible_square = [
        [
            sum(
                ((F(int(v == i)) - P[v][i]) * PI[v]
                 * (F(int(v == j)) - P[v][j]))
                for v in range(N)
            )
            for j in range(N)
        ]
        for i in range(N)
    ]
    assert all(
        2 * laplacian[i][j] - k_zero[i][j] == reversible_square[i][j]
        for i in range(N)
        for j in range(N)
    )

    for state in transient:
        indicator = [F(int(bit(state, i))) for i in range(N)]
        k_state = [
            [
                sum(
                    PI[v] * covariance[v][i][j]
                    / (1 + x_value(state, v))
                    for v in range(N)
                )
                for j in range(N)
            ]
            for i in range(N)
        ]
        matrix_gain = sum(
            indicator[i] * k_state[i][j] * indicator[j]
            for i in range(N)
            for j in range(N)
        )
        collision_sum = sum(
            PI[v] * P[v][i] * P[v][j]
            * (indicator[i] - indicator[j]) ** 2
            / (2 * (1 + x_value(state, v)))
            for v in range(N)
            for i in range(N)
            for j in range(N)
        )
        assert matrix_gain == collision_sum == selection_gain(state)
        sos = sum(
            PI[v] * (
                (indicator[v] - x_value(state, v)) ** 2
                + x_value(state, v) ** 2 * (1 - x_value(state, v))
                / (1 + x_value(state, v))
            )
            for v in range(N)
        )
        assert 2 * cut(state) - selection_gain(state) == sos >= 0

    baseline = F((N - 1) * 2 ** (N - 2), N * (2 ** (N - 1) - 1))
    kappa = F(
        2 * ((N - 3) * 2 ** N + 4),
        (3 * N - 7) * 2 ** N + 8,
    )
    assert (gain_integral <= kappa * cut_integral) == (rho <= baseline)


def verify_fixed_matrix_contractions() -> None:
    """Check the exact fixed-``L_pi``/``K_0`` contraction audit.

    This includes the two-step response, its sign changes, and the full
    rank-profile drift formula for a nonconstant rational profile.
    """

    transient, occupation, rho = exact_green_occupation()
    mu = {state: occupation[j] for j, state in enumerate(transient)}

    laplacian = [
        [(PI[i] if i == j else F(0)) - CONDUCTANCE[i][j] for j in range(N)]
        for i in range(N)
    ]
    k_zero = [
        [
            (PI[i] if i == j else F(0))
            - sum(P[v][i] * PI[v] * P[v][j] for v in range(N))
            for j in range(N)
        ]
        for i in range(N)
    ]
    p_squared = [
        [sum(P[i][v] * P[v][j] for v in range(N)) for j in range(N)]
        for i in range(N)
    ]
    chi = sum(
        PI[v] * sum(P[v][i] ** 2 for i in range(N)) for v in range(N)
    )
    assert chi >= F(1, N - 1)

    def indicator(state: int) -> list[F]:
        return [F(int(bit(state, i))) for i in range(N)]

    def quadratic(matrix: list[list[F]], vector: list[F]) -> F:
        return sum(
            vector[i] * matrix[i][j] * vector[j]
            for i in range(N)
            for j in range(N)
        )

    def drift_activity(state: int) -> tuple[list[F], list[F]]:
        drift = []
        activity = []
        for i in range(N):
            x = x_value(state, i)
            if bit(state, i):
                drift.append(-(1 - x) / (1 + x))
                activity.append((1 - x) / (1 + x))
            else:
                drift.append(2 * x / (1 + x))
                activity.append(2 * x / (1 + x))
        return drift, activity

    cut_values = [cut(state) for state in range(FULL + 1)]
    r_zero_values = [
        quadratic(k_zero, indicator(state)) for state in range(FULL + 1)
    ]
    assert all(
        r_zero_values[state]
        == sum(
            PI[v] * x_value(state, v) * (1 - x_value(state, v))
            for v in range(N)
        )
        for state in range(FULL + 1)
    )

    j_two = {}
    for state in transient:
        s = indicator(state)
        drift, activity = drift_activity(state)
        p2s = [sum(p_squared[i][j] * s[j] for j in range(N)) for i in range(N)]
        j_two[state] = 2 * sum(
            PI[i] * p2s[i] * drift[i] for i in range(N)
        ) + sum(
            PI[i] * p_squared[i][i] * activity[i] for i in range(N)
        )

        # The L_pi contraction is only the already-known boundary identity.
        assert generator(state, cut_values) == 3 * selection_gain(state) - 2 * cut(state)

        # The K_0 contraction is gain minus its signed two-step response.
        assert (
            generator(state, r_zero_values)
            == selection_gain(state) - j_two[state]
        )

    assert j_two[3] == F(3604, 11025) > 0
    assert j_two[4] == -F(107, 3024) < 0
    assert generator(3, r_zero_values) == -F(1882, 11025) < 0
    assert generator(4, r_zero_values) == F(719, 7560) > 0

    assert sum(
        mu[state] * generator(state, cut_values) for state in transient
    ) == -F(1, N)
    assert sum(
        mu[state] * generator(state, r_zero_values) for state in transient
    ) == -(1 - chi) / N
    assert sum(mu[state] * j_two[state] for state in transient) == rho - chi / N

    # Check the full rank-dependent formula with a deliberately nonconstant
    # rational sequence.  K_0 annihilates the all-ones vector, so both
    # absorbing boundary values vanish.
    profile = [F((k + 1) * (k + 4), 3 * k + 5) for k in range(N + 1)]
    weighted_values = [
        profile[state.bit_count()] * r_zero_values[state]
        for state in range(FULL + 1)
    ]
    for state in transient:
        k = state.bit_count()
        s = indicator(state)
        up = sum(
            rate for target, rate in rates(state) if target.bit_count() == k + 1
        )
        down = sum(
            rate for target, rate in rates(state) if target.bit_count() == k - 1
        )
        right = r_zero_values[state] * (
            (profile[k + 1] - profile[k]) * up
            + (profile[k - 1] - profile[k]) * down
        )
        for vertex in range(N):
            ks = sum(k_zero[vertex][j] * s[j] for j in range(N))
            if bit(state, vertex):
                x = x_value(state, vertex)
                rate = (1 - x) / (1 + x)
                right += profile[k - 1] * rate * (
                    -2 * ks + k_zero[vertex][vertex]
                )
            else:
                x = x_value(state, vertex)
                rate = 2 * x / (1 + x)
                right += profile[k + 1] * rate * (
                    2 * ks + k_zero[vertex][vertex]
                )
        assert generator(state, weighted_values) == right

    trace_k_zero = sum(k_zero[i][i] for i in range(N))
    assert trace_k_zero == 1 - chi
    assert (
        profile[1] * trace_k_zero / N
        + sum(
            mu[state] * generator(state, weighted_values)
            for state in transient
        )
        == 0
    )

    # For the constant profile, the diagonal carré term is nonnegative.
    mixed = F(0)
    diagonal_carre = F(0)
    for state in transient:
        s = indicator(state)
        drift, activity = drift_activity(state)
        mixed += mu[state] * sum(
            s[i] * k_zero[i][j] * drift[j]
            for i in range(N)
            for j in range(N)
        )
        diagonal_carre += mu[state] * sum(
            k_zero[i][i] * activity[i] for i in range(N)
        )
    assert diagonal_carre >= 0
    assert 2 * mixed + diagonal_carre == -trace_k_zero / N
    assert mixed <= -trace_k_zero / (2 * N)

    # The first genuinely new full-pair direction beyond H and K_0 is the
    # rank-one matrix pi*pi^T, i.e. stationary mutant mass squared.  Its
    # 2-by-2 covariance determinant gives the sharp statewise inequality
    # C^2 <= M(1-M) D, with D=2C-R_0.  Equality means that the request
    # probability is affine in the mutant indicator (constant on each side
    # of the cut), and holds on every complete-graph rank.
    stationary_square = sum(value * value for value in PI)
    stationary_covariance = [
        [
            (PI[i] if i == j else F(0)) - PI[i] * PI[j]
            for j in range(N)
        ]
        for i in range(N)
    ]
    prediction_error_matrix = [
        [2 * laplacian[i][j] - k_zero[i][j] for j in range(N)]
        for i in range(N)
    ]
    theta_test = F(7, 5)
    schur_matrix = [
        [
            prediction_error_matrix[i][j]
            - 2 * theta_test * laplacian[i][j]
            + theta_test ** 2 * stationary_covariance[i][j]
            for j in range(N)
        ]
        for i in range(N)
    ]
    prediction_minus_projection = [
        [
            (F(int(i == j)) - P[i][j])
            - theta_test * (F(int(i == j)) - PI[j])
            for j in range(N)
        ]
        for i in range(N)
    ]
    schur_gram = [
        [
            sum(
                prediction_minus_projection[v][i]
                * PI[v]
                * prediction_minus_projection[v][j]
                for v in range(N)
            )
            for j in range(N)
        ]
        for i in range(N)
    ]
    assert schur_matrix == schur_gram
    for test in (
        [F(1), F(-2), F(4), F(3)],
        [F(0), F(5), F(-1), F(2)],
    ):
        assert sum(
            test[i] * schur_matrix[i][j] * test[j]
            for i in range(N)
            for j in range(N)
        ) >= 0

    # The complete loopless kernel kills the square at the unique radial
    # value theta=n/(n-1).
    complete_theta = F(N, N - 1)
    complete_a = [
        [
            (F(int(i == j)) - (F(0) if i == j else F(1, N - 1)))
            - complete_theta * (F(int(i == j)) - F(1, N))
            for j in range(N)
        ]
        for i in range(N)
    ]
    assert all(value == 0 for row in complete_a for value in row)

    mass_values = [mass(state) for state in range(FULL + 1)]
    mass_square_values = [value * value for value in mass_values]
    mass_variance_values = [value * (1 - value) for value in mass_values]
    stationary_linear_values = [
        sum((PI[i] ** 2 for i in range(N) if bit(state, i)), F(0))
        for state in range(FULL + 1)
    ]
    product_internal_values = [
        F(mass_square_values[state] - stationary_linear_values[state]) / 2
        for state in range(FULL + 1)
    ]
    assert product_internal_values[0] == 0
    assert all(product_internal_values[1 << i] == 0 for i in range(N))
    assert product_internal_values[FULL] == (1 - stationary_square) / 2
    activity_square_integral = F(0)
    mass_gain_integral = F(0)
    for state in transient:
        mutant_mass = mass_values[state]
        variance = mutant_mass * (1 - mutant_mass)
        collision_cut = cut_values[state]
        collision_variance = r_zero_values[state]
        prediction_error = 2 * collision_cut - collision_variance
        request_variance = variance - collision_variance
        covariance = variance - collision_cut
        determinant = variance * request_variance - covariance * covariance
        assert determinant == variance * prediction_error - collision_cut ** 2
        assert determinant >= 0

        drift, activity = drift_activity(state)
        gain = sum(PI[v] * drift[v] for v in range(N))
        activity_square = sum(PI[v] ** 2 * activity[v] for v in range(N))
        assert gain == selection_gain(state)
        assert (
            generator(state, mass_square_values)
            == 2 * mutant_mass * gain + activity_square
        )
        activity_square_integral += mu[state] * activity_square
        mass_gain_integral += mu[state] * mutant_mass * gain

    assert (
        stationary_square / N
        + 2 * mass_gain_integral
        + activity_square_integral
        == rho
    )
    for k in range(1, N):
        variance = F(k * (N - k), N * N)
        collision_cut = F(k * (N - k), N * (N - 1))
        prediction_error = F(N, N - 1) * collision_cut
        assert variance * prediction_error == collision_cut ** 2

    # Resolve the L_pi contraction into its two oriented selection-gain
    # currents.  These are the minimal rank currents retained by the
    # rank-H plus arbitrary-one-mark dual.
    cut_occupation = [F(0) for _ in range(N + 1)]
    gain_up = [F(0) for _ in range(N + 1)]
    gain_down = [F(0) for _ in range(N + 1)]
    mass_up = [F(0) for _ in range(N + 1)]
    mass_down = [F(0) for _ in range(N + 1)]
    cut_up = [F(0) for _ in range(N + 1)]
    cut_down = [F(0) for _ in range(N + 1)]
    internal_up = [F(0) for _ in range(N + 1)]
    internal_down = [F(0) for _ in range(N + 1)]
    creation = [F(0) for _ in range(N + 1)]
    destruction = [F(0) for _ in range(N + 1)]
    mass_square_up = [F(0) for _ in range(N + 1)]
    mass_square_down = [F(0) for _ in range(N + 1)]
    mass_square_creation = [F(0) for _ in range(N + 1)]
    mass_square_destruction = [F(0) for _ in range(N + 1)]
    variance_occupation = [F(0) for _ in range(N + 1)]
    prediction_error_occupation = [F(0) for _ in range(N + 1)]
    nonlinear_remainder_by_rank = [F(0) for _ in range(N + 1)]
    variance_up = [F(0) for _ in range(N + 1)]
    variance_down = [F(0) for _ in range(N + 1)]
    variance_response_up = [F(0) for _ in range(N + 1)]
    variance_response_down = [F(0) for _ in range(N + 1)]
    product_internal_up = [F(0) for _ in range(N + 1)]
    product_internal_down = [F(0) for _ in range(N + 1)]
    product_creation = [F(0) for _ in range(N + 1)]
    product_destruction = [F(0) for _ in range(N + 1)]
    mass_creation = [F(0) for _ in range(N + 1)]
    mass_destruction = [F(0) for _ in range(N + 1)]
    stationary_mark_destruction = [F(0) for _ in range(N + 1)]
    complete_schur_occupation = [F(0) for _ in range(N + 1)]
    d_zero_integral = F(0)
    nonlinear_remainder_integral = F(0)
    internal_values = [internal(state) for state in range(FULL + 1)]
    assert internal_values[0] == 0
    assert internal_values[FULL] == F(1, 2)
    assert all(internal_values[1 << vertex] == 0 for vertex in range(N))
    for state in transient:
        k = state.bit_count()
        mutant_mass = mass(state)
        collision_cut = cut(state)
        up = F(0)
        down = F(0)
        q_plus = F(0)
        q_minus = F(0)
        mass_response_up = F(0)
        mass_response_down = F(0)
        cut_response_up = F(0)
        cut_response_down = F(0)
        square_response_up = F(0)
        square_response_down = F(0)
        variance_drift_up = F(0)
        variance_drift_down = F(0)
        product_creation_state = F(0)
        product_destruction_state = F(0)
        nonlinear_remainder = F(0)
        for vertex in range(N):
            x = x_value(state, vertex)
            local_gain = PI[vertex] * x * (1 - x) / (1 + x)
            if bit(state, vertex):
                rate = (1 - x) / (1 + x)
                down += rate
                q_minus += local_gain
                mass_response_down -= PI[vertex] * rate
                cut_response_down -= PI[vertex] * (1 - 2 * x) * rate
                square_response_down += rate * (
                    -2 * mutant_mass * PI[vertex] + PI[vertex] ** 2
                )
                variance_drift_down += rate * PI[vertex] * (
                    2 * mutant_mass - 1 - PI[vertex]
                )
                product_destruction_state += (
                    rate * PI[vertex] * (mutant_mass - PI[vertex])
                )
            else:
                rate = 2 * x / (1 + x)
                up += rate
                q_plus += local_gain
                mass_response_up += PI[vertex] * rate
                cut_response_up += PI[vertex] * (1 - 2 * x) * rate
                square_response_up += rate * (
                    2 * mutant_mass * PI[vertex] + PI[vertex] ** 2
                )
                variance_drift_up += rate * PI[vertex] * (
                    1 - 2 * mutant_mass - PI[vertex]
                )
                product_creation_state += rate * PI[vertex] * mutant_mass
            nonlinear_remainder += (
                PI[vertex] * x * x * (1 - x) / (1 + x)
            )

        assert mass_response_up == collision_cut + q_plus
        assert mass_response_down == q_minus - collision_cut
        assert cut_response_up == 3 * q_plus - collision_cut
        assert cut_response_down == 3 * q_minus - collision_cut
        assert q_plus + q_minus == selection_gain(state)
        assert 0 <= q_plus <= collision_cut
        assert 0 <= 2 * q_minus <= collision_cut
        assert generator(state, internal_values) == collision_cut - q_plus - q_minus
        assert (
            generator(state, mass_square_values)
            == square_response_up + square_response_down
        )
        assert (
            generator(state, mass_variance_values)
            == variance_drift_up + variance_drift_down
            == (1 - 2 * mutant_mass) * selection_gain(state)
            - sum(
                PI[vertex] ** 2
                * (
                    (1 - x_value(state, vertex)) / (1 + x_value(state, vertex))
                    if bit(state, vertex)
                    else 2 * x_value(state, vertex) / (1 + x_value(state, vertex))
                )
                for vertex in range(N)
            )
        )
        assert square_response_up >= 0
        assert square_response_down <= 0
        assert product_creation_state >= 0
        assert product_destruction_state >= 0
        assert (
            generator(state, product_internal_values)
            == product_creation_state - product_destruction_state
        )

        # The operator Schur square specializes on the mutant indicator to
        # the scalar covariance tangent checked above.
        indicator_state = indicator(state)
        schur_quadratic = quadratic(schur_matrix, indicator_state)
        assert schur_quadratic == (
            2 * collision_cut
            - r_zero_values[state]
            - 2 * theta_test * collision_cut
            + theta_test ** 2 * mutant_mass * (1 - mutant_mass)
        )

        # At the complete-kernel slope theta=n/(n-1), the discrepancies
        # between the first and third creation/debt channels are linear
        # functionals of the same Schur error.  Weighted Cauchy--Schwarz
        # gives the exact mixed-current cone used by the Riccati route.
        alpha = F(N - 1, N)
        theta_complete = 1 / alpha
        schur_error = []
        up_error = F(0)
        down_error = F(0)
        down_stationary_mark = F(0)
        for vertex in range(N):
            error = (
                F(int(bit(state, vertex))) - x_value(state, vertex)
                - theta_complete
                * (F(int(bit(state, vertex))) - mutant_mass)
            )
            schur_error.append(error)
            x = x_value(state, vertex)
            if bit(state, vertex):
                rate = (1 - x) / (1 + x)
                down_error += rate * PI[vertex] * error
                down_stationary_mark += (
                    rate * PI[vertex] * (PI[vertex] - F(1, N))
                )
            else:
                rate = 2 * x / (1 + x)
                up_error += rate * PI[vertex] * error
        complete_schur = sum(
            PI[vertex] * schur_error[vertex] ** 2 for vertex in range(N)
        )
        first_creation_state = collision_cut - q_plus
        first_destruction_state = q_minus
        assert (
            alpha * first_creation_state - product_creation_state
            == -alpha * up_error
        )
        assert (
            alpha * first_destruction_state
            - product_destruction_state
            - down_stationary_mark
            == -alpha * down_error
        )
        assert up_error ** 2 <= mass_response_up * complete_schur
        assert down_error ** 2 <= (-mass_response_down) * complete_schur

        weight = mu[state]
        cut_occupation[k] += weight * collision_cut
        gain_up[k] += weight * q_plus
        gain_down[k] += weight * q_minus
        mass_up[k] += weight * mutant_mass * up
        mass_down[k] += weight * mutant_mass * down
        cut_up[k] += weight * collision_cut * up
        cut_down[k] += weight * collision_cut * down
        internal_up[k] += weight * internal_values[state] * up
        internal_down[k] += weight * internal_values[state] * down
        creation[k] += weight * (collision_cut - q_plus)
        destruction[k] += weight * q_minus
        mass_square_up[k] += weight * mutant_mass ** 2 * up
        mass_square_down[k] += weight * mutant_mass ** 2 * down
        mass_square_creation[k] += weight * square_response_up
        mass_square_destruction[k] -= weight * square_response_down
        variance_occupation[k] += weight * mutant_mass * (1 - mutant_mass)
        variance_up[k] += weight * mutant_mass * (1 - mutant_mass) * up
        variance_down[k] += weight * mutant_mass * (1 - mutant_mass) * down
        variance_response_up[k] += weight * variance_drift_up
        variance_response_down[k] += weight * variance_drift_down
        product_internal_up[k] += (
            weight * product_internal_values[state] * up
        )
        product_internal_down[k] += (
            weight * product_internal_values[state] * down
        )
        product_creation[k] += weight * product_creation_state
        product_destruction[k] += weight * product_destruction_state
        mass_creation[k] += weight * mass_response_up
        mass_destruction[k] -= weight * mass_response_down
        stationary_mark_destruction[k] += weight * down_stationary_mark
        complete_schur_occupation[k] += weight * complete_schur

        d_zero = 2 * collision_cut - r_zero_values[state]
        direct_gradient = sum(
            PI[v]
            * (F(int(bit(state, v))) - x_value(state, v)) ** 2
            for v in range(N)
        )
        assert d_zero == direct_gradient >= 0
        assert (
            2 * collision_cut - selection_gain(state)
            == d_zero + nonlinear_remainder
        )
        d_zero_integral += weight * d_zero
        nonlinear_remainder_integral += weight * nonlinear_remainder
        prediction_error_occupation[k] += weight * d_zero
        nonlinear_remainder_by_rank[k] += weight * nonlinear_remainder

    # Rank-resolved M and C recurrences, including both boundary sources.
    for k in range(1, N + 1):
        mass_rank_residual = F(1, N) if k == 1 else F(0)
        if k > 1:
            mass_rank_residual += (
                mass_up[k - 1]
                + cut_occupation[k - 1]
                + gain_up[k - 1]
            )
        if k < N:
            mass_rank_residual += (
                mass_down[k + 1]
                + gain_down[k + 1]
                - cut_occupation[k + 1]
            )
            mass_rank_residual -= mass_up[k] + mass_down[k]
        mass_rank_residual -= rho if k == N else F(0)
        assert mass_rank_residual == 0

        cut_rank_residual = F(1, N) if k == 1 else F(0)
        if k > 1:
            cut_rank_residual += (
                cut_up[k - 1]
                + 3 * gain_up[k - 1]
                - cut_occupation[k - 1]
            )
        if k < N:
            cut_rank_residual += (
                cut_down[k + 1]
                + 3 * gain_down[k + 1]
                - cut_occupation[k + 1]
            )
            cut_rank_residual -= cut_up[k] + cut_down[k]
        assert cut_rank_residual == 0

        internal_rank_residual = F(0)
        if k > 1:
            internal_rank_residual += internal_up[k - 1] + creation[k - 1]
        if k < N:
            internal_rank_residual += internal_down[k + 1] - destruction[k + 1]
            internal_rank_residual -= internal_up[k] + internal_down[k]
        internal_rank_residual -= F(1, 2) * rho if k == N else F(0)
        assert internal_rank_residual == 0

        square_rank_residual = stationary_square / N if k == 1 else F(0)
        if k > 1:
            square_rank_residual += (
                mass_square_up[k - 1]
                + mass_square_creation[k - 1]
            )
        if k < N:
            square_rank_residual += (
                mass_square_down[k + 1]
                - mass_square_destruction[k + 1]
                - mass_square_up[k]
                - mass_square_down[k]
            )
        square_rank_residual -= rho if k == N else F(0)
        assert square_rank_residual == 0

        variance_rank_residual = (
            (1 - stationary_square) / N if k == 1 else F(0)
        )
        if k > 1:
            variance_rank_residual += (
                variance_up[k - 1] + variance_response_up[k - 1]
            )
        if k < N:
            variance_rank_residual += (
                variance_down[k + 1]
                + variance_response_down[k + 1]
                - variance_up[k]
                - variance_down[k]
            )
        assert variance_rank_residual == 0

        product_rank_residual = F(0)
        if k > 1:
            product_rank_residual += (
                product_internal_up[k - 1] + product_creation[k - 1]
            )
        if k < N:
            product_rank_residual += (
                product_internal_down[k + 1]
                - product_destruction[k + 1]
                - product_internal_up[k]
                - product_internal_down[k]
            )
        product_rank_residual -= (
            rho * (1 - stationary_square) / 2 if k == N else F(0)
        )
        assert product_rank_residual == 0

    # Summing the stationary target/request covariance matrix over one rank
    # preserves positive semidefiniteness.  Its determinant is precisely the
    # sharp rankwise Schur inequality C_k^2 <= V_k D_k.  The final check is
    # its equivalent tangent form for a deliberately nonconstant sequence.
    schur_profile = [F((k + 2) * (2 * k + 1), 3 * k + 7) for k in range(N + 1)]
    for k in range(1, N):
        assert variance_occupation[k] >= 0
        assert prediction_error_occupation[k] >= 0
        assert (
            variance_occupation[k] * prediction_error_occupation[k]
            - cut_occupation[k] ** 2
            >= 0
        )
        theta = schur_profile[k]
        assert (
            prediction_error_occupation[k]
            - 2 * theta * cut_occupation[k]
            + theta ** 2 * variance_occupation[k]
            >= 0
        )
        alpha = F(N - 1, N)
        assert (
            alpha * creation[k] - product_creation[k]
        ) ** 2 <= (
            alpha ** 2 * mass_creation[k] * complete_schur_occupation[k]
        )
        assert (
            alpha * destruction[k]
            - product_destruction[k]
            - stationary_mark_destruction[k]
        ) ** 2 <= (
            alpha ** 2 * mass_destruction[k] * complete_schur_occupation[k]
        )

    kappa = F(
        2 * ((N - 3) * 2 ** N + 4),
        (3 * N - 7) * 2 ** N + 8,
    )
    total_cut = sum(cut_occupation)
    total_gain = sum(gain_up) + sum(gain_down)
    assert sum(creation) - sum(destruction) == rho / 2
    assert (
        sum(mass_square_creation) - sum(mass_square_destruction)
        == rho - stationary_square / N
    )
    assert (
        sum(product_creation) - sum(product_destruction)
        == rho * (1 - stationary_square) / 2
    )
    assert (
        total_gain <= kappa * total_cut
    ) == (
        (2 - kappa) * total_cut
        <= d_zero_integral + nonlinear_remainder_integral
    )

    # Gauge away the diagonal of K_0 with the available one-mark fields.
    # The resulting pure-pair statistic is -2 times the internal flow of
    # two independent requests from a common stationary target.
    collision_conductance = [
        [
            sum(PI[v] * P[v][i] * P[v][j] for v in range(N))
            for j in range(N)
        ]
        for i in range(N)
    ]
    assert all(
        collision_conductance[i][j] == collision_conductance[j][i]
        for i in range(N) for j in range(N)
    )
    collision_degree = [
        sum(collision_conductance[i][j] for j in range(N) if j != i)
        for i in range(N)
    ]
    assert all(
        collision_degree[i]
        == PI[i] * (1 - p_squared[i][i])
        for i in range(N)
    )
    collision_internal_values = [
        sum(
            collision_conductance[i][j]
            for i in range(N) for j in range(i + 1, N)
            if bit(state, i) and bit(state, j)
        )
        for state in range(FULL + 1)
    ]
    collision_mass_values = [
        sum(collision_degree[i] for i in range(N) if bit(state, i))
        for state in range(FULL + 1)
    ]
    assert collision_internal_values[0] == 0
    assert all(
        collision_internal_values[1 << vertex] == 0
        for vertex in range(N)
    )
    assert collision_internal_values[FULL] == (1 - chi) / 2
    assert all(
        r_zero_values[state]
        == collision_mass_values[state]
        - 2 * collision_internal_values[state]
        for state in range(FULL + 1)
    )

    collision_internal_up = [F(0) for _ in range(N + 1)]
    collision_internal_down = [F(0) for _ in range(N + 1)]
    collision_creation = [F(0) for _ in range(N + 1)]
    collision_destruction = [F(0) for _ in range(N + 1)]
    for state in transient:
        k = state.bit_count()
        s = indicator(state)
        p2s = [
            sum(p_squared[i][j] * s[j] for j in range(N))
            for i in range(N)
        ]
        up = F(0)
        down = F(0)
        p_two = F(0)
        n_two = F(0)
        for vertex in range(N):
            x = x_value(state, vertex)
            if bit(state, vertex):
                rate = (1 - x) / (1 + x)
                lower_internal = PI[vertex] * (
                    p2s[vertex] - p_squared[vertex][vertex]
                )
                assert lower_internal >= 0
                target = state ^ (1 << vertex)
                assert (
                    collision_internal_values[target]
                    - collision_internal_values[state]
                    == -lower_internal
                )
                down += rate
                n_two += rate * lower_internal
            else:
                rate = 2 * x / (1 + x)
                upper_increment = PI[vertex] * p2s[vertex]
                assert upper_increment >= 0
                target = state ^ (1 << vertex)
                assert (
                    collision_internal_values[target]
                    - collision_internal_values[state]
                    == upper_increment
                )
                up += rate
                p_two += rate * upper_increment

        assert (
            generator(state, collision_internal_values)
            == p_two - n_two
        )
        weight = mu[state]
        collision_internal_up[k] += (
            weight * collision_internal_values[state] * up
        )
        collision_internal_down[k] += (
            weight * collision_internal_values[state] * down
        )
        collision_creation[k] += weight * p_two
        collision_destruction[k] += weight * n_two

    # This is the second component of the combined rank-H/rank-K_0
    # storage recurrence, including its exact upper boundary flux.
    for k in range(1, N + 1):
        residual = F(0)
        if k > 1:
            residual += (
                collision_internal_up[k - 1]
                + collision_creation[k - 1]
            )
        if k < N:
            residual += (
                collision_internal_down[k + 1]
                - collision_destruction[k + 1]
                - collision_internal_up[k]
                - collision_internal_down[k]
            )
        residual -= rho * (1 - chi) / 2 if k == N else F(0)
        assert residual == 0

    first_net = sum(creation) - sum(destruction)
    second_net = sum(collision_creation) - sum(collision_destruction)
    assert first_net == rho / 2
    assert second_net == rho * (1 - chi) / 2
    complete_ratio = F(N - 2, N - 1)
    row_variance = sum(
        PI[v] * sum(
            (P[v][i] - F(1, N - 1)) ** 2
            for i in range(N) if i != v
        )
        for v in range(N)
    )
    assert chi - F(1, N - 1) == row_variance >= 0
    assert complete_ratio * first_net - second_net == rho * row_variance / 2

    # K(theta)=L_pi+theta K_0 is the Laplacian of the effective
    # conductances c_ij+theta*q_ij when theta is nonnegative.  Verify the
    # corresponding cut/internal-flow identity for a nontrivial rational
    # theta; the analytic note proves the all-kernel spectral PSD range.
    theta = F(7, 5)
    for state in range(FULL + 1):
        effective_internal = (
            internal_values[state]
            + theta * collision_internal_values[state]
        )
        effective_mass = mass(state) + theta * collision_mass_values[state]
        effective_cut = cut_values[state] + theta * r_zero_values[state]
        assert effective_cut == effective_mass - 2 * effective_internal
        assert effective_internal >= 0
        assert effective_cut >= 0

    # The genuinely new combined direction is the boundary-neutral,
    # traceless collision excess.  A fixed PSD contraction cannot isolate
    # it: every nonzero symmetric trace-zero matrix is indefinite.
    k_perp = [
        [
            k_zero[i][j] - (1 - chi) * laplacian[i][j]
            for j in range(N)
        ]
        for i in range(N)
    ]
    assert all(sum(row) == 0 for row in k_perp)
    assert sum(k_perp[i][i] for i in range(N)) == 0
    positive_vector = [F(1), F(0), F(-1), F(0)]
    negative_vector = [F(1), F(-1), F(0), F(0)]

    def form(matrix: list[list[F]], vector: list[F]) -> F:
        return sum(
            vector[i] * matrix[i][j] * vector[j]
            for i in range(N) for j in range(N)
        )

    assert form(k_perp, positive_vector) == F(19, 105) > 0
    assert form(k_perp, negative_vector) == -F(23, 525) < 0

    # K_perp=L_pi(P+chi I), together with its exact centered
    # difference-of-squares identity and sharp Loewner cone.
    factorized = [
        [
            sum(
                laplacian[i][u]
                * (P[u][j] + (chi if u == j else F(0)))
                for u in range(N)
            )
            for j in range(N)
        ]
        for i in range(N)
    ]
    assert factorized == k_perp
    center = (1 - chi) / 2
    radius = (1 + chi) / 2
    for vector in (
        positive_vector,
        negative_vector,
        [F(2), F(-1), F(3), F(-4)],
    ):
        p_vector = [
            sum(P[i][j] * vector[j] for j in range(N))
            for i in range(N)
        ]
        centered_square = sum(
            PI[i] * (p_vector[i] - center * vector[i]) ** 2
            for i in range(N)
        )
        norm = sum(PI[i] * vector[i] ** 2 for i in range(N))
        assert form(k_perp, vector) == radius ** 2 * norm - centered_square
        l_energy = form(laplacian, vector)
        assert -(1 - chi) * l_energy <= form(k_perp, vector)
        assert form(k_perp, vector) <= (1 + chi) * l_energy

    excess_values = [
        collision_internal_values[state]
        - (1 - chi) * internal_values[state]
        for state in range(FULL + 1)
    ]
    assert excess_values[0] == excess_values[FULL] == 0
    assert all(excess_values[1 << vertex] == 0 for vertex in range(N))
    for state in range(FULL + 1):
        s = indicator(state)
        pure_pair = (
            quadratic(k_perp, s)
            - sum(k_perp[i][i] * s[i] for i in range(N))
        )
        assert pure_pair == -2 * excess_values[state]

    collision_defect = [
        [
            p_squared[i][j]
            - (p_squared[i][i] if i == j else F(0))
            - (1 - p_squared[i][i]) * P[i][j]
            for j in range(N)
        ]
        for i in range(N)
    ]
    assert all(sum(row) == 0 for row in collision_defect)
    for state in transient:
        s = indicator(state)
        drift, _ = drift_activity(state)
        x = [x_value(state, i) for i in range(N)]
        y = [
            sum(p_squared[i][j] * s[j] for j in range(N))
            for i in range(N)
        ]
        defect = [
            y[i] - p_squared[i][i] * s[i] - (1 - chi) * x[i]
            for i in range(N)
        ]
        decomposed = [
            (chi - p_squared[i][i]) * x[i]
            + sum(collision_defect[i][j] * s[j] for j in range(N))
            for i in range(N)
        ]
        assert defect == decomposed
        assert generator(state, excess_values) == sum(
            PI[i] * drift[i] * defect[i] for i in range(N)
        )

    # Its rank recurrence has no source at either boundary.  This is the
    # exact rankwise Schur mode which can redistribute first-channel debt
    # without changing fixation flux or the singleton objective.
    excess_up = [
        collision_internal_up[k] - (1 - chi) * internal_up[k]
        for k in range(N + 1)
    ]
    excess_down = [
        collision_internal_down[k] - (1 - chi) * internal_down[k]
        for k in range(N + 1)
    ]
    excess_creation = [
        collision_creation[k] - (1 - chi) * creation[k]
        for k in range(N + 1)
    ]
    excess_destruction = [
        collision_destruction[k] - (1 - chi) * destruction[k]
        for k in range(N + 1)
    ]
    for k in range(1, N + 1):
        residual = F(0)
        if k > 1:
            residual += excess_up[k - 1] + excess_creation[k - 1]
        if k < N:
            residual += (
                excess_down[k + 1]
                - excess_destruction[k + 1]
                - excess_up[k]
                - excess_down[k]
            )
        assert residual == 0
    assert sum(excess_creation) - sum(excess_destruction) == 0


def main() -> None:
    verify_storage_identities()
    rho = verify_dual_and_rank_recurrences()
    verify_geometric_green_bridge()
    verify_fixed_matrix_contractions()
    print("all exact rank-pair/conductance checks passed")
    print("test-graph fixation numerator", rho.numerator)
    print("test-graph fixation denominator", rho.denominator)


if __name__ == "__main__":
    main()
