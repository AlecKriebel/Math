#!/usr/bin/env python3
"""Exact verifier for three product-chain proof barriers at r=3/2.

The program independently constructs the Bd branching--coalescing dual and
the geometric-union dB dual from their atomic rules.  It then checks:

1. a five-atom Farkas obstruction to every radial/overlap product-chain
   Poisson potential on the unweighted three-path;
2. an exact weighted order-four failure of rank-sum stochastic domination;
3. an exact weighted order-four failure of the all-z coverage-product
   transform whose endpoint derivative is the fixation-product conjecture.

None of the examples violates the fixation-product conjecture itself.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


R = sp.Rational(3, 2)
Z = sp.symbols("z")


def subsets(mask: int):
    sub = mask
    while True:
        yield sub
        if sub == 0:
            return
        sub = (sub - 1) & mask


def finish_generator(matrix: sp.MutableDenseMatrix) -> sp.Matrix:
    for row in range(matrix.rows):
        matrix[row, row] = -sum(
            matrix[row, column]
            for column in range(matrix.cols)
            if column != row
        )
    return sp.Matrix(matrix)


def add_rate(matrix, row, column, rate):
    if row != column and rate:
        matrix[row, column] += rate


def geometric_union_law(row):
    """Law of the union of K iid row samples, K~Geom(success=2/3)."""
    support = sum(1 << i for i, value in enumerate(row) if value)
    # E[x^K]=2x/(3-x) at r=3/2.
    pgf = lambda x: 2 * sp.sympify(x) / (3 - sp.sympify(x))
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


def dual_generator(weights, rule):
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
        row = state - 1
        for target in range(n):
            if not ((state >> target) & 1):
                continue
            if rule == "Bd":
                for source in range(n):
                    rate = transition[source][target]
                    neutral = (state & ~(1 << target)) | (1 << source)
                    selective = state | (1 << source)
                    add_rate(matrix, row, neutral - 1, rate)
                    add_rate(matrix, row, selective - 1, (R - 1) * rate)
            elif rule == "dB":
                without_target = state & ~(1 << target)
                for source_set, probability in union_laws[target].items():
                    new_state = without_target | source_set
                    add_rate(matrix, row, new_state - 1, probability)
            else:
                raise ValueError(rule)
    return finish_generator(matrix)


def stationary(generator):
    matrix = generator.T.copy()
    rhs = sp.zeros(generator.rows, 1)
    for column in range(generator.cols):
        matrix[-1, column] = 1
    rhs[-1] = 1
    answer = list(matrix.inv() * rhs)
    assert all(value >= 0 for value in answer)
    assert sum(answer) == 1
    assert sp.Matrix(answer).T * generator == sp.zeros(1, generator.cols)
    return list(map(sp.cancel, answer))


def complete_rank_laws(n):
    a = R - 1
    z_bd = (1 + a) ** n - 1
    bd = [sp.Integer(0)] + [
        sp.binomial(n, k) * a**k / z_bd for k in range(1, n + 1)
    ]
    z_db = n * ((1 + a) ** (n - 1) - 1)
    db = [sp.Integer(0)] + [
        sp.binomial(n, k) * (n - k) * a**k / z_db
        for k in range(1, n + 1)
    ]
    assert sum(bd) == sum(db) == 1
    return bd, db


def rank_law(weights, rule):
    n = len(weights)
    invariant = stationary(dual_generator(weights, rule))
    answer = [sp.Integer(0)] * (n + 1)
    for state, mass in enumerate(invariant, start=1):
        answer[state.bit_count()] += mass
    assert sum(answer) == 1
    return list(map(sp.cancel, answer))


def pgf(law):
    return sum(mass * Z**rank for rank, mass in enumerate(law))


def mean(law):
    return sp.cancel(sum(rank * mass for rank, mass in enumerate(law)))


def verify_orbit_poisson_obstruction():
    # Vertices 0 and 1 are the leaves and vertex 2 is the center.
    weights = ((0, 0, 1), (0, 0, 1), (1, 1, 0))
    n = 3
    full = (1 << n) - 1
    bd = dual_generator(weights, "Bd")
    db_full = dual_generator(weights, "dB")
    # The full dB-dual state is transient and cannot be re-entered, so the
    # proper states form the recurrent generator used in the product chain.
    db = db_full.extract(range(full - 1), range(full - 1))
    assert all(sum(db.row(i)) == 0 for i in range(db.rows))

    complete_bd, complete_db = complete_rank_laws(n)
    m_bd = mean(complete_bd)
    m_db = mean(complete_db)
    assert m_bd == sp.Rational(27, 19)
    assert m_db == sp.Rational(6, 5)

    # A five-atom probability law Lambda on product states (A,B).
    atoms = {
        (0b001, 0b011): sp.Rational(133, 284),
        (0b011, 0b011): sp.Rational(77, 568),
        (0b100, 0b011): sp.Rational(361, 2272),
        (0b101, 0b011): sp.Rational(209, 1136),
        (0b111, 0b011): sp.Rational(121, 2272),
    }
    assert all(mass > 0 for mass in atoms.values())
    assert sum(atoms.values()) == 1

    a_states = list(range(1, full + 1))
    b_states = list(range(1, full))
    orbits = sorted(
        {
            (a.bit_count(), b.bit_count(), (a & b).bit_count())
            for a in a_states
            for b in b_states
        }
    )
    assert len(orbits) == 10

    # Lambda annihilates Q=LBd tensor I + I tensor DdB on every orbit
    # indicator, hence on every Psi(|A|,|B|,|A intersect B|).
    for orbit in orbits:
        expected_drift = 0
        for (a, b), mass in atoms.items():
            ai = a - 1
            bi = b - 1
            drift = sum(
                bd[ai, aj]
                * int(
                    (aa.bit_count(), b.bit_count(), (aa & b).bit_count())
                    == orbit
                )
                for aj, aa in enumerate(a_states)
            )
            drift += sum(
                db[bi, bj]
                * int(
                    (a.bit_count(), bb.bit_count(), (a & bb).bit_count())
                    == orbit
                )
                for bj, bb in enumerate(b_states)
            )
            expected_drift += mass * drift
        assert sp.cancel(expected_drift) == 0, (orbit, expected_drift)

    target_expectation = sum(
        mass
        * (
            sp.Rational(a.bit_count(), 1) / m_bd
            + sp.Rational(b.bit_count(), 1) / m_db
            - 2
        )
        for (a, b), mass in atoms.items()
    )
    assert sp.cancel(target_expectation - sp.Rational(571, 852)) == 0

    # The actual normalized arithmetic inequality is strict in the correct
    # direction on this graph.  Lambda is a separating pseudo-law, not the
    # stationary product law and not a fixation counterexample.
    actual_bd = rank_law(weights, "Bd")
    actual_db = rank_law(weights, "dB")
    normalized_slack = sp.cancel(
        2 - mean(actual_bd) / m_bd - mean(actual_db) / m_db
    )
    assert normalized_slack == sp.Rational(19, 504) > 0


def verify_rank_convolution_counterexample():
    weights = (
        (0, 7, 2, 3),
        (7, 0, 3, 0),
        (2, 3, 0, 7),
        (3, 0, 7, 0),
    )
    bd = rank_law(weights, "Bd")
    db = rank_law(weights, "dB")
    complete_bd, complete_db = complete_rank_laws(4)
    difference = sp.cancel(
        pgf(bd) * pgf(db) - pgf(complete_bd) * pgf(complete_db)
    )
    quotient = sp.cancel(difference / (Z**2 * (1 - Z)))
    assert sp.rem(
        sp.Poly(sp.together(difference).as_numer_denom()[0], Z),
        sp.Poly(Z**2 * (1 - Z), Z),
    ).is_zero
    constant = sp.cancel(quotient.subs(Z, 0))
    assert constant == -sp.Rational(
        6470085667377135548, 28216589762863303936875
    ) < 0
    # The endpoint derivative still has the conjectured sign.
    assert sp.cancel(quotient.subs(Z, 1)) > 0
    assert mean(bd) + mean(db) < mean(complete_bd) + mean(complete_db)


def verify_coverage_product_counterexample():
    weights = (
        (0, 0, 7, 0),
        (0, 0, 1, 7),
        (7, 1, 0, 1),
        (0, 7, 1, 0),
    )
    bd = rank_law(weights, "Bd")
    db = rank_law(weights, "dB")
    complete_bd, complete_db = complete_rank_laws(4)
    complete_coverage = (1 - pgf(complete_bd)) * (1 - pgf(complete_db))
    graph_coverage = (1 - pgf(bd)) * (1 - pgf(db))
    gap = sp.cancel(complete_coverage - graph_coverage)
    quotient = sp.cancel(gap / (Z * (1 - Z) ** 2))
    assert sp.rem(
        sp.Poly(sp.together(gap).as_numer_denom()[0], Z),
        sp.Poly(Z * (1 - Z) ** 2, Z),
    ).is_zero
    constant = sp.cancel(quotient.subs(Z, 0))
    assert constant == -sp.Rational(
        60733866936691239552155, 10628249467345628376063975
    ) < 0
    # At z=1 the quotient is exactly the finite fixation-product gap in
    # dual-mean units, and it is positive on this example.
    endpoint = sp.cancel(quotient.subs(Z, 1))
    product_gap = sp.cancel(
        mean(complete_bd) * mean(complete_db) - mean(bd) * mean(db)
    )
    assert endpoint == product_gap > 0


def main():
    verify_orbit_poisson_obstruction()
    verify_rank_convolution_counterexample()
    verify_coverage_product_counterexample()
    print("PASS: exact five-atom radial/overlap Poisson Farkas obstruction")
    print("PASS: exact order-four rank-convolution domination counterexample")
    print("PASS: exact order-four all-z coverage-product counterexample")
    print("PASS: every underlying fixation product remains below complete")


if __name__ == "__main__":
    main()
