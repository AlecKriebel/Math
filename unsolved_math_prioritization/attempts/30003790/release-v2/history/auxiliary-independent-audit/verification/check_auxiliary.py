#!/usr/bin/env python3
"""Portable independent controls for the exact guarded-consistency candidate.
Standard library only. Run with optional rank618-30003790 directory to bind inputs.
Finite checks support, but do not replace, the mathematical proof in AUDIT.md.
"""
import hashlib
import itertools
import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
import sys

CANDIDATE_HASH = '072aba944c908baf44bb86d6c9a3d1c87444b5f779c53a14b4a9648d9595351c'
MANIFEST_HASH = 'a18df1c214a6ea7ed7aa14d8a038827f463a7c9ff4f069228e0eb68b247367d2'
RESULT_HASH = '0c63e1801d50434d217a8a66d16ea8bad27cac4867919f7532abc4819eb9dc16'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bind(root):
    candidate = root/'independent-audit/AUXILIARY_CANDIDATE.md'
    assert digest(candidate) == CANDIDATE_HASH
    p = root/'public'
    assert digest(p/'MANIFEST.json') == MANIFEST_HASH
    assert digest(p/'RESULT.md') == RESULT_HASH
    rows = json.loads((p/'MANIFEST.json').read_text())['files']
    for row in rows:
        f = p/row['path']
        assert len(f.read_bytes()) == row['bytes']
        assert digest(f) == row['sha256']
    return {'candidate_sha256':CANDIDATE_HASH, 'original_manifest_sha256':MANIFEST_HASH,
            'original_manifest_entries_verified':len(rows), 'inputs_unchanged':True}


def fixed_guard_exact():
    count = 0
    points = [Q(-2), Q(-1), Q(0), Q(0), Q(2)]
    unique = sorted(set(points))
    for values in itertools.product([Q(-1),Q(0),Q(1)], repeat=len(unique)):
        field = dict(zip(unique,values))
        for x, lam in itertools.product([Q(-1),Q(-1,4),Q(0),Q(3)],
                                        [Q(1),Q(1,3),Q(1,100),Q(1,1000000)]):
            radii = [abs(x-z) for z in points]
            distances = [abs(field[z]*(x-z))+lam*r for z,r in zip(points,radii)]
            order = sorted(range(len(points)),key=lambda i:(distances[i],i))
            for k in range(1,len(points)+1):
                radius = sorted(radii)[k-1]
                actual = max(radii[i] for i in order[:k])
                assert actual <= (1+lam)*radius/lam
                if radius == 0:
                    assert actual == 0
                count += 1
    # Rational Pythagorean 2D vectors avoid floating point in the norm checks.
    points2 = [(Q(0),Q(0)),(Q(3),Q(4)),(Q(0),Q(5)),(Q(-5),Q(12)),(Q(0),Q(5))]
    radii2 = [Q(0),Q(5),Q(5),Q(13),Q(5)]
    unique2 = sorted(set(points2))
    vectors = [(Q(0),Q(0)),(Q(1),Q(0)),(Q(0),Q(1)),(Q(3,5),Q(4,5)),(Q(-3,5),Q(4,5))]
    for values in itertools.product(vectors,repeat=len(unique2)):
        field = dict(zip(unique2,values))
        for lam in [Q(1),Q(1,7),Q(1,10000)]:
            distances = [abs(sum((a*b for a,b in zip(field[z],z)),Q(0)))+lam*r
                         for z,r in zip(points2,radii2)]
            order = sorted(range(len(points2)),key=lambda i:(distances[i],i))
            for k in range(1,len(points2)+1):
                radius = sorted(radii2)[k-1]
                actual = max(radii2[i] for i in order[:k])
                assert actual <= (1+lam)*radius/lam
                count += 1
    return {'exact_fraction_cases':count,'includes_atoms_ties_zero_fields_sign_changes':True}


def adaptive_guard_decimal():
    count = 0
    with localcontext() as context:
        context.prec = 70
        zero, one = Decimal(0), Decimal(1)
        points = [Decimal('-0.25'),zero,zero,Decimal('0.5'),Decimal(2)]
        unique = sorted(set(points))
        for values in itertools.product([Decimal(-1),zero,one],repeat=len(unique)):
            field = dict(zip(unique,values))
            for x in [Decimal('-0.25'),zero,Decimal('0.2'),Decimal(3)]:
                radii = [abs(x-z) for z in points]
                for k in range(1,len(points)+1):
                    r = sorted(radii)[k-1]
                    lam = min(one,(r+one/len(points)).sqrt())
                    assert 0 < lam <= 1
                    ds = [abs(field[z]*(x-z))+lam*rad for z,rad in zip(points,radii)]
                    order = sorted(range(len(points)),key=lambda i:(ds[i],i))
                    actual = max(radii[i] for i in order[:k])
                    tol = Decimal('1e-60')
                    assert actual <= (1+lam)*r/lam+tol
                    if r <= 1:
                        assert (1+lam)*r/lam <= 2*r.sqrt()+tol
                    if r == 0:
                        assert actual == 0
                    count += 1
        boundary_count = 0
        for r,n in itertools.product([zero,Decimal('1e-30'),Decimal('0.01'),
                                      Decimal('0.999999'),one,Decimal('1e12')],
                                     [1,2,17,1000000]):
            lam = min(one,(r+one/n).sqrt())
            assert lam > 0
            if r <= 1:
                assert (1+lam)*r/lam <= 2*r.sqrt()+Decimal('1e-60')
            boundary_count += 1
    return {'decimal_precision':70,'selected_radius_cases':count,
            'formula_boundary_cases':boundary_count,'tolerance':'1e-60'}


