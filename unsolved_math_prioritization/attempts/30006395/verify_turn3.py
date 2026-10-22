"""Exact recurrence controls and separately labeled critical-limit diagnostics.
The limit is proved analytically in TURN_3.md, not inferred from these samples.
"""
from fractions import Fraction as F
from math import prod,factorial
from collections import Counter
import json
import mpmath as mp
import sympy as sp
counts=Counter()
def ck(x,kind):
    assert x,kind
    counts[kind]+=1
def falling(n,v):return prod(range(n-v+1,n+1))
def parts(total,minsize=2):
    if not total:yield ();return
    for s in range(minsize,total+1):
        for tail in parts(total-s,s):yield (s,)+tail

def exact(n,k,p):
    t=F(k*k,n);rho=(1/p-1)/n
    aa=[F(0)]*(k+1)
    for s in range(2,k+1):aa[s]=t*rho**(s-1)*F(s**s,factorial(s))
    b=[F(0)]*(k+1);b[0]=F(1)
    for v in range(1,k+1):
        b[v]=sum((s*aa[s]*b[v-s] for s in range(2,v+1)),F(0))/v
        partition=F(0)
        for sizes in parts(v):
            term=prod(aa[s] for s in sizes)
            for mult in Counter(sizes).values():term/=factorial(mult)
            partition+=term
        ck(b[v]==partition,'coefficient_recurrence_vs_partition')
    R=[F(1)]
    for v in range(1,k+1):
        R.append(R[-1]*F((k-v+1)**2,k*k)/F(n-v+1,n))
        ck(R[v]==F(falling(k,v)**2*n**v,k**(2*v)*falling(n,v)),'falling_factorial_ratio_recurrence')
    value=sum(R[v]*b[v] for v in range(k+1))
    direct=F(1);z=1/p-1
    for v in range(2,k+1):
        for sizes in parts(v):
            r=len(sizes);term=F(falling(k,v)**2,falling(n,v)*k**(2*(v-r)))*z**(v-r)
            for s in sizes:term*=F(s**s,factorial(s))
            for mult in Counter(sizes).values():term/=factorial(mult)
            direct+=term
    ck(value==direct,'full_recurrence_vs_exact_forest_moment')
    return value
cases=0
for n in range(4,41):
    for k in range(2,min(n//2,14)+1):
        for p in [F(1,n),F(2,n),F(1,3),F(2,3)]:exact(n,k,p);cases+=1
# Symbolic coefficient recurrence, with e factored out.
for r in range(1,33):
    ar=sp.gamma(sp.Rational(r,4))/(2*sp.factorial(r)*2**sp.Rational(r,2)*sp.gamma(sp.Rational(r,2)))
    ar4=sp.gamma(sp.Rational(r+4,4))/(2*sp.factorial(r+4)*2**sp.Rational(r+4,2)*sp.gamma(sp.Rational(r+4,2)))
    ck(sp.simplify(ar4/ar-sp.Rational(1,4*(r+1)*(r+2)**2*(r+3)*(r+4)))==0,'gamma_four_step_coefficient_ratio')
ck(sp.gamma(1)/(2*sp.factorial(4)*2**2*sp.gamma(2))==sp.Rational(1,192),'zeroth_four_step_coefficient')
# High-precision diagnostics, kept separate from exact assertion count.
mp.mp.dps=60

def finite(k,n,c):
    t=mp.mpf(k)**2/n;rho=(1-c/n)/c
    aa=[mp.mpf(0)]*(k+1)
    for s in range(2,k+1):aa[s]=t*rho**(s-1)*mp.mpf(s)**s/mp.factorial(s)
    b=[mp.mpf(0)]*(k+1);b[0]=1
    for v in range(1,k+1):b[v]=sum(s*aa[s]*b[v-s] for s in range(2,v+1))/v
    R=mp.mpf(1);ans=mp.mpf(1)
    for v in range(1,k+1):
        R*=(mp.mpf(k-v+1)/k)**2/(1-mp.mpf(v-1)/n);ans+=R*b[v]
    return ans

def M0(lam):
    return 1+sum((lam*mp.e/mp.sqrt(2))**r*mp.gamma(mp.mpf(r)/4)/(2*mp.factorial(r)*mp.gamma(mp.mpf(r)/2)) for r in range(1,100))
diagnostics=[]
for lam in map(mp.mpf,['0.1','0.5','1']):
    lim=M0(lam)
    for k in [25,50,100,200]:
        n=int(mp.nint(mp.mpf(k)**mp.mpf('2.25')/lam));val=finite(k,n,mp.e)
        diagnostics.append({'lambda_target':str(lam),'k':k,'n':n,'finite_second_moment':mp.nstr(val,22),'limit_series':mp.nstr(lim,22),'absolute_difference':mp.nstr(abs(val-lim),10)})
# Integral/Gamma consistency at theta zero, avoiding endpoint singularities by u=x^4.
quad=[]
for r in range(1,9):
    # u^(r/2-1)du = 4 x^(2r-1) dx.
    integral=mp.quad(lambda x:4*x**(2*r-1)*mp.exp(-x**8),[0,1,mp.inf])
    value=mp.gamma(mp.mpf(r)/4)/2
    err=abs(integral-value)
    assert err<mp.mpf('1e-50')
    quad.append({'r':r,'absolute_error':mp.nstr(err,6)})
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'exact_parameter_cases':cases,'diagnostic_decimal_precision':60,'critical_convergence_diagnostics_not_certificates':diagnostics,'gamma_integral_diagnostics_not_certificates':quad,'scope':'Finite exact recurrence/algebra controls plus separately labeled high-precision diagnostics. Dominated convergence and all testing limitations are in TURN_3.md; no TV conclusion is inferred from second-moment divergence.'},indent=2,sort_keys=True))
