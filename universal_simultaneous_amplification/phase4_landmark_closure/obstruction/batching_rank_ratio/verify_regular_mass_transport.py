#!/usr/bin/env python3
"""Exact certificate for the regular-case mass-transport reformulation."""

from __future__ import annotations

import sympy as sp


R = sp.Rational(3, 2)


def popcount(state: int) -> int:
    return bin(state).count("1")


def link_generator(p: sp.Matrix, fitness: sp.Rational) -> tuple[list[int], dict[int, int], sp.Matrix]:
    n = p.rows
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    generator = sp.zeros(len(states), len(states))
    for state in states:
        row = index[state]
        for target in range(n):
            q = sum(
                p[target, source]
                for source in range(n)
                if (state >> source) & 1
            )
            if (state >> target) & 1:
                rate = 1 - q
                new_state = state & ~(1 << target)
            else:
                rate = fitness * q
                new_state = state | (1 << target)
            generator[row, row] -= rate
            if new_state not in (0, full):
                generator[row, index[new_state]] += rate
    return states, index, generator


def state_statistic(p: sp.Matrix, state: int, kind: str) -> sp.Expr:
    n = p.rows
    indicator = sp.Matrix([(state >> vertex) & 1 for vertex in range(n)])
    q = p * indicator
    if kind == "internal":
        return sp.cancel((indicator.T * p * indicator)[0])
    if kind == "E":
        return sp.cancel((indicator.T * (p * p - p) * indicator)[0])
    if kind == "B":
        return sp.cancel(
            sum(q[v] ** 2 for v in range(n) if not ((state >> v) & 1))
        )
    raise ValueError(kind)


def occupation(
    p: sp.Matrix, initial_states: list[int], fitness: sp.Rational = R
) -> tuple[list[int], dict[int, int], sp.Matrix, sp.Matrix]:
    states, index, generator = link_generator(p, fitness)
    initial = sp.zeros(1, len(states))
    for state in initial_states:
        initial[0, index[state]] += 1
    measure = initial * (-generator).inv()
    return states, index, generator, measure


def forward_log_derivative(p: sp.Matrix) -> sp.Expr:
    """Differentiate the exact absorbing equations for q_s at s=0."""
    n = p.rows
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    matrix = sp.zeros(len(states), len(states))
    matrix_prime = sp.zeros(len(states), len(states))
    rhs = sp.zeros(len(states), 1)
    rhs_prime = sp.zeros(len(states), 1)
    for state in states:
        row = index[state]
        for target in range(n):
            q = sum(
                p[target, source]
                for source in range(n)
                if (state >> source) & 1
            )
            if (state >> target) & 1:
                base = 1 - q
                new_state = state & ~(1 << target)
            else:
                base = R * q
                new_state = state | (1 << target)
            rate = base
            rate_prime = -(R - 1) * q * base
            matrix[row, row] += rate
            matrix_prime[row, row] += rate_prime
            if new_state == full:
                rhs[row] += rate
                rhs_prime[row] += rate_prime
            elif new_state:
                matrix[row, index[new_state]] -= rate
                matrix_prime[row, index[new_state]] -= rate_prime
    values = matrix.inv() * rhs
    derivative = matrix.inv() * (rhs_prime - matrix_prime * values)
    rho = sum(values[index[1 << x]] for x in range(n)) / n
    rho_prime = sum(derivative[index[1 << x]] for x in range(n)) / n
    return sp.cancel(rho_prime / rho)


