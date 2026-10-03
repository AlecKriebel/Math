#!/usr/bin/env python3
"""Independent exact arithmetic audit. Run from any working directory.

Only the Python standard library and the sibling public artifacts are needed.
This reconstructs g=f(phi) as a series before differentiation, rather than
starting from the rational expression for (g')**7 in the author's verifier.
It is an arithmetic audit, not a formal verification of the analytic proof.
"""
from fractions import Fraction as Q
from pathlib import Path
from hashlib import sha256
from math import comb
import json
import subprocess
import sys


EXPECTED_HASHES = {
    'PROOF.md': 'a6612c7c1302de4db4d9f1bc1da1784264665496ba83cdaece76531d6303bffe',
    'README.md': 'fb52117feb7d365dff2c3960b57d1c8d7506557f1a7c46d9ee2a28d02b13c38b',
    'RESEARCH_LOG.md': '7c77390c68f0c1f74785d6ceb364a9bb6b1d91377b52e786bc87cde61c7ed55d',
    'SOURCE_GATE.md': '6c525aae6822e0e6bc1cbf18538eccb985f1c740bdfe9225ea7224b7b439adec',
    'STATUS.json': '8588d0f1a82559fb04c77a6e3aef37b46e003346fbeb3d7555c1c507bf2bde66',
    'verification.json': '1a21fb94f9e69e1b8edf9e12893cb8f491d49a7b263c25eaa005a59e34b126ab',
    'verify.py': '3d198c04d275901444c74ea20098c5bffda0976b66665bd0802fc555ba710dd4',
}


def convolution(x, y, degree):
    return [sum((x[j] * y[n-j]
                 for j in range(max(0, n-len(y)+1), min(n, len(x)-1)+1)), Q(0))
            for n in range(degree+1)]


def run():
    checks = []

    def check(label, statement):
        if not statement:
            raise AssertionError(label)
        checks.append(label)

    artifacts = Path(__file__).resolve().parent.parent / 'artifacts'
    for name, expected in EXPECTED_HASHES.items():
        check('frozen_hash_' + name, sha256((artifacts/name).read_bytes()).hexdigest() == expected)

    # phi = a*z + (1-a*a)*z*z/(1+a*z), then g = phi + phi*phi/10.
    # Retain phi and g through z**11 to determine g' through z**10 exactly.
    a, r, order = Q(2, 3), Q(99, 200), 10
    phi = [Q(0), a] + [(1-a*a)*(-a)**(n-2) for n in range(2, order+2)]
    phi_squared = convolution(phi, phi, order+1)
    g = [u + v/10 for u, v in zip(phi, phi_squared)]
    derivative = [(n+1)*g[n+1] for n in range(order+1)]
    seventh_power = [Q(1)]
    for _ in range(7):
        seventh_power = convolution(seventh_power, derivative, order)

    published = json.loads((artifacts/'verification.json').read_text())
    expected_coefficients = list(map(Q, published['certificate']['coefficients']))
    for n, (actual, expected) in enumerate(zip(seventh_power, expected_coefficients)):
        check('direct_composition_coefficient_%02d' % n, actual == expected)
    check('eleven_coefficient_count', len(seventh_power) == len(expected_coefficients) == 11)

    left = sum((v*v*r**(2*n) for n, v in enumerate(seventh_power)), Q(0))
    # f'=1+z/5; compute its seventh power by direct multiplication as well.
    rhs_coefficients = [Q(1)]
    for _ in range(7):
        rhs_coefficients = convolution(rhs_coefficients, [Q(1), Q(1, 5)], len(rhs_coefficients))
    right = sum((v*v*r**(2*n) for n, v in enumerate(rhs_coefficients)), Q(0))
    check('right_binomial_formula', right == sum((Q(comb(7,n)**2,5**(2*n))*r**(2*n) for n in range(8)), Q(0)))
    gap = left-right
    check('exact_gap', gap == Q(published['certificate']['lower_bound_minus_right']))
    check('strict_margin', gap > Q(1,200))
    check('counterexample_below_half', 0 < r < Q(1,2))
    check('admissible_parameter', 0 < a < 1)

    # Exact rational examples test the stated optimizer parametrization on
    # both sides of a=0. The general inequalities are reviewed analytically.
    pointwise = []
    for radius in map(Q, ['5/12', '9/20', '1/2', '3/4', '9/10']):
        k = radius/(1-radius*radius)
        t = (1-radius*radius)/(2*radius)
        parameter = (t-radius)/(1-t*radius)
        value = (parameter+2*radius+parameter*radius*radius)/(1+parameter*radius)**2
        check('optimizer_admissible_' + str(radius), k > Q(1,2) and 0 < t < 1 and -1 < parameter < 1)
        check('optimizer_attains_t_' + str(radius), (parameter+radius)/(1+parameter*radius) == t)
        check('optimizer_derivative_' + str(radius), value == k+1/(4*k) and value > 1)
        pointwise.append({'r':str(radius), 'a':str(parameter), 'derivative':str(value)})

    # Fourier moments of the independently expanded phi'/2z at radius 1/2.
    # phi=z**2+a*(z-z**3)+a**2*(z**4-z**2)+O(a**3).
    v = {-1:Q(1), 1:Q(-3,4)}
    w = {0:Q(-1), 2:Q(1,2)}
    real_v = {n:(v.get(n,Q(0))+v.get(-n,Q(0)))/2 for n in (-1,1)}
    mean_abs_v_squared = sum((c*c for c in v.values()),Q(0))
    mean_real_v_squared = sum((c*real_v[-n] for n,c in real_v.items()),Q(0))
    check('perturbation_linear_in_p', w[0]+mean_abs_v_squared/2-mean_real_v_squared == Q(-1,4))
    check('perturbation_quadratic_in_p', mean_real_v_squared/2 == Q(1,64))

    first = subprocess.check_output([sys.executable, str(artifacts/'verify.py')])
    second = subprocess.check_output([sys.executable, str(artifacts/'verify.py')])
    check('author_replay_byte_identical', first == second == (artifacts/'verification.json').read_bytes())
    check('author_replay_36_checks', json.loads(first)['exact_check_count'] == 36)

    return {
        'problem_id':2305039,
        'result':'PASS',
        'exact_check_count':len(checks),
        'checks':checks,
        'independent_method':'Expand phi, compose g=phi+phi^2/10, differentiate, then take the seventh power.',
        'coefficients':list(map(str,seventh_power)),
        'left_partial_mean_power':str(left),
        'right_mean_power':str(right),
        'lower_bound_minus_right':str(gap),
        'pointwise_optimizer_checks':pointwise,
        'author_artifacts_unchanged':True,
        'limitations':['Arithmetic checks do not prove analytic statements.',
                       'The finite-p>2 problem remains unresolved in this package.',
                       'No exhaustive literature or historical-priority finding is made.']
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
