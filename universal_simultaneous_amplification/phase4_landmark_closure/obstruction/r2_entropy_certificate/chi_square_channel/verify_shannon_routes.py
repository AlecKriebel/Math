#!/usr/bin/env python3
"""Exact checks for the algebraic claims in SHANNON_REFLECTION.md."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product

from verify_resolvent_identities import solve


def positive(value: F) -> F:
    return value if value > 0 else F(0)


def channel_data(weights: list[list[int]]):
    P, states, index, kernels, pi = solve(weights)
    n = len(P)
    mus = [
        [sum(pi[a] * kernels[v][a][b] for a in range(len(states)))
         for b in range(len(states))]
        for v in range(n)
    ]
    return P, states, index, kernels, pi, mus


def check_reverse_paths(weights: list[list[int]], max_length: int = 4) -> int:
    P, states, index, kernels, pi, mus = channel_data(weights)
    n = len(P)
    all_size = 1 << n
    pi_all = [F(0) for _ in range(all_size)]
    for A, mass in zip(states, pi):
        pi_all[A] = mass
    checks = 0

    for v in range(n):
        sigma = [F(0) for _ in range(all_size)]
        nu = [F(0) for _ in range(all_size)]
        for C in range(all_size):
            if not (C >> v) & 1:
                sigma[C] = pi_all[C | (1 << v)]
        for b, B in enumerate(states):
            if not (B >> v) & 1:
                nu[B] = mus[v][b] - pi[b]
        lam = [(x + y) / 2 for x, y in zip(sigma, nu)]
        p = sum(sigma)
        assert p == sum(nu) > 0

        # Normalization of the labelled reverse last-sample kernel.
        for B in range(all_size):
            if not nu[B]:
                continue
            total = F(0)
            for C in range(all_size):
                for i in range(n):
                    if B == (C | (1 << i)):
                        total += lam[C] * P[v][i] / nu[B]
            assert total == 1
            checks += 1

        # Exact equality of every positive labelled path through max_length.
        support = [i for i in range(n) if P[v][i]]
        for C0 in range(all_size):
            if not sigma[C0]:
                continue
            for length in range(1, max_length + 1):
                for labels in product(support, repeat=length):
                    path = [C0]
                    for label in labels:
                        path.append(path[-1] | (1 << label))
                    forward = sigma[C0] / p / (2 ** length)
                    for label in labels:
                        forward *= P[v][label]

                    reverse = nu[path[-1]] / p
                    assert reverse > 0
                    for j in range(length, 0, -1):
                        C, B, label = path[j - 1], path[j], labels[j - 1]
                        reverse *= lam[C] * P[v][label] / nu[B]
                        denominator = sigma[C] + nu[C]
                        assert denominator > 0
                        if j == 1:
                            reverse *= sigma[C] / denominator
                        else:
                            reverse *= nu[C] / denominator
                    assert reverse == forward
                    checks += 1
    return checks


def membership_tv(pi: list[F], states: list[int], u: int, v: int) -> F:
    return sum(
        pi[pos] for pos, A in enumerate(states)
        if ((A >> u) & 1) != ((A >> v) & 1)
    )


def output_tv(mus: list[list[F]], u: int, v: int) -> F:
    return sum(abs(x - y) for x, y in zip(mus[u], mus[v])) / 2


def stop_loss_gap(weights: list[list[int]], threshold: F) -> F:
    _, states, _, _, pi, mus = channel_data(weights)
    n = len(weights)
    actual = F(0)
    membership = F(0)
    for b, B in enumerate(states):
        k = B.bit_count()
        h = n - k
        if h == 0:
            continue
        for v in range(n):
            actual += pi[b] / n * positive(mus[v][b] / pi[b] - threshold)
        membership += pi[b] * (
            F(k, n) ** 2 * positive(F(n, k) - threshold)
            + F(h, n) ** 2 * positive(F(n, h) - threshold)
        )
    return membership - actual


def check_membership_second_moment(weights: list[list[int]]) -> None:
    _, states, _, _, pi, _ = channel_data(weights)
    n = len(weights)
    moment = F(0)
    for B, mass in zip(states, pi):
        k = B.bit_count()
        h = n - k
        if h:
            moment += mass * (
                F(k, n) ** 2 * F(n, k) ** 2
                + F(h, n) ** 2 * F(n, h) ** 2
            )
    assert moment == 2


def main() -> None:
    path = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    triangle = [[0, 7, 1], [7, 0, 1], [1, 1, 0]]

    reverse_checks = check_reverse_paths(path) + check_reverse_paths(triangle)
    _, states, _, _, pi, mus = channel_data(path)
    tv_membership = membership_tv(pi, states, 0, 1)
    tv_output = output_tv(mus, 0, 1)
    assert tv_membership == F(7, 9)
    assert tv_output == F(5, 6)
    assert tv_output - tv_membership == F(1, 18)

    convex_gap = stop_loss_gap(triangle, F(3, 2))
    assert convex_gap == -F(8, 327)
    check_membership_second_moment(path)
    check_membership_second_moment(triangle)

    print(f"PASS: {reverse_checks} exact normalized-reverse/path checks")
    print("PASS: path Blackwell obstruction TV expansion = 1/18")
    print("PASS: triangle convex-order stop-loss gap = -8/327")
    print("PASS: exact membership-channel second moment = 2")
    print("OPEN: Shannon entropy reflection M-I(V;B)>=0")


if __name__ == "__main__":
    main()
