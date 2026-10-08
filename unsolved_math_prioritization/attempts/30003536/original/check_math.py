#!/usr/bin/env python3
"""Finite exact algebraic controls, not a proof of the analytic report."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

class CheckError(Exception):
    pass

def require(condition, message):
    if not condition:
        raise CheckError(message)

def loads_strict(data):
    def pairs(items):
        out = {}
        for key, val in items:
            if key in out:
                raise CheckError('duplicate JSON key: ' + key)
            out[key] = val
        return out
    def bad_constant(value):
        raise CheckError('nonfinite JSON constant: ' + value)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=bad_constant)

EXPECTED = {'problem_id': 30003536, 'code': 'OWR-15577-004', 'status': 'unsolved', 'author_turns': 5, 'target': {'dimension': 'integer d >= 3', 'exponent': '1 < s < d-1', 'density': 'nonnegative C_c^infinity', 'kernel': 'z/|z|^(s+1)', 'norm': 'full Euclidean vector norm', 'support': 'closed support', 'constant': 'C(d,s) independent of f'}, 'original_inequality_proved': False, 'original_inequality_disproved': False, 'independent_audit_performed': False, 'mass_lower_coefficient': '1/2', 'latitude': {'d': 8, 's': 2, 'hessian_parallel': '-8/3', 'hessian_transverse': '-4/147', 'laplacian': '-20/7', 'claim': 'strict local maximum away from smooth positive source support', 'global_counterexample': False}, 'collinear_s2_t2': '-1/2', 'flat_model': {'d': 4, 's': 2, 'normal_magnitude': '2*pi', 'admissible_target_density': False, 'smooth_support_boundary_layer_survives': True}, 'scope_of_computation': 'finite algebraic controls only; analytic arguments require mathematical review'}

def run(claims_path):
    raw = claims_path.read_bytes()
    data = loads_strict(raw)
    # Canonical JSON comparison distinguishes booleans from integers and rejects
    # extra keys, omitted qualifications, modified parameters and wrong signs.
    require(json.dumps(data, sort_keys=True) == json.dumps(EXPECTED, sort_keys=True),
            'claim schema or mathematical scope differs from the checked packet')
    counts = {'scope': 1, 'latitude': 0, 'symmetrization': 0,
              'moment': 0, 'geometric_sums': 0, 'boundary_layer': 0}
    def check(condition, category, label):
        require(condition, label)
        counts[category] += 1

    # Derive latitude Hessian from first three moments rather than comparing
    # only the printed constants. q is E[y_1^2]; q=1/(s+1).
    for n in range(3, 21):
        for twice_s in range(3, 2*n):
            s = Q(twice_s, 2)
            q = 1/(s+1)
            transverse_second = (1-q)/n
            j11 = 1-(s+1)*q
            lam = 1-(s+1)*transverse_second
            hp = 2*j11*j11-2*q*(s+1)*(3-(s+3)*q)
            ht = 2*lam*lam-2*q*(s+1)*(1-(s+3)*transverse_second)
            check(j11 == 0, 'latitude', 'latitude gradient factor')
            check(hp == -4*s/(s+1), 'latitude', 'parallel Hessian identity')
            check(ht == 2*s/n*(s/n-(s-1)/(s+1)), 'latitude', 'transverse Hessian identity')
            check(hp+n*ht == -2*s*(n-s)/n < 0, 'latitude', 'trace identity')
            check((ht < 0) == (n > s*(s+1)/(s-1)), 'latitude', 'strict-concavity threshold')
            if n == 7 and s == 2:
                check(hp == Q(data['latitude']['hessian_parallel']), 'latitude', 'recorded parallel value')
                check(ht == Q(data['latitude']['hessian_transverse']), 'latitude', 'recorded transverse value')
                check(hp+n*ht == Q(data['latitude']['laplacian']), 'latitude', 'recorded trace')

    for s in range(2, 13):
        for t in range(2, 41):
            direct = Q(1, t**s)-Q(1, (t-1)**s)+Q(1, (t*(t-1))**s)
            combined = Q((t-1)**s-t**s+1, (t*(t-1))**s)
            check(direct == combined, 'symmetrization', 'three-point identity')
            check(direct < 0, 'symmetrization', 'collinear sign')
            if s == 2 and t == 2:
                check(direct == Q(data['collinear_s2_t2']), 'symmetrization', 'recorded three-point value')
    # For equilateral side lengths 2,4,...,20, the dot product at each vertex
    # is one half of the product of the kernel magnitudes.
    for s in range(2, 13):
        for ell in range(2, 21, 2):
            check(3*Q(1,2)*Q(1,ell**s)**2 == Q(3,2*ell**(2*s)) > 0,
                  'symmetrization', 'equilateral sign and scaling')

    # Discrete diagonal-omitting identity checks antisymmetry only. It is not
    # the smooth-measure diameter lower bound; atoms are not target densities.
    for s in range(2, 8):
        for n in range(2, 13):
            xs = [Q(i*i+i, 2) for i in range(n)]
            ws = [Q(i+1, n+1) for i in range(n)]
            fs = []
            for i, x in enumerate(xs):
                fs.append(sum((ws[j]*(1 if x>xs[j] else -1)/abs(x-xs[j])**s
                               for j in range(n) if j != i), Q(0)))
            rhs = sum((ws[i]*ws[j]*abs(xs[i]-xs[j])**(1-s)
                       for i in range(n) for j in range(i)), Q(0))
            for a in (Q(-2), Q(0), Q(3), Q(11,2)):
                lhs = sum((ws[i]*(xs[i]-a)*fs[i] for i in range(n)), Q(0))
                check(lhs == rhs, 'moment', 'antisymmetric pair-moment identity')

    for s in range(2, 7):
        for n in range(1, 21):
            radii = [Q(1,2**j) for j in range(1,n+1)]
            for exponent in range(-25,4):
                r = Q(2)**exponent
                inner = sum(((a/r)**s for a in radii if a < r), Q(0))
                outer = sum((r/a for a in radii if a >= r), Q(0))
                check(outer <= 2, 'geometric_sums', 'outer dyadic bound')
                check(inner <= 1/(1-Q(1,2**s)), 'geometric_sums', 'inner dyadic bound')
                direct = sum((min(r/a,(a/r)**s) for a in radii), Q(0))
                check(direct == inner+outer, 'geometric_sums', 'dyadic split identity')

    for i in range(-10,11):
        for j in range(-10,11):
            if i*i+j*j <= 100:
                x,y = Q(i,20),Q(j,20)
                numerator = 1-x
                distance_squared = (1-x)**2+y*y
                check(numerator >= Q(1,2), 'boundary_layer', 'positive numerator on half disk')
                check(9*numerator*numerator >= distance_squared,
                      'boundary_layer', 'squared ratio lower bound 1/3')
    return {'result': 'PASS', 'checks': counts, 'total_checks': sum(counts.values()),
            'claims_sha256': hashlib.sha256(raw).hexdigest(),
            'scope': 'Finite algebraic controls only; no analytic or literature-status certification.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--claims', type=Path, default=Path(__file__).resolve().with_name('CLAIMS.json'))
    args = parser.parse_args()
    try:
        output = run(args.claims)
    except (CheckError, ValueError, TypeError, KeyError, OSError, ZeroDivisionError) as exc:
        print(json.dumps({'result':'FAIL', 'error':str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(output, sort_keys=True, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
