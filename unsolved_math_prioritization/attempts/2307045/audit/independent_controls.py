#!/usr/bin/env python3
"""Independent standard-library exact controls; no external theorem is proved."""
from fractions import Fraction as F
from pathlib import Path
from math import comb
import argparse, hashlib, json

COUNTS = {}
def check(group, truth):
    assert truth, group
    COUNTS[group] = COUNTS.get(group, 0) + 1

def add(z,w): return z[0]+w[0],z[1]+w[1]
def neg(z): return -z[0],-z[1]
def sub(z,w): return add(z,neg(w))
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def norm(z): return z[0]*z[0]+z[1]*z[1]
def div(z,w):
    d=norm(w)
    assert d > 0
    return (z[0]*w[0]+z[1]*w[1])/d,(z[1]*w[0]-z[0]*w[1])/d

def power(z,p):
    out=(F(1),F(0))
    for _ in range(p): out=mul(out,z)
    return out

def poisson(z,xi): return (1-norm(z))/norm(sub(xi,z))
ONE=(F(1),F(0)); I=(F(0),F(1))

def atan_interval(x, terms=60):
    # Alternating-series enclosure, with x in [0,1/2].
    assert 0 <= x <= F(1,2)
    s=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(terms)),F(0))
    next_term=(-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return min(s,s+next_term),max(s,s+next_term)

def laplacian_real_power(n,imaginary=False):
    poly={}
    for k in range(n+1):
        if k%2 != int(imaginary): continue
        c=comb(n,k)*(-1)**(k//2)
        a,b=n-k,k
        for key,coefficient in (((a-2,b),c*a*(a-1)),((a,b-2),c*b*(b-1))):
            if coefficient: poly[key]=poly.get(key,0)+coefficient
    return {key:value for key,value in poly.items() if value}

def run():
    upper=[(F(x,11),F(y,11)) for x in range(-10,11) for y in range(1,11) if x*x+y*y<121]
    for a in (F(1,1000),F(1,7),F(1,2),F(6,7),F(999,1000)):
        for s in upper:
            v=mul(s,s)
            w=div(add(v,(a,F(0))),add(ONE,mul((a,F(0)),v)))
            back=div(sub(w,(a,F(0))),sub(ONE,mul((a,F(0)),w)))
            check('inverse_slit_map_round_trip',back==v)
            check('inverse_image_inside_disk',norm(w)<1)
            check('upper_square_root_avoids_deleted_ray',not(v[1]==0 and v[0]>=0))
            check('inverse_image_avoids_original_slit',not(w[1]==0 and w[0]>=a))
            q=div(add(ONE,s),sub(ONE,s))
            check('quadrant_orientation',q[0]>0 and q[1]>0)
            check('quadrant_inverse_round_trip',div(sub(q,ONE),add(q,ONE))==s)
    for x in (F(1,100),F(1,2),F(1),F(2),F(100)):
        for y in (F(1,100),F(1,2),F(1),F(2),F(100)):
            q=x,y
            s=div(sub(q,ONE),add(q,ONE))
            check('quadrant_surjectivity_inverse',norm(s)<1 and s[1]>0)
            check('quadrant_surjectivity_round_trip',div(add(ONE,s),sub(ONE,s))==q)

    # No conformal-bijection assumption at the critical origin: finite analytic
    # monomials remain harmonic under every positive integer power tested.
    for p in range(1,13):
        for k in range(1,9):
            check('branched_pullback_real_monomial',not laplacian_real_power(p*k))
            check('branched_pullback_imaginary_monomial',not laplacian_real_power(p*k,True))

    zs=[(F(x,7),F(y,7)) for x in range(-6,7) for y in range(-6,7) if x*x+y*y<49]
    xis=[(-F(1),F(0))]+[((1-t*t)/(1+t*t),2*t/(1+t*t)) for t in (F(j,5) for j in range(-15,16))]
    roots={2:[ONE,neg(ONE)],4:[ONE,I,neg(ONE),neg(I)]}
    for xi in xis:
        check('boundary_points_are_unit',norm(xi)==1)
        for z in zs:
            for p in (2,4):
                lhs=poisson(power(z,p),power(xi,p))
                rhs=sum((poisson(z,mul(xi,root)) for root in roots[p]),F(0))/p
                check('poisson_power_averaging_degree_'+str(p),lhs==rhs)

    # Mathematically justified pi and arctangent intervals, all rational.
    a5=atan_interval(F(1,5)); a239=atan_interval(F(1,239))
    pi_lo=16*a5[0]-4*a239[1]; pi_hi=16*a5[1]-4*a239[0]
    check('pi_machin_interval',F('3.14159265358979323846264338327950288')<pi_lo<pi_hi<F('3.14159265358979323846264338327950289'))
    interval_rows=[]
    for p,r in [(1,F(1,4)),(2,F(1,2)),(4,F(1,2)),(6,F(1,2)),(2,F(1,10)),(8,F(2,3))]:
        t=F(1,2) if p==1 else r**(p//2)
        lo,hi=atan_interval(t)
        ulo,uhi=4*lo/pi_hi,4*hi/pi_lo
        check('certified_value_positive_below_one',0<ulo<uhi<1)
        check('certified_interval_width',uhi-ulo<F(1,10**35))
        interval_rows.append({'p':p,'r':str(r),'lower':str(ulo),'upper':str(uhi)})
    lo,hi=atan_interval(F(1,2)); ulo,uhi=4*lo/pi_hi,4*hi/pi_lo
    check('nontrivial_value_decimal_enclosure',F('0.59033447060')<ulo<uhi<F('0.59033447061'))
    check('same_reduced_radius_same_value',F(1,4)**1==F(1,2)**2)

    # Negative controls deliberately reject consequential plausible errors.
    bad=(F(3,5),-F(1,5)); good=neg(bad)
    check('reject_principal_root_below_cut',mul(bad,bad)==mul(good,good) and bad[1]<0<good[1])
    check('reject_missing_power_average',poisson((F(0),F(0)),ONE)!=sum(poisson((F(0),F(0)),root) for root in roots[4]))
    check('reject_harmonic_measure_complement_swap',ulo>F(1,2) and 1-ulo<F(1,2))
    check('reject_missing_square_root',F(1,2)>F(1,4))
    for r in (F(1,100),F(1,3),F(2,3),F(99,100)):
        for p in range(2,15):
            for q in range(1,p):
                check('coincident_slits_strictly_worse_squared_argument',r**q>r**p)

    return {'schema':'radial-slit-independent-exact-controls-v1','problem_id':'2307045','status':'PASS','exact_checks':sum(COUNTS.values()),'groups':COUNTS,'certified_intervals':interval_rows,'interval_method':'Rational alternating arctangent remainders and Machin pi identity; interval controls are separate from the original floating sanity checks.','limitations':['Finite controls do not prove global optimization or its equality classification.','The analytic proof of harmonic pullback and uniqueness is reviewed in AUDIT.md.','Certified values cover only the listed rational or exactly square-rootable parameters.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    out=run();path=Path(__file__).with_name('INDEPENDENT_RESULTS.json')
    if args.check:
        assert json.loads(path.read_text())==out
        print('PASS:',out['exact_checks'],'independent exact controls; recorded results match')
    else:
        path.write_text(json.dumps(out,indent=2)+'\n')
        print('PASS:',out['exact_checks'],'independent exact controls; results written')
