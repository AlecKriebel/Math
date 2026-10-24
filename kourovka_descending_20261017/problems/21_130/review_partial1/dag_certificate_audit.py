#!/usr/bin/env python3
"""Check the n=7 obstruction DAG using independent integer lattice routines."""
from itertools import combinations,permutations
from collections import deque
from pathlib import Path
import hashlib,json,datetime,time
from lattice_row_reproduction import row_hnf,saturation_at_two,member

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def need(x,message):
    if not x:raise ValueError(message)

def audit():
    started=time.monotonic();path=ROOT/'combinatorial/universal_7_certificate.json'
    raw=path.read_bytes();sha=hashlib.sha256(raw).hexdigest();data=json.loads(raw)
    n=data['n'];need(n==7 and data['format']=='odd-abelian-collision-cover-v1','format/domain')
    cycles=[(0,)+p for p in permutations(range(1,n)) if p[0]<p[-1]]
    events=[]
    for a,b,c,d in combinations(range(n),4):
        for e,f in (((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))):
            events.append((tuple(int(k in e)-int(k in f) for k in range(1,n)),frozenset(e),frozenset(f)))
    CE=[]
    for c in cycles:
        E={frozenset((c[i],c[(i+1)%n])) for i in range(n)}
        CE.append([j for j,(_,e,f) in enumerate(events) if e in E and f in E])
    differences=[tuple(int(k==i)-int(k==j) for k in range(1,n)) for i,j in combinations(range(n),2)]
    nodes=data['nodes'];need(data['node_count']==len(nodes),'node count')
    Hs=[tuple(tuple(r) for r in node['lattice']) for node in nodes]
    root=data['root'];need(type(root)is int and 0<=root<len(nodes) and Hs[root]==(),'root')
    need(len(set(Hs))==len(Hs),'duplicate lattice nodes')
    graph=[set() for _ in nodes];indegree=[0]*len(nodes);edges=leaves=0
    for u,node in enumerate(nodes):
        H=Hs[u]
        need(all(len(r)==n-1 and all(type(x)is int for x in r) for r in H),'integer lattice dimension')
        need(saturation_at_two(H,n-1)==H,'noncanonical or nonsaturated node')
        need(not any(member(H,v) for v in differences),'collided node vertices')
        ci=node['cycle'];need(type(ci)is int and 0<=ci<len(cycles),'cycle index')
        need(all(not member(H,events[j][0]) for j in CE[ci]),'already forced collision in branch cycle')
        branches=node['branches'];need([b['event'] for b in branches]==CE[ci],'incomplete branch coverage')
        for branch in branches:
            j=branch['event'];Q=saturation_at_two((*H,events[j][0]),n-1)
            need(Q!=H and all(member(Q,r) for r in H),'child lattice not strict enlargement')
            if 'child' in branch:
                v=branch['child'];need(type(v)is int and 0<=v<len(nodes),'child range')
                need(Hs[v]==Q,'incorrect child quotient')
                if v not in graph[u]:graph[u].add(v);indegree[v]+=1
                edges+=1
            else:
                i,k=branch['forced_equal_vertices']
                need(type(i)is int and type(k)is int and 0<=i<k<n,'forced pair domain')
                d=tuple(int(z==i)-int(z==k) for z in range(1,n))
                need(member(Q,d),'unproved equality leaf');leaves+=1
    # Independently verify finiteness of the proof by ordinary directed-graph checks.
    queue=deque(i for i,z in enumerate(indegree) if z==0);topological=[]
    while queue:
        u=queue.popleft();topological.append(u)
        for v in graph[u]:
            indegree[v]-=1
            if not indegree[v]:queue.append(v)
    need(len(topological)==len(nodes),'directed cycle')
    reached={root};queue=deque((root,))
    while queue:
        for v in graph[queue.popleft()]:
            if v not in reached:reached.add(v);queue.append(v)
    need(len(reached)==len(nodes),'unreachable nodes')
    need(hashlib.sha256(path.read_bytes()).hexdigest()==sha,'certificate changed during review')
    return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'certificate_sha256':sha,'certificate_bytes':len(raw),
            'method':'independent Euclidean row HNF and exhaustive parity-subset saturation; independent cycle events and explicit DAG/reachability checks',
            'n':n,'nodes':len(nodes),'branch_child_edges':edges,'forced_equality_leaves':leaves,
            'acyclic':True,'all_nodes_reachable':True,'all_branches_covered':True,'seconds':time.monotonic()-started,'passed':True}

if __name__=='__main__':
    r=audit();(HERE/'dag_certificate_audit_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
