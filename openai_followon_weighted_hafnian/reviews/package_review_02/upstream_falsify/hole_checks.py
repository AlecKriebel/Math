"""Independent exact deletion and threshold-capacity tests for family 113.
Uses generic weighted graph recursion, not source partition formulas, for the LHS.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json,hashlib,datetime,random
OUT=Path(__file__).parent
n=4;p=4
lam=dict(zip(combinations(range(n),2),map(F,['4','1/7','2','3','1/3','1'])))
def bottleneck(N,edges):
    out={(i,j):F(1) for i in range(N) for j in range(i+1,N)}
    parts=[{i} for i in range(N)];owners=list(range(N))
    for (a,b),w in sorted(edges.items(),key=lambda ew:ew[1],reverse=True):
        x,y=owners[a],owners[b]
        if x==y:continue
        if w>1:
            for u in parts[x]:
                for v in parts[y]:out[tuple(sorted((u,v)))]=w
        for v in parts[y]:owners[v]=x
        parts[x]|=parts[y];parts[y]=set()
    return out
B=bottleneck(n,lam);H={i:max(B[tuple(sorted((i,j)))] for j in range(n) if j!=i) for i in range(n)}
N=n;paths={};edges={};C0=F(1);home={};strength={}
for (u,v),w in lam.items():
    xs=[u]+list(range(N,N+4*p))+[v];N+=4*p
    ts=[None]*(4*p+2)
    for r in range(1,p+1):
        ts[2*r-1]=ts[2*r]=max(B[u,v],H[u]*F(1,2**(r-1)))
        ts[4*p+3-2*r]=ts[4*p+2-2*r]=max(B[u,v],H[v]*F(1,2**(r-1)))
    ts[2*p+1]=w
    for j in range(1,4*p+2):edges[tuple(sorted((xs[j-1],xs[j])))]=ts[j]
    for j in range(2,4*p+2,2):C0*=ts[j]
    for j in range(1,4*p+1):home[xs[j]]=u if j<=2*p else v;strength[xs[j]]=ts[j] if j<=2*p else ts[j+1]
    paths[u,v]=(xs,ts)
Bp=bottleneck(N,edges)
def graph_counter(N,ed):
    adj=[[] for _ in range(N)]
    for (u,v),w in ed.items():adj[u].append((v,w));adj[v].append((u,w))
    @lru_cache(maxsize=20000)
    def Z(mask):
        if not mask:return F(1)
        vertices=[i for i in range(N) if (mask>>i)&1]
        if len(vertices)%2:return F(0)
        u=min(vertices,key=lambda i:sum((mask>>j)&1 for j,w in adj[i]))
        return sum((w*Z(mask^(1<<u)^(1<<v)) for v,w in adj[u] if (mask>>v)&1),F(0))
    return Z
realZ=graph_counter(N,edges);logicalZ=graph_counter(n,lam)
assert realZ((1<<N)-1)==C0*logicalZ((1<<n)-1)
def capacity(U,b):
    U=tuple(sorted(U))
    @lru_cache(None)
    def go(T):
        if not T:return F(1)
        u=T[0];return max(b[tuple(sorted((u,v)))]*go(tuple(x for x in T[1:] if x!=v)) for v in T[1:])
    return go(U)
def predicted(U):
    U=set(U);R=set(U&set(range(n)));factor=F(1);forbidden=set()
    for e,(xs,ts) in paths.items():
        hs=[j for j in range(1,4*p+1) if xs[j] in U]
        if not hs:continue
        forbidden.add(e)
        if any((j-k)%2==0 for j,k in zip(hs,hs[1:])):return None
        cons=[]
        if hs[0]%2==0:cons.append((hs.pop(0),e[0]))
        if hs and hs[-1]%2==1:cons.append((hs.pop(),e[1]))
        for j,terminal in cons:
            if terminal in R:return None
            R.add(terminal)
            if terminal!=home[xs[j]]:factor*=lam[e]/strength[xs[j]]
        assert len(hs)%2==0
        for j,k in zip(hs[::2],hs[1::2]):
            assert j%2==1 and k%2==0
            if k<=2*p:factor/=strength[xs[j]]
            elif j>=2*p+1:factor/=strength[xs[k]]
            else:factor*=lam[e]/(strength[xs[j]]*strength[xs[k]])
    return R,factor,forbidden
rng=random.Random(11320261007);tests={frozenset()}
for r in (2,4,6,8):
    for _ in range(200):tests.add(frozenset(rng.sample(range(N),r)))
for xs,ts in paths.values():
    picks=[1,2,3,2*p-1,2*p,2*p+1,2*p+2,4*p-1,4*p]
    for r in (2,4):
        for inds in combinations(picks,r):tests.add(frozenset(xs[j] for j in inds))
for r in (2,4):
    for U in combinations(range(n),r):tests.add(frozenset(U))
feasible=0;infeasible=0
for U in sorted(tests,key=lambda s:(len(s),tuple(sorted(s)))):
    mask=((1<<N)-1)^sum(1<<i for i in U);z=realZ(mask);ans=predicted(U)
    if ans is None:assert z==0;infeasible+=1;continue
    R,factor,forbidden=ans
    e={uv:w for uv,w in lam.items() if uv not in forbidden}
    c=graph_counter(n,e);zl=c(((1<<n)-1)^sum(1<<i for i in R))
    assert z==C0*factor*zl,(U,z,C0*factor*zl)
    if z:
        feasible+=1
        assert len(R)%2==0 and len(R)<=len(U)
        assert factor*capacity(U,Bp)<=capacity(R,B)
    else:infeasible+=1
# Finite set-theoretic check of the ANOVA residual charging for all subsets.
slots=list(range(9));tier={i:2-i//3 for i in slots};allowed=[(x,y) for x in slots for y in slots if tier[x]==tier[y]+1]
charges={}
for x,y in allowed:
    for mask in range(1<<9):
        S={i for i in slots if (mask>>i)&1}
        if {x,y}<=S and S<=set(range(x))|{x,y}:
            assert mask not in charges;charges[mask]=(x,y)
            assert sorted(S)[-2:]==[x,y]
result={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','scope':'generic exact weighted real-graph counts vs deletion formula; rational threshold pairing charge; all subset residual assignments for 3 tiers x 3 replicas','logical_vertices':n,'enlarged_vertices':N,'path_p':p,'hole_sets':len(tests),'feasible_hole_sets':feasible,'infeasible_hole_sets':infeasible,'unique_ANOVA_charged_components':len(charges),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/'hole_check_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
