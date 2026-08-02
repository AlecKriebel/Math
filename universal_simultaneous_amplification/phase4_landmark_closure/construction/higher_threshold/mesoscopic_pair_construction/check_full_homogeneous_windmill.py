#!/usr/bin/env python3
"""Independent full-chain audit of the homogeneous balanced windmill.

Part 1 enumerates every microstate for three blades with symbolic `r,a` and
checks exact lumpability to `(portal type, heterotypic blades, mutant
blades)` directly from the two update definitions.

Part 2 solves the resulting finite chains numerically for growing blade
counts.  Those convergence values are diagnostics, not proof; the limiting
formulas are proved analytically in MESOSCOPIC_PAIR_BURST_NO_GO.md.
"""

from collections import defaultdict

import numpy as np
import sympy as sp
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


def lump(bits: tuple[int, ...], blades: int) -> tuple[int, int, int]:
    hetero = 0
    mutant = 0
    for j in range(blades):
        pair_sum = bits[1 + 2 * j] + bits[2 + 2 * j]
        hetero += pair_sum == 1
        mutant += pair_sum == 2
    return bits[0], int(hetero), int(mutant)


def edges(blades: int, a):
    out = []
    for j in range(blades):
        u, v = 1 + 2 * j, 2 + 2 * j
        out.extend([(0, u, a), (0, v, a), (u, v, sp.Integer(1))])
    return out


def micro_rates(bits, blades: int, rule: str, r, a):
    n = 2 * blades + 1
    adjacency = [[] for _ in range(n)]
    degree = [sp.Integer(0) for _ in range(n)]
    for u, v, w in edges(blades, a):
        adjacency[u].append((v, w))
        adjacency[v].append((u, w))
        degree[u] += w
        degree[v] += w

    ans = defaultdict(lambda: sp.Integer(0))
    if rule == "Bd":
        for u in range(n):
            fitness_u = r if bits[u] else 1
            for v, w in adjacency[u]:
                if bits[u] == bits[v]:
                    continue
                changed = list(bits)
                changed[v] = bits[u]
                ans[lump(tuple(changed), blades)] += fitness_u * w / degree[u]
    else:
        for v in range(n):
            denominator = sum(
                (r if bits[u] else 1) * w for u, w in adjacency[v]
            )
            for u, w in adjacency[v]:
                if bits[u] == bits[v]:
                    continue
                changed = list(bits)
                changed[v] = bits[u]
                ans[lump(tuple(changed), blades)] += (
                    (r if bits[u] else 1) * w / denominator
                )
    return dict(ans)


def predicted_rates(state, blades: int, rule: str, r, a):
    z, h, k = state
    resident = blades - h - k
    ans = defaultdict(lambda: sp.Integer(0))

    def add(new_state, rate):
        if rate != 0:
            ans[new_state] += rate

    if rule == "Bd":
        add(
            (z, h - 1, k + 1),
            h * (r / (1 + a) + (r / (2 * blades) if z else 0)),
        )
        add(
            (z, h - 1, k),
            h * (1 / (1 + a) + (1 / (2 * blades) if not z else 0)),
        )
        if z:
            add((z, h + 1, k), r * resident / blades)
            add((0, h, k), a * (h + 2 * resident) / (1 + a))
        else:
            add((z, h + 1, k - 1), k / blades)
            add((1, h, k), r * a * (h + 2 * k) / (1 + a))
    else:
        add(
            (z, h - 1, k + 1),
            h * (1 if z else r / (r + a)),
        )
        add(
            (z, h - 1, k),
            h * (1 / (1 + r * a) if z else 1),
        )
        if z:
            add((z, h + 1, k), 2 * resident * r * a / (1 + r * a))
        else:
            add((z, h + 1, k - 1), 2 * k * a / (r + a))
        denominator = r * (h + 2 * k) + h + 2 * resident
        if denominator:
            if z:
                add((0, h, k), (h + 2 * resident) / denominator)
            else:
                add((1, h, k), r * (h + 2 * k) / denominator)
    return dict(ans)


def check_symbolic_lumpability() -> None:
    blades = 3
    r, a = sp.symbols("r a", positive=True)
    representatives = {}
    for mask in range(1 << (2 * blades + 1)):
        bits = tuple((mask >> j) & 1 for j in range(2 * blades + 1))
        state = lump(bits, blades)
        for rule in ("Bd", "dB"):
            rates = micro_rates(bits, blades, rule, r, a)
            expected = predicted_rates(state, blades, rule, r, a)
            keys = set(rates) | set(expected)
            for key in keys:
                assert sp.factor(rates.get(key, 0) - expected.get(key, 0)) == 0
            rep_key = rule, state
            canonical = tuple(
                sorted((key, sp.factor(value)) for key, value in rates.items())
            )
            if rep_key in representatives:
                old = dict(representatives[rep_key])
                for key in set(old) | set(rates):
                    assert sp.factor(old.get(key, 0) - rates.get(key, 0)) == 0
            else:
                representatives[rep_key] = canonical
    print("PASS: exact symbolic microstate lumpability for Bd and dB")


def finite_fixation(blades: int, r: float, c: float, rule: str) -> float:
    a = c / blades
    transient = []
    for z in (0, 1):
        for h in range(blades + 1):
            for k in range(blades - h + 1):
                state = (z, h, k)
                if state not in ((0, 0, 0), (1, 0, blades)):
                    transient.append(state)
    index = {state: j for j, state in enumerate(transient)}
    matrix = lil_matrix((len(transient), len(transient)))
    rhs = np.zeros(len(transient))

    for state, row in index.items():
        rates = predicted_rates(state, blades, rule, r, a)
        total = float(sum(rates.values()))
        matrix[row, row] = total
        for new_state, rate in rates.items():
            rate = float(rate)
            if new_state == (1, 0, blades):
                rhs[row] += rate
            elif new_state != (0, 0, 0):
                matrix[row, index[new_state]] -= rate
    solution = spsolve(matrix.tocsr(), rhs)
    center_start = solution[index[(1, 0, 0)]]
    blade_start = solution[index[(0, 1, 0)]]
    return float((center_start + 2 * blades * blade_start) / (2 * blades + 1))


def limiting_values(r: float, c: float) -> tuple[float, float]:
    bd = 2 * c * (r**3 - 1) / (r * (1 + 2 * r * (r + 1) * c))
    db = (r**3 - 1) / (2 * r * (r**2 + c))
    return bd, db


def convergence_diagnostic() -> None:
    r, c = 1.5, 0.5
    bd_limit, db_limit = limiting_values(r, c)
    print(f"predicted limits at r={r}, c={c}: Bd={bd_limit:.12f}, dB={db_limit:.12f}")
    errors = []
    for blades in (10, 20, 40, 80):
        bd = finite_fixation(blades, r, c, "Bd")
        db = finite_fixation(blades, r, c, "dB")
        errors.append((abs(bd - bd_limit), abs(db - db_limit)))
        print(f"s={blades:3d}: Bd={bd:.12f}, dB={db:.12f}")
    assert errors[-1][0] < errors[0][0]
    assert errors[-1][1] < errors[0][1]
    print("PASS: full lumped chains converge toward the proved limits (diagnostic)")


if __name__ == "__main__":
    check_symbolic_lumpability()
    convergence_diagnostic()
