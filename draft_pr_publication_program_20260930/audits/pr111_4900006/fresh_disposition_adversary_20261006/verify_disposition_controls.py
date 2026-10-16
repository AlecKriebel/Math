#!/usr/bin/env python3
"""Exact spectrum/scope controls for the reviewed disposition, not priority proof."""
from fractions import Fraction as Q
import json
import os

checks = []
def require(label, condition):
    if not condition:
        raise RuntimeError(label)
    checks.append(label)

def ky(spectrum):
    values = sorted(map(Q, spectrum), reverse=True)
    partial = Q(0)
    j = 0
    previous = Q(0)
    for k, rate in enumerate(values, 1):
        partial += rate
        if partial >= 0:
            j, previous = k, partial
    if j == len(values):
        return Q(j)
    return Q(j) + previous / -values[j]

intrinsic = [0, 0, -1]
ambient = [0, 0, 0, 0, -1]
require('Intrinsic product dimension is2', ky(intrinsic) == 2)
require('Ambient extension dimension is4', ky(ambient) == 4)
require('Intrinsic and ambient conventions differ', ky(intrinsic) != ky(ambient))
require('Both dissipative spectra have sum minus1', sum(intrinsic) == sum(ambient) == -1)
for rates, index in [(intrinsic, 2), (ambient, 4)]:
    require(f'Global index{index} has zero partial sum', sum(rates[:index]) == 0)
    require(f'Global index{index} next partial sum negative', sum(rates[:index+1]) < 0)

types = {'O': (Q(-4), Q(-4)), 'U': (Q(3), Q(0)), 'S': (Q(0), -Q(24,17))}
expected_ky = {'OO': Q(0), 'OU': Q(11,4), 'OS': Q(1), 'UU': Q(203,50), 'US': Q(6827,1700), 'SS': Q(2)}
expected_fixed = {'OO': Q(96,25), 'OU': Q(79,20), 'OS': Q(332,85), 'UU': Q(203,50), 'US': Q(6827,1700), 'SS': Q(1688,425)}
profiles = {}
for kind in expected_ky:
    spectrum = sorted(types[kind[0]] + types[kind[1]] + (Q(-100),), reverse=True)
    local = ky(spectrum)
    fixed = Q(4) + sum(spectrum[:4]) / Q(100)
    require(f'{kind} pointwise value exact', local == expected_ky[kind])
    require(f'{kind} fixed-index value exact', fixed == expected_fixed[kind])
    if kind != 'UU':
        require(f'{kind} strictly below torus in both conventions', local < Q(203,50) and fixed < Q(203,50))
    profiles[kind] = {'spectrum': list(map(str,spectrum)), 'pointwise': str(local), 'fixed_global_index': str(fixed)}

require('Finite-time transient exact excess', Q(63459,15625) - Q(203,50) == Q(43,31250))
require('Finite-time equality not supplied by transient control', Q(63459,15625) > Q(203,50))

# A radial singleton exceeds any compact set's maximal first radius by1.
# Rational controls illustrate the all-size metric proof in REPORT.md.
for bound in [Q(0), Q(1), Q(1000), Q(1,1000)]:
    witness = bound + 1
    require(f'Invariant-radius witness gap at bound{bound}', witness - bound == 1)

result = {
    'schema': 'pr111-fresh-disposition-exact-spectrum-controls/v1',
    'actual_pid': os.getpid(),
    'status': 'PASS',
    'explicit_guards': len(checks),
    'checks': checks,
    'profiles': profiles,
    'mathematical_proofs_in_report': ['global attraction and minimality', 'irrationality excludes periods', 'ambient extension has no entire-space compact global attractor'],
    'numerical_controls_are_not_all_size_proofs': True,
    'novelty_or_historical_priority_certified': False,
    'new_central_proof_search': False,
}
print(json.dumps(result, indent=2, sort_keys=True))
