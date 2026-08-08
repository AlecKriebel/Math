#!/usr/bin/env python3
"""Exact orbit-lumped audit of the three complete-refresh Hessian sectors."""

from __future__ import annotations

from math import comb

from flint import fmpq as Q, fmpq_mat


def perturbation(n, sector):
    delta = [[Q(0) for _ in range(n)] for _ in range(n)]
    if sector == "anti":
        marked = 3
        for i, j in ((0, 1), (1, 2), (2, 0)):
            delta[i][j] = 1
            delta[j][i] = -1
        norm = Q(6)
    elif sector == "sym":
        marked = 4
        for i, j, sign in ((0, 1, 1), (2, 3, 1), (0, 2, -1), (1, 3, -1)):
            delta[i][j] = delta[j][i] = sign
        norm = Q(8)
    elif sector == "std":
        marked = 2
        N = n - 1
        column = [Q(1), Q(-1)] + [Q(0)] * (n - 2)
        for i in range(n):
            for j in range(n):
                if i != j:
                    delta[i][j] = (column[i] + N * column[j]) / (n * (n - 2))
        # The standard eigenvalue multiplies the squared column-sum norm,
        # which is two for this canonical vector.
        norm = Q(2)
    else:
        raise ValueError(sector)
    assert all(sum(row, Q(0)) == 0 for row in delta)
    return delta, marked, norm


def orbit_keys(n, marked):
    bulk = n - marked
    keys = []
    for target in range(marked):
        for mask in range(1 << marked):
            if mask >> target & 1:
                continue
            for count in range(bulk + 1):
                if mask or count:
                    keys.append((target, mask, count))
    if bulk:
        for mask in range(1 << marked):
            for count in range(bulk):
                if mask or count:
                    keys.append((marked, mask, count))
    return keys


def representative(n, marked, key):
    target_class, mask, count = key
    target = target_class if target_class < marked else marked
    subset = mask
    used = 0
    for vertex in range(marked, n):
        if vertex == target:
            continue
        if used < count:
            subset |= 1 << vertex
            used += 1
    return subset, target


def orbit_key(n, marked, subset, target):
    return (
        target if target < marked else marked,
        subset & ((1 << marked) - 1),
        sum(1 for vertex in range(marked, n) if subset >> vertex & 1),
    )


def orbit_size(n, marked, key):
    target, _, count = key
    bulk = n - marked
    if target < marked:
        return comb(bulk, count)
    return bulk * comb(bulk - 1, count)


def complete_orbit_chain(n, marked):
    keys = orbit_keys(n, marked)
    index = {key: i for i, key in enumerate(keys)}
    N = n - 1
    kernel = fmpq_mat(len(keys), len(keys))
    for source, key in enumerate(keys):
        subset, target = representative(n, marked, key)
        rank = subset.bit_count()
        for sample in range(n):
            if sample != target:
                destination = orbit_key(n, marked, subset | (1 << sample), target)
                kernel[source, index[destination]] += Q(1, 2 * N)
        for new_target in range(n):
            if subset >> new_target & 1:
                retained = subset & ~(1 << new_target)
                for sample in range(n):
                    if sample != new_target:
                        destination = orbit_key(
                            n, marked, retained | (1 << sample), new_target
                        )
                        kernel[source, index[destination]] += Q(1, 2 * rank * N)
        assert sum((kernel[source, j] for j in range(len(keys))), Q(0)) == 1

    denominator = n * N * 2 ** (N - 1)
    stationary = []
    for key in keys:
        subset, _ = representative(n, marked, key)
        stationary.append(Q(orbit_size(n, marked, key) * subset.bit_count(), denominator))
    assert sum(stationary, Q(0)) == 1
    for column in range(len(keys)):
        assert sum(
            (stationary[row] * kernel[row, column] for row in range(len(keys))),
            Q(0),
        ) == stationary[column]
    return keys, index, kernel, stationary


