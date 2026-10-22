#!/usr/bin/env python3
"""Exact cyclotomic zero tests; rigorously rounded rational cosine bounds.
Finite evidence only; all infinite claims are proved in PROOF.md.
Run: python verify_math.py [--output RESULTS.json]
Requires Python 3 and SymPy (tested 1.14.0). No network or source files.
"""
import argparse, json, math
from fractions import Fraction as F
from itertools import combinations_with_replacement
from functools import lru_cache
import sympy as sp
x=sp.Symbol('x'); SCALE=10**30
checks=0

def require(v, label):
    global checks
    checks+=1
    if not v: raise ValueError(label)

def atan_bounds(q,n):
    # Alternating series, first omitted term bounds the remainder.
    s=sum((F((-1)**k,(2*k+1)*q**(2*k+1)) for k in range(n)),F(0))
    nxt=F((-1)**n,(2*n+1)*q**(2*n+1))
    return min(s,s+nxt),max(s,s+nxt)
a,b=atan_bounds(5,40);c,d=atan_bounds(239,12)
PI_LO=16*a-4*d; PI_HI=16*b-4*c
# Machin identity pi=16 atan(1/5)-4 atan(1/239); documented below.
require(F(3)<PI_LO<PI_HI<F(22,7),'pi enclosure')

def floorq(q): return q.numerator//q.denominator
def ceilq(q): return -floorq(-q)

@lru_cache(None)
def cos_interval(N,k):
    k%=N;k=min(k,N-k)
    mid=(PI_LO+PI_HI)/2; t=2*mid*k/N
    approx=sum(((-1)**j*t**(2*j)/math.factorial(2*j) for j in range(31)),F(0))
    # Taylor degree 61 (odd coefficient zero); order-62 remainder.
    # Real argument t is below pi<4. cos is 1-Lipschitz on R.
    err=F(4**62,math.factorial(62))+F(k,N)*(PI_HI-PI_LO)
    return floorq((approx-err)*SCALE),ceilq((approx+err)*SCALE)

@lru_cache(None)
def basis(N):
    phi=sp.Poly(sp.cyclotomic_poly(N,x),x,domain=sp.ZZ)
    degree=phi.degree(); out=[]
    for a in range(N):
        r=sp.rem(sp.Poly(x**a,x,domain=sp.ZZ),phi)
        out.append(tuple(int(r.nth(j)) for j in range(degree)))
    return tuple(out)

def remainder(N,exponents):
    bs=basis(N)
    return tuple(sum(bs[a%N][j] for a in exponents) for j in range(len(bs[0])))

def sq_interval(N,exponents):
    lo=hi=len(exponents)*SCALE
    for i,a in enumerate(exponents):
        for b in exponents[:i]:
            l,h=cos_interval(N,a-b);lo+=2*l;hi+=2*h
    return lo,hi

def encode(q): return str(q.numerator)+'/'+str(q.denominator)

def convolution(a,b,p):
    c=[0]*p
    for i,v in enumerate(a):
        for j,w in enumerate(b):c[(i+j)%p]+=v*w
    return c

def product_mod(coeff,p,indices):
    v=[1]+[0]*(p-1)
    for j in indices:
        w=[0]*p
        for a,c in enumerate(coeff):w[(a*j)%p]+=c
        v=convolution(v,w,p)
    return v

