#!/usr/bin/env python3
"""Exact audit of the fitness-two normalized cross-rule tree reduction.

The script builds the Bd dual ``L``, reversed-arrow dual ``C``, and
fair-geometric dB dual ``D`` directly from an undirected integer weight
matrix.  It checks the uniform-reference adjoint, every targetwise resolvent
identity, marginal directed-tree cofactors, and the paired-tree numerator.

All arithmetic is ``Fraction`` arithmetic.  The all-graph sign SAPT_n is
not asserted: this verifies the exact reduction and frozen fingerprints.
"""

from __future__ import annotations

from fractions import Fraction as F


def add_rate(matrix, row, column, rate):
    if row != column and rate:
        matrix[row][column] += rate


def finish_generator(matrix):
    for row in range(len(matrix)):
        matrix[row][row] = -sum(
            (matrix[row][column] for column in range(len(matrix)) if column != row),
            F(0),
        )
        assert sum(matrix[row], F(0)) == 0
    return matrix


def transition_matrix(weights):
    n = len(weights)
    degrees = [sum(row) for row in weights]
    assert all(degree > 0 for degree in degrees)
    assert all(weights[i][j] == weights[j][i] for i in range(n) for j in range(n))
    return [[F(weights[i][j], degrees[i]) for j in range(n)] for i in range(n)]


def unbatched_generators(weights):
    """Return L and C at a=r-1=1 on all nonempty subsets."""

    p = transition_matrix(weights)
    n = len(p)
    full = (1 << n) - 1
    left = [[F(0) for _ in range(full)] for _ in range(full)]
    reverse = [[F(0) for _ in range(full)] for _ in range(full)]
    for state in range(1, full + 1):
        row = state - 1
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            for source in range(n):
                neutral = (state & ~(1 << target)) | (1 << source)
                selective = state | (1 << source)
                # L uses the graphical source->target rate P_source,target.
                add_rate(left, row, neutral - 1, p[source][target])
                add_rate(left, row, selective - 1, p[source][target])
                # C reverses the base arrow and hence samples row P_target,*.
                add_rate(reverse, row, neutral - 1, p[target][source])
                add_rate(reverse, row, selective - 1, p[target][source])
    return finish_generator(left), finish_generator(reverse)


def subsets(mask):
    sub = mask
    while True:
        yield sub
        if sub == 0:
            break
        sub = (sub - 1) & mask


def geometric_union_law(row):
    """Law of the nonempty union of N iid samples, P(N=j)=2^-j."""

    n = len(row)
    support = sum((1 << i) for i, value in enumerate(row) if value)

    def pgf(mass):
        return mass / (2 - mass)

    law = {}
    for target_set in subsets(support):
        if not target_set:
            continue
        probability = F(0)
        for included in subsets(target_set):
            mass = sum(
                (row[i] for i in range(n) if (included >> i) & 1), F(0)
            )
            sign = -1 if (target_set.bit_count() - included.bit_count()) & 1 else 1
            probability += sign * pgf(mass)
        if probability:
            assert probability > 0
            law[target_set] = probability
    assert sum(law.values(), F(0)) == 1
    return law


def local_kernels(weights, target):
    """Return S_v,N_v,G_v on all nonempty subsets as row kernels."""

    p = transition_matrix(weights)
    n = len(p)
    full = (1 << n) - 1
    selective = [[F(0) for _ in range(full)] for _ in range(full)]
    neutral = [[F(0) for _ in range(full)] for _ in range(full)]
    burst = [[F(0) for _ in range(full)] for _ in range(full)]
    union_law = geometric_union_law(p[target])
    for state in range(1, full + 1):
        row_index = state - 1
        if not ((state >> target) & 1):
            selective[row_index][row_index] = 1
            neutral[row_index][row_index] = 1
            burst[row_index][row_index] = 1
            continue
        without = state & ~(1 << target)
        for source in range(n):
            probability = p[target][source]
            selective[row_index][(state | (1 << source)) - 1] += probability
            neutral[row_index][(without | (1 << source)) - 1] += probability
        for source_set, probability in union_law.items():
            burst[row_index][(without | source_set) - 1] += probability
    for kernel in (selective, neutral, burst):
        assert all(sum(row, F(0)) == 1 for row in kernel)
    return selective, neutral, burst


def db_generator(weights):
    """Fair-geometric D generator on nonempty proper subsets."""

    n = len(weights)
    full = (1 << n) - 1
    size = full - 1
    generator = [[F(0) for _ in range(size)] for _ in range(size)]
    for target in range(n):
        _, _, burst = local_kernels(weights, target)
        for state in range(1, full):
            for output in range(1, full):
                add_rate(generator, state - 1, output - 1, burst[state - 1][output - 1])
    return finish_generator(generator)


