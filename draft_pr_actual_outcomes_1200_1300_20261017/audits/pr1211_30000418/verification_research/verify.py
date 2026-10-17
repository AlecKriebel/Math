#!/usr/bin/env python3
"""Root exact global-CSP reproduction, no historical code or solver dependencies."""
from collections import deque
from pathlib import Path
import hashlib,json,random
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'specimen.json').read_text())
VERTICES=tuple(DATA['vertices'])
EDGES=tuple(tuple(e) for e in DATA['edges'])
ADJ={v:set() for v in VERTICES}
for u,v in EDGES:ADJ[u].add(v);ADJ[v].add(u)
def require(c,m):
 if not c:raise ValueError(m)
DIST={}
for root in VERTICES:
 seen={root:0};q=deque([root])
 while q:
  v=q.popleft()
  for w in ADJ[v]:
   if w not in seen:seen[w]=seen[v]+1;q.append(w)
 DIST[root]=seen
require(len(EDGES)==len(VERTICES)-1 and all(len(d)==len(VERTICES) for d in DIST.values()),'tree')
CONSTRAINTS=[(u,v,2 if DIST[u][v]==1 else 1) for i,u in enumerate(VERTICES) for v in VERTICES[i+1:] if DIST[u][v]<=2]
A=(1,2,3,4,5);B=(1,3,4,5,6)
BAD={v:tuple(DATA['lists'][v]) for v in VERTICES}
def check(witness,lists):
 return set(witness)==set(VERTICES) and all(witness[v] in lists[v] for v in VERTICES) and all(abs(witness[u]-witness[v])>=gap for u,v,gap in CONSTRAINTS)
def solve(lists):
 count=0;nodes=0;first=None;levels={}
 assignment={}
 def search():
  nonlocal count,nodes,first
  nodes+=1;levels[len(assignment)]=levels.get(len(assignment),0)+1
  if len(assignment)==len(VERTICES):
   require(check(assignment,lists),'independent witness check');count+=1
   if first is None:first=dict(assignment)
   return
  options=[]
  for v in VERTICES:
   if v in assignment:continue
   available=[x for x in lists[v] if all(DIST[v][u]>2 or abs(x-y)>=(2 if DIST[v][u]==1 else 1) for u,y in assignment.items())]
   options.append((len(available),-sum(DIST[v][u]<=2 for u in VERTICES if u not in assignment),v,available))
  _,_,v,available=min(options)
  for x in available:assignment[v]=x;search();del assignment[v]
 search()
 return {'solutions':count,'first_witness':first,'search_nodes':nodes,'depth_node_counts':levels}
def greedy(lists):
 order=[];parent={'c':None};q=deque(['c'])
 while q:
  v=q.popleft();order.append(v)
  for w in sorted(ADJ[v]):
   if w!=parent[v]:parent[w]=v;q.append(w)
 out={};forbidden_max=0
 for v in order:
  forbidden={x for x in lists[v] for u,y in out.items() if DIST[v][u]<=2 and abs(x-y)<(2 if DIST[v][u]==1 else 1)}
  forbidden_max=max(forbidden_max,len(forbidden));available=set(lists[v])-forbidden
  require(bool(available),'six-list greedy availability');out[v]=min(available)
 require(check(out,lists),'six-list greedy witness')
 return forbidden_max

def main():
 require(DATA['schema']=='tree-L21-specimen-v1','input schema')
 require(VERTICES==('a','b','c','d','e','a1','a2','b1','d1','e1','e2'),'paper vertex binding')
 require(set(tuple(sorted(e)) for e in EDGES)==set(tuple(sorted(e)) for e in [('a','b'),('b','c'),('c','d'),('d','e'),('a','a1'),('a','a2'),('b','b1'),('d','d1'),('e','e1'),('e','e2')]),'paper edge binding')
 require(len(EDGES)==10 and len(set(VERTICES))==11,'simple graph cardinality')
 require(set(DATA['lists'])==set(VERTICES),'complete list domain')
 require(all(len(BAD[v])==5 and len(set(BAD[v]))==5 and all(type(x) is int and x>0 for x in BAD[v]) for v in VERTICES),'five distinct positive integer list labels')
 require(all(type(x) is int for x in DATA['ordinary_five_witness'].values()),'integer witness labels')
 require(all(type(x) is int for x in DATA['expected_counts'].values()),'integer count metadata')
 require(all(BAD[v]==(B if v in ('a1','a2','e1','e2') else A) for v in VERTICES),'paper list binding')
 require(check(DATA['ordinary_five_witness'],{v:A for v in VERTICES}),'provided common-palette witness')
 require(DATA['expected_counts']=={'common_4':0,'common_5':8,'common_6':6336,'bad_five_lists':0},'claimed count metadata')
 outputs={f'common_{k}':solve({v:tuple(range(1,k+1)) for v in VERTICES}) for k in range(1,7)}
 outputs['bad_five_lists']=solve(BAD)
 require(outputs['common_4']['solutions']==0 and outputs['common_5']['solutions']>0,'ordinary exact5')
 require(outputs['bad_five_lists']['solutions']==0,'bad list assignment')
 r=random.Random(20261017);greedy_max=0
 for _ in range(1000):greedy_max=max(greedy_max,greedy({v:tuple(sorted(r.sample(range(1,45),6))) for v in VERTICES}))
 common=outputs['common_5']['first_witness'];require(check(common,{v:A for v in VERTICES}),'ordinary witness')
 broken=dict(common);broken['b']=broken['a'];require(not check(broken,{v:A for v in VERTICES}),'edge corruption rejected')
 broken=dict(common);broken['a1']=broken['a2'];require(not check(broken,{v:A for v in VERTICES}),'distance2 corruption rejected')
 broken=dict(common);broken['a1']=99;require(not check(broken,{v:A for v in VERTICES}),'list-membership corruption rejected')
 report={'specimen_sha256':hashlib.sha256((HERE/'specimen.json').read_bytes()).hexdigest(),'mechanism':'global minimum-remaining-values backtracking, all solutions enumerated; direct all-pair distance checks; no submitted program imported','tree_vertices':len(VERTICES),'tree_edges':len(EDGES),'maximum_degree':max(map(len,ADJ.values())),'diameter':max(max(d.values()) for d in DIST.values()),'radius':min(max(d.values()) for d in DIST.values()),'constraints':[list(c) for c in CONSTRAINTS],'lists':BAD,'enumerations':outputs,'random_greedy_6_list_instances':1000,'maximum_forbidden_list_entries_observed':greedy_max,'negative_controls_rejected':['edge equality','distance2 equality','outside-list label'],'limits':'Finite enumeration verifies only specified lists. Universal six-list upper bound and infinite extension are analytic arguments, not consequences of random checks.'}
 (HERE/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:{'solutions':v['solutions'],'nodes':v['search_nodes']} for k,v in outputs.items()},indent=2))
if __name__=='__main__':main()
