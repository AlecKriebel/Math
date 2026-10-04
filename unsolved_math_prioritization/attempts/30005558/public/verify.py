#!/usr/bin/env python3
"""Exact algebra checks for PROOF.md; not verification of geometric theorems.
Requires Python 3 and SymPy (tested with 1.14.0). No network or source PDF required.
"""
from collections import Counter
from fractions import Fraction as F
from math import factorial
import json
import sympy as s

x, q = s.symbols('x q')
checks = 0

def require(value, message):
    global checks
    assert value, message
    checks += 1

def parts(n, lo=1):
    if n == 0:
        yield ()
    for k in range(lo, n+1):
        for rest in parts(n-k, k):
            yield (k,) + rest

def divisors(n):
    return [k for k in range(1, n+1) if n % k == 0]

def sigma(n, power):
    return sum(F(k) ** power for k in divisors(n))

def a(k):
    return s.Rational(k*k, 2)*(x**k+1)/(x**k-1) - s.Rational(k, 2)*(x+1)/(x-1)

def same(a, b):
    return s.cancel(a-b) == 0

D = 10
partitions = [list(parts(d)) for d in range(D+1)]
p = [len(v) for v in partitions]
U = [s.Integer(0)] + [s.factor(sum(a(k) for k in divisors(d))) for d in range(1,D+1)]
T = [s.Integer(0)] + [s.factor(sum(a(k) for mu in partitions[d] for k in mu)) for d in range(1,D+1)]
L = [s.Integer(0)] + [s.Rational(sigma(d,-1)) for d in range(1,D+1)]
pL = [sum(p[d-k]*L[k] for k in range(d+1)) for d in range(D+1)]

for d in range(1,D+1):
    require(same(T[d],sum(p[d-m]*U[m] for m in range(1,d+1))), f'trace partition identity d={d}')
    R = T[d] + sum(L[k]*T[d-k] for k in range(1,d))
    extracted = sum((p[d-m]+pL[d-m])*U[m] for m in range(1,d+1))
    require(same(R,extracted), f'disconnected correction d={d}')
    require(same(U[d].subs(x,1/x),-U[d]), f'inversion oddness d={d}')
    require(s.limit(U[d],x,1)==0, f'regularity and zero at u=0 d={d}')

require(same(U[2].subs(x,-q),(q+1)/(q-1)), 'degree two source normalization')
require(same(U[3].subs(x,-q),3*(q*q-1)/(q*q-q+1)), 'degree three connected formula')
R3 = (T[3]+T[2]).subs(x,-q)
require(same(R3,(5*q**3-3*q*q-3*q+5)/((q-1)*(q*q-q+1))), 'source Theorem 1 d=3 example')
R4 = (T[4]+T[3]+s.Rational(3,2)*T[2]).subs(x,-q)
require(same(R4,(35*q**5-28*q**4+23*q**3+23*q*q-28*q+35)/(2*(q-1)*(q*q+1)*(q*q-q+1))), 'source Theorem 1 d=4 example')
R5 = (T[5]+T[4]+s.Rational(3,2)*T[3]+s.Rational(4,3)*T[2]).subs(x,-q)
require(R5.subs(q,0)==-s.Rational(136,3), 'trace theorem d=5 constant (printed example sign differs)')

# Independent formal division of exp(k*t)+1 by exp(k*t)-1, through t^(2N-1).
# Store the Laurent series shifted by t, so all exponents here are nonnegative.
N = 8
order = 2*N

def exp_ratio_shifted(k):
    numer = [F(2)] + [F(k**j,factorial(j)) for j in range(1,order+1)]
    denom = [F(k**(j+1),factorial(j+1)) for j in range(order+1)]
    out=[]
    for j in range(order+1):
        out.append((numer[j]-sum(denom[r]*out[j-r] for r in range(1,j+1)))/denom[0])
    return out

ratios = {k:exp_ratio_shifted(k) for k in range(1,D+1)}
# Bernoulli numbers calculated separately by the defining binomial recurrence.
B = [F(1)]
for m in range(1,2*N+1):
    B.append(-sum(F(s.binomial(m+1,k))*B[k] for k in range(m))/F(m+1))

values={}
for d in range(1,D+1):
    raw = [sum(F(k*k,2)*ratios[k][j]-F(k,2)*ratios[1][j] for k in divisors(d)) for j in range(order+1)]
    require(raw[0]==0,f'Laurent pole cancellation d={d}')
    for n in range(1,N+1):
        # F=-i U(e^(iu))/24: -i*i^(2n-1)=(-1)^(n-1).
        coefficient = F((-1)**(n-1),24)*raw[2*n]
        integral = coefficient*factorial(2*n-1)
        proposed = abs(B[2*n])*F(1,48*n)*(sigma(d,2*n+1)-sigma(d,1))
        require(integral==proposed,f'Bernoulli coefficient and factorial d={d}, n={n}')
        values[f'{d},{n}']=str(integral)
    for j in range(1,order+1,2):
        require(raw[j]==0,f'oddness after u substitution d={d}, shifted exponent={j}')

require(values['2,1']=='1/48','known I_2,1')
require(values['2,2']=='1/96','known I_2,2 with 3! restored')
require(values['2,3']=='1/48','known I_2,3 with 5! restored')
require(values['3,1']=='1/12','I_3,1')
require(values['4,1']=='11/48','I_4,1')

# Formal Chern-polynomial coefficients used in (10), before geometric identities.
t1,t2,h=s.symbols('t1 t2 h')
for g in range(2,9):
    lam=[s.Integer(1)]+list(s.symbols(f'l1:{g+1}'))
    def ell(j): return lam[j] if 0<=j<=g else s.Integer(0)
    def term(c):
        return sum((-1)**(a+b)*ell(a)*ell(b)*t1**(g-a)*t2**(g-b)/(t1*t2)
                   for a in range(g+1) for b in range(g+1) if a+b==c)
    require(s.expand(term(2*g)-lam[g]**2/(t1*t2))==0,f'Euler top g={g}')
    require(s.expand(term(2*g-1)+(t1+t2)*lam[g]*lam[g-1]/(t1*t2))==0,f'Euler next g={g}')
    residual=term(2*g-2)-(t1+t2)**2/(t1*t2)*lam[g]*ell(g-2)
    require(s.expand(residual-(lam[g-1]**2-2*lam[g]*ell(g-2)))==0,f'Euler maximum modulo Mumford g={g}')
    next_expected=-(t1**3+t2**3)/(t1*t2)*lam[g]*ell(g-3)-(t1+t2)*lam[g-1]*ell(g-2)
    require(s.expand(term(2*g-3)-next_expected)==0,f'Euler next coefficient before h multiplication g={g}')

result={
    'status':'PASS',
    'exact_assertions':checks,
    'sympy_version':s.__version__,
    'degree_range':'1..10',
    'branch_pair_range':'1..8',
    'chern_genus_range':'2..8',
    'sample_integrals':{k:values[k] for k in ['2,1','2,2','2,3','3,1','3,2','4,1','5,1']},
    'source_example_note':'The trace theorem gives -136/3 for the q=0 normalized d=5 expression; the displayed d=5 example in arXiv v2 has the opposite sign.',
    'limits':'Exact algebra checks only; no formal verification of intersection theory or cited geometric theorems.'
}
print(json.dumps(result,indent=2,sort_keys=True))
