#!/usr/bin/env python3
"""Exact finite diagnostics, not a simulation or proof of an asymptotic law."""
from fractions import Fraction as F
from itertools import product, combinations
from math import isqrt, comb
from pathlib import Path
import hashlib, json

Q=F(3,4); R=F(1,4)
counts={}
def ck(test, group):
    assert test, group
    counts[group]=counts.get(group,0)+1

def pi(w):
    if not w: return F(1)
    p=F(1,2)
    for a,b in zip(w,w[1:]): p*=Q if a==b else R
    return p

def interval(w):
    left=F(0); mass=F(1); prev=None
    for a in w:
        p0=F(1,2) if prev is None else (Q if prev=='0' else R)
        if a=='0': mass*=p0
        else: left+=mass*p0; mass*=1-p0
        prev=a
    return left,left+mass

def m_const(w,tail):
    # w is nonempty; exact sum for the infinite word w + tail^infinity.
    s=sum((pi(w[:i]) for i in range(len(w)+1)),F(0))
    return s+pi(w)*(Q if w[-1]==tail else R)/(1-Q)

def vprefix(d):
    return ''.join('1' if isqrt(i)**2==i and i>=4 else '0' for i in range(1,d+1))

def P(j): return F(1,2)*R**(2*j-4)*Q**(j*j-2*j+2)
def ceilfrac(x): return -(-x.numerator//x.denominator)

for i in range(2):
    ck(sum((Q if i==j else R for j in range(2)),F(0))==1,'source')
    ck(sum(F(1,2)*(Q if i==j else R) for j in range(2))==F(1,2),'source')
    for j in range(2): ck(0<(Q if i==j else R)<1,'source')

for d in range(1,9):
    words=[''.join(w) for w in product('01',repeat=d)]
    ints=[interval(w) for w in words]
    ck(sum((pi(w) for w in words),F(0))==1,'cylinder_partition')
    ck(ints[0][0]==0 and ints[-1][1]==1,'cylinder_partition')
    for w,(a,b) in zip(words,ints):
        ck(b-a==pi(w),'cylinder_partition')
        ck(pi(w)<=F(1,2)*Q**(d-1),'cylinder_partition')
        ck(pi(w+'0')+pi(w+'1')==pi(w),'cylinder_partition')
    for i in range(len(ints)-1): ck(ints[i][1]==ints[i+1][0],'cylinder_partition')

for d in range(1,8):
    for tup in product('01',repeat=d-1):
        w=''.join(tup)+'0'
        a=m_const(w+'0','1'); b=m_const(w+'1','0')
        ck(a-b==pi(w),'endpoint_jump')
        for K in range(1,7):
            il=interval(w+'0'+'1'*K); ir=interval(w+'1'+'0'*K)
            boundary=interval(w+'1')[0]
            ck(il[1]==boundary==ir[0],'local_cylinders')
            ck(il[1]-il[0]==pi(w)*Q**K/4,'local_cylinders')
            ck(ir[1]-ir[0]==pi(w)*Q**K/12,'local_cylinders')
            # Check the full [prefix sum,prefix sum+3*mass] tail enclosure.
            for pre,endval in [(w+'0'+'1'*K,a),(w+'1'+'0'*K,b)]:
                S=sum((pi(pre[:i]) for i in range(len(pre)+1)),F(0))
                ck(S<=endval<=S+3*pi(pre),'tail_enclosure')
                for tail in '01':
                    value=m_const(pre,tail)
                    ck(abs(value-endval)<=3*pi(pre),'tail_enclosure')

series=F(0); last_n=0
for j in range(2,25):
    w=vprefix(j*j-1); p=P(j); series+=Q*p
    ck(w[-1]=='0' and len(w)==j*j-1,'square_rank')
    ck(pi(w)==p,'square_rank')
    ck(P(j+1)/p==R**2*Q**(2*j-1),'square_rank')
    ck(interval(w+'1')[0]==series,'square_rank')
    ck(vprefix((j+1)**2-1)==w+'1'+'0'*(2*j),'square_rank')
    lo,hi=interval(w+'1'+'0'*(2*j))
    ck(lo==series and hi-lo==p*Q**(2*j)/12,'square_rank')
    # Entire remaining series bounded by a geometric majorant of its ratios.
    majorant=Q*P(j+1)/(1-R**2*Q**(2*j+1))
    ck(0<majorant<p*Q**(2*j)/12,'rank_remainder')
    ck(majorant/(p*Q**j)<Q**j/12,'rank_remainder')
    width=p*Q**j; n=ceilfrac(width**-2)
    ck(1<=n*width**2<1+width**2,'subsequence')
    ck(n*p*p>=Q**(-2*j),'subsequence')
    ck(n>last_n,'subsequence'); last_n=n
    ck(p>=F(1,4)**(j*j-1),'subsequence')
    ck(n<=2*16**(j*j+j-1),'subsequence')

for j in range(18,81):
    K=j//2
    ck(12*Q**(j-K)<1,'window_inclusion')
    ck(Q**j<Q**K/12,'window_inclusion')
    ck(F(3,4)*Q**K<=Q**K,'tail_constants')
    ck(F(1,4)*Q**K<=Q**K,'tail_constants')

# Exhaustive small finite input sets: direct singleton-stopping recursion versus
# the exact prefix-count cost, plus the deterministic discrepancy bound.
words=[''.join(w) for w in product('01',repeat=3)]
U={w:sum(interval(w),F(0))/2 for w in words}
def recursive_cost(strings,k,depth=0):
    if len(strings)<=1:return 0
    parts=[[w for w in strings if w[depth]==a] for a in '01']
    if k<len(parts[0]):return len(strings)+recursive_cost(parts[0],k,depth+1)
    return len(strings)+recursive_cost(parts[1],k-len(parts[0]),depth+1)
for size in range(2,7):
    for inds in combinations(words,size):
        us=sorted(U[w] for w in inds)
        D=max(max(abs(F(i,size)-u),abs(F(i+1,size)-u)) for i,u in enumerate(us))
        for d in range(4):
            for tup in product('01',repeat=d):
                pre=''.join(tup); N=sum(w.startswith(pre) for w in inds)
                ck(abs(N-size*pi(pre))<=2*size*D,'uniform_count_bound')
        for k,w in enumerate(inds):
            Ns=[sum(s.startswith(w[:d]) for s in inds) for d in range(3)]
            cost=sum(N for N in Ns if N>1)
            ck(cost==recursive_cost(inds,k),'exact_cost')
            truncated_mean=sum((pi(w[:d]) for d in range(3)),F(0))
            ck(abs(cost-size*truncated_mean)<=2*size*3*D+3,'uniform_cost_bound')
            ck(all(sum(s.startswith(w) for s in inds)<=1 for w in words),'stopping_depth')

for n in range(2,101):
    ck(2*F(n*n+1,n**4)<=F(4,n*n),'grid_union_bound')
    H=1
    while Q**(H-1)>F(1,n**5): H+=1
    ck(Q**(H-1)<=F(1,n**5),'height_tail')
    ck(F(n*n,4)*Q**(H-1)<=F(1,4*n**3),'height_tail')
    ck(2*n*Q**(H-1)<=F(2,n**4),'height_tail')

# Exact binomial side probabilities at a fixed cylinder boundary, as a control
# of rank rounding and the order-statistic/binomial event identity.
for n in range(2,21):
    for t in [F(1,5),F(1,3),F(1,2),F(3,4)]:
        k=(n*t).numerator//(n*t).denominator+1
        law=[F(comb(n,r))*t**r*(1-t)**(n-r) for r in range(n+1)]
        ck(sum(law,F(0))==1,'binomial_indexing')
        ck(1<=k<=n,'binomial_indexing')
        ck(sum(law[k:],F(0))+sum(law[:k],F(0))==1,'binomial_indexing')

root=Path(__file__).resolve().parent
receipt={
 'status':'PASS', 'assertions':sum(counts.values()), 'groups':counts,
 'scope':'Exact finite identities, cylinder geometry, source parameters and cost diagnostics; no finite check certifies the asymptotic theorem.',
 'counterexample_sha256':hashlib.sha256((root/'COUNTEREXAMPLE.md').read_bytes()).hexdigest(),
 'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'approximate_rank_for_orientation_only':float(sum((Q*P(j) for j in range(2,15)),F(0))),
}
(root/'verification.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
