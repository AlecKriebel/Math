from pathlib import Path
from functools import lru_cache
from itertools import combinations,product
import json,time
START=time.time();COUNTS={}
def require(c,label):
 COUNTS[label]=COUNTS.get(label,0)+1
 if not c:raise ValueError(label)
class Graph:
 def __init__(self,n,edges):
  self.n=n;self.edges=tuple(edges);self.all=(1<<n)-1;self.adj=[0]*n;self.inc=[[] for _ in range(n)]
  for j,(a,b) in enumerate(edges):self.adj[a]|=1<<b;self.adj[b]|=1<<a;self.inc[a].append((b,j));self.inc[b].append((a,j))
 def connected(self,S):
  if not S:return False
  seen=S&-S;todo=seen
  while todo:
   b=todo&-todo;todo-=b;v=b.bit_length()-1;new=self.adj[v]&S&~seen;seen|=new;todo|=new
  return seen==S
 def two(self,S):return S.bit_count()>=3 and self.connected(S) and all(self.connected(S&~(1<<v)) for v in range(self.n) if S>>v&1)
 @lru_cache(None)
 def pm(self,S):
  if not S:return True
  if S.bit_count()%2:return False
  b=S&-S;v=b.bit_length()-1;rest=S^b;choices=self.adj[v]&rest
  while choices:
   c=choices&-choices;choices-=c
   if self.pm(rest^c):return True
  return False
 def induced_edges(self,S):return sum(1 for a,b in self.edges if S>>a&1 and S>>b&1)
 def fc_beta(self):
  best=0
  for S in range(1,1<<self.n):
   if S.bit_count()%2 and self.two(S) and all(self.pm(S&~(1<<v)) for v in range(self.n) if S>>v&1):best=max(best,self.induced_edges(S)-S.bit_count()+1)
  return best
 def direct_beta(self):
  full=(1<<len(self.edges))-1;cycles=set()
  def cy(start,v,verts,used):
   for w,j in self.inc[v]:
    bit=1<<j
    if used&bit:continue
    if w==start:
     if used.bit_count()>=1:cycles.add((used|bit,verts))
    elif w>start and not verts>>w&1:cy(start,w,verts|1<<w,used|bit)
  for v in range(self.n):cy(v,v,1<<v,0)
  @lru_cache(None)
  def ears(used,old):
   found=set()
   def path(start,v,vertices,edgepath):
    for w,j in self.inc[v]:
     b=1<<j
     if used&b or edgepath&b:continue
     if old>>w&1:
      if w!=start:found.add((edgepath|b,vertices&~old))
     elif not vertices>>w&1:path(start,w,vertices|1<<w,edgepath|b)
   for v in range(self.n):
    if old>>v&1:path(v,v,1<<v,0)
   return tuple(found)
  @lru_cache(None)
  def complete(used,old,stopped):
   if used==full:return 0
   best=-10000
   for em,vm in ears(used,old):
    odd=em.bit_count()%2==1;rest=complete(used|em,old|vm,stopped or not odd)
    if rest>=0:best=max(best,rest+(1 if not stopped and odd else 0))
   return best
  best=-10000
  for em,vm in cycles:
   odd=em.bit_count()%2==1;rest=complete(em,vm,not odd)
   if rest>=0:best=max(best,rest+int(odd))
  return best
 def bipartite(self):
  color={}
  for start in range(self.n):
   if start in color:continue
   color[start]=0;todo=[start]
   while todo:
    v=todo.pop()
    for w,j in self.inc[v]:
     if w in color:
      if color[w]==color[v]:return False
     else:color[w]=1-color[v];todo.append(w)
  return True
 def cone(self):return Graph(self.n+1,self.edges+tuple((self.n,v) for v in range(self.n)))
 def connected_pm_score(self):
  best=0;witness=0
  for S in range(1,1<<self.n):
   if S.bit_count()%2:continue
   e=self.induced_edges(S)
   if e>best and self.connected(S) and self.pm(S):best=e;witness=S
  return best,witness
