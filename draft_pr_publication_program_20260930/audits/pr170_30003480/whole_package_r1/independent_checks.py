"""Independent exact arithmetic and face controls, distinct from submitted checker."""
from fractions import Fraction as F
from itertools import product, chain
from math import prod
import json

checks=0
def require(ok,label):
    global checks
    if not ok:raise RuntimeError(label)
    checks+=1

def gram(t,axis):
    n=len(next(iter(t)))
    rows=[{},{}]
    for k,v in t.items():rows[k[axis]][k[:axis]+k[axis+1:]]=v
    keys=set(rows[0])|set(rows[1])
    aa=sum(rows[0].get(k,0)**2 for k in keys)
    bb=sum(rows[1].get(k,0)**2 for k in keys)
    ab=sum(rows[0].get(k,0)*rows[1].get(k,0) for k in keys)
    return (aa,ab,bb,aa*bb-ab*ab)

def extend(t,u):return {k+(bit,):v*u[bit] for k,v in t.items() for bit in [0,1]}

# Actual rational Gram contractions on zero faces, including zero tensor.
slice_cases=0
for entries in chain([(0,)*8],product([-1,0,1],repeat=8)):
    if slice_cases>=300:break
    t=dict(zip(product([0,1],repeat=3),map(F,entries)))
    old=[gram(t,i) for i in range(3)]
    norm=sum(v*v for v in t.values())
    for u in [(F(3,5),F(4,5)),(F(-5,13),F(12,13)),(F(1),F(0))]:
        t=extend(t,u)
        require(sum(v*v for v in t.values())==norm,'slice norm contraction')
        require([gram(t,i) for i in range(3)]==old,'slice full Gram contraction')
        require(all(gram(t,i)[3]==0 for i in range(3,len(next(iter(t))))),'all peeled factors rank one')
    slice_cases+=1

# Parity realization via squared masses and combinatorial off-diagonal absence.
support=[(0,0,0),(0,1,1),(1,0,1),(1,1,0)]
require(all(sum(x!=y for x,y in zip(a,b))!=1 for a in support for b in support),'no single-bit support pairs')
parity_cases=0
for numerators in product(range(7),repeat=3):
    t=tuple(F(x,12) for x in numerators)
    if any(2*x>sum(t) for x in t):continue
    a,b,c=t
    w=[1-(a+b+c)/2,(-a+b+c)/2,(a-b+c)/2,(a+b-c)/2]
    require(min(w)>=0 and sum(w)==1 and w[0]>=F(1,4),'parity endpoint weights')
    for axis in range(3):
        masses=[sum(w[j] for j,k in enumerate(support) if k[axis]==bit) for bit in [0,1]]
        require(masses==[1-t[axis],t[axis]],'actual parity diagonal masses')
    parity_cases+=1

def source_Q(d,r):
    slacks=[sum(d)-2*x for x in d]
    q1=prod(slacks)
    q2=prod(sum(sign[i]*r[i] for i in range(len(r))) for sign in product([-1,1],repeat=len(r)))/2
    return q1,q2,slacks

r=tuple(F(x,100) for x in [49,36,36,1]);d=tuple(x*x for x in r)
q1,q2,slacks=source_Q(d,r)
require(q1==F(168760917,305175781250),'Q1 printed fraction')
require(q2==F(23632249608,2384185791015625),'Q2 printed fraction')
require(q1-q2==F(2589624828909,4768371582031250)>0,'source witness exact difference')
require(min(slacks)>0 and all(0<x<F(1,4) for x in d),'witness hull and cube interior')
require(d[0]>F(6,25) and d[1]<F(5,36) and d[2]<F(5,36) and d[3]<F(99,10000),'inverse lambda thresholds')
require(F(103,300)<F(2,5),'exact spectral separation')
ghz=source_Q((F(1,4),)*3,(F(1,2),)*3)
require(ghz[:2]==(F(1,64),F(9,512)),'GHZ full sign product')
require(F(1,4)>F(3,16),'GHZ printed secondary direction')

# Hull patches and zero-polynomial witness.
for b,c in product([F(1,16),F(1,12),F(1,8)],repeat=2):
    t=(b+c,b,c);p=tuple(x*(1-x) for x in t)
    require(tuple(sum(p)-2*x for x in p)==(2*b*c,2*c*(1-b-c),2*b*(1-b-c)),'boundary hull slack identity')
    require(tuple(x*(1-x) for x in (1-t[0],*t[1:]))==p,'reflection determinant identity')
t=(F(5,16),F(1,8),F(1,8));p=tuple(x*(1-x) for x in t)
require(p==(F(55,256),F(28,256),F(28,256)) and 2*t[0]>sum(t) and min(sum(p)-2*x for x in p)>0,'hull zero polynomial excluded')
for t in [(F(1,3),)*3,(F(2,5),F(3,10),F(3,10))]:
    p=tuple(x*(1-x) for x in t)
    require(all(sum(p)-2*p[i]==2*t[(i+1)%3]*t[(i+2)%3]>0 for i in range(3)),'interior reflected-plane hull identity')

print(json.dumps({'status':'PASS','checks':checks,'slice_cases':slice_cases,'parity_cases':parity_cases,'Q1':str(q1),'Q2':str(q2),'difference':str(q1-q2),'determinant_hull_slacks':[str(x) for x in slacks],'finite_controls_are_not_universal_proof':True},sort_keys=True))
