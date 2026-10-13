#!/usr/bin/env python3
"""Independent exact controls. Standard library only; no assert statements.

The mathematics is proved in DERIVATION.md. These finite checks exercise
normalization, real supports, tensor contractions and source arithmetic.
Run `python3 controls.py --suite` to check baseline and false variants in
both ordinary and optimized interpreters.
"""
from fractions import Fraction as F
from itertools import product, combinations
from functools import reduce
import operator
import argparse
import json
import subprocess
import sys


class ValidationFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise ValidationFailure(message)


def prod(xs):
    return reduce(operator.mul, xs, F(1))


def det(g):
    return g[0][0] * g[1][1] - g[0][1] * g[1][0]


def grams(coeff, n, scale_squared=F(1)):
    """Actual real tensor with entries sqrt(scale_squared)*rational coeff."""
    answer = []
    for i in range(n):
        g = [[F(0), F(0)], [F(0), F(0)]]
        for tail in product((0, 1), repeat=n-1):
            k0 = tail[:i] + (0,) + tail[i:]
            k1 = tail[:i] + (1,) + tail[i:]
            a, b = coeff.get(k0, F(0)), coeff.get(k1, F(0))
            g[0][0] += a*a*scale_squared
            g[0][1] += a*b*scale_squared
            g[1][0] += a*b*scale_squared
            g[1][1] += b*b*scale_squared
        answer.append(g)
    return answer


def squared_norm(coeff, scale_squared=F(1)):
    return sum((a*a*scale_squared for a in coeff.values()), F(0))


def weights(t):
    a, b, c = t
    return [1-(a+b+c)/2, (b+c-a)/2, (a+c-b)/2, (a+b-c)/2]


def determinant_polygon(d):
    return all(x <= sum(d)-x for x in d)


def eigenvalue_polygon(t):
    return all(x <= sum(t)-x for x in t)


def source_q(d, roots, variant):
    q1 = prod(sum(d)-2*x for x in d)
    signs = list(product((-1, 1), repeat=len(d)))
    if variant == 'omit_global_sign_partners':
        signs = [es for es in signs if es[0] == 1]
    q2 = prod(sum(e*r for e, r in zip(es, roots)) for es in signs) / 2
    if variant == 'omit_q2_half':
        q2 *= 2
    return q1, q2


VARIANTS = [
    'reversed_ratio_derivative',
    'wrong_determinant_normalization',
    'wrong_parity_weight_labels',
    'wrong_parity_support',
    'unnormalized_peeling',
    'annihilate_retained_grams',
    'outer_hull_as_exact_locus',
    'omit_q2_half',
    'omit_global_sign_partners',
    'printed_secondary_accepts_ghz',
]


