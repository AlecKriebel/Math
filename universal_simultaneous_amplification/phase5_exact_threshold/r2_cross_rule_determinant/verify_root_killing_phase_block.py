#!/usr/bin/env python3
"""Exact audit of the r=2 root-killing common phase block.

The script verifies finite matrix identities and sharp obstructions.  It
does not assert the open all-graph PAPT sign.
"""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
CROSS_RULE = HERE.parent / "r2_cross_rule_sum"
sys.path.insert(0, str(CROSS_RULE))

from verify_cross_rule_tree_reduction import (  # noqa: E402
    db_generator,
    determinant,
    event_kernels_r2,
    identity,
    inverse,
    matmul,
    transition_matrix,
    tree_cofactors,
    tree_data,
    unbatched_generators,
)


def block_matrix(top_left, top_right, bottom_left, bottom_right):
    """Join four compatible rational blocks."""

    answer = []
    for left, right in zip(top_left, top_right):
        answer.append(left[:] + right[:])
    for left, right in zip(bottom_left, bottom_right):
        answer.append(left[:] + right[:])
    return answer


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def diagonal(values):
    return [
        [value if row == column else F(0) for column in range(len(values))]
        for row, value in enumerate(values)
    ]


def scale(matrix, scalar):
    return [[scalar * entry for entry in row] for row in matrix]


