#!/usr/bin/env python3
"""Exact, bounded checks for a fixed genus-12 sufficient coefficient test.

No source download, symbolic CAS, or untrusted upstream code is executed.
The mathematical scope is stated in RESEARCH.md; this does not test general type.
"""
from fractions import Fraction as F
from math import lcm
import json
from pathlib import Path


def datum(g, prongs, top_vertices=1, compensation=None):
    k = F(4*g*(g-1), 2*g-1)
    n = 2*g
    p = sum(prongs)
    q = sum((F(1,t) for t in prongs), F(0))
    ell = lcm(*prongs)
    r = q/F(len(prongs)+1) if compensation is None else F(compensation)
    top_k = p-q
    bottom_k = k-top_k
    bottom_n = n-p-top_vertices
    w_lambda = 12/k + F(1,2)
    c_h = -1-k/n
    c_b = k/n*(bottom_n-r)-bottom_k
    w_h = 12*(1+k/8)/(12+k/2)
    w_b = 12/w_lambda*(bottom_k/k+F(top_vertices-1,2))
    nf_h = F(2*g*g+2*g-1, g*g+3*g-1)
    nf_b = 2*(q*F(g*g+g-2,g*g+3*g-1)-F(3,2*g*g+6*g-2)*top_k)
    hu_h = F(2*(3*g*g+12*g-6),(g+8)*(3*g-1))
    hu_b = hu_h*q
    return dict(k=k,n=n,p=p,q=q,ell=ell,r=r,top_k=top_k,bottom_k=bottom_k,
                bottom_n=bottom_n,w_lambda=w_lambda,c_h=c_h,c_b=c_b,
                w_h=w_h,w_b=w_b,nf_h=nf_h,nf_b=nf_b,hu_h=hu_h,hu_b=hu_b)


def verify():
    d=datum(12,(9,1,1,1,1,1,1,1))
    expected={'k':F(528,23),'p':16,'q':F(64,9),'ell':9,'r':F(64,81),
        'top_k':F(80,9),'bottom_k':F(2912,207),'bottom_n':7,'w_lambda':F(45,44),
        'c_h':F(-45,23),'c_b':F(-15142,1863),'w_h':F(89,45),'w_b':F(2912,405),
        'nf_h':F(311,179),'nf_b':F(19472,1611),'hu_h':F(57,35),'hu_b':F(1216,105)}
    assert all(d[k]==v for k,v in expected.items())
    h0=d['c_h']+d['nf_h']; h1=d['w_h']-d['nf_h']
    b0=d['c_b']+d['nf_b']; b1=d['w_b']-d['nf_b']
    lo=-h0/h1;hi=-b0/b1
    assert (h0,h1)==(F(-902,4117),F(1936,8055))
    assert (b0,b1)==(F(1320286,333477),F(-354992,72495))
    assert (lo,hi)==(F(1845,2024),F(300065,371128)) and lo>hi
    assert b0+b1*lo==F(-940,1863)
    dual=-b1/h1
    constant=b0+dual*h0
    hu_coefficient=d['hu_b']-d['nf_b']+dual*(d['hu_h']-d['nf_h'])
    assert (dual,constant,hu_coefficient)==(F(2017,99),F(-940,1863),F(-286,105))
    # Test the linear identity on all normalized triples of denominator 100.
    count=0
    for i in range(101):
        for j in range(101-i):
            t,u=F(i,100),F(j,100);v=1-t-u
            h=d['c_h']+d['w_h']*t+d['nf_h']*u+d['hu_h']*v
            b=d['c_b']+d['w_b']*t+d['nf_b']*u+d['hu_b']*v
            assert b+dual*h==constant+hu_coefficient*v<0
            assert not (b>=0 and h>=0)
            count+=1
    assert count==5151
    # Integer twisting problem for a_e=ell/p_e: one length-1 bridge,
    # seven length-9 bridges, total twist sigma in [0,ell].
    gains=[]
    for sigma in range(10):
        a,r=divmod(sigma,9)
        min_energy=7*((9-r)*a*a+r*(a+1)**2)+sigma*sigma
        gain=F(16*sigma-min_energy,2)
        assert gain==F(sigma*(9-sigma),2)
        gains.append(gain)
    assert max(gains)==10 and [i for i,x in enumerate(gains) if x==10]==[4,5]
    assert F(d['ell'],8)*(d['p']-d['q'])==10
    # Conditional arithmetic thresholds; not valid new extension estimates.
    deficit=-(b0+b1*lo)
    critical_r=d['r']-deficit/(d['k']/d['n'])
    critical_w=deficit/(12*lo/d['w_lambda'])
    assert critical_r==F(26,99) and critical_w==F(470,9963)
    # Genus-13 boundary pair as a positive arithmetic control (not all strata).
    c=datum(13,(11,1,1,1,1,1,1,1))
    bn_h=F(2*(13+1),13+3);bn_b=bn_h*c['q']
    ch0=c['c_h']+bn_h;ch1=c['w_h']-bn_h
    cb0=c['c_b']+bn_b;cb1=c['w_b']-bn_b
    clo=-ch0/ch1;chi=-cb0/cb1
    assert (clo,chi)==(F(1071,1375),F(40409,51625)) and clo<chi
    assert cb0+cb1*clo==F(64,3025)
    return {'scope':'fixed sufficient coefficient test only; not a Kodaira-dimension computation',
      'status':'all assertions passed','genus':12,'dimension':23,
      'horizontal_lower_bound':str(lo),'witness_upper_bound':str(hi),
      'value_at_horizontal_boundary':str(-deficit),
      'dual_multiplier':str(dual),'dual_constant':str(constant),
      'hurwitz_weight_coefficient':str(hu_coefficient),
      'simplex_grid_controls':count,
      'integer_twist_gains':[str(x) for x in gains],
      'optimal_integer_twists':[4,5], 'optimal_gain':10,
      'conditional_compensation_threshold':str(critical_r),
      'conditional_weierstrass_improvement_threshold':str(critical_w),
      'genus13_pair_control':{'lower':str(clo),'upper':str(chi),'value_at_lower':str(F(64,3025))},
      'full_problem_solved':False,'independent_review':'not performed by this author'}

if __name__=='__main__':
    result=verify()
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    (Path(__file__).resolve().parent/'RESULTS.json').write_text(text)
    print(text,end='')
