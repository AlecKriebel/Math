#!/usr/bin/env python3
"""Exact forward absorbing-forest audit at fitness 3/2.

This verifier has two purposes.

1.  It constructs the Bd and dB absorbing generators directly from the
    update rules and checks the single paired absorbing-forest determinant
    equivalent to the endpoint fixation-product inequality.
2.  It tests the natural reverse/complement root-path surgery.  The local
    Bd--dB edge factor and its complemented partner are exact reciprocals.
    The required pointwise forest domination therefore fails in both
    directions, already on the weighted path P3 with edge ratio 1:17.

All arithmetic is over QQ.  The small P3 forest sums are also enumerated
directly, independently of determinants or linear solves.
"""

from __future__ import annotations

import hashlib
import itertools

from flint import fmpq, fmpq_mat


R = fmpq(3, 2)
A = fmpq(1, 2)


def normalized_kernel(weights):
    degrees = tuple(sum(row) for row in weights)
    assert all(degree > 0 for degree in degrees)
    return tuple(
        tuple(fmpq(weights[i][j], degrees[i]) for j in range(len(weights)))
        for i in range(len(weights))
    )


def forward_system(weights, rule: str):
    """Return ``L h=b`` for fixation, using a row-scaled exact generator."""
    n = len(weights)
    full = (1 << n) - 1
    states = tuple(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    kernel = normalized_kernel(weights)
    laplacian = fmpq_mat(len(states), len(states))
    fixation_boundary = fmpq_mat(len(states), 1)
    outgoing = {state: {} for state in states}

    def add(state: int, new_state: int, rate) -> None:
        if not rate:
            return
        outgoing[state][new_state] = outgoing[state].get(new_state, fmpq(0)) + rate

    for state in states:
        for target in range(n):
            if state & (1 << target):
                new_state = state & ~(1 << target)
                if rule == "Bd":
                    rate = sum(
                        kernel[source][target]
                        for source in range(n)
                        if not (state & (1 << source))
                    )
                elif rule == "dB":
                    mutant_mass = sum(
                        kernel[target][source]
                        for source in range(n)
                        if state & (1 << source)
                    )
                    rate = (1 - mutant_mass) / (1 + A * mutant_mass)
                else:
                    raise ValueError(rule)
            else:
                new_state = state | (1 << target)
                if rule == "Bd":
                    rate = R * sum(
                        kernel[source][target]
                        for source in range(n)
                        if state & (1 << source)
                    )
                elif rule == "dB":
                    mutant_mass = sum(
                        kernel[target][source]
                        for source in range(n)
                        if state & (1 << source)
                    )
                    rate = R * mutant_mass / (1 + A * mutant_mass)
                else:
                    raise ValueError(rule)
            add(state, new_state, rate)

    for state in states:
        row = index[state]
        laplacian[row, row] = sum(outgoing[state].values())
        for new_state, rate in outgoing[state].items():
            if new_state == full:
                fixation_boundary[row, 0] += rate
            elif new_state:
                laplacian[row, index[new_state]] -= rate

    values = laplacian.solve(fixation_boundary)
    rho = sum(values[index[1 << vertex], 0] for vertex in range(n)) / n
    determinant = laplacian.det()
    numerator = determinant * rho
    assert determinant > 0
    assert 0 < rho < 1
    return {
        "states": states,
        "outgoing": outgoing,
        "laplacian": laplacian,
        "values": values,
        "rho": rho,
        "Z": determinant,
        "N": numerator,
    }


def enumerate_absorbing_forests(system, n: int):
    """Enumerate every two-root outgoing forest; used only for n=3."""
    assert n == 3
    states = system["states"]
    outgoing = system["outgoing"]
    full = (1 << n) - 1
    choices = tuple(tuple(outgoing[state].items()) for state in states)
    partition = fmpq(0)
    numerator = fmpq(0)
    valid = 0

    for selected in itertools.product(*choices):
        successor = {
            state: new_state
            for state, (new_state, _rate) in zip(states, selected)
        }
        destinations = {}
        valid_forest = True
        for start in states:
            seen = set()
            current = start
            while current not in (0, full):
                if current in seen:
                    valid_forest = False
                    break
                seen.add(current)
                current = successor[current]
            if not valid_forest:
                break
            destinations[start] = current
        if not valid_forest:
            continue

        weight = fmpq(1)
        for _new_state, rate in selected:
            weight *= rate
        singleton_score = fmpq(
            sum(destinations[1 << vertex] == full for vertex in range(n)), n
        )
        partition += weight
        numerator += singleton_score * weight
        valid += 1

    assert partition == system["Z"]
    assert numerator == system["N"]
    return valid


def complete_means(n: int):
    b = n * A * R ** (n - 1) / (R**n - 1)
    d = (n - 1) * A * R ** (n - 2) / (R ** (n - 1) - 1)
    return b, d


def local_bias_data(weights, state: int, target: int):
    """Exact same-edge Bd/dB biases and reverse/complement factors."""
    n = len(weights)
    full = (1 << n) - 1
    assert state and not (state & (1 << target))
    kernel = normalized_kernel(weights)
    row_mass = sum(
        kernel[target][source]
        for source in range(n)
        if state & (1 << source)
    )
    column_mass = sum(
        kernel[source][target]
        for source in range(n)
        if state & (1 << source)
    )
    column_total = sum(kernel[source][target] for source in range(n))
    assert 0 < row_mass < 1
    assert 0 < column_mass < column_total

    bias_bd = R * column_mass / (column_total - column_mass)
    bias_db = R * row_mass / (1 - row_mass)
    orientation = bias_bd / bias_db
    complement_state = full ^ (state | (1 << target))
    rank = state.bit_count()
    baseline_bias = R * rank / (n - 1 - rank)
    product_ratio = bias_bd * bias_db / baseline_bias**2
    return {
        "x": row_mass,
        "y": column_mass,
        "t": column_total,
        "B_Bd": bias_bd,
        "B_dB": bias_db,
        "Xi": orientation,
        "Pi": product_ratio,
        "complement": complement_state,
    }


def check_complement_pair(weights, state: int, target: int, xi, pi):
    partner = local_bias_data(
        weights,
        local_bias_data(weights, state, target)["complement"],
        target,
    )
    assert partner["Xi"] == 1 / xi
    assert partner["Pi"] == 1 / pi
    original = local_bias_data(weights, state, target)
    assert original["B_Bd"] * partner["B_Bd"] == R**2
    assert original["B_dB"] * partner["B_dB"] == R**2
    return partner


def rational_hash(value) -> str:
    return hashlib.sha256(f"{value.p}/{value.q}".encode("ascii")).hexdigest()


def graph(matrix):
    answer = tuple(tuple(int(value) for value in row) for row in matrix)
    assert all(answer[i][i] == 0 for i in range(len(answer)))
    assert all(
        answer[i][j] == answer[j][i]
        for i in range(len(answer))
        for j in range(len(answer))
    )
    return answer


def hostile_graphs():
    yield "K4", graph(
        [[0 if i == j else 1 for j in range(4)] for i in range(4)]
    ), None
    yield "weighted-P3-1:17", graph(
        [[0, 0, 1], [0, 0, 17], [1, 17, 0]]
    ), (1, 2, fmpq(17), fmpq(1, 17))
    yield "batching-persistence-n4", graph(
        [
            [0, 2, 0, 3],
            [2, 0, 1, 30],
            [0, 1, 0, 1],
            [3, 30, 1, 0],
        ]
    ), (4, 1, fmpq(1360, 109), fmpq(85, 1744))
    yield "batching-timing-n5", graph(
        [
            [0, 0, 5, 5, 11],
            [0, 0, 7, 13, 1],
            [5, 7, 0, 1, 7],
            [5, 13, 1, 0, 2],
            [11, 1, 7, 2, 0],
        ]
    ), (4, 0, fmpq(21, 20), fmpq(945, 1024))
    windmill = [[0] * 7 for _ in range(7)]
    for (left, right), outer, internal in zip(
        ((1, 2), (3, 4), (5, 6)),
        (100, 10, 1),
        (600, 1200, 1800),
    ):
        windmill[left][right] = windmill[right][left] = internal
        windmill[0][left] = windmill[left][0] = outer
        windmill[0][right] = windmill[right][0] = outer
    yield "dB-windmill-n7", graph(windmill), (
        1,
        5,
        fmpq(1801, 222),
        fmpq(1801, 28771200),
    )


def analyze(label: str, weights, edge_witness):
    n = len(weights)
    bd = forward_system(weights, "Bd")
    db = forward_system(weights, "dB")
    complete = graph(
        [[0 if i == j else 1 for j in range(n)] for i in range(n)]
    )
    bd_k = forward_system(complete, "Bd")
    db_k = forward_system(complete, "dB")
    b, d = complete_means(n)
    assert bd_k["rho"] == b / n
    assert db_k["rho"] == d / n

    fixation_gap = bd_k["rho"] * db_k["rho"] - bd["rho"] * db["rho"]
    forest_gap = (
        bd_k["N"]
        * db_k["N"]
        * bd["Z"]
        * db["Z"]
        - bd["N"]
        * db["N"]
        * bd_k["Z"]
        * db_k["Z"]
    )
    positive_scale = bd["Z"] * db["Z"] * bd_k["Z"] * db_k["Z"]
    assert forest_gap == positive_scale * fixation_gap
    assert fixation_gap >= 0

    if n == 3:
        valid_bd = enumerate_absorbing_forests(bd, n)
        valid_db = enumerate_absorbing_forests(db, n)
        assert valid_bd > 0 and valid_db > 0

    if edge_witness is None:
        for state in range(1, (1 << n) - 1):
            if state.bit_count() >= n - 1:
                continue
            for target in range(n):
                if state & (1 << target):
                    continue
                data = local_bias_data(weights, state, target)
                assert data["Xi"] == 1
                assert data["Pi"] == 1
    else:
        state, target, expected_xi, expected_pi = edge_witness
        data = local_bias_data(weights, state, target)
        assert data["Xi"] == expected_xi
        assert data["Pi"] == expected_pi
        partner = check_complement_pair(
            weights, state, target, data["Xi"], data["Pi"]
        )
        assert (data["Xi"] > 1) and (partner["Xi"] < 1)
        assert (data["Pi"] < 1) != (partner["Pi"] < 1)
        print(
            label,
            "fixation_gap", float(fixation_gap),
            "Xi", data["Xi"],
            "Xi_comp", partner["Xi"],
            "Pi", data["Pi"],
            "Pi_comp", partner["Pi"],
            "hash", rational_hash(fixation_gap),
        )
        return

    print(
        label,
        "fixation_gap", float(fixation_gap),
        "Xi=Pi=1 on every admissible state edge",
        "hash", rational_hash(fixation_gap),
    )


def main() -> None:
    for label, weights, edge_witness in hostile_graphs():
        analyze(label, weights, edge_witness)
    print("PASS: exact paired absorbing-forest sign and path-bias obstruction")


if __name__ == "__main__":
    main()