def rank_poisson(n):
    N = n - 1
    kernel = fmpq_mat(N, N)
    rank_law = []
    for rank in range(1, n):
        upward = Q(N - rank, 2 * N)
        downward = Q(rank - 1, 2 * N)
        kernel[rank - 1, rank - 1] = 1 - upward - downward
        if rank < N:
            kernel[rank - 1, rank] = upward
        if rank > 1:
            kernel[rank - 1, rank - 2] = downward
        rank_law.append(Q(comb(N - 1, rank - 1), 2 ** (N - 1)))
    fundamental = fmpq_mat(N, N, [
        int(i == j) for i in range(N) for j in range(N)
    ]) - kernel
    for i in range(N):
        for j in range(N):
            fundamental[i, j] += rank_law[j]
    c0 = Q(2**N - 1, N * 2 ** (N - 1))
    forcing = fmpq_mat(N, 1, [Q(1, rank) - c0 for rank in range(1, n)])
    solution = fundamental.solve(forcing)
    return [solution[i, 0] for i in range(N)]


def delta_apply(n, marked, delta, keys, index, function):
    output = []
    for key in keys:
        subset, target = representative(n, marked, key)
        rank = subset.bit_count()
        value = Q(0)
        for sample in range(n):
            if delta[target][sample]:
                destination = orbit_key(
                    n, marked, subset | (1 << sample), target
                )
                value += delta[target][sample] * function[index[destination]] / 2
        for new_target in range(n):
            if subset >> new_target & 1:
                retained = subset & ~(1 << new_target)
                for sample in range(n):
                    if delta[new_target][sample]:
                        destination = orbit_key(
                            n, marked, retained | (1 << sample), new_target
                        )
                        value += (
                            delta[new_target][sample]
                            * function[index[destination]] / (2 * rank)
                        )
        output.append(value)
    return output


def sector_eigenvalue(n, sector):
    delta, marked, normalization = perturbation(n, sector)
    keys, index, kernel, stationary = complete_orbit_chain(n, marked)
    h_rank = rank_poisson(n)
    h = [
        h_rank[representative(n, marked, key)[0].bit_count() - 1]
        for key in keys
    ]
    first = delta_apply(n, marked, delta, keys, index, h)
    assert sum((mass * value for mass, value in zip(stationary, first)), Q(0)) == 0
    fundamental = fmpq_mat(len(keys), len(keys), [
        int(i == j) for i in range(len(keys)) for j in range(len(keys))
    ]) - kernel
    for i in range(len(keys)):
        for j in range(len(keys)):
            fundamental[i, j] += stationary[j]
    response_column = fundamental.solve(fmpq_mat(len(keys), 1, first))
    response = [response_column[i, 0] for i in range(len(keys))]
    second = delta_apply(n, marked, delta, keys, index, response)
    value = sum(
        (mass * entry for mass, entry in zip(stationary, second)), Q(0)
    ) / normalization
    assert value > 0
    return value


def main():
    known = {
        3: (Q(2, 33), None, Q(1, 9)),
        4: (Q(261, 5120), Q(3, 208), Q(57, 640)),
        5: (Q(3434, 85971), Q(359, 26660), Q(143, 2100)),
        6: (Q(2268275, 73893888), Q(176345, 14823936), Q(1435, 27648)),
        7: (Q(117521693, 4968964480), Q(7823511, 760600064), Q(207131, 5174400)),
        8: (Q(141339691089527, 7662417260052480), Q(385860864319, 43668090112000), Q(993349, 31629312)),
        9: (Q(15468663676289, 1058158932994800), Q(5420382036149, 713606969283264), Q(4558321, 181621440)),
        10: (Q(19782952499295763, 1678791062965452800), Q(1843878454004847, 281229006667743232), Q(569294067, 27880652800)),
        11: (Q(6499280769761759945875, 672969901386106928222208), Q(14700724333113143041, 2582641116999109771264), Q(949006649, 56189472768)),
        12: (Q(457580604207195486235493, 56931654195002744021975040), Q(571539495163858763086501, 114919265759376438618144768), Q(12291373259, 866834841600)),
    }
    for n, expected in known.items():
        standard, symmetric, antisymmetric = expected
        assert sector_eigenvalue(n, "std") == standard
        if symmetric is not None:
            assert sector_eigenvalue(n, "sym") == symmetric
        assert sector_eigenvalue(n, "anti") == antisymmetric
    print("PASS: independent exact orbit reduction for all three Hessian sectors, 3<=n<=12")
    print("EXACTLY COMPUTED: every displayed sector value is positive")
    print("OPEN: all-n positivity of the standard and symmetric sectors")


if __name__ == "__main__":
    main()
