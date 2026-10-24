from pathlib import Path
from fractions import Fraction
from itertools import product
import gzip,json,hashlib
base=Path(__file__).resolve().parent
raw=(base/'release/square_flow_certificate.json.gz').read_bytes()
d=json.loads(gzip.decompress(raw))
radius=10
levels=[ [()] ]
for k in range(1,radius+1):
    levels.append([(first,)+tail for first in range(3) for tail in product(range(2),repeat=k-1)])
words=[w for level in levels for w in level]
idx={w:i for i,w in enumerate(words)}
assert len(words)==3070

def parent(w):
    return w+(0,) if all(a==0 for a in w) else w[:-1]

def tree_neighbors(w):
    if not w:return [(0,),(1,),(2,)]
    return [w[:-1],w+(0,),w+(1,)]

def infinity_neighbors(w):
    pr=parent(w)
    kids=[v for v in tree_neighbors(w) if v!=pr]
    grandkids=[z for v in kids for z in tree_neighbors(v) if z!=w]
    return set([pr,parent(pr)]+kids+grandkids)

adj=[set() for w in words]
for w,i in idx.items():
    for v in [parent(w),parent(parent(w))]:
        if v in idx:
            j=idx[v];adj[i].add(j);adj[j].add(i)
for w,i in idx.items():assert adj[i]=={idx[v] for v in infinity_neighbors(w) if v in idx}
squared=[]
for i,near in enumerate(adj):
    neighborhood=set(near)
    for j in near:neighborhood.update(adj[j])
    neighborhood.discard(i)
    squared.append(neighborhood)
edges=[(i,j) for i,near in enumerate(squared) for j in sorted(near) if i<j]
assert len(edges)==19931
assert edges==[tuple(e) for e in d['edge_order']]
root=set(infinity_neighbors(()))
full=set(root)
for w in root:full.update(infinity_neighbors(w))
full.discard(())
assert len(root)==8 and len(full)==40
targets=sorted(idx[v] for v in full)
assert targets==d['root_neighbors']==sorted(squared[0])
assert d['denominator']==10**9
energy=[]
for target,flow in zip(targets,d['flows']):
    assert len(flow)==len(edges)
    divergences=[0]*len(words)
    en=0
    for (u,v),current in zip(edges,flow):
        assert type(current)==int
        divergences[u]+=current;divergences[v]-=current
        en+=current*current
    assert divergences[target]==10**9
    assert divergences[0]==-10**9
    assert all(a==0 for i,a in enumerate(divergences) if i not in (0,target))
    energy.append(en)
assert len(energy)==40
assert energy==d['energy_numerators']
assert sum(energy)==3208526010913748780==d['total_energy_numerator']
assert d['total_energy_denominator']==10**18
upper=Fraction(sum(energy),10**18)
assert upper < Fraction(321,100)
assert Fraction(73,50)**2>2
lower=(24-Fraction(73,50))/7
assert lower==Fraction(161,50)
assert (lower-upper)/2>Fraction(1,200)
print(json.dumps(dict(status='PASS_INDEPENDENT_WORD_TREE_CERTIFICATE',certificate_sha256=hashlib.sha256(raw).hexdigest(),tree_vertices=len(words),square_edges=len(edges),root_degree_G=len(root),root_degree_square=len(full),exact_current_entries=sum(len(r) for r in d['flows']),exact_divergence_equations=len(words)*len(energy),square_expected_degree_upper=str(upper),bF_gap_lower=str((lower-upper)/2),notes='Independent tuple-word tree and complete finite edge enumeration; integer feasibility and energy checks only. Infinite free-boundary transfer reviewed analytically.'),indent=2))
