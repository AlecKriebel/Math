#!/usr/bin/env python3
"""Exact controls for the fixed-factor classification obstruction."""
from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache
from collections import Counter
import sympy as sp
import json
C=Counter()
def ck(g,v):
    if not v:raise AssertionError(g)
    C[g]+=1
t,r,s,b1,b2,b3=sp.symbols('t r s b1 b2 b3')
ka=[0,1,r-1,s-3*r+2]
kb=[0,b1,b2-b1*b1,b3-3*b1*b2+2*b1**3]
@lru_cache(None)
def ev(word):
    if not word:return sp.Integer(1)
    candidates=[i for i in range(1,len(word)) if word[i]==word[0]]
    out=0
    for k in range(len(candidates)+1):
        for tail in combinations(candidates,k):
            block=(0,)+tail
            value=(ka if word[0]==0 else kb)[len(block)]
            for i,j in zip(block,block[1:]+(len(word),)):value*=ev(word[i+1:j])
            out+=value
    return sp.expand(out)
formulas=[0,b1,b2+(r-1)*b1*b1,b3+3*(r-1)*b1*b2+(s-3*r+2)*b1**3]
for n in range(1,4):ck('general_colored_product_identity',sp.expand(ev((0,1)*n)-formulas[n])==0)
sol={b1:2*t,b2:2*t+(2-4*r)*t*t,b3:2*t+(8-12*r)*t*t+(24*r*r-12*r-8*s)*t**3}
target=[0,2*t,2*t-2*t*t,2*t-4*t*t+4*t**3]
for n in range(1,4):ck('triangular_factor_moment_identity',sp.expand(formulas[n].subs(sol)-target[n])==0)
K=32*r*r-8*r-16*s-4
det=sp.expand((b1*b3-b2*b2).subs(sol))
ck('general_hankel_identity',sp.expand(det-t**3*(-8*(r-1)+K*t))==0)
ck('arcsine_normalization',sp.factor(det.subs({r:sp.Rational(3,2),s:sp.Rational(5,2)}))==4*t**3*(4*t-1))
for n in range(1,4):ck('scalar_factor_boundary',sp.expand(sol[[b1,b2,b3][n-1]].subs({r:1,s:1})-target[n])==0)

# Modest finite controls using genuine nonnegative discrete laws, normalized
# to mean one. Select a strictly positive rational p below the proved cutoff.
laws=0;witnesses=[]
for weight_den in range(2,13):
    for weight_num in range(1,weight_den):
        w=F(weight_num,weight_den)
        for x,y in [(F(0),F(1)),(F(1),F(2)),(F(1,3),F(5,2)),(F(2),F(3))]:
            mean=w*x+(1-w)*y
            rr=(w*x*x+(1-w)*y*y)/(mean*mean)
            ss=(w*x**3+(1-w)*y**3)/(mean**3)
            kk=32*rr*rr-8*rr-16*ss-4
            pp=F(1,4)
            while kk>0 and pp>=8*(rr-1)/kk:pp/=2
            tt=pp*(1-pp)
            bb1=2*tt
            bb2=2*tt+(2-4*rr)*tt*tt
            bb3=2*tt+(8-12*rr)*tt*tt+(24*rr*rr-12*rr-8*ss)*tt**3
            dd=bb1*bb3-bb2*bb2
            ck('genuine_factor_positive_variance',rr>1 and ss>=rr*rr)
            ck('strict_positive_projection_parameter',0<pp<F(1,2) and 0<tt<pp)
            ck('explicit_parameter_cutoff',kk<=0 or tt<8*(rr-1)/kk)
            ck('rational_hankel_counterexample',dd<0)
            ck('rational_symbolic_agreement',dd==tt**3*(-8*(rr-1)+kk*tt))
            laws+=1
            if len(witnesses)<4:witnesses.append({'r':str(rr),'s':str(ss),'p':str(pp),'determinant':str(dd)})
print(json.dumps({'problem_id':30004022,'turn':3,'status':'PASS','exact_assertions':sum(C.values()),
    'counts':dict(sorted(C.items())),'discrete_factor_controls':laws,'sample_witnesses':witnesses,
    'arithmetic':'exact rational arithmetic and symbolic polynomial identities',
    'scope':'Checks the general moment identities and modest factor controls. The universal classification and arbitrary-factor boundedness are proved analytically in TURN_3.md; original representation target remains unresolved.'},indent=2,sort_keys=True))
