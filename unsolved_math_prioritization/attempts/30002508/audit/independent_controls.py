#!/usr/bin/env python3
"""Independent standard-library rational audit. No network or original writes.

The witness is rebuilt by midpoint evaluation on a common partition, rather
than the author's sweep/event algorithm. Generator pairings use a global
fractional-part primitive, rather than splitting at generator jumps. Mobius
values use divisor recursion, rather than prime factorization.
Run from any working directory: python3 /path/to/audit/independent_controls.py
"""
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


@lru_cache(None)
def mu(n):
    assert n >= 1
    return 1 if n == 1 else -sum(mu(d) for d in range(1, n) if n % d == 0)


def floor(x):
    return x.numerator // x.denominator


def integral_power(lo, hi, degree):
    return F(0) if lo >= hi else (hi ** (degree + 1) - lo ** (degree + 1)) / (degree + 1)


def psi(x, q, eps):
    if q - eps < x < q:
        return -1 / eps
    if q < x < q + eps:
        return 1 / eps
    return F(0)


def integrate_psi_power(q, eps, lo, hi, degree):
    return sum((sgn / eps * integral_power(max(lo, a), min(hi, b), degree)
                for a, b, sgn in [(q - eps, q, -1), (q, q + eps, 1)]), F(0))


def rebuild(q, eps, omit_n=False):
    q, eps = F(q), F(eps)
    assert q > 1 and 0 < eps < min(1, q - 1)
    last = floor(q + eps)
    # Integrate A on intervals split at ALL integer jumps of sum mu(n)/n.
    breaks = sorted({q - eps, q, q + eps} |
                    {F(n) for n in range(1, last + 1) if q - eps < n < q + eps})
    A = F(0)
    for a, b in zip(breaks, breaks[1:]):
        mid = (a + b) / 2
        coeff = sum((F(mu(n), n) for n in range(1, floor(mid) + 1)), F(0))
        A += coeff * psi(mid, q, eps) * integral_power(a, b, 1)
    points = sorted({F(1), q + eps} |
                    {t / n for n in range(1, last + 1)
                     for t in (q - eps, q, q + eps) if t / n > 1})
    pieces = []
    for a, b in zip(points, points[1:]):
        mid = (a + b) / 2
        k = -sum((mu(n) * (1 if omit_n else n) * psi(n * mid, q, eps)
                  for n in range(1, last + 1)), F(0))
        if k:
            pieces.append((a, b, k))
    norm = A * A + sum((k * k * integral_power(a, b, 2) for a, b, k in pieces), F(0))
    return A, pieces, norm


def fractional_primitive(t, a):
    """Integral of {u/a} from 0 to t; valid also at integer multiples."""
    x = t / a
    n = floor(x)
    return a * (n + (x - n) ** 2) / 2


def pairing_generator(w, a):
    A, pieces, _ = w
    a = F(a)
    return A / a + sum((k * (fractional_primitive(hi, a) - fractional_primitive(lo, a))
                        for lo, hi, k in pieces), F(0))


def pairing_chi(w):
    return sum((k * (hi - lo) for lo, hi, k in w[1]), F(0))


def tent(q, eps, a):
    return max(F(0), 1 - abs(a - q) / eps)


def direct_chi_L(q, eps):
    # Integral of psi against -M(t), calculated from its jumps independently.
    return -sum((mu(n) * integrate_psi_power(q, eps, F(n), q + eps, 0)
                 for n in range(1, floor(q + eps) + 1)), F(0))


def pairing_test_function(w, lo, hi, degree):
    # f(u)=u^degree 1_(lo,hi). Degrees >=1 make every below-1 integral rational.
    A, pieces, _ = w
    below = A * integral_power(lo, min(hi, F(1)), degree - 1)
    return below + sum((k * integral_power(max(lo, a), min(hi, b), degree)
                        for a, b, k in pieces), F(0))


def direct_test_function_L(q, eps, lo, hi, degree):
    C = integral_power(lo, min(hi, F(1)), degree - 1)
    val = F(0)
    for n in range(1, floor(q + eps) + 1):
        val += F(mu(n), n) * C * integrate_psi_power(q, eps, F(n), q + eps, 1)
        val -= F(mu(n), n ** degree) * integrate_psi_power(
            q, eps, max(F(n), n * lo), min(q + eps, n * hi), degree)
    return val


