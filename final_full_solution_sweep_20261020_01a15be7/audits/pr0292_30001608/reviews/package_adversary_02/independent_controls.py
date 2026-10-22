"""Fresh package-review controls. Standard library only; imports no candidate code.

The Poisson solution and its mean are simultaneous unknowns in a full linear
system, solved by generic Gaussian elimination. These finite controls supplement
the separate analytic proof review; they do not prove universal quantifiers.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

COUNTS = Counter()


def check(condition, label):
    if not condition:
        raise RuntimeError(label)
    COUNTS[label] += 1


def ceiling(q):
    return -((-q.numerator) // q.denominator)


def gaussian(matrix, target):
    """Generic elimination, with exact arithmetic and no tridiagonal shortcut."""
    a = [list(row) + [rhs] for row, rhs in zip(matrix, target)]
    size = len(a)
    for col in range(size):
        pivot = next(row for row in range(col, size) if a[row][col])
        a[col], a[pivot] = a[pivot], a[col]
        for row in range(col + 1, size):
            if not a[row][col]:
                continue
            scale = a[row][col] / a[col][col]
            for j in range(col, size + 1):
                a[row][j] -= scale * a[col][j]
    values = [F(0)] * size
    for row in reversed(range(size)):
        values[row] = (a[row][-1] - sum(a[row][j] * values[j]
                                      for j in range(row + 1, size))) / a[row][row]
    return values


class Certificate:
    def __init__(self, lam):
        self.lam = lam
        self.beta = F(17, 8) * lam
        self.c = 2 * (self.beta + 4)
        self.m = 4 * self.c
        self.theta = self.beta + self.c + 4
        self.gamma = (self.theta + 1) / (self.theta + 2)
        self.eta = (1 + self.gamma) / 2
        self.ell = 1 / (self.eta - self.gamma)
        R = 1
        while True:
            weights = [self.gamma ** k for k in range(R + 1)]
            mean = sum(k * w for k, w in enumerate(weights)) / sum(weights)
            if mean > self.theta and F(7, 8) * (R + 1) > self.beta + self.c + 2:
                break
            R += 1
        self.R = R
        # Unknowns are g(0),...,g(R-1),mu; g(R)=0. Include the terminal row.
        rows, rhs = [], []
        for k in range(R + 1):
            row = [F(0)] * (R + 1)
            if k < R:
                birth = self.gamma * (k + 1)
                row[k] -= birth
                if k + 1 < R:
                    row[k + 1] += birth
            if k:
                row[k - 1] += k
                if k < R:
                    row[k] -= k
            row[-1] = 1
            rows.append(row)
            rhs.append(F(k))
        solved = gaussian(rows, rhs)
        self.gs, self.mu = solved[:-1] + [F(0)], solved[-1]
        check(self.mu == mean, 'simultaneous_mean_matches_geometric_mean')
        self.G = self.gs[0]
        self.N = ceiling(max(F(R + 2), F(3 * (R + 1)),
                             (self.m + (1 + self.eta) * R + self.eta) / (1 - self.eta),
                             self.ell * self.G * (lam + 4 * (2 * R + 1))))
        self.B = (self.N + R + 1) * (self.beta + self.c + self.G *
                                   (lam + 2 * (self.N + R)) + 1)

    def g(self, k):
        check(k >= 0, 'g_nonnegative_argument')
        return self.gs[k] if k < self.R else F(0)

    def f(self, t):
        return max(F(0), min(F(1), self.ell * (t - self.gamma)))

    def h(self, z):
        return z * z / (2 * self.m) + self.m / 2 if abs(z) <= self.m else abs(z)

    def hp(self, z):
        return min(F(1), max(F(-1), z / self.m))

    def values(self, s):
        a, b, x, y = s
        D = x + y + 1
        W, Z = 2 * (a + b) + x + y, a + x - b - y
        f = (self.f(F(b, D)), self.f(F(a, D)))
        g = (self.g(y), self.g(x))
        J = sum(v * w for v, w in zip(f, g))
        return W, Z, f, g, J, W + self.c * self.h(F(Z)) + J


def events(s, lam):
    a, b, x, y = s
    D = x + y + 1
    rates = (lam / 2, lam / 2, F(a * (x + 1), D), F(b * (y + 1), D),
             F(x * (y + 1), D), F(y * (x + 1), D))
    vectors = ((1, 0, 0, 0), (0, 1, 0, 0), (-1, 0, 1, 0),
               (0, -1, 0, 1), (0, 0, -1, 0), (0, 0, 0, -1))
    return [(i, rate, tuple(v + dv for v, dv in zip(s, delta)))
            for i, (rate, delta) in enumerate(zip(rates, vectors)) if rate]


def inspect(s, cert, regions):
    a, b, x, y = s
    D = x + y + 1
    old = cert.values(s)
    W, Z, fs, gs, J, V = old
    u, d = F(a * (x + 1) + b * (y + 1), D), F(2 * x * y + x + y, D)
    LW = LZ = LH = LJ = LV = error = principal = F(0)
    for kind, rate, after in events(s, cert.lam):
        check(min(after) >= 0, 'valid_event')
        wt, zt, ft, gt, jt, vt = cert.values(after)
        LW += rate * (wt - W)
        LZ += rate * (zt - Z)
        LH += rate * (cert.h(F(zt)) - cert.h(F(Z)))
        LJ += rate * (jt - J)
        LV += rate * (vt - V)
        e = sum(g * (new - pre) for g, new, pre in zip(gt, ft, fs))
        p = sum(f * (new - pre) for f, new, pre in zip(fs, gt, gs))
        check(jt - J == e + p, 'postjump_product_identity')
        error += rate * e
        principal += rate * p
        if kind in (2, 3):
            check(e <= 0 and jt <= J, 'first_download_both_signs')
        if kind in (4, 5):
            check(all(0 <= new - pre <= 2 * cert.ell / D
                      for new, pre in zip(ft, fs)), 'departure_cutoff_bound')
    check(LW == 2 * cert.lam - u - d, 'physical_workload_generator')
    check(LZ == F(y - x, D), 'cohort_generator')
    check(LH <= cert.hp(F(Z)) * LZ + (cert.lam + d) / (2 * cert.m), 'rounded_generator')
    check(LJ == principal + error, 'generator_product_identity')
    check(error <= cert.ell * cert.G * (cert.lam + 4 * d) / D, 'interface_upper_bound')
    check(LJ <= cert.G * (cert.lam + 2 * d), 'coarse_upper_bound')
    check(sum(s) <= W <= V <= (1 + cert.c) * W + cert.c * cert.m / 2 + 2 * cert.G,
          'coercivity_and_exact_paper_linear_upper_bound')
    if min(x, y) > cert.R:
        regions['both_large'] += 1
        check(LJ == 0 and LV < -2, 'both_large_full_drift')
    elif max(x, y) >= cert.N:
        regions['corner'] += 1
        check(LV <= -3, 'corner_full_drift')
    else:
        regions['strip'] += 1
        check(x + y <= cert.N + cert.R, 'coverage')
        if a + b > cert.B:
            regions['strip_outside_F'] += 1
            check(LV <= -1, 'strip_full_drift')
    if x + y > cert.N + cert.R or a + b > cert.B:
        check(LV <= -1, 'outside_F_full_drift')


def support_tests(cert):
    for k in range(cert.R + 2):
        result = cert.gamma * (k + 1) * (cert.g(k + 1) - cert.g(k)) if k < cert.R else F(0)
        if k:
            result += k * (cert.g(k - 1) - cert.g(k))
        check(result == k - cert.mu if k <= cert.R else result == 0, 'all_poisson_rows_and_extension')
        check(cert.g(k) >= 0, 'g_nonnegative')
        if k < cert.R:
            check(cert.g(k) > cert.g(k + 1), 'g_strictly_decreasing')
    for sign in (-1, 1):
        for delta, jump in product((F(-4, 3), F(-1, 7), F(0), F(1, 7), F(4, 3)),
                                   (F(-2), F(-1), F(1), F(2))):
            z = sign * cert.m + delta
            check(cert.h(z + jump) - cert.h(z) <= cert.hp(z) * jump + jump * jump / (2 * cert.m),
                  'noninteger_rounding_crossings')


def mutations(cert):
    witnesses = []
    # Replacing post-jump g in the exact identity by pre-jump g omits a cross term.
    found = None
    for D in range(2, 301):
        b = ceiling((cert.gamma + cert.eta) * D / 2)
        s, after = (0, b, D - 1, 0), (0, b - 1, D - 1, 1)
        old, new = cert.values(s), cert.values(after)
        wrong = sum(f * (gn - go) + go * (fn - f)
                    for f, fn, go, gn in zip(old[2], new[2], old[3], new[3]))
        if new[4] - old[4] != wrong:
            found = {'mutation': 'prejump_g_product_rule', 'state': s, 'after': after,
                     'missing_cross_term_positive': new[4] - old[4] > wrong}
            break
    check(found is not None and found['missing_cross_term_positive'], 'reject_prejump_product_mutation')
    witnesses.append(found)
    # A constant added only at R creates a nonzero R+1 down-jump.
    bad_g = lambda k: F(1) if k == cert.R else cert.g(k)
    boundary = (0, 0, 0, cert.R + 1)
    mutated_Lg = sum(rate * (bad_g(after[3]) - bad_g(boundary[3]))
                     for _, rate, after in events(boundary, cert.lam))
    check(mutated_Lg > 0, 'reject_nonzero_terminal_extension_mutation')
    witnesses.append({'mutation': 'set_g_R_to_1', 'state': boundary,
                      'actual_mutated_Lg': str(mutated_Lg), 'claimed_extension_value': '0'})
    # Arrival clock normalization would violate the physical generator at zero.
    embedded_LW = F(2)
    physical_LW = 2 * cert.lam
    check(embedded_LW != physical_LW, 'reject_embedded_clock_mutation')
    witnesses.append({'mutation': 'normalize_rates_to_total_one', 'state': [0, 0, 0, 0],
                      'physical_LW': str(physical_LW), 'normalized_LW': str(embedded_LW)})
    return witnesses


def run():
    rows, negatives = [], []
    for lam in (F(1, 19), F(17, 11), F(7, 2)):
        c = Certificate(lam)
        support_tests(c)
        states = set(product(range(3), repeat=4))
        for x in (c.R, c.R + 1, c.N - 1, c.N, c.N + 1):
            for y in (0, c.R - 1, c.R, c.R + 1):
                D = x + y + 1
                bs = {0, max(0, ceiling(c.gamma * D) - 1), ceiling(c.gamma * D),
                      max(0, ceiling(c.eta * D) - 1), ceiling(c.eta * D), D * D}
                for b in bs:
                    for a in (0, D * D):
                        states.add((a, b, x, y))
                        states.add((b, a, y, x))
        for x, y in ((0, 0), (c.R, c.R), (c.N - 1, c.R)):
            for wait in (ceiling(c.B) - 1, ceiling(c.B), ceiling(c.B) + 1):
                for a, b in ((wait, 0), (0, wait), (wait // 2, wait - wait // 2)):
                    states.add((a, b, x, y))
        regions = Counter()
        for s in sorted(states):
            inspect(s, c, regions)
        check(all(regions[k] > 0 for k in ('both_large', 'corner', 'strip', 'strip_outside_F')),
              'nonvacuous_region_coverage')
        negatives.extend({'lambda': str(lam), **v} for v in mutations(c))
        rows.append({'lambda': str(lam), 'R': c.R, 'N_digits': len(str(c.N)),
                     'states': len(states), 'regions': dict(regions),
                     'mean_minus_theta_positive': c.mu > c.theta})
    return {'status': 'PASS_FRESH_REVIEW_CONTROLS', 'loads': rows,
            'independent_poisson_method': 'Simultaneously solve every finite Qg+mu=k row with g(R)=0 by generic Gaussian elimination',
            'assertion_counts': dict(COUNTS), 'negative_controls': negatives,
            'scope': 'Finite exact falsification evidence only; no sample-to-real or sample-to-all-state inference.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
