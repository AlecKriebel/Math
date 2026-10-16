#!/usr/bin/env python3
"""Independent literal-grid/lattice and actual dual-alcove graph checks."""
from pathlib import Path
from itertools import product,permutations
from fractions import Fraction
from collections import deque,Counter
from math import comb
import json,hashlib,datetime
C=Path(__file__).resolve().parent

def require(v,m):
    if not v:raise RuntimeError(m)

def admitted(x,signs,m):
    return all(x[i]+x[i+1]<=m if s=='-' else x[i]+x[i+1]>=m for i,s in enumerate(signs))

def alcoves(n):
    result=[]
    for order in permutations(range(n)):
        rank={v:i for i,v in enumerate(order)};floor=[0]
        for i in range(1,n):floor.append(floor[-1]+int(rank[i]<rank[i-1]))
        y=floor[:];verts=[]
        def original(v):return tuple(a-b for a,b in zip(v,[0]+v[:-1]))
        verts.append(original(y))
        for v in reversed(order):y[v]+=1;verts.append(original(y))
        require(all(all(t in (0,1) for t in v) for v in verts),'nonintegral/noncube alcove')
        result.append(frozenset(verts))
    return result

def main():
    lattice_points=0;patterns=0;root_checks=0
    for n in range(1,7):
        for m in range(4):
            for x in product(range(m+1),repeat=n):
                y=[];running=0
                for v in x:running+=v;y.append(running)
                mean=Fraction(sum(y),n+1);lam=[-mean]+[Fraction(v)-mean for v in y]
                require(sum(lam)==0 and all((a-b).denominator==1 for a in lam for b in lam),'coweight lattice')
                require([lam[i+1]-lam[0] for i in range(n)]==y,'inverse difference coordinates')
                require(tuple(y[i]-(y[i-1] if i else 0) for i in range(n))==x,'integral cumulative inverse')
                for signs in product('-+',repeat=n-1):
                    translated=all(y[i+1]-(y[i-1] if i else 0)<=m if s=='-' else y[i+1]-(y[i-1] if i else 0)>=m for i,s in enumerate(signs))
                    require(admitted(x,signs,m)==translated,'signed root-difference equivalence')
                lattice_points+=1
    require(any(v.denominator!=1 for v in [Fraction(-3,4),Fraction(1,4),Fraction(1,4),Fraction(1,4)]),'ambient root-lattice negative control')
    for n in range(1,5):
        all_cells=alcoves(n)
        for signs in product('-+',repeat=n-1):
            cells=[v for v in all_cells if all(admitted(p,signs,1) for p in v)];require(cells,'empty full-dimensional family')
            graph=[[j for j,w in enumerate(cells) if j!=i and len(v&w)==n] for i,v in enumerate(cells)]
            counts=[sum(admitted(x,signs,m) for x in product(range(m+1),repeat=n)) for m in range(n+2)]
            h=[sum((-1)**j*comb(n+1,j)*counts[k-j] for j in range(k+1)) for k in range(n+1)]
            roots=range(len(cells)) if n<=3 else sorted(set([0,len(cells)-1]))
            for root in roots:
                d={root:0};q=deque([root])
                while q:
                    i=q.popleft()
                    for j in graph[i]:
                        if j not in d:d[j]=d[i]+1;q.append(j)
                require(len(d)==len(cells),'disconnected alcove graph')
                require(all(abs(d[i]-d[j])==1 for i,edges in enumerate(graph) for j in edges),'same-level adjacency')
                histogram=Counter(sum(d[j]==d[i]-1 for j in edges) for i,edges in enumerate(graph))
                require([histogram[k] for k in range(n+1)]==h,'prior incoming-arc numerator mismatch');root_checks+=1
            patterns+=1
    r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS_ROOT_PRIOR_FULL_COVERAGE_REDUCTION_CONTROLS','lattice_grid_points':lattice_points,'lattice_dimensions':[1,6],'all_weak_signs_and_ties_checked':True,'alcove_graph_dimensions':[1,4],'signed_families_graph_checked':patterns,'distinct_root_histograms_checked':root_checks,'mechanism':'Candidate-free literal grids, exact cumulative inverse and A_n coweight-lattice coordinates. Actual unit cube alcoves with integral vertices, facet adjacency, BFS indegrees compared with directly counted full h-star numerators.','primary_prior_rule':'Benedetti-Velasquez/Knauer/Valencia-Porras arXiv2303.10458v1 Theorem2.6; independently corroborated by typeA specialization of Bullock/Jiang2412.02787v2 Theorem5.4.','limits':'Finite falsification checks supplement elementary all-n lattice reduction and prior full-covering theorem. No historical explicit OWR closure or journal-status inference. Bullock/Jiang rational-simplex statement must be restricted to unimodular typeA alcoves.','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with (C/'ROOT_PRIORITY_REDUCTION_CONTROLS.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
    print(json.dumps(r))
if __name__=='__main__':main()
