#!/usr/bin/env python3
"""Exact Farkas barrier for a vertex-sensitive bilinear product potential.

At r=3/2, consider the product of the additive Bd dual and the
geometric-union dB dual.  Start with the sum of the exact complete-graph
radial Poisson solutions and allow the correction

    psi_C(A,B) = sum_{i,j} C_ij 1{i in A} 1{j in B},

with an arbitrary real 3 by 3 matrix C.  On one rational weighted path,
this script gives an exact nonnegative Farkas law proving that no C can make
the desired Poisson drift inequality hold at every product state.

This is a proof barrier, not a counterexample to the balanced fixation
inequality.  The graph itself satisfies that inequality strictly.
"""

from __future__ import annotations

import sympy as sp


R = sp.Rational(3, 2)


def subsets(mask: int):
    sub = mask
    while True:
        yield sub
        if sub == 0:
            return
        sub = (sub - 1) & mask


def add_rate(matrix: sp.MutableDenseMatrix, row: int, column: int, rate):
    if row != column and rate:
        matrix[row, column] += rate


def finish_generator(matrix: sp.MutableDenseMatrix) -> sp.Matrix:
    for row in range(matrix.rows):
        matrix[row, row] = -sum(
            matrix[row, column]
            for column in range(matrix.cols)
            if column != row
        )
    result = sp.Matrix(matrix)
    assert all(sum(result.row(row)) == 0 for row in range(result.rows))
    return result


def geometric_union_law(row):
    """Union of K iid row samples for K geometric with success 2/3."""
    support = sum(1 << i for i, value in enumerate(row) if value)
    # E[z^K] = 2z/(3-z).
    pgf = lambda z: 2 * sp.sympify(z) / (3 - sp.sympify(z))
    law = {}
    for target in subsets(support):
        if not target:
            continue
        probability = 0
        for included in subsets(target):
            mass = sum(
                (row[i] for i in range(len(row)) if (included >> i) & 1),
                sp.Integer(0),
            )
            probability += (-1) ** (
                target.bit_count() - included.bit_count()
            ) * pgf(mass)
        law[target] = sp.cancel(probability)
    assert sp.cancel(sum(law.values()) - 1) == 0
    assert all(value > 0 for value in law.values())
    return law


def dual_generator(weights, rule: str) -> sp.Matrix:
    """Derive the nonempty-set dual generator from the atomic rules."""
    n = len(weights)
    full = (1 << n) - 1
    states = list(range(1, full + 1))
    degree = [sum(map(sp.Rational, row)) for row in weights]
    transition = [
        [sp.Rational(weights[i][j]) / degree[i] for j in range(n)]
        for i in range(n)
    ]
    matrix = sp.zeros(full, full)
    union_laws = (
        [geometric_union_law(row) for row in transition]
        if rule == "dB"
        else None
    )
    for state in states:
        row_index = state - 1
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            if rule == "Bd":
                for source in range(n):
                    rate = transition[source][target]
                    neutral = (state & ~(1 << target)) | (1 << source)
                    selective = state | (1 << source)
                    add_rate(matrix, row_index, neutral - 1, rate)
                    add_rate(
                        matrix,
                        row_index,
                        selective - 1,
                        (R - 1) * rate,
                    )
            elif rule == "dB":
                assert union_laws is not None
                without_target = state & ~(1 << target)
                for source_set, probability in union_laws[target].items():
                    add_rate(
                        matrix,
                        row_index,
                        (without_target | source_set) - 1,
                        probability,
                    )
            else:
                raise ValueError(rule)
    return finish_generator(matrix)


def stationary(generator: sp.Matrix) -> list[sp.Expr]:
    matrix = generator.T.copy()
    rhs = sp.zeros(generator.rows, 1)
    for column in range(generator.cols):
        matrix[-1, column] = 1
    rhs[-1] = 1
    answer = list(matrix.inv() * rhs)
    assert all(value >= 0 for value in answer)
    assert sum(answer) == 1
    assert sp.Matrix(answer).T * generator == sp.zeros(1, generator.cols)
    return [sp.cancel(value) for value in answer]


def poisson(generator, invariant, target):
    """Solve Qf=target with invariant-mean-zero normalization."""
    assert sp.cancel(sum(p * g for p, g in zip(invariant, target))) == 0
    matrix = generator.copy()
    rhs = sp.Matrix(target)
    for column in range(matrix.cols):
        matrix[-1, column] = invariant[column]
    rhs[-1] = 0
    answer = list(matrix.inv() * rhs)
    return [sp.cancel(value) for value in answer]


def complete_baseline(n: int):
    weights = tuple(
        tuple(0 if i == j else 1 for j in range(n)) for i in range(n)
    )
    full = (1 << n) - 1
    bd = dual_generator(weights, "Bd")
    db_full = dual_generator(weights, "dB")
    pi_bd = stationary(bd)
    pi_db_full = stationary(db_full)
    mean_bd = sp.cancel(
        sum(pi_bd[state - 1] * state.bit_count() for state in range(1, full + 1))
    )
    mean_db = sp.cancel(
        sum(
            pi_db_full[state - 1] * state.bit_count()
            for state in range(1, full + 1)
        )
    )
    f_bd = poisson(
        bd,
        pi_bd,
        [sp.Integer(state.bit_count()) - mean_bd for state in range(1, full + 1)],
    )
    # The full dB-dual state is transient and has no incoming edge.  Its
    # recurrent proper-state block is the relevant Poisson chain.
    proper = list(range(1, full))
    db = db_full.extract(range(full - 1), range(full - 1))
    pi_db = pi_db_full[:-1]
    assert pi_db_full[-1] == 0
    f_db = poisson(
        db,
        pi_db,
        [sp.Integer(state.bit_count()) - mean_db for state in proper],
    )
    return mean_bd, mean_db, f_bd, f_db