def verify_kernel(p: sp.Matrix, expected_t: sp.Rational) -> None:
    n = p.rows
    full = (1 << n) - 1
    assert p == p.T
    assert all(sum(p.row(v)) == 1 for v in range(n))
    states, index, generator, co_occupation = occupation(
        p, [full ^ (1 << x) for x in range(n)]
    )

    e_vector = sp.Matrix([state_statistic(p, state, "E") for state in states])
    b_vector = sp.Matrix([state_statistic(p, state, "B") for state in states])
    i_vector = sp.Matrix(
        [state_statistic(p, state, "internal") for state in states]
    )
    t_value = sp.cancel((co_occupation * e_vector)[0])
    b_occupation = sp.cancel((co_occupation * b_vector)[0])
    assert t_value == expected_t

    # Q_1 I = 2 E on every transient state: E is a neutral-flow divergence.
    _, _, neutral_generator = link_generator(p, sp.Integer(1))
    neutral_action = neutral_generator * i_vector
    # Absorbing full-state jumps contribute I(V)=n to Q_1 I.
    for state in states:
        row = index[state]
        for target in range(n):
            if (state >> target) & 1:
                continue
            q = sum(
                p[target, source]
                for source in range(n)
                if (state >> source) & 1
            )
            if (state | (1 << target)) == full:
                neutral_action[row] += q * n
    assert neutral_action == 2 * e_vector

    # The harmonic Doob transform z(A)=r^(-|A|), followed by complement,
    # turns singleton occupation with weight r^{-(|A|-1)} into co-singleton
    # occupation without a weight.
    _, _, _, singleton_occupation = occupation(p, [1 << x for x in range(n)])
    weighted_e = sp.Matrix(
        [R ** (1 - popcount(state)) * e_vector[index[state]] for state in states]
    )
    assert sp.cancel((singleton_occupation * weighted_e)[0] - t_value) == 0

    # Dynkin's formula for I under Q_r:
    # T = n/2 [n phi_{n-1}-(n-2)] - (r-1) int B.
    phi = sp.cancel((1 - R ** (-(n - 1))) / (1 - R ** (-n)))
    universal_term = sp.cancel(
        sp.Rational(n, 2) * (n * phi - (n - 2))
    )
    assert sp.cancel(
        t_value - universal_term + (R - 1) * b_occupation
    ) == 0

    # This occupation statistic gives the exact normalized derivative.
    assert sp.cancel(
        forward_log_derivative(p) + (R - 1) * t_value / n
    ) == 0


def verify_collision_green(p: sp.Matrix, expected_b_occupation: sp.Expr) -> None:
    """Transpose the collision occupation to the reversible C-chain Green kernel."""
    n = p.rows
    full = (1 << n) - 1
    states = list(range(1, full + 1))
    index = {state: row for row, state in enumerate(states)}
    selective = R - 1
    generator = sp.zeros(full, full)
    for state in states:
        row = index[state]
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            for source in range(n):
                probability = p[target, source]
                neutral = (state & ~(1 << target)) | (1 << source)
                branch = state | (1 << source)
                if neutral != state:
                    generator[row, index[neutral]] += probability
                if branch != state:
                    generator[row, index[branch]] += selective * probability
        generator[row, row] = -sum(generator.row(row))

    source_vector = sp.zeros(full, 1)
    for state in states:
        vertices = [v for v in range(n) if (state >> v) & 1]
        if len(vertices) == 1:
            value = 1
        elif len(vertices) == 2:
            i, j = vertices
            probability = p[i, j]
            value = 2 * (probability**2 - 2 * probability) / selective
        elif len(vertices) == 3:
            value = 0
            for target in vertices:
                others = [v for v in vertices if v != target]
                value += (
                    2
                    * p[target, others[0]]
                    * p[target, others[1]]
                    / selective**2
                )
        else:
            value = 0
        source_vector[index[state]] = sp.cancel(value)

    invariant = sp.Matrix(
        [
            selective ** popcount(state) / (R**n - 1)
            for state in states
        ]
    )
    assert sp.cancel((invariant.T * source_vector)[0]) == 0
    for i in range(full):
        for j in range(full):
            assert sp.cancel(
                invariant[i] * generator[i, j]
                - invariant[j] * generator[j, i]
            ) == 0

    # Solve -L g=b using g(V)=0; for this collision source the resulting
    # potential is also pi-centered, hence it is the actual Green integral.
    poisson = -generator.copy()
    rhs = source_vector.copy()
    poisson[-1, :] = sp.zeros(1, full)
    poisson[-1, -1] = 1
    rhs[-1] = 0
    potential = poisson.inv() * rhs
    assert sp.cancel((invariant.T * potential)[0]) == 0
    green_value = sp.cancel(
        sum(potential[index[1 << x]] for x in range(n))
    )
    assert green_value == expected_b_occupation


