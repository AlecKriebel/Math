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
