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


def generator(state: int, values: tuple[tuple[Q, Q], ...]) -> tuple[Q, Q]:
    answer = [Q(0), Q(0)]
    for target, rate in rates(state):
        for a in range(2):
            answer[a] += rate * (values[target][a] - values[state][a])
    return tuple(answer)


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
    for state in range(1, FULL):
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

        k_theta = sum(PI[v] * e[v] * e[v] for v in range(N))
        endpoint_zero = (ALPHA * multiplier[0]) ** 2
        endpoint_two = (-ALPHA * multiplier[0] + 2 * multiplier[1]) ** 2
        assert action <= max(endpoint_zero, endpoint_two) * k_theta


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

    for state in transient:
        mu = occupation[state]
        k = state.bit_count()
        up_rate = sum(rate for target, rate in rates(state) if target.bit_count() == k + 1)
        down_rate = sum(rate for target, rate in rates(state) if target.bit_count() == k - 1)
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

    for a in range(2):
        assert sum(pair_plus[k][a] - pair_minus[k][a] for k in range(1, N)) == rho * BOUNDARY_VECTOR[a] / 2
        assert sum(mark_plus[k][a] - mark_minus[k][a] for k in range(1, N)) == BOUNDARY_VECTOR[a] * (rho - Q(1, N))
        centered_total = sum(
            pair_plus[k][a] - mark_plus[k][a] / 2
            - pair_minus[k][a] + mark_minus[k][a] / 2
            for k in range(1, N)
        )
        assert centered_total == BOUNDARY_VECTOR[a] / (2 * N)
    return rho


def verify_complete_equality() -> None:
    complete = tuple(
        tuple(Q(0) if i == v else Q(1, N - 1) for i in range(N))
        for v in range(N)
    )
    pi = tuple(Q(1, N) for _ in range(N))
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
    print(f"exact fixation={rho}")
    print("state identities, endpoint data, rank recurrences, and vector SOC checked")


if __name__ == "__main__":
    main()
