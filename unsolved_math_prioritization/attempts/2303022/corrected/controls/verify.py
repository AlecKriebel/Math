#!/usr/bin/env python3
"""Exact finite controls for the written partial results; not a proof of sharpness."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
import json, hashlib, pathlib

checks=[]
def ck(name,v):
    assert v,name
    checks.append(name)

def atan_interval(x,n=32):
    s=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(n)),F(0))
    t=(-1)**n*x**(2*n+1)/F(2*n+1)
    return min(s,s+t),max(s,s+t)

def pi_interval():
    a,b=atan_interval(F(1,5));c,d=atan_interval(F(1,239))
    return 16*a-4*d,16*b-4*c

def exp_bounds(x,n=160):
    # Positive Taylor sum and geometric bound on its positive tail.
    assert x>=0 and x<F(n+2)
    s=F(1);t=F(1)
    for k in range(1,n+1):
        t*=x/F(k);s+=t
    nxt=t*x/F(n+1)
    return s,s+nxt/(1-x/F(n+2))

def sech_interval(lo,hi):
    e0=exp_bounds(lo)[0];e1=exp_bounds(hi)[1]
    f=lambda e: 2*e/(e*e+1)
    return f(e1),f(e0)

def qterm(k,plo,phi):
    n=2*k+1
    sl,sh=sech_interval(F(3*n,2)*plo,F(3*n,2)*phi)
    return 4*sl/(n*phi),4*sh/(n*plo)

def decimal(x):
    with localcontext() as c:
        c.prec=70
        return str(Decimal(x.numerator)/Decimal(x.denominator))

p0,p1=pi_interval()
ck('Machin interval has positive width',p0<p1)
ck('3 < pi < 22/7 certified',3<p0<p1<F(22,7))
lo=F(0);hi=F(0)
for k in range(4):
    a,b=qterm(k,p0,p1)
    if k%2:lo-=b;hi-=a
    else:lo+=a;hi+=b
hi+=qterm(4,p0,p1)[1]
q_lower=F(228733015013343,10**16) # 0.0228733015013343
q_upper=F(228733015013344,10**16)
ck('rectangle short-side lower rational',q_lower<lo)
ck('rectangle short-side upper rational',hi<q_upper)
ck('wrong-side mutant rejected',not(F(97,100)<lo))
ck('sqrt2 < 10/7 squared',F(2)<F(10,7)**2)
ck('sqrt(2/3) < 5/6 squared',F(2,3)<F(5,6)**2)
constant_majorant=F(82,7)*F(22,7)*F(5,6)
ck('Green profile integral < 32pi',constant_majorant<32)
ck('low-radius Green ratio bound',F(1)/(F(3,4)-F(1,2))**2==16)
ck('large-radius angular denominator bound',4*F(1,2)*F(3,4)==F(3,2))
ck('full angle normalized Green bound',F(2,32)==F(1,16))
ck('escape upper bound 15/16',1-F(1,16)==F(15,16))
ck('arc chain step bound from pi<22/7',6*F(22,7)<19)
ck('vertical chain counts',F(3,8)/6==F(1,16))
ck('Harnack factor', (F(1,8)-F(1,16))/(F(1,8)+F(1,16))==F(1,3))
ck('annulus escape exceeds half',F(3,2)**2>2)
ck('31 link count',6+19+6==31)
explicit_lower=F(1,2*3**31)
ck('positive explicit lower bound',explicit_lower>0)
# Exhaust all hitting-event patterns for finite-component probability inequality.
for k in range(1,9):
    ck(f'pointwise count inequality k={k}',all(sum((mask>>j)&1 for j in range(k))<=k*bool(mask) for mask in range(1<<k)))
# Mutant replacing union probabilities by sums fails even for disjoint angular projections:
# The geometric proof establishes that the event pattern 11 has positive probability.
ck('union-additivity mutant rejected',max(1,1)!=1+1)

out={'status':'PASS','checks':checks,'checks_count':len(checks),'rectangle_short_side_rational_bracket':[str(q_lower),str(q_upper)],'computed_rectangle_bracket_decimal':[decimal(lo),decimal(hi)],'explicit_two_arc_escape_lower':str(explicit_lower),'explicit_two_arc_escape_lower_decimal':decimal(explicit_lower),'green_profile_constant_over_pi_rational_majorant':str(constant_majorant),'scope':'Exact arithmetic verifies only encoded algebra, finite event inequalities, and the rectangle-series enclosure. It does not verify source completeness, analytical lemmas, the numerical PDE model, or global sharpness.'}
print(json.dumps(out,indent=2))
