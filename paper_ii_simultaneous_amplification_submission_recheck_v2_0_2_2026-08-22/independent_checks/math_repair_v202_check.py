#!/usr/bin/env python3
"""Independent exact-rational checks for the v2.0.2 stopped-time repair.

This file deliberately imports no manuscript or delivered verifier code.
It constructs the clique--pendant Bd chain directly from the displayed rates.
"""

from fractions import Fraction as F


def solve(matrix, rhs):
    """Solve a square rational system by Gauss--Jordan elimination."""
    n = len(rhs)
    aug = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col or not aug[row][col]:
                continue
            scale = aug[row][col]
            aug[row] = [
                aug[row][j] - scale * aug[col][j] for j in range(n + 1)
            ]
    return [aug[i][-1] for i in range(n)]


def bd_rates(c, m, r, state):
    """Return the six changing transitions from manuscript Table 1."""
    h, i, ell = state
    d = c + m
    out = []

    def add(rate, target, kind):
        if rate:
            out.append((rate, target, kind))

    if i < c:
        add(r * (c - i) * (F(h, d) + F(i, c)), (h, i + 1, ell), "core")
    if i > 0:
        add(i * (F(1 - h, d) + F(c - i, c)), (h, i - 1, ell), "core")
    if h == 0:
        add(r * (F(i, c) + ell), (1, i, ell), "hub")
    else:
        add(F(c - i, c) + m - ell, (0, i, ell), "hub")
    if h == 1 and ell < m:
        add(r * F(m - ell, d), (h, i, ell + 1), "up")
    if h == 0 and ell > 0:
        add(F(ell, d), (h, i, ell - 1), "down")
    return out


def stopped_system(c, m, r, exit_r):
    states = [
        (h, i, ell)
        for h in (0, 1)
        for i in range(c - exit_r + 1, c + 1)
        for ell in range(m + 1)
        if (h, ell) != (1, m)
    ]
    index = {state: j for j, state in enumerate(states)}
    matrix = [[F(0) for _ in states] for _ in states]
    rhs_time = [F(1) for _ in states]
    rhs_target = [F(0) for _ in states]
    for state, row in index.items():
        rates = bd_rates(c, m, r, state)
        total = sum((rate for rate, _, _ in rates), F(0))
        matrix[row][row] = total
        for rate, target, _ in rates:
            h2, i2, ell2 = target
            if c - i2 >= exit_r:
                continue
            if (h2, ell2) == (1, m):
                rhs_target[row] += rate
            else:
                matrix[row][index[target]] -= rate
    return states, solve(matrix, rhs_time), solve(matrix, rhs_target)


def next_outcome_system(c, m, r, exit_r, ell):
    states = [
        (h, i, ell)
        for h in (0, 1)
        for i in range(c - exit_r + 1, c + 1)
    ]
    index = {state: j for j, state in enumerate(states)}
    matrix = [[F(0) for _ in states] for _ in states]
    rhs = [F(0) for _ in states]
    for state, row in index.items():
        rates = bd_rates(c, m, r, state)
        total = sum((rate for rate, _, _ in rates), F(0))
        matrix[row][row] = total
        for rate, target, kind in rates:
            if kind == "up":
                rhs[row] += rate
            elif kind == "down":
                pass
            elif c - target[1] >= exit_r:
                rhs[row] += rate
            else:
                matrix[row][index[target]] -= rate
    return states, solve(matrix, rhs)


def target_before_extinction(c, m, r, start):
    extinction = (0, 0, 0)
    states = [
        (h, i, ell)
        for h in (0, 1)
        for i in range(c + 1)
        for ell in range(m + 1)
        if (h, i, ell) != extinction and (h, ell) != (1, m)
    ]
    index = {state: j for j, state in enumerate(states)}
    matrix = [[F(0) for _ in states] for _ in states]
    rhs = [F(0) for _ in states]
    for state, row in index.items():
        rates = bd_rates(c, m, r, state)
        total = sum((rate for rate, _, _ in rates), F(0))
        matrix[row][row] = total
        for rate, target, _ in rates:
            if target == extinction:
                continue
            if (target[0], target[2]) == (1, m):
                rhs[row] += rate
            else:
                matrix[row][index[target]] -= rate
    return solve(matrix, rhs)[index[start]]


def main():
    r = F(3, 2)
    cases = [(20, 3, 2), (40, 3, 3), (80, 4, 4)]
    for c, m, exit_r in cases:
        states, times, target_probs = stopped_system(c, m, r, exit_r)
        max_time = max(times)
        scale = (c + 1) * m
        print(
            "stopped",
            f"c={c}",
            f"m={m}",
            f"exit_R={exit_r}",
            f"states={len(states)}",
            f"max_E={float(max_time):.12g}",
            f"max_E/(Cm)={float(max_time / scale):.12g}",
            f"min_target_before_exit={float(min(target_probs)):.12g}",
        )
        if not all(time > 0 for time in times):
            raise RuntimeError("stopped hitting time was not strictly positive")
        if not all(F(0) <= value <= F(1) for value in target_probs):
            raise RuntimeError("invalid stopped target probability")

        for ell in range(m):
            outcome_states, favorable = next_outcome_system(c, m, r, exit_r, ell)
            if ell == 0:
                if any(value != 1 for value in favorable):
                    raise RuntimeError("ell=0 did not have certain up-or-exit outcome")
                print(f"  ell=0: all {len(favorable)} up-or-exit probabilities equal 1")
                continue
            min_p = min(favorable)
            min_odds = min_p / (1 - min_p)
            max_r_fraction = F(exit_r, c)
            h_plus = r * (1 - max_r_fraction + ell)
            h_minus = max_r_fraction + m - ell
            u = r * F(m - ell, c + m)
            v = F(ell, c + m)
            worst_odds = (h_plus * u) / (h_minus * v) / (1 + u / h_minus)
            if min_odds < worst_odds or worst_odds <= 1:
                raise RuntimeError("committor odds comparison failed")
            drift = 2 * min_p - 1
            print(
                f"  ell={ell}:",
                f"min_exact_odds={float(min_odds):.12g}",
                f"worst_rate_bound={float(worst_odds):.12g}",
                f"min_unit_step_drift={float(drift):.12g}",
            )

    old_start = (0, 3, 0)
    old_hit_probability = target_before_extinction(4, 2, r, old_start)
    print(
        "unstopped target check",
        f"start={old_start}",
        f"P(hit_(h,ell)=(1,m)_before_extinction)={float(old_hit_probability):.12g}",
        f"P(extinction_first)={float(1-old_hit_probability):.12g}",
    )
    if not F(0) < old_hit_probability < F(1):
        raise RuntimeError("expected a positive extinction-before-target probability")
    print("PASS: exact finite chains corroborate the stopped repair and ell=0 boundary")


if __name__ == "__main__":
    main()