def dual_mean(weights, rule: str) -> sp.Expr:
    n = len(weights)
    invariant = stationary(dual_generator(weights, rule))
    return sp.cancel(
        sum(
            invariant[state - 1] * state.bit_count()
            for state in range(1, 1 << n)
        )
    )


def verify_farkas_barrier():
    # Leaves 0 and 1 attach to center 2 with weights 1 and 17.
    weights = ((0, 0, 1), (0, 0, 17), (1, 17, 0))
    n = 3
    full = (1 << n) - 1
    a_states = list(range(1, full + 1))
    b_states = list(range(1, full))

    bd = dual_generator(weights, "Bd")
    db_full = dual_generator(weights, "dB")
    db = db_full.extract(range(full - 1), range(full - 1))
    mean_bd_k, mean_db_k, f_bd, f_db = complete_baseline(n)
    assert mean_bd_k == sp.Rational(27, 19)
    assert mean_db_k == sp.Rational(6, 5)

    # Seek Q_G(F_0 + psi_C) >= g, where
    # g=|A|/m_B+|B|/m_D-2 and F_0 is the sum of the complete radial
    # Poisson solutions divided by their complete dual means.  In standard
    # form this is A_ub vec(C) <= defect, with defect=Q_G F_0-g.
    rows = []
    defects = []
    pairs = []
    for ai, a in enumerate(a_states):
        indicator_a = [int((a >> i) & 1) for i in range(n)]
        drift_a = [
            sum(
                bd[ai, aj] * int((aa >> i) & 1)
                for aj, aa in enumerate(a_states)
            )
            for i in range(n)
        ]
        for bi, b in enumerate(b_states):
            indicator_b = [int((b >> j) & 1) for j in range(n)]
            drift_b = [
                sum(
                    db[bi, bj] * int((bb >> j) & 1)
                    for bj, bb in enumerate(b_states)
                )
                for j in range(n)
            ]
            correction_drift = [
                drift_a[i] * indicator_b[j]
                + indicator_a[i] * drift_b[j]
                for i in range(n)
                for j in range(n)
            ]
            target = (
                sp.Rational(a.bit_count(), 1) / mean_bd_k
                + sp.Rational(b.bit_count(), 1) / mean_db_k
                - 2
            )
            base_drift = sum(
                bd[ai, aj] * f_bd[aj] / mean_bd_k
                for aj in range(full)
            ) + sum(
                db[bi, bj] * f_db[bj] / mean_db_k
                for bj in range(full - 1)
            )
            rows.append([-value for value in correction_drift])
            defects.append(sp.cancel(base_drift - target))
            pairs.append((a, b))

    matrix = sp.Matrix(rows)
    rhs = sp.Matrix(defects)

    # Exact nonnegative Farkas law Lambda.  Its ten atoms annihilate every
    # one of the nine vertex-labelled bilinear correction columns.
    atoms = {
        (0b001, 0b011): sp.Rational(
            582284621889024156, 15163025068234244645
        ),
        (0b011, 0b010): sp.Rational(
            4361460837878293794, 15163025068234244645
        ),
        (0b011, 0b011): sp.Rational(
            479455448163476994, 15163025068234244645
        ),
        (0b011, 0b100): sp.Rational(
            5179944965981123466, 15163025068234244645
        ),
        (0b100, 0b010): sp.Rational(
            2639384150023151759, 45489075204702733935
        ),
        (0b100, 0b011): sp.Rational(
            1024557889515681802, 45489075204702733935
        ),
        (0b100, 0b100): sp.Rational(
            2530794517338006736, 45489075204702733935
        ),
        (0b101, 0b010): sp.Rational(
            512208588578716118, 45489075204702733935
        ),
        (0b101, 0b100): sp.Rational(
            2292008198046553793, 45489075204702733935
        ),
        (0b101, 0b110): sp.Rational(
            4680684239464868497, 45489075204702733935
        ),
    }
    assert all(mass > 0 for mass in atoms.values())
    dual = sp.Matrix([atoms.get(pair, 0) for pair in pairs])
    assert sum(dual) == 1
    assert dual.T * matrix == sp.zeros(1, n * n)
    expected_defect = sp.cancel((dual.T * rhs)[0])
    assert expected_defect == -sp.Rational(
        2914284766335459263489, 11053845274742764346205
    ) < 0

    # Farkas: if matrix*c <= rhs held, multiplying by dual would give
    # 0 <= expected_defect, contradicting the strict negative value above.

    # Confirm separately that this is only a proof obstruction.  Via the
    # exact stationary-dual identity rho(G)/rho(K)=m(G)/m(K), the graph has
    # a strictly positive balanced slack.
    graph_bd_mean = dual_mean(weights, "Bd")
    graph_db_mean = dual_mean(weights, "dB")
    normalized_slack = sp.cancel(
        2
        - graph_bd_mean / mean_bd_k
        - graph_db_mean / mean_db_k
    )
    assert graph_bd_mean == sp.Rational(30299, 26474)
    assert graph_db_mean == sp.Rational(6053, 5883)
    assert normalized_slack == sp.Rational(236336950, 700859439) > 0

    return expected_defect, normalized_slack


def main():
    defect, slack = verify_farkas_barrier()
    print("PASS: exact ten-atom vertex-bilinear Farkas obstruction")
    print(f"Farkas expected defect = {defect}")
    print(f"graph balanced slack = {slack}")
    print("PASS: the witness is a proof barrier, not a fixation counterexample")


if __name__ == "__main__":
    main()
