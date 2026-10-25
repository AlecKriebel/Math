"""Exact independent finite controls for the published infinite proof.
Finite rooted trees are viewed as attached at root 0 to an infinite ray.
No historical author/reviewer verification code is imported.
"""
from pathlib import Path
from itertools import product,combinations
from collections import Counter,deque
from fractions import Fraction as F
import json
ROOT=Path(__file__).resolve().parent

def prufer(code,n):
 deg=[1]*n
 for v in code:deg[v]+=1
 edges=[]
 for v in code:
  u=next(i for i in range(n) if deg[i]==1)
  edges.append(tuple(sorted((u,v))));deg[u]-=1;deg[v]-=1
 u,v=[i for i in range(n) if deg[i]==1];edges.append(tuple(sorted((u,v))))
 return edges

def graph(edges,n):
 adj=[[] for _ in range(n)]
 for i,(u,v) in enumerate(edges):adj[u].append((v,i));adj[v].append((u,i))
 return adj

def root_tree(adj,root=0):
 par={root:None};order=[root]
 for u in order:
  for v,e in adj[u]:
   if v not in par:par[v]=(u,e);order.append(v)
 if len(par)!=len(adj):return None
 sides={}
 for u in reversed(order):
  below={u}
  for v,e in adj[u]:
   if par.get(v)==(u,e):below|=sides[e]
  if par[u] is not None:sides[par[u][1]]=below
 return par,sides

def path(adj,x,y):
 prev={x:None};queue=[x]
 for u in queue:
  if u==y:break
  for v,e in adj[u]:
   if v not in prev:prev[v]=(u,e);queue.append(v)
 out=[];verts=[y]
 while y!=x:
  u,e=prev[y];out.append(e);y=u;verts.append(y)
 return out,verts

counts=Counter();negative=None
for n in range(2,7):
 for code in product(range(n),repeat=n-2):
  edges=prufer(code,n);adj=graph(edges,n);par,sides=root_tree(adj);size={e:len(s) for e,s in sides.items()};counts['rooted_trees']+=1
  for v in range(1,n):
   pp,_=path(adj,v,0);values=[size[e] for e in pp]
   assert values==sorted(set(values),reverse=True) or values==sorted(set(values))
   counts['ancestor_chains']+=1
  for u,v in combinations(range(n),2):
   pp,_=path(adj,u,v);multiplicity=Counter(size[e] for e in pp)
   assert max(multiplicity.values())<=2
   counts['edge_path_multiplicity_checks']+=1
   for t,S in sides.items():
    crosses=(u in S)!=(v in S)
    assert crosses==(t in pp)
    counts['cut_path_equivalences']+=1
    if tuple(sorted((u,v))) not in edges and crosses:
     correct=F(1,2**max(size[e] for e in pp));bound=F(1,2**size[t])
     assert correct<=bound;counts['bypass_bounds']+=1
     mutant=F(1,2**min(size[e] for e in pp))
     if mutant>bound and negative is None:negative={'n':n,'tree_edges':edges,'cut_edge':edges[t],'finite_side':sorted(S),'non_tree_edge':[u,v],'path_sizes':[size[e] for e in pp],'correct_probability':str(correct),'wrong_min_probability':str(mutant),'required_bound':str(bound)}
  # Subdivide every edge, independently count monochromatic finite past at midpoints.
  sub=[]
  for i,(u,v) in enumerate(edges):sub.extend([(u,n+i),(n+i,v)])
  sa=graph(sub,2*n-1);sp,ss=root_tree(sa)
  past={0:2*n-2}
  for v in range(1,2*n-1):past[v]=len(ss[sp[v][1]])-1
  for i in range(n-1):
   assert past[n+i]==2*size[i]-1
   counts['midpoint_counts']+=1
  for u,v in combinations(range(2*n-1),2):
   _,vs=path(sa,u,v);multiplicity=Counter(past[x] for x in vs)
   assert max(multiplicity.values())<=2
   counts['subdivided_vertex_path_multiplicity_checks']+=1
assert negative

