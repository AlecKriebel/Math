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


def identity(size):
    return [[F(i == j) for j in range(size)] for i in range(size)]


def inverse(matrix):
    """Gauss--Jordan inverse over QQ."""

    size = len(matrix)
    work = [row[:] + unit[:] for row, unit in zip(matrix, identity(size))]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
        value = work[column][column]
        work[column] = [entry / value for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[column])
            ]
    return [row[size:] for row in work]


def row_times_matrix(row, matrix):
    return [
        sum((row[i] * matrix[i][j] for i in range(len(row))), F(0))
        for j in range(len(matrix[0]))
    ]


def dot(row, column):
    return sum((left * right for left, right in zip(row, column)), F(0))


def event_kernels_r2(weights):
    """Return target-refreshed C and target-locked D event kernels at r=2."""

    p = transition_matrix(weights)
    n = len(weights)
    full = (1 << n) - 1
    size = full
    selective = [[F(0) for _ in range(size)] for _ in range(size)]
    neutral = [[F(0) for _ in range(size)] for _ in range(size)]
    locked = [[F(0) for _ in range(size)] for _ in range(size)]
    union_laws = [geometric_union_law(row) for row in p]
    for state in range(1, full + 1):
        row = state - 1
        reciprocal_rank = F(1, state.bit_count())
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            without = state & ~(1 << target)
            for source in range(n):
                probability = reciprocal_rank * p[target][source]
                selective[row][(state | (1 << source)) - 1] += probability
                neutral[row][(without | (1 << source)) - 1] += probability
            for source_set, probability in union_laws[target].items():
                locked[row][(without | source_set) - 1] += (
                    reciprocal_rank * probability
                )
    for kernel in (selective, neutral, locked):
        assert all(sum(row, F(0)) == 1 for row in kernel)

    # At r=2, a selective arrow and the terminating neutral arrow are fair.
    resolvent_inverse = [
        [F(i == j) - selective[i][j] / 2 for j in range(size)]
        for i in range(size)
    ]
    refreshed_run = [
        [entry / 2 for entry in row] for row in inverse(resolvent_inverse)
    ]
    refreshed = matmul(refreshed_run, neutral)
    assert all(sum(row, F(0)) == 1 for row in refreshed)
    return selective, neutral, refreshed, locked


def internal_mass(weights, state):
    r"""I_P(A)=sum_{v in A} sum_{u in A\{v}} P_vu."""

    p = transition_matrix(weights)
    n = len(weights)
    return sum(
        (
            p[target][source]
            for target in range(n)
            if (state >> target) & 1
            for source in range(n)
            if source != target and (state >> source) & 1
        ),
        F(0),
    )


def neutral_collision_numerator(weights, state):
    """Sum over occupied neutral targets of the output reciprocal rank."""

    p = transition_matrix(weights)
    n = len(weights)
    return sum(
        (
            p[target][source]
            / ((state & ~(1 << target)) | (1 << source)).bit_count()
            for target in range(n)
            if (state >> target) & 1
            for source in range(n)
        ),
        F(0),
    )


def marked_kernel_r2(weights):
    """Exact one-sample marked dB kernel M_P on (C,v), v not in C."""

    p = transition_matrix(weights)
    n = len(weights)
    states = tuple(
        (cache, target)
        for cache in range(1 << n)
        for target in range(n)
        if not ((cache >> target) & 1)
    )
    index = {state: row for row, state in enumerate(states)}
    kernel = [[F(0) for _ in states] for _ in states]
    for row, (cache, target) in enumerate(states):
        for sample in range(n):
            probability = p[target][sample]
            if not probability:
                continue
            active = cache | (1 << sample)
            # Continue with the same target.
            kernel[row][index[active, target]] += probability / 2
            # Stop and retarget uniformly within the active set.
            for new_target in range(n):
                if (active >> new_target) & 1:
                    output = active & ~(1 << new_target)
                    kernel[row][index[output, new_target]] += (
                        probability / (2 * active.bit_count())
                    )
    assert all(sum(row, F(0)) == 1 for row in kernel)
    return states, kernel


def marked_psi(n, rank):
    """Alternating inverse-rank observable on marked cache rank."""

    return sum(
        (2 * F((-1) ** (active_rank - 1 - rank), active_rank)
         for active_rank in range(rank + 1, n)),
        F(0),
    )


def shared_l_two_step_forcing(weights, marked_states, marked_two_step):
    """F_P(A)=sum_{v in A} (M_P^2 psi)(A^c,v)."""

    n = len(weights)
    full = (1 << n) - 1
    index = {state: row for row, state in enumerate(marked_states)}
    answer = []
    for occupied in range(1, full + 1):
        cache = full ^ occupied
        answer.append(
            sum(
                (
                    marked_two_step[index[cache, target]]
                    for target in range(n)
                    if (occupied >> target) & 1
                ),
                F(0),
            )
        )
    return answer


