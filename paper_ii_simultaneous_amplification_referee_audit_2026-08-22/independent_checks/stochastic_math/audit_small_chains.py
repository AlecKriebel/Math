#!/usr/bin/env python3
"""Independent finite-chain checks for the stochastic mathematics audit.

This script uses only the Python standard library.  It constructs transition
rates directly from the labelled Bd and dB update rules; no manuscript or
certificate code is imported.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F


def graph_hybrid(C: int, m: int, q: int, W: F, eps: F):
    n = C + m + 2 * q
    w = [[F(0) for _ in range(n)] for _ in range(n)]

    def edge(u, v, weight):
        w[u][v] = w[v][u] = weight

    for u in range(C):
        for v in range(u + 1, C):
            edge(u, v, F(1))
    for j in range(m):
        edge(0, C + j, F(1))
    p0 = C + m
    for a in range(q):
        u, v = p0 + 2 * a, p0 + 2 * a + 1
        edge(u, v, W)
        for x in range(C):
            edge(u, x, eps)
            edge(v, x, eps)
    return w


def graph_center(C: int, m: int):
    return graph_hybrid(C, m, 0, F(1), F(0))


def graph_pair(W: F):
    return [[F(0), W], [W, F(0)]]


def changing_rates(mask: int, w, r: F, update: str):
    """Return off-diagonal continuous-time rates, with a harmless time change."""
    n = len(w)
    typ = [(mask >> u) & 1 for u in range(n)]
    fit = [r if typ[u] else F(1) for u in range(n)]
    out = defaultdict(F)
    if update == "Bd":
        degrees = [sum(row) for row in w]
        for u in range(n):
            for v in range(n):
                if w[u][v] and typ[u] != typ[v]:
                    new = mask | (1 << v) if typ[u] else mask & ~(1 << v)
                    out[new] += fit[u] * w[u][v] / degrees[u]
    elif update == "dB":
        for v in range(n):
            denominator = sum(fit[u] * w[u][v] for u in range(n))
            for u in range(n):
                if w[u][v] and typ[u] != typ[v]:
                    new = mask | (1 << v) if typ[u] else mask & ~(1 << v)
                    out[new] += fit[u] * w[u][v] / denominator
    else:
        raise ValueError(update)
    return dict(out)


def solve_fixation(w, r: F, update: str):
    """Dense Gaussian solve of the harmonic system (small graphs only)."""
    n = len(w)
    full = (1 << n) - 1
    transient = list(range(1, full))
    pos = {s: j for j, s in enumerate(transient)}
    size = len(transient)
    aug = [[0.0] * (size + 1) for _ in range(size)]
    for s in transient:
        row = pos[s]
        rates = changing_rates(s, w, r, update)
        total = float(sum(rates.values()))
        aug[row][row] = total
        for dst, rate in rates.items():
            if dst == full:
                aug[row][-1] += float(rate)
            elif dst:
                aug[row][pos[dst]] -= float(rate)
    for col in range(size):
        pivot = max(range(col, size), key=lambda i: abs(aug[i][col]))
        if abs(aug[pivot][col]) < 1e-14:
            raise ArithmeticError("singular harmonic system")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        for j in range(col, size + 1):
            aug[col][j] /= scale
        for i in range(size):
            if i == col:
                continue
            scale = aug[i][col]
            if scale:
                for j in range(col, size + 1):
                    aug[i][j] -= scale * aug[col][j]
    h = [0.0] * (full + 1)
    h[full] = 1.0
    for s in transient:
        h[s] = aug[pos[s]][-1]
    return h


def orbit_label(mask: int, C: int, m: int, q: int):
    h = mask & 1
    i = sum((mask >> x) & 1 for x in range(1, C))
    ell = sum((mask >> (C + j)) & 1 for j in range(m))
    p0 = C + m
    mixed = full = 0
    for a in range(q):
        k = ((mask >> (p0 + 2 * a)) & 1) + ((mask >> (p0 + 2 * a + 1)) & 1)
        mixed += k == 1
        full += k == 2
    return int(bool(h)), i, mixed, full, ell


def aggregated_generator(mask, w, r, update, labeler):
    rates = changing_rates(mask, w, r, update)
    out = defaultdict(F)
    total = sum(rates.values())
    out[labeler(mask)] -= total
    for dst, rate in rates.items():
        out[labeler(dst)] += rate
    return dict(out)


def check_lumping():
    C, m, q = 3, 2, 2
    w = graph_hybrid(C, m, q, F(7, 2), F(2, 13))
    labeler = lambda s: orbit_label(s, C, m, q)
    for update in ("Bd", "dB"):
        representatives = {}
        for mask in range(1 << len(w)):
            label = labeler(mask)
            row = aggregated_generator(mask, w, F(7, 5), update, labeler)
            if label in representatives and row != representatives[label]:
                raise AssertionError((update, label, row, representatives[label]))
            representatives[label] = row
        print(f"strong_lumping_{update}=PASS fibres={len(representatives)} states={1 << len(w)}")


def expected_center_table(label, C, m, r, update):
    h, i, _, _, ell = label
    c, d = C - 1, C - 1 + m
    result = defaultdict(F)

    def add(target, value):
        if value:
            result[target] += value

    if update == "Bd":
        add((h, i + 1, 0, 0, ell), r * (c - i) * (F(h, d) + F(i, c)))
        add((h, i - 1, 0, 0, ell), i * (F(1 - h, d) + F(c - i, c)))
        if h == 0:
            add((1, i, 0, 0, ell), r * (F(i, c) + ell))
        else:
            add((0, i, 0, 0, ell), F(c - i, c) + m - ell)
        add((h, i, 0, 0, ell + 1), r * h * F(m - ell, d))
        add((h, i, 0, 0, ell - 1), (1 - h) * F(ell, d))
    else:
        add((h, i + 1, 0, 0, ell), (c - i) * F(r * (h + i), c + (r - 1) * (h + i)))
        add((h, i - 1, 0, 0, ell), i * F(c - i + 1 - h, c + (r - 1) * (i - 1 + h)))
        if h == 0:
            add((1, i, 0, 0, ell), F(r * (i + ell), d + (r - 1) * (i + ell)))
        else:
            add((0, i, 0, 0, ell), F(d - i - ell, d + (r - 1) * (i + ell)))
        add((h, i, 0, 0, ell + 1), h * (m - ell))
        add((h, i, 0, 0, ell - 1), (1 - h) * ell)
    return {key: value for key, value in result.items() if value}


def check_center_tables():
    C, m, r = 5, 3, F(11, 7)
    w = graph_center(C, m)
    labeler = lambda s: orbit_label(s, C, m, 0)
    for update in ("Bd", "dB"):
        for mask in range(1 << len(w)):
            label = labeler(mask)
            actual = defaultdict(F)
            for dst, rate in changing_rates(mask, w, r, update).items():
                actual[labeler(dst)] += rate
            expected = expected_center_table(label, C, m, r, update)
            if dict(actual) != expected:
                raise AssertionError((update, label, dict(actual), expected))
        print(f"center_intensity_table_{update}=PASS states={1 << len(w)}")


def complete_baselines():
    for update in ("Bd", "dB"):
        for n in range(2, 8):
            w = [[F(int(u != v)) for v in range(n)] for u in range(n)]
            r = F(3, 2)
            h = solve_fixation(w, r, update)
            observed = sum(h[1 << v] for v in range(n)) / n
            if update == "Bd":
                expected = float((1 - 1 / r) / (1 - r ** (-n)))
            else:
                expected = float(F(n - 1, n) * (1 - 1 / r) / (1 - r ** (-(n - 1))))
            if abs(observed - expected) > 2e-11:
                raise AssertionError((update, n, observed, expected))
        print(f"complete_baseline_{update}=PASS n=2..7")


def separated_trace(C, m, W, r, update):
    center = graph_center(C, m)
    pair = graph_pair(W)
    hc = solve_fixation(center, r, update)
    hp = solve_fixation(pair, r, update)
    hcr = solve_fixation(center, 1 / r, update)
    hpr = solve_fixation(pair, 1 / r, update)
    aH = sum(hc[1 << x] for x in range(C + m)) / (C + m)
    aP = (hp[1] + hp[2]) / 2
    degrees_c = [sum(row) for row in center]
    I_H = sum(1 / degrees_c[x] for x in range(C))
    J_H = sum(F.from_float(hc[1 << x]) / degrees_c[x] for x in range(C))
    J_H_rec = sum(F.from_float(hcr[1 << x]) / degrees_c[x] for x in range(C))
    I_P = F(2, 1) / W
    J_P = F(1, 1) / W
    u_core = sum(hc[1 << x] for x in range(C)) / C
    u_core_rec = sum(hcr[1 << x] for x in range(C)) / C
    if update == "Bd":
        A = float(C * r * I_P) * u_core
        D = float(2 * I_H) * ((hpr[1] + hpr[2]) / 2)
        B = float(2 * r * I_H) * aP
        Cp = float(C * I_P) * u_core_rec
    else:
        A = float(2 * r * J_H)
        # J_P already sums the two singleton committors divided by W.
        D = float(F(C, 1) / r * J_P)
        B = float(C * r * J_P)
        Cp = float(F(2, 1) / r * J_H_rec)
    PH = B / (B + Cp)
    PP = A / (A + D)
    N = C + m + 2
    rho0 = (C + m) / N * aH * PH + 2 / N * aP * PP
    return rho0, (A, D, B, Cp, PH, PP)


def check_weak_cut():
    C, m, q = 3, 1, 1
    W, r = F(7, 2), F(8, 5)
    for update in ("Bd", "dB"):
        rho0, rates = separated_trace(C, m, W, r, update)
        errors = []
        for denominator in (10, 100, 1000, 10000):
            eps = F(1, denominator)
            w = graph_hybrid(C, m, q, W, eps)
            h = solve_fixation(w, r, update)
            rho = sum(h[1 << v] for v in range(len(w))) / len(w)
            errors.append(abs(rho - rho0))
        if not all(errors[j + 1] < errors[j] for j in range(len(errors) - 1)):
            raise AssertionError((update, errors))
        print(
            f"weak_cut_{update}=PASS rho0={rho0:.12f} "
            f"errors=" + ",".join(f"{x:.3e}" for x in errors)
        )
        A, D, B, Cp, PH, PP = rates
        print(
            f"macro_{update}: A/D={A / D:.12f} Cprime/B={Cp / B:.12f} "
            f"PH={PH:.12f} PP={PP:.12f}"
        )


def check_gate_limits_and_responses():
    # Exact rational evaluations of the independently derived limiting formulas.
    for r, sigma, lam in ((F(3, 2), F(19, 137), F(20, 27)), (F(7, 5), F(1, 6), F(2, 3))):
        p = 1 - 1 / r
        ZB = sigma * (r * r - 1)
        ZD = 2 * r * (r - 1) / sigma
        pairB = F(2) * ((r / (r + 1)) * (ZB / (1 + ZB)) / p - 1)
        pairD = F(2) * (F(1, 2) * (ZD / (1 + ZD)) / p - 1)
        responseB = pairB + lam / (r - 1)
        responseD = pairD - lam
        closedB = 2 * (sigma - 1) / (1 + sigma * (r * r - 1)) + lam / (r - 1)
        closedD = 2 * (r * (2 - r) - sigma) / (sigma + 2 * r * (r - 1)) - lam
        assert responseB == closedB and responseD == closedD
        print(
            f"response_identity=PASS r={r} sigma={sigma} lambda={lam} "
            f"B={responseB} D={responseD} ZB={ZB} ZD={ZD}"
        )


def main():
    complete_baselines()
    check_lumping()
    check_center_tables()
    check_weak_cut()
    check_gate_limits_and_responses()


if __name__ == "__main__":
    main()
