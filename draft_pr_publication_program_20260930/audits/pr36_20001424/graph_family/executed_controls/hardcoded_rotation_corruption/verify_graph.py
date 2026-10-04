#!/usr/bin/env python3
"""Exhaustive finite graph/rotation-system checks; not a dynamics theorem proof."""
from itertools import permutations,product
from collections import Counter,defaultdict
import json

# Four-cycle; pendant path lengths 1,2,1,2. North at roots0,1; south2,3.
roots=list(range(4)); edges=[(0,1),(1,2),(2,3),(3,0)]
paths={0:[4],1:[5,6],2:[7],3:[8,9]}
for v,path in paths.items():
    prev=v
    for w in path:edges.append((prev,w));prev=w
E={frozenset(e) for e in edges};V=list(range(10));adj={v:set() for v in V}
for u,v in edges:adj[u].add(v);adj[v].add(u)
rot={}
for i in roots:
    prev,next_,pend=(i-1)%4,(i+1)%4,paths[i][0]
    rot[i]=[prev,next_,pend] if i<3 else [prev,pend,next_]
for v in V:
    if v not in rot:rot[v]=sorted(adj[v])
assert len(E)==10 and len(V)==10
assert sorted(map(len,adj.values()))==[1,1,1,1,2,2,3,3,3,3]

def cyclic(a,b):
    return len(a)==len(b) and any(a==b[k:]+b[:k] for k in range(len(b)))
def signs(g):
    s=[]
    for v in roots:
        mapped=[g[w] for w in rot[v]];target=rot[g[v]]
        if cyclic(mapped,target):s.append(1)
        elif cyclic(mapped,list(reversed(target))):s.append(-1)
        else:raise AssertionError('invalid cyclic order')
    return s

# Exhaust all permutations within degree classes: 4!*2!*4!=1152 possibilities.
classes=[[v for v in V if len(adj[v])==d] for d in (1,2,3)]
autos=[];tested=0
for images in product(*(list(permutations(c)) for c in classes)):
    g={v:w for c,im in zip(classes,images) for v,w in zip(c,im)}
    tested+=1
    if {frozenset((g[u],g[v])) for u,v in edges}==E:
        autos.append(g)
assert tested==1152 and len(autos)==4
pres=[g for g in autos if signs(g)==[1]*4]
rev=[g for g in autos if signs(g)==[-1]*4]
assert len(pres)==len(rev)==1
assert all(pres[0][v]==v for v in V)
h=rev[0]
assert [h[i] for i in roots]==[2,3,0,1]
assert all(h[v]!=v and h[h[v]]==v for v in V)
assert all(frozenset((h[u],h[v]))!=frozenset((u,v)) for u,v in edges)

# Face boundary cycles of the orientable rotation system.
darts=[(u,v) for u,v in edges]+[(v,u) for u,v in edges]
def successor(d):
    u,v=d;row=rot[v]
    return (v,row[(row.index(u)+1)%len(row)])
seen=set();faces=[]
for d in darts:
    if d in seen:continue
    cur=d;face=[]
    while cur not in seen:
        seen.add(cur);face.append(cur);cur=successor(cur)
    assert cur==d
    faces.append(face)
assert len(faces)==2 and len(V)-len(E)+len(faces)==2
# Reversal transports directed face boundary with endpoint reversal.
face_sets=[set(f) for f in faces]
for i,f in enumerate(faces):
    mirrored={(h[v],h[u]) for u,v in f}
    assert mirrored==face_sets[1-i]

# Radial/Tischler incidence has a vertex for each charge vertex and each face.
# Every corner contributes one ray; bridge incidences retain multiplicity.
radial_edges=[]
for i,f in enumerate(faces):
    radial_edges += [(u,10+i) for u,v in f]
assert len(radial_edges)==20
radial_counts=Counter(radial_edges)
h2=dict(h);h2.update({10:11,11:10})
assert Counter((h2[u],h2[v]) for u,v in radial_edges)==radial_counts
assert all(h2[v]!=v for v in range(12))
assert all(frozenset((h2[u],h2[v]))!=frozenset((u,v)) for u,v in radial_edges)
radj=defaultdict(set)
for u,v in radial_edges:radj[u].add(v);radj[v].add(u)
reach={0};todo=[0]
while todo:
    for v in radj[todo.pop()]:
        if v not in reach:reach.add(v);todo.append(v)
assert len(reach)==12

local=Counter(len(adj[v])+1 for v in V)
assert local==Counter({2:4,3:2,4:4})
assert sum((d-1)*n for d,n in local.items())==20==2*11-2
print(json.dumps({'pass':True,'vertices':len(V),'edges':len(E),'faces':len(faces),
 'candidate_degree':11,'permutations_checked':tested,'abstract_automorphisms':len(autos),
 'orientation_preserving_automorphisms':len(pres),'orientation_reversing_automorphisms':len(rev),
 'automorphisms':[{'vertex_images':[g[v] for v in V],'root_orientation_signs':signs(g)} for g in autos],
 'antipodal_vertex_images':[h[v] for v in V],'face_boundary_lengths':[len(f) for f in faces],
 'rotation_system':rot,'edges_list':edges,'face_boundaries':faces,
 'radial_vertices':12,'radial_edges_with_multiplicity':20,'radial_connected':True,
 'critical_local_degrees':dict(local),'ramification_total':20,'postcritical_cardinality':10,
 'scope':'Finite graph and rotation-system verification only. Rational realization, naturality, algebraicity, and field-of-moduli obstruction require the written proof.'},indent=2))
