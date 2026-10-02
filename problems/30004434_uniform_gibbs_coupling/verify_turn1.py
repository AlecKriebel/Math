#!/usr/bin/env python3
"""Exact supplementary controls; the general argument is in TURN_1.md."""
from fractions import Fraction as Q
from itertools import product
import json
R=Q(1,2)
def K(a,b,t=1): return (1+a*b*R**t)/2
def bridge(x,a,b):
    v=Q(1); old=a
    for s in x: v*=K(old,s); old=s
    return v*K(old,b)/K(a,b,len(x)+1)
def plus(s,b,k,m): return K(s,1)*K(1,b,m+1-k)/K(s,b,m+2-k)
controls=0
rows=[]
for m in range(1,9):
    states=list(product((-1,1),repeat=m))
    laws={(a,b):{x:bridge(x,a,b) for x in states} for a,b in product((-1,1),repeat=2)}
    for law in laws.values(): assert sum(law.values())==1; controls+=1
    for k in range(1,m+1):
        mean=sum(x[k-1]*p for x,p in laws[1,1].items())
        assert mean==(R**k+R**(m+1-k))/(1+R**(m+1)); controls+=1
    # Exact common-uniform sequential coupling, aggregating its full joint law.
    joint={((),()):Q(1)}
    for k in range(1,m+1):
        new={}
        for (x,y),w in joint.items():
            px=plus(x[-1] if x else 1,1,k,m)
            py=plus(y[-1] if y else -1,-1,k,m)
            assert px>=py
            for sx,sy,v in [(1,1,py),(1,-1,px-py),(-1,-1,1-px)]:
                if v: new[x+(sx,),y+(sy,)]=new.get((x+(sx,),y+(sy,)),Q(0))+w*v
        joint=new
    for i,law in enumerate((laws[1,1],laws[-1,-1])):
        marginal={x:Q(0) for x in states}
        for xy,w in joint.items(): marginal[xy[i]]+=w
        assert marginal==law; controls+=1
    cost=sum(w*sum(a!=b for a,b in zip(x,y)) for (x,y),w in joint.items())
    expected=2*R*(1-R**m)/((1-R)*(1+R**(m+1)))
    assert cost==expected and cost>=R; controls+=2
    rows.append({'m':m,'exact_cost':str(cost),'joint_support':len(joint)})
probs={(a,b):K(a,1)*K(1,b)/K(a,b,2) for a,b in product((-1,1),repeat=2)}
assert sorted(set(probs.values()))==[Q(1,10),Q(1,2),Q(9,10)]
assert max(abs(probs[1,b]-probs[-1,b]) for b in (-1,1))==Q(2,5)
controls+=2
print(json.dumps({'status':'PASS','exact_controls':controls,'rows':rows,'scope':'Finite exact controls only; not independent review or a substitute for the general proof.'},indent=2))
