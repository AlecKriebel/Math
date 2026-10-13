"""Exact finite generator controls only, not a proof of recurrence."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(v,k):
    assert v,k
    C[k]+=1
def transitions(s,la):
    a,b,x,y=s;D=x+y+1
    return [((1,0,0,0),la/2),((0,1,0,0),la/2),((-1,0,1,0),F(a*(x+1),D)),((0,-1,0,1),F(b*(y+1),D)),((0,0,-1,0),F(x*(y+1),D)),((0,0,0,-1),F(y*(x+1),D))]
def gen(s,la,f):
    return sum(q*(f(tuple(a+b for a,b in zip(s,v)))-f(s)) for v,q in transitions(s,la) if q)
for la in [F(1,4),F(1,2),F(3,4),F(1),F(10)]:
    c=(1+1/la)/2
    for s in product(range(5),repeat=4):
        a,b,x,y=s;D=x+y+1
        V=lambda t:c*(t[0]+t[1])+t[2]+t[3]
        Z=lambda t:t[0]+t[2]-t[1]-t[3]
        rhs=c*la-F((c-1)*(a*(x+1)+b*(y+1))+2*x*y+x+y,D)
        ck(gen(s,la,V)==rhs,'weighted_workload_identity')
        ck(gen(s,la,Z)==F(y-x,D),'imbalance_identity')
        ck(gen(s,la,lambda t:Z(t)**2)==la+F(2*x*y+x+y-2*Z(s)*(x-y),D),'squared_imbalance_identity')
        if la<1:
            ck(F((c-1)*(a*(x+1)+b*(y+1))+2*x*y+x+y,D)>=F((c-1)*(a+b)+x+y,D),'service_lower_bound')
        for v,q in transitions(s,la):
            if q:ck(min(t+u for t,u in zip(s,v))>=0,'valid_state_boundary')
for la in [F(1,10),F(1,2),F(9,10),F(99,100)]:
    c=(1+1/la)/2;eta=(1-c*la)/2
    R=1
    while F(R,R+1)<c*la+eta:R+=1
    K=1
    while (c-1)*K/(R+1)<c*la+eta:K+=1
    for n in [0,1,R-1,R,R+1,10*R]:
        for w in [0,1,K-1,K,K+1,10*K]:
            if n>=R or w>=K:ck(F((c-1)*w+n,n+1)>=c*la+eta,'explicit_Foster_threshold')
for la in [F(1),F(3,2),F(100)]:
    for alpha,beta in [(F(2),F(1)),(F(101,100),F(1)),(F(100),F(1))]:
        for x in [0,1,10,10000]:ck(la*alpha-beta*F(x,x+1)>0,'affine_obstruction_high_load')
for x,y in product(range(101),repeat=2):
    D=x+y+1;rX=F(x*(y+1),D);rY=F(y*(x+1),D)
    ck(rX+rY==F(2*x*y,D)+1-F(1,D),'stationary_overlap_algebra')
    ck(rX-rY==F(x-y,D),'stationary_imbalance_algebra')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Finite exact controls of the source generator, boundary transitions, Foster thresholds and algebra; infinite stochastic proofs are in TURN_1.md.'},sort_keys=True,indent=2))
