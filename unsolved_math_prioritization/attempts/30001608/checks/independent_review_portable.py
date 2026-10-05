"""Independent rational audit of the six-rate Foster certificate.

No author code is imported. The finite corrector is reconstructed backward
from its reflecting upper boundary, not from the author's prefix-sum formula.
The finite controls are falsification tests; the all-state review is separate.
"""
from fractions import Fraction as Q
from collections import Counter
from pathlib import Path
import hashlib
import json
import random
import sys

sys.set_int_max_str_digits(0)
checks = Counter()


def test(x, label):
    if not x:
        raise AssertionError(label)
    checks[label] += 1


def floor(x):
    return x.numerator // x.denominator


def ceil(x):
    return -((-x.numerator) // x.denominator)


def build(lam):
    beta = Q(17, 8) * lam
    c = 2 * beta + 8
    m = 4 * c
    theta = beta + c + 4
    gamma = (theta + 1) / (theta + 2)
    eta = (1 + gamma) / 2
    ell = 1 / (eta - gamma)
    R = 1
    while True:
        power = gamma ** (R + 1)
        mu = gamma / (1 - gamma) - (R + 1) * power / (1 - power)
        if mu > theta and Q(7, 8) * (R + 1) > beta + c + 2:
            break
        R += 1
    # Independent backward differences: at the upper boundary,
    # R (g(R-1)-g(R))=R-mu, with g(R)=0.
    delta = [Q(0)] * R
    delta[-1] = mu / R - 1
    for k in range(R - 1, 0, -1):
        delta[k - 1] = (gamma * (k + 1) * delta[k] - k + mu) / k
    gs = [Q(0)] * (R + 1)
    for k in range(R - 1, -1, -1):
        gs[k] = gs[k + 1] - delta[k]

    def g(k):
        return gs[k] if 0 <= k < R else Q(0)

    G = gs[0]
    N = ceil(max(Q(R + 2), Q(3 * (R + 1)),
                 (m + (1 + eta) * R + eta) / (1 - eta),
                 ell * G * (lam + 4 * (2 * R + 1))))
    B = (N + R + 1) * (beta + c + G * (lam + 2 * (N + R)) + 1)

    def cutoff(t):
        if t <= gamma:
            return Q(0)
        if t >= eta:
            return Q(1)
        return (t - gamma) / (eta - gamma)

    def smooth(z):
        return abs(z) if abs(z) >= m else (z * z + m * m) / (2 * m)

    def smooth_derivative(z):
        return max(Q(-1), min(Q(1), z / m))

    def fields(s):
        a, b, x, y = s
        D = x + y + 1
        W = 2 * (a + b) + x + y
        Z = a + x - b - y
        factors = (cutoff(Q(b, D)), cutoff(Q(a, D)))
        correctors = (g(y), g(x))
        J = sum(f * h for f, h in zip(factors, correctors))
        return W, Z, factors, correctors, J, W + c * smooth(Q(Z)) + J

    for k in range(R + 1):
        value = (gamma * (k + 1) * (g(k + 1) - g(k)) if k < R else 0)
        value += k * (g(k - 1) - g(k)) if k else 0
        test(value == k - mu, 'backward_poisson_all_states')
        test(g(k) >= 0, 'corrector_nonnegative')
        if k < R:
            test(g(k + 1) < g(k), 'corrector_strictly_decreasing')
    test(Q(0) < gamma < eta < Q(1), 'cutoff_parameters')
    test(mu > theta and mu < R, 'mean_bounds')
    test(N >= R + 2 and N >= 3 * (R + 1), 'visible_thresholds')
    test((1 - eta) * N - (1 + eta) * R - eta >= m, 'imbalance_threshold')
    test(ell * G * (lam + 4 * (2 * R + 1)) / N <= 1, 'interface_threshold')
    return locals()


def events(s, lam):
    a, b, x, y = s
    D = x + y + 1
    vectors = ((1, 0, 0, 0), (0, 1, 0, 0), (-1, 0, 1, 0),
               (0, -1, 0, 1), (0, 0, -1, 0), (0, 0, 0, -1))
    rates = (lam / 2, lam / 2, Q(a * (x + 1), D), Q(b * (y + 1), D),
             Q(x * (y + 1), D), Q(y * (x + 1), D))
    return [(j, tuple(z + dz for z, dz in zip(s, v)), rate)
            for j, (v, rate) in enumerate(zip(vectors, rates)) if rate > 0]


def inspect(s, p):
    lam, fields = p['lam'], p['fields']
    a, b, x, y = s
    D = x + y + 1
    W, Z, fs, gs, J, V = fields(s)
    u = Q(a * (x + 1) + b * (y + 1), D)
    d = Q(2 * x * y + x + y, D)
    sums = [Q(0)] * 6  # workload, imbalance, smooth, J, V, interface
    base = Q(0)
    for j, t, rate in events(s, lam):
        Wt, Zt, ft, gt, Jt, Vt = fields(t)
        sums[0] += rate * (Wt - W)
        sums[1] += rate * (Zt - Z)
        sums[2] += rate * (p['smooth'](Q(Zt)) - p['smooth'](Q(Z)))
        sums[3] += rate * (Jt - J)
        sums[4] += rate * (Vt - V)
        error = sum(h * (new - old) for h, new, old in zip(gt, ft, fs))
        principal = sum(f * (new - old) for f, new, old in zip(fs, gt, gs))
        test(Jt - J == error + principal, 'exact_postjump_product_rule')
        base += rate * principal
        sums[5] += rate * error
        if j in (2, 3):
            test(error <= 0, 'first_download_error_signed')
            test(Jt <= J, 'first_download_full_product_signed')
        if j in (4, 5):
            test(all(Q(0) <= new - old <= 2 * p['ell'] / D
                     for new, old in zip(ft, fs)), 'departure_interface_bound')
    test(sums[0] == 2 * lam - u - d, 'generator_workload')
    test(sums[1] == Q(y - x, D), 'generator_imbalance')
    test(sums[2] <= p['smooth_derivative'](Q(Z)) * Q(y - x, D)
         + (lam + d) / (2 * p['m']), 'smooth_generator_upper_bound')
    test(sums[5] <= p['ell'] * p['G'] * (lam + 4 * d) / D, 'total_interface_upper_bound')
    test(sums[3] == base + sums[5], 'generator_product_decomposition')
    test(sums[3] <= p['G'] * (lam + 2 * d), 'coarse_global_correction_bound')
    test(V >= sum(s), 'coercivity')
    if min(x, y) >= p['R'] + 1:
        test(sums[3] == 0, 'region_I_correction_zero')
        test(sums[4] < -2, 'region_I_drift')
    elif max(x, y) >= p['N']:
        test(sums[4] <= -3, 'region_II_drift')
    elif a + b > p['B']:
        test(sums[4] <= -1, 'region_III_drift')
    if x + y > p['N'] + p['R'] or a + b > p['B']:
        test(sums[4] <= -1, 'outside_F_drift')


def run():
    rng = random.Random(160830000048)
    reports = []
    for lam in (Q(1, 7), Q(7, 3), Q(13, 2)):
        p = build(lam)
        R, N, B = p['R'], p['N'], p['B']
        states = set()
        for _ in range(250):
            states.add(tuple(rng.randrange(2 * R + 2) for _ in range(4)))
        for y in (0, 1, R - 1, R, R + 1):
            for x in (N - 1, N, N + 1):
                D = x + y + 1
                waiting = {0, floor(p['gamma'] * D), ceil(p['gamma'] * D),
                           floor(p['eta'] * D), ceil(p['eta'] * D), 2 * D}
                for b in waiting:
                    for a in (0, D):
                        states.add((a, b, x, y))
                        states.add((b, a, y, x))
        big = ceil(B) + 1
        for x, y in ((0, 0), (0, R), (R, 0), (R, R), (N - 1, 0)):
            for a, b in ((big, 0), (0, big), (big // 2, big)):
                states.add((a, b, x, y))
        for x, y in ((R + 1, R + 1), (R + 1, R + 2), (N, R + 1)):
            for a, b in ((0, 0), (N, 0), (0, N), (big, big)):
                states.add((a, b, x, y))
        for s in states:
            inspect(s, p)
        reports.append({'lambda': str(lam), 'R': R, 'N': N,
                        'B_ceiling': ceil(B), 'states': len(states)})
        print('PASS lambda=' + str(lam), file=sys.stderr, flush=True)
    proof = (Path(__file__).resolve().parents[1] / 'TURN_4.md')
    return {'status': 'PASS_INDEPENDENT_RATIONAL_CONTROLS',
            'proof_sha256': hashlib.sha256(proof.read_bytes()).hexdigest(),
            'independent_method': 'Backward reflecting-boundary recurrence, no author imports',
            'total_assertions': sum(checks.values()), 'checks': dict(sorted(checks.items())),
            'loads': reports,
            'qualification': 'Finite falsification controls supplement the all-state analytic review; no finite sample alone proves recurrence.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
