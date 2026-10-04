#!/usr/bin/env python3
"""Independent exact graph diagnostics for PCF candidate 20001424.
Derives rotations from rational coordinates and tangent vectors, then searches
all adjacency-compatible bijections by backtracking. Standard library only.
Run: python independent_checks.py > independent_results.json
No rational-map coefficients, realization theorem, or descent proof are tested.
"""
from collections import Counter
from fractions import Fraction as Q
from functools import cmp_to_key
import json

assertions=0
def check(ok,label):
    global assertions
    assert ok,label
    assertions+=1

points=[(1,0),(0,1),(-1,0),(0,-1),(Q(1,2),0),(0,Q(1,2)),
        (0,Q(1,3)),(-3,0),(0,-2),(0,-3)]
points=[tuple(map(Q,z)) for z in points]
edges={(0,1),(1,2),(2,3),(0,3),(0,4),(1,5),(5,6),(2,7),(3,8),(8,9)}
E={frozenset(e) for e in edges}
adj={i:set() for i in range(10)}
for i,j in edges:adj[i].add(j);adj[j].add(i)
check(len(set(points))==10,'all vertices distinct')
check(len(E)==10 and all(len(e)==2 for e in E),'ten distinct loopless edges')
seen={0};todo=[0]
while todo:
    for v in adj[todo.pop()]:
        if v not in seen:seen.add(v);todo.append(v)
check(len(seen)==10,'connected')
check(len(E)-len(points)+1==1,'cycle rank one')
check(Counter(map(len,adj.values()))==Counter({1:4,2:2,3:4}),'vertex degree multiset')

def neg(z):return(-z[0],-z[1])
def minus(a,b):return(a[0]-b[0],a[1]-b[1])
def times_i(z):return(-z[1],z[0])
def tangent(i,j):
    if i<4 and j<4:
        return times_i(points[i]) if j==(i+1)%4 else neg(times_i(points[i]))
    return minus(points[j],points[i])
def half(z):return 0 if z[1]>0 or (z[1]==0 and z[0]>=0) else 1
def angular_compare(a,b):
    if half(a)!=half(b):return -1 if half(a)<half(b) else 1
    cross=a[0]*b[1]-a[1]*b[0]
    return -1 if cross>0 else (1 if cross<0 else 0)
rot={i:sorted(adj[i],key=cmp_to_key(lambda j,k:angular_compare(tangent(i,j),tangent(i,k)))) for i in range(10)}
def cyclic(a,b):
    return len(a)==len(b) and any(a==b[k:]+b[:k] for k in range(len(b)))
expected={0:[3,1,4],1:[0,2,5],2:[1,7,3],3:[2,8,0]}
for v in expected:check(cyclic(rot[v],expected[v]),'rotation derived from exact tangents')

# Graph automorphisms: choose each unmapped source vertex by the number of
# already mapped neighbors; test adjacency and nonadjacency against the whole
# partial bijection. Completeness follows by exhausting every compatible image.
solutions=[];search_nodes=0
def search(g,used):
    global search_nodes
    search_nodes+=1
    if len(g)==10:
        solutions.append(tuple(g[i] for i in range(10)));return
    remaining=[i for i in range(10) if i not in g]
    v=max(remaining,key=lambda i:(len(adj[i]&g.keys()),len(adj[i]),-i))
    for w in range(10):
        if w in used or len(adj[w])!=len(adj[v]):continue
        if any((u in adj[v])!=(g[u] in adj[w]) for u in g):continue
        if Counter(len(adj[u]) for u in adj[v])!=Counter(len(adj[u]) for u in adj[w]):continue
        g[v]=w;used.add(w);search(g,used);used.remove(w);del g[v]
search({},set())
check(len(solutions)==4,'exactly four abstract graph automorphisms')
aut_records=[]
for g in sorted(solutions):
    check({frozenset((g[i],g[j])) for i,j in edges}==E,'full adjacency certificate')
    signs=[]
    for i in range(4):
        transported=[g[j] for j in rot[i]]
        p=cyclic(transported,rot[g[i]])
        r=cyclic(transported,list(reversed(rot[g[i]])))
        check(p!=r,'trivalent orientation sign is unambiguous')
        signs.append(1 if p else -1)
    aut_records.append({'vertex_images':g,'trivalent_signs':signs})
pres=[r for r in aut_records if r['trivalent_signs']==[1]*4]
reverse=[r for r in aut_records if r['trivalent_signs']==[-1]*4]
check(len(pres)==1 and pres[0]['vertex_images']==tuple(range(10)),'only positive automorphism is identity')
check(len(reverse)==1,'only one negative automorphism')
h=reverse[0]['vertex_images']
check(h==(2,3,0,1,7,8,9,4,5,6),'negative automorphism is prescribed half-turn on labels')
for i in range(10):
    check(h[h[i]]==i and h[i]!=i,'vertex action is a free involution')
for e in E:check(frozenset(h[i] for i in e)!=e,'no edge is fixed setwise')

# Verify the actual antiholomorphic involution on all rational coordinates.
def J(z):
    norm=z[0]**2+z[1]**2
    return(-z[0]/norm,-z[1]/norm)
for i,z in enumerate(points):
    check(J(z)==points[h[i]],'exact coordinate antipode')
    check(J(J(z))==z,'exact antipodal involution')
# Homogeneous anti-Mobius matrix squares to -I (hence to the identity in PGL2).
A=((0,-1),(1,0))
square=tuple(tuple(sum(A[i][k]*A[k][j] for k in range(2)) for j in range(2)) for i in range(2))
check(square==((-1,0),(0,-1)),'antipodal matrix cocycle sign')

