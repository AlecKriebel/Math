#!/usr/bin/env python3
"""Independent exact audit of the endpoint clique--pendant product witness.

The graph G(c,m) consists of a clique on H,C_1,...,C_c and m leaves,
each adjacent only to H.  All edges have weight one.  The quotient state is
(h,i,j), where h is the type of H and i,j are the mutant counts among the C
vertices and leaves.  Nothing in this file imports a fixation implementation
from the discovery search.
"""

from __future__ import annotations

import argparse
import hashlib
from fractions import Fraction
from itertools import combinations

import numpy as np
from flint import fmpq, fmpq_mat
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.linalg import spsolve


Q = fmpq


def _add(row, target, probability):
    if probability:
        row[target] = row.get(target, Q(0)) + probability


def quotient_changes(c: int, m: int, r, rule: str, state):
    """Return all type-changing probabilities from one quotient state."""
    h, i, j = state
    n = c + m + 1
    row = {}
    if rule == "Bd":
        total_fitness = Q(n) + (r - 1) * (h + i + j)

        # An ordinary clique vertex changes type.
        if i < c:
            _add(
                row,
                (h, i + 1, j),
                r * (c - i) * (Q(h, c + m) + Q(i, c)) / total_fitness,
            )
        if i:
            _add(
                row,
                (h, i - 1, j),
                i * (Q(1 - h, c + m) + Q(c - i, c)) / total_fitness,
            )

        # The hub changes type.
        if not h:
            _add(row, (1, i, j), r * (Q(i, c) + j) / total_fitness)
        else:
            _add(
                row,
                (0, i, j),
                (Q(c - i, c) + (m - j)) / total_fitness,
            )

        # A pendant changes type; only the hub can replace it.
        if j < m:
            _add(
                row,
                (h, i, j + 1),
                r * h * Q(m - j, c + m) / total_fitness,
            )
        if j:
            _add(
                row,
                (h, i, j - 1),
                (1 - h) * Q(j, c + m) / total_fitness,
            )

    elif rule == "dB":
        hub_fitness = 1 + (r - 1) * h

        # A resident ordinary clique vertex dies.  Its competing neighbors
        # are H and the other c-1 ordinary clique vertices.
        if i < c:
            denominator = hub_fitness + r * i + (c - i - 1)
            _add(
                row,
                (h, i + 1, j),
                Q(c - i, n) * r * (h + i) / denominator,
            )
        # A mutant ordinary clique vertex dies.
        if i:
            denominator = hub_fitness + r * (i - 1) + (c - i)
            _add(
                row,
                (h, i - 1, j),
                Q(i, n) * ((1 - h) + (c - i)) / denominator,
            )

        # The hub dies; its c+m neighbors compete.
        denominator = c + m + (r - 1) * (i + j)
        if not h:
            _add(row, (1, i, j), Q(1, n) * r * (i + j) / denominator)
        else:
            _add(
                row,
                (0, i, j),
                Q(1, n) * ((c - i) + (m - j)) / denominator,
            )

        # A leaf has one neighbor, so the replacement is deterministic.
        if j < m:
            _add(row, (h, i, j + 1), Q(m - j, n) * h)
        if j:
            _add(row, (h, i, j - 1), Q(j, n) * (1 - h))
    else:
        raise ValueError(rule)

    assert all(p > 0 for p in row.values())
    assert sum(row.values(), Q(0)) <= 1
    return row


def states(c: int, m: int):
    return [
        (h, i, j)
        for h in range(2)
        for i in range(c + 1)
        for j in range(m + 1)
    ]


def exact_fixation(c: int, m: int, rule: str, r=Q(3, 2)):
    """Solve the embedded quotient chain exactly over QQ with FLINT."""
    extinction = (0, 0, 0)
    fixation = (1, c, m)
    transient = [s for s in states(c, m) if s not in (extinction, fixation)]
    index = {s: k for k, s in enumerate(transient)}
    matrix = fmpq_mat(len(transient), len(transient))
    rhs = fmpq_mat(len(transient), 1)

    for state, row_index in index.items():
        changes = quotient_changes(c, m, r, rule, state)
        exit_probability = sum(changes.values(), Q(0))
        assert exit_probability > 0
        matrix[row_index, row_index] = exit_probability
        for target, probability in changes.items():
            if target == fixation:
                rhs[row_index, 0] += probability
            elif target != extinction:
                matrix[row_index, index[target]] -= probability

    solution = matrix.solve(rhs)
    # This is a second, cheap exact certificate after the solve: substituting
    # the result into every first-step equation gives an identically zero
    # rational residual.
    assert matrix * solution == rhs
    hub = solution[index[(1, 0, 0)], 0]
    ordinary = solution[index[(0, 1, 0)], 0]
    leaf = solution[index[(0, 0, 1)], 0]
    average = (hub + c * ordinary + m * leaf) / (c + m + 1)
    assert 0 < average < 1
    return average, (hub, ordinary, leaf)


