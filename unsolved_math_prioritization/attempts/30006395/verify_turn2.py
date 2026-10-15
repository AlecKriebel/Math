"""Exact checks of Cayley path/prefix conditioning and the explicit test constant.
Enumerates actual labelled trees via independent Prüfer decoding.
"""
from itertools import product
from fractions import Fraction as F
from collections import Counter,defaultdict,deque
from math import factorial,comb,prod
import json
counts=Counter()
def ck(x,kind):
    assert x,kind
    counts[kind]+=1
def falling(n,j):return prod(range(n-j+1,n+1))
def decode(k,word):
    degree=[1]*k
    for x in word:degree[x]+=1
    adj=[[] for _ in range(k)]
    for x in word:
        leaf=next(v for v in range(k) if degree[v]==1)
        adj[x].append(leaf);adj[leaf].append(x);degree[x]-=1;degree[leaf]-=1
    u,v=[x for x in range(k) if degree[x]==1]
    adj[u].append(v);adj[v].append(u)
    return adj

def path01(adj):
    parent={0:None};todo=deque([0])
    while todo:
        x=todo.popleft()
        if x==1:break
        for y in adj[x]:
            if y not in parent:parent[y]=x;todo.append(y)
    seq=[];x=1
    while x is not None:seq.append(x);x=parent[x]
    return list(reversed(seq))
def binmass(m,j,p):
    if j<0 or j>m:return F(0)
    return comb(m,j)*p**j*(1-p)**(m-j)
alltrees=0;prefixes=0
for k in range(2,8):
    histD=Counter();histB=defaultdict(Counter)
    for word in product(range(k),repeat=k-2):
        adj=decode(k,word);path=path01(adj);d=len(path)-1;histD[d]+=1;alltrees+=1
        for size in range(1,d+1):
            S=set(path[:size])
            boundary=sum(y not in S for x in S for y in adj[x])
            ck(boundary==sum(len(adj[x]) for x in S)-2*(size-1),'prefix_tree_degree_identity')
            histB[d,size][boundary]+=1;prefixes+=1
    total=k**(k-2)
    ck(sum(histD.values())==total,'cayley_total')
    for d,count in histD.items():
        ck(F(count,total)==F(falling(k-2,d-1)*(d+1),k**d),'exact_two_vertex_distance_law')
        for size in range(1,d+1):
            hist=histB[d,size]
            ck(sum(hist.values())==count,'prefix_conditional_normalization')
            if d==k-1:
                ck(hist==Counter({1:count}),'hamilton_path_exception')
                continue
            m=k-d-2;q=F(size,d+1);r=F(size,k)
            for b in range(0,k+1):
                expected=(1-q)*binmass(m,b-1,r)+q*binmass(m,b-2,r)
                ck(F(hist[b],count)==expected,'exact_prefix_boundary_distribution')
    for ell in range(1,k):
        ck(F(sum(v for d,v in histD.items() if d<=ell),total)<=F(ell*(ell+3),2*k),'short_distance_bound')
# Exact logarithmic intervals using the convergent atanh series.
def loginterval(x,m=8):
    assert x>1
    u=(x-1)/(x+1)
    low=2*sum((u**(2*j+1)/F(2*j+1) for j in range(m)),F(0))
    tail=2*u**(2*m+1)/((2*m+1)*(1-u*u))
    return low,low+tail

def ginterval(c):
    l1,u1=loginterval(1+1/c);l2,u2=loginterval(c)
    return (c+1)*l1-1-u2,(c+1)*u1-1-l2
lo=ginterval(F(4,3));hi=ginterval(F(7,5))
ck(lo[0]>0,'criterion_positive_at_four_thirds')
ck(hi[1]<0,'criterion_negative_at_seven_fifths')
c=F(4,3);delta=F(1,100);K=100;y=c+1-delta
l1,u1=loginterval(y/c);l2,u2=loginterval(c)
gap=(y*l1-y+c-u2,y*u1-y+c-l2)
ck(K*gap[0]>1,'explicit_test_length_constant')
ck(y>c and 0<delta<min(F(1),c)/2,'explicit_test_threshold')
# Probability-channel formula is exact for null and non-template edges.
for n in range(3,51):
    for i in range(1,n-1):
        p1=F(i,n);p2=F(i+1,n);r=(p2-p1)/(1-p1)
        ck(0<r<=1,'monotone_channel_valid_probability')
        ck(p1+(1-p1)*r==p2,'monotone_channel_null_edge')
        ck(1+(1-1)*r==1,'monotone_channel_forced_edge')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'labelled_trees_enumerated':alltrees,'actual_path_prefixes_enumerated':prefixes,'g_four_thirds_interval':[str(x) for x in lo],'g_seven_fifths_interval':[str(x) for x in hi],'explicit_c_four_thirds_delta_one_hundredth_gap_interval':[str(x) for x in gap],'explicit_K':K,'scope':'Exact finite Cayley-tree conditioning and rational test-constant/channel controls. The asymptotic detection proof is in TURN_2.md; no polynomial-time or sharp-transition claim.'},indent=2,sort_keys=True))
