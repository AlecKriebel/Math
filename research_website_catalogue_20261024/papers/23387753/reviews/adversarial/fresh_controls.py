#!/usr/bin/env python3
"""Independent exact finite controls. These are not an infinite-volume proof.

Every finite rooted tree is regarded as attached at its root to an infinite ray.
Then descendant sets below its finite edges are the actual finite pasts of that
one-ended extension. No published/archived checker is imported.
"""
from collections import Counter, deque
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib, json, math

BASE=Path(__file__).resolve().parent
counts=Counter()

def demand(condition,label):
    counts[label]+=1
    if not condition: raise AssertionError(label)

def edge(a,b): return tuple(sorted((a,b)))

def prufer(seq,n):
    degree=[1]*n
    for x in seq: degree[x]+=1
    es=[]
    for x in seq:
        leaf=next(i for i in range(n) if degree[i]==1)
        es.append(edge(leaf,x));degree[leaf]-=1;degree[x]-=1
    a,b=[i for i in range(n) if degree[i]==1]
    es.append(edge(a,b))
    return es

def rooted(es,n,root):
    adj=[[] for _ in range(n)]
    for a,b in es:adj[a].append(b);adj[b].append(a)
    par={root:None};order=[root]
    for x in order:
        for y in adj[x]:
            if y not in par:par[y]=x;order.append(y)
    past={x:{x} for x in range(n)}
    for x in reversed(order[1:]):past[par[x]].update(past[x])
    sizes={edge(x,par[x]):len(past[x]) for x in order[1:]}
    return adj,par,past,sizes

def path(adj,a,b):
    par={a:None};q=deque([a])
    while b not in par:
        v=q.popleft()
        for u in adj[v]:
            if u not in par:par[u]=v;q.append(u)
    out=[b]
    while out[-1]!=a:out.append(par[out[-1]])
    return out[::-1]

for n in range(2,7):
    allpairs=list(combinations(range(n),2))
    for seq in product(range(n),repeat=n-2):
        es=prufer(seq,n);te=set(es)
        for root in range(n):
            adj,par,past,sizes=rooted(es,n,root)
            counts['rooted_tree_cases']+=1
            paths={ab:path(adj,*ab) for ab in allpairs}
            maxima={ab:max(sizes[edge(x,y)] for x,y in zip(p, p[1:])) for ab,p in paths.items() if ab not in te}
            for v in range(n):
                p=[];x=v
                while x!=root:
                    p.append(sizes[edge(x,par[x])]);x=par[x]
                demand(all(a<b for a,b in zip(p,p[1:])), 'strict_ancestor_past_growth')
            for child in range(n):
                if child==root:continue
                S=past[child];t=edge(child,par[child]);s=len(S)
                cut=[ab for ab in allpairs if (ab[0] in S)!=(ab[1] in S)]
                demand([ab for ab in cut if ab in te]==[t], 'singleton_tree_cut')
                # Complete finite graph plus one infinite ray at root has max degree n.
                union=F(1,2**s)
                for ab in cut:
                    if ab==t:continue
                    demand(t in {edge(x,y) for x,y in zip(paths[ab],paths[ab][1:])}, 'crossing_path_uses_cut_edge')
                    demand(maxima[ab]>=s, 'maximum_suppresses_every_bypass')
                    union+=F(1,2**maxima[ab])
                demand(union <= F(1+n*s,2**s), 'exact_bad_cut_union_bound')
                # HM edge midpoint finite past: s vertices and s-1 internal midpoints.
                internal=sum(a in S and b in S for a,b in es)
                demand(s+internal==2*s-1, 'HM_midpoint_count')
                demand(F(1,2**(s+internal+1))==F(1,4**s),'HM_exact_midpoint_flip_rate')
            for p in paths.values():
                ec=Counter(sizes[edge(x,y)] for x,y in zip(p,p[1:]))
                vc=Counter(len(past[v])-1 for v in p)
                demand(max(ec.values())<=2,'edge_past_size_multiplicity_on_path')
                demand(max(vc.values())<=2,'vertex_past_size_multiplicity_on_path')
                demand(sum(F(1,4**m) for m in ec.elements())<=F(2,3),'HM_dual_edge_path_expected_flips')
                demand(sum(F(1,2**(m+1)) for m in vc.elements())<=2,'HM_site_path_expected_flips')

