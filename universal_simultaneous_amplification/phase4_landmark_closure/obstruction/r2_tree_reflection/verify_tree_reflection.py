#!/usr/bin/env python3
"""Exact verifier for the r=2 tree/reflection reduction.

This is deliberately independent of the posterior/Brier strengthening.  It
constructs the fair-geometric subset chain, checks the Markov-chain tree
formula, evaluates the exact finite-baseline mean inequality on the frozen
hostile corpus, and certifies two failures of local complement/root-moving
proof strategies on the unweighted triangle.

All arithmetic is ``Fraction`` arithmetic.  Finite tests validate the
reduction and refute the stated strengthenings; they are not a proof of the
open all-graph tree inequality.
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
OBSTRUCTION = HERE.parent
CHI_DIR = OBSTRUCTION / "r2_entropy_certificate" / "chi_square_channel"
COLLISION_DIR = OBSTRUCTION / "r2_collision_closure"
sys.path.insert(0, str(CHI_DIR))
sys.path.insert(0, str(COLLISION_DIR))

from verify_resolvent_identities import solve  # noqa: E402
from verify_direct_flow_screen import (  # noqa: E402
    connected,
    deterministic_graphs,
    exhaustive_graphs,
    matrix_from_edges,
)


def average_kernel(weights):
    """Return the exact occupied-target-average subset kernel."""

    _, states, _, kernels, pi = solve(weights)
    size = len(states)
    n = len(weights)
    q = [[F(0) for _ in range(size)] for _ in range(size)]
    for kernel in kernels:
        for source in range(size):
            for target in range(size):
                q[source][target] += kernel[source][target] / n
    assert all(sum(row, F(0)) == 1 for row in q)
    return states, q, pi


def geometric_all_inside(mass):
    """P(all fair-geometric samples lie in a set of row mass ``mass``)."""

    return mass / (2 - mass)


def burst_probability(row, redundant, additions):
    """Probability that the new (nonredundant) sampled set is ``additions``.

    ``redundant`` and ``additions`` are disjoint bitmasks.  Inclusion-
    exclusion forces every addition to be sampled while allowing arbitrary
    samples in the redundant set.
    """

    vertices = [i for i in range(len(row)) if (additions >> i) & 1]
    answer = F(0)
    for omitted_mask in range(1 << len(vertices)):
        allowed = redundant
        parity = 0
        for j, vertex in enumerate(vertices):
            if (omitted_mask >> j) & 1:
                parity += 1
            else:
                allowed |= 1 << vertex
        mass = sum(
            (row[i] for i in range(len(row)) if (allowed >> i) & 1),
            F(0),
        )
        answer += (-1 if parity & 1 else 1) * geometric_all_inside(mass)
    assert answer >= 0
    return answer


def audit_burst_and_complement_formula(weights):
    """Check every state edge against the exact complement-reflection law."""

    P, states, _, kernels, _ = solve(weights)
    n = len(P)
    q = [[F(0) for _ in states] for _ in states]
    for kernel in kernels:
        for source in range(len(states)):
            for target in range(len(states)):
                q[source][target] += kernel[source][target] / n
    assert all(sum(row, F(0)) == 1 for row in q)
    full = (1 << n) - 1
    index = {state: position for position, state in enumerate(states)}
    degrees = [sum(row) for row in weights]
    for v in range(n):
        for i in range(n):
            assert degrees[v] * P[v][i] == degrees[i] * P[i][v]

    for source_position, source in enumerate(states):
        for target_position, target in enumerate(states):
            observed = q[source_position][target_position]
            if source == target:
                assert observed == F(n - source.bit_count(), n)
                continue
            lost = source & ~target
            if lost.bit_count() != 1:
                assert observed == 0
                continue
            v = lost.bit_length() - 1
            redundant = source & ~(1 << v)
            assert redundant & ~target == 0
            additions = target & ~redundant
            formula = burst_probability(P[v], redundant, additions) / n
            assert observed == formula

            # Complement plus path reversal exchanges the redundant set C
            # with R=V\(C union D union {v}) and retains the same additions D.
            complement_source = full ^ target
            complement_target = full ^ source
            outside = full ^ (redundant | additions | (1 << v))
            reflected = burst_probability(P[v], outside, additions) / n
            assert q[index[complement_source]][index[complement_target]] == reflected


def determinant(matrix):
    """Exact determinant by fraction-preserving Gaussian elimination."""

    a = [row[:] for row in matrix]
    n = len(a)
    sign = 1
    answer = F(1)
    for column in range(n):
        pivot = next((row for row in range(column, n) if a[row][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            a[pivot], a[column] = a[column], a[pivot]
            sign *= -1
        value = a[column][column]
        answer *= value
        for row in range(column + 1, n):
            if not a[row][column]:
                continue
            scale = a[row][column] / value
            for j in range(column + 1, n):
                a[row][j] -= scale * a[column][j]
        # Entries below the pivot no longer matter, and clearing them avoids
        # accidental reuse if this routine is modified.
        for row in range(column + 1, n):
            a[row][column] = F(0)
    return sign * answer


def tree_cofactors(q):
    """Directed in-arborescence weights for a row-stochastic kernel."""

    size = len(q)
    laplacian = [[F(0) for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if i != j:
                laplacian[i][j] = -q[i][j]
        laplacian[i][i] = sum(
            (q[i][j] for j in range(size) if j != i), F(0)
        )
    cofactors = []
    for root in range(size):
        minor = [
            [laplacian[i][j] for j in range(size) if j != root]
            for i in range(size)
            if i != root
        ]
        cofactors.append(determinant(minor))
    assert all(value > 0 for value in cofactors)
    return cofactors


def complete_mean(n):
    return F((n - 1) * 2 ** (n - 2), 2 ** (n - 1) - 1)


def mean_from_tree_cofactors(states, cofactors):
    total = sum(cofactors, F(0))
    return sum(
        (state.bit_count() * weight for state, weight in zip(states, cofactors)),
        F(0),
    ) / total


def exact_mean_screen(weights, check_cofactors=False):
    states, q, pi = average_kernel(weights)
    n = len(weights)
    mean = sum(
        (state.bit_count() * probability for state, probability in zip(states, pi)),
        F(0),
    )
    if check_cofactors:
        cofactors = tree_cofactors(q)
        tree_total = sum(cofactors, F(0))
        assert all(
            pi[i] == cofactors[i] / tree_total for i in range(len(states))
        )
        assert mean == mean_from_tree_cofactors(states, cofactors)
    return mean, complete_mean(n)


def is_in_arborescence(parent, root):
    """Check a functional digraph is a tree directed into ``root``."""

    size = len(parent)
    for source in range(size):
        if source == root:
            continue
        seen = set()
        vertex = source
        while vertex != root:
            if vertex in seen or vertex not in parent:
                return False
            seen.add(vertex)
            vertex = parent[vertex]
    return True


def enumerate_in_trees(q, root):
    size = len(q)
    vertices = [vertex for vertex in range(size) if vertex != root]
    choices = [
        [target for target in range(size) if target != source and q[source][target]]
        for source in vertices
    ]
    for targets in product(*choices):
        parent = dict(zip(vertices, targets))
        if not is_in_arborescence(parent, root):
            continue
        edges = tuple(sorted(parent.items()))
        weight = F(1)
        for source, target in edges:
            weight *= q[source][target]
        yield edges, weight


def complement_reverse_edges(states, edges, n):
    """Map X->Y to complement(Y)->complement(X)."""

    full = (1 << n) - 1
    index = {state: position for position, state in enumerate(states)}
    answer = []
    for source, target in edges:
        new_source = index[full ^ states[target]]
        new_target = index[full ^ states[source]]
        answer.append((new_source, new_target))
    return tuple(sorted(answer))


def edge_product(q, edges):
    answer = F(1)
    for source, target in edges:
        answer *= q[source][target]
    return answer


def audit_first_treewise_failures():
    """Certify the first exact failures of local path/root reflection."""

    triangle = [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]
    states, q, _ = average_kernel(triangle)
    assert states == [1, 2, 3, 4, 5, 6]
    index = {state: position for position, state in enumerate(states)}

    # An in-tree rooted at {0,1}.  Complementing vertices and reversing every
    # arrow gives an out-tree rooted at {2}, but its weight is four times
    # smaller.  Thus no edgewise/pathwise likelihood domination is available,
    # even at the maximally symmetric original graph.
    in_edges_masks = ((1, 6), (2, 5), (4, 3), (5, 3), (6, 3))
    in_edges = tuple((index[a], index[b]) for a, b in in_edges_masks)
    assert is_in_arborescence(dict(in_edges), index[3])
    reversed_edges = complement_reverse_edges(states, in_edges, 3)
    in_weight = edge_product(q, in_edges)
    reversed_weight = edge_product(q, reversed_edges)
    assert in_weight == F(4, 59049)
    assert reversed_weight == F(1, 59049)
    assert in_weight == 4 * reversed_weight

    # A stronger obstruction to same-skeleton root transport.  On the state
    # skeleton which is the star centred at mask 1, the *only* orientation
    # supported as an in-tree is rooted at mask 6 (rank two).  Its conditional
    # root mean is therefore 2, strictly above the complete mean 4/3.
    skeleton_masks = ((1, 2), (1, 3), (1, 4), (1, 5), (1, 6))
    root_weights = {}
    for root_mask in states:
        root = index[root_mask]
        oriented = []
        # Orient the undirected tree uniquely toward the proposed root.
        adjacency = {state: [] for state in states}
        for a, b in skeleton_masks:
            adjacency[a].append(b)
            adjacency[b].append(a)
        for source_mask in states:
            if source_mask == root_mask:
                continue
            previous = None
            vertex = source_mask
            while vertex != root_mask:
                candidates = [x for x in adjacency[vertex] if x != previous]
                # In a tree, the neighbor whose component contains the root is
                # found by a tiny breadth-first test.
                next_vertex = None
                for candidate in candidates:
                    stack = [candidate]
                    seen = {vertex}
                    while stack:
                        x = stack.pop()
                        if x == root_mask:
                            next_vertex = candidate
                            break
                        if x in seen:
                            continue
                        seen.add(x)
                        stack.extend(adjacency[x])
                    if next_vertex is not None:
                        break
                assert next_vertex is not None
                oriented.append((index[source_mask], index[next_vertex]))
                break
        weight = edge_product(q, oriented)
        root_weights[root_mask] = weight
    assert root_weights[6] == F(1, 59049)
    assert all(root_weights[state] == 0 for state in states if state != 6)
    skeleton_mean = sum(
        (state.bit_count() * value for state, value in root_weights.items()),
        F(0),
    ) / sum(root_weights.values(), F(0))
    assert skeleton_mean == 2 > complete_mean(3)

    # Complementing the first in-tree without reversing its arrows would make
    # an in-tree at the complementary root, but already its first edge 1->6
    # becomes the forbidden edge 6->1.  The fair-geometric state support is
    # directed, despite reversibility of the original vertex walk.
    full = 7
    complemented_same_orientation = tuple(
        (index[full ^ states[source]], index[full ^ states[target]])
        for source, target in in_edges
    )
    assert edge_product(q, complemented_same_orientation) == 0

    print(
        "PASS: exact K3 complement-path failure: in/out weight ratio = "
        f"{in_weight / reversed_weight}"
    )
    print(
        "PASS: exact K3 same-skeleton failure: sole supported root has "
        f"rank {skeleton_mean} > m_K={complete_mean(3)}"
    )


def labelled_sequence_count(source, target, length, n):
    """Number of length-``length`` labelled bursts for unweighted K_n."""

    lost = source & ~target
    if lost.bit_count() != 1:
        return 0
    v = lost.bit_length() - 1
    redundant = source & ~(1 << v)
    if redundant & ~target:
        return 0
    additions = target & ~redundant
    addition_vertices = [i for i in range(n) if (additions >> i) & 1]
    answer = 0
    for omitted_mask in range(1 << len(addition_vertices)):
        allowed = redundant
        parity = 0
        for j, vertex in enumerate(addition_vertices):
            if (omitted_mask >> j) & 1:
                parity += 1
            else:
                allowed |= 1 << vertex
        choices = sum(
            1 for i in range(n) if i != v and ((allowed >> i) & 1)
        )
        answer += (-1 if parity & 1 else 1) * choices ** length
    return answer


def truncated_convolution(left, right, degree):
    answer = [0 for _ in range(degree + 1)]
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            if i + j <= degree:
                answer[i + j] += x * y
    return answer


def audit_labelled_history_lift_failure():
    """Refute length-preserving microscopic path reversal exactly on K3.

    At regular K3, every labelled burst history of total sample length M has
    the same geometric/walk factor 4^{-M} (apart from the common target
    factor).  Hence a two-copy high-root-to-low-root injection produced by
    reversing microscopic vertex-walk arrows would preserve M.  The exact
    coefficient count is already deficient at M=10.
    """

    triangle = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
    states, q, _ = average_kernel(triangle)
    # Every K3 edge-history series has denominator dividing
    # (1-z)(1-2z).  A state arborescence has five edges, so the aggregate
    # denominator divides D=(1-z)^5(1-2z)^5.  Computing through degree 20
    # and multiplying by D therefore verifies the displayed rational
    # identity exactly, not just its first bad coefficient.
    degree = 20
    totals = {
        1: [0 for _ in range(degree + 1)],
        2: [0 for _ in range(degree + 1)],
    }
    for root in range(len(states)):
        for edges, _ in enumerate_in_trees(q, root):
            polynomial = [1] + [0 for _ in range(degree)]
            for source, target in edges:
                edge_polynomial = [0] + [
                    labelled_sequence_count(
                        states[source], states[target], length, 3
                    )
                    for length in range(1, degree + 1)
                ]
                polynomial = truncated_convolution(
                    polynomial, edge_polynomial, degree
                )
            rank = states[root].bit_count()
            totals[rank] = [
                x + y for x, y in zip(totals[rank], polynomial)
            ]

    assert totals[1][:11] == [
        0, 0, 0, 0, 0, 450, 4050, 21870, 92070, 333468, 1091844
    ]
    assert totals[2][:11] == [
        0, 0, 0, 0, 0, 0, 450, 4950, 31770, 155610, 644688
    ]
    difference = [x - 2 * y for x, y in zip(totals[1], totals[2])]
    assert difference[9] == 22248
    assert difference[10] == -197532

    def polynomial_power(linear, exponent):
        answer = [1] + [0 for _ in range(degree)]
        padded = linear + [0 for _ in range(degree + 1 - len(linear))]
        for _ in range(exponent):
            answer = truncated_convolution(answer, padded, degree)
        return answer

    denominator = truncated_convolution(
        polynomial_power([1, -1], 5),
        polynomial_power([1, -2], 5),
        degree,
    )
    quadratic = [5, -10, 4] + [0 for _ in range(degree - 2)]
    numerator = truncated_convolution(quadratic, quadratic, degree)
    numerator = truncated_convolution(
        numerator,
        [0, 0, 0, 0, 0, 18, -72]
        + [0 for _ in range(degree - 6)],
        degree,
    )
    assert truncated_convolution(difference, denominator, degree) == numerator
    print(
        "PASS: labelled-history lift is not lengthwise positive: "
        "[z^10](T_1-2T_2)=-197532 on K3 (rational identity exact)"
    )


def audit_markov_tree_theorem_and_frozen_graphs():
    path3 = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    audit_burst_and_complement_formula(path3)
    mean, baseline = exact_mean_screen(path3, check_cofactors=True)
    assert mean == F(11, 9) < baseline == F(4, 3)

    regular_k4 = [
        [0, 1, 1, 2],
        [1, 0, 2, 1],
        [1, 2, 0, 1],
        [2, 1, 1, 0],
    ]
    audit_burst_and_complement_formula(regular_k4)
    mean, baseline = exact_mean_screen(regular_k4, check_cofactors=True)
    assert mean == F(70, 41) < baseline == F(12, 7)

    split_witness = matrix_from_edges(
        6,
        (3, 300, 2, 5, 1, 3, 3, 1, 300, 1, 1, 1, 20, 1, 1),
    )
    audit_burst_and_complement_formula(split_witness)
    mean, baseline = exact_mean_screen(split_witness)
    assert mean < baseline

    # Graphs used in the earlier complementary-level diagnostics, retained as
    # an exact hostile regression set here.
    complementary_level_witnesses = [
        [[0, 1, 0], [1, 0, 2], [0, 2, 0]],
        [[0, 1, 3], [1, 0, 2], [3, 2, 0]],
        [
            [0, 1, 3, 0],
            [1, 0, 2, 4],
            [3, 2, 0, 5],
            [0, 4, 5, 0],
        ],
        [
            [0, 1, 0, 2],
            [1, 0, 3, 0],
            [0, 3, 0, 4],
            [2, 0, 4, 0],
        ],
    ]
    for weights in complementary_level_witnesses:
        mean, baseline = exact_mean_screen(weights)
        assert mean <= baseline

    print("PASS: directed Markov-chain tree theorem on exact P3 and K4 chains")
    print("PASS: exact burst/complement formula and vertex reversibility")
    print(
        "PASS: actual mean bound on P3, regular K4, frozen n=6 split, and "
        f"{len(complementary_level_witnesses)} complementary-level witnesses"
    )


def audit_complete_root_polynomial():
    """Check tau(A) is proportional to n-|A| at the complete reference."""

    for n in (3, 4):
        complete = [
            [0 if i == j else 1 for j in range(n)]
            for i in range(n)
        ]
        states, q, _ = average_kernel(complete)
        cofactors = tree_cofactors(q)
        ratios = {
            cofactors[position] / (n - state.bit_count())
            for position, state in enumerate(states)
        }
        assert len(ratios) == 1
        z_at_one = sum(cofactors, F(0))
        z_prime_at_one = sum(
            (state.bit_count() * cofactors[position]
             for position, state in enumerate(states)),
            F(0),
        )
        assert z_prime_at_one / z_at_one == complete_mean(n)
    print("PASS: complete-reference tree root polynomial for n=3,4")


def screen(label, graphs):
    count = 0
    minimum = None
    for weights in graphs:
        if not connected(weights):
            continue
        mean, baseline = exact_mean_screen(weights)
        slack = baseline - mean
        assert slack >= 0, (label, weights, slack)
        if minimum is None or slack < minimum:
            minimum = slack
        count += 1
    assert count and minimum is not None
    minimum_text = "0" if minimum == 0 else f">0 (~{float(minimum):.12g})"
    print(f"PASS: {label}: {count} exact graphs; min(m_K-m)={minimum_text}")


def main():
    audit_first_treewise_failures()
    audit_labelled_history_lift_failure()
    audit_complete_root_polynomial()
    audit_markov_tree_theorem_and_frozen_graphs()
    screen("n=3 weights in {0,1,2,5}", exhaustive_graphs(3, (0, 1, 2, 5)))
    screen("n=4 weights in {0,1,2}", exhaustive_graphs(4, (0, 1, 2)))
    screen(
        "n=5 deterministic sparse/extreme",
        deterministic_graphs(5, 24, 26080808),
    )
    print("OPEN: universal fair-geometric arborescence root-rank inequality")


if __name__ == "__main__":
    main()