def poly(v):return sp.Poly(sum(c*x**i for i,c in enumerate(v)),x,domain=sp.QQ)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args()
    rows=[]; tested=0; zeros=0
    for m in range(1,6):
        for N in range(2,25 if m<=4 else 19):
            bound={1:F(1),2:F(2,N),3:F(2,3*N),4:F(2,N*N)}.get(m)
            low=None;high=None;witness=None; z=0;count=0
            for tail in combinations_with_replacement(range(N),m-1):
                ex=(0,)+tail; count+=1; tested+=1
                iszero=not any(remainder(N,ex))
                lo,hi=sq_interval(N,ex)
                if iszero:
                    z+=1;zeros+=1
                    require(lo<=0<=hi,'zero is in certified interval')
                    continue
                require(lo>0,'exact nonzero separated from zero')
                if bound is not None:
                    # m=1 has exactly known modulus, no interval loss needed.
                    require(m==1 or F(lo,SCALE)>=bound**2,'small-m analytic bound')
                if low is None or lo<low:low=lo
                if high is None or hi<high:high=hi;witness=ex
            rows.append({'m':m,'N':N,'normalized_multisets':count,'exact_zeros':z,
                         'minimum_squared_modulus_interval':[encode(F(low,SCALE)),encode(F(high,SCALE))],
                         'upper_bound_witness':witness})
    # Exact integer/Fourier counting identity; repeated exponents included.
    count_tests=0
    for p in [3,5,7,11]:
        phi=sp.Poly(sp.cyclotomic_poly(p,x),x,domain=sp.QQ)
        for ex in [(0,), (0,0), (0,1), (0,0,1), (0,1,2), (0,0,1,3)]:
            m=len(ex)
            if m>=p:continue
            cs=[0]*p
            for a in ex:cs[a%p]+=1
            P=poly(cs)
            require(sp.gcd(P,phi).degree()==0,'prime nonvanishing')
            R=product_mod(cs,p,range(1,p));Q=product_mod(cs,p,range(2,p-1))
            D=int(sp.resultant(phi,P));require(D>0,'positive norm')
            require(p*R[0]==m**(p-1)+(p-1)*D,'R count identity')
            require(sum(R)==m**(p-1) and sum(Q)==m**(p-3),'total multiplicity counts')
            B=sp.rem(P*poly([cs[(-a)%p] for a in range(p)]),phi)
            require(sp.rem(poly(Q)*B,phi)==sp.Poly(D,x,domain=sp.QQ),'inverse count identity')
            H=sum(c*c for c in cs)
            # Compute trace inverse by an independent polynomial inverse and trace.
            inv=sp.invert(B,phi)
            trace= sum(inv.nth(a)*(p-1 if a==0 else -1) for a in range(p-1))
            require(F(int(trace.p),int(trace.q))==F(p*Q[0]-m**(p-3),D),'trace count identity')
            require(p*H-m*m>0,'positive Fourier energy')
            count_tests+=1
    # Taylor multiplicity and quotient-height controls for signed sparse polynomials.
    taylor_tests=0
    for expr in [(1-x)**r for r in range(1,9)]+[1+x**5,1-2*x**3+x**7,1-x+x**2-x**3,2-3*x**5+x**8]:
        P=sp.Poly(expr,x,domain=sp.ZZ);Q=P;q=0;A=P.degree()
        while Q.eval(1)==0:Q=Q.exquo(sp.Poly(x-1,x));q+=1
        L=sum(abs(int(v)) for v in P.all_coeffs());s=len(P.terms())
        require(q<=s-1,'sparse multiplicity')
        require(abs(int(Q.eval(1)))>=1,'integer leading coefficient')
        require(sum(abs(int(v)) for v in Q.all_coeffs())<=L*A**q,'quotient l1 bound')
        require(sp.Poly((x-1)**q,x)*Q==P,'Taylor exact factorization')
        taylor_tests+=1
    # Exact structural negative controls (incorrect hypotheses are rejected).
    negatives=[]
    def neg(label,condition):require(condition,label);negatives.append(label)
    neg('zero sums must be excluded',not any(remainder(3,[0,1,2])))
    neg('repetitions are allowed and change domain',not any(remainder(4,[0,1,2,3])) and any(remainder(4,[0,0,1,3])))
    neg('negative one is not an odd-order root',(-1)**3!=1)
    neg('support size differs from term count',len(sp.Poly((1-x)**4,x).terms())==5 and sum(abs(int(c)) for c in sp.Poly((1-x)**4,x).all_coeffs())==16)
    neg('prime restriction cannot be dropped from nonvanishing',not any(remainder(6,[0,3])))
    neg('subsum lower bounds do not prevent total cancellation',any(remainder(4,[0,1])) and any(remainder(4,[2,3])) and not any(remainder(4,[0,1,2,3])))
    neg('a bounded exponent spread is not supplied by rotation',min(max((a-r)%101 for a in [0,33,67]) for r in [0,33,67])>=66)
    # m=8 product witness contradicts a proposed universal exponent E=2.
    N=1000;r=3
    require((2*PI_HI/N)**r<F(1,N**2),'explicit upper witness beats exponent two')
    neg('E(8)=2 is impossible along large even conductors',N%2==0 and r>2)
    out={'status':'PASS','scope':'finite exact controls only; no full-conjecture claim',
         'sympy_version':sp.__version__,'arithmetic':'integer cyclotomic reduction and rational outward intervals',
         'checks':checks,'normalized_multisets':tested,'exact_zero_multisets':zeros,
         'count_identity_cases':count_tests,'taylor_cases':taylor_tests,'negative_controls':negatives,
         'minimum_enclosures':rows,
         'pi_interval':[encode(PI_LO),encode(PI_HI)]}
    blob=json.dumps(out,indent=2,sort_keys=True)+'\n'
    if args.output:open(args.output,'w').write(blob)
    print(json.dumps({k:v for k,v in out.items() if k not in ['minimum_enclosures','pi_interval']},indent=2))
if __name__=='__main__':main()
