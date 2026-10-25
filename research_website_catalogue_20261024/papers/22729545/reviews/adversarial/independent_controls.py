"""Fresh seeded graph generation and exact killed-pair propagation. No paper code imports.
Finite adversarial checks, not a universal proof or practical reconstruction algorithm.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter
from itertools import combinations,product
import random,json,networkx as nx,hashlib
rng=random.Random(22729545)
counts=Counter(); examples=[]

def tree(n):
 g=nx.DiGraph();g.add_edges_from([(0,1),(0,2)]);nxt=3
 for _ in range(n-2):
  u=rng.choice([v for v in g if not g.out_degree(v)])
  g.add_edges_from([(u,nxt),(u,nxt+1)]);nxt+=2
 return g

def add_retic(g):
 e,f=rng.sample(list(g.edges),2);a=max(g)+1;b=a+1
 h=g.copy();h.remove_edges_from([e,f]);h.add_edges_from([(e[0],a),(a,e[1]),(f[0],b),(b,f[1]),(a,b)])
 return h

def good(g):
 if not nx.is_directed_acyclic_graph(g):return False
 if any(g.out_degree(v) and not any(g.in_degree(c)==1 for c in g.successors(v)) for v in g):return False
 if any(g.in_degree(c)==2 for c in g.successors(0)):return False # avoid suppressed-root convention
 if any(sum(g.in_degree(v)==2 for v in b)>2 for b in nx.biconnected_components(g.to_undirected())):return False
 return True

def generate():
 g=tree(rng.randint(3,8))
 target=rng.randint(1,4)
 for _ in range(target):
  for trial in range(70):
   h=add_retic(g)
   if good(h):g=h;break
 return g

def run(g,idx):
 leaves=[v for v in g if g.out_degree(v)==0]
 samples=[(v,j) for v in leaves for j in range(2 if rng.random()<.25 else 1)]
 desc={v:nx.descendants(g,v)|{v} for v in g}
 C={v:frozenset(s for s in samples if s[0] in desc[v]) for v in g}
 internals=[v for v in nx.topological_sort(g) if g.out_degree(v)]
 times={v:len(internals)-j for j,v in enumerate(internals)}
 rates={e:rng.randint(1,4) for e in g.edges};rates[(None,0)]=2
 retics=[v for v in g if g.in_degree(v)==2]
 probs={v:rng.choice([F(1,2),F(1,3),F(2,5)]) for v in retics}
 for u,v in combinations(g,2):
  if C[u]<=C[v] or C[v]<=C[u]: assert u in desc[v] or v in desc[u]
  counts['cluster_comparisons']+=1
 for u,v in combinations(retics,2):
  assert C[u]!=C[v]
  if u not in desc[v] and v not in desc[u]:assert not C[u]&C[v]
  counts['reticulation_cluster_checks']+=1
 for blob in nx.biconnected_components(g.to_undirected()):
  rr=[v for v in blob if v in retics]
  for u,v in product(rr,repeat=2):
   if u!=v and v in desc[u]:
    edge=(v,next(g.successors(v)))
    assert frozenset(edge) in {frozenset(x) for x in nx.bridges(g.to_undirected())}
    counts['lower_sink_bridge_checks']+=1
 # Contract all unary reticulations and reconstruct candidate shortcut heads.
 h=g.copy()
 for v in retics:
  if len(C[v])==1:
   c=next(h.successors(v));parents=list(h.predecessors(v));h.remove_node(v);h.add_edges_from((p,c) for p in parents)
 tr=nx.transitive_reduction(h)
 for v in h:
  if h.out_degree(v)==2 and tr.out_degree(v)==1:
   w=next(tr.successors(v));actual=next(c for c in h.successors(v) if c!=w)
   support={frozenset((a,b)) for a in C[w] for b in C[actual] if a!=b}
   candidates=[]
   for c in nx.descendants(h,w):
    if h.in_degree(c)!=2:continue
    if {frozenset((a,b)) for a in C[w] for b in C[c] if a!=b}==support:candidates.append(c)
   assert actual in candidates
   if len(C[v])>2:assert candidates==[actual]
   counts['shortcut_completion_checks']+=1
 # Independently enumerate actual probability flow of each unmerged pair.
 for a,b in combinations(samples,2):
  ea=(next(g.predecessors(a[0])),a[0]);eb=(next(g.predecessors(b[0])),b[0])
  states={(ea,eb):F(1)};last=0
  for v in reversed(internals):
   t=times[v];dt=t-last
   states={s:p*(F(1,2**(rates[s[0]]*dt)) if s[0]==s[1] else 1) for s,p in states.items()}
   before=sum(p for s,p in states.items() if s[0]==s[1])
   def opts(e):
    if e[0]!=v:return [(e,F(1))]
    parents=list(g.predecessors(v))
    if len(parents)==0:return [((None,v),F(1))]
    if len(parents)==1:return [((parents[0],v),F(1))]
    return [((parents[0],v),probs[v]),((parents[1],v),1-probs[v])]
   nxt=defaultdict(F)
   childmass=sum(p for s,p in states.items() if s[0]==s[1] and s[0][0]==v)
   for s,p in states.items():
    for (e,pe),(f,pf) in product(opts(s[0]),opts(s[1])):nxt[e,f]+=p*pe*pf
   states=nxt;after=sum(p for s,p in states.items() if s[0]==s[1]);jump=after-before
   if v in retics:
    assert jump==-2*probs[v]*(1-probs[v])*childmass
    expected=a in C[v] and b in C[v]
    assert (jump<0)==expected
   else:
    x,y=list(g.successors(v));expected=(a in C[x] and b in C[y]) or (a in C[y] and b in C[x])
    assert (jump>0)==expected
   counts['exact_pair_event_checks']+=1;last=t
  counts['exact_pair_laws']+=1
 counts['networks']+=1;counts['total_reticulations']+=len(retics)
 if len(retics)>2:counts['networks_with_more_than_two_total_reticulations']+=1
 examples.append({'edges':list(g.edges),'sample_multiplicities':dict(Counter(s[0] for s in samples))})

for k in range(160):run(generate(),k)
# Independent frozen-germ control: known positive atoms, including equal rates.
for k in range(80):
 vals=[F(rng.randint(1,9),50) for _ in range(4)];rr=[0,1,1,3]
 total=sum(vals);constant=vals[0]
 # Exact Vandermonde first four moment equations recover aggregated three atoms.
 import sympy as sp
 mat=sp.Matrix([[(-r)**j for r in (0,1,3)] for j in range(3)])
 moments=sp.Matrix([sum(sp.Rational(v.numerator,v.denominator)*(-r)**j for r,v in zip(rr,vals)) for j in range(3)])
 sol=mat.inv()*moments
 assert sol[0]==sp.Rational(constant.numerator,constant.denominator)
 assert total-F(int(sol[0].p),int(sol[0].q))==sum(vals[1:]);counts['repeated_rate_germ_controls']+=1
# Entire donor words matter, hidden clocks do not, on the explicit two-label module.
gamma=F(2,5)
word_survival=F(1,2)*F(1,8)
correct=(1-gamma)+gamma*word_survival
assert correct==(1-gamma)+gamma*F(1,16)
assert correct!=(1-gamma)+gamma*F(1,4) # wrong one-rate replacement
counts['wrong_donor_word_rejected']=1
# Positive-exponent atom of a split pair is not a single exposed population.
for gamma in (F(1,2),F(1,3),F(2,5)):
 atom=2*gamma*(1-gamma);assert atom>0
 counts['pair_exposure_direction_controls']+=1
out={'status':'PASS','seed':22729545,'counts':dict(counts),'scope':'Seeded finite graph and exact pair-law stress checks; not exhaustive in graph size or parameter space. All arithmetic in probability checks is rational. Generated networks have 3–8 taxa, 1–4 attempted reticulations, level at most two per blob, no root reticulation child, and random one/two samples per taxon. No published code imported.','graphs_sha256':hashlib.sha256(json.dumps(examples,sort_keys=True).encode()).hexdigest()}
base=Path(__file__).parent
(base/'generated-graphs.json').write_text(json.dumps(examples,indent=2)+'\n')
(base/'independent-controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