def matmul(left, right):
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def determinant(matrix):
    work = [row[:] for row in matrix]
    size = len(work)
    answer = F(1)
    sign = 1
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
            sign *= -1
        value = work[column][column]
        answer *= value
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            scale = work[row][column] / value
            for j in range(column + 1, size):
                work[row][j] -= scale * work[column][j]
    return sign * answer


def tree_cofactors(generator):
    laplacian = [[-value for value in row] for row in generator]
    size = len(generator)
    answer = []
    for root in range(size):
        minor = [
            [laplacian[i][j] for j in range(size) if j != root]
            for i in range(size)
            if i != root
        ]
        answer.append(determinant(minor))
    assert all(value > 0 for value in answer)
    # The cofactor vector itself is a stationary row measure.
    for column in range(size):
        assert sum(
            (answer[row] * generator[row][column] for row in range(size)), F(0)
        ) == 0
    return answer


def tree_data(generator, states):
    cofactors = tree_cofactors(generator)
    partition = sum(cofactors, F(0))
    first = sum(
        (state.bit_count() * weight for state, weight in zip(states, cofactors)),
        F(0),
    )
    return cofactors, partition, first, first / partition


def conditional_tree_root_weights(generator, skeleton):
    """Root weights from orienting one undirected skeleton toward each root."""

    size = len(generator)
    adjacency = [[] for _ in range(size)]
    for left, right in skeleton:
        adjacency[left].append(right)
        adjacency[right].append(left)
    assert len(skeleton) == size - 1
    answer = []
    for root in range(size):
        parent = {root: None}
        queue = [root]
        for vertex in queue:
            for neighbor in adjacency[vertex]:
                if neighbor not in parent:
                    parent[neighbor] = vertex
                    queue.append(neighbor)
        assert len(parent) == size
        weight = F(1)
        for source in range(size):
            if source != root:
                weight *= generator[source][parent[source]]
        answer.append(weight)
    return answer


def check_local_resolvents(weights):
    n = len(weights)
    size = (1 << n) - 1
    identity = [[F(i == j) for j in range(size)] for i in range(size)]
    for target in range(n):
        selective, neutral, burst = local_kernels(weights, target)
        left_factor = [
            [identity[i][j] - selective[i][j] / 2 for j in range(size)]
            for i in range(size)
        ]
        burst_minus_identity = [
            [burst[i][j] - identity[i][j] for j in range(size)]
            for i in range(size)
        ]
        local_c_over_two = [
            [
                (neutral[i][j] - identity[i][j] + selective[i][j] - identity[i][j])
                / 2
                for j in range(size)
            ]
            for i in range(size)
        ]
        assert matmul(left_factor, burst_minus_identity) == local_c_over_two


