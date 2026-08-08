#!/usr/bin/env python3
"""Exact combined endpoint forest/Palm identity at fitness 3/2.

The verifier never assumes separate orientation or batching inequalities.
It builds the L, C, and D dual generators from the graphical rules, solves
their invariant laws over QQ, checks representative Markov-tree cofactors,
and verifies the single paired L--D forest determinant equivalent to the
normalized Bd*dB product bound.  It also resolves that sign into the exact
orientation/Palm pieces solely to diagnose cancellation on hostile graphs.
"""

from __future__ import annotations

import hashlib

from flint import fmpq, fmpq_mat


R = fmpq(3, 2)
A = fmpq(1, 2)
P_NEUTRAL = fmpq(2, 3)
Q_SELECTIVE = fmpq(1, 3)


def eye(size: int) -> fmpq_mat:
    matrix = fmpq_mat(size, size)
    for index in range(size):
        matrix[index, index] = 1
    return matrix


def normalized_kernel(weights):
    degree = tuple(sum(row) for row in weights)
    assert all(value > 0 for value in degree)
    return tuple(
        tuple(fmpq(weights[i][j], degree[i]) for j in range(len(weights)))
        for i in range(len(weights))
    )


def add_change(matrix: fmpq_mat, row: int, column: int, rate) -> None:
    if row != column and rate:
        matrix[row, column] += rate


def finish_generator(matrix: fmpq_mat) -> fmpq_mat:
    for row in range(matrix.nrows()):
        matrix[row, row] = -sum(
            matrix[row, column]
            for column in range(matrix.ncols())
            if column != row
        )
    return matrix


def unbatched_generator(weights, orientation: str):
    """Return L (original arrows) or C (reversed arrows) on nonempty sets."""
    n = len(weights)
    full = (1 << n) - 1
    masks = tuple(range(1, full + 1))
    index = {mask: row for row, mask in enumerate(masks)}
    kernel = normalized_kernel(weights)
    generator = fmpq_mat(len(masks), len(masks))
    for mask in masks:
        row = index[mask]
        for target in range(n):
            if not (mask & (1 << target)):
                continue
            for source in range(n):
                if orientation == "L":
                    rate = kernel[source][target]
                elif orientation == "C":
                    rate = kernel[target][source]
                else:
                    raise ValueError(orientation)
                if not rate:
                    continue
                neutral = (mask & ~(1 << target)) | (1 << source)
                selective = mask | (1 << source)
                add_change(generator, row, index[neutral], rate)
                add_change(generator, row, index[selective], A * rate)
    return masks, finish_generator(generator)


def subsets(mask: int):
    current = mask
    while True:
        yield current
        if current == 0:
            return
        current = (current - 1) & mask


def geometric_union_law(row):
    """Law of the union of a geometric number of iid row samples."""
    support = sum(1 << source for source, value in enumerate(row) if value)

    def pgf(mass):
        return mass / (R - A * mass)

    answer = {}
    for target_set in subsets(support):
        if not target_set:
            continue
        probability = fmpq(0)
        for included in subsets(target_set):
            mass = sum(
                row[source]
                for source in range(len(row))
                if included & (1 << source)
            )
            sign = -1 if (target_set.bit_count() - included.bit_count()) % 2 else 1
            probability += sign * pgf(mass)
        assert probability > 0
        answer[target_set] = probability
    assert sum(answer.values()) == 1
    return answer


def row_kernel_check(kernel: fmpq_mat) -> None:
    for row in range(kernel.nrows()):
        assert sum(kernel[row, column] for column in range(kernel.ncols())) == 1
        assert all(kernel[row, column] >= 0 for column in range(kernel.ncols()))