def run(variant='baseline'):
    checks = []
    # Exact trace-one derivative for di=6/25, dj=5/36:
    # Ri=1/5, Rj=2/3, hence derivative of log ratio is 7/2.
    derivative = F(5)-F(3, 2)
    if variant == 'reversed_ratio_derivative':
        derivative = -derivative
    require(derivative == F(7, 2) and derivative > 0,
            'ratio derivative must be +7/2 on a strictly dominant determinant')
    checks.append('exact ratio derivative sign')

    support = [(0,0,0), (0,1,1), (1,0,1), (1,1,0)]
    grid_count = 0
    for t in product([F(i, 8) for i in range(5)], repeat=3):
        if not eigenvalue_polygon(t):
            continue
        w = weights(t)
        require(all(x >= 0 for x in w) and sum(w) == 1 and w[0] >= F(1,4),
                'triangle grid weights must be nonnegative, normalized and w0>=1/4')
        row_one = [sum(w[k] for k, bits in enumerate(support) if bits[i])
                   for i in range(3)]
        require(row_one == list(t), 'three parity-support row norms must match target t')
        for i in range(3):
            for a, b in combinations(support, 2):
                require(not (a[:i]+a[i+1:] == b[:i]+b[i+1:] and a[i] != b[i]),
                        'even-parity support must forbid off-diagonal Gram terms')
        grid_count += 1
    # Deliberately asymmetric positive-weight rational real tensor.
    t = [F(1,5), F(1,5), F(8,25)]
    w = weights(t)
    # Entries 4/5,2/5,2/5,1/5 have exactly these squares.
    amplitudes = [F(4,5), F(2,5), F(2,5), F(1,5)]
    if variant == 'wrong_parity_weight_labels':
        amplitudes[1], amplitudes[3] = amplitudes[3], amplitudes[1]
    selected_support = list(support)
    if variant == 'wrong_parity_support':
        selected_support[1] = (0,0,1)
    tensor = dict(zip(selected_support, amplitudes))
    expected_d = [x*(1-x) for x in t]
    gg = grams(tensor,3)
    require(squared_norm(tensor)==1, 'rational parity tensor must have norm one')
    require([det(g) for g in gg] == expected_d,
            'actual asymmetric real tensor must have the target determinants')
    require(all(g[0][1] == 0 for g in gg), 'actual parity Gram matrices must be diagonal')
    require([g[1][1] for g in gg] == t, 'parity weight labels must give intended eigenvalues')
    checks.append({'closed parity construction grid': grid_count,
                   'actual rational tensor entries': [str(x) for x in amplitudes]})

    scaled = {k: a/2 for k,a in tensor.items()}
    s = squared_norm(scaled)
    small_d = [det(g) for g in grams(scaled,3)]
    norm_d = [x/(s*s) for x in small_d]
    if variant == 'wrong_determinant_normalization':
        norm_d = [x/s for x in small_d]
    require(s==F(1,4) and norm_d==expected_d,
            'normalized determinants must divide by squared trace s^2')
    checks.append('subunit tensor determinant normalization')

    # Exact zero, rank-one, equal eigenvalue, saturated triangle controls.
    for target in [(F(0),F(0),F(0)), (F(0),F(1,2),F(1,2)),
                   (F(1,2),F(1,2),F(1,2)), (F(1,4),F(1,8),F(1,8))]:
        require(all(x>=0 for x in weights(target)), 'closed construction boundary weights')
    zero = {(0,0,0):F(0)}
    require(squared_norm(zero)==0 and all(det(g)==0 for g in grams(zero,3)),
            'zero tensor must be treated without normalization division')
    # trace endpoint s=4/5 and two identical maximal determinants 4/25.
    s, a = F(4,5), F(2,5)
    require(a*(s-a)==F(4,25) and s*s-4*F(4,25)==0,
            'endpoint determinant must have vanishing discriminant')
    checks.append('zero, degenerate, equal and lower-trace endpoint cases')

    unit = [F(3,5),F(4,5)]
    if variant == 'unnormalized_peeling':
        unit = [F(3,5),F(3,5)]
    extended = dict(tensor)
    tested_n = []
    for n in range(4,9):
        extended = {k+(bit,): a*u for k,a in extended.items()
                    for bit,u in enumerate(unit)}
        all_grams = grams(extended,n)
        retained = all_grams[:3]
        if variant == 'annihilate_retained_grams':
            retained = [[[F(0),F(0)],[F(0),F(0)]] for _ in range(3)]
        require(squared_norm(extended)==1 and retained==gg,
                'peeling unit factors must preserve norm and every retained Gram matrix')
        require(all(det(g)==0 for g in all_grams[3:]), 'peeled factors must have determinant zero')
        tested_n.append(n)
    checks.append({'exact noncoordinate unit-factor peeling':tested_n})

    outer_t = [F(2,5), F(1,6), F(1,6)]
    outer_d = [x*(1-x) for x in outer_t]
    require(determinant_polygon(outer_d), 'negative witness must be inside determinant hull')
    accepted = eigenvalue_polygon(outer_t)
    if variant == 'outer_hull_as_exact_locus':
        accepted = determinant_polygon(outer_d)
    require(not accepted and min(weights(outer_t))<0,
            'determinant polygon inequalities alone are not exact G3 membership')
    checks.append('strict-H3 spectral counterexample rejects outer-hull substitution')

    vertex_count = 0
    for n in range(2,8):
        for mask in product((0,1),repeat=n):
            if sum(mask)<2:
                continue
            v = {tuple([0]*n):F(1), mask:F(1)}
            actual = [det(g) for g in grams(v,n,F(1,2))]
            require(actual==[F(bit,4) for bit in mask], 'subset GHZ must realize convex-hull vertex')
            vertex_count += 1
    singleton = {(0,0,0):F(1),(1,0,0):F(1)}
    require([det(g) for g in grams(singleton,3,F(1,2))]==[F(0)]*3,
            'singleton support is a product tensor, not a forbidden convex-hull vertex')
    checks.append({'subset-GHZ convex-hull vertices':vertex_count})

    roots = [F(49,100),F(36,100),F(36,100),F(1,100)]
    d = [x*x for x in roots]
    q1,q2 = source_q(d,roots,variant)
    require(q1==F(168760917,305175781250), 'source n4 Q1 exact value')
    require(q2==F(23632249608,2384185791015625), 'source n4 Q2 must contain all 16 factors and 1/2')
    require(q1-q2==F(2589624828909,4768371582031250)>0, 'source n4 inequality strictly holds')
    require(all(0<x<F(1,4) for x in d) and all(sum(d)-2*x>0 for x in d),
            'source n4 witness must be in open cube and strict determinant hull')
    require(d[0]>F(2,5)*(1-F(2,5)), 'n4 lambda1>2/5 certificate')
    require(d[1]<F(1,6)*(1-F(1,6)) and d[2]<F(1,6)*(1-F(1,6)),
            'n4 lambda2,lambda3<1/6 certificates')
    require(d[3]<F(1,100)*(1-F(1,100)) and F(103,300)<F(2,5),
            'n4 lambda4 and violated eigenvalue polygon certificates')
    checks.append({'source n4 Q1':str(q1),'Q2':str(q2),'difference':str(q1-q2),
                   'H4 slacks':[str(sum(d)-2*x) for x in d]})

    ghz = {(0,0,0):F(1),(1,1,1):F(1)}
    ghz_d = [det(g) for g in grams(ghz,3,F(1,2))]
    require(ghz_d==[F(1,4)]*3 and squared_norm(ghz,F(1,2))==1, 'actual unit real GHZ determinants')
    q1,q2 = source_q(ghz_d,[F(1,2)]*3,'baseline')
    pair = (ghz_d[0]-ghz_d[1])**2+(ghz_d[0]+ghz_d[1])/2
    printed_region = q1>=q2 or (q1<=q2 and pair<=F(3,16))
    if variant == 'printed_secondary_accepts_ghz':
        printed_region = True
    require((q1,q2,pair)==(F(1,64),F(9,512),F(1,4)) and not printed_region,
            'printed Theorem 1.4 union excludes the actual GHZ tuple')
    # A nearby open-cube feasible tuple shows this is not only an endpoint issue.
    near_t = [F(9,20)]*3
    near_d = [x*(1-x) for x in near_t]
    near_q1 = prod(near_d)
    near_q2 = F(9,2)*near_d[0]**4
    require(eigenvalue_polygon(near_t) and near_q1<near_q2 and near_d[0]>F(3,16),
            'printed union also excludes a feasible open-cube parity tuple')
    checks.append({'GHZ printed-source caution':{'Q1':str(q1),'Q2':str(q2),'pair':str(pair)},
                   'near-GHZ feasible d':[str(x) for x in near_d]})
    return {'status':'PASS','variant':variant,'checks':checks,
            'finite_controls_are_not_the_universal_proof':True}


