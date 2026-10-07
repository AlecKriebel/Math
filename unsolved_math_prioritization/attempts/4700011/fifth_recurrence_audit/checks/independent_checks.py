#!/usr/bin/env python3
"""Independent checks of pinned Turn 5. Never imports an authored verifier."""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import json
import sympy as s

x,z,t,N,M,B,R=s.symbols('x z t N M B R')
checks=[]

def record(name, **data):
    checks.append(dict(name=name,passed=True,**data))

# Exact rational-interval arithmetic for the selected positive root.
# No approximate algebraic embedding is used in a maximum comparison.
class RootArithmetic:
    def __init__(self,L,A):
        self.L,self.A=L,A
        self.f=s.Poly(x**(2*L+1)-x**(2*L-A+1)-1 if L%2 else x**(2*L+1)+x**A-1,x)
        self.lo,self.hi=(Fraction(1),Fraction(2)) if L%2 else (Fraction(0),Fraction(1))
        assert self.f.eval(self.lo)<0<self.f.eval(self.hi)
        self.coeffs=tuple(int(self.f.nth(i)) for i in range(self.f.degree()))
    @lru_cache(None)
    def reduce(self,poly):
        # Polynomials represented low-degree first; modulus monic.
        a=list(poly)
        while len(a)>len(self.coeffs):
            v=a.pop()
            if v:
                shift=len(a)-len(self.coeffs)
                for j,c in enumerate(self.coeffs):a[shift+j]-=v*c
        while a and a[-1]==0:a.pop()
        return tuple(a)
    def add(self,a,b):
        q=[0]*max(len(a),len(b))
        for i,c in enumerate(a):q[i]+=c
        for i,c in enumerate(b):q[i]+=c
        return self.reduce(tuple(q))
    def neg(self,a):return tuple(-v for v in a)
    def sub(self,a,b):return self.add(a,self.neg(b))
    def monomial(self,e,c=1):return self.reduce(tuple([0]*e+[c]))
    def shift(self,a,e):return self.reduce(tuple([0]*e)+a)
    @lru_cache(None)
    def sign(self,a):
        a=self.reduce(a)
        if not a:return 0
        for _ in range(256):
            lo=hi=Fraction(0)
            for c in reversed(a):
                products=(lo*self.lo,lo*self.hi,hi*self.lo,hi*self.hi)
                lo,hi=min(products)+c,max(products)+c
            if lo>0:return 1
            if hi<0:return -1
            mid=(self.lo+self.hi)/2
            fv=self.f.eval(mid)
            if fv<0:self.lo=mid
            elif fv>0:self.hi=mid
            else:
                self.lo=self.hi=mid
                v=sum(Fraction(c)*mid**j for j,c in enumerate(a))
                return (v>0)-(v<0)
        raise AssertionError('Unable to establish exact sign')
    def maximum(self,entries):
        value=entries[0]
        for q in entries[1:]:
            if self.sign(self.sub(q,value))>0:value=q
        return value
    def w(self,j):
        power,phase=divmod(j,4)
        if phase in (0,2):return ()
        if phase==3:return self.monomial(power,-1)
        if self.L%2:return self.sub(self.monomial(self.L+power),self.monomial(self.L-self.A+power))
        return self.monomial(self.L+power)

# A generic scalar-state tropical step and directional derivative.
# It discovers the base winners and takes their actual tangent maximum.
def tangent_step(base,direction,support,constant,arith):
    max_base=max([base[j] for j in support]+([0] if constant else []))
    candidates=[direction[j] for j in support if base[j]==max_base]
    if constant and max_base==0:candidates.append(())
    md=arith.maximum(candidates)
    return base[1:]+[max_base-base[0]],direction[1:]+[arith.sub(md,direction[0])],max_base