report={'scope':'Direct complete-ear enumeration and exact controls supplement, rather than prove, universal reduction.'}
graph_count=0;cone_count=0
for n in range(3,6):
 pairs=list(combinations(range(n),2))
 for mask in range(1<<len(pairs)):
  g=Graph(n,[e for j,e in enumerate(pairs) if mask>>j&1])
  if not g.two(g.all):continue
  a=g.direct_beta();b=g.fc_beta();require(a==b,'direct_complete_ear_vs_induced_fc');graph_count+=1
for n in range(2,5):
 pairs=list(combinations(range(n),2))
 for mask in range(1<<len(pairs)):
  b=Graph(n,[e for j,e in enumerate(pairs) if mask>>j&1])
  if not b.connected(b.all) or not b.bipartite():continue
  score,_=b.connected_pm_score();g=b.cone();require(g.direct_beta()==score==g.fc_beta(),'cone_identity_small_bases');cone_count+=1
multi=[]
for n,e in [(3,[(0,1),(1,2),(2,0)]),(4,[(0,1),(1,2),(2,3),(3,0)]),(4,list(combinations(range(4),2)))]:
 for copies in [1,2]:
  g=Graph(n,e+[e[0]]*copies);a=g.direct_beta();b=g.fc_beta();require(a==b,'parallel_edge_conventions');multi.append({'n':n,'edges':len(g.edges),'beta':a})
report.update({'all_two_connected_simple_graphs_n3_to5':graph_count,'connected_bipartite_bases_n2_to4':cone_count,'multigraph_controls':multi})
for k in range(1,41):
 for a in range(k+1):
  for b in range(k+1):
   d=k*(a+b)-a*b;require(d-k*(a-b)==b*(2*k-a)>=0,'full_partial_block_identity')
def cover(U,sets,s):
 if s<0:return None
 for r in range(min(s,len(sets))+1):
  for J in combinations(range(len(sets)),r):
   union=set().union(*(sets[j] for j in J))
   if union==U:return J
 return None
def preprocessing(U,sets,s):
 if s<0:return False
 if not U:return True
 union=set().union(*sets) if sets else set()
 if not sets or union!=U or s==0:return False
 if s>=len(sets):return True
 return None
def construction(m,sets,k=None):
 T=sum(1+len(x) for x in sets);k=k or T+len(sets)+3;edges=[];L=[];R=[]
 for i in range(m+1):
  left=list(range(2*k*i,2*k*i+k));right=list(range(2*k*i+k,2*k*(i+1)));L.append(left);R.append(right)
  edges.extend((a,b) for a in left for b in right)
 offset=2*k*(m+1)
 for j,A in enumerate(sets):
  edges.append((offset+j,R[0][0]));edges.extend((offset+j,R[i][0]) for i in A)
 return Graph(offset+len(sets),edges),L,R,T,k,offset
def forward(m,sets,J):
 b,L,R,T,k,off=construction(m,sets);chosen=set(J)
 # Remove redundant sets to get a private-element certificate.
 for j in list(chosen):
  if set().union(*(sets[h] for h in chosen-{j}))==set(range(1,m+1)):chosen.remove(j)
 private={j:next(i for i in sets[j] if all(i not in sets[h] for h in chosen-{j})) for j in chosen}
 selected=set(range(off))|{off+j for j in chosen};matching=[]
 for j,i in private.items():selected.remove(L[i][0]);matching.append((off+j,R[i][0]))
 for i in range(m+1):
  ll=[v for v in L[i] if v in selected];rr=R[i][1:] if i in private.values() else R[i]
  matching.extend(zip(ll,rr))
 mask=sum(1<<v for v in selected);covered=[v for edge in matching for v in edge]
 require(set(covered)==selected and len(covered)==len(selected),'actual_size_forward_matching')
 require(all((b.adj[u]>>v)&1 for u,v in matching),'actual_matching_edges')
 require(b.connected(mask),'actual_size_forward_connectivity')
 expected=(m+1)*k*k-k*len(chosen)+sum(1+len(sets[j]) for j in chosen)
 require(b.induced_edges(mask)==expected,'actual_size_score')
 require(expected>0,'actual_size_positive_threshold')
 return {'m':m,'n':len(sets),'T':T,'k':k,'base_vertices':b.n,'base_edges':len(b.edges),'selected_sets':sorted(chosen),'private_elements':private,'score':expected}
