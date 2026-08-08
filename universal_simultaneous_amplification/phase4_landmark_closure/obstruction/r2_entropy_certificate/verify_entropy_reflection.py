#!/usr/bin/env python3
"""Exact verifier for ENTROPY_REFLECTION_REDUCTION.md.

The Markov-chain calculations use Fraction arithmetic.  Entropies of rational
laws are stored as rational linear combinations of log(prime); equality and
strict signs then reduce to exact integer arithmetic.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import comb, lcm


LogForm = dict[int, F]


def inverse(matrix: list[list[F]]) -> list[list[F]]:
    n = len(matrix)
    aug = [row[:] + [F(int(i == j)) for j in range(n)]
           for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            scale = aug[row][col]
            if scale:
                aug[row] = [x - scale * y
                            for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def union_law(row: list[F]) -> dict[int, F]:
    """Law of the union of a fair-geometric number of row samples."""
    support = [i for i, x in enumerate(row) if x]
    values = [F(0) for _ in range(1 << len(support))]
    for mask in range(1, 1 << len(support)):
        mass = sum(row[support[j]] for j in range(len(support))
                   if mask >> j & 1)
        values[mask] = mass / (2 - mass)
    for j in range(len(support)):
        for mask in range(1 << len(support)):
            if mask >> j & 1:
                values[mask] -= values[mask ^ (1 << j)]
    answer = {}
    for mask in range(1, 1 << len(support)):
        actual = sum(1 << support[j] for j in range(len(support))
                     if mask >> j & 1)
        if values[mask]:
            answer[actual] = values[mask]
    assert sum(answer.values()) == 1
    assert all(x > 0 for x in answer.values())
    return answer


def solve(weights: list[list[int]]):
    n = len(weights)
    assert all(weights[i][i] == 0 for i in range(n))
    assert all(weights[i][j] == weights[j][i]
               for i in range(n) for j in range(n))
    P = [[F(weights[i][j], sum(weights[i])) for j in range(n)]
         for i in range(n)]
    states = list(range(1, (1 << n) - 1))
    index = {state: pos for pos, state in enumerate(states)}
    laws = [union_law(P[v]) for v in range(n)]
    kernels = []
    average = [[F(0) for _ in states] for _ in states]
    for v in range(n):
        kernel = [[F(0) for _ in states] for _ in states]
        for A in states:
            ia = index[A]
            if not (A >> v) & 1:
                kernel[ia][ia] = F(1)
            else:
                for U, probability in laws[v].items():
                    B = (A & ~(1 << v)) | U
                    kernel[ia][index[B]] += probability
            assert sum(kernel[ia]) == 1
        kernels.append(kernel)
        for i in range(len(states)):
            for j in range(len(states)):
                average[i][j] += kernel[i][j] / n

    size = len(states)
    matrix = [[average[j][i] - F(int(i == j)) for j in range(size)]
              for i in range(size)]
    matrix[-1] = [F(1) for _ in range(size)]
    rhs = [F(0) for _ in range(size)]
    rhs[-1] = F(1)
    inv = inverse(matrix)
    pi = [sum(inv[i][j] * rhs[j] for j in range(size))
          for i in range(size)]
    assert sum(pi) == 1
    assert all(x > 0 for x in pi)
    for j in range(size):
        assert sum(pi[i] * average[i][j] for i in range(size)) == pi[j]
    return P, states, index, kernels, pi


def factor_integer(value: int) -> dict[int, int]:
    assert value >= 1
    answer: dict[int, int] = {}
    prime = 2
    while prime * prime <= value:
        while value % prime == 0:
            answer[prime] = answer.get(prime, 0) + 1
            value //= prime
        prime += 1
    if value > 1:
        answer[value] = answer.get(value, 0) + 1
    return answer


def clean(form: LogForm) -> LogForm:
    return {prime: coefficient for prime, coefficient in form.items()
            if coefficient}


def add_log(form: LogForm, coefficient: F, argument: F) -> None:
    """Add coefficient*log(argument) to a prime-log normal form."""
    assert argument > 0
    for value, sign in ((argument.numerator, 1),
                        (argument.denominator, -1)):
        for prime, exponent in factor_integer(value).items():
            form[prime] = form.get(prime, F(0)) \
                + coefficient * sign * exponent


def plus(left: LogForm, right: LogForm) -> LogForm:
    answer = left.copy()
    for prime, coefficient in right.items():
        answer[prime] = answer.get(prime, F(0)) + coefficient
    return clean(answer)


def minus(left: LogForm, right: LogForm) -> LogForm:
    return plus(left, {prime: -coefficient
                       for prime, coefficient in right.items()})


def scale(coefficient: F, form: LogForm) -> LogForm:
    return clean({prime: coefficient * value
                  for prime, value in form.items()})


def entropy(probabilities) -> LogForm:
    answer: LogForm = {}
    for probability in probabilities:
        if probability:
            add_log(answer, -probability, probability)
    return clean(answer)


def binary_entropy(probability: F) -> LogForm:
    return entropy((probability, 1 - probability))


def form_sign(form: LogForm) -> int:
    """Return the exact sign of a rational prime-log form."""
    form = clean(form)
    if not form:
        return 0
    denominator = 1
    for coefficient in form.values():
        denominator = lcm(denominator, coefficient.denominator)
    exponents = {prime: int(coefficient * denominator)
                 for prime, coefficient in form.items()}
    numerator = 1
    divisor = 1
    for prime, exponent in exponents.items():
        if exponent > 0:
            numerator *= prime ** exponent
        elif exponent < 0:
            divisor *= prime ** (-exponent)
    return (numerator > divisor) - (numerator < divisor)


def experiment(weights: list[list[int]]):
    P, states, index, kernels, pi = solve(weights)
    n = len(P)
    pi_map = {A: pi[index[A]] for A in states}
    mu = [[sum(pi[a] * kernels[v][a][b] for a in range(len(states)))
           for b in range(len(states))] for v in range(n)]

    # Exact stationarity, target exclusion, and effective posterior identity.
    for b, B in enumerate(states):
        assert sum(mu[v][b] for v in range(n)) / n == pi[b]
        for v in range(n):
            if (B >> v) & 1:
                assert mu[v][b] == 0
        effective = sum(mu[v][b] - pi[b]
                        for v in range(n) if not (B >> v) & 1)
        assert effective == B.bit_count() * pi[b]

    M: LogForm = {}
    information: LogForm = {}
    conditional_c_given_bv: LogForm = {}
    reflected: LogForm = {}

    for b, B in enumerate(states):
        probability = pi[b]
        k = B.bit_count()
        h = n - k
        M = plus(M, scale(probability, binary_entropy(F(k, n))))

        posterior = []
        divergence: LogForm = {}
        for v in range(n):
            mass = mu[v][b]
            if mass:
                add_log(information, mass / n, mass / probability)
                tau = mass / (n * probability)
                posterior.append(tau)
                add_log(divergence, tau, tau * h)

                nu = mass - probability
                active_posterior = nu / mass
                conditional_c_given_bv = plus(
                    conditional_c_given_bv,
                    scale(mass / n, binary_entropy(active_posterior)),
                )
        assert sum(posterior) == 1
        state_reflection: LogForm = {}
        add_log(state_reflection, F(k, n), F(h, k))
        state_reflection = minus(state_reflection, divergence)
        reflected = plus(reflected, scale(probability, state_reflection))

    gap = minus(M, information)
    assert gap == reflected

    active_entropy: LogForm = {}
    active_deltas = []
    p_values = []
    for v in range(n):
        p_v = sum(pi_map[A] for A in states if (A >> v) & 1)
        p_values.append(p_v)
        source: dict[int, F] = {}
        output: dict[int, F] = {}
        for b, B in enumerate(states):
            if (B >> v) & 1:
                C = B & ~(1 << v)
                source[C] = source.get(C, F(0)) + pi[b] / p_v
            else:
                nu = mu[v][b] - pi[b]
                if nu:
                    output[B] = nu / p_v
        assert sum(source.values()) == 1
        assert sum(output.values()) == 1
        delta = minus(entropy(output.values()), entropy(source.values()))
        active_deltas.append(delta)
        active_entropy = plus(active_entropy, scale(p_v / n, delta))

    conditional_information = minus(M, conditional_c_given_bv)
    assert gap == plus(conditional_information, active_entropy)
    return {
        "P": P,
        "states": states,
        "pi": pi_map,
        "mu": mu,
        "M": M,
        "information": information,
        "gap": gap,
        "conditional_information": conditional_information,
        "active_entropy": active_entropy,
        "active_deltas": active_deltas,
        "p_values": p_values,
    }


def verify_complete_reflection() -> None:
    # The general complement-pair cancellation in equation (17), represented
    # exactly as a prime-log form for a range of symbolic finite n.
    for n in range(3, 13):
        normalizer = n * (2 ** (n - 1) - 1)
        form: LogForm = {}
        for k in range(1, n):
            h = n - k
            level_mass = F(comb(n, k) * h, normalizer)
            add_log(form, level_mass * F(k, n), F(h, k))
        assert clean(form) == {}

    complete = experiment([[0 if i == j else 1 for j in range(4)]
                           for i in range(4)])
    assert complete["gap"] == {}
    n = 4
    for B in complete["states"]:
        h = n - B.bit_count()
        for v in range(n):
            if not (B >> v) & 1:
                b = complete["states"].index(B)
                assert complete["mu"][v][b] / complete["pi"][B] == F(n, h)

    # Statewise reflection is already negative on a size-three K4 state.
    pointwise: LogForm = {}
    add_log(pointwise, F(3, 4), F(1, 3))
    assert form_sign(pointwise) < 0


def verify_active_counterexample() -> None:
    weighted_cycle = [
        [0, 4, 1, 4],
        [4, 0, 4, 1],
        [1, 4, 0, 4],
        [4, 1, 4, 0],
    ]
    result = experiment(weighted_cycle)
    assert result["p_values"] == [F(168, 395)] * 4

    expected_delta = {
        2: F(79, 168),
        3: F(3, 112),
        5: F(-5, 168),
        7: F(1, 4),
        37: F(-37, 168),
    }
    assert all(delta == expected_delta for delta in result["active_deltas"])
    assert form_sign(expected_delta) < 0
    assert form_sign(result["active_entropy"]) < 0
    assert form_sign(result["conditional_information"]) > 0
    assert form_sign(result["gap"]) > 0


def main() -> None:
    path = experiment([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    assert form_sign(path["gap"]) > 0
    verify_complete_reflection()
    verify_active_counterexample()
    print("PASS: exact stationary posterior and entropy-reflection identities")
    print("PASS: complete-graph cross-level cancellation for 3 <= n <= 12")
    print("PASS: exact negative statewise K4 reflection integrand")
    print("PASS: exact regular weighted-K4 active entropy contraction")
    print("PASS: full weighted-K4 entropy-reflection gap remains positive")
    print("OPEN: universal entropy-reflection inequality M >= I(V;B)")


if __name__ == "__main__":
    main()
