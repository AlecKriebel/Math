"""Independent standard-library subset-DP audit; no author code imports."""
from functools import lru_cache
from itertools import combinations
from collections import Counter
import json
import random

C=Counter()
def ck(k,b):
    assert b,k
    C[k]+=1
def from_mask(n,mask):
    a=[0]*n
    for bit,(i,j) in enumerate(combinations(range(n),2)):
        if mask>>bit&1:a[i]|=1<<j;a[j]|=1<<i
    return tuple(a)
def subset_graph(a,S):
    ids=[i for i in range(len(a)) if S>>i&1]
    return tuple(sum(1<<j for j,v in enumerate(ids) if a[u]>>v&1) for u in ids)
@lru_cache(None)
def analyze(a):
    n=len(a);N=1<<n
    indep=[False]*N;indep[0]=True
    for S in range(1,N):
        v=(S&-S).bit_length()-1;R=S^(1<<v)
        indep[S]=indep[R] and not(a[v]&R)
    dp=[n+1]*N;part=[None]*N;dp[0]=0;part[0]=()
    for S in range(1,N):
        bit=S&-S;T=S
        while T:
            if T&bit and indep[T] and dp[S^T]+1<dp[S]:dp[S]=dp[S^T]+1;part[S]=(T,)+part[S^T]
            T=(T-1)&S
    deg=[x.bit_count() for x in a]
    return dp[-1],part[-1],tuple(S for S in range(N) if indep[S]),tuple(deg)
def core_property(a):
    S=sum(1<<i for i,x in enumerate(a) if x)
    if not S:return True
    h=subset_graph(a,S);k,_,_,deg=analyze(h);n=len(h);d=n-len(set(deg))
    return n<=(2*k-1)*d
def combine(a,b,complete=False):
    n=len(a);m=len(b)
    return tuple((x|(((1<<m)-1)<<n)) if complete else x for x in a)+tuple((x<<n)|((1<<n)-1 if complete else 0) for x in b)

inputs=[]
for n in range(1,7):inputs.extend(from_mask(n,m) for m in range(1<<(n*(n-1)//2)))
rng=random.Random(3242)
for n in range(7,10):
    inputs.extend(from_mask(n,rng.getrandbits(n*(n-1)//2)) for _ in range(96))
    for pattern in range(1<<(n-1)):
        a=(0,)
        for bit in range(n-1):a=combine(a,(0,),bool(pattern>>bit&1))
        inputs.append(a)
orders=Counter();classes=Counter();base=[]
for a in inputs:
    n=len(a);k,part,sets,deg=analyze(a);w=len(set(deg));d=n-w;orders[n]+=1
    ck('DP_color_partition',sum(S.bit_count() for S in part)==n and all(S in sets for S in part))
    if n>=2:
        ck('source_integer_diagnostic',n-1<=(2*k-1)*d)
        ck('rounding_exact',k>((w//2+d-1)//d))
        ck('degree_deficit_positive',d>=1)
    if n<=4:base.append(a)
    isolated=any(v==0 for v in deg)
    allmask=(1<<n)-1
    split=False
    for I in sets:
        K=allmask^I
        if all((a[v]&K)==(K^(1<<v)) for v in range(n) if K>>v&1):split=True;break
    tri=any(a[i]&a[j] for i,j in combinations(range(n),2) if a[i]>>j&1)
    if split:classes['split']+=1;ck('split_core_bound',core_property(a))
    if not tri:classes['trianglefree']+=1;ck('trianglefree_core_bound',core_property(a))
    if n>=2 and d==1:
        ck('antiregular_chromatic_exact',k==(n//2+1 if max(deg)==n-1 else (n+1)//2))
    if isolated:continue
    sizes=sorted(S.bit_count() for S in part);prefix=0
    for size in sizes:ck('proper_class_capacity',size<=prefix+d);prefix+=size
    ck('core_exponential_bound',n<=(2**k-1)*d)
    for I in sets:
        if I==0:continue
        c=I.bit_count();S=n-c;other=allmask^I
        cutdiff=sum(deg[i] for i in range(n) if other>>i&1)-sum(deg[i] for i in range(n) if I>>i&1)
        twiceinside=sum((a[i]&other).bit_count() for i in range(n) if other>>i&1)
        ck('independent_set_cut_identity',cutdiff==twiceinside)
        if w>=S:ck('representative_cut_lower_bound',w*(w+1)//2-S*(S+1)-d*S<=twiceinside)
    Delta=max(deg)
    for v in range(n):
        if deg[v]!=Delta:continue
        h=analyze(subset_graph(a,a[v]))[0]
        ck('maximum_neighborhood_capacity',n<=(2**(h+1)-1)*d)
        if k>=2**h:ck('local_chromatic_sufficient_condition',n<=(2*k-1)*d)

for a in base:
    for b in base:
        if not(core_property(a) and core_property(b)):continue
        u=combine(a,b);j=combine(a,b,True)
        ck('union_closure',core_property(u))
        ck('join_closure',core_property(j))
        ck('union_chromatic',analyze(u)[0]==max(analyze(a)[0],analyze(b)[0]))
        ck('join_chromatic',analyze(j)[0]==analyze(a)[0]+analyze(b)[0])
out={'status':'PASS','independent_assertions':sum(C.values()),'counts':dict(sorted(C.items())),
 'input_graphs_by_order':dict(sorted(orders.items())),'class_counts':dict(classes),
 'method':'Independent exact subset-partition dynamic programming: all labeled graphs through6, all threshold-construction strings at7-9, and96fixed-seed graphs per order7-9. No author helper imported. Finite controls supplement the reviewed proofs.'}
print(json.dumps(out,indent=2,sort_keys=True))
