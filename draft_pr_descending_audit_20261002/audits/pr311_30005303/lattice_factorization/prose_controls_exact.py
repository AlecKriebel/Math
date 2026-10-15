#!/usr/bin/env python3
"""Independent prose-stage controls; reads no candidate code or outputs.

The flow implementation uses antisymmetric net flows and exact base-2 weights.
This differs from the candidate's nonnegative directed-flow notation.
"""
from itertools import product, combinations
from collections import defaultdict, deque
from fractions import Fraction
from pathlib import Path
import json, random


def states(n): return list(product((0,1), repeat=n))
def pow2(k): return Fraction(2**k) if k>=0 else Fraction(1,2**(-k))
def proj(x,A): return tuple(x[i] for i in A)

def sep(n,edges,A,B,C):
    seen=set(A); q=list(A)
    while q:
        v=q.pop()
        for u,w in edges:
            z=w if u==v else u if w==v else None
            if z is not None and z not in C and z not in seen:
                seen.add(z); q.append(z)
    return not bool(seen & set(B))

def mtp(weights):
    checks=0
    for x,y in product(weights,repeat=2):
        lo=tuple(min(a,b) for a,b in zip(x,y)); hi=tuple(max(a,b) for a,b in zip(x,y))
        assert weights[lo]*weights[hi]>=weights[x]*weights[y], (x,y)
        checks+=1
    return checks

def markov(n,edges,weights):
    count=minor_count=0
    for lab in product(range(4),repeat=n):
        A=tuple(i for i,t in enumerate(lab) if t==1)
        B=tuple(i for i,t in enumerate(lab) if t==2)
        C=tuple(i for i,t in enumerate(lab) if t==3)
        if not A or not B or not sep(n,edges,A,B,C): continue
        count+=1; tabs=defaultdict(lambda:defaultdict(Fraction))
        for x,w in weights.items(): tabs[proj(x,C)][proj(x,A),proj(x,B)]+=w
        for tab in tabs.values():
            aa=sorted({a for a,b in tab}); bb=sorted({b for a,b in tab})
            for a0,a1,b0,b1 in product(aa,aa,bb,bb):
                assert tab[a0,b0]*tab[a1,b1]==tab[a0,b1]*tab[a1,b0]
                minor_count+=1
    return count,minor_count

def local_support(n,edges,weights):
    S=[x for x,w in weights.items() if w>0]
    unaries=[{x[i] for x in S} for i in range(n)]
    pairs={e:{(x[e[0]],x[e[1]]) for x in S} for e in edges}
    reconstructed={x for x in weights if all(x[i] in unaries[i] for i in range(n)) and all((x[i],x[j]) in pairs[(i,j)] for i,j in edges)}
    assert reconstructed==set(S)
    return len(S)

# Prose C4 independently reconstructed, not copied from candidate checker.
edges4=((0,1),(1,2),(2,3),(3,0))
w4={x:(2 if x==(1,)*4 else 1) if x[0]==x[1] else 0 for x in states(4)}
c4_mtp=mtp(w4); c4_sep,c4_ci=markov(4,edges4,w4)
c4_even=c4_odd=1
for a,b,c in product((0,1),repeat=3):
    if (a+b+c)%2: c4_odd*=w4[(a,a,b,c)]
    else: c4_even*=w4[(a,a,b,c)]
assert c4_even==1 and c4_odd==2
assert local_support(4,edges4,w4)==8

# Negative original couplings can aggregate positively across equality classes.
agg_edges=((0,1),(0,2),(1,2),(2,3))
agg={x:pow2(-2*x[0]*x[2]+3*x[1]*x[2]+2*x[2]*x[3]) if x[0]==x[1] else Fraction(0) for x in states(4)}
agg_mtp=mtp(agg); agg_sep,agg_ci=markov(4,agg_edges,agg)
for x,w in agg.items():
    if w: assert w==pow2(x[0]*x[2]+2*x[2]*x[3])
assert local_support(4,agg_edges,agg)==8

# On a comparable-component support, an apparently negative quadratic is unary.
chain_edges=((0,1),(1,2),(0,2))
chain={x:pow2(-3*x[0]*x[2]+2*x[1]) if x[0]<=x[1]<=x[2] else Fraction(0) for x in states(3)}
chain_mtp=mtp(chain)
for x,w in chain.items():
    if w: assert w==pow2(-3*x[0]+2*x[1])
assert local_support(3,chain_edges,chain)==4

