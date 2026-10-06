"""Exact structural falsification checks for the frozen observable transport.

These do not replace the general proof. They deliberately cover multiplicities,
empty rows, order-two edges, and nontrivial period subgroups. Stdlib only.
"""

from fractions import Fraction
from itertools import product


def shift(values, displacement):
    n = len(values)
    return tuple(values[(i + displacement) % n] for i in range(n))


def observable_gate(values, edge, gate):
    n = len(values)

    def event(v, s):
        if gate == 0:
            return True
        if gate == 1:
            return v[0] >= 2 and s == 1 % n
        if gate == 2:
            return v[0] < v[s]
        return sum(v) % 2 == 0 and s != 0

    return Fraction(
        int(event(values, edge))
        + int(event(shift(values, edge), (-edge) % n)),
        2,
    )


def matrix(values, neighborhood, gate):
    n = len(values)
    rows = []
    for start in range(n):
        row = []
        start_count = sum(values[(start + c) % n] for c in neighborhood)
        for end in range(n):
            edge = (end - start) % n
            if start == end or edge not in neighborhood:
                row.append(Fraction(0))
                continue
            end_count = sum(values[(end + c) % n] for c in neighborhood)
            gate_value = observable_gate(shift(values, start), edge, gate)
            row.append(gate_value * Fraction(values[end], (1 + start_count) * (1 + end_count)))
        moved = sum(row)
        assert 0 <= moved <= 1
        assert moved <= Fraction(start_count, 1 + start_count)
        row[start] = 1 - moved
        rows.append(tuple(row))
    return tuple(rows)


def run():
    checked = 0
    for n in range(1, 6):
        symmetric_sets = []
        for flags in product((False, True), repeat=n - 1):
            c = {0} | {i + 1 for i, flag in enumerate(flags) if flag}
            if c == {(-i) % n for i in c}:
                symmetric_sets.append(c)
        for values in product(range(4), repeat=n):
            for c in symmetric_sets:
                for gate in range(4):
                    transport = matrix(values, c, gate)
                    for row in transport:
                        assert sum(row) == 1
                    for end in range(n):
                        assert sum(values[start] * transport[start][end] for start in range(n)) == values[end]
                    for displacement in range(n):
                        shifted_transport = matrix(shift(values, displacement), c, gate)
                        for start in range(n):
                            for end in range(n):
                                assert shifted_transport[(start - displacement) % n][(end - displacement) % n] == transport[start][end]
                    checked += 1

            # Check the residual-configuration signs separately from transport.
            for edge in range(1, n):
                observed = list(values)
                observed[0] += 1
                observed[edge] += 1
                reversed_observed = list(shift(observed, edge))
                reversed_observed[0] -= 1
                reversed_observed[(-edge) % n] -= 1
                assert tuple(reversed_observed) == shift(values, edge)
                # At an output edge s, J came from input edge -s.
                inverse_observed = list(values)
                inverse_observed[0] += 1
                inverse_observed[(-edge) % n] += 1
                j_output = list(shift(inverse_observed, -edge))
                j_output[0] -= 1
                j_output[edge] -= 1
                assert tuple(j_output) == shift(values, -edge)

            # Finite Haar inversion on the entire period subgroup.
            periods = {s for s in range(n) if shift(values, s) == values}
            for s in periods:
                assert values[s] == values[(-s) % n]

    print(f"PASS: {checked} exact transport fixtures; all row sums, preservation, covariance, endpoint signs, and finite period inversions.")


if __name__ == "__main__":
    run()