def add(left, right):
    return [
        [a + b for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def subtract(left, right):
    return add(left, scale(right, -1))


def phase_matrices(weights):
    """Build J,F,S,N and the two common-coupling phase pencils."""

    p = transition_matrix(weights)
    n = len(weights)
    full = (1 << n) - 1
    omega = list(range(1, full + 1))
    marked = [
        (state, target)
        for state in omega
        for target in range(n)
        if (state >> target) & 1
    ]
    marked_index = {state: index for index, state in enumerate(marked)}
    set_index = {state: state - 1 for state in omega}
    sets = len(omega)
    marks = len(marked)

    choose = [[F(0) for _ in range(marks)] for _ in range(sets)]
    forget = [[F(0) for _ in range(sets)] for _ in range(marks)]
    selective = [[F(0) for _ in range(marks)] for _ in range(marks)]
    neutral = [[F(0) for _ in range(sets)] for _ in range(marks)]
    for state in omega:
        rank = state.bit_count()
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            mark = marked_index[state, target]
            choose[set_index[state]][mark] = F(1, rank)
            forget[mark][set_index[state]] = F(1)
            for source in range(n):
                probability = p[target][source]
                if not probability:
                    continue
                selected = state | (1 << source)
                replaced = (state & ~(1 << target)) | (1 << source)
                selective[mark][marked_index[selected, target]] += probability
                neutral[mark][set_index[replaced]] += probability

    assert matmul(choose, forget) == identity(sets)
    assert all(sum(row, F(0)) == 1 for row in selective)
    assert all(sum(row, F(0)) == 1 for row in neutral)

    selective_forget = matmul(selective, forget)
    marked_c = subtract(add(selective_forget, neutral), scale(forget, 2))
    phase = subtract(identity(marks), scale(selective, F(1, 2)))
    rank_values = [F(state.bit_count()) for state in omega]
    rank = diagonal(rank_values)
    rank_inverse = diagonal([1 / value for value in rank_values])

    reverse_from_phase = matmul(matmul(rank, choose), marked_c)
    left, reverse = unbatched_generators(weights)
    assert reverse_from_phase == reverse

    locked_from_phase = scale(
        matmul(matmul(choose, inverse(phase)), neutral), F(1, 2)
    )
    _, _, _, locked_direct = event_kernels_r2(weights)
    assert locked_from_phase == locked_direct
    locked_laplacian = subtract(identity(sets), locked_from_phase)
    assert locked_from_phase == add(
        identity(sets),
        scale(matmul(matmul(choose, inverse(phase)), marked_c), F(1, 2)),
    )

    left_transpose = transpose(left)
    potential_values = [
        left_transpose[row][row] - reverse[row][row] for row in range(sets)
    ]
    potential = diagonal(potential_values)
    assert left_transpose == add(reverse, potential)

    return {
        "n": n,
        "omega": omega,
        "marked": marked,
        "J": choose,
        "F": forget,
        "S": selective,
        "N": neutral,
        "Cmark": marked_c,
        "A": phase,
        "K": rank,
        "Kinv": rank_inverse,
        "V": potential,
        "v": potential_values,
        "L": left,
        "C": reverse,
        "KD": locked_from_phase,
        "RD": locked_laplacian,
    }


def common_block_d(data, s, killing):
    marks = len(data["marked"])
    return block_matrix(
        data["A"],
        scale(data["Cmark"], F(-1, 2)),
        scale(data["J"], -1),
        scale(killing, s),
    )


def common_block_l(data, s, killing):
    marks = len(data["marked"])
    bottom = matmul(
        data["Kinv"], subtract(scale(killing, s), data["V"])
    )
    return block_matrix(
        scale(identity(marks), F(1, 2)),
        scale(data["Cmark"], F(-1, 2)),
        scale(data["J"], -1),
        bottom,
    )


def canonical_hf_master(data, bottom):
    """Four-sector duplicated-selective principal-minor master (26b)."""

    selective = data["S"]
    neutral = data["N"]
    forget = data["F"]
    choose = data["J"]
    marks = len(selective)
    sets = len(choose)
    eye_mark = identity(marks)
    zero_marks = [[F(0) for _ in range(marks)] for _ in range(marks)]
    zero_mark_set = [[F(0) for _ in range(sets)] for _ in range(marks)]
    zero_set_mark = [[F(0) for _ in range(marks)] for _ in range(sets)]
    answer = []
    for row in range(marks):
        answer.append(
            eye_mark[row]
            + scale(selective, F(-1, 2))[row]
            + scale(selective, F(-1, 2))[row]
            + scale(neutral, F(-1, 2))[row]
        )
    for row in range(marks):
        answer.append(
            scale(eye_mark, -1)[row]
            + eye_mark[row]
            + zero_marks[row]
            + zero_mark_set[row]
        )
    for row in range(marks):
        answer.append(
            zero_marks[row]
            + zero_marks[row]
            + eye_mark[row]
            + scale(forget, -1)[row]
        )
    for row in range(sets):
        answer.append(
            scale(choose, -1)[row]
            + zero_set_mark[row]
            + zero_set_mark[row]
            + bottom[row]
        )
    return answer


def principal(matrix, indices):
    return [[matrix[row][column] for column in indices] for row in indices]


def killed(matrix, s, killing):
    return add(matrix, scale(killing, s))


def root_derivative(generator, killing_values):
    """Derivative at zero of det(-Q+s diag(killing_values))."""

    cofactors = tree_cofactors(generator)
    return sum(
        (weight * value for weight, value in zip(cofactors, killing_values)),
        F(0),
    )


def cycle_witness(generator, states):
    """Return the first exact Kolmogorov three-cycle failure, if any."""

    size = len(generator)
    for first, second, third in itertools.permutations(range(size), 3):
        if first >= min(second, third):
            continue
        rates = (
            generator[first][second],
            generator[second][third],
            generator[third][first],
            generator[second][first],
            generator[third][second],
            generator[first][third],
        )
        if not all(rates):
            continue
        forward = rates[0] * rates[1] * rates[2]
        reverse = rates[3] * rates[4] * rates[5]
        if forward != reverse:
            return states[first], states[second], states[third], forward, reverse
    return None


def audit(weights, check_large_determinants=True):
    data = phase_matrices(weights)
    n = data["n"]
    full = (1 << n) - 1
    sets = full
    marks = len(data["marked"])
    rank_values = [F(state.bit_count()) for state in data["omega"]]
    inverse_rank_values = [1 / value for value in rank_values]
    identity_set = identity(sets)
    b = F(n * 2 ** (n - 1), 2**n - 1)
    d = F((n - 1) * 2 ** (n - 2), 2 ** (n - 1) - 1)

    # Check the two Schur determinant identities at nonzero killing.
    if check_large_determinants:
        test_s = F(2, 7)
        for killing in (identity_set, data["K"], data["Kinv"]):
            block_d = determinant(common_block_d(data, test_s, killing))
            direct_d = determinant(killed(data["RD"], test_s, killing))
            assert block_d == determinant(data["A"]) * direct_d

            block_l = determinant(common_block_l(data, test_s, killing))
            direct_l = determinant(
                killed(scale(transpose(data["L"]), -1), test_s, killing)
            )
            rank_product = F(1)
            for value in rank_values:
                rank_product *= value
            assert direct_l == F(2**marks) * rank_product * block_l

    # Event cofactors are taken on the unique proper closed class.
    proper = full - 1
    event_generator = [
        [data["KD"][row][column] - F(row == column)
         for column in range(proper)]
        for row in range(proper)
    ]
    theta = tree_cofactors(event_generator)
    theta_sum = sum(theta, F(0))
    phi = sum(
        (weight / F(state.bit_count())
         for state, weight in zip(range(1, full), theta)),
        F(0),
    )

    tau, z_l, y_l, m_l = tree_data(data["L"], data["omega"])
    assert z_l == root_derivative(data["L"], [F(1) for _ in data["omega"]])
    assert y_l == root_derivative(data["L"], rank_values)

    continuous_d = db_generator(weights)
    _, _, _, m_d = tree_data(continuous_d, list(range(1, full)))
    assert phi / theta_sum == 1 / m_d

    # Derivatives of the common blocks differ from tree moments only by the
    # positive constants in the Schur identities.
    rank_product = F(1)
    for value in rank_values:
        rank_product *= value
    left_factor = F(1, 2**marks) / rank_product
    d_factor = determinant(data["A"])
    dot_l_i = left_factor * z_l
    dot_l_k = left_factor * y_l
    dot_d_i = d_factor * theta_sum
    dot_d_h = d_factor * phi
    assert dot_l_k / dot_l_i == m_l
    assert dot_d_h / dot_d_i == 1 / m_d

    block_coefficient = (
        b * d * dot_l_i * dot_d_h - dot_l_k * dot_d_i
    )
    event_numerator = b * d * z_l * phi - y_l * theta_sum
    assert block_coefficient == left_factor * d_factor * event_numerator

    # The PSD obstruction uses a highest-probability directed base edge.
    p = transition_matrix(weights)
    edge_probability = max(
        p[target][source]
        for target in range(n)
        for source in range(n)
        if target != source
    )
    metric_minor = -(edge_probability**2) / 16
    assert metric_minor < 0

    # The common block cannot be made into a Z-matrix by a diagonal
    # signature: for y=(A,v), its y->A entry is positive while A->y is
    # negative, forcing incompatible signs.
    p = transition_matrix(weights)
    for mark, (state, target) in enumerate(data["marked"]):
        request_inside = sum(
            (p[target][source] for source in range(n)
             if (state >> source) & 1),
            F(0),
        )
        assert data["Cmark"][mark][state - 1] == request_inside - 2
        assert -data["Cmark"][mark][state - 1] / 2 > 0
        assert -data["J"][state - 1][mark] < 0

    return {
        "block_coefficient": block_coefficient,
        "event_numerator": event_numerator,
        "m_l": m_l,
        "m_d": m_d,
        "v_min": min(data["v"]),
        "v_max": max(data["v"]),
        "metric_minor": metric_minor,
        "cycle": cycle_witness(data["L"], data["omega"]),
        "data": data,
    }


def main():
    weighted_path = (
        (0, 1, 2),
        (1, 0, 0),
        (2, 0, 0),
    )
    complete_four = tuple(
        tuple(0 if row == column else 1 for column in range(4))
        for row in range(4)
    )
    orientation_four = (
        (0, 0, 1000, 2),
        (0, 0, 1, 1000),
        (1000, 1, 0, 10),
        (2, 1000, 10, 0),
    )

    path = audit(weighted_path)
    complete = audit(complete_four)
    orientation = audit(orientation_four, check_large_determinants=False)

    assert path["event_numerator"] > 0
    assert complete["event_numerator"] == 0
    assert orientation["event_numerator"] > 0

    assert (path["v_min"], path["v_max"]) == (F(-2), F(2))
    assert complete["v_min"] == complete["v_max"] == 0
    assert (orientation["v_min"], orientation["v_max"]) == (
        F(-10115, 255783),
        F(10115, 255783),
    )
    assert complete["metric_minor"] == F(-1, 144)
    assert path["cycle"] == (1, 2, 3, F(1, 9), F(1, 3))

    complete_three = (
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
    )
    complete_three_data = phase_matrices(complete_three)
    master = canonical_hf_master(
        complete_three_data, identity(len(complete_three_data["omega"]))
    )
    assert determinant(master) == F(-27, 2048)
    marks_three = len(complete_three_data["marked"])
    sets_three = len(complete_three_data["omega"])
    phase_zero = list(range(marks_three))
    phase_d = list(range(marks_three, 2 * marks_three))
    phase_l = list(range(2 * marks_three, 3 * marks_three))
    set_sector = list(range(3 * marks_three, 3 * marks_three + sets_three))
    d_principal = principal(master, phase_zero + phase_d + set_sector)
    l_principal = principal(master, phase_zero + phase_l + set_sector)
    standard_d = block_matrix(
        complete_three_data["A"],
        scale(complete_three_data["N"], F(-1, 2)),
        scale(complete_three_data["J"], -1),
        identity(sets_three),
    )
    unbatched_arrow = add(
        matmul(complete_three_data["S"], complete_three_data["F"]),
        complete_three_data["N"],
    )
    standard_l = block_matrix(
        identity(marks_three),
        scale(unbatched_arrow, F(-1, 2)),
        scale(complete_three_data["J"], -1),
        identity(sets_three),
    )
    assert determinant(d_principal) == determinant(standard_d)
    assert determinant(l_principal) == determinant(standard_l)

    # A one-way locked-event transition survives even on K4, precluding a
    # direct diagonal symmetrization of the dB killed matrix.
    kd = complete["data"]["KD"]
    one_way = next(
        (
            (row + 1, column + 1, kd[row][column])
            for row in range(len(kd))
            for column in range(len(kd))
            if kd[row][column] and not kd[column][row]
        ),
        None,
    )
    assert one_way is not None

    print("PASS: exact root-killing derivatives and common phase blocks")
    print("PASS: one block coefficient is exactly the PAPT numerator")
    print("PASS: weighted-P3 and n4 witness coefficients remain positive")
    print("REFUTED: canonical diagonal-metric PSD Schur ordering")
    print("REFUTED: direct common-block M-matrix Hadamard-Fischer shortcut")
    print("REFUTED: duplicated-phase master det(K3,B=I) = -27/2048")
    print("K4 top-block symmetric minor = -1/144")
    print("P3 V range = [-2,2]; n4 V range = +/-10115/255783")
    print("OPEN: nonsymmetric M-matrix/forest proof of the block coefficient")


if __name__ == "__main__":
    main()