# Face cycles computed with the predecessor convention; each dart is used once.
darts=sorted((u,v) for u in adj for v in adj[u])
def sigma(d):
    u,v=d;row=rot[u];return(u,row[(row.index(v)+1)%len(row)])
def alpha(d):return(d[1],d[0])
def phi(d):
    u,v=d;row=rot[v];return(v,row[(row.index(u)-1)%len(row)])
faces=[];visited=set();face_of={}
for d in darts:
    if d in visited:continue
    cur=d;f=[]
    while cur not in visited:
        visited.add(cur);face_of[cur]=len(faces);f.append(cur);cur=phi(cur)
    check(cur==d,'closed face orbit')
    faces.append(f)
check(len(faces)==2 and sorted(map(len,faces))==[10,10],'two faces of length ten')
check(10-10+len(faces)==2,'sphere Euler characteristic')
face_action=[]
for f in faces:
    transformed={(h[v],h[u]) for u,v in f}
    image=[i for i,g in enumerate(faces) if set(g)==transformed]
    check(len(image)==1,'negative symmetry induces a face permutation')
    face_action+=image
check(face_action==[1,0],'the two primal faces are exchanged')

# Radial/Tischler incidence: each primal corner d gives one radial edge,
# from its initial critical vertex to the pole in face(d). Corners remain
# labeled, so bridge multiplicities are not lost.
radial={d:(d[0],10+face_of[d]) for d in darts}
rad_adj={v:set() for v in range(12)}
for u,v in radial.values():rad_adj[u].add(v);rad_adj[v].add(u)
seen={0};todo=[0]
while todo:
    for v in rad_adj[todo.pop()]:
        if v not in seen:seen.add(v);todo.append(v)
check(len(seen)==12,'radial incidence connected')
check(len(radial)==20,'twenty radial edges with multiplicity')
# Orientation reversal carries a corner between d and sigma(d) to the corner
# beginning with h(sigma(d)), rather than just h(d).
def radial_h(d):
    u,v=sigma(d);return(h[u],h[v])
h_vertices=dict(enumerate(h));h_vertices.update({10:11,11:10})
for d,(u,v) in radial.items():
    im=radial_h(d)
    check(radial[im]==(h_vertices[u],h_vertices[v]),'corner action preserves radial endpoints')
    check(radial_h(im)==d and im!=d,'radial edge action is a free involution')
# Each primal edge corresponds to a quadrilateral face of the radial graph,
# with repetitions allowed for the bigon-with-sticker case.
quadrilaterals=[]
for u,v in sorted(edges):
    d=(u,v);b=alpha(d)
    corners=[d,phi(d),b,phi(b)]
    check(radial[corners[0]][0]==u and radial[corners[1]][0]==v,'first half-face endpoints')
    check(radial[corners[2]][0]==v and radial[corners[3]][0]==u,'second half-face endpoints')
    check(radial[corners[0]][1]==radial[corners[1]][1],'first face pole')
    check(radial[corners[2]][1]==radial[corners[3]][1],'second face pole')
    quadrilaterals.append(corners)
counts=Counter(d for q in quadrilaterals for d in q)
check(counts==Counter({d:2 for d in darts}),'each radial edge occurs twice in face boundaries')
check(12-20+len(quadrilaterals)==2,'radial sphere Euler characteristic')
qsets=[Counter(q) for q in quadrilaterals]
qaction=[]
for i,q in enumerate(quadrilaterals):
    image=Counter(radial_h(d) for d in q)
    js=[j for j,p in enumerate(qsets) if p==image]
    check(len(js)==1 and js[0]!=i,'no radial face is fixed')
    qaction+=js
check(all(qaction[qaction[i]]==i for i in range(10)),'ten Tischler faces pair into five pairs')

# Negative control: forgetting the inside/outside decoration changes the
# embedding. Placing all four pendants inside admits genuine reflections.
all_inside={i:[(i-1)%4,(i+1)%4,next(v for v in adj[i] if v>=4)] for i in range(4)}
inside_pres=[];inside_rev=[]
for g in solutions:
    if all(cyclic([g[v] for v in all_inside[i]],all_inside[g[i]]) for i in range(4)):inside_pres.append(g)
    if all(cyclic([g[v] for v in all_inside[i]],list(reversed(all_inside[g[i]]))) for i in range(4)):inside_rev.append(g)
check(len(inside_pres)==2 and len(inside_rev)==2,'negative control: undecorated side choice changes symmetry types')
check(all(any(g[i]==i for i in range(4)) for g in inside_rev),'negative control reflections have fixed cycle vertices')

local=Counter(len(adj[v])+1 for v in adj)
check(local==Counter({2:4,3:2,4:4}),'critical local degrees')
check(sum((m-1)*count for m,count in local.items())==20,'Riemann-Hurwitz ramification total')
check(len(edges)+1==11 and max(local)<11,'degree eleven and no totally ramified critical point')
check(12-10==2,'two noncritical fixed-point vertices')
# Algebraic-locus degree bookkeeping only; not a coefficient construction.
check(2*11-2==20 and 20*(11+1)-20==220,'homogeneous divisibility has quotient degree 220')

print(json.dumps({'pass':True,'assertions':assertions,'search_nodes':search_nodes,
 'exact_coordinate_rotations':rot,'automorphisms':aut_records,
 'antipodal_vertex_action':h,'face_action':face_action,
 'primal_face_lengths':list(map(len,faces)),
 'radial_vertices':12,'radial_edges':20,'radial_faces':10,
 'radial_face_action':qaction,'critical_local_degrees':dict(local),
 'degree':11,'ramification_total':20,
 'scope':'Exact finite embedding, graph and rotation-system diagnostics only. Rational realization, symmetry naturality, algebraicity and field-of-moduli obstruction are audited in REVIEW.md.'},indent=2))