def suite():
    matrix=[]
    for optimized in (False,True):
        prefix=[sys.executable]+(['-O'] if optimized else [])+[__file__]
        baseline=subprocess.run(prefix+['--variant','baseline'],capture_output=True,text=True)
        require(baseline.returncode==0,'baseline failed in '+('optimized' if optimized else 'ordinary')+' mode')
        row={'mode':'optimized' if optimized else 'ordinary','baseline':json.loads(baseline.stdout),'false_variants':[]}
        for variant in VARIANTS:
            failed=subprocess.run(prefix+['--variant',variant],capture_output=True,text=True)
            require(failed.returncode==2,variant+' did not fail explicitly in '+row['mode']+' mode')
            event=json.loads(failed.stdout)
            require(event['status']=='REJECTED' and event['variant']==variant,
                    'variant failed without the expected checkable rejection')
            row['false_variants'].append(event)
        matrix.append(row)
    return {'status':'PASS','baseline_runs':2,'false_variant_rejections':2*len(VARIANTS),'matrix':matrix}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--variant',default='baseline',choices=['baseline']+VARIANTS)
    parser.add_argument('--suite',action='store_true')
    args=parser.parse_args()
    try:
        result=suite() if args.suite else run(args.variant)
        print(json.dumps(result,indent=2,sort_keys=True))
    except ValidationFailure as error:
        print(json.dumps({'status':'REJECTED','variant':args.variant,'reason':str(error)},sort_keys=True))
        sys.exit(2)
