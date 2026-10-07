"""Exact rational finite arrangement enumeration; authored for OPG-605.
A row [a_1,...,a_d,b] represents sum(a_i*x_i)=b.
No external packages or floating-point geometric decisions.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from collections import defaultdict, deque, Counter
from math import comb

def require(ok, message):
    if not ok: raise ValueError(message)

def solve(rows):
    d=len(rows); m=[[Q(x) for x in r] for r in rows]
    for k in range(d):
        i=next((i for i in range(k,d) if m[i][k]),None)
        require(i is not None,'Normals are not in general position')
        m[i],m[k]=m[k],m[i]; t=m[k][k];m[k]=[x/t for x in m[k]]
        for i in range(d):
            if i!=k:
                t=m[i][k];m[i]=[x-t*y for x,y in zip(m[i],m[k])]
    return tuple(m[i][-1] for i in range(d))

def sgn(x):return (x>0)-(x<0)

def signs(rows,p):return tuple(sgn(sum(Q(a)*x for a,x in zip(r[:-1],p))-Q(r[-1])) for r in rows)

def extensions(s):
    zero=[i for i,x in enumerate(s) if not x]
    for t in product((-1,1),repeat=len(zero)):
        r=list(s)
        for i,x in zip(zero,t):r[i]=x
        yield tuple(r)

def enumerate_arrangement(rows, details=False):
    n=len(rows);d=len(rows[0])-1
    require(d>=2 and n>=d+1,'Need d>=2 and n>=d+1')
    require(all(len(r)==d+1 for r in rows),'Unequal row lengths')
    vertices={}; vertexsign={};cellvertices=defaultdict(set);celledges=defaultdict(set);unbounded=set()
    for basis in combinations(range(n),d):
        p=solve([rows[i] for i in basis]);s=signs(rows,p)
        require(sum(x==0 for x in s)==d,'Concurrent d+1 hyperplanes')
        vertices[basis]=p;vertexsign[basis]=s
        for t in extensions(s):cellvertices[t].add(basis)
    for ridge in combinations(range(n),d-1):
        ids=[b for b in vertices if set(ridge)<=set(b)]
        # Lexicographic order is a strict linear order along this line.
        ids.sort(key=lambda b:vertices[b])
        for u,v in zip(ids,ids[1:]):
            p=tuple((x+y)/2 for x,y in zip(vertices[u],vertices[v]))
            s=signs(rows,p)
            require(sum(x==0 for x in s)==d-1,'Invalid line-edge midpoint')
            for t in extensions(s):celledges[t].add(tuple(sorted((u,v))))
        for u,v in [(ids[0],ids[1]),(ids[-1],ids[-2])]:
            p=tuple(2*x-y for x,y in zip(vertices[u],vertices[v]))
            s=signs(rows,p)
            require(sum(x==0 for x in s)==d-1,'Invalid ray witness')
            unbounded.update(extensions(s))
    require(len(cellvertices)==sum(comb(n,i) for i in range(d+1)),'Wrong total chamber count')
    bounded=sorted(set(cellvertices)-unbounded)
    require(len(bounded)==comb(n-1,d),'Wrong bounded chamber count')
    cells=[];facetuses=Counter()
    for t in bounded:
        vs=cellvertices[t];adj={v:set() for v in vs}
        for u,v in celledges[t]:
            require(u in vs and v in vs,'Edge outside cell')
            adj[u].add(v);adj[v].add(u)
        require(all(len(w)==d for w in adj.values()),'Bounded simple cell is not d-regular')
        diameter=0
        for start in vs:
            dist={start:0};q=deque([start])
            while q:
                u=q.popleft()
                for v in adj[u]:
                    if v not in dist:dist[v]=dist[u]+1;q.append(v)
            require(len(dist)==len(vs),'Disconnected cell graph')
            diameter=max(diameter,max(dist.values()))
        facets=sorted(set().union(*[set(v) for v in vs]))
        for j in facets:
            f=list(t);f[j]=0;facetuses[tuple(f)]+=1
        item={'signs':list(t),'vertices':len(vs),'facets':len(facets),'diameter':diameter}
        if details:
            item['vertex_bases']=[list(v) for v in sorted(vs)]
            item['edges']=[[list(u),list(v)] for u,v in sorted(celledges[t])]
        cells.append(item)
    require(all(x in (1,2) for x in facetuses.values()),'Invalid facet multiplicity')
    # Standard bounded-facet count, checked independently against constructed incidence.
    F=n*comb(n-2,d-1);E=sum(x==1 for x in facetuses.values())
    require(len(facetuses)==F,'Bounded-facet count mismatch')
    S=sum(c['diameter'] for c in cells);I=len(cells)
    slack=sum(c['facets']-d-c['diameter'] for c in cells)
    require(S==d*I+2*comb(n-2,d-1)-E-slack,'Defect identity mismatch')
    out={'dimension':d,'hyperplanes':n,'bounded_cells':I,'diameter_sum':S,'average':str(Q(S,I)),
         'external_facets':E,'hirsch_slack':slack,'defect':d*I-S,
         'diameter_histogram':{str(k):v for k,v in sorted(Counter(c['diameter'] for c in cells).items())},
         'facet_histogram':{str(k):v for k,v in sorted(Counter(c['facets'] for c in cells).items())}}
    if d==3:
        R=sum(2*c['facets']%3 for c in cells)
        T=sum((2*c['facets'])//3-1-c['diameter'] for c in cells)
        require(all((2*c['facets'])//3-1-c['diameter']>=0 for c in cells),'3D cell diameter inequality violated')
        require(3*(3*I-S)==2*E+R+3*T-2*(n-2)*(n-3),'3D identity mismatch')
        out.update(residue_sum=R,barnette_slack=T)
    if details:out['cells']=cells
    return out
