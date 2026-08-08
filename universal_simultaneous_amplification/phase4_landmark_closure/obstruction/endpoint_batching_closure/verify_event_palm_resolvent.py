#!/usr/bin/env python3
"""Exact event--Palm/resolvent audit of the C-to-dB batching factor.

All assertions use rational arithmetic.  The verifier constructs the
neutral-event kernels directly, checks the marked burst-resolvent identity,
reconstructs both invariant laws from their directed-tree cofactors, and
certifies that the two natural pieces of the endpoint gap can each have the
wrong sign.  It also independently rebuilds both forward fixation chains
and checks the Palm harmonic-mean formula.
"""

from __future__ import annotations

import hashlib

from flint import fmpq, fmpq_mat


P_NEUTRAL = fmpq(2, 3)
Q_SELECTIVE = fmpq(1, 3)
FITNESS = fmpq(3, 2)


def eye(size: int) -> fmpq_mat:
    matrix = fmpq_mat(size, size)
    for index in range(size):
        matrix[index, index] = 1
    return matrix


def ones(size: int) -> fmpq_mat:
    vector = fmpq_mat(size, 1)
    for index in range(size):
        vector[index, 0] = 1
    return vector


def row_kernel_check(kernel: fmpq_mat) -> None:
    assert kernel.nrows() == kernel.ncols()
    for row in range(kernel.nrows()):
        assert sum(kernel[row, column] for column in range(kernel.ncols())) == 1
        assert all(kernel[row, column] >= 0 for column in range(kernel.ncols()))


def normalized_kernel(weights):
    degrees = tuple(sum(row) for row in weights)
    assert all(degree > 0 for degree in degrees)
    return tuple(
        tuple(fmpq(value, degree) for value in row)
        for row, degree in zip(weights, degrees)
    )


def event_operators(weights):
    """Build the unmarked and target-marked event operators over QQ.

    ``J`` chooses a uniform occupied target, ``H`` forgets the target,
    ``S`` performs one locked selective add, and ``N`` performs the final
    neutral replacement.  Matrices act on row distributions from the left.
    """
    n = len(weights)
    kernel = normalized_kernel(weights)
    masks = tuple(range(1, 1 << n))
    index = {mask: row for row, mask in enumerate(masks)}
    marks = tuple(
        (mask, target)
        for mask in masks
        for target in range(n)
        if mask & (1 << target)
    )
    marked_index = {marked: row for row, marked in enumerate(marks)}

    choose = fmpq_mat(len(masks), len(marks))
    forget = fmpq_mat(len(marks), len(masks))
    selective = fmpq_mat(len(marks), len(marks))
    neutral = fmpq_mat(len(marks), len(masks))

    for mask in masks:
        reciprocal = fmpq(1, mask.bit_count())
        for target in range(n):
            if mask & (1 << target):
                choose[index[mask], marked_index[mask, target]] = reciprocal

    for mask, target in marks:
        row = marked_index[mask, target]
        forget[row, index[mask]] = 1
        for source, probability in enumerate(kernel[target]):
            if not probability:
                continue
            added = mask | (1 << source)
            replaced = (mask & ~(1 << target)) | (1 << source)
            selective[row, marked_index[added, target]] += probability
            neutral[row, index[replaced]] += probability

    assert choose * forget == eye(len(masks))
    for matrix in (selective,):
        for row in range(matrix.nrows()):
            assert sum(matrix[row, column] for column in range(matrix.ncols())) == 1
    for row in range(neutral.nrows()):
        assert sum(neutral[row, column] for column in range(neutral.ncols())) == 1

    return masks, index, choose, forget, selective, neutral


def event_kernels(weights):
    """Return C-pre, C-post, and locked-D neutral-event kernels.

    C is sampled immediately before neutral arrows, so its epoch kernel is
    ``N_C R_C``.  The post-neutral kernel is ``R_C N_C``.  D locks one target
    for the full geometric batch, giving ``p J (I-qS)^(-1) N``.
    """
    masks, index, choose, forget, selective, neutral = event_operators(weights)
    unmarked_selective = choose * selective * forget
    unmarked_neutral = choose * neutral
    c_resolvent = P_NEUTRAL * (
        eye(len(masks)) - Q_SELECTIVE * unmarked_selective
    ).inv()
    c_pre = unmarked_neutral * c_resolvent
    c_post = c_resolvent * unmarked_neutral

    locked_matrix = eye(selective.nrows()) - Q_SELECTIVE * selective
    locked_to_unmarked = locked_matrix.solve(neutral)
    d_kernel = P_NEUTRAL * choose * locked_to_unmarked

    for kernel in (c_pre, c_post, d_kernel):
        row_kernel_check(kernel)
    return {
        "masks": masks,
        "index": index,
        "J": choose,
        "H": forget,
        "S": selective,
        "N": neutral,
        "R_C": c_resolvent,
        "K_C": c_pre,
        "K_R": c_post,
        "K_D": d_kernel,
    }


