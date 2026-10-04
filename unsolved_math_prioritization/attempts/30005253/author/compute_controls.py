#!/usr/bin/env python3
"""Exact finite controls for the authored arguments; not a full-target certificate."""
import argparse
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path


def run():
    counts = {}
    minorants = 0
    for r in itertools.product(range(4), repeat=5):
        e = tuple(min(r[i:]) for i in range(5))
        assert all(e[i] <= e[i+1] for i in range(4))
        assert all(e[i] <= r[i] for i in range(5))
        assert tuple(min(e[i:]) for i in range(5)) == e
        for h in itertools.combinations_with_replacement(range(4), 5):
            if all(h[i] <= r[i] for i in range(5)):
                assert all(h[i] <= e[i] for i in range(5))
                minorants += 1
    counts['profiles'] = 4**5
    counts['admissible_minorants_checked'] = minorants
    selectors = 0
    for d in itertools.product(range(1,5), repeat=3):
        for perturbation in itertools.product((-F(1,10), F(0), F(1,10)), repeat=3):
            q = [F(x)+y for x,y in zip(d,perturbation)]
            for error in itertools.product((-F(1,5), F(0), F(1,5)), repeat=3):
                hat = [x+y for x,y in zip(q,error)]
                for j in range(3):
                    if hat[j] == min(hat):
                        assert min(d)-F(1,10) <= q[j] <= min(d)+F(1,10)+2*F(1,5)
                        selectors += 1
    counts['selector_bounds_including_ties'] = selectors

    rare = []
    for N in (16,64,256,1024,10000):
        a = math.isqrt(N)
        assert a*a == N
        product = F(1)
        for m in range(a,N+1):
            product *= 1-F(1,m)
        assert product == F(a-1,N)
        v = a
        # Conservative bad event: Ybar >= 1/2; tie is counted as bad.
        threshold = (3*v+3)//4
        validation_bad = F(sum(math.comb(v,k) for k in range(threshold,v+1)),2**v)
        success = (1-product)*(1-validation_bad)
        rare.append({'N':N,'a':a,'v':v,'no_zero_candidate':str(product),
                     'conservative_validation_bad':str(validation_bad),
                     'success_probability_lower_bound_exact':str(success),
                     'success_probability_lower_bound_decimal':float(success)})
    # Torus cumulative-sum transform checked exactly on small cyclic grids.
    torus = []
    for q in (2,3,5):
        image = set()
        for u in itertools.product(range(q),repeat=4):
            s=[]; acc=0
            for z in u:
                acc=(acc+z)%q; s.append(acc)
            image.add(tuple(s))
        assert len(image)==q**4
        torus.append({'modulus':q,'dimension':4,'image_size':len(image)})

    gaussian = []
    for z in [F(k,10) for k in range(11,201)]:
        r = 1+4*(1-1/z)+1/(z-1)
        assert r-4 == (z-2)**2/(z*(z-1))
        assert r>=4
    for t in [F(k,12) for k in range(-12,25)]:
        q = 3+2*(t-1)**2+t*t
        assert q == F(11,3)+3*(t-F(2,3))**2
    for m in (3,4,8,16,64,256,1024):
        p = 2*m
        exact = 1 + 4*(1-F(m,p)) + (F(2,3)-1)**2*4*F(m,p) + F(2,3)**2*F(m,p-m-1)
        assert exact == F(11,3)+F(4,9*(m-1))
        assert exact<4
        gaussian.append({'m':m,'p':p,'expected_shrunk_risk_exact':str(exact),
                         'expected_shrunk_risk':float(exact),'envelope_asymptotic':4})
    profile_models={'P_base':F(1)+F(1),'P_bayes':F(1),
                    'Q_base':F(2),'Q_bayes':F(2)}
    assert profile_models['P_base']==profile_models['Q_base']==2
    assert profile_models['P_bayes']<profile_models['P_base']
    assert profile_models['Q_bayes']==profile_models['Q_base']
    matrix=((1,2),(2,1))
    sup_inf=max(min(row) for row in matrix)
    inf_sup=min(max(row[j] for row in matrix) for j in range(2))
    assert (sup_inf,inf_sup)==(1,2)
    return {'passed':True,'arithmetic':'exact integers and fractions; decimals are display only',
            'finite_controls':counts,'rare_dip_controls':rare,'torus_bijections':torus,
            'gaussian_controls':gaussian,'same_profile_models':{k:str(v) for k,v in profile_models.items()},
            'minimax_order_control':{'sup_inf':sup_inf,'inf_sup':inf_sup},
            'full_target_proved':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='control_results.json')
    args=parser.parse_args()
    result=run()
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':result['passed'],'finite_controls':result['finite_controls'],
                      'output':args.output},sort_keys=True))
