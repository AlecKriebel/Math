#!/usr/bin/env python3
"""Independent exact audit controls, not verification of intersection theory."""
import json
from fractions import Fraction
from math import comb, factorial
import sympy as s

q,u,z=s.symbols('q u z')
checks=0
def check(c, label):
    global checks
    if not c: raise AssertionError(label)
    checks+=1

# Count partitions and total part multiplicities using a dynamic program.
# This does not import or execute the frozen verifier.
D=12
p=[0]*(D+1); p[0]=1
for k in range(1,D+1):
    for n in range(k,D+1): p[n]+=p[n-k]

def ds(d): return s.divisors(d)
def sig(d,k): return sum(s.Rational(a)**k for a in ds(d))
def a(k):
    x=-q
    return s.Rational(k*k,2)*(x**k+1)/(x**k-1)-s.Rational(k,2)*(x+1)/(x-1)
A=[s.Integer(0)]+[s.cancel(a(k)) for k in range(1,D+1)]
U=[s.Integer(0)]+[s.cancel(sum(A[k] for k in ds(d))) for d in range(1,D+1)]
T=[s.Integer(0)]*(D+1)
for d in range(1,D+1):
    T[d]=s.cancel(sum(A[k]*sum(p[d-r*k] for r in range(1,d//k+1)) for k in range(1,d+1)))
L=[s.Integer(0)]+[sig(d,-1) for d in range(1,D+1)]
R=[s.cancel(T[d]+sum(L[j]*T[d-j] for j in range(1,d))) for d in range(D+1)]
# Recursive formal division, first by (1+L), then by P.
V=[s.Integer(0)]*(D+1); C=[s.Integer(0)]*(D+1)
for d in range(1,D+1):
    V[d]=s.cancel(R[d]-sum(L[k]*V[d-k] for k in range(1,d+1)))
    C[d]=s.cancel(V[d]-sum(p[k]*C[d-k] for k in range(1,d+1)))
    check(s.cancel(C[d]-U[d])==0,f'extraction degree {d}')
    check(s.cancel(U[d].subs(q,1/q)+U[d])==0,f'inversion degree {d}')
    check(s.limit(U[d],q,-1)==0,f'regularity degree {d}')

# The complete displayed degree-five rational example has the wrong overall sign.
num=272*q**9-539*q**8+760*q**7-629*q**6+302*q**5+302*q**4-629*q**3+760*q**2-539*q+272
den=6*(q-1)*(q*q+1)*(q*q-q+1)*(q**4-q**3+q*q-q+1)
printed=-num/den
check(s.cancel(R[5]+printed)==0,'degree-five entire printed rational function has opposite sign')
check(s.cancel(R[5]-printed)!=0,'degree-five printed expression is not the theorem')
check(R[5].subs(q,0)==-s.Rational(136,3),'degree-five trace constant')
check(s.diff(R[5],q).subs(q,0)==-s.Rational(277,6),'degree-five trace first derivative')

# Independent Bernoulli coefficients through exact cotangent series in SymPy.
N=7
cot=s.cot(u/2).series(u,0,2*N).removeO()
for d in range(1,9):
    F=s.expand(sum(k*cot-k*k*cot.subs(u,k*u) for k in ds(d))/48)
    check(F.coeff(u,-1)==0,f'pole cancellation d={d}')
    for n in range(1,N+1):
        I=s.cancel(F.coeff(u,2*n-1)*factorial(2*n-1))
        target=abs(s.bernoulli(2*n))*(sig(d,2*n+1)-sig(d,1))/(48*n)
        check(I==target,f'integral coefficient d={d} n={n}')
check(s.cancel(U[1])==0,'degree-one emptiness')
check(s.cancel(U[2]-(q+1)/(q-1))==0,'degree-two normalization')
check(s.cancel(U[3]-3*(q*q-1)/(q*q-q+1))==0,'degree-three connected normalization')
check(s.cancel(R[3]-U[3]-2*U[2])==0,'degree-three two-copy disconnected excess')

# Enumeration of elliptic unramified covers and component-weighted attachments.
# exp(sum sigma_1(m)/m Q^m) and derivative in component marker.
P=[s.Integer(1)] + [s.Integer(0)]*D
for n in range(1,D+1): P[n]=sum(k*L[k]*P[n-k] for k in range(1,n+1))/n
for n in range(D+1): check(P[n]==p[n],f'unramified cover count degree {n}')
PL=[sum(P[n-k]*L[k] for k in range(1,n+1)) for n in range(D+1)]
check(PL[1]==1,'one unramified sheet component weight')
check(PL[2]==s.Rational(5,2),'degree-two component weight')

print(json.dumps({'status':'PASS','independent_exact_assertions':checks,
    'degree_range':'1..12 for extraction; 1..8 for cotangent coefficients',
    'branch_pair_range':'1..7', 'partition_counts':p,
    'source_degree5':{'theorem_q0':str(R[5].subs(q,0)), 'printed_q0':str(printed.subs(q,0)),
    'full_rational_relation':'printed expression = negative of theorem',
    'theorem_first_terms':str(s.series(R[5],q,0,8))},
    'limits':'Exact algebra only; geometric arguments are audited in AUDIT.md.'},indent=2,sort_keys=True))