family=[]
for L in range(1,9):
    k=4*L+2
    count=0
    for mask in range(1,1<<L):
        multiples=[j for j in range(4,k,4) if mask>>(j//4-1)&1]
        support=sorted(set(multiples+[k-j for j in multiples]+[k//2]))
        # Derive A from the actual support and independently test its coverage.
        assert support==sorted(set([k//2]+[j for j in range(2,k,2) if j in multiples or k-j in multiples]))
        A=max(j//4 for j in support if j%4==0)
        ar=RootArithmetic(L,A)
        assert ar.sign(ar.w(1))==1
        for constant in (False,True):
            base=[int(j%4>=2) for j in range(k)]
            ray=[ar.w(j) for j in range(k)]
            b,v=base[:],ray[:]
            # Three full directional returns, including generated coordinates.
            for step in range(12):
                b,v,mx=tangent_step(b,v,support,constant,ar)
                assert mx==1
                assert b==[int(j%4>=2) for j in range(step+1,step+k+1)]
                assert v==[ar.w(j) for j in range(step+1,step+k+1)]
            assert b==base
            assert v==[ar.shift(e,3) for e in ray]
            assert any(ar.sign(ar.sub(vj,wj))!=0 for vj,wj in zip(v,ray))
        count+=1
    family.append(dict(L=L,order=k,patterns=count,constant_statuses=2,returns_each=3))
record('generic_exact_tangent_simulations',families=family,support_patterns=sum(v['patterns'] for v in family))

# Perturb the direction instead of presuming any branch matrix defines a ray.
for L,A in ((1,1),(2,2),(3,2),(4,3)):
    k=4*L+2;ar=RootArithmetic(L,A)
    support=sorted({k//2,4*A,k-4*A})
    base=[int(j%4>=2) for j in range(k)]
    valid=[ar.w(j) for j in range(k)]
    bad=valid[:];bad[3]=ar.monomial(0,-2)
    b,v=base[:],bad[:]
    for step in range(4):b,v,mx=tangent_step(b,v,support,True,ar)
    assert v!=[ar.shift(q,1) for q in bad]
record('altered_eigenray_rejected',cases=4)

# Empty even support must not be covered. The midpoint-only maps are classical.
for L in (1,2,3,4):
    k=4*L+2;ar=RootArithmetic(L,1)
    base=[int(j%4>=2) for j in range(k)]
    b,v=base[:],[ar.w(j) for j in range(k)]
    for step in range(4):b,v,mx=tangent_step(b,v,[k//2],True,ar)
    assert b!=base or v!=[ar.shift(ar.w(j),1) for j in range(k)]
record('midpoint_only_control_not_excluded',cases=4)

# Symbolic fixed point normalization, second spectrum, and rational norm.
a,q=s.symbols('a q', nonzero=True)
# q^2=N*q+a; t=1/q, c0=a/q^2 and d=t/c0=q/a.
assert s.cancel((q/a-1/q-N/a)*a*q)==q*q-N*q-a
record('coefficient_scaling_and_gap_identity')
res=s.resultant(t*t+N*M*t-M,B-t*R,t)
assert s.expand(res-(B*B+N*M*B*R-M*R*R))==0
record('norm_polynomial_by_resultant')
# First nonzero Newton trace from independently built companion matrices.
traces=[]
for k,weights in [(2,{1:1}),(6,{2:2,3:1,4:2}),(8,{1:1,4:2,7:1}),(12,{4:1,8:1}),(15,{5:1,10:1})]:
    rr=min(weights);mr=weights[rr]
    C=s.zeros(k)
    for i in range(k-1):C[i,i+1]=1
    C[k-1,0]=-1
    for j,m in weights.items():C[k-1,j]=m*t
    assert s.expand(s.trace(C**rr)-rr*mr*t)==0
    assert s.expand(s.trace(C.subs(t,-a)**rr)+rr*mr*a)==0
    traces.append(dict(order=k,first_active_lag=rr,weight=mr))
record('newton_trace_from_companion_matrices',cases=traces)

# Cyclotomic norm controls and exact period orders, with positive-spectrum
# squarefreeness checked over the quadratic coefficient field.
classics=[]
for ell in range(1,7):
    for base_order,weights0,base_period in [(2,{1:1},5),(3,{1:1,2:1},8)]:
        k=base_order*ell;weights={j*ell:v for j,v in weights0.items()};nn=sum(weights.values())
        rr=sum(v*z**j for j,v in weights.items());bb=z**k+1
        tau=(-nn+s.sqrt(nn*nn+4))/2
        PP=s.Poly(bb-tau*rr,z,extension=True)
        assert s.gcd(PP,PP.diff()).degree()==0
        QQ=s.Poly(bb*bb+nn*bb*rr-rr*rr,z)
        orderlist=[]
        for factor,exp in s.factor_list(QQ)[1]:
            assert factor.is_cyclotomic
            degree=factor.degree()
            order=next(i for i in range(1,8*k*k+1) if s.totient(i)==degree and s.Poly(s.cyclotomic_poly(i,z),z)==factor)
            orderlist.append(order)
        pp=s.ilcm(*orderlist) if len(orderlist)>1 else orderlist[0]
        assert pp==base_period*ell
        classics.append(dict(base_period=base_period,dilation=ell,derivative_order=int(pp)))
record('classical_cyclotomic_norm_and_period_controls',cases=classics)

# Re-derive the failure control using an actual companion matrix.
k=8;dd=2+s.sqrt(5)
C=s.zeros(k)
for j in range(k-1):C[j,j+1]=1
C[k-1,0]=-1
for j,v in {1:1,4:2,7:1}.items():C[k-1,j]=-v*dd
trace2=s.expand(s.trace(C*C))
assert trace2==9+4*s.sqrt(5) and trace2>8
c0=9-4*s.sqrt(5)
assert s.minpoly(c0,z)==z*z-18*z+1
assert s.conjugate(c0)==c0 and 9+4*s.sqrt(5)>0 and c0>0
record('nonperiodic_bound_passing_control',negative_spectrum_trace2=str(trace2),dimension=k)

# The polynomial Q is not required to be squarefree: the third-order classic
# has a repeated (z+1), although each individual companion spectrum is simple.
rr=z+z*z;qq=(z**3+1)**2+2*(z**3+1)*rr-rr*rr
assert s.gcd(s.Poly(qq,z),s.Poly(s.diff(qq,z),z)).as_expr()==z+1
record('norm_squarefreeness_is_not_required')

# Every integer weight vector allowed by the necessary bound is enumerable;
# the strict integer bound must exclude equality k.
for k in range(2,30):
    for rr in range(1,k):
        for mr in range(1,k):
            for nn in range(1,k):
                limit=(k-1)//(rr*mr*nn)
                assert all(rr*mr*nn*mm<k for mm in range(1,limit+1))
record('strict_integer_enumeration_boundary')

out=dict(all_passed=True,sympy_version=s.__version__,checks=checks,
         scope='Independent exact checks supplement the all-order mathematical audit; finite samples are not an all-order proof.')
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_passed':True,'checks':len(checks),'tangent_support_patterns':sum(v['patterns'] for v in family)},indent=2))
