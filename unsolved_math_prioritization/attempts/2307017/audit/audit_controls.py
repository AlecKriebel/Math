#!/usr/bin/env python3
"""Independent bounded supplementary checks. These do not certify the proof."""
from fractions import Fraction as Q
from pathlib import Path
import json, math

out={'purpose':'Independent supplementary arithmetic checks; analytic audit is authoritative.'}
hs=[Q(0),Q(1,3),Q(-1,3),Q(3,4),Q(-3,4),Q(999999,1000000),Q(-999999,1000000)]
angles=[((1-h*h)/(1+h*h),2*h/(1+h*h)) for h in hs]
counts={'kernel':0,'nonlocal_near_origin':0,'nonlocal_far':0,'nonlocal_small_real_part':0,'poisson_domination':0,'near_zero_weight':0}
for c,s in angles:
    assert c>0 and c*c+s*s==1
    for n in [1,2,3,10,100,10**6]:
        for u in [Q(1,1000000),Q(1,2),Q(1),Q(7),Q(10**4)]:
            for v in [-10**8,-100,-1,0,1,100,10**8]:
                rr=u*u+v*v
                den=(n*c-u)**2+(n*s-v)**2
                num=(n*c+u)**2+(n*s-v)**2
                assert num-den==4*n*c*u
                counts['kernel']+=1
                if den==0: continue
                bound=2*c*u/den
                beta=u/(1+rr)
                if 4*rr<n*n:
                    assert bound<=8*c*u/(n*n)<=10*c*beta
                    counts['nonlocal_near_origin']+=1
                elif rr>4*n*n:
                    assert bound<=8*c*u/rr<=10*c*beta
                    counts['nonlocal_far']+=1
                elif u<c*n/2:
                    assert bound<=8*u/(c*n*n)<=40*beta/c
                    counts['nonlocal_small_real_part']+=1
    for r in [Q(1),Q(3,2),Q(10),Q(10**6)]:
        for t in [-10**12,-100,-1,0,1,100,10**12]:
            den=r*r-2*r*s*t+t*t
            assert den>=(1-abs(s))*(r*r+t*t)
            assert (1+t*t)/den<=1/(1-abs(s))
            counts['poisson_domination']+=1
    min_n=(c.denominator+c.numerator-1)//c.numerator
    directions=[(Q(1),Q(0)),(Q(-1),Q(0)),(Q(0),Q(1)),(Q(0),Q(-1)),(Q(3,5),Q(4,5)),(Q(-3,5),Q(-4,5))]
    for n in [min_n,min_n+1,10*min_n,100*min_n]:
        for dx,dy in directions:
            u=n*c+Q(249,1000)*dx
            v=n*s+Q(249,1000)*dy
            assert u>0
            assert (u-n*c)**2+(v-n*s)**2<Q(1,16)
            beta=u/(1+u*u+v*v)
            assert beta>=c/Q(6*n)
            counts['near_zero_weight']+=1
out['exact_rational_checks']=counts

# Independent check of the all-integer envelope, including smallest permitted R,
# p near integers/half-integers, large R, and phase-dependent sample counts.
envelopes=0;max_ratio=0.0
for R in [0.5,0.500001,0.75,1,1.000001,2,10,100,1000,10000]:
    for p in [-R,-0.500001,-0.5,-0.499999,0,0.249999,0.25,0.250001,0.499999,0.5,0.500001,R]:
        vals=[]
        for n in range(math.floor(p-3*R)-1, math.ceil(p+3*R)+2):
            vals.append(max(0.0,math.log(3*R/max(0.25,abs(n-p)))))
        actual=math.fsum(vals)
        assert actual<=6*R+2*math.log(12*R)+1e-9
        assert 6*R+2*math.log(12*R)<=14*R+1e-9
        max_ratio=max(max_ratio,actual/(14*R))
        envelopes+=1
out['layer_cake_envelope_checks']={'cases':envelopes,'largest_ratio_to_14R':max_ratio}

# Dyadic product tails: defects have explicitly summable bounds at both ends.
for j in range(-200,201):
    x=Q(2)**j
    factor=abs((x-3)/(x+3))
    assert 0<factor<1
    if j<=1: assert 1-factor<=2*x/3
    else: assert 1-factor<=6/x
out['exact_dyadic_defect_checks']=401
out['limitations']=['No numeric check proves infinite summability or a limsup.','The layer-cake checks use floating-point arithmetic, not interval arithmetic.','Rational arithmetic checks cover a finite adversarial grid.','No source bytes or frozen candidate files are modified.']
Path(__file__).with_name('AUDIT_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
