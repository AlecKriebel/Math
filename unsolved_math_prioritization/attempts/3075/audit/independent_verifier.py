#!/usr/bin/env python3
"""Independent exact planar audit by feasible vertices and recession-cone rays.
Does not import either author geometry implementation and uses no clipping.
A row (a,b,c) is a*x+b*y=c. All geometric decisions use Fraction.
"""
from fractions import Fraction
from itertools import combinations, product
from collections import Counter, deque
from pathlib import Path
import hashlib,json,sys
ROWS=((1,1,5),(1,2,-1),(1,4,2),(1,5,-2),(1,7,2),(1,8,-5),(1,9,-1),(1,10,-2))

def need(test, message):
    if not test: raise ValueError(message)

def enumerate_cells(rows):
    n=len(rows); points={}
    for i,j in combinations(range(n),2):
        a,b,c=rows[i]; d,e,f=rows[j]; determinant=a*e-b*d
        need(determinant!=0,'Parallel pair')
        p=(Fraction(c*e-b*f,determinant),Fraction(a*f-c*d,determinant))
        need(all(k in (i,j) or u*p[0]+v*p[1]!=w for k,(u,v,w) in enumerate(rows)), 'Concurrent triple')
        points[(i,j)]=p
    cells=[]; feasible_count=0; unbounded_count=0
    for signs in product((-1,1),repeat=n):
        vs={pair:p for pair,p in points.items() if all(s*(a*p[0]+b*p[1]-c)>=0 for s,(a,b,c) in zip(signs,rows))}
        if not vs: continue
        feasible_count+=1
        # A nontrivial pointed 2D polyhedral cone has an extreme ray lying
        # on a defining homogeneous line. Test both directions of every line.
        is_unbounded=any(all(s*(a*dx+b*dy)>=0 for s,(a,b,c) in zip(signs,rows))
                         for u,v,w in rows for dx,dy in [(v,-u),(-v,u)])
        if is_unbounded: unbounded_count+=1;continue
        need(len(vs)>=3,'Bounded polygon has fewer than three vertices')
        edges=[];adj={pair:set() for pair in vs}
        for line in range(n):
            endpoints=[p for p in vs if line in p]
            need(len(endpoints) in (0,2),'Facet endpoint count is not zero or two')
            if len(endpoints)==2:
                a,b=sorted(endpoints);edges.append((a,b));adj[a].add(b);adj[b].add(a)
        need(all(len(v)==2 for v in adj.values()),'Polygon not a cycle')
        diameter=0
        for v in vs:
            dist={v:0};queue=deque([v])
            while queue:
                u=queue.popleft()
                for w in adj[u]:
                    if w not in dist:dist[w]=dist[u]+1;queue.append(w)
            need(len(dist)==len(vs),'Disconnected polygon')
            diameter=max(diameter,max(dist.values()))
        need(diameter==len(vs)//2,'Graph/cycle diameter disagreement')
        cells.append({'signs':list(signs),'vertices':len(vs),'facets':len(edges),'diameter':diameter,
                      'vertex_bases':[list(p) for p in sorted(vs)],
                      'edges':[[list(a),list(b)] for a,b in sorted(edges)],
                      'coordinates':sorted([[str(x),str(y)] for x,y in vs.values()])})
    need(feasible_count==1+n*(n+1)//2,'All-cell count mismatch')
    need(len(cells)==(n-1)*(n-2)//2,'Bounded-cell count mismatch')
    need(unbounded_count==2*n,'Unbounded-cell count mismatch')
    facet_counts=Counter()
    for cell in cells:
        for a,b in cell['edges']:
            common=set(a)&set(b);need(len(common)==1,'Invalid supporting line')
            label=cell['signs'].copy();label[next(iter(common))]=0;facet_counts[tuple(label)]+=1
    need(all(v in (1,2) for v in facet_counts.values()),'Facet incidence count')
    need(len(facet_counts)==n*(n-2),'Total bounded-facet count')
    S=sum(c['diameter'] for c in cells);I=len(cells)
    E=sum(v==1 for v in facet_counts.values());sigma=sum(c['facets']-2-c['diameter'] for c in cells)
    need(2*I-S==E+sigma-2*(n-2),'Planar defect identity')
    return {'hyperplanes':n,'bounded_cells':I,'feasible_cells':feasible_count,
            'unbounded_cells':unbounded_count,'diameter_sum':S,'defect':2*I-S,
            'average':str(Fraction(S,I)),'external_facets':E,'hirsch_slack':sigma,
            'facet_histogram':dict(sorted(Counter(str(c['facets']) for c in cells).items())),
            'cells':cells}

def main():
    witness=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent/'accepted/witness.json'
    data=json.loads(witness.read_text());need(data['hyperplanes']==[list(r) for r in ROWS],'Coefficient identity')
    need(data['delete_zero_based']==5,'Deletion identity')
    output={}
    for label,rows in [('full',ROWS),('deletion',ROWS[:5]+ROWS[6:])]:
        result=enumerate_cells(rows);auth=data[label]
        authored={tuple(c['signs']):c for c in auth['cells']}
        polygons={tuple(c['signs']):c for c in auth['polygons']}
        need(len(authored)==len(result['cells'])==len(polygons),'Certificate cell count')
        for c in result['cells']:
            key=tuple(c['signs']);need(key in authored and key in polygons,'Missing sign cell')
            need({k:c[k] for k in authored[key]}==authored[key],'Author graph certificate disagreement')
            need(c['coordinates']==sorted(polygons[key]['polygon']),'Author rational polygon disagreement')
        for key in ['bounded_cells','diameter_sum','defect','average','external_facets','hirsch_slack','facet_histogram']:
            need(result[key]==auth[key],'Author aggregate disagreement: '+key)
        output[label]={k:v for k,v in result.items() if k!='cells'}
    deletion_defects=[enumerate_cells(ROWS[:j]+ROWS[j+1:])['defect'] for j in range(8)]
    need(deletion_defects==[6,5,5,6,6,7,6,6],'All-deletion defects disagree')
    need(output['full']['diameter_sum']-output['deletion']['diameter_sum']==13>12,'No arbitrary-deletion obstruction')
    output.update(result='PASS',algorithm='feasible pair intersections, recession rays, and BFS; no author imports',
                  all_deletion_defects=deletion_defects,witness_sha256=hashlib.sha256(witness.read_bytes()).hexdigest())
    print(json.dumps(output,sort_keys=True,indent=2))
if __name__=='__main__':
    try:main()
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