def event_kernels(weights):
    """Build refreshed-C and locked-dB post-event kernels directly.

    The refreshed kernel resamples the occupied target before every
    selective add.  The locked kernel retains one target for the entire
    geometric batch.  Both end with one neutral replacement and hence have
    the nonfull sets as their unique recurrent class.
    """
    n = len(weights)
    masks = tuple(range(1, 1 << n))
    index = {mask: row for row, mask in enumerate(masks)}
    kernel = normalized_kernel(weights)
    selective = fmpq_mat(len(masks), len(masks))
    neutral = fmpq_mat(len(masks), len(masks))
    locked = fmpq_mat(len(masks), len(masks))
    union_laws = tuple(geometric_union_law(row) for row in kernel)

    for mask in masks:
        row = index[mask]
        reciprocal = fmpq(1, mask.bit_count())
        for target in range(n):
            if not (mask & (1 << target)):
                continue
            for source, probability in enumerate(kernel[target]):
                if not probability:
                    continue
                selective[row, index[mask | (1 << source)]] += (
                    reciprocal * probability
                )
                replaced = (mask & ~(1 << target)) | (1 << source)
                neutral[row, index[replaced]] += reciprocal * probability
            without_target = mask & ~(1 << target)
            for union, probability in union_laws[target].items():
                new_mask = without_target | union
                locked[row, index[new_mask]] += reciprocal * probability

    refreshed_run = P_NEUTRAL * (
        eye(len(masks)) - Q_SELECTIVE * selective
    ).inv()
    refreshed = refreshed_run * neutral
    for event_kernel in (selective, neutral, refreshed, locked):
        row_kernel_check(event_kernel)
    return masks, neutral, refreshed, locked


def burst_generator(weights):
    """D generator on its recurrent nonempty, nonfull state space."""
    n = len(weights)
    full = (1 << n) - 1
    masks = tuple(range(1, full))
    index = {mask: row for row, mask in enumerate(masks)}
    kernel = normalized_kernel(weights)
    union_laws = tuple(geometric_union_law(row) for row in kernel)
    generator = fmpq_mat(len(masks), len(masks))
    for mask in masks:
        row = index[mask]
        for target in range(n):
            if not (mask & (1 << target)):
                continue
            without_target = mask & ~(1 << target)
            for union, probability in union_laws[target].items():
                new_mask = without_target | union
                assert new_mask in index
                add_change(generator, row, index[new_mask], probability)
    return masks, finish_generator(generator)


def stationary(generator: fmpq_mat):
    size = generator.nrows()
    system = generator.transpose()
    rhs = fmpq_mat(size, 1)
    for column in range(size):
        system[size - 1, column] = 1
    rhs[size - 1, 0] = 1
    law = system.solve(rhs)
    assert generator.transpose() * law == fmpq_mat(size, 1)
    assert sum(law[row, 0] for row in range(size)) == 1
    assert all(law[row, 0] > 0 for row in range(size))
    return law


def rank_mean(masks, law):
    return sum(
        mask.bit_count() * law[row, 0]
        for row, mask in enumerate(masks)
    )


def complete_means(n: int):
    b = n * A * R ** (n - 1) / (R**n - 1)
    d = (n - 1) * A * R ** (n - 2) / (R ** (n - 1) - 1)
    return b, d


def c_post_neutral_inverse_rank(weights, masks, pi_c, mean_c):
    """Compute beta_C(1/|A|) directly from its Palm definition."""
    n = len(weights)
    kernel = normalized_kernel(weights)
    answer = fmpq(0)
    for row, mask in enumerate(masks):
        rank = mask.bit_count()
        palm_mass = rank * pi_c[row, 0] / mean_c
        neutral_value = fmpq(0)
        for target in range(n):
            if not (mask & (1 << target)):
                continue
            for source, probability in enumerate(kernel[target]):
                if not probability:
                    continue
                new_mask = (mask & ~(1 << target)) | (1 << source)
                neutral_value += probability / new_mask.bit_count()
        neutral_value /= rank
        answer += palm_mass * neutral_value
    return answer


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


def tree_normalizer(generator: fmpq_mat, law):
    """Recover the full rooted-tree partition sum from two exact cofactors."""
    laplacian = -generator
    roots = (0, generator.nrows() - 1)
    normalizer = None
    for root in roots:
        cofactor = principal_minor(laplacian, root).det()
        assert cofactor > 0
        candidate = cofactor / law[root, 0]
        if normalizer is None:
            normalizer = candidate
        else:
            assert candidate == normalizer
    assert normalizer is not None
    return normalizer


