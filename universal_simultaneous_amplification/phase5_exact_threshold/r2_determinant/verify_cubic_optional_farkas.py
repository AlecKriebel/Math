#!/usr/bin/env python3
"""Exact Farkas refutation of the cubic optional-potential lemma.

The witness is the seven-vertex complete-support undirected weighted graph
with two vertex classes of sizes two and five and edge weights

    w_AA=10000,  w_BB=100,  w_AB=1.

The script independently builds the fitness-two dB drift columns over
``Fraction`` arithmetic, checks the full labelled system against its
``S_2 x S_5`` quotient, verifies a sparse integer Farkas ray proving that
degree at most three is infeasible, and verifies an exact strict degree-four
potential on the same graph.  The degree-four calculation is a witness
computation, not a universal theorem.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
from math import comb


N_VERTICES = 7
A_VERTICES = (0, 1)
B_VERTICES = (2, 3, 4, 5, 6)

DEGREE_THREE_TYPES = (
    (1, 0), (0, 1),
    (2, 0), (1, 1), (0, 2),
    (2, 1), (1, 2), (0, 3),
)

DEGREE_FOUR_TYPES = (
    (0, 1), (1, 0),
    (0, 2), (1, 1), (2, 0),
    (0, 3), (1, 2), (2, 1),
    (0, 4), (1, 3), (2, 2),
)


def choose(n: int, k: int) -> int:
    return comb(n, k) if 0 <= k <= n else 0


def graph_weights() -> list[list[Q]]:
    weights = [[Q(0) for _ in range(N_VERTICES)] for _ in range(N_VERTICES)]
    for i, j in combinations(range(N_VERTICES), 2):
        if i in A_VERTICES and j in A_VERTICES:
            value = Q(10000)
        elif i in B_VERTICES and j in B_VERTICES:
            value = Q(100)
        else:
            value = Q(1)
        weights[i][j] = weights[j][i] = value
    return weights


def replacement_kernel(weights: list[list[Q]]) -> list[list[Q]]:
    answer = []
    for row in weights:
        degree = sum(row, Q(0))
        assert degree > 0
        normalized = [value / degree for value in row]
        assert sum(normalized, Q(0)) == 1
        answer.append(normalized)
    return answer


def labelled_rates(
    mask: int,
    replacement: list[list[Q]],
) -> tuple[list[Q], list[Q], Q]:
    """Return add rates g, removal rates ell, and constant drift column."""

    inside = [bool((mask >> vertex) & 1) for vertex in range(N_VERTICES)]
    x = [
        sum(
            (replacement[vertex][target] for target in range(N_VERTICES)
             if inside[target]),
            Q(0),
        )
        for vertex in range(N_VERTICES)
    ]
    gain = [Q(2) * value / (1 + value) for value in x]
    loss = [(1 - value) / (1 + value) for value in x]
    constant = -sum(
        (gain[vertex] for vertex in range(N_VERTICES) if not inside[vertex]),
        Q(0),
    ) + Q(2) * sum(
        (loss[vertex] for vertex in range(N_VERTICES) if inside[vertex]),
        Q(0),
    )
    return gain, loss, constant


def monomial_drift_column(
    mask: int,
    subset: tuple[int, ...],
    gain: list[Q],
    loss: list[Q],
    constant: Q,
) -> Q:
    missing = [vertex for vertex in subset if not ((mask >> vertex) & 1)]
    if not missing:
        return constant - Q(4) * sum((loss[vertex] for vertex in subset), Q(0))
    if len(missing) == 1:
        return gain[missing[0]]
    return Q(0)


def orbit_states() -> list[tuple[int, int]]:
    return [
        (a_count, b_count)
        for a_count in range(3)
        for b_count in range(6)
        if (a_count, b_count) not in ((0, 0), (2, 5))
    ]


def orbit_rates(a_count: int, b_count: int) -> tuple[Q, Q, Q, Q, Q]:
    """Return g_A,g_B,ell_A,ell_B,d on one state orbit."""

    if a_count < 2:
        x_a_out = Q(10000 * a_count + b_count, 10005)
        gain_a = Q(2) * x_a_out / (1 + x_a_out)
    else:
        gain_a = Q(0)
    if b_count < 5:
        x_b_out = Q(100 * b_count + a_count, 402)
        gain_b = Q(2) * x_b_out / (1 + x_b_out)
    else:
        gain_b = Q(0)

    if a_count:
        x_a_in = Q(10000 * (a_count - 1) + b_count, 10005)
        loss_a = (1 - x_a_in) / (1 + x_a_in)
    else:
        loss_a = Q(0)
    if b_count:
        x_b_in = Q(100 * (b_count - 1) + a_count, 402)
        loss_b = (1 - x_b_in) / (1 + x_b_in)
    else:
        loss_b = Q(0)

    constant = (
        -(2 - a_count) * gain_a
        -(5 - b_count) * gain_b
        +2 * a_count * loss_a
        +2 * b_count * loss_b
    )
    return gain_a, gain_b, loss_a, loss_b, constant


def reduced_system(
    types: tuple[tuple[int, int], ...],
) -> tuple[list[tuple[int, int]], list[list[Q]], list[Q], list[list[Q]]]:
    states = orbit_states()
    rows: list[list[Q]] = []
    constants: list[Q] = []
    for a_count, b_count in states:
        gain_a, gain_b, loss_a, loss_b, constant = orbit_rates(a_count, b_count)
        row = []
        for a_order, b_order in types:
            contained = choose(a_count, a_order) * choose(b_count, b_order)
            value = contained * (
                constant - 4 * (a_order * loss_a + b_order * loss_b)
            )
            value += (
                (2 - a_count)
                * choose(a_count, a_order - 1)
                * choose(b_count, b_order)
                * gain_a
            )
            value += (
                (5 - b_count)
                * choose(a_count, a_order)
                * choose(b_count, b_order - 1)
                * gain_b
            )
            row.append(value)
        rows.append(row)
        constants.append(constant)

    singleton = [
        Q(choose(2, a_order) * choose(5, b_order))
        if a_order + b_order == 1 else Q(0)
        for a_order, b_order in types
    ]
    higher = [
        Q(choose(2, a_order) * choose(5, b_order))
        if a_order + b_order >= 2 else Q(0)
        for a_order, b_order in types
    ]
    return states, rows, constants, [singleton, higher]


def general_two_class_system(
    a_size: int,
    b_size: int,
    within_a: int,
    within_b: int,
    types: tuple[tuple[int, int], ...],
) -> tuple[list[tuple[int, int]], list[list[Q]], list[Q], list[list[Q]]]:
    """Exact quotient for arbitrary complete-support two-class weights."""

    degree_a = (a_size - 1) * within_a + b_size
    degree_b = (b_size - 1) * within_b + a_size
    states = [
        (a_count, b_count)
        for a_count in range(a_size + 1)
        for b_count in range(b_size + 1)
        if (a_count, b_count) not in ((0, 0), (a_size, b_size))
    ]
    rows: list[list[Q]] = []
    constants: list[Q] = []
    for a_count, b_count in states:
        if a_count < a_size:
            x = Q(within_a * a_count + b_count, degree_a)
            gain_a = 2 * x / (1 + x)
        else:
            gain_a = Q(0)
        if b_count < b_size:
            x = Q(within_b * b_count + a_count, degree_b)
            gain_b = 2 * x / (1 + x)
        else:
            gain_b = Q(0)
        if a_count:
            x = Q(within_a * (a_count - 1) + b_count, degree_a)
            loss_a = (1 - x) / (1 + x)
        else:
            loss_a = Q(0)
        if b_count:
            x = Q(within_b * (b_count - 1) + a_count, degree_b)
            loss_b = (1 - x) / (1 + x)
        else:
            loss_b = Q(0)

        constant = (
            -(a_size - a_count) * gain_a
            -(b_size - b_count) * gain_b
            +2 * a_count * loss_a
            +2 * b_count * loss_b
        )
        row = []
        for a_order, b_order in types:
            value = choose(a_count, a_order) * choose(b_count, b_order) * (
                constant - 4 * (a_order * loss_a + b_order * loss_b)
            )
            value += (
                (a_size - a_count)
                * choose(a_count, a_order - 1)
                * choose(b_count, b_order)
                * gain_a
            )
            value += (
                (b_size - b_count)
                * choose(a_count, a_order)
                * choose(b_count, b_order - 1)
                * gain_b
            )
            row.append(value)
        rows.append(row)
        constants.append(constant)

    singleton = [
        Q(choose(a_size, a_order) * choose(b_size, b_order))
        if a_order + b_order == 1 else Q(0)
        for a_order, b_order in types
    ]
    higher = [
        Q(choose(a_size, a_order) * choose(b_size, b_order))
        if a_order + b_order >= 2 else Q(0)
        for a_order, b_order in types
    ]
    return states, rows, constants, [singleton, higher]


def full_to_reduced_audit() -> None:
    """Match every labelled degree-three row to the orbit formulas."""

    replacement = replacement_kernel(graph_weights())
    states, rows, constants, _equalities = reduced_system(DEGREE_THREE_TYPES)
    orbit_index = {state: position for position, state in enumerate(states)}
    subsets_by_type = {
        orbit_type: [
            subset
            for subset in combinations(range(N_VERTICES), sum(orbit_type))
            if (
                sum(vertex in A_VERTICES for vertex in subset),
                sum(vertex in B_VERTICES for vertex in subset),
            ) == orbit_type
        ]
        for orbit_type in DEGREE_THREE_TYPES
    }

    for mask in range(1, (1 << N_VERTICES) - 1):
        a_count = sum((mask >> vertex) & 1 for vertex in A_VERTICES)
        b_count = sum((mask >> vertex) & 1 for vertex in B_VERTICES)
        row_index = orbit_index[(a_count, b_count)]
        gain, loss, constant = labelled_rates(mask, replacement)
        assert constant == constants[row_index]
        aggregate = []
        for orbit_type in DEGREE_THREE_TYPES:
            aggregate.append(sum(
                (
                    monomial_drift_column(
                        mask, subset, gain, loss, constant
                    )
                    for subset in subsets_by_type[orbit_type]
                ),
                Q(0),
            ))
        assert aggregate == rows[row_index]


def cubic_farkas_certificate() -> None:
    """Verify a sparse exact dual ray proving cubic infeasibility."""

    states, rows, constants, equalities = reduced_system(DEGREE_THREE_TYPES)
    weights = {
        (0, 1): 540627933005591230440428186696715600,
        (0, 4): 429319667664502797137297911715830905,
        (1, 0): 137468247559120961049408712647905728,
        (1, 1): 1134179440520231288656990994323140,
        (2, 0): 4237612806797289633945417624252880740,
        (2, 1): 91732144491776328233927490827063760,
        (2, 4): 171180400691387791097268387428693360,
    }
    z_singleton = -292949884113599470025054765354884048
    z_higher = -19087225856145491530878236546713200
    assert all(value > 0 for value in weights.values())

    for column in range(len(DEGREE_THREE_TYPES)):
        balance = -sum(
            (
                Q(weights.get(state, 0)) * rows[position][column]
                for position, state in enumerate(states)
            ),
            Q(0),
        )
        balance += z_singleton * equalities[0][column]
        balance += z_higher * equalities[1][column]
        assert balance == 0

    objective = sum(
        (
            Q(weights.get(state, 0)) * constants[position]
            for position, state in enumerate(states)
        ),
        Q(0),
    ) + z_singleton
    expected = Q(-16671847733465987326305780396702792)
    assert objective == expected < 0


DEGREE_FOUR_COEFFICIENTS = (
    Q(
        2891703962896880034693027658221919350324688643,
        11189871811342308523548170110283043944090672885,
    ),
    Q(
        -326864800314209164991696818082655280753277033,
        2237974362268461704709634022056608788818134577,
    ),
    Q(
        965387209988645578150347838178176187545850043,
        11189871811342308523548170110283043944090672885,
    ),
    Q(
        -1339429980855978668957543081865360495793726983,
        11189871811342308523548170110283043944090672885,
    ),
    Q(
        -2794139538187679483270286730618014118850138658,
        2237974362268461704709634022056608788818134577,
    ),
    Q(
        7439749098131722155917387568776096629711976523,
        89518974490738468188385360882264351552725383080,
    ),
    Q(
        8371573984015194557008060375877542164593079009,
        89518974490738468188385360882264351552725383080,
    ),
    Q(
        -800964878413211274508413046018503834948263172,
        11189871811342308523548170110283043944090672885,
    ),
    Q(
        448368964235667205262941877427834733224964503,
        3443037480413018007245590803164013521258668580,
    ),
    Q(
        2720132220190871451465497964767643046602608241,
        89518974490738468188385360882264351552725383080,
    ),
    Q(
        -9039599104132650041855193800292386151425633361,
        44759487245369234094192680441132175776362691540,
    ),
)

DEGREE_FOUR_MARGIN = Q(
    59103658221160944397237122483432978029271180,
    2237974362268461704709634022056608788818134577,
)


def degree_four_certificate() -> None:
    """Verify an exact strict quartic potential on the cubic witness."""

    states, rows, constants, equalities = reduced_system(DEGREE_FOUR_TYPES)
    coefficients = DEGREE_FOUR_COEFFICIENTS
    assert sum(
        (left * right for left, right in zip(equalities[0], coefficients)),
        Q(0),
    ) == 1
    assert sum(
        (left * right for left, right in zip(equalities[1], coefficients)),
        Q(0),
    ) == 0

    reduced_drifts = [
        constant + sum(
            (entry * coefficient for entry, coefficient in zip(row, coefficients)),
            Q(0),
        )
        for row, constant in zip(rows, constants)
    ]
    assert min(reduced_drifts) == DEGREE_FOUR_MARGIN > 0

    # Check the quotient drift against direct fitness-two dB expectation of
    # F(S)=2^(-|S|)G(S) on every labelled transient state.
    replacement = replacement_kernel(graph_weights())

    def g_value(mask: int) -> Q:
        a_count = sum((mask >> vertex) & 1 for vertex in A_VERTICES)
        b_count = sum((mask >> vertex) & 1 for vertex in B_VERTICES)
        return 1 + sum(
            (
                coefficient
                * choose(a_count, a_order)
                * choose(b_count, b_order)
                for (a_order, b_order), coefficient in zip(
                    DEGREE_FOUR_TYPES, coefficients
                )
            ),
            Q(0),
        )

    assert g_value(0) == 1
    assert g_value((1 << N_VERTICES) - 1) == 2
    assert sum((g_value(1 << vertex) for vertex in range(N_VERTICES)), Q(0)) == 8

    orbit_index = {state: position for position, state in enumerate(states)}
    for mask in range(1, (1 << N_VERTICES) - 1):
        rank = mask.bit_count()
        current = g_value(mask) / 2**rank
        expected_change = Q(0)
        gain, loss, _constant = labelled_rates(mask, replacement)
        for vertex in range(N_VERTICES):
            if (mask >> vertex) & 1:
                next_value = g_value(mask & ~(1 << vertex)) / 2 ** (rank - 1)
                expected_change += loss[vertex] * (next_value - current) / N_VERTICES
            else:
                next_value = g_value(mask | (1 << vertex)) / 2 ** (rank + 1)
                expected_change += gain[vertex] * (next_value - current) / N_VERTICES

        a_count = sum((mask >> vertex) & 1 for vertex in A_VERTICES)
        b_count = sum((mask >> vertex) & 1 for vertex in B_VERTICES)
        reduced = reduced_drifts[orbit_index[(a_count, b_count)]]
        assert expected_change == reduced / (N_VERTICES * 2 ** (rank + 1))
        assert expected_change > 0


def quartic_farkas_certificate() -> None:
    """Verify that degree four also fails on a larger two-class graph."""

    states, rows, constants, equalities = general_two_class_system(
        2, 8, 10000, 100, DEGREE_FOUR_TYPES
    )
    support = (
        (0, 1), (0, 2), (0, 7),
        (1, 0), (1, 2), (1, 6),
        (2, 0), (2, 1), (2, 2), (2, 7),
    )
    ray = (
        8649656205914429056200358981027370036772950218815842747619353592,
        9258872961634584383270662928713494855565187454892989057125040908,
        2865347419127689628745970223264245320536157336871244994209855576,
        2765556040034306779671952620615324909717168557679356334209506446,
        8606103461872791872154597821555801637319982368380285718701353,
        2598302466332915478097511176399399118396985955557141633216049,
        89416839773950564464082291322756766590833007388877343460170969854,
        1226657918429851187393801208218592230166740419440012693861572872,
        1267834151946865357153109970028494013023108399210690134492518980,
        3742282920328279022413459964065662511585859841741639869221134372,
    )
    z_singleton = (
        -5940417125220043859384538275707641233799292450031367755309242704
    )
    z_higher = (
        -514564835860806903622088674268257413545438411398266952640826096
    )
    weights = dict(zip(support, ray))
    assert all(value > 0 for value in ray)

    for column in range(len(DEGREE_FOUR_TYPES)):
        balance = -sum(
            (
                Q(weights.get(state, 0)) * rows[position][column]
                for position, state in enumerate(states)
            ),
            Q(0),
        )
        balance += z_singleton * equalities[0][column]
        balance += z_higher * equalities[1][column]
        assert balance == 0

    objective = sum(
        (
            Q(weights.get(state, 0)) * constants[position]
            for position, state in enumerate(states)
        ),
        Q(0),
    ) + z_singleton
    expected = Q(
        -591738467543996669461667803880418671550252755178182911237183584
    )
    assert objective == expected < 0


def main() -> None:
    full_to_reduced_audit()
    cubic_farkas_certificate()
    degree_four_certificate()
    quartic_farkas_certificate()
    print("PASS: full labelled degree-three rows match the S2 x S5 quotient")
    print("EXACTLY REFUTED: cubic optional-potential lemma")
    print("FARKAS OBJECTIVE: -16671847733465987326305780396702792")
    print("PASS: exact strict degree-four potential on the same graph")
    print("EXACTLY REFUTED: quartic optional-potential lemma on order ten")
    print("OPEN: no universal bounded-degree optional-potential theorem follows")


if __name__ == "__main__":
    main()
