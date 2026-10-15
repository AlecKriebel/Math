#!/usr/bin/env python3
"""New rational controls, independent of the archived four programs.
Finite identities only; no asymptotic or imported-geometry certificate.
"""
from fractions import Fraction as F
from math import comb, factorial
from functools import lru_cache
import json

COUNT = 0

def ck(ok):
    global COUNT
    assert ok
    COUNT += 1

B = [F(1)]
for m in range(1, 19):
    B.append(-sum(F(comb(m + 1, k))*B[k] for k in range(m))/F(m + 1))
a = [F(0)] + [(-1)**(j+1)*F(2**(2*j-1))*B[2*j]/F(factorial(2*j)*2*j) for j in range(1, 10)]
ck(a[1] == F(1, 12))
ck(a[2] == F(1, 360))
h = [F(1)]
for n in range(1, 10):
    h.append(sum(F(j)*a[j]*h[n-j] for j in range(1, n+1))/n)

@lru_cache(None)
def compositions(n):
    if n == 0:
        return ((),)
    return tuple((j,) + t for j in range(1, n+1) for t in compositions(n-j))

def beta_window(p, total, lo, hi):
    if p == total:
        return F(int(lo <= 1 <= hi))
    # Integer Beta CDF through its exact binomial tail, independently of simplex expansion.
    def cdf(x):
        return sum(F(comb(total-1,k))*x**k*(1-x)**(total-1-k) for k in range(p,total))
    return cdf(hi)-cdf(lo)

@lru_cache(None)
def rectangle(p, q, total, A, Bwin):
    r = total-p-q
    if r == 0:
        # The two selected coordinates sum to one, whereas the chosen rectangle lies below it.
        ck(A[1]+Bwin[1] < 1)
        return F(0)
    assert r >= 1
    c = F(factorial(total-1), factorial(p-1)*factorial(q-1)*factorial(r-1))
    out = F(0)
    for u in range(r):
        for v in range(r-u):
            coef = (-1)**(u+v)*F(factorial(r-1),factorial(u)*factorial(v)*factorial(r-1-u-v))
            xint = (A[1]**(p+u)-A[0]**(p+u))/F(p+u)
            yint = (Bwin[1]**(q+v)-Bwin[0]**(q+v))/F(q+v)
            out += c*coef*xint*yint
    ck(0 <= out <= 1)
    return out

A = (F(1,20),F(1,10)); W = (F(1,8),F(1,6))
rows=[]
for n in range(1,9):
    norm=F(0); first=F(0); mixed=F(0)
    for js in compositions(n):
        mass=F(1, factorial(len(js)))
        for j in js:
            mass *= a[j]
        mass /= h[n]
        norm += mass
        first += mass*sum(beta_window(2*j,2*n,*A) for j in js)
        mixed += mass*sum(rectangle(2*j,2*k,2*n,A,W) for i,j in enumerate(js) for l,k in enumerate(js) if i != l)
    ck(norm == 1)
    selected_first=sum(a[j]*h[n-j]/h[n]*beta_window(2*j,2*n,*A) for j in range(1,n+1))
    selected_mixed=sum(a[j]*a[k]*h[n-j-k]/h[n]*rectangle(2*j,2*k,2*n,A,W) for j in range(1,n) for k in range(1,n-j+1))
    ck(first == selected_first)
    ck(mixed == selected_mixed)
    rows.append({'n':n,'ordered_compositions':len(compositions(n)),'E_count_A':str(first),'E_count_A_count_B':str(mixed)})

# Exact log inequalities establish cutoff feasibility without floating-point sign claims.
x=F(1,10)
log_11_10_lower=x-x*x/2+x**3/3-x**4/4
eta_lower=F(3,5)*log_11_10_lower-F(1,20)
ck(eta_lower > F(1,220))
ck(F(11,10) < F(8,7))
# log(3/2) > (1/2)/(3/2)=1/3, so 2log(3/2)-1/2 >1/6.
ck(2*F(1,3)-F(1,2) == F(1,6))
# log(9/4) < 9/4-1=5/4, hence (3/5)log(9/4)<3/4<1.
ck(F(3,5)*F(5,4) < 1)
print(json.dumps({'status':'PASS','new_exact_assertions':COUNT,'method':'Bernoulli recurrence, ordered compositions, binomial Beta CDFs, direct polynomial integration of two-coordinate Dirichlet rectangles','finite_sizes':[1,8],'rectangles':{'A':[str(x) for x in A],'B':[str(x) for x in W]},'rows':rows,'eta_rational_lower_bound':str(eta_lower),'limits':'Finite algebra controls and rational sign witnesses only; not asymptotic certification.'},indent=2))