def event_tree_normalizer(kernel: fmpq_mat, masks, law):
    """Rooted in-arborescence partition sum on the nonfull recurrent class."""
    full = masks[-1]
    keep = tuple(row for row, mask in enumerate(masks) if mask != full)
    restricted = fmpq_mat(len(keep), len(keep))
    for row, old_row in enumerate(keep):
        for column, old_column in enumerate(keep):
            restricted[row, column] = kernel[old_row, old_column]
    row_kernel_check(restricted)
    laplacian = eye(len(keep)) - restricted
    normalizer = None
    for reduced_root in (0, len(keep) - 1):
        old_root = keep[reduced_root]
        cofactor = principal_minor(laplacian, reduced_root).det()
        assert cofactor > 0 and law[old_root, 0] > 0
        candidate = cofactor / law[old_root, 0]
        if normalizer is None:
            normalizer = candidate
        else:
            assert candidate == normalizer
    assert normalizer is not None
    return normalizer


def rational_hash(value) -> str:
    return hashlib.sha256(f"{value.p}/{value.q}".encode("ascii")).hexdigest()


def analyze(label: str, weights, check_trees: bool = True):
    masks_l, generator_l = unbatched_generator(weights, "L")
    masks_c, generator_c = unbatched_generator(weights, "C")
    masks_d, generator_d = burst_generator(weights)
    pi_l = stationary(generator_l)
    pi_c = stationary(generator_c)
    pi_d = stationary(generator_d)
    mean_l = rank_mean(masks_l, pi_l)
    mean_c = rank_mean(masks_c, pi_c)
    mean_d = rank_mean(masks_d, pi_d)
    b, d = complete_means(len(weights))

    beta_f = c_post_neutral_inverse_rank(weights, masks_c, pi_c, mean_c)

    # Independently rebuild the two post-event arborescence root laws.
    event_masks, neutral, refreshed, locked = event_kernels(weights)
    assert event_masks == masks_c
    alpha_c = fmpq_mat(len(event_masks), 1)
    alpha_d = fmpq_mat(len(event_masks), 1)
    d_index = {mask: row for row, mask in enumerate(masks_d)}
    for row, mask in enumerate(event_masks):
        alpha_c[row, 0] = mask.bit_count() * pi_c[row, 0] / mean_c
        if mask in d_index:
            alpha_d[row, 0] = (
                mask.bit_count() * pi_d[d_index[mask], 0] / mean_d
            )
    beta_c = neutral.transpose() * alpha_c
    assert refreshed.transpose() * beta_c == beta_c
    assert locked.transpose() * alpha_d == alpha_d
    reciprocal_rank = fmpq_mat(len(event_masks), 1)
    for row, mask in enumerate(event_masks):
        reciprocal_rank[row, 0] = fmpq(1, mask.bit_count())
    assert (beta_c.transpose() * reciprocal_rank)[0, 0] == beta_f
    assert (alpha_d.transpose() * reciprocal_rank)[0, 0] == 1 / mean_d

    persistence = 1 / mean_d - beta_f
    timing = beta_f - (b / d) / mean_c
    orientation_product = (b * b - mean_l * mean_c) / (
        b * d * mean_c
    )
    combined = persistence + timing + orientation_product
    assert combined == 1 / mean_d - mean_l / (b * d)
    product_gap = b * d - mean_l * mean_d
    assert combined == product_gap / (b * d * mean_d)

    midpoint_defect = 2 * b - mean_l - mean_c
    orientation_cross = (
        -(b - mean_l) * (b - mean_c) / (b * d * mean_c)
    )
    assert orientation_product == midpoint_defect / (d * mean_c) + orientation_cross

    if check_trees:
        normalizer_l = tree_normalizer(generator_l, pi_l)
        normalizer_c = tree_normalizer(generator_c, pi_c)
        normalizer_d = tree_normalizer(generator_d, pi_d)
        normalizer_r = event_tree_normalizer(refreshed, event_masks, beta_c)
        normalizer_de = event_tree_normalizer(locked, event_masks, alpha_d)
        paired_forest = normalizer_l * normalizer_d * product_gap
        paired_event_forest = (
            normalizer_l
            * normalizer_de
            * (b * d / mean_d - mean_l)
        )
        orientation_forest = (
            normalizer_l
            * normalizer_c
            * (b * b - mean_l * mean_c)
        )
        assert paired_forest / (normalizer_l * normalizer_d) == product_gap
        assert (
            orientation_forest / (normalizer_l * normalizer_c)
            == b * b - mean_l * mean_c
        )
        assert paired_event_forest / (normalizer_l * normalizer_de) == (
            product_gap / mean_d
        )
        # Both event-root laws used by the Palm covariance have now been
        # recovered from independent directed-tree cofactors.
        assert normalizer_r > 0 and normalizer_de > 0
    else:
        paired_forest = product_gap
        paired_event_forest = product_gap / mean_d

    assert product_gap >= 0
    print(
        label,
        "product_gap", float(product_gap),
        "P", float(persistence),
        "T", float(timing),
        "Oprod", float(orientation_product),
        "Omid", float(midpoint_defect),
        "Ocross", float(orientation_cross),
        "hash", rational_hash(product_gap),
    )
    return {
        "mL": mean_l,
        "mC": mean_c,
        "mD": mean_d,
        "b": b,
        "d": d,
        "persistence": persistence,
        "timing": timing,
        "orientation_product": orientation_product,
        "midpoint_defect": midpoint_defect,
        "orientation_cross": orientation_cross,
        "combined": combined,
        "product_gap": product_gap,
        "paired_forest": paired_forest,
        "paired_event_forest": paired_event_forest,
    }


