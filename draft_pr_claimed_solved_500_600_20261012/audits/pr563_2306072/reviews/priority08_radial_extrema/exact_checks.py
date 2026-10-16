#!/usr/bin/env python3
"""Exact, dependency-free checks for the bounded source-priority comparison.

This checks finite algebra and source order bookkeeping, not extremality,
analytic continuation, the source theorems, or historical novelty.
"""
from fractions import Fraction as F
import json

NAMES = ('z','a2','a3','a4','x','eps','I','u')
NV = len(NAMES)
ZERO = (0,) * NV

def norm(p):
    q = {}
    for mon, coeff in p.items():
        mon = list(mon)
        power = mon[6] % 4
        mon[6] = power % 2
        coeff *= -1 if power >= 2 else 1
        mon = tuple(mon)
        q[mon] = q.get(mon, F(0)) + coeff
    return {mon: coeff for mon, coeff in q.items() if coeff}

def const(c): return {ZERO: F(c)} if c else {}
def var(n):
    mon = list(ZERO); mon[NAMES.index(n)] = 1
    return {tuple(mon): F(1)}
def add(*ps):
    q = {}
    for p in ps:
        for mon, coeff in p.items(): q[mon] = q.get(mon, F(0)) + coeff
    return norm(q)
def scale(p,c): return norm({m:v*F(c) for m,v in p.items()})
def mul(*ps):
    q = const(1)
    for p in ps:
        r = {}
        for a,b in q.items():
            for c,d in p.items():
                mon = tuple(x+y for x,y in zip(a,c))
                r[mon] = r.get(mon,F(0)) + b*d
        q = norm(r)
    return q
def power(p,n): return mul(*([p]*n))
def coeff(p,name,n):
    k = NAMES.index(name); q = {}
    for mon,v in p.items():
        if mon[k] == n:
            mon = list(mon); mon[k] = 0
            q[tuple(mon)] = v
    return norm(q)
def deriv(p,name):
    k=NAMES.index(name); q={}
    for mon,v in p.items():
        if mon[k]:
            m=list(mon); m[k]-=1; q[tuple(m)] = v*mon[k]
    return norm(q)
def subst(p,name,value):
    k=NAMES.index(name); q={}
    for mon,v in p.items():
        mon=list(mon); v*=F(value)**mon[k]; mon[k]=0
        mon=tuple(mon); q[mon]=q.get(mon,F(0))+v
    return norm(q)

z,a2,a3,a4,x,eps,I,u = map(var,NAMES)
f=add(z,mul(a2,power(z,2)),mul(a3,power(z,3)),mul(a4,power(z,4)))
H=scale(add(mul(x,power(f,2)),mul(power(x,2),power(f,3)),mul(power(x,3),power(f,4))),-1)
h2,h3,h4 = [coeff(H,'z',n) for n in (2,3,4)]
assert h2==scale(x,-1)
assert h3==scale(add(mul(const(2),a2,x),power(x,2)),-1)
assert h4==scale(add(mul(add(scale(a3,2),power(a2,2)),x),mul(scale(a2,3),power(x,2)),power(x,3)),-1)
A=add(scale(a3,2),power(a2,2),scale(a2,-6)); B=add(scale(a2,3),const(-3))
Phi=add(h2,mul(I,eps,add(h4,scale(h3,-3))))
assert Phi==scale(add(x,mul(I,eps,A,x),mul(I,eps,B,power(x,2)),mul(I,eps,power(x,3))),-1)

# Equality source's missing case: all stated nonzero premises and a
# permissible local branch value differing from zero and u0.
h=add(mul(add(const(-1),scale(I,F(-1,2))),power(u,2)),mul(add(const(2),scale(I,F(3,2))),u),scale(I,-1))
P=add(I,mul(power(add(u,const(-1)),2),h))
assert subst(P,'u',0)=={}
assert subst(deriv(P,'u'),'u',0)==add(const(2),scale(I,F(7,2)))
assert subst(P,'u',2)==I
assert subst(deriv(P,'u'),'u',2)==add(const(-2),scale(I,F(-1,2)))
assert subst(P,'u',1)==I
assert subst(deriv(P,'u'),'u',1)=={}
assert subst(deriv(deriv(P,'u'),'u'),'u',1)==const(2)
# With z1=1, omega=1, u0=2, c^2=-i, local Q(1)=i*c^2=1.
# Local R coefficient is (P''(1)/2)*c^4/(1-2)^2=-1;
# on z=e^(is), R~s^2 is positive. This is local compatibility only.
c2=scale(I,-1)
assert mul(I,c2)==const(1)
assert power(c2,2)==const(-1)
alpha=F(1); n=2
assert 2*(alpha-1)==0
assert n*alpha+2*(alpha-1)==2

# Candidate's denominator and degree-four sign mechanism.
e=F(1,10**24); eta=F(1,10**12)
assert 106*eta<1 and 24*eta<1  # |A|<3 and |B|<4 from candidate bounds.
assert 28*e<4  # |Delta + 4 i eps| < 28 eps^2 < 4 eps.
q=lambda t: t*t-F(2,5)*t**4
q1,qT=q(F(1)),q(F(7,4))
assert q1==F(3,5) and qT==F(-441,640)
assert q1-2000*eta>F(1,2)
assert qT+2000*eta<F(-1,2)
assert F(7,25)+7*eta<F(3,10)
assert F(25,81)-F(3,10)==F(7,810)
assert F(7,4)+333*e<F(9,5)

# Degree-three comparison at its Koebe limiting coefficients.
# For a2+i eps(mu a3+lambda a2), P0=4mu+lambda-mu v^2.
# d=-(4mu+lambda)t/2+mu t^3/6 gives q=mu t^2/3,
# of constant sign. The fourth-degree term supplies the t^4 reversal.
# Check the exact cancellation of the constant perturbation term.
mu,lam,t=F(7,3),F(-11,5),F(9,7)
d=-(4*mu+lam)*t/2+mu*t**3/6
dprime=-(4*mu+lam)/2+mu*t*t/2
assert dprime-d/t==mu*t*t/3

out={
 'status':'PASS',
 'arithmetic':'fractions.Fraction; sparse rational polynomial ring with I^2=-1',
 'checks':[
  'all z^2,z^3,z^4 extraction identities and exact candidate Phi',
  'explicit rational P witness for omitted Zhang-Ma local-order case',
  'source missing branch alpha=1,n=2 has required orders 0 and 2',
  'leading local circle positivity can coexist with the omitted branch',
  'candidate Phi numerator discriminant nonzero under recorded uniform bounds',
  'degree-four reversal signs after exact stated error margins',
  'actual-tip and witness-radius separation with exact gap 7/810',
  'degree-three first-order q has a fixed sign whereas degree-four q changes sign'
 ],
 'q_at_1':str(q1), 'q_at_7_over_4':str(qT),
 'source_gap_witness':{
   'P':'i+(u-1)^2*((-1-i/2)*u^2+(2+3i/2)*u-i)',
   'u0':'2','omega':'1','P_at_u0':'i','P_at_omega':'i',
   'Pprime_at_omega':'0','Pdoubleprime_at_omega':'2',
   'Pprime_at_u0':'-2-i/2','Pprime_at_0':'2+7i/2',
   'limitation':'local-order and leading-sign compatibility only; no actual support-point counterexample to the source theorem'
 },
 'not_certified':[
  'classical support-slit theorems','global rational-type support realization of source-gap witness',
  'full candidate analytic proof','historical novelty','unread 2014 commentary'
 ]
}
print(json.dumps(out,indent=2))
