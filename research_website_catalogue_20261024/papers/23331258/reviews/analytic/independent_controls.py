from pathlib import Path
from itertools import combinations,product
from functools import lru_cache
from collections import deque
from fractions import Fraction
import json,time
START=time.time();counts={}
def require(c,label):
 counts[label]=counts.get(label,0)+1
 if not c:raise RuntimeError(label)
class G:
 def __init__(self,n,edges):
  self.n=n;self.edges=list(edges);self.inc=[[] for _ in range(n)]
  for j,(a,b) in enumerate(edges):self.inc[a].append((b,j));self.inc[b].append((a,j))
 def distances(self,terms,F=0):
  result=[]
  for i,a in enumerate(terms[:-1]):
   dist=[999]*self.n;dist[a]=0;todo=deque([a])
   while todo:
    v=todo.popleft()
    for w,j in self.inc[v]:
     if F>>j&1 or dist[w]!=999:continue
     dist[w]=dist[v]+1;todo.append(w)
   result.extend(dist[b] for b in terms[i+1:])
  return tuple(result)
def cover(n,edges):
 adj=[0]*n
 for a,b in edges:adj[a]|=1<<b;adj[b]|=1<<a
 @lru_cache(None)
 def solve(S):
  active=[v for v in range(n) if S>>v&1 and adj[v]&S]
  if not active:return 0
  v=max(active,key=lambda v:(adj[v]&S).bit_count());neigh=adj[v]&S
  return min(1+solve(S&~(1<<v)),neigh.bit_count()+solve(S&~(neigh|1<<v)))
 value=solve((1<<n)-1)
 return value

def attach(n,edges,parts,backup=0):
 terminals=(n,n+1,n+2);all_edges=list(edges)+[(terminals[parts[v]],v) for v in range(n)];N=n+3
 if backup:
  for a,b in combinations(terminals,2):
   internal=list(range(N,N+backup-1));N+=backup-1;path=[a]+internal+[b];all_edges.extend(zip(path,path[1:]))
 return G(N,all_edges),terminals

def direct_opt(graph,terms,finite=False,exact=False):
 original=graph.distances(terms);best=len(graph.edges)+1;witness=None
 for k in range(len(graph.edges)+1):
  for J in combinations(range(len(graph.edges)),k):
   F=sum(1<<j for j in J);d=graph.distances(terms,F)
   ok=all(y>=x+1 for x,y in zip(original,d)) and (not finite or all(y<999 for y in d)) and (not exact or all(y==x+1 for x,y in zip(original,d)))
   if ok:return k,F
 return None,None
report={'scope':'Direct BFS over arbitrary edge deletions is independent of the cover optimizer; finite controls supplement universal proof.'};small=[];allF=0;blockers=0
for sizes in [(1,1,1),(2,1,1),(2,2,1)]:
 parts=[i for i,s in enumerate(sizes) for _ in range(s)];n=len(parts);possible=[(u,v) for u,v in combinations(range(n),2) if parts[u]!=parts[v]]
 for mask in range(1<<len(possible)):
  es=[e for i,e in enumerate(possible) if mask>>i&1];types={tuple(sorted((parts[a],parts[b]))) for a,b in es}
  if types!={(0,1),(0,2),(1,2)}:continue
  graph,term=attach(n,es,parts);require(graph.distances(term)==(3,3,3),'all_three_original_distances');tau=cover(n,es);best=999;valid=0
  for F in range(1<<len(graph.edges)):
   allF+=1;d=graph.distances(term,F)
   if not all(x>=4 for x in d):continue
   valid+=1;blockers+=1;best=min(best,F.bit_count());X=set()
   for j,(a,b) in enumerate(graph.edges):
    if F>>j&1:X.add(a if j<len(es) else b)
   require(len(X)<=F.bit_count() and all(a in X or b in X for a,b in es),'arbitrary_middle_edge_extraction')
  require(best==tau,'direct_bfs_blocker_vs_vertex_cover');small.append({'parts':sizes,'H_edges':es,'optimum':best,'deletion_subsets':1<<len(graph.edges),'blockers':valid})
