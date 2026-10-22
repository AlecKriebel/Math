"""Fresh rational flow/cut and extremal-cut checks; imports no candidate code."""
from fractions import Fraction as Q
from collections import deque
from pathlib import Path
import json, random, math

HERE=Path(__file__).resolve().parent
rng=random.Random(39720261021)
count={'rational_instances':0,'flow_cut_equalities':0,'right_slope_checks':0,'physical_edges':0,'cut_size_pairs':0,'small_class_counts':0}

def maxflow(d):
    k=len(d);n=2*k+2;s=2*k;t=s+1
    residual=[[Q(0) for _ in range(n)] for _ in range(n)]
    for i in range(k):
        residual[s][i]=residual[k+i][t]=Q(2*k)
        for j in range(k):residual[i][k+j]=d[i][j]
    total=Q(0)
    while True:
        parent=[None]*n;parent[s]=s;queue=deque([s])
        while queue and parent[t] is None:
            u=queue.popleft()
            for v in range(n):
                if parent[v] is None and residual[u][v]>0:
                    parent[v]=u;queue.append(v)
        if parent[t] is None:break
        path=[];v=t
        while v!=s:path.append((parent[v],v));v=parent[v]
        push=min(residual[u][v] for u,v in path)
        for u,v in path:residual[u][v]-=push;residual[v][u]+=push
        total+=push
    y=[[d[i][j]-residual[i][k+j] for j in range(k)] for i in range(k)]
    assert sum(map(sum,y))==total
    assert all(Q(0)<=y[i][j]<=d[i][j] for i in range(k) for j in range(k))
    assert all(sum(row)<=2*k for row in y)
    assert all(sum(y[i][j] for i in range(k))<=2*k for j in range(k))
    return total,y

def lines(x):
    k=len(x);out=[]
    for aa in range(1<<k):
        A=[i for i in range(k) if aa>>i&1]
        for bb in range(1<<k):
            B=[j for j in range(k) if bb>>j&1]
            m=sum((x[i][j] for i in A for j in range(k) if j not in B),Q(0))
            b=Q(2*k*(k-len(A)+len(B))+len(A)*(k-len(B)))
            out.append((b,m))
    return out

def physical(y):
    k=len(y);height=k.bit_length()-1
    rows=list(map(sum,y));cols=[sum(y[i][j] for i in range(k)) for j in range(k)]
    # An edge is specified independently by a nonempty binary prefix of a leaf.
    for side in [0,1]:
        words=[str(side)+format(i,'0'+str(height)+'b') for i in range(k)]
        for depth in range(1,height+2):
            for prefix in sorted({w[:depth] for w in words}):
                I=[i for i,w in enumerate(words) if w.startswith(prefix)]
                direct=sum((y[i][j] for i in range(k) for j in range(k) if (i if side==0 else j) in I),Q(0))
                aggregate=sum((rows if side==0 else cols)[i] for i in I)
                assert direct==aggregate<=2*k*len(I)
                count['physical_edges']+=1

for k in [2,4]:
    for trial in range(18):
        x=[[Q(rng.randrange(1,81),20) for j in range(k)] for i in range(k)]
        ls=lines(x);S=sum(map(sum,x))
        for t in [Q(1),Q(3,2),Q(2),Q(5,2),Q(5)]:
            d=[[1+(t-1)*v for v in row] for row in x]
            value,y=maxflow(d);values=[b+(t-1)*m for b,m in ls]
            assert value==min(values);count['flow_cut_equalities']+=1
            active=[m for (b,m),v in zip(ls,values) if v==value]
            slope=min(active)
            assert Q(0)<=slope<=S
            gaps=[v-value for v in values if v>value]
            h=min(gaps+[Q(1)])/(2*(1+S))
            next_value,_=maxflow([[1+(t+h-1)*v for v in row] for row in x])
            assert (next_value-value)/h==slope
            count['right_slope_checks']+=1;count['rational_instances']+=1
            physical(y)
            if all(sum(row)<2*k for row in d) and all(sum(d[i][j] for i in range(k))<2*k for j in range(k)):
                assert y==d and slope==S
            if value==2*k*k:
                assert all(sum(row)==2*k for row in y)
                assert all(sum(y[i][j] for i in range(k))==2*k for j in range(k))

# Strictly positive rates with all offered terminal totals sufficient but a mixed cut failing.
d=[[Q(11,10) if j<2 else Q(4) for j in range(4)] for i in range(3)]
d.append([Q(5),Q(5),Q(11,10),Q(11,10)])
assert all(sum(row)>=8 for row in d)
assert all(sum(d[i][j] for i in range(4))>=8 for j in range(4))
mixed,_=maxflow(d);assert mixed==Q(153,5)<32
# At the uniform critical tie the right marginal is zero, the left marginal one.
uniform=lines([[Q(1)]*4 for _ in range(4)])
active=[m for b,m in uniform if b+m==32]
assert min(active)==0 and max(active)==16
# Exact offered-slope normalization differs from baseline normalization.
tworate=lines([[Q(2)]*4 for _ in range(4)])
v=min(b+Q(1,4)*m for b,m in tworate)
assert v==24 and min(m for b,m in tworate if b+Q(1,4)*m==v)==32

for k in range(1,81):
    for a in range(k+1):
        for d in range(k+1):
            assert a*d-k*(a+d-k)==(k-a)*(k-d)
            if a+d<=k:continue
            q=min(a,d);ell=k-max(a,d)
            assert 0<=ell<q and a*d==q*(k-ell)
            if q<=k//2:assert a*d>=Q(q*k,2)
            else:assert a*d>Q(k*k,4)
            count['cut_size_pairs']+=1
    for q in range(1,k//2+1):
        exact=sum(2*math.comb(k,q)*math.comb(k,ell) for ell in range(q))
        assert exact<=2*q*k**(2*q);count['small_class_counts']+=1
result={'all_assertions_passed':True,'counts':count,'mixed_cut_witness_flow':str(mixed),
        'critical_tie_right_slope':0,'critical_tie_left_slope':16,
        'normalization_witness_S':32,'normalization_witness_baseline':16,
        'scope':'Finite rational controls supplement the independent analytic proof; no asymptotic or novelty inference.'}
(HERE/'FRESH_EXACT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