def numeric_fixation(c: int, m: int, rule: str, r=1.5):
    extinction = (0, 0, 0)
    fixation = (1, c, m)
    transient = [s for s in states(c, m) if s not in (extinction, fixation)]
    index = {s: k for k, s in enumerate(transient)}
    matrix = lil_matrix((len(transient), len(transient)), dtype=float)
    rhs = np.zeros(len(transient))
    rational_r = Fraction(r)
    rq = Q(rational_r.numerator, rational_r.denominator)
    for state, row_index in index.items():
        changes = quotient_changes(c, m, rq, rule, state)
        matrix[row_index, row_index] = float(sum(changes.values(), Q(0)))
        for target, probability in changes.items():
            p = float(probability)
            if target == fixation:
                rhs[row_index] += p
            elif target != extinction:
                matrix[row_index, index[target]] -= p
    solution = spsolve(csr_matrix(matrix), rhs)
    return (
        solution[index[(1, 0, 0)]]
        + c * solution[index[(0, 1, 0)]]
        + m * solution[index[(0, 0, 1)]]
    ) / (c + m + 1)


def complete_baselines(n: int):
    bd = Q(3 ** (n - 1), 3**n - 2**n)
    db = Q((n - 1) * 3 ** (n - 2), n * (3 ** (n - 1) - 2 ** (n - 1)))
    return bd, db


