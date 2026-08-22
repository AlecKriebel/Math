#!/usr/bin/env python3
"""Independent exact checks for the complete-graph-extremality manuscript.

This program was written from the transition equations in the manuscript.  It
does not import, execute, or copy the delivered verification implementation.
All arithmetic is fractions.Fraction; every pass/fail decision is exact.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
import platform
import sys


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def fsum(values):
    total = F(0)
    for value in values:
        total += value
    return total


def dot(left, right):
    require(len(left) == len(right), "dot-product dimension mismatch")
    return fsum(a * b for a, b in zip(left, right))


def matvec(matrix, vector):
    return [dot(row, vector) for row in matrix]


def rowvec(vector, matrix):
    require(len(vector) == len(matrix), "row-vector dimension mismatch")
    width = len(matrix[0])
    return [fsum(vector[i] * matrix[i][j] for i in range(len(vector)))
            for j in range(width)]


def solve_fraction(matrix, rhs):
    """Solve a nonsingular rational system by pivoted Gaussian elimination."""
    n = len(matrix)
    require(n == len(rhs), "linear-system dimension mismatch")
    a = [list(row) for row in matrix]
    b = list(rhs)
    require(all(len(row) == n for row in a), "matrix is not square")
    for column in range(n):
        pivot_row = next((i for i in range(column, n)
                          if a[i][column] != 0), None)
        require(pivot_row is not None, f"singular matrix at column {column}")
        if pivot_row != column:
            a[column], a[pivot_row] = a[pivot_row], a[column]
            b[column], b[pivot_row] = b[pivot_row], b[column]
        pivot = a[column][column]
        for i in range(column + 1, n):
            if a[i][column] == 0:
                continue
            factor = a[i][column] / pivot
            a[i][column] = F(0)
            for j in range(column + 1, n):
                a[i][j] -= factor * a[column][j]
            b[i] -= factor * b[column]
    solution = [F(0) for _ in range(n)]
    for i in range(n - 1, -1, -1):
        residual = b[i] - fsum(a[i][j] * solution[j]
                               for j in range(i + 1, n))
        require(a[i][i] != 0, f"zero diagonal at backsolve row {i}")
        solution[i] = residual / a[i][i]
    require(matvec(matrix, solution) == list(rhs),
            "exact residual failed after linear solve")
    return solution


def validate_kernel(p):
    n = len(p)
    require(all(len(row) == n for row in p), "kernel is not square")
    for v, row in enumerate(p):
        require(row[v] == 0, f"kernel diagonal is nonzero in row {v}")
        require(all(value >= 0 for value in row), "negative kernel entry")
        require(fsum(row) == 1, f"row {v} does not sum to one")


def complete_kernel(n):
    return [[F(0) if u == v else F(1, n - 1) for u in range(n)]
            for v in range(n)]


def normalize_undirected_weights(weights):
    n = len(weights)
    p = []
    for v in range(n):
        incoming = fsum(weights[u][v] for u in range(n) if u != v)
        require(incoming > 0, f"target {v} has zero incoming degree")
        p.append([F(0) if u == v else weights[u][v] / incoming
                  for u in range(n)])
    validate_kernel(p)
    return p


def normalize_target_by_source(weights):
    """Equation (2.1), with raw weights stored as weights[source][target]."""
    n = len(weights)
    p = []
    for v in range(n):
        incoming = fsum(weights[u][v] for u in range(n) if u != v)
        require(incoming > 0, f"target {v} has zero incoming degree")
        p.append([F(0) if u == v else weights[u][v] / incoming
                  for u in range(n)])
    validate_kernel(p)
    return p


def normalize_wrong_source_rows(weights):
    """Deliberately wrong orientation, retained only as a negative control."""
    n = len(weights)
    p = []
    for v in range(n):
        outgoing = fsum(weights[v][u] for u in range(n) if u != v)
        require(outgoing > 0, f"source {v} has zero outgoing degree")
        p.append([F(0) if u == v else weights[v][u] / outgoing
                  for u in range(n)])
    validate_kernel(p)
    return p


def baseline(n, r):
    if r == 1:
        return F(1, n)
    return F(n - 1, n) * (1 - 1 / r) / (1 - r ** (-(n - 1)))


def subset_transition(p, r, mask):
    """Literal dB subset transition from manuscript equations (2.1)--(2.2)."""
    n = len(p)
    transitions = {}
    for v in range(n):
        x = fsum(p[v][u] for u in range(n) if mask & (1 << u))
        mutant_parent = r * x / (1 + (r - 1) * x)
        if mask & (1 << v):
            changed = mask & ~(1 << v)
            alternatives = ((mask, mutant_parent),
                            (changed, 1 - mutant_parent))
        else:
            changed = mask | (1 << v)
            alternatives = ((changed, mutant_parent),
                            (mask, 1 - mutant_parent))
        for destination, conditional_probability in alternatives:
            transitions[destination] = (
                transitions.get(destination, F(0))
                + conditional_probability / n
            )
    require(fsum(transitions.values()) == 1,
            "subset transition row is not stochastic")
    return transitions


def subset_fixation(p, r):
    validate_kernel(p)
    n = len(p)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {mask: i for i, mask in enumerate(states)}
    size = len(states)
    matrix = [[F(int(i == j)) for j in range(size)] for i in range(size)]
    rhs = [F(0) for _ in states]
    for mask in states:
        row = index[mask]
        for destination, probability in subset_transition(p, r, mask).items():
            if destination == full:
                rhs[row] += probability
            elif destination != 0:
                matrix[row][index[destination]] -= probability
    committor = solve_fraction(matrix, rhs)
    rho = fsum(committor[index[1 << i]] for i in range(n)) / n
    require(F(0) <= rho <= F(1), "fixation probability outside [0,1]")
    return rho, {mask: committor[index[mask]] for mask in states}


def active_states(n):
    return [(mask, v) for v in range(n)
            for mask in range(1, 1 << n)
            if not (mask & (1 << v))]


def active_matrix(p):
    """Literal one-sample active kernel from manuscript (3.10)--(3.12)."""
    validate_kernel(p)
    n = len(p)
    states = active_states(n)
    index = {state: i for i, state in enumerate(states)}
    matrix = [[F(0) for _ in states] for _ in states]
    for row, (mask, v) in enumerate(states):
        members = [w for w in range(n) if mask & (1 << w)]
        for i in range(n):
            probability = p[v][i] / 2
            if probability == 0:
                continue
            destination = (mask | (1 << i), v)
            matrix[row][index[destination]] += probability
        for w in members:
            for i in range(n):
                probability = p[w][i] / (2 * len(members))
                if probability == 0:
                    continue
                destination = ((mask & ~(1 << w)) | (1 << i), w)
                matrix[row][index[destination]] += probability
        require(fsum(matrix[row]) == 1,
                f"active row {row} is not stochastic")
    return states, matrix


def active_delta(delta):
    """Directional derivative of the active kernel, derived move-by-move."""
    n = len(delta)
    states = active_states(n)
    index = {state: i for i, state in enumerate(states)}
    matrix = [[F(0) for _ in states] for _ in states]
    for row, (mask, v) in enumerate(states):
        members = [w for w in range(n) if mask & (1 << w)]
        for i in range(n):
            if delta[v][i] == 0:
                continue
            destination = (mask | (1 << i), v)
            matrix[row][index[destination]] += delta[v][i] / 2
        for w in members:
            for i in range(n):
                if delta[w][i] == 0:
                    continue
                destination = ((mask & ~(1 << w)) | (1 << i), w)
                matrix[row][index[destination]] += (
                    delta[w][i] / (2 * len(members))
                )
        require(fsum(matrix[row]) == 0,
                f"active derivative row {row} does not sum to zero")
    return states, matrix


def stationary(matrix):
    size = len(matrix)
    equations = [[matrix[j][i] - F(int(i == j))
                  for j in range(size)] for i in range(size)]
    equations[-1] = [F(1) for _ in range(size)]
    rhs = [F(0) for _ in range(size)]
    rhs[-1] = F(1)
    pi = solve_fraction(equations, rhs)
    require(rowvec(pi, matrix) == pi, "stationary-law residual failed")
    require(fsum(pi) == 1, "stationary law is not normalized")
    require(all(value > 0 for value in pi), "stationary law is not positive")
    return pi


def collision_identity(p):
    n = len(p)
    rho, _ = subset_fixation(p, F(2))
    states, kernel = active_matrix(p)
    pi = stationary(kernel)
    h = [F(1, mask.bit_count()) for mask, _ in states]
    collision = dot(pi, h)
    require(collision == 1 / (n * rho),
            "active collision identity does not match literal subset chain")
    return rho, collision, len(states)


def validate_tangent(delta):
    n = len(delta)
    require(all(len(row) == n for row in delta), "tangent is not square")
    for i, row in enumerate(delta):
        require(row[i] == 0, "tangent has nonzero diagonal")
        require(fsum(row) == 0, "tangent row sum is nonzero")


def frobenius_squared(delta):
    return fsum(value * value for row in delta for value in row)


def standard_representative(n):
    s = [F(0) for _ in range(n)]
    s[0], s[1] = F(1), F(-1)
    delta = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                delta[i][j] = (s[i] + (n - 1) * s[j]) / (n * (n - 2))
    validate_tangent(delta)
    require([fsum(delta[i][j] for i in range(n)) for j in range(n)] == s,
            "standard representative has the wrong column sums")
    return delta


def symmetric_balanced_representative(n):
    require(n >= 4, "symmetric-balanced sector is absent below n=4")
    delta = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, j, value in ((0, 1, 1), (2, 3, 1),
                        (0, 2, -1), (1, 3, -1)):
        delta[i][j] = delta[j][i] = F(value)
    validate_tangent(delta)
    require(all(fsum(delta[i][j] for i in range(n)) == 0
                for j in range(n)), "symmetric representative is not balanced")
    return delta


def antisymmetric_balanced_representative(n):
    delta = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        j = (i + 1) % n
        delta[i][j] += 1
        delta[j][i] -= 1
    validate_tangent(delta)
    require(all(fsum(delta[i][j] for i in range(n)) == 0
                for j in range(n)), "antisymmetric representative is not balanced")
    return delta


def hessian_value(n, delta):
    """Compute nu0 Delta G Delta Gq from the literal active chain."""
    validate_tangent(delta)
    states, k0 = active_matrix(complete_kernel(n))
    states_delta, perturbation = active_delta(delta)
    require(states_delta == states, "active-state order mismatch")
    N = n - 1
    denominator = n * N * (2 ** (N - 1))
    nu0 = [F(mask.bit_count(), denominator) for mask, _ in states]
    require(fsum(nu0) == 1, "displayed complete stationary law is not normalized")
    require(rowvec(nu0, k0) == nu0,
            "displayed complete stationary law is not stationary")
    c0 = F(2 ** N - 1, N * (2 ** (N - 1)))
    h = [F(1, mask.bit_count()) for mask, _ in states]
    require(dot(nu0, h) == c0, "displayed complete collision rate failed")
    q = [value - c0 for value in h]
    size = len(states)
    group_matrix = [[F(int(i == j)) - k0[i][j] + nu0[j]
                     for j in range(size)] for i in range(size)]
    gq = solve_fraction(group_matrix, q)
    delta_gq = matvec(perturbation, gq)
    first = dot(nu0, delta_gq)
    require(first == 0, "first variation did not vanish")
    g_delta_gq = solve_fraction(group_matrix, delta_gq)
    second = dot(nu0, matvec(perturbation, g_delta_gq))
    return second, second / frobenius_squared(delta), len(states)


def strong_selection_expansion(p):
    """Exact epsilon=1/r expansion of the literal subset equations."""
    validate_kernel(p)
    n = len(p)
    full = (1 << n) - 1
    states = list(range(1, full))
    index = {mask: i for i, mask in enumerate(states)}
    size = len(states)
    q0 = [[F(0) for _ in states] for _ in states]
    q1 = [[F(0) for _ in states] for _ in states]
    b0 = [F(0) for _ in states]
    b1 = [F(0) for _ in states]
    for mask in states:
        row = index[mask]
        for v in range(n):
            x = fsum(p[v][u] for u in range(n) if mask & (1 << u))
            if x == 0:
                f0, f1 = F(0), F(0)
            else:
                f0, f1 = F(1), -(1 - x) / x
            if mask & (1 << v):
                alternatives = ((mask, (f0, f1)),
                                (mask & ~(1 << v), (1 - f0, -f1)))
            else:
                alternatives = ((mask | (1 << v), (f0, f1)),
                                (mask, (1 - f0, -f1)))
            for destination, (prob0, prob1) in alternatives:
                prob0 /= n
                prob1 /= n
                if destination == full:
                    b0[row] += prob0
                    b1[row] += prob1
                elif destination != 0:
                    q0[row][index[destination]] += prob0
                    q1[row][index[destination]] += prob1
        require(fsum(q0[row]) + b0[row] <= 1,
                "limiting expansion has excessive non-extinction mass")
    a0 = [[F(int(i == j)) - q0[i][j] for j in range(size)]
          for i in range(size)]
    h0 = solve_fraction(a0, b0)
    derivative_rhs = [b1[i] + dot(q1[i], h0) for i in range(size)]
    h1 = solve_fraction(a0, derivative_rhs)
    rho0 = fsum(h0[index[1 << i]] for i in range(n)) / n
    rho1 = fsum(h1[index[1 << i]] for i in range(n)) / n
    return rho0, rho1


def directed_defect(p):
    validate_kernel(p)
    n = len(p)
    total = F(0)
    for v in range(n):
        sources = [u for u in range(n) if u != v]
        for u, z in combinations(sources, 2):
            require(p[v][u] > 0 and p[v][z] > 0,
                    "directed defect requires complete positive support")
            total += (p[v][u] - p[v][z]) ** 2 / (p[v][u] * p[v][z])
    return total


def triangle_weights(a, b, c):
    # Edges 01, 02, 12 respectively.
    return [[F(0), a, b], [a, F(0), c], [b, c, F(0)]]


def g13_weights(x):
    weights = [[F(0) for _ in range(4)] for _ in range(4)]
    for satellite in (1, 2, 3):
        weights[0][satellite] = weights[satellite][0] = F(1)
    for i, j in combinations((1, 2, 3), 2):
        weights[i][j] = weights[j][i] = x
    return weights


def g22_weights(x, y):
    weights = [[F(0) for _ in range(4)] for _ in range(4)]
    weights[0][1] = weights[1][0] = x
    weights[2][3] = weights[3][2] = y
    for i in (0, 1):
        for j in (2, 3):
            weights[i][j] = weights[j][i] = F(1)
    return weights


def short(value):
    return str(value) if value.denominator != 1 else str(value.numerator)


def main():
    print("INDEPENDENT EXACT CROSS-CHECKS")
    print(f"python={platform.python_version()} optimize={sys.flags.optimize}")
    print("arithmetic=fractions.Fraction; delivered_modules_imported=false")

    nonsymmetric = {
        "P3-A": [
            [F(0), F(1, 3), F(2, 3)],
            [F(3, 4), F(0), F(1, 4)],
            [F(2, 5), F(3, 5), F(0)],
        ],
        "P3-B": [
            [F(0), F(4, 5), F(1, 5)],
            [F(1, 6), F(0), F(5, 6)],
            [F(7, 9), F(2, 9), F(0)],
        ],
        "P4-A": [
            [F(0), F(1, 2), F(1, 3), F(1, 6)],
            [F(1, 5), F(0), F(1, 2), F(3, 10)],
            [F(2, 7), F(3, 7), F(0), F(2, 7)],
            [F(1, 4), F(1, 2), F(1, 4), F(0)],
        ],
        "P4-B": [
            [F(0), F(2, 9), F(1, 3), F(4, 9)],
            [F(1, 2), F(0), F(1, 8), F(3, 8)],
            [F(1, 6), F(1, 2), F(0), F(1, 3)],
            [F(3, 7), F(2, 7), F(2, 7), F(0)],
        ],
    }

    print("\n[collision identity: literal subset versus literal active chain]")
    for name, p in nonsymmetric.items():
        rho, collision, active_count = collision_identity(p)
        print(f"{name}: n={len(p)} active_states={active_count} "
              f"rho2={short(rho)} nuH={short(collision)} "
              f"n*rho*nuH={short(len(p) * rho * collision)} PASS")

    print("\n[target-by-source orientation and incoming-column gauge]")
    raw = [
        [F(0), F(2), F(7), F(3)],
        [F(5), F(0), F(1), F(8)],
        [F(4), F(9), F(0), F(6)],
        [F(11), F(3), F(2), F(0)],
    ]
    p_target = normalize_target_by_source(raw)
    column_scales = [F(2), F(3), F(5), F(7)]
    scaled_raw = [[raw[u][v] * column_scales[v] for v in range(4)]
                  for u in range(4)]
    p_scaled = normalize_target_by_source(scaled_raw)
    p_wrong = normalize_wrong_source_rows(raw)
    rho_target, _ = subset_fixation(p_target, F(2))
    rho_scaled, _ = subset_fixation(p_scaled, F(2))
    rho_wrong, _ = subset_fixation(p_wrong, F(2))
    require(p_scaled == p_target and rho_scaled == rho_target,
            "incoming-column scaling changed the normalized chain")
    require(rho_wrong != rho_target,
            "orientation negative control unexpectedly tied")
    print(f"correct_rho2={short(rho_target)} scaled_column_rho2={short(rho_scaled)} "
          f"wrong_source_row_rho2={short(rho_wrong)} "
          "correct=scaled and correct!=wrong PASS")

    print("\n[complete-kernel Hessian sectors: literal active-chain resolvent]")
    expected = {
        (3, "standard"): F(1, 11),
        (3, "antisymmetric-balanced"): F(1, 9),
        (4, "standard"): F(87, 640),
        (4, "symmetric-balanced"): F(3, 208),
        (4, "antisymmetric-balanced"): F(57, 640),
        (5, "standard"): F(8585, 57314),
        (5, "symmetric-balanced"): F(359, 26660),
        (5, "antisymmetric-balanced"): F(143, 2100),
    }
    for n in (3, 4, 5):
        representatives = [("standard", standard_representative(n))]
        if n >= 4:
            representatives.append(("symmetric-balanced",
                                    symmetric_balanced_representative(n)))
        representatives.append(("antisymmetric-balanced",
                                antisymmetric_balanced_representative(n)))
        for label, delta in representatives:
            second, normalized, active_count = hessian_value(n, delta)
            require(normalized == expected[(n, label)],
                    f"Hessian eigenvalue mismatch for n={n} {label}: "
                    f"got {normalized}, expected {expected[(n, label)]}")
            print(f"n={n} sector={label} active_states={active_count} "
                  f"R2={short(second)} norm2={short(frobenius_squared(delta))} "
                  f"normalized={short(normalized)} PASS")

    print("\n[strong-selection coefficient from independent epsilon differentiation]")
    for name, p in nonsymmetric.items():
        n = len(p)
        rho0, rho1 = strong_selection_expansion(p)
        defect = directed_defect(p)
        observed_gap_coefficient = -F(n - 1, n) - rho1
        expected_gap_coefficient = defect / (n * n * (n - 2))
        require(rho0 == F(n - 1, n), f"wrong strong limit for {name}")
        require(observed_gap_coefficient == expected_gap_coefficient,
                f"strong-selection coefficient mismatch for {name}")
        print(f"{name}: rho0={short(rho0)} rho1={short(rho1)} "
              f"Edir={short(defect)} gap_coeff={short(observed_gap_coefficient)} PASS")

    print("\n[weighted triangles: full subset chain]")
    triangle_cases = [
        ("uniform/equality", F(1), F(1), F(1), F(2), "equal"),
        ("nonuniform", F(1), F(2), F(3), F(2), "strict"),
        ("nonuniform-rational-r", F(2), F(5), F(7), F(7, 3), "strict"),
        ("near-positive-boundary", F(1, 1000), F(2), F(3), F(3, 2), "strict"),
        ("support-boundary-outside-theorem", F(0), F(2), F(3), F(2), "strict"),
        ("neutral-r-boundary", F(1), F(2), F(3), F(1), "equal"),
    ]
    for label, a, b, c, r, relation in triangle_cases:
        p = normalize_undirected_weights(triangle_weights(a, b, c))
        rho, _ = subset_fixation(p, r)
        base = baseline(3, r)
        gap = base - rho
        require((gap == 0) if relation == "equal" else (gap > 0),
                f"triangle relation failed: {label}")
        print(f"{label}: weights=({short(a)},{short(b)},{short(c)}) "
              f"r={short(r)} rho={short(rho)} baseline={short(base)} "
              f"gap={short(gap)} {relation.upper()} PASS")

    print("\n[weighted K4 slices: full 14-state subset chain, no lumping]")
    k4_cases = [
        ("G13-uniform/equality", g13_weights(F(1)), F(2), "equal"),
        ("G13-nonuniform", g13_weights(F(1, 3)), F(2), "strict"),
        ("G13-near-boundary", g13_weights(F(1, 1000)), F(7, 3), "strict"),
        ("G13-support-boundary-outside-theorem", g13_weights(F(0)), F(2), "strict"),
        ("G22-uniform/equality", g22_weights(F(1), F(1)), F(2), "equal"),
        ("G22-equal-internal-but-nonuniform", g22_weights(F(2), F(2)), F(3, 2), "strict"),
        ("G22-asymmetric", g22_weights(F(1, 10), F(10)), F(2), "strict"),
        ("G22-support-boundary-outside-theorem", g22_weights(F(0), F(0)), F(2), "strict"),
        ("G22-neutral-r-boundary", g22_weights(F(1, 10), F(10)), F(1), "equal"),
    ]
    for label, weights, r, relation in k4_cases:
        p = normalize_undirected_weights(weights)
        rho, _ = subset_fixation(p, r)
        base = baseline(4, r)
        gap = base - rho
        require((gap == 0) if relation == "equal" else (gap > 0),
                f"K4 relation failed: {label}")
        print(f"{label}: r={short(r)} rho={short(rho)} "
              f"baseline={short(base)} gap={short(gap)} "
              f"{relation.upper()} PASS")

    print("\n[endpoint and monotonicity spot checks]")
    for name, p in nonsymmetric.items():
        n = len(p)
        rho1, _ = subset_fixation(p, F(1))
        rho2, _ = subset_fixation(p, F(2))
        rho3, _ = subset_fixation(p, F(3))
        require(rho1 == F(1, n), f"neutral endpoint mismatch for {name}")
        require(rho1 < rho2 < rho3, f"fitness monotonicity spot check failed for {name}")
        print(f"{name}: rho1={short(rho1)} < rho2={short(rho2)} "
              f"< rho3={short(rho3)} PASS")
    for raw_weight in (F(1, 1000), F(1), F(1000)):
        p2 = normalize_undirected_weights(
            [[F(0), raw_weight], [raw_weight, F(0)]])
        for r in (F(1), F(2), F(7, 3)):
            rho, _ = subset_fixation(p2, r)
            require(rho == baseline(2, r), "n=2 weighting failed to tie baseline")
    print("n=2 raw weights 1/1000,1,1000 tie baseline at r=1,2,7/3 PASS")
    print("n=3 symmetric-balanced sector dimension 3*(3-3)/2=0 PASS")

    print("\nALL INDEPENDENT EXACT CROSS-CHECKS PASSED")


if __name__ == "__main__":
    main()