def verify_all_regular_k4_symbolically() -> None:
    """Prove the exact trace-gap formula on the full K4 stochastic polytope."""
    a, b, fitness = sp.symbols("a b fitness")
    c = 1 - a - b
    p = sp.Matrix(
        [
            [0, a, b, c],
            [a, 0, c, b],
            [b, c, 0, a],
            [c, b, a, 0],
        ]
    )
    # Translation orbits: singleton, the three pair differences, co-singleton.
    representatives = [0b0001, 0b0011, 0b0101, 0b1001, 0b1110]
    pair_orbit = {
        0b0011: 1,
        0b1100: 1,
        0b0101: 2,
        0b1010: 2,
        0b1001: 3,
        0b0110: 3,
    }

    def orbit(state: int) -> int | None:
        if popcount(state) == 1:
            return 0
        if popcount(state) == 2:
            return pair_orbit[state]
        if popcount(state) == 3:
            return 4
        return None

    generator = sp.zeros(5, 5)
    integrand = sp.zeros(5, 1)
    for row, state in enumerate(representatives):
        indicator = sp.Matrix([(state >> v) & 1 for v in range(4)])
        integrand[row] = sp.expand(
            (indicator.T * (p * p - p) * indicator)[0]
        )
        for target in range(4):
            q = sum(
                p[target, source]
                for source in range(4)
                if (state >> source) & 1
            )
            if (state >> target) & 1:
                rate = 1 - q
                new_state = state & ~(1 << target)
            else:
                rate = fitness * q
                new_state = state | (1 << target)
            generator[row, row] -= rate
            new_orbit = orbit(new_state)
            if new_orbit is not None:
                generator[row, new_orbit] += rate
    potential = (-generator).inv() * integrand
    t_value = sp.factor(4 * potential[4])
    complete_value = sp.factor(
        4
        * (fitness**2 + 2 * fitness + 3)
        / (3 * (fitness + 1) * (fitness**2 + 1))
    )
    variance = sum(
        (value - sp.Rational(1, 3)) ** 2 for value in (a, b, c)
    )
    expected = sp.factor(
        complete_value
        + 4
        * fitness
        * (fitness - 1)
        / ((fitness + 1) * (fitness**2 + 1))
        * variance
    )
    assert sp.factor(t_value - expected) == 0
    trace_gap = sp.factor(sp.trace(p * p) - sp.Rational(4, 3))
    assert sp.factor(trace_gap - 4 * variance) == 0


def verify_two_block_k6_boundary() -> None:
    """Check exact positivity on the K3/K3 modular-to-bipartite segment."""
    epsilon = sp.symbols("epsilon")
    module_size = 3
    n = 6
    within = (1 - epsilon) / 2
    across = epsilon / 3
    states = [
        (i, j)
        for i in range(4)
        for j in range(4)
        if (i, j) not in ((0, 0), (3, 3))
    ]
    index = {state: row for row, state in enumerate(states)}
    generator = sp.zeros(len(states), len(states))
    integrand = sp.zeros(len(states), 1)
    for state in states:
        i, j = state
        row = index[state]
        q_a_out = within * i + across * j
        q_a_in = within * (i - 1) + across * j if i else 0
        q_b_out = within * j + across * i
        q_b_in = within * (j - 1) + across * i if j else 0
        transitions = (
            ((i + 1, j), R * (module_size - i) * q_a_out),
            ((i - 1, j), i * (1 - q_a_in)),
            ((i, j + 1), R * (module_size - j) * q_b_out),
            ((i, j - 1), j * (1 - q_b_in)),
        )
        for new_state, rate in transitions:
            if rate == 0:
                continue
            generator[row, row] -= rate
            if new_state not in ((0, 0), (3, 3)):
                generator[row, index[new_state]] += rate
        integrand[row] = sp.expand(
            (module_size - i) * q_a_out**2
            + i * q_a_in**2
            + (module_size - j) * q_b_out**2
            + j * q_b_in**2
            - i * q_a_in
            - j * q_b_in
        )
    potential = (-generator).inv() * integrand
    t_value = sp.factor(
        3 * potential[index[(2, 3)]] + 3 * potential[index[(3, 2)]]
    )
    complete = sp.Rational(5676, 3325)
    difference = sp.factor(t_value - complete)
    expected = (
        2
        * (5 * epsilon - 3) ** 2
        * (
            39 * epsilon**3
            + 2 * epsilon**2
            - 13439 * epsilon
            - 10602
        )
        / (
            3325
            * (epsilon + 1)
            * (13 * epsilon**2 - 149 * epsilon - 114)
        )
    )
    assert sp.factor(difference - expected) == 0
    assert sp.limit(t_value, epsilon, 0) == sp.Rational(42, 19)
    assert t_value.subs(epsilon, 1) == sp.Rational(1212, 665)
    assert t_value.subs(epsilon, sp.Rational(3, 5)) == complete