def digest(value):
    numerator, denominator = value.numerator, value.denominator
    payload = f"{numerator}/{denominator}".encode()
    return {
        "numerator_digits": len(str(abs(numerator))),
        "denominator_digits": len(str(denominator)),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def labelled_changes(c: int, m: int, r, rule: str, mask: int):
    """Direct definition-level type-changing row on labelled subsets."""
    n = c + m + 1
    hub = 0
    adjacency = [set() for _ in range(n)]
    for u, v in combinations(range(c + 1), 2):
        adjacency[u].add(v)
        adjacency[v].add(u)
    for leaf in range(c + 1, n):
        adjacency[hub].add(leaf)
        adjacency[leaf].add(hub)
    mutant = [(mask >> vertex) & 1 for vertex in range(n)]
    fitness = [r if mutant[vertex] else Q(1) for vertex in range(n)]
    row = {}
    if rule == "Bd":
        total = sum(fitness, Q(0))
        for parent in range(n):
            for target in adjacency[parent]:
                probability = fitness[parent] / total / len(adjacency[parent])
                if mutant[parent] != mutant[target]:
                    next_mask = mask ^ (1 << target)
                    row[next_mask] = row.get(next_mask, Q(0)) + probability
    else:
        for target in range(n):
            denominator = sum((fitness[u] for u in adjacency[target]), Q(0))
            for parent in adjacency[target]:
                probability = Q(1, n) * fitness[parent] / denominator
                if mutant[parent] != mutant[target]:
                    next_mask = mask ^ (1 << target)
                    row[next_mask] = row.get(next_mask, Q(0)) + probability
    return row


def quotient_label(c: int, m: int, mask: int):
    h = mask & 1
    i = sum((mask >> vertex) & 1 for vertex in range(1, c + 1))
    j = sum((mask >> vertex) & 1 for vertex in range(c + 1, c + m + 1))
    return (h, i, j)


def check_strong_lumping(c=3, m=2):
    """Aggregate every labelled row and compare with the closed formulas."""
    n = c + m + 1
    r = Q(3, 2)
    for rule in ("Bd", "dB"):
        representatives = {}
        for mask in range(1 << n):
            label = quotient_label(c, m, mask)
            aggregated = {}
            for next_mask, probability in labelled_changes(c, m, r, rule, mask).items():
                target = quotient_label(c, m, next_mask)
                aggregated[target] = aggregated.get(target, Q(0)) + probability
            assert aggregated == quotient_changes(c, m, r, rule, label)
            if label in representatives:
                assert aggregated == representatives[label]
            else:
                representatives[label] = aggregated


def scan(max_n=60):
    witnesses = []
    for n in range(4, max_n + 1):
        for m in range(1, n - 2):
            c = n - m - 1
            bd = numeric_fixation(c, m, "Bd")
            db = numeric_fixation(c, m, "dB")
            base_bd, base_db = complete_baselines(n)
            x = bd / float(base_bd)
            y = db / float(base_db)
            if x * y > 1 + 1e-10:
                witnesses.append((n, c, m, x, y, x * y))
                break
        if witnesses:
            break
    return witnesses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan", action="store_true")
    parser.add_argument("--max-n", type=int, default=60)
    parser.add_argument("--c", type=int, default=31)
    parser.add_argument("--m", type=int, default=4)
    parser.add_argument("--exact", action="store_true")
    args = parser.parse_args()

    check_strong_lumping()
    print("PASS definition-level labelled/quotient strong-lumping audit (c=3,m=2)")
    if args.scan:
        print("first numerical witness by population size:", scan(args.max_n))

    c, m, n = args.c, args.m, args.c + args.m + 1
    bd_float = numeric_fixation(c, m, "Bd")
    db_float = numeric_fixation(c, m, "dB")
    base_bd, base_db = complete_baselines(n)
    print(f"G(c={c},m={m}), n={n}, r=3/2")
    print("numeric normalized Bd =", bd_float / float(base_bd))
    print("numeric normalized dB =", db_float / float(base_db))
    print(
        "numeric normalized product =",
        bd_float * db_float / float(base_bd * base_db),
    )

    if args.exact:
        bd, bd_singletons = exact_fixation(c, m, "Bd")
        print("PASS exact Bd solve and zero residual")
        db, db_singletons = exact_fixation(c, m, "dB")
        print("PASS exact dB solve and zero residual")
        ratio_bd = bd / base_bd
        ratio_db = db / base_db
        product_gap = ratio_bd * ratio_db - 1
        arithmetic_gap = (ratio_bd + ratio_db) / 2 - 1
        lambda_zero = (1 - ratio_db) / (ratio_bd - ratio_db)
        one_third_slack = 1 - (ratio_bd + 2 * ratio_db) / 3
        assert ratio_bd > 1
        assert ratio_db < 1
        assert product_gap > 0
        assert arithmetic_gap > 0
        assert Q(1, 3) < lambda_zero < Q(1, 2)
        assert one_third_slack > 0
        if (c, m) == (31, 4):
            # Compact manuscript certificate: these two short rational lower
            # bounds alone prove both the product and balanced-mean failures.
            assert ratio_bd > Q(5609, 5000)
            assert ratio_db > Q(223, 250)
            assert Q(5609, 5000) * Q(223, 250) == Q(1_250_807, 1_250_000) > 1
            assert (Q(5609, 5000) + Q(223, 250)) / 2 == Q(10_069, 10_000) > 1
            print(
                "PASS compact bounds x>5609/5000, y>223/250; "
                "xy>1250807/1250000 and (x+y)/2>10069/10000"
            )
        print(
            "exact signs: Bd/K > 1, dB/K < 1, product gap > 0, "
            "balanced-arithmetic gap > 0"
        )
        print("Bd ratio", float(ratio_bd), digest(ratio_bd))
        print("dB ratio", float(ratio_db), digest(ratio_db))
        print("product gap", float(product_gap), digest(product_gap))
        print("balanced-arithmetic gap", float(arithmetic_gap), digest(arithmetic_gap))
        print("affine crossing lambda_0", float(lambda_zero), digest(lambda_zero))
        print("lambda=1/3 slack", float(one_third_slack), digest(one_third_slack))
        assert one_third_slack == (ratio_bd - ratio_db) * (
            lambda_zero - Q(1, 3)
        )
        print(
            "PASS transparent affine factorization: "
            "1-[lambda*x+(1-lambda)*y]=(x-y)(lambda_0-lambda)"
        )
        print("Bd singleton values", [float(x) for x in bd_singletons])
        print("dB singleton values", [float(x) for x in db_singletons])


if __name__ == "__main__":
    main()