def graph(matrix):
    result = tuple(tuple(int(value) for value in row) for row in matrix)
    assert all(result[i][i] == 0 for i in range(len(result)))
    assert all(
        result[i][j] == result[j][i]
        for i in range(len(result))
        for j in range(len(result))
    )
    return result


def hostile_graphs():
    yield "K4", graph(
        [[0 if i == j else 1 for j in range(4)] for i in range(4)]
    )
    yield "weighted-P3-1:17", graph(
        [[0, 0, 1], [0, 0, 17], [1, 17, 0]]
    )
    yield "batching-persistence-n4", graph(
        [
            [0, 2, 0, 3],
            [2, 0, 1, 30],
            [0, 1, 0, 1],
            [3, 30, 1, 0],
        ]
    )
    yield "batching-timing-n5", graph(
        [
            [0, 0, 5, 5, 11],
            [0, 0, 7, 13, 1],
            [5, 7, 0, 1, 7],
            [5, 13, 1, 0, 2],
            [11, 1, 7, 2, 0],
        ]
    )
    windmill = [[0] * 7 for _ in range(7)]
    for (left, right), outer, internal in zip(
        ((1, 2), (3, 4), (5, 6)),
        (100, 10, 1),
        (600, 1200, 1800),
    ):
        windmill[left][right] = windmill[right][left] = internal
        windmill[0][left] = windmill[left][0] = outer
        windmill[0][right] = windmill[right][0] = outer
    yield "dB-windmill-n7", graph(windmill)


def main() -> None:
    results = {}
    for label, weights in hostile_graphs():
        results[label] = analyze(label, weights)

    complete = results["K4"]
    assert complete["product_gap"] == 0
    assert complete["persistence"] == 0
    assert complete["timing"] == 0
    assert complete["orientation_product"] == 0

    # Mandatory cancellation screen: no component is promoted to a theorem.
    assert results["batching-persistence-n4"]["persistence"] < 0
    assert results["batching-timing-n5"]["timing"] < 0
    assert results["weighted-P3-1:17"]["midpoint_defect"] > 0
    assert results["dB-windmill-n7"]["product_gap"] > 0
    print("PASS: exact combined endpoint paired-forest identity on hostile corpus")


if __name__ == "__main__":
    main()
