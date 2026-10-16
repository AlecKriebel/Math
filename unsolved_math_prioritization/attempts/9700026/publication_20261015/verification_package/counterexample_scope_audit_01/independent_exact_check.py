#!/usr/bin/env python3
"""Independent rational scope/witness checks; analytic reasoning is in REPORT.md.

No imports or execution from author verifier. All numeric comparisons use Fraction.
"""
from fractions import Fraction as F
from pathlib import Path
import copy
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'source' / 'author'
EXPECTED_PROOF_SHA256 = '8b0922482116df0b6510b4d5a6c089c3478765d4fecf2c151fd04c50a6814767'


def demand(value, why):
    if not value:
        raise ValueError(why)


def fmt(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: fmt(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [fmt(v) for v in value]
    return value


def check(c):
    a, b = F(c['alpha']), F(c['beta'])
    demand(a > 1 and b > 2*a, 'outside counterexample parameter region')
    points = [tuple(F(v) for v in row) for row in c['cities']]
    m = len(points)
    demand(m >= 2, 'one city cannot refute collapse')
    demand(all(len(row) == 2 for row in points), 'nonplanar coordinates')
    weights = tuple(F(v) for v in c['initial_weights'])
    demand(len(weights) == m, 'wrong vector dimension')
    demand(sum(weights) == 1, 'not normalized')
    demand(min(weights) > 0, 'nonpositive initial mass')
    h = F(c['square_halfwidth'])
    demand(h > 0, 'nonpositive geometric scale')
    demand(all(0 < v < 1 for row in points for v in row), 'boundary/outside site')
    boundary_margins = [min(*row, *(1-v for v in row)) - h for row in points]
    demand(min(boundary_margins) > 0, 'no strict interior square slack')
    squared_distances = {}
    for i in range(m):
        for j in range(i):
            d = sum((points[i][k]-points[j][k])**2 for k in (0, 1))
            demand(d > 8*h*h, 'no strict separation slack')
            squared_distances[f'{j+1},{i+1}'] = d
    p = 2*a/b
    k = 4*h*h
    demand(p == F(1, 2), 'specialized rational threshold requires p=1/2')
    lower = k*k
    upper = 1-(m-1)*lower
    demand(F(c['claimed_p']) == p, 'incorrect exponent')
    demand(F(c['claimed_K']) == k, 'incorrect square area coefficient')
    demand(F(c['claimed_lower_bound']) == lower, 'incorrect lower bound')
    demand(F(c['claimed_upper_bound']) == upper, 'incorrect upper bound')
    demand(all(w >= lower for w in weights), 'initial mass too small for stated bound')
    demand(0 < lower < upper < 1, 'does not exclude collapse')
    out = {'city_count': m, 'p': p, 'K': k, 'lower': lower, 'upper': upper,
           'initial_sum': sum(weights), 'boundary_square_margins': boundary_margins,
           'squared_distances': squared_distances,
           'minimum_separation_squared_slack': min(squared_distances.values())-8*h*h}
    if m == 3:
        v = tuple(points[1][j]-points[0][j] for j in (0, 1))
        w = tuple(points[2][j]-points[0][j] for j in (0, 1))
        determinant = v[0]*w[1]-v[1]*w[0]
        demand(determinant != 0, 'collinear triangle')
        demand(len(set(squared_distances.values())) == 3, 'triangle not scalene')
        out['triangle_determinant'] = determinant
    return out


def perturbation_box(c):
    points = [tuple(F(v) for v in row) for row in c['cities']]
    eps = F(1, 10000)
    h = F(c['square_halfwidth'])
    demand(all(h+eps < v < 1-h-eps for row in points for v in row),
           'position box loses square containment')
    intervals = {}
    for i in range(3):
        for j in range(i):
            d = tuple(abs(points[i][r]-points[j][r]) for r in (0, 1))
            lo = sum(max(v-2*eps, F(0))**2 for v in d)
            hi = sum((v+2*eps)**2 for v in d)
            demand(lo > 8*h*h, 'position box loses cell-square condition')
            intervals[f'{j+1},{i+1}'] = (lo, hi)
    ordered = sorted(intervals.values())
    demand(all(ordered[i][1] < ordered[i+1][0] for i in (0, 1)),
           'not every perturbed triangle certified scalene')
    v = tuple(points[1][j]-points[0][j] for j in (0, 1))
    w = tuple(points[2][j]-points[0][j] for j in (0, 1))
    det = v[0]*w[1]-v[1]*w[0]
    det_error = 2*eps*sum(abs(t) for t in v+w)+8*eps*eps
    demand(det-det_error > 0, 'position box may become collinear')
    weights = tuple(F(x) for x in c['initial_weights'])
    demand(min(weights)-eps > F(1,8192), 'state box loses common lower bound')
    # Relative-open state box is intersected with sum z_i=1.
    amin, amax = F(199,100), F(201,100)
    bmin, bmax = F(799,100), F(801,100)
    demand(amin > 1 and bmin > 2*amax, 'parameter box leaves counterexample regime')
    pmax = 2*amax/bmin
    p0 = F(51,100)
    demand(pmax < p0 < 1, 'bad dominating exponent')
    # At L=2^-13, K=2^-6, require L^(1-p0) <= K.
    # Since 2^-x decreases, this is exactly 13(1-p0)>=6.
    demand(13*(1-p0) > 6, 'uniform rational lower bound invalid')
    return {'position_supnorm_radius': eps, 'initial_supnorm_radius': eps,
            'initial_box_normalization': 'intersection with sum z_i=1',
            'distance_squared_intervals': intervals,
            'determinant_lower': det-det_error,
            'alpha_interval': (amin,amax), 'beta_interval': (bmin,bmax),
            'p_upper_bound': pmax, 'comparison_exponent': p0,
            'all_time_lower_bound': F(1,8192), 'all_time_upper_bound': F(4095,4096),
            'exact_exponent_slack': 13*(1-p0)-6}


def negative_controls(c):
    cases = []
    for label, key, value in [('alpha critical', 'alpha', '1'),
                              ('beta critical', 'beta', '4'),
                              ('beta smaller', 'beta', '2'),
                              ('bad normalization', 'initial_weights', ['1/5','1/3','1/2']),
                              ('zero mass', 'initial_weights', ['0','1/3','2/3']),
                              ('claimed lower too large','claimed_lower_bound','1/1024'),
                              ('claimed upper one','claimed_upper_bound','1')]:
        d = copy.deepcopy(c); d[key] = value; cases.append((label,d))
    d = copy.deepcopy(c);d['cities'][0][0]='0';cases.append(('boundary site',d))
    d = copy.deepcopy(c);d['cities'][1]=d['cities'][0];cases.append(('colliding sites',d))
    d = copy.deepcopy(c);d['cities']=d['cities'][:1];d['initial_weights']=['1'];cases.append(('m=1',d))
    d = copy.deepcopy(c);d['cities']=[['1/4','1/4'],['1/2','1/2'],['3/4','3/4']];cases.append(('collinear witness',d))
    rejected=[]
    for label,d in cases:
        try:
            check(d)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('failed negative control: '+label)
    # Homogeneous exponent rescaling preserves q, not stochastic arrival probabilities.
    d = copy.deepcopy(c);d['alpha']='3';d['beta']='12';check(d)
    demand(F(2,8) == F(1,2)/2 == F(3,12), 'ratio invariance arithmetic failed')
    # Failure of this persistence mechanism at/above p=1 is not a collapse proof.
    k=F(1,64);s=F(1,4096)
    demand(k*s-s < 0 and k*s*s-s < 0, 'critical/supercritical controls failed')
    return {'rejected':rejected, 'accepted_scaled_pair':['3','12'],
            'p_at_least_one_control':'scalar lower field can be negative near zero; no persistence conclusion'}


def main():
    proof = SOURCE/'PROOF.md'
    demand(proof.stat().st_size == 5736, 'frozen proof byte count changed')
    demand(hashlib.sha256(proof.read_bytes()).hexdigest() == EXPECTED_PROOF_SHA256,
           'frozen proof hash changed')
    c = json.loads((SOURCE/'certificate.json').read_text())
    results = {'status':'PASS','method':'independent exact rational arithmetic; no ODE simulation',
               'proof_sha256':EXPECTED_PROOF_SHA256, 'certificate':check(c),
               'robust_open_box':perturbation_box(c), 'controls':negative_controls(c),
               'limits':'All-time theorem relies on the analytic geometry and scalar comparison in REPORT.md; these computations do not replace that proof.'}
    print(json.dumps(fmt(results), indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
