"""Own tree sum-product states and explicit distances; no supplied imports.
Finite checks support, rather than replace, the universal proofs.
"""
from collections import deque
from functools import lru_cache
from itertools import product
from random import Random
from datetime import datetime,timezone
import json,hashlib
V=['a','b','c','d','e','a1','a2','b1','d1','e1','e2']
EDGES=[(0,1),(1,2),(2,3),(3,4),(0,5),(0,6),(1,7),(3,8),(4,9),(4,10)]
W=[1,5,3,1,5,3,4,2,4,2,3];LEAVES=[5,6,7,8,9,10]
A=(1,2,3,4,5);B=(1,3,4,5,6)
def adj(n,edges):
 g=[[] for _ in range(n)]
 for u,v in edges:g[u].append(v);g[v].append(u)
 return g
def distances(g):
 out=[]
 for s in range(len(g)):
  d=[-1]*len(g);d[s]=0;q=deque([s])
  while q:
   x=q.popleft()
   for y in g[x]:
    if d[y]<0:d[y]=d[x]+1;q.append(y)
  assert min(d)>=0;out.append(d)
 return out
def valid(g,f,lists=None):
 if lists is not None and any(f[i] not in lists[i] for i in range(len(g))):return False
 d=distances(g)
 return all((abs(f[i]-f[j])>=2 if d[i][j]==1 else f[i]!=f[j]) for i in range(len(g)) for j in range(i) if d[i][j] in (1,2))
def tree_count(g,lists,root=2,sibling=True,grandparent=True):
 parent=[None]*len(g);parent[root]=-1;order=[root]
 for v in order:
  for u in g[v]:
   if u==parent[v]:continue
   assert parent[u] is None,'not a tree';parent[u]=v;order.append(u)
 assert len(order)==len(g)
 children=[[u for u in g[v] if parent[u]==v] for v in range(len(g))]
 @lru_cache(None)
 def F(v,p,x):
  if x not in lists[v] or (p is not None and abs(x-p)<2):return 0
  options=[[y for y in lists[u] if abs(y-x)>=2 and (p is None or y!=p or not grandparent)] for u in children[v]]
  total=0
  for ys in product(*options):
   if sibling and len(set(ys))!=len(ys):continue
   term=1
   for u,y in zip(children[v],ys):term*=F(u,x,y)
   total+=term
  return total
 ans=sum(F(root,None,x) for x in lists[root])
 # Locally inadmissible states must be zero even for a leaf.
 leaf=next(v for v in range(len(g)) if not children[v]);x=lists[leaf][0];assert F(leaf,x,x)==0
 return ans,F.cache_info().currsize
def generic_count(g,lists):
 d=distances(g);f=[None]*len(g)
 def rec(left):
  if not left:return 1
  allowed={v:[x for x in lists[v] if all(f[u] is None or (abs(x-f[u])>=2 if d[v][u]==1 else x!=f[u]) for u in range(len(g)) if d[v][u] in (1,2))] for v in left}
  v=min(left,key=lambda v:(len(allowed[v]),v));total=0
  for x in allowed[v]:f[v]=x;total+=rec(left-{v})
  f[v]=None;return total
 return rec(set(range(len(g))))
def extend(lengths):
 edges=list(EDGES);labels=list(W)
 for leaf,L in zip(LEAVES,lengths):
  p=leaf;gp=next(u if v==leaf else v for u,v in EDGES if leaf in (u,v))
  for _ in range(L):
   x=len(labels);labels.append(next(c for c in A if abs(c-labels[p])>=2 and c!=labels[gp]));edges.append((p,x));gp,p=p,x
 return adj(len(labels),edges),labels
def greedy(g,lists,root):
 f=[None]*len(g);parent=[None]*len(g);parent[root]=-1;q=[root];d=distances(g)
 for v in q:
  f[v]=next(x for x in lists[v] if all(f[u] is None or (abs(x-f[u])>=2 if d[v][u]==1 else x!=f[u]) for u in range(len(g)) if d[v][u] in (1,2)))
  for u in g[v]:
   if u!=parent[v]:assert parent[u] is None;parent[u]=v;q.append(u)
 assert valid(g,f,lists);return f