flow_cases=flow_state_checks=flow_cut_checks=0

def check_flow(n,edges,h,J,reverse=False):
    global flow_cases,flow_state_checks,flow_cut_checks
    N=n+2; s=n; t=n+1
    cap=[[0]*N for _ in range(N)]
    b=[-z for z in h]
    for (i,j),coupling in zip(edges,J):
        if reverse and (i+j)%2: i,j=j,i
        cap[i][j]+=coupling; b[i]-=coupling
    for i,z in enumerate(b):
        if z>=0: cap[i][t]+=z
        else: cap[s][i]+=-z
    net=[[0]*N for _ in range(N)]
    while True:
        parent=[None]*N; parent[s]=s; q=deque([s])
        while q and parent[t] is None:
            u=q.popleft()
            for v in range(N):
                if parent[v] is None and cap[u][v]-net[u][v]>0:
                    parent[v]=u; q.append(v)
        if parent[t] is None: break
        u=t; bottleneck=None
        while u!=s:
            v=parent[u]; r=cap[v][u]-net[v][u]
            bottleneck=r if bottleneck is None else min(bottleneck,r); u=v
        u=t
        while u!=s:
            v=parent[u]; net[v][u]+=bottleneck; net[u][v]-=bottleneck; u=v
    residual=[[cap[u][v]-net[u][v] for v in range(N)] for u in range(N)]
    assert all(z>=0 for row in residual for z in row)
    for i in range(n): assert sum(net[i])==0
    value=sum(net[s]); assert sum(net[t])==-value
    omega=states(n)
    energy={x:-sum(z*bit for z,bit in zip(h,x))-sum(c*x[i]*x[j] for (i,j),c in zip(edges,J)) for x in omega}
    minE=min(energy.values()); kappa=sum(-z for z in b if z<0)
    assert value==minE+kappa
    weights={x:pow2(-energy[x]+minE) for x in omega}
    assert 1<=sum(weights.values())<=2**n
    for x in omega:
        cut={s}|{i for i,bit in enumerate(x) if bit}
        C=sum(cap[u][v] for u in cut for v in range(N) if v not in cut)
        R=sum(residual[u][v] for u in cut for v in range(N) if v not in cut)
        assert C==energy[x]+kappa and R==C-value and R==energy[x]-minE
        local=Fraction(1)
        for i,bit in enumerate(x): local*=pow2(-residual[s][i] if not bit else -residual[i][t])
        for i,j in edges:
            if x[i]==1 and x[j]==0: local*=pow2(-residual[i][j])
            if x[j]==1 and x[i]==0: local*=pow2(-residual[j][i])
        assert local==weights[x]
        flow_state_checks+=1; flow_cut_checks+=1
    flow_cases+=1

# Exhaustive n=3 graph / integer parameter grid, plus zero-size and isolated cases.
for n in (0,1,2,3):
    all_edges=list(combinations(range(n),2))
    for present in product((0,1),repeat=len(all_edges)):
        edges=tuple(e for e,p in zip(all_edges,present) if p)
        for J in product((0,1,2),repeat=len(edges)):
            for h in product((-2,0,2),repeat=n): check_flow(n,edges,h,J)

# Deterministic larger graphs with mixed orientations and large fields/couplings.
rng=random.Random(30005303)
for n in (4,5,6):
    for _ in range(100):
        edges=tuple(e for e in combinations(range(n),2) if rng.randrange(2))
        h=tuple(rng.randrange(-9,10) for _ in range(n))
        J=tuple(rng.randrange(7) for _ in edges)
        check_flow(n,edges,h,J,reverse=True)

result={
    'c4_mtp2_pairs':c4_mtp,'c4_ordered_global_separations':c4_sep,
    'c4_exact_ci_minors':c4_ci,'c4_even_weight_product':c4_even,'c4_odd_weight_product':c4_odd,
    'equality_aggregation_mtp2_pairs':agg_mtp,'equality_aggregation_global_separations':agg_sep,
    'equality_aggregation_exact_ci_minors':agg_ci,
    'comparable_chain_mtp2_pairs':chain_mtp,
    'exact_independent_flow_cases':flow_cases,'exact_energy_cut_factor_states':flow_state_checks,
    'exact_cut_checks':flow_cut_checks,'normalization_bounds':'1 <= Z <= 2^n in every exact case',
    'candidate_code_or_output_read':False,'all_assertions_passed':True
}
Path(__file__).with_name('prose_controls_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
