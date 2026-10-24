#!/usr/bin/env python3
"""Exact supporting identities; unbounded claims are proved in the companion notes."""
from collections import Counter
from itertools import product
from pathlib import Path
import json, random

# Target A(P4): p--b--c and p--z. Signed generator codes 1,2,3,4.
adj={frozenset(e) for e in ((1,2),(2,3),(1,4))}
def free_reduce(w):
    ans=[]
    for x in w:
        if ans and ans[-1]==-x:ans.pop()
        else:ans.append(x)
    return ans

def inverse(w):return [-x for x in reversed(w)]
def raag_reduce(w):
    w=list(w)
    while True:
        changed=False
        for i,x in enumerate(w):
            for j in range(i+1,len(w)):
                y=w[j]
                if y==-x:
                    w=w[:i]+w[i+1:j]+w[j+1:];changed=True;break
                if frozenset((abs(x),abs(y))) not in adj:break
            if changed:break
        if not changed:return w

images={1:[1],2:[2],3:[-3,1,3],4:[4,3]} # x,y,w,r

def expand(source):
    out=[]
    for x in source:out+=images[abs(x)] if x>0 else inverse(images[-x])
    return out

def comm(x,y):return x+y+inverse(x)+inverse(y)
relators=[comm([1],[2]),comm([2],[3]),[-4,1,4,-3]]
assert all(not raag_reduce(expand(w)) for w in relators)

rng=random.Random(21125)
def baseword():
    w=free_reduce([rng.choice((1,-1,3,-3)) for _ in range(rng.randrange(8))])
    yp=rng.randrange(-3,4)
    return w+[2 if yp>0 else -2]*abs(yp),w,yp
sample_count=0
for _ in range(8000):
    length=rng.randrange(1,9);eps=[rng.choice((-1,1)) for _ in range(length)]
    source=[]
    for i,e in enumerate(eps):
        source.append(4*e)
        if i+1<length:
            while True:
                w,fw,yp=baseword()
                # r^-1 B r pinches precisely in <x>; r B r^-1 in <w>.
                pinch=(eps[i]==-1 and eps[i+1]==1 and yp==0 and all(abs(x)==1 for x in fw)) or (eps[i]==1 and eps[i+1]==-1 and yp==0 and all(abs(x)==3 for x in fw))
                if not pinch:break
            source+=w
    assert raag_reduce(expand(source)),source
    sample_count+=1

# Integral abelianized-fiber identities, with arbitrary signed phi powers.
def binomial(n,k):
    ans=1
    for j in range(k):ans=ans*(n-j)//(j+1)
    return ans
checks=[]
for rank in range(3,31):
    zero=(0,)*rank
    def e(i):return tuple(int(j==i) for j in range(rank))
    def phi(v,n):return tuple(sum(binomial(n,j)*v[i+j] for j in range(rank-i)) for i in range(rank))
    def mul(x,y):
        v,k=x;w,l=y;w=phi(w,-k)
        return tuple(a+b for a,b in zip(v,w)),k+l
    def inv(x):
        v,k=x;return phi(tuple(-a for a in v),k),-k
    def cm(x,y):return mul(mul(mul(x,y),inv(x)),inv(y))
    s=(zero,-1);u={rank:(e(rank-1),0)}
    for i in range(rank-1,0,-1):u[i]=mul(mul(inv(u[i+1]),s),u[i+1])
    U=u[1];V=mul(mul(u[rank],s),inv(u[rank]))
    assert U==(e(0),-1)
    assert V==(tuple(-a for a in e(rank-2)),-1)
    W=cm(U,V)
    assert W==(tuple(-a for a in e(rank-3)),0)
    for _ in range(rank-3):W=cm(V,W)
    assert W==(tuple(-a for a in e(0)),0)
    recovered_s=mul(W,U)
    assert recovered_s==s
    recovered_top=inv(mul(V,inv(s)))
    assert recovered_top==(e(rank-2),0)
    for i in range(rank-3,-1,-1):
        recovered_top=cm(s,recovered_top)
        assert recovered_top==(e(i),0)
    assert all(v[0][-1]==0 and v[1]==-1 for i,v in u.items() if i<rank)
    checks.append({'rank':rank,'all_integral_identities_passed':True})

# A concrete balanced extension from H2 to H3: regular V4 plus a swap conjugator.
vertices=list(product((0,1),repeat=2));idx={v:i for i,v in enumerate(vertices)}
s=[idx[(1-a,b)] for a,b in vertices];a=[idx[(a,1-b)] for a,b in vertices];v=[idx[(b,a)] for a,b in vertices]
def compose(p,q):return tuple(p[q[i]] for i in range(4))
def pi(p):return tuple(p.index(i) for i in range(4))
assert compose(compose(pi(v),s),v)==tuple(a)
assert compose(s,a)==compose(a,s)
closure={tuple(range(4))};todo=list(closure)
while todo:
    w=todo.pop()
    for g in (s,a,v):
        z=compose(w,g)
        if z not in closure:closure.add(z);todo.append(z)
assert len(closure)==8
result={'scope':'Exact identities and bounded examples only; unbounded Britton and finite-cover arguments are in the proof notes','rank2_relator_images_trivial':True,'britton_reduced_nontrivial_samples':sample_count,'integral_fiber_checks':checks,'balanced_H3_quotient_order':len(closure),'balanced_H2_edge_orders':[2,2]}
Path(__file__).with_name('algebraic_reduction_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'britton_samples':sample_count,'integral_ranks_checked':len(checks),'balanced_quotient_order':len(closure)}))
