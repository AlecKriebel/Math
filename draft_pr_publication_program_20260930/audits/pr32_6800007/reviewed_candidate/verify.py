#!/usr/bin/env python3
"""Exact algebra checks for the proposed formula, not a topology proof.
Requires SymPy (tested with 1.14.0); no network or numerical approximation.
"""
import json
from math import gcd
import sympy as s

x,y,p,q,t=s.symbols('x y p q t')
xs=[x,y,-x-y]; hs=[p,q,-p-q]
rs=[xs[j]-xs[i] for i in range(3) for j in range(i+1,3)]
ks=[hs[j]-hs[i] for i in range(3) for j in range(i+1,3)]
checks=[]
def eq(a,b,label):
    assert s.expand(a-b)==0,(label,s.expand(a-b))
    checks.append(label)

alpha=sum(a*b for a,b in zip(xs,hs))
eq(sum(rs),-4*x-2*y,'tangent determinant weight')
eq(sum(ks),-4*p-2*q,'loop determinant weight')
eq(alpha,(2*x+y)*p+(x+2*y)*q,'first monodromy coordinate')
eq(sum(a*b for a,b in zip(rs,ks)),3*alpha,'root-weight index three')

def c2(vals):
    return sum(vals[i]*vals[j] for i in range(len(vals)) for j in range(i+1,len(vals)))
a0=[a+b*t for a,b in zip(xs,hs)]
eq(-s.expand(c2(a0)).coeff(t,1),alpha,'SU3 negative c2 slant')
ar=[a+b*t for a,b in zip(rs,ks)]
delta=sum(rs)
virtual_c2=c2(ar)-sum(ar)*delta+delta**2-c2(rs)
eq(-s.expand(virtual_c2).coeff(t,1),3*alpha,'virtual c2 cancellation with nontrivial target determinant')
eq(-s.expand(c2(ar)).coeff(t,1),3*alpha-delta*sum(ks),'negative control: ordinary c2 has an extra term')
# This extra term is genuinely a nonzero polynomial, so dropping it is detected.
assert s.expand(delta*sum(ks))!=0
checks.append('negative control is nonzero')

D=s.Matrix([[-4,-2],[2*x+y,x+2*y]])
T=s.Matrix([[1,0],[-2,1]])
n=s.symbols('n',integer=True)
assert D.subs({x:n,y:-2*n})*T==s.Matrix([[0,-2],[6*n,-3*n]])
checks.append('S2xS1 unimodular basis change')
smith=[]
for nn in range(-12,13):
    vals=[0,-2,6*nn,-3*nn]
    g=0
    for a in vals:g=gcd(g,abs(a))
    det=12*nn
    if nn:
        assert g==gcd(2,3*nn)
        d2=abs(det)//g
        assert d2%g==0 and g*d2==12*abs(nn)
        smith.append({'n':nn,'torsion_invariant_factors':[g,d2],'free_rank':1})
    else:
        assert g==2 and det==0
        smith.append({'n':0,'torsion_invariant_factors':[2],'free_rank':2})
checks.append('25 exact Smith-normal-form determinantal-divisor checks')

# Coefficient-ring checks guard against using division or cancelling torsion.
torsion_count=0
for m in (2,4,6):
    for xx in range(m):
        for yy in range(m):
            for pp in range(-2,3):
                for qq in range(-2,3):
                    xxv=[xx,yy,-xx-yy];hh=[pp,qq,-pp-qq]
                    aa=sum(a*b for a,b in zip(xxv,hh))
                    bb=sum((xxv[j]-xxv[i])*(hh[j]-hh[i]) for i in range(3) for j in range(i+1,3))
                    assert (bb-3*aa)%m==0
                    assert (aa-((2*xx+yy)*pp+(xx+2*yy)*qq))%m==0
                    torsion_count+=1
checks.append(f'{torsion_count} finite torsion coefficient-ring cases')
# The RP2xS1 obstruction model has B=Z/2 and delta=1.
assert not [(xx,yy) for xx in range(2) for yy in range(2) if (-4*xx-2*yy-1)%2==0]
checks.append('RP2xS1 index-set obstruction model')

print(json.dumps({'pass':True,'sympy_version':s.__version__,'symbolic_and_group_checks':checks,
                  'torsion_cases':torsion_count,'S2xS1_examples':smith,
                  'scope':'Exact algebra and finite coefficient-ring checks only; no computational certification of h-principle, bundle classification, mapping-space exactness, or novelty.'},indent=2))