def conditional_noise_exact():
    # Freeze any covariate-only selected indices. Heteroskedastic centered signs.
    scales = [Q(1,4),Q(1,2),Q(1),Q(3,4),Q(1,3)]
    checks = []
    for selected in [(0,),(0,2),(1,3,4),tuple(range(5))]:
        k = len(selected)
        averaged = [sum((scales[i]*signs[i] for i in selected),Q(0))/k
                    for signs in itertools.product([-1,1],repeat=len(scales))]
        mean = sum(averaged,Q(0))/len(averaged)
        second = sum((v*v for v in averaged),Q(0))/len(averaged)
        assert mean == 0
        assert second == sum((scales[i]**2 for i in selected),Q(0))/k**2
        assert second <= Q(1,k)
        checks.append({'selected':list(selected),'variance':str(second),'bound':str(Q(1,k))})
    # Equal covariates: a forbidden response-based tie rule chooses largest signs.
    n,k = 12,3
    means = [Q(sum(sorted(signs,reverse=True)[:k]),k)
             for signs in itertools.product([-1,1],repeat=n)]
    bad_mean = sum(means,Q(0))/len(means)
    bad_mse = sum((v*v for v in means),Q(0))/len(means)
    assert bad_mean > Q(9,10) and bad_mse > Q(9,10)
    assert bad_mse > Q(1,k)
    return {'valid_conditional_variances':checks,'response_selection_negative_control':
            {'n':n,'k':k,'mean':str(bad_mean),'mse':str(bad_mse),'invalid_bound':str(Q(1,k))}}


def atomic_model_exact():
    # X Bernoulli(1/2), F(x)=x, independent unit-variance centered noise.
    # Both guards select as many exact matches as available; averaging noise adds 1/k.
    rows = []
    for n in [1,4,9,16,64,256,1024]:
        k = math.isqrt(n)
        # For an independent query, matching count has Binomial(n,1/2) law.
        # Conditional bias magnitude is (k-matches)_+/k.
        bias2 = sum((Q(math.comb(n,m),2**n)*Q(k-m,k)**2 for m in range(k)),Q(0))
        risk = bias2+Q(1,k)
        rows.append({'n':n,'k':k,'expected_bias_squared':float(bias2),
                     'expected_mse':float(risk),'zero_radius_probability':
                     1-float(sum((Q(math.comb(n,m),2**n) for m in range(k)),Q(0)))})
    assert rows[-1]['expected_mse'] < rows[0]['expected_mse']
    return rows


def failure_controls():
    # Without the guard, constant tangent e1 ignores x2 for uniform[-1,1]^2.
    rows = [{'k':k,'noiseless_expected_risk':str(Q(1,3)+Q(1,3*k)),
             'with_independent_unit_noise':str(Q(1,3)+Q(1,3*k)+Q(1,k))}
            for k in [1,10,100,1000]]
    # Generic localization allows arbitrarily bad finite n when local mass is tiny.
    n,k,p = 100,10,Q(1,1000000)
    no_local = (1-p)**n
    assert no_local > Q(999,1000)
    # Candidate Cauchy example in report: on z>=max(1,2B), squared error density
    # is >=1/(8*pi), so truncated-tail lower bound grows linearly.
    cauchy_bounds = [(L, (L-2)/(8*math.pi)) for L in [10,100,1000]]
    assert all(cauchy_bounds[i+1][1]>cauchy_bounds[i][1] for i in range(2))
    return {'unguarded_square_risk':rows,
            'rare_atom':{'n':n,'k':k,'atom_mass':str(p),'probability_no_matches':float(no_local)},
            'cauchy_unbounded_target_tail_lower_bounds_B1':cauchy_bounds,
            'fixed_k_point_mass_risk':{'k':3,'risk':str(Q(1,3))},
            'noncentered_noise_point_mass_risk':{'k':100,'risk':str(1+Q(1,100))},
            'shared_noise_violating_iid_risk':1}


if __name__ == '__main__':
    result = {'status':'PASS','scope':'Finite controls and exact algebra; not a theorem prover',
              'binding':bind(Path(sys.argv[1])) if len(sys.argv)>1 else 'Not requested',
              'fixed_guard':fixed_guard_exact(),'adaptive_guard':adaptive_guard_decimal(),
              'conditional_noise':conditional_noise_exact(),'atomic_design':atomic_model_exact(),
              'negative_controls':failure_controls()}
    print(json.dumps(result,indent=2,sort_keys=True))
