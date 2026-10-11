#!/usr/bin/env python3
"""Independent falsification probes, not a proof or unrestricted search."""
import math,json,random
from independent_controls import Leaf,Node,rec

def envelope(e):
    if e<=0 or e>=1:return 0.0
    q=1-e
    if e<=0.5:return 1.5*e*e
    k=max(2,math.ceil(1/q))
    a=(1+math.sqrt(max(0,(k*q-1)/(k-1))))/k
    b=1-(k-1)*a
    return 3*(q*q-((k-1)*a**4+b**4))

def main():
    rng=random.Random(37430005116)
    worst={'union':(-1,None),'join':(-1,None)}
    counts={'union':0,'join':0}
    for trial in range(100000):
        n=rng.randrange(2,11)
        raw=[rng.random()**rng.choice([1,2,8]) for _ in range(n)]
        if trial%17==0:raw[rng.randrange(n)]=0
        s=sum(raw);w=[x/s for x in raw]
        ei=[rng.choice([0.,1.,0.5,2/3,3/4,rng.random()]) for _ in range(n)]
        for join in (False,True):
            c=sum(a**4*envelope(b) for a,b in zip(w,ei))
            e=sum(a*a*b for a,b in zip(w,ei))
            if join:
                e+=1-sum(a*a for a in w)
                c+=6*sum(w[i]**2*w[j]**2*(1-ei[i])*(1-ei[j]) for i in range(n) for j in range(i))
            gap=c-envelope(e)
            kind='join' if join else 'union'
            counts[kind]+=1
            if gap>worst[kind][0]:worst[kind]=(gap,{'w':w,'ei':ei,'edge':e,'upper':envelope(e),'trial_value':c})
    print(json.dumps({'status':'no violation found' if max(x[0] for x in worst.values())<1e-12 else 'VIOLATION','seed':37430005116,'counts':counts,'worst':worst,'scope':'numeric relaxed child-profile join/union probes only; no proof'},indent=2))
if __name__=='__main__':main()