# Exact posterior conditional probabilities after mixing latent input trees.
n=3;E=list(combinations(range(n),2));trees=[prufer(code,n) for code in product(range(n),repeat=n-2)]
rates=[]
for es in trees:
 ad=graph(es,n);_,sides=root_tree(ad);sizes={e:len(s) for e,s in sides.items()};rs=[]
 for e in E:
  if e in es:rs.append(1-F(1,2**sizes[es.index(e)]))
  else:
   pp,_=path(ad,*e);rs.append(F(1,2**max(sizes[x] for x in pp)))
 rates.append(rs)
conditionals=[]
for e in range(len(E)):
 other=[j for j in range(len(E)) if j!=e]
 for bits in product((0,1),repeat=len(other)):
  weights=[]
  for rs in rates:
   w=F(1,len(rates))
   for j,b in zip(other,bits):w*=rs[j] if b else 1-rs[j]
   weights.append(w)
  q=sum(w*rs[e] for w,rs in zip(weights,rates))/sum(weights)
  assert 0<q<1
  # Compute the same conditional directly from the joint output distribution.
  joint1=joint0=F(0)
  for rs in rates:
   base=F(1,len(rates))
   for j,b in zip(other,bits):base*=rs[j] if b else 1-rs[j]
   joint1+=base*rs[e];joint0+=base*(1-rs[e])
  assert q==joint1/(joint0+joint1)
  conditionals.append(str(q))

# Finite planar dual control: enumerate every spanning tree of the 3x3 vertex grid.
# The outer face is dual root 0; internal faces have indices 1..4.
N=3;coords=list(product(range(N),repeat=2));index={v:i for i,v in enumerate(coords)}
face=lambda x,y:1+x*(N-1)+y if 0<=x<N-1 and 0<=y<N-1 else 0
GE=[];DE=[]
for x,y in coords:
 if x<N-1:GE.append((index[x,y],index[x+1,y]));DE.append((face(x,y-1),face(x,y)))
 if y<N-1:GE.append((index[x,y],index[x,y+1]));DE.append((face(x-1,y),face(x,y)))
for inds in combinations(range(len(GE)),len(coords)-1):
 es=[GE[i] for i in inds];ad=graph(es,len(coords));rooted=root_tree(ad)
 if rooted is None:continue
 counts['planar_spanning_trees']+=1;_,sides=rooted
 comp=[i for i in range(len(GE)) if i not in inds];dad=graph([DE[i] for i in comp],5)
 assert len(comp)==4 and root_tree(dad) is not None
 for j,S in sides.items():
  t=inds[j];cut={i for i,(u,v) in enumerate(GE) if (u in S)!=(v in S)}
  pp,_=path(dad,*DE[t]);cycle={t}|{comp[k] for k in pp}
  assert cut==cycle
  deg=Counter(v for i in cut for v in DE[i]);assert set(deg.values())=={2}
  counts['planar_fundamental_cycles']+=1

# Exact series identities with their analytic tails, not floating truncation.
series=[]
for delta in (2,4,6,20):
 for N in (1,2,10,40):
  prefix=sum((1+delta*m)*F(1,2**m) for m in range(1,N+1))
  tail=F(1+delta*(N+2),2**N)
  assert prefix+tail==1+2*delta
  series.append({'delta':delta,'N':N,'prefix':str(prefix),'tail':str(tail),'total':str(prefix+tail)})
assert 1+2*F(1,3)==F(5,3)
result={'all_controls_passed':True,'counts':dict(counts),'max_to_min_negative_control':negative,'latent_tree_mixture':{'conditional_cases':len(conditionals),'min_conditional':str(min(F(x) for x in conditionals)),'max_conditional':str(max(F(x) for x in conditionals)),'all_strict':True},'series_identities':series,'limitations':['Finite controls do not establish existence of an infinite stationary tree; that is an imported theorem.','No finite experiment proves Borel-Cantelli or a quenched threshold. Those steps are checked analytically.']}
(ROOT/'independent_controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'all_controls_passed':True,'counts':dict(counts),'negative_control':negative,'mixture':result['latent_tree_mixture']},indent=2))
