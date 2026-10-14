#!/usr/bin/env python3
"""Finite regressions only; all asymptotic claims have separate proofs."""
from pathlib import Path
from itertools import permutations, combinations
from functools import cache
from fractions import Fraction
from math import comb
import hashlib,json,sys
P=Path(__file__).resolve().parent
N=8

def require(ok,data):
    if not ok: raise RuntimeError(data)
def av213(p):return not any(p[j]<p[i]<p[k] for i,j,k in combinations(range(len(p)),3))
def av1324(p):return not any(p[i]<p[k]<p[j]<p[l] for i,j,k,l in combinations(range(len(p)),4))
def lis(p):
    dp=[]
    for i,v in enumerate(p):dp.append(1+max([dp[j] for j in range(i) if p[j]<v],default=0))
    return max(dp,default=0)
def S(p):
    inv=[0]*len(p)
    for i,v in enumerate(p,1):inv[v-1]=i
    return tuple(len(p)+1-v for v in inv[::-1])
def std(p):
    r={v:i+1 for i,v in enumerate(sorted(p))};return tuple(r[v] for v in p)
def A(p):return (1,)+tuple(range(p,1,-1))
def skew_blocks(p):
    answer=[];start=0
    for j in range(1,len(p)+1):
        if j==len(p) or min(p[:j])>max(p[j:]):
            answer.append(std(p[start:j]));start=j
    return answer
@cache
def kernel(U,C):
    a=len(U);b=len(C);V=S(C);count=pairs=0
    for ix in combinations(range(a+b),a):
        upper=set(ix);ui=iter(v+b for v in U);vi=iter(V)
        p=tuple(next(ui) if j in upper else next(vi) for j in range(a+b))
        j=p.index(b)
        greedy=any(p[i]>b and p[k]>b and p[i]<p[k] for i in range(j) for k in range(j+1,a+b))
        if not greedy or not av1324(p):continue
        count+=1;pairs+=sum(p[i]<=b<p[j] for i,j in combinations(range(a+b),2))
    return count,pairs
states={n:[p for p in permutations(range(1,n+1)) if av213(p)] for n in range(1,N+1)}
heights={p:lis(p) for ss in states.values() for p in ss}
s2=[1]+[2**(n-1) for n in range(1,N+1)]
s3=[1,1]
for n in range(2,N+1):s3.append(3*s3[-1]-s3[-2])
state_rows=[]
for n,ss in states.items():
    c2=sum(heights[p]<=2 for p in ss);c3=sum(heights[p]<=3 for p in ss)
    require((c2,c3)==(s2[n],s3[n]),('height counts',n,c2,c3))
    for p in ss:
        bs=skew_blocks(p)
        require(p[0]==n-len(bs[0])+1,('first minimum block',p,bs))
        require(S(p).index(n)+1==len(bs[0]),('lower max position',p))
        if heights[p]<=2:require(all(b==A(len(b)) for b in bs),('unique H2 blocks',p,bs))
    state_rows.append({'size':n,'all_states':len(ss),'LIS_at_most_2':c2,'LIS_at_most_3':c3})
row_checks=0;family_checks=0
for p in range(2,9):
    for q in range(1,min(N,9-p)+1):
        for C in states[q]:
            d=len(skew_blocks(C)[0]);want=comb(p+q-1,q)-comb(p+d-2,d-1)
            require(kernel(A(p),C)[0]==want,('exact A_p row',p,C,d,want,kernel(A(p),C)))
            row_checks+=1
for p in range(2,9):
    for q in range(2,11-p):
        k,j=kernel(A(p),A(q));want=comb(p+q-2,q)
        require(k==want and 2*j==p*q*k,('dense family',p,q,k,j));family_checks+=1
# Equation (8), checked coefficientwise without floating point radicals.
series_checks=0
for p in range(2,9):
    for q in range(1,N+1):
        direct=sum(comb(p+q-1,q)-comb(p+len(skew_blocks(C)[0])-2,len(skew_blocks(C)[0])-1)
                   for C in states[q] if heights[C]<=3)
        transform=s3[q]*comb(p+q-1,q)
        subtraction=sum(s3[q-1-r]*s2[r]*comb(p+r-1,r) for r in range(q))
        require(direct==transform-subtraction,('exact W coefficients',p,q,direct,transform,subtraction))
        series_checks+=1
# Enumerate actual canonical chains, retaining their exact product of K's.
# An arbitrary number of cells is allowed; n<=8 is only a finite regression scope.
actual=[1]+[sum(av1324(p) for p in permutations(range(1,n+1))) for n in range(1,N+1)]
b=[0]*(N+1);path_rows=[];run_tables={}
def paths(remaining,prefix=(),weight=1):
    if remaining==0:
        yield prefix,weight;return
    for a in range(1,remaining+1):
        for C in states[a]:
            k=kernel(prefix[-1],C)[0] if prefix else 1
            if k:yield from paths(remaining-a,prefix+(C,),weight*k)
for n in range(1,N+1):
    total=chain_count=0;tab={}
    for chain,w in paths(n):
        total+=w;chain_count+=1
        if all(heights[C]<=2 for C in chain):b[n]+=w
        for i in range(len(chain)):
            mass=0
            for j in range(i,len(chain)):
                if heights[chain[j]]>2:break
                mass+=len(chain[j])
                boundary=(len(chain[i-1]) if i else 0)+(len(chain[j+1]) if j+1<len(chain) else 0)
                tab[mass,boundary]=tab.get((mass,boundary),0)+w
    require(total==actual[n],('canonical full count',n,total,actual[n]))
    run_tables[n]=tab
    path_rows.append({'n':n,'actual_avoidance_count':actual[n],'canonical_chain_count':chain_count,'restricted_LIS2_count':b[n]})
run_checks=0
for n,tab in run_tables.items():
    for m in range(1,n+1):
        for delta in [Fraction(0),Fraction(1,4),Fraction(1,2),Fraction(1),Fraction(2),Fraction(8)]:
            cap=int(delta*m)
            left=sum(v for (mass,boundary),v in tab.items() if mass==m and boundary<=cap)
            right=(n-m+1)*actual[n-m]*b[m]*comb(2*m+cap+1,cap)
            require(left<=right,('two-boundary count',n,m,str(delta),left,right));run_checks+=1
# A finite exact rational check on the H2 positive operator majorant at t=3/2,z=1/9.
t=Fraction(3,2);z=Fraction(1,9)
require(t==1+2*z*t*t,('Catalan choice',t,z))
for a in range(1,41):
    lhs=sum(Fraction(2**(c-1)*comb(a+c,c))*(z*t)**c for c in range(1,81))
    require(lhs<=(t/Fraction(2))*t**a,('H2 majorant',a))
files=['LOW_CHAIN_RUN_THEOREM.md','HEIGHT_THREE_SIZE_WEIGHT_BARRIER.md',Path(__file__).name]
result={'status':'passed','scope':'Finite exact regressions only; no radius or asymptotic inference',
        'state_size_max':N,'row_shuffle_total_size_max':9,'dense_family_total_size_max':10,
        'state_rows':state_rows,'path_rows':path_rows,'exact_general_row_checks':row_checks,
        'dense_edge_checks':family_checks,'height3_series_coefficient_checks':series_checks,
        'marked_run_bound_checks':run_checks,'kernel_pairs_evaluated':kernel.cache_info().currsize,
        'pins':{f:{'sha256':hashlib.sha256((P/f).read_bytes()).hexdigest(),'bytes':(P/f).stat().st_size} for f in files}}
out=P/(sys.argv[1] if len(sys.argv)>1 else 'CHECK_NORMAL.json')
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