# Exact posterior mixtures on a complete four-vertex graph. The hidden rooted
# tree has two possible shapes; all output patterns on the other edges are used.
n=4;allpairs=list(combinations(range(n),2))
trees=[[(0,1),(1,2),(2,3)],[(0,1),(0,2),(0,3)]]
rates=[]
for es in trees:
    adj,par,past,sizes=rooted(es,n,0);te=set(es)
    row={}
    for ab in allpairs:
        if ab in te:row[ab]=1-F(1,2**sizes[ab])
        else:
            p=path(adj,*ab);M=max(sizes[edge(a,b)] for a,b in zip(p,p[1:]))
            row[ab]=F(1,2**M)
    rates.append(row)
posterior_min=F(1);posterior_max=F(0)
for e in allpairs:
    others=[f for f in allpairs if f!=e]
    for bits in product((0,1),repeat=len(others)):
        weights=[]
        for prior,row in zip([F(1,3),F(2,3)],rates):
            weight=prior
            for f,bit in zip(others,bits):weight*=row[f] if bit else 1-row[f]
            weights.append(weight)
        den=sum(weights);num=sum(w*row[e] for w,row in zip(weights,rates));prob=num/den
        demand(0<prob<1,'hidden_tree_posterior_finite_energy')
        posterior_min=min(posterior_min,prob);posterior_max=max(posterior_max,prob)

# Explicit countercontrol: replacing the maximum by the minimum on the path
# would not furnish the claimed bypass bound, even on a simple four-vertex path.
adj,par,past,sizes=rooted(trees[0],4,0)
path_sizes=[sizes[edge(a,b)] for a,b in zip([0,1,2],[1,2,3])]
negative={'path_edge_pasts':path_sizes,'cut_past':3,'wrong_min_insertion_probability':str(F(1,2**min(path_sizes))),'required_upper_bound':str(F(1,2**3))}
demand(F(1,2**min(path_sizes))>F(1,2**3),'wrong_minimum_rule_rejected')

# Exact geometric-series remainder; no numerical infinite-series truncation.
for Delta in [2,4,6,10]:
    for N in [1,2,10,50]:
        finite=sum(F(1+Delta*m,2**m) for m in range(1,N))
        tail=F(1+Delta*(N+1),2**(N-1))
        demand(finite+tail==1+2*Delta,'summability_tail_identity')

# Three internally redundant diamonds joined by two forced bridge coordinates.
# Enumerate all edge thinnings at p=1/2, allowing arbitrary within-block cycles.
es=[]
for j in range(3):
    a=4*j;es.extend([(a,a+1),(a,a+2),(a+1,a+3),(a+2,a+3)])
es.extend([(3,4),(7,8)])
def connected(chosen,allowed=None):
    if allowed is not None and (0 not in allowed or 11 not in allowed):return False
    adj=[[] for _ in range(12)]
    for a,b in chosen:
        if allowed is None or (a in allowed and b in allowed):adj[a].append(b);adj[b].append(a)
    seen={0};q=[0]
    for a in q:
        for b in adj[a]:
            if b not in seen:seen.add(b);q.append(b)
    return 11 in seen
success=sum(connected([e for e,bit in zip(es,bits) if bit]) for bits in product((0,1),repeat=len(es)))
bond_probability=F(success,2**len(es))
demand(bond_probability==F(343,16384) and bond_probability<=F(1,4),'bridge_thinning_exact_enumeration')
site_success=sum(connected(es,{v for v,bit in enumerate(bits) if bit}) for bits in product((0,1),repeat=12))
site_probability=F(site_success,2**12)
demand(site_probability<=F(1,16),'distinct_cut_vertices_site_thinning')

result={'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'counts':dict(counts),'total_assertions':sum(v for k,v in counts.items() if k!='rooted_tree_cases'),
 'posterior_probability_range':[str(posterior_min),str(posterior_max)],
 'wrong_rule_control':negative,'diamond_bond_probability':str(bond_probability),
 'diamond_site_probability':str(site_probability),
 'limits':'Exact finite structural/probability controls only. No simulation or finite enumeration certifies the infinite tree input, Borel-Cantelli conclusion, mixing or quenched probability-one theorem.'}
(BASE/'fresh_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
