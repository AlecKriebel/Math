#!/usr/bin/env python3
"""Independent rational simplicial embedding certificate, 2026-10-03.

Mathematical data transcribed directly from Mizhaev arXiv:2609.17700v1,
Tables 1--2. No import or reuse of the author's verification functions.
The alternate route is ear triangulation plus all 1,540 triangle pairs.
Plane sections of convex triangles use signed endpoint distances, never
polygon ray casting, sample points, or a solved intersection-line origin.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import defaultdict, Counter
import ast, hashlib, json, pathlib

XYZ = '''
-72 84 18; -36 112 102; 72 -84 18; 36 -112 102;
0 300 234; -84 48 -18; 9 147 207; 0 -300 234;
84 -48 -18; -112 -36 -102; 48 84 18; -147 9 -207;
-9 -147 207; 84 72 -18; 112 36 -102; -48 -84 18;
147 -9 -207; -18 126 144; -126 -18 -144; -300 0 -234;
-84 -72 -18; 18 -126 144; 126 18 -144; 300 0 -234
'''
WALKS = '''
6 10 16 22 18 7 5 1 2;
9 15 11 18 22 13 8 3 4;
7 5 8 3 17 23 9 15 14;
13 8 5 1 12 19 6 10 21;
1 2 11 18 7 14 24 20 12;
3 4 16 22 13 21 20 24 17;
14 24 17 23 19 6 2 11 15;
10 21 20 12 19 23 9 4 16
'''
V = [tuple(F(x) for x in row.split()) for row in XYZ.split(';')]
C = [[int(x)-1 for x in row.split()] for row in WALKS.split(';')]
def minus(x,y): return tuple(a-b for a,b in zip(x,y))
def inner(x,y): return sum(a*b for a,b in zip(x,y))
def vector(x,y): return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
def det(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def boundary(c): return zip(c,c[1:]+c[:1])
def normal(t): return vector(minus(t[1],t[0]),minus(t[2],t[0]))
def signed_area(p): return sum(a[0]*b[1]-a[1]*b[0] for a,b in boundary(p))
def between(p,a,b):
    return not det(a,b,p) and all((p[i]-a[i])*(p[i]-b[i])<=0 for i in (0,1))
def crossing(a,b,c,d):
    q=(det(a,b,c),det(a,b,d),det(c,d,a),det(c,d,b))
    if q[0]*q[1]<0 and q[2]*q[3]<0: return True
    return between(c,a,b) or between(d,a,b) or between(a,c,d) or between(b,c,d)
def validate_simple(p):
    assert len(p)==len(set(p))>=3
    assert signed_area(p)
    n=len(p)
    assert all(det(p[i-1],p[i],p[(i+1)%n]) for i in range(n))
    for i,j in combinations(range(n),2):
        if j-i not in (1,n-1):
            assert not crossing(p[i],p[(i+1)%n],p[j],p[(j+1)%n])

def ears(c,points):
    """Standard exact closed-triangle ear exclusion on a simple polygon."""
    todo=c[:] if signed_area([points[i] for i in c])>0 else c[::-1]
    tris=[]
    while len(todo)>3:
        for pos in range(len(todo)):
            tri=(todo[pos-1],todo[pos],todo[(pos+1)%len(todo)])
            a,b,d=(points[x] for x in tri)
            if det(a,b,d)<=0: continue
            if any(all(det(u,v,points[x])>=0 for u,v in boundary([a,b,d]))
                   for x in todo if x not in tri): continue
            tris.append(tri); todo.pop(pos); break
        else: raise AssertionError('no valid ear')
    tris.append(tuple(todo))
    assert len(tris)==len(c)-2
    assert all(det(*(points[i] for i in t))>0 for t in tris)
    assert sum(det(*(points[i] for i in t)) for t in tris)==abs(signed_area([points[i] for i in c]))
    return tris

def clip(subject,triangle):
    """Closed convex polygon intersection via exact half-plane clipping."""
    p=list(subject)
    for a,b in boundary(list(triangle)):
        q=[]
        for u,v in boundary(p):
            su,sv=det(a,b,u),det(a,b,v)
            if su>=0: q.append(u)
            if su*sv<0:
                q.append(tuple((su*v[k]-sv*u[k])/(su-sv) for k in range(2)))
        p=q
        if not p: break
    return set(p)

def triangle_cut(tri,plane_origin,plane_normal,axis):
    """Convex triangle's full intersection interval with another plane.

    The coordinate inner(axis,p) is injective on the two-plane line.
    All extremes are either on-plane vertices or exact crossed-edge points.
    """
    dist=[inner(plane_normal,minus(p,plane_origin)) for p in tri]
    assert any(dist), 'coplanar planes handled separately'
    values=[inner(axis,p) for p,s in zip(tri,dist) if s==0]
    for i,j in ((0,1),(1,2),(2,0)):
        a,b=dist[i],dist[j]
        if a*b<0:
            p=tuple((a*tri[j][k]-b*tri[i][k])/(a-b) for k in range(3))
            values.append(inner(axis,p))
    return (min(values),max(values)) if values else None

def cross_triangle(a,b):
    axis=vector(normal(a),normal(b)); assert any(axis)
    x=triangle_cut(a,b[0],normal(b),axis)
    y=triangle_cut(b,a[0],normal(a),axis)
    if x is None or y is None: return None,axis
    lo,hi=max(x[0],y[0]),min(x[1],y[1])
    return ((lo,hi) if lo<=hi else None),axis

def orient_and_topology(cycles):
    ed=defaultdict(list)
    for i,c in enumerate(cycles):
        for a,b in boundary(c): ed[tuple(sorted((a,b)))].append((i,1 if a<b else -1))
    assert all(len(v)==2 for v in ed.values())
    orientations={0:1}; todo=[0]
    while todo:
        i=todo.pop()
        for a,b in boundary(cycles[i]):
            uses=ed[tuple(sorted((a,b)))]; first,second=uses
            (j,sj),(k,sk)=first,second
            if j!=i: j,k,sj,sk=k,j,sk,sj
            needed=-orientations[i]*sj*sk
            if k in orientations: assert orientations[k]==needed
            else: orientations[k]=needed; todo.append(k)
    assert len(orientations)==len(cycles)
    vertices=set().union(*(set(c) for c in cycles))
    link_lengths=[]
    for v in vertices:
        links=[]
        for c in cycles:
            if v in c:
                i=c.index(v); links.append(tuple(sorted((c[i-1],c[(i+1)%len(c)]))))
        assert len(links)==len(set(links))
        graph=defaultdict(set)
        for a,b in links: graph[a].add(b); graph[b].add(a)
        assert all(len(n)==2 for n in graph.values())
        reached={next(iter(graph))}; frontier=list(reached)
        while frontier:
            u=frontier.pop()
            for w in graph[u]-reached: reached.add(w);frontier.append(w)
        assert len(reached)==len(graph)
        link_lengths.append(len(graph))
    return ed,[orientations[i] for i in range(len(cycles))],link_lengths

def verify(vertices=V,cycles=C):
    assert len(vertices)==len(set(vertices))==24 and len(cycles)==8
    planes=[]; projections=[]; triangles=[]; face_of=[]; reflex=[]
    for fi,c in enumerate(cycles):
        assert len(c)==len(set(c))==9 and all(0<=i<24 for i in c)
        poly=[vertices[i] for i in c]; n=normal(poly)
        assert any(n) and all(inner(n,minus(p,poly[0]))==0 for p in poly)
        planes.append((poly[0],n))
        # Any nonzero normal coordinate yields an injective affine projection.
        drop=next(i for i in range(3) if n[i])
        proj={i:tuple(vertices[i][k] for k in range(3) if k!=drop) for i in c}
        polygon=[proj[i] for i in c]; validate_simple(polygon)
        area=signed_area(polygon)
        reflex.append(sum(det(polygon[i-1],polygon[i],polygon[(i+1)%9])*area<0 for i in range(9)))
        projections.append(proj)
        ts=ears(c,proj); triangles.extend(ts); face_of.extend([fi]*len(ts))
    edge_incidence,orientation,links=orient_and_topology(cycles)
    assert len(edge_incidence)==36 and links==[3]*24
    tri_edges,tri_orient,tri_links=orient_and_topology([list(t) for t in triangles])
    assert len(triangles)==56 and len(tri_edges)==84
    counts=Counter(); contacts=Counter()
    for i,j in combinations(range(56),2):
        a,b=triangles[i],triangles[j]; shared=set(a)&set(b)
        assert len(shared)<=2
        if face_of[i]==face_of[j]:
            proj=projections[face_of[i]]
            actual=clip([proj[x] for x in a],[proj[x] for x in b])
            expected={proj[x] for x in shared}
            assert expected<=actual
            if len(expected)<2: assert actual==expected
            else:
                u,v=tuple(expected); assert all(between(p,u,v) for p in actual)
            counts['coplanar_triangle_pairs']+=1
        else:
            actual,axis=cross_triangle([vertices[x] for x in a],[vertices[x] for x in b])
            vals=[inner(axis,vertices[x]) for x in shared]
            expected=(min(vals),max(vals)) if vals else None
            assert actual==expected, ('unintended triangle contact',i,j,actual,expected)
            counts['noncoplanar_triangle_pairs']+=1
        contacts[len(shared)]+=1
    pairs=[]
    for i,j in combinations(range(8),2):
        assert any(vector(planes[i][1],planes[j][1]))
        ei={tuple(sorted(e)) for e in boundary(cycles[i])}
        ej={tuple(sorted(e)) for e in boundary(cycles[j])}
        common=sorted(ei&ej); assert len(common) in (1,2)
        assert (set(cycles[i])&set(cycles[j]))==set().union(*(set(e) for e in common))
        if len(common)==2:
            assert not (set(common[0])&set(common[1]))
            u,v=common[0]; r,s=common[1]
            assert not any(vector(minus(vertices[v],vertices[u]),minus(vertices[r],vertices[u])))
            assert not any(vector(minus(vertices[v],vertices[u]),minus(vertices[s],vertices[u])))
        pairs.append({'faces':[i+1,j+1],'edges':[[a+1,b+1] for a,b in common]})
    mult=Counter(len(x['edges']) for x in pairs); assert mult=={1:20,2:8}
    # Exact signed solid volume from consistently oriented triangles, independent
    # sanity check; orientation choice can change its sign.
    volume=sum(tri_orient[i]*inner(vertices[t[0]],vector(vertices[t[1]],vertices[t[2]]))/6
               for i,t in enumerate(triangles))
    assert volume
    return dict(status='PASS',arithmetic='Fraction',vertices=24,polygon_edges=36,faces=8,
                triangles=56,triangulated_edges=84,euler_characteristic=-4,genus=3,
                original_orientation=orientation,original_link_lengths=links,
                triangulated_link_lengths=tri_links,reflex_corners=reflex,
                pair_counts=dict(counts),triangle_contact_counts=dict(contacts),
                pair_multiplicities=dict(mult),face_pair_edges=pairs,
                absolute_volume=str(abs(volume)),triangles_by_vertex=[[v+1 for v in t] for t in triangles])

def controls():
    checks=[]
    def reject(name,fn):
        try: fn()
        except AssertionError: checks.append(name)
        else: raise AssertionError('negative control accepted: '+name)
    reject('bow-tie polygon rejected',lambda:validate_simple([(F(0),F(0)),(F(2),F(2)),(F(0),F(2)),(F(2),F(0))]))
    reject('nonzero-area self-crossing rejected',lambda:validate_simple([(F(0),F(0)),(F(3),F(2)),(F(0),F(2)),(F(2),F(0))]))
    bad=V.copy();bad[0]=(V[0][0]+1,*V[0][1:])
    reject('coordinate mutation rejected',lambda:verify(bad))
    badc=[c[:] for c in C];badc[0][2],badc[0][4]=badc[0][4],badc[0][2]
    reject('face cycle mutation rejected',lambda:verify(V,badc))
    a=[tuple(map(F,p)) for p in ((0,0,0),(2,0,0),(0,2,0))]
    for name,b,expect in [
        ('transverse interval',[(0,1,-1),(0,1,1),(2,1,0)],'segment'),
        ('tangent point',[(0,0,0),(0,-1,1),(-1,0,1)],'point'),
        ('shared full edge',[(0,0,0),(2,0,0),(0,0,2)],'segment'),
        ('separated triangles',[(3,0,-1),(3,0,1),(3,2,0)],'empty')]:
        actual,_=cross_triangle(a,[tuple(map(F,p)) for p in b])
        kind='empty' if actual is None else ('point' if actual[0]==actual[1] else 'segment')
        assert kind==expect;checks.append(name)
    transformed=[(2*x+3*y-z+17,x-2*y+4*z-23,3*x+y+2*z+11) for x,y,z in V]
    # Matrix determinant is 7, so this is an invertible affine transformation.
    base=verify();affine=verify(transformed)
    determinant=inner((2,3,-1),vector((1,-2,4),(3,1,2)))
    assert determinant and F(affine['absolute_volume'])==abs(determinant)*F(base['absolute_volume'])
    checks.append('invertible affine transformation preserves all contacts and scales volume')
    modified=[(c[k:]+c[:k])[::(-1 if i%2 else 1)] for i,c in enumerate(C) for k in [i%9]]
    verify(V,modified[::-1]);checks.append('face permutation, cyclic shifts, and reversals preserve certificate')
    return checks

if __name__=='__main__':
    if not __debug__: raise RuntimeError('assertions required')
    root=pathlib.Path(__file__).resolve().parent.parent
    source=(root/'author/verify_witness.py').read_text()
    # Compare only literal data, without executing or importing the author code.
    literals={node.targets[0].id:ast.literal_eval(node.value) for node in ast.parse(source).body
              if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name)
              and node.targets[0].id in ('VERTICES','FACES')}
    assert literals['VERTICES']==[tuple(map(int,v)) for v in V]
    assert literals['FACES']==[[v+1 for v in c] for c in C]
    result=verify();result['independent_controls']=controls();result['source_data_match']=True
    result['author_manifest_sha256']=hashlib.sha256((root/'author/AUTHOR_MANIFEST.json').read_bytes()).hexdigest()
    print(json.dumps(result,indent=2))