def freeze_and_replay():
    frozen = ROOT / 'frozen_inputs'
    expected = {}
    for line in (frozen / 'SHA256SUMS').read_text().splitlines():
        digest, filename = line.split(maxsplit=1)
        actual = hashlib.sha256((frozen / filename).read_bytes()).hexdigest()
        assert actual == digest, filename
        expected[filename] = digest
    assert expected['PROOF.md'] == '6a2176d75e5bd5c53ccb75fd085674f272fefabf95046b56de82d9f79fe289d3'
    with tempfile.TemporaryDirectory(prefix='rank624-audit-') as temp:
        script = Path(temp) / 'verify_controls.py'
        shutil.copyfile(frozen / script.name, script)
        run = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, check=True)
        result = (Path(temp) / 'control_results.json').read_bytes()
        assert result == (frozen / 'control_results.json').read_bytes()
        assert json.loads(run.stdout) == json.loads(result)
    return expected, json.loads(result)


def negative_geometry():
    # E=<e1>, F=<e1,(0,1,1)>; genuine gain and genuine plateau.
    for x, expected_gain in [((2, 3, -1), F(2)), ((2, 1, -1), F(0))]:
        old = F(x[1] ** 2 + x[2] ** 2)
        gain = F((x[1] + x[2]) ** 2, 2)
        residual = (F(x[1]) - F(x[1] + x[2], 2), F(x[2]) - F(x[1] + x[2], 2))
        new = sum(t * t for t in residual)
        assert old - new == gain == expected_gain
    # Continuous generators alone allow right jumps: g_a=(1,max(0,a-2)).
    # At 2 the span is <e1>; at any 2+h it contains two independent vectors.
    for h in [F(1, n) for n in (2, 10, 100, 10000)]:
        assert h > 0 and (1 * h - 0 * 1) != 0
        assert h * h <= h  # squared generator displacement tends to 0
    # Infimum of continuous decreasing scalar approximants has a right jump.
    for n in range(1, 50):
        b = lambda x: max(F(0), 1 - n * max(F(0), x - 2))
        assert b(F(2)) == 1 and b(F(2) + F(1, n)) == 0
    return {'proper_space_plateau': True, 'projection_gain_identity': True,
            'continuous_generators_right_jump': True, 'continuous_infimum_right_jump': True}


def divisor_inverse_controls():
    # F(t)=Ct-f(t) for t>=1. The finite transform mu*F is inverted by 1*.
    examples = [
        (lambda t: F(int(t > 1)), F(0)),
        (lambda t: t - floor(t), F(1)),
        (lambda t: t / F(7, 3) - floor(t / F(7, 3)), F(3, 7)),
        (lambda t: t * t if t < 2 else F(0), F(1, 2)),
    ]
    count = 0
    for func, C in examples:
        def transformed(t):
            return sum((mu(n) * (C * t / n - func(t / n))
                        for n in range(1, floor(t) + 1)), F(0))
        for k in range(1, 201):
            t = 1 + F(k, 23)
            recovered = sum((transformed(t / n) for n in range(1, floor(t) + 1)), F(0))
            assert recovered == C * t - func(t)
            count += 1
    return count


def one_generator_controls():
    # Independent interval-by-interval integration. Tail is in [0,1/(N+1)].
    gamma = 0.577215664901532860606512090082402431
    N = 10000
    chi_partial = math.fsum(math.log1p(1 / n) - 1 / (n + 1) for n in range(1, N + 1))
    norm_partial = 1 + math.fsum(1 + n / (n + 1) - 2 * n * math.log1p(1 / n)
                               for n in range(1, N + 1))
    c, K = 1 - gamma, math.log(2 * math.pi) - gamma
    tail = 1 / (N + 1)
    assert chi_partial <= c <= chi_partial + tail
    assert norm_partial <= K <= norm_partial + tail
    assert 0 < c < 1 and K > 0
    endpoint = 1 - c * c / K
    rows = []
    for lam in (1.001, 1.1, 2, 5, 20):
        a = min(lam, math.exp(2 - c))
        ub = 1 - (math.log(a) + c) ** 2 / (a * K)
        assert ub < endpoint
        rows.append({'lambda': lam, 'one_generator_upper_bound_D_squared': ub})
    # Exact checks of dilation unitarity for compact polynomial functions.
    for scale, sqrt_scale in [(F(4), F(2)), (F(9, 4), F(3, 2))]:
        for lo, hi in [(F(0), F(1)), (F(1, 2), F(5, 2)), (F(2), F(9))]:
            for d in (1, 2, 3):
                old = integral_power(lo, hi, 2 * d - 2)
                coeff = sqrt_scale / scale ** d
                new = coeff ** 2 * integral_power(scale * lo, scale * hi, 2 * d - 2)
                assert new == old
    return {'status': 'passed; floating sanity checks plus exact dilation tests',
            'tail_bound': tail, 'chi_integral_enclosure': [chi_partial, chi_partial + tail],
            'norm_integral_enclosure': [norm_partial, norm_partial + tail],
            'endpoint_D_squared': endpoint, 'upper_bounds': rows,
            'exact_dilation_tests': 18}