def verify_second_variation_response() -> None:
    """Certify T''=2 nu (||Delta 1_H||^2-A_Delta u') exactly."""
    p = sp.Matrix(
        [
            [0, sp.Rational(2, 5), sp.Rational(7, 20), sp.Rational(1, 4)],
            [sp.Rational(2, 5), 0, sp.Rational(1, 4), sp.Rational(7, 20)],
            [sp.Rational(7, 20), sp.Rational(1, 4), 0, sp.Rational(2, 5)],
            [sp.Rational(1, 4), sp.Rational(7, 20), sp.Rational(2, 5), 0],
        ]
    )
    delta = sp.Matrix(
        [
            [0, 1, -1, 0],
            [1, 0, 0, -1],
            [-1, 0, 0, 1],
            [0, -1, 1, 0],
        ]
    )
    assert p == p.T and delta == delta.T
    assert p * sp.ones(4, 1) == sp.ones(4, 1)
    assert delta * sp.ones(4, 1) == sp.zeros(4, 1)
    full = 15
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}

    def transient_matrix(kernel: sp.Matrix) -> sp.Matrix:
        generator = sp.zeros(len(states), len(states))
        for state in states:
            row = index[state]
            for target in range(4):
                q = sum(
                    kernel[target, source]
                    for source in range(4)
                    if (state >> source) & 1
                )
                if (state >> target) & 1:
                    rate = 1 - q
                    new_state = state & ~(1 << target)
                else:
                    rate = R * q
                    new_state = state | (1 << target)
                generator[row, row] -= rate
                if new_state not in (0, full):
                    generator[row, index[new_state]] += rate
        return -generator

    def statistic(kernel: sp.Matrix) -> sp.Matrix:
        return sp.Matrix(
            [
                (
                    sp.Matrix([(state >> v) & 1 for v in range(4)]).T
                    * (kernel * kernel - kernel)
                    * sp.Matrix([(state >> v) & 1 for v in range(4)])
                )[0]
                for state in states
            ]
        )

    matrix = transient_matrix(p)
    matrix_delta = transient_matrix(p + delta) - matrix
    value = statistic(p)
    value_prime = sp.Matrix(
        [
            (
                sp.Matrix([(state >> v) & 1 for v in range(4)]).T
                * (p * delta + delta * p - delta)
                * sp.Matrix([(state >> v) & 1 for v in range(4)])
            )[0]
            for state in states
        ]
    )
    square = sp.Matrix(
        [
            (
                sp.Matrix([(state >> v) & 1 for v in range(4)]).T
                * delta**2
                * sp.Matrix([(state >> v) & 1 for v in range(4)])
            )[0]
            for state in states
        ]
    )
    inverse = matrix.inv()
    potential = inverse * value
    response = inverse * (value_prime - matrix_delta * potential)
    initial = sp.zeros(1, len(states))
    for vertex in range(4):
        initial[0, index[full ^ (1 << vertex)]] = 1
    occupation = initial * inverse
    square_term = sp.cancel(2 * (occupation * square)[0])
    response_term = sp.cancel(
        -2 * (occupation * matrix_delta * response)[0]
    )
    second_derivative = sp.cancel(square_term + response_term)
    coefficient = sp.cancel(
        R * (R - 1) / ((R + 1) * (R**2 + 1))
    )
    expected = sp.cancel(2 * coefficient * sp.trace(delta**2))
    assert second_derivative == expected
    assert square_term > 0
    assert response_term < 0
    assert second_derivative > 0


def main() -> None:
    c4 = sp.Matrix(
        [
            [0, sp.Rational(1, 2), 0, sp.Rational(1, 2)],
            [sp.Rational(1, 2), 0, sp.Rational(1, 2), 0],
            [0, sp.Rational(1, 2), 0, sp.Rational(1, 2)],
            [sp.Rational(1, 2), 0, sp.Rational(1, 2), 0],
        ]
    )
    complete = (sp.ones(4, 4) - sp.eye(4)) / 3
    verify_kernel(c4, sp.Rational(92, 65))
    verify_kernel(complete, sp.Rational(88, 65))
    verify_collision_green(c4, sp.Rational(208, 65))
    verify_all_regular_k4_symbolically()
    verify_two_block_k6_boundary()
    verify_second_variation_response()

    # The complete kernel is strictly smaller for this noncomplete regular
    # example, although no general proof of its minimality is asserted.
    assert sp.Rational(92, 65) > sp.Rational(88, 65)
    print("PASS exact regular Doob-transform occupation identity")
    print("PASS exact neutral-flow/Dynkin mass transport")
    print("PASS exact reversible-C collision Green identity")
    print("PASS C4 T=92/65 > T(K4)=88/65")
    print("PASS all regular K4 kernels, symbolic fitness r>1 trace gap")
    print("PASS exact K3/K3 modular boundary factorization")
    print("PASS exact square-plus-response second variation")


if __name__ == "__main__":
    main()
