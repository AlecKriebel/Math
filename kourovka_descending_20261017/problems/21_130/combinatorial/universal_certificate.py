#!/usr/bin/env python3
"""Generate a finite obstruction-tree certificate for a universal small-n result."""
import itertools,json,time,sys
from pathlib import Path
from universal_small import canonical,contains

def problem(n):
 V=tuple(range(n));cycles=[(0,)+p for p in itertools.permutations(range(1,n)) if p[0]<p[-1]]
 events=[]
 for Q in itertools.combinations(V,4):
  a,b,c,d=Q
  for L,R in [((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))]:events.append((tuple(int(k in L)-int(k in R) for k in range(1,n)),L,R))
 cycle_events=[]
 for a in cycles:
  E={tuple(sorted((a[i],a[(i+1)%n]))) for i in range(n)}
  cycle_events.append([j for j,(_,L,R) in enumerate(events) if L in E and R in E])
 diffs=[(tuple(int(k==i)-int(k==j) for k in range(1,n)),(i,j)) for i,j in itertools.combinations(V,2)]
 return cycles,events,cycle_events,diffs

def generate(n):
 cycles,events,CE,diffs=problem(n);nodes=[];ids={};started=time.time()
 def visit(H):
  if H in ids:return ids[H]
  idx=len(nodes);ids[H]=idx;nodes.append(None)
  assert not any(contains(H,v) for v,_ in diffs)
  implied={j for j,(r,_,_) in enumerate(events) if contains(H,r)}
  uncovered=[i for i,C in enumerate(CE) if not implied.intersection(C)]
  if not uncovered:raise RuntimeError('Found a realizable no-rainbow quotient')
  cache={}
  def child(j):
   if j not in cache:
    Q=canonical(H+(events[j][0],),n-1)
    collapse=next((ij for v,ij in diffs if contains(Q,v)),None)
    cache[j]=(Q,collapse)
   return cache[j]
  i=min(uncovered,key=lambda i:len({Q for j in CE[i] for Q,collapse in [child(j)] if collapse is None}))
  branches=[]
  for j in CE[i]:
   Q,collapse=child(j)
   assert Q!=H
   if collapse is not None:branches.append({'event':j,'forced_equal_vertices':collapse})
   else:branches.append({'event':j,'child':visit(Q)})
  nodes[idx]={'lattice':H,'cycle':i,'branches':branches}
  return idx
 root=visit(tuple());result={'format':'odd-abelian-collision-cover-v1','n':n,'root':root,'node_count':len(nodes),'nodes':nodes,'generation_seconds':time.time()-started}
 p=Path(f'universal_{n}_certificate.json');p.write_text(json.dumps(result,separators=(',',':'))+'\n')
 print('CERTIFICATE',n,len(nodes),time.time()-started,p,flush=True)

def verify(n):
 data=json.loads(Path(f'universal_{n}_certificate.json').read_text());cycles,events,CE,diffs=problem(n);nodes=data['nodes'];started=time.time();edges=0;collapses=0
 Hs=[tuple(tuple(r) for r in x['lattice']) for x in nodes]
 assert Hs[data['root']]==tuple()
 for k,node in enumerate(nodes):
  H=Hs[k];assert canonical(H,n-1)==H
  assert not any(contains(H,v) for v,_ in diffs)
  ci=node['cycle'];assert 0<=ci<len(cycles)
  assert all(not contains(H,events[j][0]) for j in CE[ci])
  assert [b['event'] for b in node['branches']]==CE[ci]
  for branch in node['branches']:
   j=branch['event'];Q=canonical(H+(events[j][0],),n-1);assert Q!=H
   if 'child' in branch:
    assert Q==Hs[branch['child']];edges+=1
   else:
    i,j=branch['forced_equal_vertices'];v=tuple(int(z==i)-int(z==j) for z in range(1,n));assert contains(Q,v);collapses+=1
 # Strictly increasing relation lattices on every child edge preclude directed cycles.
 result={'n':n,'verified_nodes':len(nodes),'verified_child_edges':edges,'verified_collision_leaves':collapses,'seconds':time.time()-started,'passed':True}
 Path(f'universal_{n}_certificate_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
 n=int(sys.argv[1]) if len(sys.argv)>1 else 7
 if len(sys.argv)>2 and sys.argv[2]=='verify':verify(n)
 else:generate(n);verify(n)