def collapsed_shared_l_forcing(weights, occupied):
    r"""Closed local-arrow formula for F_P(A), away from k=0,1 boundaries.

    Here A is the occupied L set, C=V\A is its marked cache, and k=|C|.
    The formula is obtained by conditioning the first marked step on whether
    its sample lies in C, then using the exact neutral collision collapse on
    the stop branch.  It is intentionally checked only for k>=2; the two
    small-cache boundary formulas are evaluated directly by M_P.
    """

    p = transition_matrix(weights)
    n = len(weights)
    full = (1 << n) - 1
    cache = full ^ occupied
    rank = cache.bit_count()
    assert rank >= 2
    targets = [target for target in range(n) if (occupied >> target) & 1]
    cache_vertices = [source for source in range(n) if (cache >> source) & 1]
    x = {
        target: sum((p[target][source] for source in cache_vertices), F(0))
        for target in targets
    }
    internal = internal_mass(weights, cache)
    x_sum = sum(x.values(), F(0))
    x_square = sum((value * value for value in x.values()), F(0))
    occupied_request = F(len(targets)) - x_sum
    new_sample_square = sum(
        (
            p[target][sample] * p[target][sample]
            for target in targets
            for sample in targets
        ),
        F(0),
    )
    new_internal_cross = sum(
        (
            p[target][sample]
            * (
                sum((p[source][sample] for source in cache_vertices), F(0))
                + sum((p[sample][source] for source in cache_vertices), F(0))
            )
            for target in targets
            for sample in targets
        ),
        F(0),
    )
    return F(1, 2) * (
        x_sum
        * (
            F(1, rank)
            + F(1, rank + 1)
            + internal / (rank * rank * (rank - 1))
        )
        + x_square / (rank * (rank + 1))
        + occupied_request
        * (
            F(1, rank + 1)
            + F(1, rank + 2)
            + internal / (rank * (rank + 1) * (rank + 1))
        )
        + (x_sum - x_square) / ((rank + 1) * (rank + 2))
        + new_sample_square / ((rank + 1) * (rank + 2))
        + new_internal_cross / (rank * (rank + 1) * (rank + 1))
    )


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
    tau_c, z_c, y_c, m_c = tree_data(reverse, list(range(1, full + 1)))
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

    # Shared-C event-Palm split of the decisive product target.  The
    # pre-neutral C Palm law is rank-size-biased pi_C, and beta_C is its
    # law immediately after the neutral arrow.  The latter is invariant
    # for the target-refreshed post-neutral event kernel.
    _, neutral, refreshed, locked = event_kernels_r2(weights)
    pi_c = [value / z_c for value in tau_c]
    alpha_c = [
        (state + 1).bit_count() * pi_c[state] / m_c for state in range(full)
    ]
    beta_c = row_times_matrix(alpha_c, neutral)
    assert row_times_matrix(beta_c, refreshed) == beta_c

    pi_d = [value / z_d for value in tau_d]
    alpha_d = [F(0) for _ in range(full)]
    for state in range(full - 1):
        alpha_d[state] = (state + 1).bit_count() * pi_d[state] / m_d
    assert row_times_matrix(alpha_d, locked) == alpha_d
    reciprocal_rank = [F(1, (state + 1).bit_count()) for state in range(full)]
    beta_f = dot(beta_c, reciprocal_rank)
    assert dot(alpha_d, reciprocal_rank) == 1 / m_d

    # A neutral replacement from A has output rank k-1 precisely when its
    # sampled source already lies in A\{v}.  Therefore the unnormalized
    # reciprocal-rank collision observable collapses pointwise to internal
    # P-mass, with no resolvent or Poisson potential.
    collision_observable = []
    for state in range(1, full + 1):
        rank = state.bit_count()
        internal = internal_mass(weights, state)
        direct = neutral_collision_numerator(weights, state)
        collapsed = F(1) if rank == 1 else F(1) + internal / (rank * (rank - 1))
        assert direct == collapsed
        collision_observable.append(collapsed)
    collision_partition = sum(
        (weight * value for weight, value in zip(tau_c, collision_observable)),
        F(0),
    )
    assert beta_f == collision_partition / y_c

    # The C rank drift is k-2 I_P(A), so stationarity fixes the first
    # internal-mass moment exactly.
    mean_internal = sum(
        (
            pi_c[state - 1] * internal_mass(weights, state)
            for state in range(1, full + 1)
        ),
        F(0),
    )
    assert mean_internal == m_c / 2

    persistence_gap = 1 / m_d - beta_f
    collision_orientation_gap = beta_f - m_l / (b * d)
    assert persistence_gap + collision_orientation_gap == (
        1 / m_d - m_l / (b * d)
    )

    # The second term is itself one global out-C / in-C collision-tree
    # determinant.  This is a strict reduction, not a claimed sign.
    collision_orientation_numerator = (
        b * d * z_l * collision_partition - y_l * y_c
    )
    assert collision_orientation_gap == collision_orientation_numerator / (
        b * d * z_l * y_c
    )

    # A tempting statewise locked-versus-refreshed comparison is recorded
    # only diagnostically; no sign assertion is made here.
    locked_f = [dot(row, reciprocal_rank) for row in locked]
    refreshed_f = [dot(row, reciprocal_rank) for row in refreshed]
    statewise_persistence_min = min(
        locked_value - refreshed_value
        for locked_value, refreshed_value in zip(locked_f, refreshed_f)
    )

    # Common-arrow marked finite-time form.  Complementing the occupied
    # target Palm law of L gives the probability q_L(C,v)=pi_L(V\C)/m_L.
    # Its stationary M_P limit is 1/m_D, so the product target is the
    # stationary lower floor q_L M_P^infinity psi >= m_L/(b d).  The exact
    # t=2 forcing is a one-copy observable F_P on occupied L sets.
    marked_states, marked_kernel = marked_kernel_r2(weights)
    psi = [marked_psi(n, cache.bit_count()) for cache, _ in marked_states]
    marked_one_step = [dot(row, psi) for row in marked_kernel]
    marked_two_step = [dot(row, marked_one_step) for row in marked_kernel]
    marked_index = {state: row for row, state in enumerate(marked_states)}
    for row, (cache, target) in enumerate(marked_states):
        rank = cache.bit_count()
        request_mass = sum(
            (
                transition_matrix(weights)[target][source]
                for source in range(n)
                if (cache >> source) & 1
            ),
            F(0),
        )
        collapsed = (
            F(1)
            if rank == 0
            else F(1, rank + 1) + request_mass / (rank * (rank + 1))
        )
        assert marked_one_step[row] == collapsed

    pi_l = [value / z_l for value in tau_l]
    q_l = []
    for cache, target in marked_states:
        occupied = full ^ cache
        q_l.append(pi_l[occupied - 1] / m_l)
    assert sum(q_l, F(0)) == 1
    q_l_t2 = dot(q_l, marked_two_step)
    forcing = shared_l_two_step_forcing(weights, marked_states, marked_two_step)
    for occupied, direct_forcing in enumerate(forcing, 1):
        if (full ^ occupied).bit_count() >= 2:
            assert collapsed_shared_l_forcing(weights, occupied) == direct_forcing
    forcing_mean = dot(pi_l, forcing)
    assert forcing_mean == m_l * q_l_t2
    two_step_gap = q_l_t2 - m_l / (b * d)
    two_copy_mean_gap = forcing_mean - m_l * m_l / (b * d)
    assert two_copy_mean_gap == m_l * two_step_gap

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
    return (
        b,
        d,
        m_l,
        m_c,
        m_d,
        delta,
        persistence_gap,
        collision_orientation_gap,
        statewise_persistence_min,
        q_l_t2,
        forcing_mean,
        two_step_gap,
    )


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
    weighted_data = audit(weighted_path)
    assert weighted_data[:6] == expected

    complete = (
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
    )
    complete_data = audit(complete)
    b, d, m_l, m_c, m_d, delta = complete_data[:6]
    assert m_l == m_c == b
    assert m_d == d
    assert delta == 0
    audit_local_paired_skeleton_obstruction()

    # The expanded local-arrow forcing has more independent quadratic terms
    # once both the occupied set and its complement have size at least two;
    # audit that regime on K4 as well as the weighted P3 boundary.
    complete_four = tuple(
        tuple(0 if left == right else 1 for right in range(4))
        for left in range(4)
    )
    complete_four_data = audit(complete_four)
    assert complete_four_data[11] == 0

    print("PASS: exact uniform-adjoint and targetwise fair-resolvent identities")
    print("PASS: marginal cofactors and paired-tree numerator")
    print("PASS: weighted-P3 normalized gap = 1033/10230")
    print("PASS: weighted-P3 normalized product gap = 172/1705")
    print(
        "PASS: exact shared-C Palm split on weighted P3 =",
        weighted_data[6],
        "+",
        weighted_data[7],
    )
    print(
        "AUDIT: minimum statewise locked-minus-refreshed reciprocal rank =",
        weighted_data[8],
    )
    assert weighted_data[10] == F(492, 341)
    print(
        "PASS: weighted-P3 common-arrow q_L M^2 psi and E_piL F =",
        weighted_data[9],
        weighted_data[10],
    )
    print("AUDIT: weighted-P3 common-arrow t=2 gap =", weighted_data[11])
    print("PASS: expanded local-arrow forcing on every complete-K4 set")
    print("REFUTED: pair-by-pair skeleton signs (both gaps = -1/2 on K3)")
    print("OPEN: the all-graph shared-arrow signs SAPT_n and PAPT_n")


if __name__ == "__main__":
    main()