def stationary(kernel: fmpq_mat) -> fmpq_mat:
    size = kernel.nrows()
    system = eye(size) - kernel.transpose()
    rhs = fmpq_mat(size, 1)
    for column in range(size):
        system[size - 1, column] = 1
    rhs[size - 1, 0] = 1
    invariant = system.solve(rhs)
    assert kernel.transpose() * invariant == invariant
    assert sum(invariant[row, 0] for row in range(size)) == 1
    # The post-neutral kernels never end at the full set: the final neutral
    # replacement removes its locked target.  Their invariant laws therefore
    # have exactly zero mass there, while the C pre-neutral law is positive.
    assert all(invariant[row, 0] >= 0 for row in range(size))
    return invariant


def dot(left: fmpq_mat, right: fmpq_mat):
    return (left.transpose() * right)[0, 0]


def complete_ratio(n: int):
    two_thirds = fmpq(2, 3)
    return (
        fmpq(n - 1, n)
        * (1 - two_thirds**n)
        / (1 - two_thirds ** (n - 1))
    )


def forward_fixation(weights, rule: str):
    """Independent exact forward-chain reconstruction from the update rule."""
    n = len(weights)
    kernel = normalized_kernel(weights)
    full = (1 << n) - 1
    states = tuple(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    matrix = fmpq_mat(len(states), len(states))
    rhs = fmpq_mat(len(states), 1)
    for state in states:
        row = index[state]
        total = fmpq(0)
        for target in range(n):
            mutant_mass = sum(
                kernel[target][source]
                for source in range(n)
                if state & (1 << source)
            )
            if state & (1 << target):
                numerator = 1 - mutant_mass
                new_state = state & ~(1 << target)
            else:
                numerator = FITNESS * mutant_mass
                new_state = state | (1 << target)
            if rule == "C":
                rate = numerator
            elif rule == "dB":
                rate = numerator / (1 + mutant_mass / 2)
            else:
                raise ValueError(rule)
            if not rate:
                continue
            total += rate
            if new_state == full:
                rhs[row, 0] += rate
            elif new_state:
                matrix[row, index[new_state]] -= rate
        matrix[row, row] += total
    values = matrix.solve(rhs)
    return sum(values[index[1 << vertex], 0] for vertex in range(n)) / n


def rational_hash(value) -> str:
    payload = f"{value.p}/{value.q}".encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def principal_minor(matrix: fmpq_mat, omitted: int) -> fmpq_mat:
    size = matrix.nrows()
    minor = fmpq_mat(size - 1, size - 1)
    for row in range(size):
        if row == omitted:
            continue
        reduced_row = row - int(row > omitted)
        for column in range(size):
            if column == omitted:
                continue
            reduced_column = column - int(column > omitted)
            minor[reduced_row, reduced_column] = matrix[row, column]
    return minor


def recurrent_tree_law(kernel: fmpq_mat, masks, full: int):
    """Cofactor/root law on the recurrent nonfull event state space."""
    keep = tuple(row for row, mask in enumerate(masks) if mask != full)
    restricted = fmpq_mat(len(keep), len(keep))
    for row, old_row in enumerate(keep):
        for column, old_column in enumerate(keep):
            restricted[row, column] = kernel[old_row, old_column]
    laplacian = eye(len(keep)) - restricted
    tree_weights = tuple(
        principal_minor(laplacian, root).det()
        for root in range(len(keep))
    )
    assert all(weight > 0 for weight in tree_weights)
    normalizer = sum(tree_weights)
    law = tuple(weight / normalizer for weight in tree_weights)
    return keep, tree_weights, normalizer, law


def analyze(weights, factorization_check: bool = True):
    context = event_kernels(weights)
    masks = context["masks"]
    c_pre = context["K_C"]
    c_post = context["K_R"]
    d_kernel = context["K_D"]
    c_invariant = stationary(c_pre)
    d_invariant = stationary(d_kernel)
    beta = context["N"].transpose() * context["J"].transpose() * c_invariant

    assert c_post.transpose() * beta == beta
    assert context["R_C"].transpose() * beta == c_invariant
    assert stationary(c_post) == beta

    reciprocal_size = fmpq_mat(len(masks), 1)
    for row, mask in enumerate(masks):
        reciprocal_size[row, 0] = fmpq(1, mask.bit_count())

    beta_mean = dot(beta, reciprocal_size)
    c_mean = dot(c_invariant, reciprocal_size)
    d_mean = dot(d_invariant, reciprocal_size)
    lam = 1 / complete_ratio(len(weights))

    # K_R Poisson equation, normalized by beta*g=0.
    poisson = eye(len(masks)) - c_post
    for row in range(len(masks)):
        for column in range(len(masks)):
            poisson[row, column] += beta[column, 0]
    centered = reciprocal_size - beta_mean * ones(len(masks))
    potential = poisson.solve(centered)
    assert dot(beta, potential) == 0
    assert (eye(len(masks)) - c_post) * potential == centered

    persistence = dot(d_invariant, (d_kernel - c_post) * potential)
    assert persistence == d_mean - beta_mean
    timing = beta_mean - lam * c_mean
    total = persistence + timing
    assert total == d_mean - lam * c_mean

    # Directed matrix-tree/root likelihood representation on Omega\{V}.
    full = (1 << len(weights)) - 1
    keep_r, trees_r, normalizer_r, law_r = recurrent_tree_law(
        c_post, masks, full
    )
    keep_d, trees_d, normalizer_d, law_d = recurrent_tree_law(
        d_kernel, masks, full
    )
    assert keep_r == keep_d
    for reduced_row, old_row in enumerate(keep_r):
        assert law_r[reduced_row] == beta[old_row, 0]
        assert law_d[reduced_row] == d_invariant[old_row, 0]

    c_coverage = context["R_C"] * reciprocal_size
    coupled_integrand = []
    for reduced_row, old_row in enumerate(keep_r):
        tree_density = (
            trees_d[reduced_row]
            * normalizer_r
            / (trees_r[reduced_row] * normalizer_d)
        )
        assert tree_density * beta[old_row, 0] == d_invariant[old_row, 0]
        value = (
            tree_density * reciprocal_size[old_row, 0]
            - lam * c_coverage[old_row, 0]
        )
        coupled_integrand.append((value, masks[old_row]))
    assert (
        sum(
            beta[context["index"][mask], 0] * value
            for value, mask in coupled_integrand
        )
        == total
    )

    # Exact marked resolvent identity retaining the entire geometric burst.
    if factorization_check:
        choose = context["J"]
        forget = context["H"]
        selective = context["S"]
        neutral = context["N"]
        refresh = forget * choose
        marked_identity = eye(selective.nrows())
        locked = marked_identity - Q_SELECTIVE * selective
        refreshed = marked_identity - Q_SELECTIVE * selective * refresh
        direct_difference = d_kernel - c_post
        factored_difference = (
            P_NEUTRAL
            * Q_SELECTIVE
            * choose
            * locked.inv()
            * selective
            * (marked_identity - refresh)
            * refreshed.inv()
            * neutral
        )
        assert direct_difference == factored_difference

    # Palm harmonic means equal the independently solved fixation values.
    rho_c = forward_fixation(weights, "C")
    rho_d = forward_fixation(weights, "dB")
    assert rho_c == 1 / (len(weights) * c_mean)
    assert rho_d == 1 / (len(weights) * d_mean)
    assert total >= 0
    return (
        persistence,
        timing,
        total,
        rho_c,
        rho_d,
        min(coupled_integrand),
        max(coupled_integrand),
    )


def graph(matrix):
    result = tuple(tuple(int(value) for value in row) for row in matrix)
    assert all(result[i][i] == 0 for i in range(len(result)))
    assert all(result[i][j] == result[j][i] for i in range(len(result)) for j in range(len(result)))
    return result


def main() -> None:
    complete_four = graph(
        [[0 if i == j else 1 for j in range(4)] for i in range(4)]
    )
    complete = analyze(complete_four)
    assert complete[0] == complete[1] == complete[2] == 0
    assert complete[5] == (-fmpq(58, 1365), 0b0111)
    assert complete[6] == (fmpq(47, 1092), 0b1000)
    print("PASS K_4: beta_C=alpha_D and the normalized endpoint gap is zero")
    print("PASS K_4: the cofactor--coverage integrand has both exact signs")

    persistence_witness = graph(
        [
            [0, 2, 0, 3],
            [2, 0, 1, 30],
            [0, 1, 0, 1],
            [3, 30, 1, 0],
        ]
    )
    persistence = analyze(persistence_witness)
    assert persistence[0] < 0 < persistence[1]
    assert persistence[5][0] < 0 < persistence[6][0]
    print(
        "PASS n=4: locked-vs-resampled persistence term is negative;",
        "hash", rational_hash(persistence[0]),
        "total gap", float(persistence[2]),
    )

    timing_witness = graph(
        [
            [0, 0, 5, 5, 11],
            [0, 0, 7, 13, 1],
            [5, 7, 0, 1, 7],
            [5, 13, 1, 0, 2],
            [11, 1, 7, 2, 0],
        ]
    )
    timing = analyze(timing_witness)
    assert timing[1] < 0 < timing[0]
    assert timing[5][0] < 0 < timing[6][0]
    print(
        "PASS n=5: neutral/selective timing term is negative;",
        "hash", rational_hash(timing[1]),
        "total gap", float(timing[2]),
    )
    print("PASS: exact event--Palm/resolvent identity and independent fixation audit")


if __name__ == "__main__":
    main()