pre=0;full=[]
for m in range(0,4):
 U=set(range(1,m+1));options=[set(c) for r in range(m+1) for c in combinations(U,r)]
 for n in range(0,4):
  for sets in product(options,repeat=n):
   for s in range(-1,n+2):
    expected=cover(U,sets,s);p=preprocessing(U,sets,s)
    if p is not None:require(p==(expected is not None),'preprocessing_all_small_inputs')
    else:
     T=sum(1+len(x) for x in sets);k=T+n+3;M=(m+1)*k*k;F=M-k*s
     require(k>T and k>s and k*k>k*s+T and F>0,'actual_constant_gaps')
     if expected is not None and len(full)<32:
      x=forward(m,sets,expected);require(x['score']>=F,'actual_size_forward_threshold');full.append(x)
    pre+=1
report['small_set_cover_input_budget_cases']=pre;report['full_size_forward_witnesses']=full
# Directly enumerate all subsets in the manuscript's20-vertex objective-separation example.
sets=({1},{2});b,L,R,T,k,off=construction(2,sets,3);leftmask=sum(1<<v for vv in L for v in vv)|sum(1<<(off+j) for j in range(2));rightmask=b.all^leftmask;best=0;witness=0;balanced=0
for S in range(1,1<<b.n):
 if (S&leftmask).bit_count()!=(S&rightmask).bit_count():continue
 balanced+=1;e=sum((b.adj[v]&S).bit_count() for v in range(b.n) if (S&leftmask)>>v&1)
 if e>best and b.connected(S) and b.pm(S):best=e;witness=S
require(best==25,'connected_optimum_three_K33')
blocks=(1<<off)-1;require(b.induced_edges(blocks)==27 and b.pm(blocks) and not b.connected(blocks),'disconnected_27_control')
whole=0
for chosen_blocks in range(8):
 for conns in range(4):
  S=sum(1<<v for i in range(3) if chosen_blocks>>i&1 for v in L[i]+R[i])|sum(1<<(off+j) for j in range(2) if conns>>j&1)
  if S and b.connected(S) and b.pm(S):whole=max(whole,b.induced_edges(S))
require(whole==9,'whole_block_only_false_model')
report['three_K33_objective_separation']={'base_vertices':b.n,'all_subsets':(1<<b.n)-1,'balanced_nonempty_subsets':balanced,'connected_optimum':best,'disconnected_feasible_score':27,'whole_block_restricted_optimum':whole,'optimum_vertex_subset':[v for v in range(b.n) if witness>>v&1]}
# Incorrectly small block constants give actual false positives on a NO cover.
mutations=[]
for k in [2,3]:
 b,L,R,T,k,off=construction(2,sets,k);opt,S=b.connected_pm_score();F=3*k*k-k
 require(opt>=F and cover({1,2},sets,1) is None,'insufficient_constant_false_positive')
 mutations.append({'k':k,'connected_optimum':opt,'threshold_for_budget1':F,'SetCover_budget1':False})
report['insufficient_constant_negative_controls']=mutations
report['counts']=COUNTS;report['elapsed_seconds']=time.time()-START;report['status']='All controls passed; no finite extrapolation of universal proof or priority.'
Path(__file__).with_name('INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'elapsed_seconds':report['elapsed_seconds'],'counts':COUNTS,'graphs':graph_count,'cones':cone_count,'set_cover_cases':pre,'full_size_witnesses':len(full),'connected_optimum':best}))
