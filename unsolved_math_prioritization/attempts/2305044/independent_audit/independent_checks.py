#!/usr/bin/env python3
"""Independent audit controls. No imports from the candidate packet.
Exact finite checks only; the universal sector/existence proofs are audited in prose.
Uses log-generating-series recurrence as an independent coefficient route.
"""
from fractions import Fraction as F
from math import prod, factorial, comb
import json
import sympy as s

def log_recurrence(a,b,x,N):
    a,b,x=map(F,(a,b,x))
    v=[F(1)]
    for n in range(1,N+1):
        v.append(sum((a*(-1)**(k+1)*x**k+b)*v[n-k]
                     for k in range(1,n+1))/n)
    return v

def convolution(a,b,x,n):
    return sum(prod((a-i) for i in range(k))/F(factorial(k))
               *prod((b+i) for i in range(n-k))/F(factorial(n-k))*x**k
               for k in range(n+1))

recurrence_cases=0
for a,b in [(F(3,2),F(1,32)),(F(3,2),F(1,14)),(F(1,9),F(1)),
            (F(8,9),F(1)),(F(1,8),F(7,8)),(F(13,5),F(11,7))]:
    for x in map(F,[-2,-1,0,1,2]):
        vals=log_recurrence(a,b,x,35)
        for n,v in enumerate(vals):
            assert v==convolution(a,b,x,n)
            recurrence_cases+=1

witnesses=[]
for b,n,expected in [(F(1,14),3,('33/686','20/343','1/98')),
                      (F(1,32),5,('2997183/268435456','3171231/268435456','5439/8388608'))]:
    plus=log_recurrence(F(3,2),b,1,n)[n]
    minus=log_recurrence(F(3,2),b,-1,n)[n]
    got=tuple(map(str,(plus,minus,abs(minus)-plus)))
    assert got==expected and 0<plus<abs(minus)
    witnesses.append({'degree':n,'alpha':'3/2','beta':str(b),'plus':str(plus),
                      'minus':str(minus),'gap':str(abs(minus)-plus)})

# Symbolic polynomial recurrence, different from candidate extraction routine.
a,b,x=s.symbols('alpha beta x')
v=[s.Integer(1)]
for n in range(1,6):
    v.append(s.expand(sum((a*(-1)**(k+1)*x**k+b)*v[n-k]
                         for k in range(1,n+1))/n))
assert s.expand(v[3].subs(x,1)-(a+b)*((a+b)**2-3*(a-b)+2)/6)==0
assert s.expand(v[3].subs(x,-1)+(a-b)*(a-b-1)*(a-b-2)/6)==0
j5=s.Poly(v[5].subs({a:s.Rational(3,2),b:s.Rational(1,32)}),x)
assert [str(j5.nth(k)) for k in range(6)]==[
    '1789359/268435456','208065/16777216','2145/524288',
    '-33/32768','3/4096','-3/256']

# Independently calculate positive-side endpoint used by the every-odd existence proof.
existence_endpoint_cases=[]
for n in range(3,62,2):
    m=(n-1)//2
    p0=log_recurrence(F(3,2),0,1,n)[n]
    phalf=log_recurrence(F(3,2),F(1,2),1,n)[n]
    assert p0<0 and phalf==F(2*comb(2*m,m),4**m)>0
    existence_endpoint_cases.append(n)

# Bernstein minimum replay by an independently formed Laurent product, not Chebyshev.
t,u,w=s.symbols('t u w',real=True)
bern=[]
for n in [3,5,7]:
    c=[s.prod(a-i for i in range(k))/s.factorial(k) for k in range(n+1)]
    # T_k recurrence constructed independently.
    T=[s.Integer(1),t]
    for k in range(2,n+1):T.append(s.expand(2*t*T[-1]-T[-2]))
    D=s.expand(sum(c)**2-sum(c[k]*c[l]*T[abs(k-l)]
              for k in range(n+1) for l in range(n+1)))
    quotient,rem=s.div(D,a*(1-t),a,t)
    assert rem==0
    P=s.Poly(s.expand(quotient.subs({a:1-u,t:1-2*w})),u,w)
    du,dw=P.degree(u),P.degree(w)
    cs=[]
    for i in range(du+1):
        for j in range(dw+1):
            cs.append(sum(P.coeff_monomial(u**k*w**l)*s.Rational(comb(i,k),comb(du,k))
                         *s.Rational(comb(j,l),comb(dw,l))
                         for k in range(i+1) for l in range(j+1)))
    minimum=min(cs)
    assert minimum=={3:-2,5:-7,7:-s.Rational(332,15)}[n]
    bern.append({'degree':n,'minimum':str(minimum)})

print(json.dumps({'status':'PASS','method':'independent logarithmic-series coefficient recurrence',
      'finite_recurrence_convolution_comparisons':recurrence_cases,
      'witnesses':witnesses,'symbolic_cubic_identities':'PASS',
      'symbolic_fifth_degree_vector':'PASS','existence_endpoint_indices':existence_endpoint_cases,
      'independent_bernstein_minima':bern,
      'finite_checks_are_universal_proofs':False},indent=2,sort_keys=True))