def audit(weights, expected=None):
    n = len(weights)
    full = (1 << n) - 1
    left, reverse = unbatched_generators(weights)
    db = db_generator(weights)

    # At a=1, the weighted adjoint is the ordinary transpose and its defect
    # from C is diagonal.  This is precisely the tree-edge reversal identity.
    for i in range(full):
        for j in range(full):
            if i != j:
                assert left[j][i] == reverse[i][j]
    check_local_resolvents(weights)

    tau_l, z_l, y_l, m_l = tree_data(left, list(range(1, full + 1)))
    _, z_c, y_c, m_c = tree_data(reverse, list(range(1, full + 1)))
    tau_d, z_d, y_d, m_d = tree_data(db, list(range(1, full)))
    b = F(n * 2 ** (n - 1), 2**n - 1)
    d = F((n - 1) * 2 ** (n - 2), 2 ** (n - 1) - 1)

    tree_numerator = 2 * b * d * z_l * z_d - d * y_l * z_d - b * z_l * y_d
    expanded = sum(
        (
            tau_l[a]
            * tau_d[c]
            * (2 * b * d - d * (a + 1).bit_count() - b * (c + 1).bit_count())
            for a in range(len(tau_l))
            for c in range(len(tau_d))
        ),
        F(0),
    )
    delta = 2 - m_l / b - m_d / d
    assert tree_numerator == expanded
    assert delta == tree_numerator / (b * d * z_l * z_d)
    assert delta == (2 - (m_l + m_c) / b) + (m_c / b - m_d / d)

    product_numerator = b * d * z_l * z_d - y_l * y_d
    product_expanded = sum(
        (
            tau_l[a]
            * tau_d[c]
            * (b * d - (a + 1).bit_count() * (c + 1).bit_count())
            for a in range(len(tau_l))
            for c in range(len(tau_d))
        ),
        F(0),
    )
    product_gap = 1 - m_l * m_d / (b * d)
    assert product_numerator == product_expanded
    assert product_gap == product_numerator / (b * d * z_l * z_d)
    assert delta - product_gap == (1 - m_l / b) * (1 - m_d / d)

    # Event-Palm form.  Row-scaling D by 1/|A| produces K_D-I.  Its tree
    # root law is the size-biased D law, and its reciprocal-rank mean is 1/m_D.
    event_generator = [
        [value / (row + 1).bit_count() for value in db[row]]
        for row in range(len(db))
    ]
    theta_d = tree_cofactors(event_generator)
    theta = sum(theta_d, F(0))
    phi = sum(
        (weight / (state + 1).bit_count() for state, weight in enumerate(theta_d)),
        F(0),
    )
    assert phi / theta == 1 / m_d
    event_product_numerator = b * d * z_l * phi - y_l * theta
    event_expanded = sum(
        (
            tau_l[a]
            * theta_d[c]
            * (b * d / (c + 1).bit_count() - (a + 1).bit_count())
            for a in range(len(tau_l))
            for c in range(len(theta_d))
        ),
        F(0),
    )
    assert event_product_numerator == event_expanded
    assert event_product_numerator / (b * d * z_l * theta) == (
        1 / m_d - m_l / (b * d)
    )

    # The tensor stationary law is checked without constructing its much
    # larger tree Laplacian.  The tree theorem then gives the
    # root-independent cofactor factor in equation (14) of the note.
    pi_l = [value / z_l for value in tau_l]
    pi_d = [value / z_d for value in tau_d]
    for a in range(len(pi_l)):
        for c in range(len(pi_d)):
            product_drift = sum(
                (pi_l[i] * pi_d[c] * left[i][a] for i in range(len(pi_l))), F(0)
            ) + sum(
                (pi_l[a] * pi_d[j] * db[j][c] for j in range(len(pi_d))), F(0)
            )
            assert product_drift == 0

    if expected is not None:
        assert (b, d, m_l, m_c, m_d, delta) == expected
    return b, d, m_l, m_c, m_d, delta


def audit_local_paired_skeleton_obstruction():
    """Refute a pair-by-pair skeleton sign on the unweighted K3."""

    weights = (
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
    )
    left, _ = unbatched_generators(weights)
    db = db_generator(weights)
    # Masks: 1,...,7.  Every listed L edge is bidirected and symmetric.
    left_skeleton_masks = ((1, 2), (1, 3), (1, 4), (1, 5), (2, 6), (3, 7))
    left_skeleton = tuple((a - 1, b - 1) for a, b in left_skeleton_masks)
    left_roots = conditional_tree_root_weights(left, left_skeleton)
    assert len(set(left_roots)) == 1
    left_mean = sum(
        ((root + 1).bit_count() * weight for root, weight in enumerate(left_roots)),
        F(0),
    ) / sum(left_roots, F(0))
    assert left_mean == F(12, 7)

    # Proper masks 1,...,6.  On this star, only the in-orientation rooted at
    # mask 6 is supported: 2,3,4,5 -> 1 -> 6.
    db_skeleton_masks = ((1, 2), (1, 3), (1, 4), (1, 5), (1, 6))
    db_skeleton = tuple((a - 1, b - 1) for a, b in db_skeleton_masks)
    db_roots = conditional_tree_root_weights(db, db_skeleton)
    assert db_roots[5] == F(1, 3**5)
    assert all(weight == 0 for root, weight in enumerate(db_roots) if root != 5)
    db_mean = F(2)

    b, d = F(12, 7), F(4, 3)
    assert 2 - left_mean / b - db_mean / d == F(-1, 2)
    assert 1 - left_mean * db_mean / (b * d) == F(-1, 2)


def main():
    weighted_path = (
        (0, 1, 2),
        (1, 0, 0),
        (2, 0, 0),
    )
    expected = (
        F(12, 7),
        F(4, 3),
        F(584, 341),
        F(118, 75),
        F(6, 5),
        F(1033, 10230),
    )
    assert audit(weighted_path, expected) == expected

    complete = (
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
    )
    b, d, m_l, m_c, m_d, delta = audit(complete)
    assert m_l == m_c == b
    assert m_d == d
    assert delta == 0
    audit_local_paired_skeleton_obstruction()

    print("PASS: exact uniform-adjoint and targetwise fair-resolvent identities")
    print("PASS: marginal cofactors and paired-tree numerator")
    print("PASS: weighted-P3 normalized gap = 1033/10230")
    print("PASS: weighted-P3 normalized product gap = 172/1705")
    print("REFUTED: pair-by-pair skeleton signs (both gaps = -1/2 on K3)")
    print("OPEN: the all-graph shared-arrow signs SAPT_n and PAPT_n")


if __name__ == "__main__":
    main()
