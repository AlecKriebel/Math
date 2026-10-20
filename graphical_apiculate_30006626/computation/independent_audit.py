import sys,itertools as it,json,collections,time
import networkx as nx
from pathlib import Path
P=str(Path(__file__).resolve().parent)+'/'
def intervals(n,edges):
 d=[[0 if i==j else 999 for j in range(n)] for i in range(n)]
 for i,j in edges:d[i][j]=d[j][i]=1
 for k in range(n):
  for i in range(n):
   for j in range(n):d[i][j]=min(d[i][j],d[i][k]+d[k][j])
 if any(999 in row for row in d):return None
 return [[sum(1<<k for k in range(n) if d[i][k]+d[k][j]==d[i][j]) for j in range(n)] for i in range(n)]
def table(n,I):
 a={}
 for u,v,w in it.product(range(n),repeat=3):
  common=I[u][v]&I[u][w]
  tops=[x for x in range(n) if common>>x&1 and common&I[u][x]==common]
  if len(tops)!=1:return None
  a[u,v,w]=tops[0]
 return a
def check(n,edges):
 I=intervals(n,edges);a=table(n,I)
 if a is None:return None,None,0
 constraints=[]
 for x,y,z in it.combinations(range(n),3):
  constraints.append(((1<<x)|(1<<y)|(1<<z),(1<<a[x,y,z])|(1<<a[y,x,z])|(1<<a[z,x,y])))
 bad=closed=0
 for mask in range(1,1<<n):
  if any(mask&inp==inp and mask&out!=out for inp,out in constraints):continue
  closed+=1;S=[x for x in range(n) if mask>>x&1]
  edgesH=[(i,j) for i in range(len(S)) for j in range(i) if I[S[i]][S[j]]&mask==(1<<S[i])|(1<<S[j])]
  J=intervals(len(S),edgesH)
  if J is None or any(sum(1<<S[k] for k in range(len(S)) if J[i][j]>>k&1)!=I[S[i]][S[j]]&mask for i in range(len(S)) for j in range(len(S))):bad+=1
 return a,bad,closed
start=time.time();counts=collections.defaultdict(collections.Counter);diff=[];idbad=[]
orig=json.load(open(P+'atlas_apex_results.json')); gs=set(orig['graphical_atlas_indices'])
for ix,G in enumerate(nx.graph_atlas_g()):
 n=len(G)
 if not n or not nx.is_connected(G):continue
 counts[n]['connected']+=1;a,bad,closed=check(n,G.edges())
 if a is None:continue
 counts[n]['apiculate']+=1;counts[n]['graphical' if not bad else 'nongraphical']+=1
 if (not bad)!=(ix in gs):diff.append(ix)
 if not bad:
  for u,v,w,x in it.product(range(n),repeat=4):
   L=a[a[u,w,x],a[a[u,v,x],w,x],u];R=a[u,w,x]
   if L!=R:idbad.append([ix,'A9',[u,v,w,x],L,R]);break
   L=a[a[w,u,x],a[u,v,w],v];R=a[w,a[u,v,w],a[v,u,a[w,u,x]]]
   if L!=R:idbad.append([ix,'A11',[u,v,w,x],L,R]);break
print('ATLAS',dict(counts),'DIFF',diff,'IDENTITY_BAD',len(idbad),idbad[:2],flush=True)
H=nx.convert_node_labels_to_integers(nx.cartesian_product(nx.graph_atlas_g()[43],nx.path_graph(3)))
a,bad,closed=check(len(H),H.edges())
print('HOUSEXP3',len(H),bad,closed,'SECONDS',time.time()-start,flush=True)
for ix in [43,147,148]:
 G=nx.graph_atlas_g()[ix];a,bad,closed=check(len(G),G.edges());print('WITNESS',ix,'BAD',bad,'CLOSED',closed,flush=True)
for name,G in [('house*K2',nx.cartesian_product(nx.graph_atlas_g()[43],nx.path_graph(2))),('C5*K2',nx.cartesian_product(nx.cycle_graph(5),nx.path_graph(2)))]:
 G=nx.convert_node_labels_to_integers(G);a,bad,closed=check(len(G),G.edges());print('PRODUCT',name,bad,closed,flush=True)
