#!/usr/bin/env python3
"""Independent exact coefficient test for the point-pair transfer identity."""
from pathlib import Path
from itertools import permutations,combinations
from functools import cache
import hashlib,json,sys
P=Path(__file__).resolve().parent

def require(ok,data):
    if not ok:raise RuntimeError(data)
def av1324(p):return not any(p[i]<p[k]<p[j]<p[l] for i,j,k,l in combinations(range(len(p)),4))
def av213(p):return not any(p[j]<p[i]<p[k] for i,j,k in combinations(range(len(p)),3))
def inc(p):return sum(p[i]<p[j] for i,j in combinations(range(len(p)),2))
def S(p):
    inv=[0]*len(p)
    for i,v in enumerate(p,1):inv[v-1]=i
    return tuple(len(p)+1-v for v in inv[::-1])
def greedy_witness(p,b):
    j=p.index(b)
    return any(p[i]>b and p[k]>b and p[i]<p[k] for i in range(j) for k in range(j+1,len(p)))
@cache
def kernels(A,C):
    a=len(A);b=len(C);B=S(C);count=pairs=0
    for ix in combinations(range(a+b),a):
        upper=set(ix);ai=iter(v+b for v in A);bi=iter(B)
        p=tuple(next(ai) if i in upper else next(bi) for i in range(a+b))
        if not av1324(p) or not greedy_witness(p,b):continue
        count+=1
        X=sum(p[i]<=b<p[j] for i,j in combinations(range(a+b),2))
        require(inc(p)==inc(A)+inc(C)+X,('edge partition',A,C,p))
        pairs+=X
    return count,pairs
N=7
states={a:[p for p in permutations(range(1,a+1)) if av213(p)] for a in range(1,N+1)}
@cache
def dp(A,n):
    a=len(A)
    if n==a:return 1,inc(A)
    count=pairs=0
    for b in range(1,n-a+1):
        for C in states[b]:
            K,J=kernels(A,C)
            if not K:continue
            d,i=dp(C,n-a)
            count+=K*d
            pairs+=K*i+(inc(A)*K+J)*d
    return count,pairs
rows=[]
for n in range(1,N+1):
    actual_count=actual_pairs=0
    for pi in permutations(range(1,n+1)):
        if not av1324(pi):continue
        I=inc(pi);actual_count+=1;actual_pairs+=I
        F=sum(abs(i+v-(n+1)) for i,v in enumerate(pi,1))
        require(F<=2*I,('footrule',pi,F,I))
        for i,j in combinations(range(n),2):
            if pi[i]>=pi[j]:continue
            inside=tuple(pi[k] for k in range(i+1,j) if pi[i]<pi[k]<pi[j])
            require(all(inside[k]<inside[k+1] for k in range(len(inside)-1)),('rectangle',pi,i,j))
    predicted=[sum(dp(A,n)[j] for a in range(1,n+1) for A in states[a]) for j in range(2)]
    require(predicted==[actual_count,actual_pairs],('pair coefficient',n,predicted,actual_count,actual_pairs))
    rows.append({'n':n,'avoidance_count':actual_count,'total_increasing_pairs':actual_pairs})
files=['POINT_PAIR_TARGET.md',Path(__file__).name]
result={'status':'passed','scope':'Finite exact coefficient and geometry tests only; no asymptotic inference','max_n':N,'rows':rows,'kernel_pairs_evaluated':kernels.cache_info().currsize,
 'pins':{f:{'sha256':hashlib.sha256((P/f).read_bytes()).hexdigest(),'bytes':(P/f).stat().st_size} for f in files}}
output=P/(sys.argv[1] if len(sys.argv)>1 else 'PAIR_CHECK_NORMAL.json')
output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
