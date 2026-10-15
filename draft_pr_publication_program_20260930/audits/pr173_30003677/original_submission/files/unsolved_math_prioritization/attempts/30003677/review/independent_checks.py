#!/usr/bin/env python3
"""Independent Floyd-distance and event-list controls; no random simulations."""
from itertools import product,combinations
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
C=Counter();instances=0;witnesses=0;INF=10**8

def ck(value,category):
    assert value,category
    C[category]+=1

def floyd(n,edges,weights,allowed=None):
    if allowed is None:allowed=set(range(n))
    d=[[INF]*n for _ in range(n)]
    for a in allowed:d[a][a]=0
    for (a,b),weight in zip(edges,weights):
        if a in allowed and b in allowed:d[a][b]=d[b][a]=min(d[a][b],weight)
    for k in allowed:
        for a in allowed:
            for b in allowed:d[a][b]=min(d[a][b],d[a][k]+d[k][b])
    return d

def evolve(n,edges,slow,fast,seeds,root):
    color=[0]*n;arrive=[INF]*n;pending=[]
    def infect(v,t,c):
        color[v]=c;arrive[v]=t
        ws=slow if c==1 else fast
        for (a,b),weight in zip(edges,ws):
            if a==v:pending.append((t+weight,-c,b,c))
            if b==v:pending.append((t+weight,-c,a,c))
    for v in seeds:infect(v,0,1)
    infect(root,0,2)
    while pending:
        event=min(pending);pending.remove(event);t,_,v,c=event
        if color[v]==0:infect(v,t,c)
    return color,arrive

def test(n,edges,slow,fast):
    global instances,witnesses
    fastdist=floyd(n,edges,fast)
    for root in range(n):
        others=[x for x in range(n) if x!=root]
        for mask in range(1,1<<len(others)):
            seeds={v for i,v in enumerate(others) if mask>>i&1}
            colors,times=evolve(n,edges,slow,fast,seeds,root);instances+=1
            for v in range(n):
                if colors[v]==2:ck(fastdist[root][v]<=times[v],'actual_fast_within_unopposed_ball')
            for T in (0,1,2,3,5):
                allowed={v for v in range(n) if fastdist[root][v]>T}
                d=floyd(n,edges,slow,allowed)
                for v in allowed:
                    if any(s in allowed and d[s][v]<=T for s in seeds):
                        witnesses+=1
                        ck(colors[v]==1 and times[v]<=T,'protected_induced_subgraph_path')

base=list(combinations(range(3),2))
for mask in range(1,8):
    edges=[e for i,e in enumerate(base) if mask>>i&1];m=len(edges)
    for weights in product((0,1,2),repeat=2*m):test(3,edges,weights[:m],weights[m:])
# Parallel edges, loops and a disconnected component are included separately.
for edges in [[(0,1),(0,1),(1,2),(2,3),(3,0),(2,2)],[(0,1),(1,1),(2,3)],[(0,1),(1,2),(2,3)]]:
    m=len(edges)
    for seed in range(12):
        test(4,edges,tuple((seed+2*i)%4 for i in range(m)),tuple((2*seed+i*i)%5 for i in range(m)))

# Deterministic parity-repair identities and uniform-repair expectations.
for n in range(1,6):
    for degrees in product((2,3,5),repeat=n):
        for k in range(3,8):
            original=sum(d for d in degrees if d>=k)
            increments=[]
            for i in range(n):
                repaired=list(degrees);repaired[i]+=1
                inc=sum(d for d in repaired if d>=k)-original;increments.append(inc)
                ck(0<=inc<=degrees[i]+1,'parity_seed_mass_bound')
                ck(sum(d>=k for d in repaired)-sum(d>=k for d in degrees) in (0,1),'parity_seed_count_bound')
                ck(sum(d*d for d in repaired)-sum(d*d for d in degrees)==2*degrees[i]+1,'parity_second_moment')
            ck(F(sum(increments),n)<=F(sum(degrees),n)+1,'uniform_repair_expectation')

for j in range(2,31):
    for p in (F(1),F(1,2),F(1,7),F(1,100),F(2,5)):
        R=(j*j*p.denominator+p.numerator-1)//p.numerator
        ck(R*p>=j*j,'ray_failure_budget')
        ck((1-p)**R<=F(1,1+R*p)<=F(1,j*j),'geometric_failure_bound')
        for rate in (F(1,9),F(2,3),F(5)):
            T=F(j*j*R)/rate
            ck(F(R)/(rate*T)==F(1,j*j),'time_failure_budget')
    for mean in (4*j*j,7*j*j):
        ck(F(4,mean)<=F(1,j*j),'seed_count_probability_budget')
        ck(F(mean,2)>=j,'diverging_seed_count')
    ck(F(3,j*j)/F(1,j)==F(3,j),'uniform_vertex_to_fraction')

# Even geometric degree law from power-series identities at z=1/2.
z=F(1,2)
ck(z/(1-z)==1,'geometric_mass')
ck(2*z/(1-z)**2==4,'degree_mean')
ck(4*z*(1+z)/(1-z)**3==24,'degree_second_moment')
for j in range(1,60):
    tail=F(j+1,2**j)
    # A size-biased tail must satisfy tail_j - tail_(j+1)=P(D*=2j).
    ck(tail-F(j+2,2**(j+1))==F(j,2**(j+1)),'size_biased_tail_recurrence')
    ck(F(2*j)*F(1,2**j)/4==F(j,2**(j+1)),'size_bias_normalization')

p=Path(__file__).resolve().parent
r={'status':'PASS','assertions':sum(C.values()),'categories':dict(C),'finite_competition_instances':instances,'protected_induced_path_witnesses':witnesses,'artifact_sha256':sha256((p/'author_replay/CANDIDATE.md').read_bytes()).hexdigest(),'limits':'Exact bounded controls for deterministic protection, parity, moments and diagonal inequalities. The local weak limit, nonexplosion and deterministic diagonal schedule are audited in the written review, not established by finite computation.'}
(p/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