def run():
    bindings, replay = freeze_and_replay()
    replay_count = sum(row['rational_generator_tests'] for row in replay['prime_witnesses'])
    assert replay_count == 701
    mobius_cases = 0
    for k in range(1, 4001):
        x = F(k, 17)
        assert sum(mu(n) * floor(x / n) for n in range(1, floor(x) + 1)) == int(x >= 1)
        mobius_cases += 1
    original = {F(row['squarefree_center']): row for row in replay['prime_witnesses']}
    cases = [(q, F(1, 4)) for q in (2, 3, 5, 7, 11)]
    cases += [(F(4), F(1, 4)), (F(6), F(1, 4)), (F(7, 3), F(1, 10)),
              (F(11, 10), F(1, 20)), (F(5, 2), F(3, 4)), (F(33, 10), F(1, 2)),
              (F(13), F(3, 4)), (F(17), F(1, 100))]
    rows = []
    pairings = riesz_cases = cutoff_cases = 0
    for q, eps in cases:
        q, eps = F(q), F(eps)
        w = rebuild(q, eps)
        assert w[2] > 0
        chi = pairing_chi(w)
        assert chi == direct_chi_L(q, eps)
        alphas = {F(1) + F(j, 37) for j in range(floor(37 * (q + eps)) + 2)}
        alphas |= {q - eps, q - eps / 2, q, q + eps / 2, q + eps}
        for a in sorted(alphas):
            assert pairing_generator(w, a) == tent(q, eps, a), (q, eps, a)
            pairings += 1
            cutoff_cases += a <= q - eps
        if q in original and eps == F(1, 4):
            row = original[q]
            assert w[0] == F(row['A']) and w[2] == F(row['h_norm_squared'])
            assert chi == F(row['h_chi']) == 1
        for lo, hi in [(F(0), F(1)), (F(1, 4), F(3, 4)), (F(1, 2), F(5, 2)),
                       (F(1), F(4)), (F(7, 3), F(17, 3)), (F(20), F(21))]:
            for degree in (1, 2, 3):
                assert pairing_test_function(w, lo, hi, degree) == direct_test_function_L(q, eps, lo, hi, degree)
                riesz_cases += 1
        rows.append({'q': str(q), 'epsilon': str(eps), 'A': str(w[0]),
                     'h_norm_squared': str(w[2]), 'h_chi': str(chi),
                     'valid_D_squared_bound': str(chi * chi / w[2]) if chi else None})
    w = rebuild(F(2), F(1, 4))
    # Concrete mutations must be caught: omission of the Jacobian n or A.
    assert pairing_generator(rebuild(F(2), F(1, 4), omit_n=True), F(1)) != 0
    no_A = (F(0), w[1], w[2] - w[0] ** 2)
    assert pairing_generator(no_A, F(1)) != 0
    # A positive witness pairing with e_q is NOT enough for a distance drop.
    for q, eps in [(F(4), F(1, 4)), (F(7, 3), F(1, 10))]:
        witness = rebuild(q, eps)
        assert pairing_generator(witness, q) == 1 and pairing_chi(witness) == 0
    # Generator annihilation stops exactly at q-eps, so reject overbroad cutoff.
    assert pairing_generator(w, F(15, 8)) == F(1, 2)
    return {'status': 'passed', 'target_status': 'unsolved', 'frozen_bindings': bindings,
            'replay_byte_identical': True, 'replayed_original_generator_checks': replay_count,
            'independent_mobius_identity_checks': mobius_cases,
            'independent_generator_pairings': pairings, 'independent_cutoff_annihilations': cutoff_cases,
            'independent_Riesz_function_tests': riesz_cases, 'witness_cases': rows,
            'mutation_controls': ['omit n Jacobian rejected', 'omit below-1 A rejected',
                                  'extend annihilation past q-epsilon rejected',
                                  'generator separation implies target gain rejected'],
            'geometry_controls': negative_geometry(),
            'independent_divisor_inversion_checks': divisor_inverse_controls(),
            'one_generator_controls': one_generator_controls(),
            'limitations': ['finite tests do not prove a continuum assertion',
                            'no test resolves right continuity or arbitrary strict decrease',
                            'floating checks are sanity checks, not rigorous interval arithmetic']}


if __name__ == '__main__':
    result = run()
    path = ROOT / 'independent_results.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