def run():
 g=adj(11,EDGES);d=distances(g);bad=[B if i in (5,6,9,10) else A for i in range(11)];assert valid(g,W)
 counts={};states={}
 for k in (4,5,6):counts[str(k)],states[str(k)]=tree_count(g,[tuple(range(1,k+1))]*11)
 badcount,badstates=tree_count(g,bad);assert counts=={'4':0,'5':8,'6':6336} and badcount==0
 assert generic_count(g,[A]*11)==8 and generic_count(g,bad)==0
 rootchecks=[]
 for root in range(11):
  assert tree_count(g,[A]*11,root)[0]==8 and tree_count(g,bad,root)[0]==0;rootchecks.append(root)
 digest=hashlib.sha256();extension_tests=0
 for lengths in product(range(3),repeat=6):
  gg,f=extend(lengths);dd=distances(gg);assert valid(gg,f) and max(map(len,gg))==3 and all(dd[i][j]==d[i][j] for i in range(11) for j in range(11))
  groups=[];start=11
  for L in lengths:groups.append(range(start,start+L));start+=L
  assert all(dd[x][y]>=4 for i in range(6) for j in range(i) for x in groups[i] for y in groups[j])
  extension_tests+=1;digest.update(str((lengths,f)).encode())
 longg,longf=extend((200,0,0,0,0,0));assert valid(longg,longf) and max(map(max,distances(longg)))==206
 rng=Random(12220261115);greedytests=0
 for n in (1,2,3,8,25,60):
  for _ in range(8):
   edges=[];degrees=[0]*n
   for v in range(1,n):
    u=rng.choice([i for i in range(v) if degrees[i]<3]);edges.append((u,v));degrees[u]+=1;degrees[v]+=1
   gg=adj(n,edges);K=max(degrees,default=0)+3
   lists=[tuple(sorted(rng.sample(range(1,35),K))) for _ in range(n)];greedy(gg,lists,rng.randrange(n));greedytests+=1
 no_sibling=tree_count(g,bad,sibling=False)[0];assert no_sibling>0
 p3=adj(3,[(0,1),(1,2)]);assert not valid(p3,[1,3,1]) and not valid(p3,[1,2,3])
 # Manually reconstructed actual FS2001Fig4: two triangular end caps and two
 # length-three rails. Only left tip has {1,2,4,5,6}; other lists are A.
 fsedges=[(0,1),(1,2),(2,3),(4,5),(5,6),(6,7),(0,4),(3,7),(8,0),(8,4),(9,3),(9,7)]
 fsg=adj(10,fsedges);fsw=[1,4,2,5,5,2,4,1,3,3];assert valid(fsg,fsw)
 fsbad=[A]*10;fsbad[8]=(1,2,4,5,6);fscount=generic_count(fsg,fsbad);assert fscount==0
 return {'status':'PASS','UTC':datetime.now(timezone.utc).isoformat(),'literal_tree':{'vertices':V,'edges':EDGES,'n':11,'m':10,'maximum_degree':3,'radius':min(map(max,d)),'diameter':max(map(max,d)),'distance_two_pairs':sum(d[i][j]==2 for i in range(11) for j in range(i))},'tree_DP_common_palette_counts':counts,'tree_DP_states':states,'bad_five_list_count':badcount,'bad_list_DP_states':badstates,'independent_generic_CSP_comparison':'[5]=8 and bad_lists=0','all_eleven_root_reorientations_checked':rootchecks,'independent_path_length_tuples_checked':extension_tests,'extension_case_SHA256':digest.hexdigest(),'long_extension':{'lengths':[200,0,0,0,0,0],'vertices':len(longg),'diameter':206},'arbitrary_sparse_list_tree_greedy_cases':greedytests,'negative_controls':{'omitting_sibling_constraint_admits_bad_lists_count':no_sibling,'grandparent_repeat_1_3_1_rejected':True,'adjacent_separation_1_2_3_rejected':True,'inadmissible_DP_leaf_parent_state_returns_zero':True},'actual_primary_FS2001Fig4_reconstruction':{'vertices':10,'edges':fsedges,'m':12,'connected_cycle_rank':3,'ordinary_five_witness':fsw,'bad_five_lists_count':fscount,'source':'manually read actual Fig4p14 after initial seal, before supplied programs'},'limits':['Finite checks do not prove all arbitrary six-list assignments or all six-parameter path lengths.','The universal greedy and extension proofs are in the initial reconstruction.','No all-tree minimality search or historical firstness claim.']}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
