#!/usr/bin/env python3
"""Supplementary controls, not a formal proof or an asymptotic certificate."""
from fractions import Fraction as Q
from math import comb, pi, sin, cos, log, sqrt
from pathlib import Path
import cmath
import hashlib
import json


def main():
    counts = {}
    n = 0
    for a in range(-30, 31):
        for b in range(-30, 31):
            A, D = max(a, 0), max(b, 0)
            loss, gain = max(A-D, 0), max(D-A, 0)
            assert A-D == loss-gain
            assert 0 <= gain <= max(b-a, 0)
            n += 1
    counts['loss_gain_scalar_cases'] = n

    n = 0
    for numerator in range(10, 41):
        s = Q(numerator, 20)
        for j in range(-20, 21):
            c = Q(j, 20)
            kernel_squared = (s-1)**2 + 2*s*(1-c)
            assert kernel_squared >= 1-c
            n += 1
    counts['fractional_kernel_algebra_cases'] = n

    n = 0
    zero_lists = [[0], [1], [-2, 0, 1], [1, 1, 1], [-3, -3, 2, 7]]
    for roots in zero_lists:
        for x in range(-5, 6):
            for y in list(range(-5, 0))+list(range(1, 6)):
                re = sum((Q(x-a, (x-a)**2+y*y) for a in roots), Q(0))
                im = sum((Q(-y, (x-a)**2+y*y) for a in roots), Q(0))
                assert im == -y*sum((Q(1, (x-a)**2+y*y) for a in roots), Q(0))
                for a in roots:
                    assert re*re+im*im >= Q(y*y, ((x-a)**2+y*y)**2)
                n += 1
    counts['real_zero_log_derivative_cases'] = n

    n = 0
    for N in range(3, 100, 6):
        coeff = [(-1)**k*comb(N, k) for k in range(N+1)]
        coeff[0] -= 1
        assert coeff[0] == 0
        derivative = [(k+1)*coeff[k+1] for k in range(N)]
        expected = [-N*(-1)**k*comb(N-1, k) for k in range(N)]
        assert derivative == expected
        assert (N//3) % 2 == 1
        n += 1
    counts['obstruction_polynomial_cases'] = n

    n = 0
    for q in range(1, 9):
        for coeff in [[1, -3, 0, 7], [0, 0, 2], [2, 1, -1, 1, 4]]:
            # Compare coefficients of d/dz f(z^q) and q z^(q-1) f'(z^q).
            left = {q*k-1: q*k*a for k, a in enumerate(coeff) if k and a}
            right = {q*(k-1)+q-1: q*k*a for k, a in enumerate(coeff) if k and a}
            assert left == right
            n += 1
    counts['ramification_chain_rule_cases'] = n

    n = 0
    for j in range(2, 101):
        k = Q(j, 1)
        lam = 2*k/(k*k-1)
        assert lam/k == 2/(k*k-1)
        assert lam*k*k - 2*k - lam == 0
        n += 1
    counts['dilation_stationarity_cases'] = n

    # Floating-point midpoint quadrature is illustrative, not validated numerics.
    size = 16384
    theta = [2*pi*(j+0.5)/size for j in range(size)]
    u = [log(2*abs(sin(t/2))) for t in theta]
    C0 = sum(max(x, 0) for x in u)/size
    I = sum(max(1+x, 0) for x in u)/size
    limit_ratio = (1+C0)/I
    rows = []
    for N in [3, 9, 21, 45, 93, 189, 381]:
        logs = []
        minimum = float('inf')
        for t in theta:
            v = abs((1-cmath.exp(1j*t))**N-1)
            minimum = min(minimum, v)
            logs.append(max(N+log(v), 0))
        Tf = sum(logs)/size
        Td = sum(max(N+log(N)+(N-1)*x, 0) for x in u)/size
        # Only a sampled diagnostic for a lower bound proved analytically.
        assert minimum >= 0.25 - 1e-10
        rows.append({'N': N, 'sampled_minimum_unscaled': round(minimum, 9),
                     'T_ratio': round(Tf/Td, 9)})
    diagnostic = {'label': 'illustrative floating-point midpoint quadrature only',
                  'points': size, 'c': 1,
                  'predicted_limit_ratio': round(limit_ratio, 9),
                  'positive_limit_gap': round(1+C0-I, 9), 'rows': rows}
    result = {'status': 'pass', 'exact_case_counts': counts,
              'total_exact_cases': sum(counts.values()),
              'diagnostic': diagnostic,
              'scope': 'Finite exact algebra controls and unvalidated quadrature. '
                       'They do not prove the infinite statements; see PROOF.md.'}
    target = Path(__file__).with_name('checks.json')
    if target.exists():
        saved = json.loads(target.read_text())
        assert saved == result, 'Recorded checks differ from this run.'
    else:
        target.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    manifest_path = Path(__file__).with_name('FROZEN_MANIFEST.json')
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        for name, expected in manifest['files'].items():
            data = manifest_path.with_name(name).read_bytes()
            assert len(data) == expected['bytes'], name
            assert hashlib.sha256(data).hexdigest() == expected['sha256'], name
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
