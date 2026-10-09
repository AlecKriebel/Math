"""Finite validation, never an all-graph proof. Run normally and under -O/-OO."""
from fractions import Fraction
from itertools import combinations,permutations,product
from collections import Counter
import random,json
from exact_model import require,graph,trees,constraints,member,maximum


def check(condition,message):
    if not condition:raise RuntimeError(message)


def rejects(fn):
    try:fn()
    except (ValueError,TypeError):return
    raise RuntimeError('expected rejection')


def k5_choice(w,k):
    es=tuple(combinations(range(5),2))
    require(member(5,es,w,k),'outside K5 polytope')
    for S in combinations(range(5),3):
        S=set(S);inside=[i for i,(a,b) in enumerate(es) if a in S and b in S]
        crossing=[i for i,(a,b) in enumerate(es) if (a in S)!=(b in S)]
        e=min(crossing,key=lambda i:w[i]);c=w[e]
        if sum(w[i] for i in inside)+2*c>2*k:continue
        a,b=es[e]
        if a not in S:a,b=b,a
        restS=sorted(S-{a});other=next(v for v in range(5) if v not in S and v!=b)
        path=(a,b,restS[0],other,restS[1])
        T=tuple(es.index(tuple(sorted(pair))) for pair in zip(path,path[1:]))
        val,witness=maximum(5,es,w,k,T)
        check(val.denominator==1,'K5 averaging choice failed')
        return T,val
    raise RuntimeError('averaging choice absent')


def validate_max(n,es,w,k,T):
    L,witness=maximum(n,es,w,k,T)
    z=[Fraction(a)-L*(i in T) for i,a in enumerate(w)]
    check(member(n,es,z,Fraction(k)-L),'maximum endpoint infeasible')
    eps=Fraction(1,97)
    zp=[Fraction(a)-(L+eps)*(i in T) for i,a in enumerate(w)]
    check(not member(n,es,zp,Fraction(k)-L-eps),'beyond maximum feasible')
    return L


def run():
    count=0
    rejects(lambda:graph(0,[]));rejects(lambda:graph(2,[(0,2)]))
    rejects(lambda:maximum(2,((0,1),),[1],0,(0,)))
    rejects(lambda:maximum(2,((0,1),),[Fraction(1)],1,(0,)))
    rejects(lambda:maximum(2,((0,1),),[2],1,(0,)))
    rejects(lambda:maximum(2,((0,1),),[1],1,()))
    check(not member(3,((0,1),),[2],1),'disconnected accepted')
    check(not member(1,((0,0),),[1],1),'loop accepted')
    check(not member(2,((0,1),),[-1],-1),'negative dilation accepted')
    check(maximum(1,((0,0),),[0],7,())[0]==7,'rank zero endpoint')
    check(maximum(2,((0,0),(0,1)),[0,4],4,(1,))[0]==4,'unique tree endpoint')
    es=((0,1),(0,1),(1,1));w=[2,3,0]
    check(maximum(2,es,w,5,(0,))[0]==2,'parallel first')
    check(maximum(2,es,w,5,(1,))[0]==3,'parallel second')
    # A fractional individual tree is not a counterexample.
    es=tuple(combinations(range(4),2));w=[3]*6
    star=(0,1,2);path=(0,3,5)
    check(validate_max(4,es,w,6,star)==Fraction(3,2),'star negative control')
    check(validate_max(4,es,w,6,path)==3,'path positive control')
    # Exact finite examples for the failed global-maximum and weighted-MST rules.
    es5=tuple(combinations(range(5),2));w5=[3,6,5,5,4,5,4,2,3,3]
    vals=[validate_max(5,es5,w5,10,t) for t in trees(5,es5)]
    check(max(vals)==Fraction(9,2),'global maximum obstruction changed')
    check(sum(v.denominator==1 for v in vals)==105,'global obstruction good count')
    w4=[11,13,11,8,8,9];ts4=trees(4,es)
    weights=[sum(w4[i] for i in t) for t in ts4]
    selected=[t for t,v in zip(ts4,weights) if v==max(weights)]
    check(selected==[star],'weighted unique maximum changed')
    check(validate_max(4,es,w4,20,star)==Fraction(15,2),'weighted obstruction')
    # Exhaust every 0..4 integral point on K4 at k<=4.
    for k in range(1,5):
      for w in product(range(k+1),repeat=6):
        if not member(4,es,w,k):continue
        vals=[validate_max(4,es,w,k,t) for t in ts4]
        check(any(v.denominator==1 and v>0 for v in vals),'low k failure');count+=1
    # Constructive K5 averaging on exact seeded points, with k=1 included.
    rng=random.Random(517);ts5=trees(5,es5)
    for j in range(1000):
      k=1+j%37;w=[0]*10
      for _ in range(k):
        for e in rng.choice(ts5):w[e]+=1
      T,L=k5_choice(w,k);check(validate_max(5,es5,w,k,T)==L,'K5 certificate disagreement')
      count+=1
    # A fake universal counterexample must be rejected by exhaustive checking.
    def certify_fake():
      vals=[maximum(4,es,[3]*6,6,t)[0] for t in ts4]
      require(all(v.denominator!=1 for v in vals),'integer-max tree exists')
    rejects(certify_fake)
    return {'passed':True,'tested_points':count,'all_graph_theorem':False,'assert_guard_dependency':False}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