report['small_tripartite_graphs']=len(small);report['arbitrary_deletion_subsets']=allF;report['valid_blockers_extracted']=blockers
# Exact two-subdivision identity on every nonempty labelled source graph through5vertices.
source_cases=0;budget_cases=0
for n in range(2,6):
 pairs=list(combinations(range(n),2))
 for mask in range(1,1<<len(pairs)):
  es=[e for i,e in enumerate(pairs) if mask>>i&1];m=len(es);hs=[];parts=[0]*n
  for i,(u,v) in enumerate(es):
   b=n+2*i;c=b+1;parts.extend([1,2]);hs.extend([(u,b),(b,c),(c,v)])
  tq=cover(n,es);th=cover(n+2*m,hs);require(th==m+tq,'subdivision_exact_cover_identity');graph,terms=attach(n+2*m,hs,parts)
  require((graph.n,len(graph.edges))==(n+2*m+3,n+5*m),'exact_reduction_size');require(graph.distances(terms)==(3,3,3),'source_reduction_terminal_distances')
  for k in {0,max(0,tq-1),tq,tq+1,1<<2048}:
   require((tq<=k)==(th<=m+k),'binary_budget_equivalence');budget_cases+=1
  source_cases+=1
report['nonempty_labelled_sources_n2_to5']=source_cases;report['budget_checks_including_2049_bit_values']=budget_cases
# Backup constraints tested by full cardinality-order edge-subset optimization on ten attachment graphs.
backups=[]
for x in small[:10]:
 sizes=x['parts'];parts=[i for i,s in enumerate(sizes) for _ in range(s)];graph,terms=attach(len(parts),[tuple(e) for e in x['H_edges']],parts,4)
 finite,F=direct_opt(graph,terms,finite=True);exact,H=direct_opt(graph,terms,exact=True)
 require(finite==exact==x['optimum'],'finite_and_exact_four_backup_optima');require(graph.distances(terms,H)==(4,4,4),'exact_four_witness')
 backups.append({'parts':sizes,'H_edges':x['H_edges'],'finite_optimum':finite,'exact_four_optimum':exact})
report['backup_controls']=backups
# Exact negative cases reject extensions beyond the actual hypotheses.
path_edges=[(0,1),(1,2)];g,terms=attach(3,path_edges,[0,1,2]);opt,F=direct_opt(g,terms)
require(cover(3,path_edges)==1 and opt==2 and g.distances(terms)==(3,4,3),'missing_cross_type_false_extension')
triangle=[(0,1),(1,2),(0,2)];g,terms=attach(3,triangle,[0,1,2],3);opt3,F=direct_opt(g,terms)
require(opt3==5,'three_edge_backup_mutation')
g,terms=attach(3,triangle,[0,1,2]);cost=[Fraction(1)]*3+[Fraction(100)]*3;best=Fraction(999);spokebest=Fraction(999);witness=None
for F in range(1<<len(g.edges)):
 if all(d>=4 for d in g.distances(terms,F)):
  total=sum((cost[j] for j in range(len(cost)) if F>>j&1),Fraction(0))
  if total<best:best=total;witness=F
  if F&7==0:spokebest=min(spokebest,total)
require(best==3 and spokebest==200,'weighted_spoke_rounding_false_extension')
report['negative_controls']={'missing_cross_part_type':{'original_distances':(3,4,3),'tauH':1,'blocker_optimum':2},'incorrect_three_edge_backups':{'tau_triangle':2,'blocker_optimum':opt3},'nonunit_spoke_rounding':{'positive_rational_cost_optimum':str(best),'spoke_only_optimum':str(spokebest),'optimal_edge_indices':[j for j in range(len(cost)) if witness>>j&1]}}
report['counts']=counts;report['elapsed_seconds']=time.time()-START;report['status']='All independent exact controls passed; no universal proof or priority inferred from finite enumeration.'
Path(__file__).with_name('INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'seconds':report['elapsed_seconds'],'tripartite_graphs':len(small),'arbitrary_edge_subsets':allF,'source_graphs':source_cases,'counts':counts}))
