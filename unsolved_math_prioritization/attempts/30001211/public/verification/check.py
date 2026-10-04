#!/usr/bin/env python3
"""Exact, bounded controls. Analytic proofs, not these samples, establish the lemmas."""
from fractions import Fraction as F
from functools import total_ordering
import json
from pathlib import Path

@total_ordering
class Q2:
    def __init__(self,a=0,b=0): self.a,self.b=F(a),F(b)
    @staticmethod
    def co(x): return x if isinstance(x,Q2) else Q2(x)
    def __add__(self,o):
        o=self.co(o);return Q2(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return Q2(-self.a,-self.b)
    def __sub__(self,o):return self+-self.co(o)
    def __rsub__(self,o):return self.co(o)+-self
    def __mul__(self,o):
        o=self.co(o);return Q2(self.a*o.a+2*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=self.co(o);norm=o.a*o.a-2*o.b*o.b
        return self*Q2(o.a/norm,-o.b/norm)
    def sign(self):
        a,b=self.a,self.b
        if not a:return (b>0)-(b<0)
        if not b:return (a>0)-(a<0)
        if a>0 and b>0:return 1
        if a<0 and b<0:return -1
        c=a*a-2*b*b
        return ((c>0)-(c<0))*(1 if a>0 else -1)
    def __lt__(self,o):return (self-self.co(o)).sign()<0
    def __eq__(self,o):
        o=self.co(o);return self.a==o.a and self.b==o.b
    def __hash__(self):return hash((self.a,self.b))
    def __abs__(self):return self if self.sign()>=0 else -self
    def conj(self):return Q2(self.a,-self.b)
    def norm(self):return self.a*self.a-2*self.b*self.b
    def encode(self):return [str(self.a),str(self.b)]

counts={}
def ck(group,condition):
    assert condition,group
    counts[group]=counts.get(group,0)+1

# A minimal 3-IET: inducing an irrational rotation on [0,1).
a=Q2(F(-1,2),F(1,2));b=Q2(F(1,4));c=1-a-b
ends=[Q2(),a,a+b,Q2(1)]
h=[b+c,c-a,-a-b]
def T(x):
    for i in range(3):
        if ends[i]<=x<ends[i+1]:return x+h[i]
    raise AssertionError('domain')
def Ti(x):
    for i in range(3):
        if ends[i]+h[i]<=x<ends[i+1]+h[i]:return x-h[i]
    raise AssertionError('inverse domain')
def iterate(x,n):
    f=T if n>=0 else Ti
    for _ in range(abs(n)):x=f(x)
    return x
L=1+b;theta=b+c
def R(x):
    z=x+theta
    return z-L if z>=L else z
for i in range(3):
    ck('field_parameters',4*h[i].a==int(4*h[i].a) and 4*h[i].b==int(4*h[i].b))
    ck('field_parameters',abs(h[i].conj())<4)
points=sorted(set([Q2(F(i,100)) for i in range(100)]+ends[:-1]))
for x in points:
    ck('inverse',Ti(T(x))==x)
    z=R(x);clock=1
    if z>=1:z=R(z);clock+=1
    ck('induction',z==T(x))
    ck('induction',clock==(2 if a<=x<a+b else 1))
    z=x
    for n in range(1,201):
        z=T(z);d=z-x
        ck('norm_orbits',d!=0)
        ck('norm_orbits',abs(d.norm())>=F(1,16))
        ck('norm_orbits',abs(d.conj())<=4*n)
        ck('norm_orbits',n*abs(d)>=F(1,64))
        ck('norm_orbits',n*min(abs(d),abs(d-1),abs(d+1))>=F(1,80))

# Two-sided endpoint separation versus each continuity cylinder.
endpoint_report=[]
for n in range(1,25):
    D=sorted(set(iterate(d,k) for d in ends[:-1] for k in range(-n,n+1)))
    spacing=min(D[i+1]-D[i] for i in range(len(D)-1))
    cuts=sorted(set([Q2(1)]+[iterate(d,-k) for d in ends[:-1] for k in range(n)]))
    for left,right in zip(cuts,cuts[1:]):
        mid=(left+right)/2;dl=iterate(left,n)-left;dm=iterate(mid,n)-mid
        ck('endpoint_cylinders',dl==dm)
        ck('endpoint_cylinders',abs(dm)>=spacing)
        ck('endpoint_cylinders',iterate(left,n) in D and left in D)
    endpoint_report.append({'n':n,'distinct_endpoints':len(D),'n_spacing':(n*spacing).encode()})

# Exact finite controls for the Tonelli/potential inequality.
mu=[(F(0),F(1,3)),(F(1,2),F(1,6)),(F(1),F(1,2))]
for y in [F(1,7),F(3,7),F(6,7)]:
    potential=sum(w/abs(z-y) for z,w in mu)
    for radius in [F(1,4),F(1),F(3)]:
        partial=sum(w for n in range(1,513) for z,w in mu if abs(z-y)<radius/n)
        ck('potential',partial<=radius*potential)

# Three complete stages of the general-sequence construction, exact rationals.
n=1;used=set();sweeps=[]
for k in range(1,4):
    start=n;left=F(0);bins=[]
    while left<1:
        assert n<=1000,'declared safety cap'
        width=min(1-left,F(1,k*n))
        m=1
        while True:
            z=left+width*(F(1,2)+F(1,8*m))
            if z not in used:break
            m+=1
        right=left+width
        ck('sweep',0<z<1)
        ck('sweep',max(abs(z-left),abs(z-right))*n<=F(2,3*k))
        ck('sweep',z not in used)
        used.add(z);bins.append((left,right,z,n));left=right;n+=1
    ck('sweep',bins[0][0]==0 and bins[-1][1]==1)
    for x,y in zip(bins,bins[1:]):ck('sweep',x[1]==y[0])
    sweeps.append({'stage':k,'first_index':start,'last_index':n-1,'count':len(bins)})

# Mutation controls: deliberately overstrong variants must be rejected.
middle=(a+a+b)/2
wrong_return=middle+h[1]+F(1,100)
ck('negative_controls',wrong_return!=R(R(middle))) # corrupted middle translation rejected
ck('negative_controls',not (Ti(T(Q2(F(1,10))))==Q2(F(2,10)))) # corrupted inverse target rejected
ck('negative_controls',all(n*abs(F(0)-F(1,2))>=1 for n in range(2,100))) # constant tail is not collapsing
result={'status':'PASS','arithmetic':'fractions.Fraction and exact Q(sqrt(2)) sign decisions','counts':counts,'total_assertions':sum(counts.values()),'endpoint_samples':endpoint_report,'sweep_blocks':sweeps,'limits':{'orbit_points':len(points),'orbit_steps_per_point':200,'endpoint_depth_max':24,'potential_terms':512,'sweep_stages':3,'sweep_index_cap':1000},'not_established':['General IET non-collapse or collapse','Minimality from a finite orbit sample','Unbounded-time conclusions from computation','Novelty or completeness of the literature search']}
print(json.dumps(result,indent=2))
