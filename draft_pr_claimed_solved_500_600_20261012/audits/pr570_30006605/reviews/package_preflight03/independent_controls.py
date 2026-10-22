#!/usr/bin/env python3
"""Fresh exact controls: threshold/search and actual repaired source recursion.
Brute structural preprocessing is deliberately not the fast BDH algorithm.
"""
from collections import deque,Counter
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
import hashlib,json,random
rng=random.Random(5703000660503)
stats=Counter(); events=Counter(); witnesses={}
def distance(adj):
 out=[]
 for x in range(len(adj)):
  ds=[999]*len(adj);ds[x]=0;q=deque([x])
  while q:
   u=q.popleft()
   for v in adj[u]:
    if ds[v]==999:ds[v]=ds[u]+1;q.append(v)
  out.append(ds)
 return out
def median(d):
 n=len(d)
 if max(d[0])==999:return False
 return all(sum(d[x][m]+d[m][y]==d[x][y] and d[y][m]+d[m][z]==d[y][z] and d[z][m]+d[m][x]==d[z][x] for m in range(n))==1 for x,y,z in combinations(range(n),3))
def radii(d,w): return [max(w[u]*d[x][u] for u in range(len(w))) for x in range(len(w))]
def budgets(w,R,D): return [max(k for k in range(D+1) if k*t<=R) for t in w]
def run_search(d,w):
 n=len(w);D=n-1;rs=radii(d,w);rho=min(rs);centers=[x for x,r in enumerate(rs) if r==rho]
 B=D*max(w);wit=0
 if not B:return B,list(range(n))
 rows=[list(range(n)) for _ in w]
 while any(rows):
  M=sum(map(len,rows)); middle=sorted((w[u]*a[(len(a)-1)//2],len(a)) for u,a in enumerate(rows) if a)
  cum=0
  for q,L in middle:
   cum+=L
   if 2*cum>=M:break
  assert 2*sum(L for t,L in middle if t<=q)>=M and 2*sum(L for t,L in middle if t>=q)>=M
  b=budgets(w,q,D);a=[D-t for t in b];feas=[x for x in range(n) if max(d[x][u]+a[u] for u in range(n))<=D]
  assert feas==[x for x in range(n) if rs[x]<=q]
  if feas:
   if q<B:B=q;wit=feas[0]
   rows=[[k for k in row if w[u]*k<q] for u,row in enumerate(rows)];events['feasible_pivots']+=1
  else:
   rows=[[k for k in row if w[u]*k>q] for u,row in enumerate(rows)];events['infeasible_pivots']+=1
  assert 4*sum(map(len,rows))<=3*M
  assert rs[wit]<=B and (B==rho or any(w[u]*k==rho for u,row in enumerate(rows) for k in row))
  stats['search_pivots']+=1
 assert B==rho and rs[wit]==rho
 assert [x for x in range(n) if rs[x]<=B]==centers
 return B,centers

def bridge_profiles(adj,profiles,label):
 d=distance(adj);n=len(adj);D=n-1
 for w in profiles:
  w=list(map(F,w));rs=radii(d,w)
  qs=sorted(set(k*t for k in range(n) for t in w));thresholds=sorted(set([F(0)]+qs+[q+F(1,97) for q in qs]+[q-F(1,97) for q in qs if q>=F(1,97)]))
  for R in thresholds:
   b=budgets(w,R,D);a=[D-t for t in b]
   actual=[max(d[x][u]+a[u] for u in range(n))<=D for x in range(n)]
   assert actual==[r<=R for r in rs]
   stats['threshold_vectors']+=1
  B,C=run_search(d,w);stats['profiles']+=1
  if label in ('singleton','square_tie','zero','single_support','cube','nonmedian_triangle') and label not in witnesses:
   witnesses[label]={'n':n,'weights':list(map(str,w)),'rho':str(B),'centers':C}

# Brute Theta/gate implementation and actual recursion, independent of packaged code.
def source_control(adj,labels,label):
 d=distance(adj);n=len(adj)
 def gate(x,S):
  valid=[p for p in S if all(d[x][p]+d[p][y]==d[x][y] for y in S)]
  assert len(valid)==1
  return valid[0]
 def truth(S,w):return {x:max(d[x][y]+w[y] for y in S) for x in S}
 def recur(S,w,depth=0):
  S=frozenset(S);s=len(S);stats['source_recursive_calls']+=1;events['source_max_depth']=max(events['source_max_depth'],depth)
  if s<=2:events['source_base']+=1;return truth(S,w)
  f=2*(s-1).bit_length();cuts={}
  for x in sorted(S):
   for y in sorted(adj[x]&S):
    if x<y:
     A=frozenset(v for v in S if d[v][x]<d[v][y]);B=S-A
     pair=tuple(sorted((tuple(sorted(A)),tuple(sorted(B)))))
     cuts[pair]=(frozenset(pair[0]),frozenset(pair[1]))
  assert cuts
  balanced=[(A,B) for A,B in cuts.values() if f*min(len(A),len(B))>=s]
  if balanced:
   events['source_balanced']+=1;A,B=balanced[0];assert len(A)+len(B)==s and f*max(len(A),len(B))<=s*(f-1)
   ea=recur(A,w,depth+1);eb=recur(B,w,depth+1);out={}
   for x in A:
    g=gate(x,B);out[x]=max(ea[x],d[x][g]+eb[g])
   for x in B:
    g=gate(x,A);out[x]=max(eb[x],d[x][g]+ea[g])
  else:
   events['source_unbalanced']+=1
   minorities=[A if len(A)<len(B) else B for A,B in cuts.values()]
   roots=S-frozenset.union(*minorities);assert len(roots)==1;v=next(iter(roots))
   e0=max(d[v][x]+w[x] for x in S)
   z=v if w[v]==e0 else min(x for x in S if d[v][x]+w[x]==e0)
   if z==v:
    events['source_root_farthest']+=1;out={x:d[x][v]+w[v] for x in S}
   else:
    ladder=[M for M in minorities if z in M and adj[v]&M];assert ladder
    assert (1<<len(ladder))<=s
    remaining=S;slices=[]
    for M in ladder:
     T=remaining&M;assert T
     rest=remaining-T;assert v in rest
     star={x:w[x] for x in T}
     fibers={x:[] for x in T}
     for y in rest:
      g=gate(y,T);fibers[g].append(y)
     for p,ys in fibers.items():
      if ys:star[p]=max(d[p][y]+w[y] for y in ys)
     assert f*len(T)<s
     slices.append((remaining,T,rest,star));remaining=rest
    volume=2*sum(len(T) for _,T,_,_ in slices);assert volume<=s
    events['source_slice_calls']+=2*len(slices);events['source_multi_ladder']+=len(ladder)>1
    out={x:d[x][v]+e0 for x in remaining}
    for x in remaining:assert d[x][v]+d[v][z]==d[x][z]
    later={}
    for current,T,rest,star in reversed(slices):
     ordinary=recur(T,w,depth+1);changed=recur(T,star,depth+1)
     for x in later:
      g=gate(x,T);later[x]=max(later[x],d[x][g]+ordinary[g])
     for x in T:
      later[x]=max(ordinary[x],changed[x])
      if ordinary[x]>changed[x]:events['original_call_necessary']+=1
      if changed[x]>ordinary[x]:events['fiber_call_necessary']+=1
     assert later=={x:truth(current,w)[x] for x in later}
    out.update(later)
  assert out==truth(S,w),(label,S,w,out,truth(S,w))
  return out
 got=recur(range(n),dict(enumerate(labels)))
 assert got==truth(range(n),dict(enumerate(labels)))
 stats['source_profiles']+=1
 if label not in witnesses:witnesses[label]={'n':n,'arrival_profile_sha256':hashlib.sha256(json.dumps(labels).encode()).hexdigest(),'eccentricity_sha256':hashlib.sha256(json.dumps(got,sort_keys=True).encode()).hexdigest()}

# All labeled connected median graphs through order 5, with exact rational profiles.
graphs=[]
for n in range(1,6):
 es=list(combinations(range(n),2))
 for mask in range(1<<len(es)):
  adj=[set() for _ in range(n)]
  for i,(u,v) in enumerate(es):
   if mask>>i&1:adj[u].add(v);adj[v].add(u)
  d=distance(adj)
  if median(d):graphs.append(adj);stats['median_graphs_through5']+=1
for i,adj in enumerate(graphs):
 n=len(adj)
 ps=list(product((0,1,2),repeat=n)) if n<=4 else [[rng.choice([F(0),F(1,13),F(2,7),F(19,3)]) for _ in range(n)] for _ in range(18)]
 bridge_profiles(adj,ps,'small_graph')
 for _ in range(3):source_control(adj,[rng.randrange(13) for _ in adj],'small_source')

def cube(k): return [{x^(1<<j) for j in range(k)} for x in range(1<<k)]
def leaves(adj,v,count):
 for _ in range(count):u=len(adj);adj.append({v});adj[v].add(u)
 return adj
special=[('singleton',[set()],[[0],[F(1,3)]]),('zero',cube(2),[[0]*4]),('square_tie',cube(2),[[1]*4]),('single_support',cube(3),[[7]+[0]*7]),('cube',cube(4),[[F((u*13)%17,11) for u in range(16)]])]
for label,adj,ps in special:bridge_profiles(adj,ps,label)
# Threshold/search work on general connected graphs as well.
for label,adj in [('nonmedian_triangle',[{1,2},{0,2},{0,1}]),('nonmedian_cycle5',[{(i-1)%5,(i+1)%5} for i in range(5)])]:
 assert not median(distance(adj));bridge_profiles(adj,[[rng.choice([F(0),F(1,9),F(5,7),F(9,2)]) for _ in adj] for _ in range(30)],label)
# Unbalanced and non-tree controls force all source mechanisms.
for k in (2,3,4):
 adj=leaves(cube(k),0,128)
 for j in range(12):
  lab=[rng.randrange(7) for _ in adj]
  if j%3==0:lab[0]=len(adj)*3
  elif j%3==1:lab[(1<<k)-1]=len(adj)*3
  source_control(adj,lab,'pendant_cube'+str(k))
# Strictly necessary original/fiber slice calls.
adj=leaves([set()],0,24)
for j in range(12):
 lab=[0]*len(adj);lab[1]=8+j;source_control(adj,lab,'star_open_fiber')
# Huge rational bit-length and near-tie rows without machine-real approximation.
adj=cube(3);huge=10**120
bridge_profiles(adj,[[F(huge+i,huge-i) for i in range(8)],[F(0),F(1,huge)]+[F(1,3)]*6],'large_rational')
assert events['source_balanced'] and events['source_unbalanced'] and events['source_root_farthest'] and events['source_multi_ladder']
assert events['original_call_necessary'] and events['fiber_call_necessary'] and events['feasible_pivots'] and events['infeasible_pivots']
result={'status':'PASS','seed':5703000660503,'counts':dict(stats),'branches':dict(events),'witnesses':witnesses,'limits':'Exact finite falsification controls with brute Theta/gates; not a fast BDH implementation or an asymptotic proof.'}
Path(__file__).with_name('INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
